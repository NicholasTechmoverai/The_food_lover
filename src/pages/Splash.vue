<template>
  <!-- Background Layer -->
  <div 
    class="fixed inset-0 z-0 transition-opacity duration-1000"
    :class="{'opacity-100': backgroundLoaded, 'opacity-0': !backgroundLoaded}"
    :style="backgroundStyle"
  >
    <img
      v-if="backgroundImageUrl"
      class="w-full h-full object-cover"
      :src="backgroundImageUrl"
      :alt="siteConfig.background.image.alt"
      @load="handleBackgroundLoad"
      @error="handleBackgroundError"
    />
  </div>

  <!-- Main Content Container -->
  <div 
    class="fixed inset-0 flex items-center justify-center overflow-hidden bg-gray-600/70"
  >
    <!-- Animated Waves -->
    <AnimatedWave 
      v-if="siteConfig.wave.enabled && !isLoading"
      class="wave-animation"
      :class="{ 'mobile-adjustment': isMobile }"
      :wave-count="siteConfig.wave.count"
      :speed="siteConfig.wave.speed"
      :amplitude="adjustedAmplitude"
      :width="adjustedWidth"
      :height="adjustedHeight"
      :depth-intensity="siteConfig.wave.depthIntensity"
      :colors="siteConfig.wave.colors"
      :style="waveStyle"
    />
    
    <!-- Site Logo -->
    <img 
      class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 transition-all duration-700 z-10"
      :class="{ 'logo-mobile': isMobile, 'logo-desktop': !isMobile }"
      :src="siteConfig.assets.logo" 
      :alt="siteConfig.assets.logoAlt"
      :style="logoStyle"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue';
import AnimatedWave from './components/AnimatedWave.vue';
import { siteConfig, getResponsiveValue } from './config/siteConfig.js';

// Reactive state
const isMobile = ref(window.innerWidth < 768);
const isLoading = ref(true);
const waveOffset = ref(0);
const scrollY = ref(0);
const backgroundLoaded = ref(false);
const backgroundError = ref(false);

// Computed properties
const backgroundImageUrl = computed(() => {
  if (!siteConfig.background?.image) return null;
  return isMobile.value 
    ? siteConfig.background.image.mobile 
    : siteConfig.background.image.desktop;
});

const backgroundStyle = computed(() => ({
  opacity: siteConfig.background.image.opacity,
  filter: `brightness(${siteConfig.background.image.brightness || 1})`
}));

const adjustedAmplitude = computed(() => 
  getResponsiveValue(siteConfig.wave.amplitude, isMobile.value)
);

const adjustedWidth = computed(() => 
  isMobile.value ? window.innerWidth : siteConfig.wave.dimensions.width
);

const adjustedHeight = computed(() => {
  const baseHeight = isMobile.value 
    ? siteConfig.wave.dimensions.height * siteConfig.wave.dimensions.mobileHeightRatio
    : siteConfig.wave.dimensions.height;
  return Math.min(baseHeight, window.innerHeight * 0.5);
});

const waveStyle = computed(() => ({
  marginBottom: isMobile.value ? '-20%' : '-10%',
  opacity: 1 - (scrollY.value / 500),
  mixBlendMode: siteConfig.wave.blendMode
}));

const logoStyle = computed(() => ({
  width: isMobile.value ? '70vw' : '40vw',
  maxWidth: siteConfig.assets.logoMaxWidth,
  filter: `drop-shadow(0 0 10px ${siteConfig.colors.logoShadow || 'rgba(0,0,0,0.3)'})`,
  opacity: 1 - (scrollY.value / 1000)
}));

// Methods
const handleBackgroundLoad = () => {
  backgroundLoaded.value = true;
  console.log('Background image loaded successfully');
};

const handleBackgroundError = () => {
  backgroundError.value = true;
  console.error('Background image failed to load');
};

const handleResize = () => {
  isMobile.value = window.innerWidth < 768;
};

const handleScroll = () => {
  scrollY.value = window.scrollY;
  waveOffset.value = scrollY.value * siteConfig.wave.parallaxIntensity;
};

// Lifecycle hooks
onMounted(() => {
  window.addEventListener('resize', handleResize);
  window.addEventListener('scroll', handleScroll);
  
  setTimeout(() => {
    isLoading.value = false;
  }, siteConfig.splash.minimumShowTime);
});

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize);
  window.removeEventListener('scroll', handleScroll);
});
</script>

<style scoped>
.wave-animation {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform, opacity;
}

.mobile-adjustment {
  transform: scaleY(0.8) translateY(10%);
}

.logo-mobile {
  width: 70vw;
  max-width: 300px;
}

.logo-desktop {
  width: 40vw;
  max-width: 600px;
}

@media (max-width: 768px) {
  .wave-animation {
    transform-origin: bottom center;
  }
}
</style>