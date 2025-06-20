<template>
  <div class="wave-container">
    <svg 
      id="visual" 
      :viewBox="`0 0 ${width} ${height}`" 
      :width="width" 
      :height="height" 
      xmlns="http://www.w3.org/2000/svg"
      preserveAspectRatio="none"
    >
      <!-- Background gradient for depth -->
      <defs>
        <linearGradient id="waveGradient" x1="0" x2="0" y1="0" y2="1">
          <stop offset="0%" stop-color="var(--top-color)" />
          <stop offset="100%" stop-color="var(--bottom-color)" />
        </linearGradient>
      </defs>
      
      <!-- Wave layers with individual gradients -->
      <g v-for="(wave, index) in computedWaves" :key="`wave-${index}`">
        <defs>
          <linearGradient :id="`waveGradient${index}`" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" :stop-color="wave.color" stop-opacity="0.8" />
            <stop offset="100%" :stop-color="wave.color" stop-opacity="0.2" />
          </linearGradient>
        </defs>
        <path 
          :d="generateWavePath(wave, index)" 
          :fill="`url(#waveGradient${index})`"
          :style="getWaveStyle(index)"
          :opacity="wave.opacity"
        />
      </g>
    </svg>
  </div>
</template>

<script>
export default {
  name: 'AnimatedWave',
  props: {
    width: {
      type: Number,
      default: 900
    },
    height: {
      type: Number,
      default: 300
    },
    waveCount: {
      type: Number,
      default: 5,
      validator: value => value >= 1 && value <= 10
    },
    speed: {
      type: Number,
      default: 0.05,
      validator: value => value > 0 && value <= 0.2
    },
    amplitude: {
      type: Number,
      default: 20,
      validator: value => value >= 1 && value <= 50
    },
    colors: {
      type: Array,
      default: () => ['#4facfe', '#00f2fe', '#4facfe', '#00f2fe', '#4facfe']
    },
    depthIntensity: {
      type: Number,
      default: 0.8,
      validator: value => value >= 0 && value <= 1
    }
  },
  data() {
    return {
      offset: 0,
      animationId: null,
      waveConfig: [
        { amplitudeFactor: 1.2, speedFactor: 1.1, segments: 24, density: 0.9 },
        { amplitudeFactor: 0.9, speedFactor: 0.9, segments: 22, density: 0.8 },
        { amplitudeFactor: 0.7, speedFactor: 0.8, segments: 20, density: 0.7 },
        { amplitudeFactor: 0.5, speedFactor: 0.7, segments: 18, density: 0.6 },
        { amplitudeFactor: 0.3, speedFactor: 0.6, segments: 16, density: 0.5 }
      ]
    }
  },
  computed: {
    computedWaves() {
      return Array.from({ length: this.waveCount }, (_, i) => ({
        color: this.colors[i % this.colors.length],
        opacity: 1 - (i * (0.15 * this.depthIntensity)),
        ...this.waveConfig[i % this.waveConfig.length],
        waveHeight: this.height * (0.6 + (i * 0.05))
      }));
    },
    waveVariables() {
      return {
        '--top-color': this.colors[0],
        '--bottom-color': this.colors[this.colors.length - 1]
      }
    }
  },
  mounted() {
    this.startAnimation();
  },
  beforeDestroy() {
    this.stopAnimation();
  },
  methods: {
 generateWavePath(wave, waveIndex) {
  const segmentCount = wave.segments;
  const segmentWidth = this.width / segmentCount;
  const baseHeight = wave.waveHeight;
  const densityFactor = wave.density;
  
  let path = `M0 ${baseHeight}`;
  
  for (let i = 0; i <= segmentCount; i++) {
    const x = i * segmentWidth;
    const progress = i / segmentCount;
    const dynamicOffset = this.offset * wave.speedFactor;
    
    const noise = Math.sin(progress * Math.PI * 6 + dynamicOffset * 2) * 2;
    const y = baseHeight + 
             (Math.sin(progress * Math.PI * 2 + dynamicOffset) * 
             this.amplitude * wave.amplitudeFactor * 0.6) +
             (Math.sin(progress * Math.PI * 4 + dynamicOffset * 1.3) * 
             this.amplitude * wave.amplitudeFactor * 0.3 * densityFactor) +
             (noise * densityFactor * 0.5);
    
    if (i === 0) {
      path += `L${x} ${y}`;
    } else {
      const prevX = (i - 1) * segmentWidth;
      const prevProgress = (i - 1) / segmentCount;
      const prevNoise = Math.sin(prevProgress * Math.PI * 6 + dynamicOffset * 2) * 2;
      const prevY = baseHeight + 
                   (Math.sin(prevProgress * Math.PI * 2 + dynamicOffset) * 
                   this.amplitude * wave.amplitudeFactor * 0.6) +
                   (Math.sin(prevProgress * Math.PI * 4 + dynamicOffset * 1.3) * 
                   this.amplitude * wave.amplitudeFactor * 0.3 * densityFactor) +
                   (prevNoise * densityFactor * 0.5);
      
      const cp1x = prevX + segmentWidth * 0.4;
      const cp1y = prevY + (y - prevY) * 0.3;
      const cp2x = x - segmentWidth * 0.4;
      const cp2y = y - (y - prevY) * 0.3;
      
      path += `C${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${x} ${y}`;
    }
  }
  
  // Fix for diagonal line - create proper bottom closure
  // First go straight down from last wave point
  path += `L${this.width} ${baseHeight}`;
  
  // Then go to bottom right corner
  path += `L${this.width} ${this.height}`;
  
  // Then to bottom left corner
  path += `L0 ${this.height}`;
  
  // Then back up to starting point
  path += `L0 ${baseHeight}`;
  
  // Close the path
  path += 'Z';
  
  return path;
},
    getWaveStyle(index) {
      return {
        transition: `all ${0.3 + index * 0.05}s cubic-bezier(0.4, 0, 0.2, 1)`,
        transform: `translateY(${index * -3}px)`,
        willChange: 'transform',
        'mix-blend-mode': index === 0 ? 'normal' : 'multiply'
      };
    },
    startAnimation() {
      const animate = () => {
        this.offset += this.speed;
        this.animationId = requestAnimationFrame(animate);
      };
      animate();
    },
    stopAnimation() {
      if (this.animationId) {
        cancelAnimationFrame(this.animationId);
      }
    }
  }
}
</script>

<style scoped>
.wave-container {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
  background: linear-gradient(
    to bottom, 
    var(--top-color) 0%, 
    var(--bottom-color) 100%
  );
}

.wave-container svg {
  display: block;
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

path {
  transition: all 0.3s ease-out;
}
</style>