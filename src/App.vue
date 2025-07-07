<script setup>
import Menubar from './components/menubar.vue';
import Footer from './pages/MainFooter.vue';
import { applyTheme } from './reusables'
import { onMounted } from 'vue'
import { useControl } from './store/control.js';
const control = useControl()

// Theme application on app mount
onMounted(() => {
  const savedTheme = localStorage.getItem('theme') || 'system'
  applyTheme(savedTheme)

  console.log(savedTheme)

  // Listen to system changes only if using system preference
  if (savedTheme === 'system') {
    const media = window.matchMedia('(prefers-color-scheme: dark)')
    media.addEventListener('change', () => {
      applyTheme('system')
    })
  }
})
</script>

<template>
  <div class="min-h-screen flex flex-col transition-colors duration-300">
    <div v-if="control.showNav" class="sticky top-0 z-400 backdrop-blur-sm">
      <Menubar />
    </div>
    <div class="relative w-full overflow-x-hidden max-w-[2500px] mx-auto">
    <router-view  />

    </div>
    <Footer v-if="control.showNav" />
  </div>
</template>



