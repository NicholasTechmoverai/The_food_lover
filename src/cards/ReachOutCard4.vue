<template>
  <div class="bg-[#0f0f1a] p-10 md:p-14 rounded-2xl border border-[#1f1f3a] shadow-2xl relative overflow-hidden">
    <!-- Header -->
    <div class="text-center mb-12 relative z-10">
      <h2 class="text-4xl font-bold font-cursive drop-shadow-sm text-purple-700 tracking-widest">
        {{ siteConfig.reachOut.title }}
      </h2>
      <p class="text-gray-300 mt-4 max-w-2xl mx-auto">
        {{ siteConfig.reachOut.note }}
      </p>
    </div>

    <!-- Card Grid -->
    <ul class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 relative z-10">
      <li
        v-for="tool in siteConfig.reachOut.tools"
        :key="tool.name"
        class="group bg-[#1a1a2e] border border-purple-600/40 hover:border-purple-400 rounded-xl p-6 shadow-lg hover:shadow-purple-500/30 transition-all duration-300 relative"
      >
        <div class="absolute -inset-1 bg-gradient-to-r from-purple-600 to-blue-600 opacity-20 blur-xl rounded-xl group-hover:opacity-40 transition-all duration-500"></div>
        <div class="relative flex items-start gap-4">
          <div class="bg-purple-800/30 p-3 rounded-lg">
            <i :class="[tool.icon, 'text-xl text-purple-300']"></i>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-white">{{ tool.name }}</h3>
            <p class="text-sm text-purple-200 mt-1">
              {{ tool.description }}
            </p>
            <a
              v-if="tool.link"
              :href="tool.link"
              class="inline-flex mt-3 text-sm text-purple-400 hover:underline"
            >
              Access →
            </a>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { siteConfig } from '../config/siteConfig.js';
</script>
