import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import router from '../router'

export const useControl = defineStore('control', () => {
  const showNav = ref(true)
  const showSearch = ref(false)

  const setShowNav = (val) => {
    showNav.value = val

    const currentQuery = { ...router.currentRoute.value.query }

    if (val) {
      router.push({ query: { ...currentQuery, search: 'true' } })
    } else {
      const { search, ...rest } = currentQuery
      router.push({ query: rest })
    }
  }

  const setShowSearch = (val) => {
    showSearch.value = val

    const currentQuery = { ...router.currentRoute.value.query }

    if (val) {
      router.push({ query: { ...currentQuery, search: 'true' } })
    } else {
      const { search, ...rest } = currentQuery
      router.push({ query: rest })
    }
  }

  // Sync showSearch with URL query param on page load or navigation
  watch(
    () => router.currentRoute.value.query.search,
    (val) => {
      showSearch.value = val === 'true'
    },
    { immediate: true }
  )

  return {
    showNav,
    showSearch,
    setShowNav,
    setShowSearch
  }
})
