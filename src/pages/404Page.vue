<template>
  <div class="min-h-screen bg-gray-400/70 flex flex-col items-center justify-center p-6 text-center">
    <!-- Illustration -->
    <div class="mb-8 w-48 h-48 md:w-64 md:h-64">
          <img :src="siteConfig.assets.logo" :alt="siteConfig.assets.logoAlt" class="w-full h-full object-contain" />

    </div>

    <!-- Title & Message -->
    <h1 class="text-4xl md:text-5xl font-bold text-amber-800 mb-4">404</h1>
    <h2 class="text-2xl md:text-3xl font-semibold text-amber-700 mb-6">
      Oops! Looks like this page got eaten...
    </h2>

    <!-- Navigation Links -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-8 w-full max-w-md">
      <RouterLink to="/"
        class="bg-amber-500 hover:bg-amber-600 text-white font-medium py-3 px-6 rounded-lg transition-all flex items-center justify-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path
            d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z" />
        </svg>
        Return Home
      </RouterLink>
      <RouterLink to="/recipes"
        class="bg-white hover:bg-gray-100 border-2 border-amber-500 text-amber-700 font-medium py-3 px-6 rounded-lg transition-all flex items-center justify-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
          <path fill-rule="evenodd"
            d="M6 3a1 1 0 011-1h.01a1 1 0 010 2H7a1 1 0 01-1-1zm2 3a1 1 0 00-2 0v1a2 2 0 00-2 2v1H5a1 1 0 000 2h1a1 1 0 100-2h1v-1a1 1 0 011-1h8a1 1 0 011 1v1h1a1 1 0 100 2h-1v1a1 1 0 11-2 0v-1a2 2 0 00-2-2V6a1 1 0 10-2 0v1H8V6z"
            clip-rule="evenodd" />
        </svg>
        Explore Recipes
      </RouterLink>
    </div>

    <!-- Search Bar -->
    <div class="w-full max-w-md mb-8">
      <div class="relative">
        <input type="text" placeholder="Find a recipe, ingredient, or restaurant..."
          class="w-full py-3 px-4 pr-12 rounded-lg border-2 border-amber-300 focus:border-amber-500 focus:ring-2 focus:ring-amber-200 outline-none transition-all">
        <button class="absolute right-2 top-1/2 transform -translate-y-1/2 text-amber-600 hover:text-amber-800">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Quote -->
    <p class="text-white italic max-w-md">
      "Life is uncertain. Eat dessert first." — Ernestine Ulmer
    </p>


  </div>
</template>

<script setup>
import { siteConfig } from '../config/siteConfig';
import { RouterLink } from 'vue-router';
</script>