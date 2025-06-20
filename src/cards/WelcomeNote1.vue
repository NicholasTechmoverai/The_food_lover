<template>
  <div class="relative flex min-h-[50vh] bg-transparent  w-full items-center justify-center overflow-hidden">
        <!-- Enhanced Video Background -->
        <div class="absolute inset-0 z-0">
            <video autoplay loop muted playsinline class="h-full w-full object-cover">
                <source :src="welcomeMessage.video" type="video/mp4">

            </video>
            <!-- Fallback image with subtle animation -->
            <img :src="welcomeMessage.image" alt="Kitchen background"
                class="h-full w-full object-cover transition-opacity duration-1000" :class="{ 'opacity-0': !videoError }"
                @error="videoError = true">
            <div
                class="absolute inset-0 bg-gradient-to-r from-gray-900/30 via-gray-900/10 to-gray-900/40 backdrop-blur-[1px]">
            </div>
        </div>


    <!-- Content Card -->
    <div class="relative z-10 max-w-4xl w-full mx-auto px-4 mt-3 mb-3 bg-transparent">
      <div class="rounded-3xl bg-grar-100/30 backdrop-blur-md shadow-xl p-8 md:p-12 border border-white/50">
        <!-- Title -->
        <h1 :style="{ fontFamily: welcomeMessage.fontFamily }"
          class="text-4xl md:text-6xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-purple-700 to-amber-600 drop-shadow-md text-center">
          {{ welcomeMessage.note || 'Welcome to our website!' }}
        </h1>

        <!-- Author -->
        <p class="mt-4 text-center text-lg text-gray-800">
          Brought to you by
          <span class="font-semibold text-purple-900">
            {{ siteConfig.author }}
          </span>
        </p>

        <!-- Social Icons -->
        <div v-if="siteConfig.social.links.length" class="mt-6 flex justify-center gap-4 flex-wrap">
          <a v-for="link in siteConfig.social.links" :key="link.name" :href="link.url" target="_blank"
            rel="noopener noreferrer"
            class="text-gray-700 hover:text-purple-600 border border-gray-400/50 hover:border-purple-500 transition-colors duration-300 p-2 rounded-lg shadow-sm"
            :aria-label="link.name">
            <i :class="[link.icon, 'text-xl']"></i>
          </a>
        </div>

        <!-- Search Bar Component -->
        <div class="mt-10 max-w-lg mx-auto w-full">
          <component :is="SearchBar" />
        </div>

        <!-- Share Text -->
        <p v-if="siteConfig.social.shareText" class="mt-6 text-sm text-gray-700 text-center">
          {{ siteConfig.social.shareText }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { siteConfig } from '../config/siteConfig.js'
import { computed } from 'vue'
import SearchBar1 from '../searchbar/SearchBar1.vue'
import SearchBar2 from '../searchbar/SearchBar2.vue'
import SearchBar3 from '../searchbar/SearchBar3.vue'
import SearchBar4 from '../searchbar/SearchBar4.vue'

const SearchBar = computed(() => {
  const searchBars = {
    1: SearchBar1,
    2: SearchBar2,
    3: SearchBar3,
    4: SearchBar4
  }
  return searchBars[siteConfig.components.searchBar] || SearchBar1
})

const welcomeMessage = siteConfig.welcomeMessage
</script>
