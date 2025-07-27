
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useControl = defineStore('control', () => {
  const showNav = ref(true)
  const showSearch = ref(false) 
  const setShowNav = (val) => {
    showNav.value = val
  }

    const setShowSearch= (val) => {
    showSearch.value = val
  }
  return {
    showNav,
    setShowNav,
    showSearch,
    setShowSearch
  }
})
