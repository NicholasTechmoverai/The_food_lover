
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useControl = defineStore('control', () => {
  const showNav = ref(true)

  const setShowNav = (val) => {
    showNav.value = val
  }
  return {
    showNav,
    setShowNav
  }
})
