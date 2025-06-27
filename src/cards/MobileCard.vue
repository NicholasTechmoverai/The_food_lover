<template>
    <div class="flex relative justify-center items-center w-full max-w-[400px] h-full -mb-12">
        <img :src="mobile_image" alt="mobile design frame" class="w-full z-50 h-full object-cover pointer-events-none select-none" />
        <div class="absolute scrollit  inset-0 px-2 pt-8 md:pt-8 lg:pt-8 overflow-y-auto mt-[5%] left-[7%] w-[86%] bg-amber-200/80 flex flex-col  items-center text-gray-900">
            <h3 class="text-2xl font-bold mb-3 font-display sticky top-0">{{ card.title }}</h3>
            <div ref="descriptionContainer" class="description-container">
                <p ref="descriptionElement" class="description-display">
                    {{ animatedDescription }}
                </p>
            </div>
            <ul class="w-full space-y-4 px-4 mt-4">
                <li v-for="(feature, index) in card.features" :key="index" class="flex items-start gap-3">
                    <div class="text-xl mt-0.5 text-primary-300">
                        <i :class="feature.icon"></i>
                    </div>
                    <div>
                        <span class="text-base font-medium block">{{ feature.title }}</span>
                        <span class="text-sm opacity-80">{{ feature.description }}</span>
                    </div>
                </li>
            </ul>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import mobile_image from "../assets/topphone.png"
import { useSiteStore } from '../config/siteConfig.js'

const { siteConfig, getResponsiveValue } = useSiteStore()
const card = {
  title: siteConfig.servicesOffred.title,
  description: siteConfig.servicesOffred.description,
  features: siteConfig.servicesOffred.features
}

const descriptionElement = ref(null)
const descriptionContainer = ref(null)
const animatedDescription = ref('')
let typingInterval = null
let restartTimeout = null
const MAX_LINES = 3
const TYPING_SPEED = 30 // milliseconds per character
const RESTART_DELAY = 3000 // 3 seconds before restart

const typeDescription = (newText) => {
  // Clear any existing animations and timeouts
  clearInterval(typingInterval)
  clearTimeout(restartTimeout)
  
  // Reset state
  animatedDescription.value = ''
  
  // Reset scroll position
  if (descriptionContainer.value) {
    descriptionContainer.value.scrollTop = 0
  }

  // Don't proceed if no text
  if (!newText) return

  let charIndex = 0
  
  typingInterval = setInterval(() => {
    if (charIndex < newText.length) {
      const nextChar = newText.charAt(charIndex)
      animatedDescription.value += nextChar
      charIndex++

      // Update lines buffer and manage overflow
      updateLinesBuffer(animatedDescription.value)

      // Scroll to bottom
      if (descriptionContainer.value) {
        descriptionContainer.value.scrollTop = descriptionContainer.value.scrollHeight
      }
    } else {
      clearInterval(typingInterval)
      // Schedule restart after completion
      scheduleRestart()
    }
  }, TYPING_SPEED)
}

const scheduleRestart = () => {
  clearTimeout(restartTimeout)
  restartTimeout = setTimeout(() => {
    typeDescription(card.description)
  }, RESTART_DELAY)
}

const updateLinesBuffer = (text) => {
  if (!descriptionElement.value) return

  // Use a temporary element to measure lines
  const tempEl = descriptionElement.value.cloneNode()
  tempEl.style.visibility = 'hidden'
  tempEl.style.position = 'absolute'
  tempEl.style.width = getComputedStyle(descriptionElement.value).width
  tempEl.textContent = text
  document.body.appendChild(tempEl)

  const lineHeight = parseInt(getComputedStyle(tempEl).lineHeight)
  const height = tempEl.clientHeight
  const lineCount = Math.round(height / lineHeight)

  document.body.removeChild(tempEl)

  // Manage line buffer
  if (lineCount > MAX_LINES) {
    // Find the last newline before we exceed MAX_LINES
    let cutoffIndex = 0
    let currentLines = 0
    for (let i = 0; i < text.length; i++) {
      if (text[i] === '\n') currentLines++
      if (currentLines >= lineCount - MAX_LINES) {
        cutoffIndex = i + 1
        break
      }
    }
    animatedDescription.value = text.substring(cutoffIndex)
  }
}

// Watch for changes in description
watch(() => card.description, (newDesc) => {
  typeDescription(newDesc)
})

// Initialize on mount
onMounted(() => {
  typeDescription(card.description)
})

// Clean up on unmount
onBeforeUnmount(() => {
  clearInterval(typingInterval)
  clearTimeout(restartTimeout)
})
</script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&family=Space+Grotesk:wght@500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Savate&display=swap');

.font-display {
    font-family: "Savate", sans-serif;
    font-weight: 600;
    font-style: normal;
    color: #1f2937;
    text-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.description-container {
    width: 80%;
    min-height: 70px !important;
    /* 3 lines * 1.5 line-height */
    height: 70px !important;
    /* 3 lines * 1.5 line-height */
    overflow-y: auto;
    scroll-behavior: smooth;
    margin-bottom: 0.5rem;
}

.description-display {
    font-family: "Poppins", sans-serif;
    font-weight: 400;
    font-size: 16px;
    line-height: 1.5;
    white-space: pre-wrap;
    margin: 0;
    padding: 0;
}

/* Custom scrollbar */
.description-container::-webkit-scrollbar {
    width: 4px;
}
.scrolll,
.description-container::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.05);
}
.scrolll,
.description-container::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 2px;
}

.scrollit::-webkit-scrollbar {
    width: 2px;
}

.scrollit::-webkit-scrollbar-thumb {
    background-color: rgba(168, 6, 217, 0.3);
    border-radius: 3px;
}

.scrollit::-webkit-scrollbar-track {
    background-color: rgba(54, 54, 52, 0.877);
    border-radius: 3px;
}

body {
    font-family: 'Poppins', sans-serif;
}
</style>