<script setup>
import Menubar from './components/menubar.vue';
import Footer from './pages/MainFooter.vue';
import { applyTheme } from './reusables'
import { onMounted } from 'vue'

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
    <div class="sticky top-0 z-100 backdrop-blur-sm">
      <Menubar />
    </div>
    <router-view class="mt-0" />
    <Footer />
  </div>
</template>



