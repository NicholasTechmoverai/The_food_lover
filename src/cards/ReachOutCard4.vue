<template>
  <div
    class="p-8 md:p-12 relative overflow-hidden rounded-3xl"
    :style="{ backgroundColor: `${siteConfig.colors.secondary}15` }"
  >
    <!-- Header (unchanged) -->
    <div class="text-center mb-12 relative z-10">
      <h2
        :style="{ fontFamily: siteConfig.welcomeMessage.fontFamily }"
        class="text-5xl font-extrabold font-cursive drop-shadow-sm text-purple-700 font-serif animate-text-gradient"
      >
        {{ siteConfig.reachOut.title }}
      </h2>
      <p class="text-gray-300 mt-4 max-w-2xl mx-auto">
        {{ siteConfig.reachOut.note }}
      </p>
    </div>

    <!-- Card Grid -->
    <ul class="grid gap-8 sm:grid-cols-2 lg:grid-cols-3 relative z-10">
      <li
        v-for="tool in siteConfig.reachOut.tools"
        :key="tool.name"
        class="group relative"
      >
        <div
          class="h-full flex flex-col rounded-2xl overflow-hidden backdrop-blur-md transition-all duration-300 shadow-lg"
          :style="{
            background: `linear-gradient(135deg, ${siteConfig.colors.primary}10, ${siteConfig.colors.secondary}30)`,
            border: `1px solid ${siteConfig.colors.primary}30`
          }"
        >
          <!-- Card Header -->
          <div class="p-6 pb-0 flex items-center gap-4">
            <div
              class="flex items-center justify-center w-12 h-12 rounded-xl"
              :style="{
                background: `linear-gradient(135deg, ${siteConfig.colors.primary}10, ${siteConfig.colors.secondary}20)`,
                border: `1px solid ${siteConfig.colors.primary}20`
              }"
            >
              <i :class="[tool.icon, 'text-xl']" :style="{ color: siteConfig.colors.secondary }" />
            </div>
            <h3
              class="text-lg font-semibold text-gray-700 dark:text-gray-300"
            >
              {{ tool.name }}
            </h3>
          </div>

          <!-- Card Body -->
          <div class="p-6 pt-4 flex-grow">
            <p
              class="text-sm leading-relaxed"
              :style="{ color: siteConfig.colors.text.secondary }"
            >
              {{ tool.description }}
            </p>
          </div>

          <!-- Card Footer -->
          <div class="px-6 pb-6 pt-2" v-if="tool.link">
            <a
              :href="tool.link"
              class="inline-flex items-center gap-1 text-sm font-medium transition-all hover:underline"
              :style="{ color: siteConfig.colors.secondary }"
            >
              <span>Get Started</span>
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
                :stroke="siteConfig.colors.secondary" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </a>
          </div>
        </div>

        <!-- Subtle Hover Glow -->
        <div
          class="absolute inset-0 rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none"
          :style="{
            boxShadow: `0 10px 50px ${siteConfig.colors.secondary}40`
          }"
        />
      </li>
    </ul>
  </div>
</template>

<script setup>
import { useSiteStore } from '../config/siteConfig.js'

const { siteConfig } = useSiteStore()
</script>
