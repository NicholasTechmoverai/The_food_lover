<template>
  <div class="grid grid-cols-1 md:grid-cols-2  overflow-hidden bg-white dark:bg-gray-900">

    <!-- Left Pane: Scrollable Card Section (Desktop Only) -->
    <div class="hidden md:flex flex-col items-center justify-center px-6 py-8 bg-gray-50 dark:bg-gray-800">
      <!-- Site Title -->
      <h1 @click="router.push('/')" class="text-4xl font-extrabold cursor-pointer text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-purple-300 to-gray-200 dark:from-yellow-400 dark:to-gray-100 mb-6" style="font-family: 'Caprasimo', sans-serif;">
        {{ siteConfig.meta.siteName }}
      </h1>

      <!-- Scrollable Card Container -->
      <div class="relative w-[500px] h-[600px] overflow-hidden rounded-2xl ">
        <div
          ref="scrollContainer"
          class="absolute inset-0 flex snap-x snap-mandatory gap-6 scroll-smooth px-4 py-6 overflow-hidden"
        >
          <div
            v-for="(card, index) in cards"
            :key="index"
            :ref="el => cardRefs[index] = el"
            class="flex-shrink-0 w-[500px] h-full snap-start rounded-xl overflow-hidden transition-transform hover:scale-[1.02]"
          >
            <component :is="card" />
          </div>
        </div>
      </div>

      <!-- Footer -->
      <footer class="mt-8 text-sm text-gray-500 dark:text-gray-400">
        &copy; 2025 All rights reserved. <a href="/terms" class="underline hover:text-gray-700 dark:hover:text-white">Terms & Conditions</a>
      </footer>
    </div>

    <!-- Right Pane: Dynamic View / Mobile View -->
    <div class="relative h-full w-full overflow-y-auto border-l border-gray-200 dark:border-gray-700">
      <!-- Mobile Site Title -->
      <h1
        @click="router.push('/')"
        class="md:hidden sticky top-0 z-10 bg-white dark:bg-gray-800 px-4 py-3 text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-purple-300 to-gray-200 dark:from-yellow-400 dark:to-gray-100 shadow"
        style="font-family: 'Caprasimo', sans-serif;"
      >
        {{ siteConfig.meta.siteName }}
      </h1>

      <!-- Route Content -->
      <router-view class="px-4 py-6" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import TiltedRecipeCard from '../cards/TiltedRecipeCard.vue'
import DishCard from '../cards/DishCard.vue'
import { useControl } from '../store/control.js'
import { useSiteStore } from '../config/siteConfig.js'
import StepperPage from '../cards/StepperPage.vue'
import Clock from '../cards/Clock.vue'
import router from '../router/index.js'
const { siteConfig, getResponsiveValue } = useSiteStore()
const control = useControl()

const scrollContainer = ref(null)
const cardRefs = ref([])

const cards = [TiltedRecipeCard, DishCard, StepperPage]
const currentCard = ref(0)
let interval

const scrollByOneCard = (direction = 'right') => {
  const container = scrollContainer.value
  if (!container || cardRefs.value.length === 0) return

  const cardWidth = cardRefs.value[0].offsetWidth || 500
  const scrollAmount = direction === 'right' ? cardWidth : -cardWidth

  const maxScrollLeft = container.scrollWidth - container.clientWidth

  // Update index
  if (direction === 'right') {
    currentCard.value = (currentCard.value + 1) % cards.length
  } else {
    currentCard.value =
      (currentCard.value - 1 + cards.length) % cards.length
  }

  // Scroll by card width, or reset if we're at the edge
  if (
    (direction === 'right' && container.scrollLeft + cardWidth >= maxScrollLeft) ||
    (direction === 'left' && container.scrollLeft <= 0)
  ) {
    // Wrap around
    container.scrollTo({
      left: direction === 'right' ? 0 : maxScrollLeft,
      behavior: 'smooth'
    })
  } else {
    container.scrollBy({
      left: scrollAmount,
      behavior: 'smooth'
    })
  }
}


// Auto-scroll every 5 seconds
onMounted(() => {
  control.setShowNav(false)
  interval = setInterval(() => {
    scrollByOneCard('right')
  }, 5000)
})

onUnmounted(() => {
  clearInterval(interval)
  control.setShowNav(true)
})
</script>
