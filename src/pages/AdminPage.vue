<template>
  <loginAdmin v-if="!isVerified" @verified="handleVerified"  />
  <div v-if="isVerified" class="min-h-screen bg-gray-50 p-6">
    <div class="relative max-w-7xl mx-auto">
      <!-- Header Section -->
      <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-4">
        <div>
          <h1 class="text-3xl font-bold text-gray-800 flex items-center gap-3">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-600" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            </svg>
            Site Configuration Editor
          </h1>
          <p class="text-gray-600 mt-1">Manage all site settings and configurations</p>

        </div>

        <div class="flex flex-wrap gap-3">
          <button @click="goHome" class="px-4 py-2 text-gray-300 cursor-pointer rounded">Home</button>
          <button @click="resetConfig"
            class="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg shadow-sm hover:bg-gray-50 text-gray-700 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            Reset Changes
          </button>
          <button @click="saveConfig" :disabled="isSaving || !hasChanges"
            class="flex items-center gap-2 px-6 py-2 bg-blue-600 rounded-lg shadow-sm hover:bg-blue-700 text-white transition-colors disabled:opacity-70 disabled:cursor-not-allowed">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <span v-if="!isSaving">Save Changes</span>
            <span v-else class="flex items-center gap-2">
              <svg class="animate-spin h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
                viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z">
                </path>
              </svg>
              Saving...
            </span>
          </button>
        </div>
      </div>

      <div class="sticky top-0 w-full p-5 text-[14px] md:text-xl text-white bg-red-500/50 border border-red-600/40">
        NOTE: There is NO database set for this site set set for NOW which means any changes you are MAKING will NOT be SAVED. so..Just GET
        OUT Of HERE!! GET LOST!!
      </div>

      <!-- Configuration Sections -->
      <div class="bg-white rounded-xl shadow-md overflow-hidden">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 p-6">
          <div v-for="(section, key) in configCopy" :key="key"
            class="border border-gray-200 rounded-lg overflow-hidden transition-all duration-200 hover:shadow-md">
            <div
              class="cursor-pointer font-semibold text-lg bg-gradient-to-r from-blue-600 to-blue-500 text-white p-4 flex justify-between items-center"
              @click="toggleSection(key)">
              <span class="flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                  stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                </svg>
                {{ formatKey(key) }}
              </span>
              <span class="text-xl font-mono">{{ openSections[key] ? '−' : '+' }}</span>
            </div>
            <transition enter-active-class="transition-all duration-300 ease-out"
              leave-active-class="transition-all duration-200 ease-in" enter-from-class="opacity-0 max-h-0"
              enter-to-class="opacity-100 max-h-screen" leave-from-class="opacity-100 max-h-screen"
              leave-to-class="opacity-0 max-h-0">
              <div v-if="openSections[key]" class="p-4 bg-gray-50">
                <ConfigEditor :keyName="String(key)" :value="section"
                  @update:modelValue="(newValue) => updateValue([key], newValue)" />
              </div>
            </transition>
          </div>
        </div>
      </div>

      <!-- Save Indicator -->
      <div v-if="hasChanges" class="mt-4 text-sm text-gray-500 flex items-center gap-2">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-yellow-500" fill="none" viewBox="0 0 24 24"
          stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
        </svg>
        You have unsaved changes
      </div>
    </div>

    <!-- Save Toast Notification -->
    <transition enter-active-class="transform ease-out duration-300 transition"
      enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
      enter-to-class="translate-y-0 opacity-100 sm:translate-x-0" leave-active-class="transition ease-in duration-100"
      leave-from-class="opacity-100" leave-to-class="opacity-0">
      <div v-if="showSaveToast" class="fixed bottom-4 right-4">
        <div class="rounded-md bg-green-50 p-4 shadow-lg border border-green-100">
          <div class="flex">
            <div class="flex-shrink-0">
              <svg class="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"
                fill="currentColor">
                <path fill-rule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                  clip-rule="evenodd" />
              </svg>
            </div>
            <div class="ml-3">
              <p class="text-sm font-medium text-green-800">
                Configuration saved successfully!
              </p>
            </div>
            <div class="ml-auto pl-3">
              <div class="-mx-1.5 -my-1.5">
                <button @click="showSaveToast = false"
                  class="inline-flex rounded-md p-1.5 text-green-500 hover:bg-green-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-600">
                  <svg class="h-5 w-5" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                    <path fill-rule="evenodd"
                      d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                      clip-rule="evenodd" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue';
import { siteConfig } from '../config/siteConfig';
import ConfigEditor from './ComponentEditor.vue';
import { goHome } from '../reusables';
import loginAdmin from '../cards/loginAdmin.vue';

// Create a deep copy of the config
const configCopy = reactive(JSON.parse(JSON.stringify(siteConfig)));
const originalConfig = JSON.parse(JSON.stringify(siteConfig));

// UI state
const openSections = ref({});
const isSaving = ref(false);
const showSaveToast = ref(false);
const isVerified = ref(false);

// Computed properties
const hasChanges = computed(() => {
  return JSON.stringify(configCopy) !== JSON.stringify(originalConfig);
});

// Format section keys for display
const formatKey = (key) => {
  return key
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, str => str.toUpperCase())
    .replace('Offred', 'Offered'); // Fix typo in original config
};

const handleVerified = (value) => {
      console.log('User verified!',value)
  if (value) {
    isVerified.value = value;
  }
}

// Toggle section visibility
const toggleSection = (key) => {
  openSections.value[key] = !openSections.value[key];
};

// Update nested values
const updateValue = (path, newValue) => {
  let target = configCopy;
  for (let i = 0; i < path.length - 1; i++) {
    target = target[path[i]];
  }
  target[path[path.length - 1]] = newValue;
};

// Save configuration
const saveConfig = async () => {
  isSaving.value = true;
  try {
    // In a real app, you would send this to your backend
    console.log('Saving config:', JSON.parse(JSON.stringify(configCopy)));

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));

    // Update original config to match current state
    Object.assign(originalConfig, JSON.parse(JSON.stringify(configCopy)));

    showSaveToast.value = true;
    setTimeout(() => showSaveToast.value = false, 3000);
  } catch (error) {
    console.error('Error saving config:', error);
  } finally {
    isSaving.value = false;
  }
};

// Reset to original values
const resetConfig = () => {
  if (confirm('Are you sure you want to reset all changes?')) {
    Object.assign(configCopy, JSON.parse(JSON.stringify(originalConfig)));
  }
};
</script>

<style scoped>
/* Smooth transitions for the save toast */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>