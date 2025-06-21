<template>
  <div class="max-w-xl mx-auto p-6 shadow rounded-lg space-y-6">
    <h2 class="text-2xl font-bold text-gray-800">User Preferences</h2>

    <!-- Language -->
    <div>
      <label class="block text-sm font-medium mb-1 text-gray-700">Language</label>
      <Dropdown
        v-model="preferences.language"
        :options="languages"
        optionLabel="label"
        placeholder="Select Language"
        class="w-full"
      />
    </div>

    <!-- Theme -->
    <div>
      <label class="block text-sm font-medium mb-1 text-gray-700">Theme</label>
      <Dropdown
        v-model="preferences.theme"
        :options="themes"
        optionLabel="label"
        placeholder="Select Theme"
        class="w-full"
      />
    </div>

    <!-- Font Size -->
    <div>
      <label class="block text-sm font-medium mb-1 text-gray-700">Font Size</label>
      <Slider v-model="preferences.fontSize" :min="12" :max="24" />
      <div class="text-sm text-gray-500 mt-1">Current: {{ preferences.fontSize }}px</div>
    </div>

    <!-- Notifications -->
    <div class="flex items-center justify-between">
      <span class="text-sm font-medium text-gray-700">Enable Notifications</span>
      <InputSwitch v-model="preferences.notifications" />
    </div>

    <!-- Save -->
    <div class="pt-4 flex justify-end">
      <Button label="Save Preferences" icon="pi pi-save" @click="savePreferences" />
    </div>

    <!-- Toast -->
    <Toast position="bottom-center" />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Dropdown from 'primevue/dropdown'
import Slider from 'primevue/slider'
import InputSwitch from 'primevue/inputswitch'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import { useToast } from 'primevue/usetoast'

const toast = useToast()

const preferences = ref({
  language: null,
  theme: null,
  fontSize: 16,
  notifications: true
})

const languages = [
  { label: 'English', value: 'en' },
  { label: 'Swahili', value: 'sw' },
  { label: 'French', value: 'fr' }
]

const themes = [
  { label: 'Light', value: 'light' },
  { label: 'Dark', value: 'dark' },
  { label: 'System', value: 'system' }
]

const savePreferences = () => {
  toast.add({
    severity: 'success',
    summary: 'Preferences Saved',
    detail: 'Your settings have been updated.',
    life: 3000
  })
}
</script>
