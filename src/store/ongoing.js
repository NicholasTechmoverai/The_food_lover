import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useOngoingStore = defineStore('ongoing', () => {
  const coverRecipe = ref(null) // ⬅️ null, not array

  const setCoverRecipe = (recipe) => {
    coverRecipe.value = recipe
  }

  const clearCoverRecipe = () => {
    coverRecipe.value = null
  }

  return {
    coverRecipe,
    setCoverRecipe,
    clearCoverRecipe,
  }
})
