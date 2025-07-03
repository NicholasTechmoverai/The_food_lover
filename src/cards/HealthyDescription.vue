<template>
  <div class="max-w[600px] w-[90%] mx-auto mt-10 bg-gradient-to-br from-green-50 via-emerald-100 to-lime-50 rounded-3xl shadow-xl p-6 border border-green-200">
    <!-- Header with PrimeVue icon -->
    <div class="flex items-center gap-3 mb-4">
      <i class="pi pi-heart-fill text-green-600 text-6xl"></i>
      <h2 :style="{ fontFamily: siteConfig.welcomeMessage.fontFamily }" class="text-5xl font-extrabold  font-cursive drop-shadow-sm text-purple-700 font-serif animate-text-gradient">{{ healthyCard.title }}</h2>
    </div>

    <!-- Benefit Points -->
    <ul :style="{ color: siteConfig.colors.text.secondary }"  class="text-purple-500 text-md space-y-3 font-light">
      <li v-for="(point, index) in healthyCard.points" :key="index" class="flex items-start gap-2">
        <i class="pi pi-check-circle text-purple-600 pt-1"></i>
        <span>{{ point }}</span>
      </li>
    </ul>

    <!-- Note -->
    <p class="mt-6 text-sm text-purple-700 italic font-mono flex items-center gap-2">
      <i class="pi pi-info-circle text-purple-500"></i>
      {{ healthyCard.note }}
    </p>
  </div>
</template>

<script setup>
import { useSiteStore } from '../config/siteConfig.js'

const { siteConfig, getResponsiveValue } = useSiteStore()

const healthyCard = {
  title: 'Healthy Tips!Healthy Meals, stay Healthy!',
  points: [
    'Boosts your energy levels naturally',
    'Strengthens your immune system over time',
    'Supports long-term heart & brain health',
  ],
  note: 'A nourished body is a strong body — start with your plate!',
};
</script>
