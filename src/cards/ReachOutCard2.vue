<template>
  <div class="bg-gradient-to-br flex flex-col w-full from-white via-gray-400 to-purple-500 p-8 md:p-12 shadow-x">

    <!-- Header (Title + Note) -->
    <div class="mb-10 text-center w-full md:text-left z-20">
      <h2 class="text-4xl md:text-5xl font-cursive drop-shadow-sm font-extrabold text-purple-700 leading-tight tracking-tight relative inline-block">
        {{ siteConfig.reachOut.title }}
        <span
          class="block h-1 w-24 mt-2 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full mx-auto md:mx-0"></span>
      </h2>
      <p class="text-gray-600 text-base md:text-lg mt-4 max-w-3xl mx-auto md:mx-0 leading-relaxed">
        {{ siteConfig.reachOut.note }}
      </p>
    </div>

    <!-- Grid Background Container -->
    <div class="relative w-full isolate rounded-xl overflow-hidden p-2">

      <!-- 🔹 Background Cooking VIDEO -->
      <video autoplay muted loop playsinline
        class="absolute inset-0 w-full h-full object-cover opacity-100 brightness-50 z-0">
        <source :src="design_video" type="video/mp4" />
        <img :src="design_image" alt="Background" class="absolute top-0 left-0 w-full h-full object-cover">

        Your browser does not support the video tag.
      </video>

      <!-- 🔸 Optional dark overlay for more contrast -->
      <div class="absolute inset-0 bg-black/0 z-0"></div>

      <!-- Grid Content Layer -->
      <ul class="relative z-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <li v-for="tool in siteConfig.reachOut.tools" :key="tool.name"
          class="bg-white/30 backdrop-blur-xl border border-white/40 hover:border-blue-300 rounded-2xl p-6 shadow-lg hover:shadow-xl  hover:scale-105 transition-all duration-400 group">
          <div class="flex items-start gap-4">
            <!-- Icon Block -->
            <div
              class="p-3 rounded-xl bg-gradient-to-br from-blue-100/40 to-purple-100/40 group-hover:from-blue-200/60 group-hover:to-purple-200/60 transition">
              <i
                :class="[tool.icon, 'text-xl md:text-2xl text-blue-600 group-hover:text-purple-600 transition-colors']"></i>
            </div>

            <!-- Text Block -->
            <div class="flex-1">
              <h3 class="text-lg font-semibold text-gray-800 group-hover:text-blue-700">
                {{ tool.name }}
              </h3>
              <p class="text-sm text-gray-200 mt-1 leading-relaxed">
                {{ tool.description }}
              </p>

              <!-- Optional CTA -->
              <a v-if="tool.link" :href="tool.link"
                class="inline-flex items-center mt-3 text-sm text-blue-600 hover:text-purple-600 font-medium transition-colors">
                Get started
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </a>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { siteConfig } from '../config/siteConfig.js'
const design_video = siteConfig.reachOut.video || '../assets/3255109-uhd_3840_2160_25fps.mp4';
const design_image = siteConfig.reachOut.image || '../assets/chips1.jpg';
</script>
