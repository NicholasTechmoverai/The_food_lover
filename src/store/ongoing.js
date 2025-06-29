
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useOngoingStore = defineStore('ongoing', () => {
  const coverRecipe = ref(null)
  const recipeSteps = ref(null)

  const setCoverRecipe = (recipe) => {
    coverRecipe.value = recipe
  }

  const clearCoverRecipe = () => {
    coverRecipe.value = null
  }

  const setRecipeSteps = (recipe) => {
    recipeSteps.value = recipe
  }

  const clearRecipeSteps = () => {
    recipeSteps.value = null
  }

  return {
    coverRecipe,
    recipeSteps,
    setCoverRecipe,
    clearCoverRecipe,
    setRecipeSteps,
    clearRecipeSteps
  }
}, {
  persist: {
    key: 'ongoing-recipe',
    storage: localStorage,
    // Optional: expire after 7 days manually
    afterRestore: (ctx) => {
      const maxAge = 7 * 24 * 60 * 60 * 1000 // 7 days in ms
      const savedAt = localStorage.getItem('ongoing-recipe-timestamp')
      if (savedAt && Date.now() - parseInt(savedAt) > maxAge) {
        localStorage.removeItem('pinia-ongoing') // clear persisted data
        localStorage.removeItem('ongoing-recipe-timestamp')
      }
    },
    beforeRestore: (ctx) => {
      if (!localStorage.getItem('ongoing-recipe-timestamp')) {
        localStorage.setItem('ongoing-recipe-timestamp', Date.now().toString())
      }
    }
  }
})
