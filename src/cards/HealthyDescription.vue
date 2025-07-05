<template>
  <div
    class="max-w-[600px] w-[90%] mx-auto mt-10 rounded-3xl shadow-xl p-6 border"
    :style="{
      background: `linear-gradient(135deg, ${withAlpha(siteConfig.colors.primary, 0.01)}, ${withAlpha(siteConfig.colors.secondary, 0.4)})`,
      borderColor: withAlpha(siteConfig.colors.primary, 0.2),
    }"
  >
    <!-- Header (Untouched) -->
    <div class="flex items-center gap-3 mb-4">
      <i class="pi pi-heart-fill text-green-600 text-6xl"></i>
      <h2
        :style="{ fontFamily: siteConfig.welcomeMessage.fontFamily }"
        class="text-5xl font-extrabold font-cursive drop-shadow-sm text-purple-700 font-serif animate-text-gradient"
      >
        {{ healthyCard.title }}
      </h2>
    </div>

    <!-- Benefit Points -->
    <ul class="text-md space-y-4 font-light">
      <li
        v-for="(point, index) in healthyCard.points"
        :key="index"
        class="flex items-start gap-3 px-3 py-2 rounded-xl transition-all duration-200 hover:bg-white/50 hover:shadow-sm"
        :style="{
          color: siteConfig.colors.text.primary,
          backgroundColor: index % 2 === 0
            ? withAlpha(siteConfig.colors.secondary, 0.04)
            : withAlpha(siteConfig.colors.primary, 0.03),
        }"
      >
        <i class="pi pi-check-circle pt-1" :style="{ color: siteConfig.colors.accent }" />
        <span>{{ point }}</span>
      </li>
    </ul>

    <!-- Note -->
    <p
      class="mt-6 text-sm italic font-mono flex items-center gap-2"
      :style="{ color: siteConfig.colors.text.secondary }"
    >
      <i class="pi pi-info-circle" :style="{ color: siteConfig.colors.accent }" />
      {{ healthyCard.note }}
    </p>
  </div>
</template>

<script setup>
import { useSiteStore } from '../config/siteConfig.js'

const { siteConfig } = useSiteStore()

const healthyCard = {
  title: 'Healthy Tips!Healthy Meals, stay Healthy!',
  points: [
    'Boosts your energy levels naturally',
    'Strengthens your immune system over time',
    'Supports long-term heart & brain health',
  ],
  note: 'A nourished body is a strong body — start with your plate!',
}

// Helper: Add alpha to hex color
function withAlpha(hex, alpha = 1) {
  const r = parseInt(hex.slice(1, 3), 16)
  const g = parseInt(hex.slice(3, 5), 16)
  const b = parseInt(hex.slice(5, 7), 16)
  return `rgba(${r}, ${g}, ${b}, ${alpha})`
}
</script>
