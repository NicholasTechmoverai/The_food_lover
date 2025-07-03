<template>
  <div :style="{ backgroundColor: `${siteConfig.colors.primary}100` }"
    class="min-h-screen bg-gradient-to-br from-amber-100/90 to-yellow-50/0 py-12 px-4 sm:px-6 lg:px-8">
    <div class="max-w-3xl mx-auto">
      <!-- Header with animated emoji -->
      <div class="text-center mb-8">
        <h1 :style="{ fontFamily: siteConfig.welcomeMessage.fontFamily }"
          class="text-5xl font-extrabold text-purple-800 font-cursive drop-shadow-sm animate-text-gradient">
          {{ timely_headline }}
        </h1>
        <p :style="{ color: siteConfig.colors.text.secondary }" class="text-lg text-purple-600 italic mt-2">
          {{ timely_motto }}
        </p>
      </div>

      <!-- Stepper Container with fun shadow -->
      <div
        class=" rounded-2xl  overflow-hidden transform hover:scale-[1.01] transition-transform duration-300">
        <!-- Step Indicators - now tabs with emoji -->
        <div class="flex border-b-2 border-purple-100 bg-gradient-to-r from-purple-50 to-pink-50">
          <div v-for="step in steps" :key="step.value" @click="goToStep(parseInt(step.value))" :class="{
            'border-b-4 border-purple-500 text-purple-600 font-bold bg-white shadow-sm': activeStep === step.value,
            'text-gray-500 hover:text-pink-600 cursor-pointer': activeStep !== step.value
          }" class="flex-1 py-4 text-center transition-all duration-300 flex flex-col items-center"
            :style="activeStep === step.value ? { backgroundColor: siteConfig.colors.primary + '90' } : {}" >
          <span class="text-2xl mb-1">{{ getStepEmoji(step.value) }}</span>
          <span>{{ step.label }}</span>
        </div>
      </div>

      <!-- Step Content with floating elements -->
      <div :style="{ backgroundColor: `${siteConfig.colors.secondary}60` }"
        class="p-6 bg-white relative overflow-hidden">
        <!-- Floating food elements -->
        <div class="absolute -top-10 -right-10 text-6xl opacity-10">🍳</div>
        <div class="absolute bottom-2 left-4 text-5xl opacity-10">🥘</div>

        <div v-for="step in steps" :key="`panel-${step.value}`" v-show="activeStep === step.value"
          class="relative z-10">
          <!-- Instruction Card with wobbly effect -->
          <div
          :style="{ backgroundColor: `${siteConfig.colors.primary}85` }"
            class="relative bg-gradient-to-br from-amber-50/10 to-yellow-100/30 rounded-xl p-8 border-2 border-dashed border-amber-300 mb-8 min-h-[200px] shadow-inner hover:animate-wobble">
            <!-- Timer as a chef hat -->
            <div
              class="absolute -top-6 -right-6 w-20 h-20 bg-white rounded-full flex flex-col items-center justify-center text-purple-600 shadow-lg border-2 border-purple-200">
              <div class="text-xs absolute -top-3 bg-purple-600 text-white px-2 py-1 rounded-full">⏲️</div>
              <span class="text-2xl font-bold">{{ step.timer }}</span>
              <span class="text-xs">sec</span>
            </div>

            <!-- Instruction with speech bubble effect -->
            <div
              class="bg-white/80 backdrop-blur-sm rounded-lg p-4 border-l-4 border-purple-400 relative max-w-[80%] mx-auto my-8">
              <p class="text-lg text-gray-800 font-comic">
                {{ step.content }}
              </p>
              <div
                class="absolute -bottom-3 left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-8 border-r-8 border-b-8 border-l-transparent border-r-transparent border-b-white">
              </div>
            </div>

            <!-- Progress Bar as a kitchen towel -->
            <div class="absolute bottom-0 left-0 w-full h-2 bg-amber-200 rounded-b-lg overflow-hidden">
              <div class="h-full bg-gradient-to-r from-purple-400 to-pink-400 transition-all duration-1000 ease-linear"
                :style="{ width: `${step.progress}%` }"></div>
            </div>
          </div>

          <!-- Navigation Buttons with fun hover effects -->
          <div class="flex justify-between items-center">
            <button v-if="step.value !== '1'" @click="goToStep(parseInt(step.value) - 1)"
              class="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-gray-100 to-gray-200 hover:from-gray-200 hover:to-gray-300 text-gray-700 rounded-full shadow-sm transition-all duration-300 hover:shadow-md hover:-translate-x-1">
              <span class="text-xl">👈</span>
              <span class="font-comic">Oops, go back!</span>
            </button>
            <div v-else class="w-10 h-10 rounded-full bg-yellow-200 flex items-center justify-center text-yellow-600">
              👨‍🍳</div>

            <button v-if="step.value !== steps.length.toString()" @click="goToStep(parseInt(step.value) + 1)"
              class="flex items-center gap-2 px-6 py-3 bg-gradient-to-r from-purple-500 to-pink-500 hover:from-purple-600 hover:to-pink-600 text-white rounded-full shadow-lg transition-all duration-300 hover:shadow-xl hover:translate-x-1">
              <span class="font-comic">
                {{ step.value === (steps.length - 1).toString() ? 'Ta-da! Finish 🎉' : 'Next step! 👉' }}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Fun footer -->
    <div class="text-center mt-8 text-gray-500 text-sm font-comic">
      <!-- <p>Warning: This timer won't actually cook your food... yet! 🔥</p> -->
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { useSiteStore } from '../config/siteConfig.js'

const { siteConfig, getResponsiveValue } = useSiteStore()

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