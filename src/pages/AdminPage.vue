<template>
  <loginAdmin v-if="!isVerified" @verified="handleVerified" />

  <div v-if="isVerified" class="min-h-screen p-6">
    <Card class="max-w-7xl mx-auto">
      <!-- Header -->
      <template #title>
        <div class="flex flex-col md:flex-row justify-between items-start md:items-center">
          <div>
            <h2 class="text-2xl font-bold text-gray-800">Site Configuration Editor</h2>
            <p class="text-gray-600">Manage all site settings and configurations</p>
          </div>
          <div class="flex gap-2 mt-4 md:mt-0">
            <Button label="Home" @click="goHome" text />
            <Button label="Reset Changes" icon="pi pi-refresh" severity="warning" outlined @click="resetConfig" />
            <Button
              label="Save Changes"
              icon="pi pi-check"
              severity="success"
              :loading="isSaving"
              :disabled="!hasChanges"
              @click="saveConfig"
            />
          </div>
        </div>
      </template>

      <template #content>
        <Message severity="warn" class="mb-5">
          <strong>NOTE:</strong> This site does not have a database connected. Changes will not be saved permanently.
        </Message>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          <Card v-for="(section, key) in configCopy" :key="key" class="border border-gray-200">
            <template #title>
              <div
                class="cursor-pointer flex justify-between items-center"
                @click="toggleSection(key)"
              >
                <span class="font-semibold">{{ formatKey(key) }}</span>
                <i :class="openSections[key] ? 'pi pi-minus' : 'pi pi-plus'" class="text-sm"></i>
              </div>
            </template>

            <template #content>
              <transition name="fade">
                <div v-if="openSections[key]">
                  <ConfigEditor
                    :keyName="String(key)"
                    :value="section"
                    @update:modelValue="(newValue) => updateValue([key], newValue)"
                  />
                </div>
              </transition>
            </template>
          </Card>
        </div>

        <div v-if="hasChanges" class="mt-5 text-yellow-600 flex items-center gap-2">
          <i class="pi pi-exclamation-triangle"></i>
          <span>You have unsaved changes</span>
        </div>
      </template>
    </Card>

    <!-- Toast -->
    <Toast />
  </div>
</template>

<script setup>
import { reactive, ref, computed } from 'vue'
import { siteConfig } from '../config/siteConfig'
import ConfigEditor from './ComponentEditor.vue'
import loginAdmin from '../cards/loginAdmin.vue'
import { goHome } from '../reusables'
import { useToast } from 'primevue/usetoast'
import Card from 'primevue/card'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import Message from 'primevue/message'

const toast = useToast()
const isVerified = ref(false)
const isSaving = ref(false)
const openSections = ref({})
const configCopy = reactive(JSON.parse(JSON.stringify(siteConfig)))
const originalConfig = JSON.parse(JSON.stringify(siteConfig))

const hasChanges = computed(() => {
  return JSON.stringify(configCopy) !== JSON.stringify(originalConfig)
})

const toggleSection = (key) => {
  openSections.value[key] = !openSections.value[key]
}

const updateValue = (path, newValue) => {
  let target = configCopy
  for (let i = 0; i < path.length - 1; i++) {
    target = target[path[i]]
  }
  target[path[path.length - 1]] = newValue
}

const saveConfig = async () => {
  isSaving.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    Object.assign(originalConfig, JSON.parse(JSON.stringify(configCopy)))
    toast.add({ severity: 'success', summary: 'Configuration saved successfully!', life: 3000 })
  } catch (error) {
    toast.add({ severity: 'error', summary: 'Failed to save configuration', detail: error.message })
  } finally {
    isSaving.value = false
  }
}

const resetConfig = () => {
  if (confirm('Are you sure you want to reset all changes?')) {
    Object.assign(configCopy, JSON.parse(JSON.stringify(originalConfig)))
  }
}

const formatKey = (key) => {
  return key
    .replace(/([A-Z])/g, ' $1')
    .replace(/^./, str => str.toUpperCase())
    .replace('Offred', 'Offered')
}

const handleVerified = (value) => {
  if (value) isVerified.value = true
}
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: all 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>