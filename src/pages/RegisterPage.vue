<template>
  <div class="grid grid-cols-1 md:grid-cols-2 h-fit ">
    
    <!-- Left: Horizontally Scrollable Card Column -->
    <div class="hidden md:flex flex-col items-center justify-center bg-gray-50 dark:bg-gray-800 h-full w-full overflow-hidden">
      <h4 @click="router.push('/')" class="mb-4 cursor-pointer text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-purple-300 to-gray-200 dark:from-yellow-400 dark:to-gray-100"
          style="font-family: 'Caprasimo', sans-serif;">
        {{ siteConfig.meta.siteName }}
      </h4>

      <div class="relative w-[500px] h-[600px] overflow-hidden ">
        <div
          ref="scrollContainer"
          class="absolute inset-0 flex overflow-hidden snap-x snap-mandatory px-4 py-6 gap-4 scroll-smooth scrollbar-thin scrollbar-thumb-gray-400 dark:scrollbar-thumb-gray-600"
        >
          <div
            v-for="(card, index) in cards"
            :key="index"
            :ref="el => cardRefs[index] = el"
            class="flex-shrink-0 w-[500px] h-full snap-start"
          >
            <component :is="card" class=" " />
          </div>
        </div>
      </div>
    </div>

    <!-- Right: Dynamic View -->
    <div class="  bg-white dark:bg-gray-800 overflow-y-auto h-full border-l border-gray-200 dark:border-gray-700">
            <h4 @click="router.push('/')" class="absolute md:hidden right-1/2 mb-4 cursor-pointer text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-purple-300 to-gray-200 dark:from-yellow-400 dark:to-gray-100"
          style="font-family: 'Caprasimo', sans-serif;">
        {{ siteConfig.meta.siteName }}
      </h4>
      <router-view />
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

const cards = [TiltedRecipeCard, DishCard ,StepperPage ] 
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
