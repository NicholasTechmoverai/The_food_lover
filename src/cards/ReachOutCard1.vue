<template>
  <div class="flex flex-col w-full bg-gradient-to-br p-4 from-white to-gray-100 shadow-xl relative overflow-hidden">
    
    <!-- Header (Title + Note) -->
    <div class="mb-10 text-center w-full md:text-left relative z-20 bg-white/20 backdrop-blur-sm rounded-lg p-6 shadow-lg">
      <h2 class="text-4xl md:text-5xl font-cursive drop-shadow-sm font-extrabold text-purple-700 leading-tight tracking-tight relative inline-block">
        {{ siteConfig.reachOut.title }}
        <span class="block h-1 w-24 mt-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mx-auto md:mx-0"></span>
      </h2>
      <p class="text-gray-300 text-base md:text-lg mt-4 max-w-3xl mx-auto md:mx-0 leading-relaxed">
        {{ siteConfig.reachOut.note }}
      </p>
    </div>

    <!-- Video Background (Window Effect) -->
    <div class="absolute inset-0 w-full h-full overflow-hidden z-0">
      <video 
        autoplay loop muted playsinline
        class="absolute top-0 left-0 w-full h-full object-cover"
      >
        <source :src="design_video" type="video/mp4">
        <!-- Fallback image if video doesn't load -->
        <img :src="design_image" alt="Background" class="absolute top-0 left-0 w-full h-full object-cover">
      </video>
      <div class="absolute inset-0 bg-black/20 backdrop-blur-[1px]"></div>
    </div>

    <!-- Grid of Feature Cards with Window Effect -->
    <ul class="relative z-10 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      <li
        v-for="tool in siteConfig.reachOut.tools"
        :key="tool.name"
        class="bg-white/20 backdrop-blur-lg border border-white/30 hover:border-blue-300/100 hover:scale-102 rounded-xl p-6 shadow-lg hover:shadow-xl transition-all duration-300 group overflow-hidden"
      >
        <!-- Card Cutout Effect -->
        <div class=" absolute inset-0 bg-black/10 rounded-xl border-4 border-white/20 mix-blend-overlay"></div>
        
        <div class="relative z-10 flex items-start gap-4">
          <!-- Icon Block -->
          <div class="p-3 rounded-xl bg-white/80 backdrop-blur-sm group-hover:bg-white transition-all shadow-sm">
            <i :class="[tool.icon, 'text-xl md:text-2xl text-gradient bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600 transition-colors']"></i>
          </div>

          <!-- Text Block -->
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-white drop-shadow-md">
              {{ tool.name }}
            </h3>
            <p class="text-sm text-white/90 mt-1 leading-relaxed drop-shadow-md">
              {{ tool.description }}
            </p>

            <!-- Optional CTA Link -->
            <a
              v-if="tool.link"
              :href="tool.link"
              class="inline-flex items-center mt-3 text-sm font-medium text-white hover:text-blue-200 transition-colors"
            >
              Get started
              <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </a>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { useSiteStore } from '../config/siteConfig.js'

const { siteConfig, getResponsiveValue } = useSiteStore()
const design_video = siteConfig.reachOut.video || '../assets/3255109-uhd_3840_2160_25fps.mp4';
const design_image = siteConfig.reachOut.image || '../assets/chips1.jpg';
</script>

<style>
/* Custom gradient text class */
.text-gradient {
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* Smooth transitions for all interactive elements */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

/* Enhance the glass morphism effect */
.backdrop-blur-lg {
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
}
</style>