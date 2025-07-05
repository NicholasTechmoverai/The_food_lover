<template>
  <div :style="{
    background: `linear-gradient(to bottom right, ${withAlpha(siteConfig.colors.secondary, '10')}, ${withAlpha(siteConfig.colors.primary, '20')})`
  }" class="min-h-screen py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">
      <!-- Header -->
      <div class="text-center mb-8">
        <h1 :style="{ fontFamily: siteConfig.welcomeMessage.fontFamily }"
          class="text-5xl font-extrabold text-purple-800 font-cursive drop-shadow-sm animate-text-gradient">
          {{ timely_headline }}
        </h1>
        <p :style="{ color: siteConfig.colors.text.secondary }" class="text-lg text-purple-600 italic mt-2">
          {{ timely_motto }}
        </p>
      </div>
      <!-- Stepper -->
      <div class="rounded-2xl overflow-hidden shadow-xl">
        <!-- Step Tabs -->
        <div class="flex border-b bg-white dark:bg-black/10">
          <div v-for="step in steps" :key="step.value" @click="goToStep(parseInt(step.value))" :class="[
            'flex-1 py-4 text-center cursor-pointer transition-all duration-300 flex flex-col items-center',
            activeStep === step.value
              ? 'font-bold text-white shadow-md'
              : 'text-gray-600 hover:text-gray-900'
          ]" :style="{
              backgroundColor: activeStep === step.value
                ? siteConfig.colors.primary
                : withAlpha(siteConfig.colors.secondary, '22')
            }">
            <span class="text-2xl mb-1">{{ getStepEmoji(step.value) }}</span>
            <span>{{ step.label }}</span>
          </div>
        </div>

        <!-- Step Panel -->
        <div :style="{ backgroundColor: withAlpha(siteConfig.colors.secondary, '08') }" class="p-6 relative">
          <div class="absolute -top-10 -right-10 text-6xl opacity-10">🍳</div>
          <div class="absolute bottom-2 left-4 text-5xl opacity-10">🥘</div>

          <div v-for="step in steps" :key="`panel-${step.value}`" v-show="activeStep === step.value"
            class="relative z-10">
            <!-- Instruction Card -->
            <div :style="{ backgroundColor: withAlpha(siteConfig.colors.primary, '15') }"
              class="rounded-xl p-6 shadow-md border border-dashed border-gray-300 backdrop-blur-md">
              <!-- Timer Badge -->
              <div :style="{ backgroundColor: siteConfig.colors.secondary }"
                class="absolute -top-6 -right-6 w-20 h-20 rounded-full flex flex-col items-center justify-center text-white shadow-lg border">
                <div class="text-xs absolute -top-3 bg-white text-black px-2 py-1 rounded-full">⏲️</div>
                <span class="text-2xl font-bold">{{ step.timer }}</span>
                <span class="text-xs">sec</span>
              </div>

              <!-- Speech Bubble -->
              <div
                class="bg-white/80 backdrop-blur-sm rounded-lg p-4 border-l-4 border-purple-400 relative max-w-[80%] mx-auto my-8">
                <p class="text-lg text-gray-800 font-comic">
                  {{ step.content }}
                </p>
                <div
                  class="absolute -bottom-3 left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-8 border-r-8 border-b-8 border-l-transparent border-r-transparent border-b-white">
                </div>
              </div>

              <!-- Progress Bar -->
              <div class="w-full h-2 bg-gray-200 rounded-full overflow-hidden">
                <div class="h-full rounded-full" :style="{
                  background: `linear-gradient(to right, ${siteConfig.colors.primary}, ${siteConfig.colors.secondary})`,
                  width: `${step.progress}%`
                }"></div>
              </div>
            </div>

            <!-- Navigation Buttons -->
            <div class="flex justify-between items-center mt-6">
              <button v-if="step.value !== '1'" @click="goToStep(parseInt(step.value) - 1)" :style="{
                background: `linear-gradient(to right, ${withAlpha(siteConfig.colors.primary, '10')}, ${withAlpha(siteConfig.colors.secondary, '33')})`
              }"
                class="flex items-center gap-2 px-6 py-3 text-gray-800 rounded-full shadow-sm transition-all duration-300 hover:shadow-md hover:-translate-x-1">
                👈 <span class="font-comic">Go Back</span>
              </button>

              <button v-if="step.value !== steps.length.toString()" @click="goToStep(parseInt(step.value) + 1)" :style="{
                background: `linear-gradient(to right, ${siteConfig.colors.secondary}, ${withAlpha(siteConfig.colors.primary, '99')})`
              }"
                class="flex items-center gap-2 px-6 py-3 text-white rounded-full shadow-lg transition-all duration-300 hover:shadow-xl hover:translate-x-1">
                <span class="font-comic">
                  {{ step.value === (steps.length - 1).toString() ? 'Finish 🎉' : 'Next 👉' }}
                </span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>



<style scoped>
@keyframes wobble {
  0% {
    transform: rotate(0deg);
  }

  25% {
    transform: rotate(1deg);
  }

  50% {
    transform: rotate(-1deg);
  }

  75% {
    transform: rotate(1deg);
  }

  100% {
    transform: rotate(0deg);
  }
}

.animate-wobble {
  animation: wobble 1s ease-in-out;
}
</style>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useSiteStore } from '../config/siteConfig.js'

const { siteConfig, getResponsiveValue } = useSiteStore()
const withAlpha = (hex, alpha = '99') => hex + alpha.replace('#', '')

// Step configuration with more playful content
const steps = ref([
  {
    value: '1',
    label: 'Prepare',
    content: 'Dump in 1 cup of water (try not to splash!) and wait for 15 seconds of anticipation',
    duration: 15,
    timer: 15,
    progress: 100
  },
  {
    value: '2',
    label: 'cook',
    content: 'Wave your spoon like a magic wand for 5 seconds (stirring optional but recommended)',
    duration: 5,
    timer: 5,
    progress: 100
  },
  {
    value: '3',
    label: 'serve',
    content: 'Plate it like a MasterChef contestant and admire for 20 seconds before devouring',
    duration: 20,
    timer: 20,
    progress: 100
  }
]);

const timely_headline = ref('Step-by-step Cooking Guide');
const timely_motto = ref('Let the timer lead you — one step at a time!');

const activeStep = ref('1');
let timerInterval = null;

// Get fun emoji for each step
const getStepEmoji = (stepValue) => {
  const emojis = ['🥄', '🔥', '🍽️'];
  return emojis[stepValue - 1] || '👨‍🍳';
};

// Auto-advance through steps
const startAutoAdvance = () => {
  timerInterval = setInterval(() => {
    const currentStep = steps.value.find(step => step.value === activeStep.value);

    if (currentStep) {
      currentStep.timer -= 1;
      currentStep.progress = (currentStep.timer / currentStep.duration) * 100;

      if (currentStep.timer <= 0) {
        const nextStepIndex = parseInt(activeStep.value);

        if (nextStepIndex < steps.value.length) {
          goToStep(nextStepIndex + 1);
        } else {
          resetAllTimers();
          goToStep(1);
        }
      }
    }
  }, 1000);
};

// Navigate to specific step
const goToStep = (stepNumber) => {
  activeStep.value = stepNumber.toString();
  resetAllTimers();
};

// Reset all timers
const resetAllTimers = () => {
  steps.value.forEach(step => {
    step.timer = step.duration;
    step.progress = 100;
  });
};

onMounted(() => {
  startAutoAdvance();
});

onBeforeUnmount(() => {
  if (timerInterval) {
    clearInterval(timerInterval);
  }
});
</script>

<style>
/* Custom animations */
@keyframes wobble {

  0%,
  100% {
    transform: rotate(0deg);
  }

  25% {
    transform: rotate(2deg);
  }

  50% {
    transform: rotate(-2deg);
  }

  75% {
    transform: rotate(1deg);
  }
}

.animate-wobble {
  animation: wobble 0.5s ease-in-out;
}

.font-comic {
  font-family: 'Comic Sans MS', 'Marker Felt', 'Comic Neue', cursive;
}
</style>