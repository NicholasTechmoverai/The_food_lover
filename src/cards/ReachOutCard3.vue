<template>
  <div class="bg-gradient-to-br from-white to-gray-50 p-8 px-2 md:p-12  shadow-xl relative overflow-hidden">
    <!-- Background Image (for text clipping) -->
    <div class="absolute inset-0 overflow-hidden z-0">
      <img 
        :src="design_image" 
        alt="Background texture"
        class="w-full h-full object-cover opacity-20"
      />
      <div class="absolute inset-0 bg-gradient-to-br from-white/10 to-gray-400/50 backdrop-blur-[2px]"></div>
    </div>

    <!-- Header -->
    <div class="relative mb-10 z-10">
      <h2 class="text-4xl md:text-5xl font-cursive drop-shadow-sm font-extrabold text-purple-700 leading-tight tracking-tight">
        {{ siteConfig.reachOut.title }}
        <span class="block h-1 w-24 mt-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full"></span>
      </h2>
      <p class="text-gray-600 text-base md:text-lg mt-4 max-w-3xl leading-relaxed">
        {{ siteConfig.reachOut.note }}
      </p>
    </div>

    <!-- Grid of Features with Text Window Effect -->
    <ul class="grid gap-4 sm:grid-cols-2 lg:grid-cols-3 relative z-10">
      <li
        v-for="tool in siteConfig.reachOut.tools"
        :key="tool.name"
        class="bg-white/80 backdrop-blur-md border border-gray-200/70 hover:border-blue-400 hover:scale-105 hover:bg-purple-500/30 rounded-xl p-6 shadow-md hover:shadow-lg transition-all duration-300 group"
      >
        <div class="flex items-start gap-4">
          <!-- Icon -->
          <div class="p-3 rounded-xl bg-gradient-to-br from-blue-100 to-purple-100 group-hover:from-blue-200 group-hover:to-purple-200 transition">
            <i :class="[tool.icon, 'text-xl md:text-2xl text-blue-600 group-hover:text-purple-600 transition-colors']"></i>
          </div>

          <!-- Text Content with Window Effect -->
          <div class="flex-1 text-window">
            <h3 class="text-lg font-semibold text-gray-800 group-hover:text-blue-700 mb-1">
              {{ tool.name }}
            </h3>
            <p class="text-sm text-gray-600 leading-relaxed">
              {{ tool.description }}
            </p>

            <!-- CTA -->
            <a
              v-if="tool.link"
              :href="tool.link"
              class="inline-flex items-center mt-3 text-sm text-blue-600 hover:text-purple-600 font-medium transition-colors"
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
const design_image = siteConfig.reachOut.image || '../assets/chips1.jpg';
</script>

<style scoped>
/* Text Window Effect */
.text-window h3,
.text-window p {
  position: relative;
  display: inline-block;
  background-image: url('../assets/chips1.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  text-shadow: 0 0 8px rgba(255,255,255,0.3);
}

/* Fallback for browsers that don't support background-clip:text */
@supports not (background-clip: text) {
  .text-window h3,
  .text-window p {
    color: inherit;
    background-image: none;
    text-shadow: none;
  }
}

/* Enhanced glass effect */
.backdrop-blur-md {
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}

/* Smooth transitions */
.transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 300ms;
}

/* Hover effects */
.group:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.1);
}
</style>