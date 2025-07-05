<template>
  <div class="max-w-xl mx-auto p-6 shadow rounded-lg space-y-6">
    <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100">User Preferences</h2>

    <!-- Language -->
    <div>
      <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Language</label>
      <Dropdown v-model="preferences.language" :options="languages" optionLabel="label" placeholder="Select Language"
        class="w-full" />
    </div>

    <!-- Theme -->
    <div>
      <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Theme</label>
      <Dropdown v-model="preferences.theme" :options="themes" optionLabel="label" placeholder="Select Theme"
        class="w-full" />
    </div>

    <!-- Font Size -->
    <div>
      <label class="block text-sm font-medium mb-1 text-gray-700 dark:text-gray-300">Font Size</label>
      <Slider v-model="preferences.fontSize" :min="12" :max="24" />
      <div class="text-sm text-gray-500 mt-1">Current: {{ preferences.fontSize }}px</div>
    </div>

    <!-- Notifications -->
    <div class="flex items-center justify-between">
      <span class="text-sm font-medium text-gray-700 dark:text-gray-300">Enable Notifications</span>
      <InputSwitch v-model="preferences.notifications" />
    </div>

    <!-- Color Pickers -->
    <div class="grid grid-cols-2 gap-4 pt-4">
      <div>
        <label for="primarycolor" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Primary
          Color {{ customColors.primary }}</label>
        <ColorPicker inputId="primarycolor" v-model="customColors.primary" format="hex" class="w-full" />
      </div>

      <div>
        <label for="secondarycolor" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Secondary
          Color  {{ customColors.secondary }}</label>

        <ColorPicker inputId="secondarycolor" v-model="customColors.secondary" format="hex" class="w-full" />
      </div>
    </div>

    <!-- Save -->
    <div class="pt-6 flex justify-end">
      <Button label="Save Preferences" icon="pi pi-save" @click="savePreferences" />
    </div>

    <!-- Toast -->
    <Toast position="bottom-center" />
  </div>
</template>


<script setup>
import { ref, watch, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import Dropdown from 'primevue/dropdown'
import Slider from 'primevue/slider'
import InputSwitch from 'primevue/inputswitch'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import { useToast } from 'primevue/usetoast'

import { applyTheme } from '../reusables'
import { useSiteStore } from '../config/siteConfig.js'

const toast = useToast()

// Store setup
const siteStore = useSiteStore()
const { siteConfig } = storeToRefs(siteStore)
const { adjustThemesColor } = siteStore

// Preferences
const preferences = ref({
  language: { label: 'English', value: 'en' },
  theme:  { label: 'System', value: 'system' },
  fontSize: 16,
  notifications: true
})

// Color customization state
const customColors = ref({
  primary: siteConfig.value.colors.primary,
  secondary: siteConfig.value.colors.secondary
})

// Languages
const languages = [
  { label: 'English', value: 'en' },
  { label: 'Swahili', value: 'sw' },
  { label: 'French', value: 'fr' }
]

// Themes
const themes = [
  { label: 'Light', value: 'light' },
  { label: 'Dark', value: 'dark' },
  { label: 'System', value: 'system' }
]


  
watch(customColors, (newColors) => {
  adjustThemesColor(newColors)
}, { deep: true })


// Watch for manual theme changes
watch(() => preferences.value.theme, (newTheme) => {
  if (newTheme === 'system') {
    localStorage.removeItem('theme') // Don't store system in localStorage
  } else {
    localStorage.setItem('theme', newTheme.value)
  }
  console.log("theme", newTheme.value,newTheme)
  applyTheme(newTheme.value)
})

// On app load
onMounted(() => {
  const storedTheme = localStorage.getItem('theme')
  if (storedTheme === 'light' || storedTheme === 'dark') {
    preferences.value.theme.value = storedTheme
        preferences.value.theme.label = storedTheme

  } else {
    preferences.value.theme.value = 'system' // Default fallback
        preferences.value.theme.label = 'System'

  }
    console.log("stored theme", storedTheme)


  applyTheme(storedTheme)

  // React to OS-level changes when in system mode
  const media = window.matchMedia('(prefers-color-scheme: dark)')
  media.addEventListener('change', () => {
    if (preferences.value.theme === 'system') {
      applyTheme('system')
    }
  })
})

// Save button action
const savePreferences = () => {
  adjustThemesColor(customColors.value)

  toast.add({
    severity: 'success',
    summary: 'Preferences Saved',
    detail: 'Your settings have been updated.',
    life: 3000
  })
}
</script>

