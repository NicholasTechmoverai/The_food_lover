<template>
  <div class="slider-wrapper">
    <div
      class="slider"
      style="--width: 240px; --height: 280px; --quantity: 9"
    >
      <div class="list">
        <div
          v-for="(recipe, index) in loop_through"
          :key="index"
          class="item cursor-pointer"
          @click="opentype(recipe.title)"
          :style="`--i: ${index}`"
        >
          <div
            class="card flex flex-col items-center justify-center relative overflow-hidden"
          >
            <div class="gradient-bg" :style="`background: linear-gradient(to bottom right, ${recipe.gradient})`"></div>
            <img
              :src="recipe.image"
              :alt="recipe.title"
              class="w-24 h-24 rounded-full object-cover mb-4 border-2 border-white shadow-lg z-10"
            />
            <h3 class="text-lg font-bold text-white z-10 dark:text-gray-700">{{ recipe.title }}</h3>
            <p class="text-sm text-white/90  z-10 px-2">{{ recipe.description }}</p>
            <div class="absolute bottom-0 left-0 right-0 h-1 bg-white/30 z-10"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { polishUrlName } from '../reusables';
import router from '../router';

const props = defineProps({
  render:String,
  loop_through:{
    type: Object,
    required: true,
    default: () => ({})
  }
})

const opentype = (type) =>{
  router.push(`/${props.render}/${polishUrlName(type)}`)
}

</script>

<style scoped>
.slider-wrapper {
  padding: 2rem 0;
  position: relative;
}

.slider {
  width: 100%;
  height: var(--height);
  position: relative;
  overflow: hidden;
  mask-image: linear-gradient(
    to right,
    transparent,
    black 5%,
    black 95%,
    transparent
  );
  -webkit-mask-image: linear-gradient(
    to right,
    transparent,
    black 5%,
    black 95%,
    transparent
  );
}

.slider .list {
  display: flex;
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: calc(var(--width) * var(--quantity) * 2);
  animation: slide 30s linear infinite;
}

.slider:hover .list {
  animation-play-state: paused;
}

.card {
  width: calc(var(--width) - 20px);
  height: calc(var(--height) - 20px);
  margin: 0 10px;
  border-radius: 12px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
  position: relative;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-8px) scale(1.03);
}

.gradient-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

/* @keyframes slide {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(calc(var(--width) * var(--quantity) * -1));
  }
} */
@keyframes slide {
  0% {
    transform: translate3d(0, 0, 0);
  }
  100% {
    transform: translate3d(calc(var(--width) * var(--quantity) * -1), 0, 0);
  }
}
.item {
  width: var(--width);
  height: var(--height);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
}

@media (max-width: 768px) {
  .slider {
    mask-image: linear-gradient(
      to right,
      transparent,
      black 2%,
      black 98%,
      transparent
    );
    -webkit-mask-image: linear-gradient(
      to right,
      transparent,
      black 2%,
      black 98%,
      transparent
    );
  }
}
.slider[reverse="true"] .item {
  animation: reversePlay 10s linear infinite;
}
@keyframes reversePlay {
  from {
    left: calc(var(--width) * -1);
  }
  to {
    left: 100%;
  }
}


</style>

