<template>
  <div class="min-h-screen relative">
    <!-- Recipe List -->
    <div v-if="!isRouterViewActive" class="p-6 z-40">
      <h1 class="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-100">Browse Recipes</h1>
      <div class="grid gap-4 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4">
        <RecipeCard
          v-for="recipe in recipes"
          :key="recipe.id"
          :recipe="recipe"
        />
      </div>
    </div>

    <router-view
      v-if="isRouterViewActive"
      class=" inset-0 bg-white dark:bg-gray-900 z-50 overflow-y-auto transition-all duration-300"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import RecipeCard from '../cards/RecipeCard.vue'
import { fetchRecipes } from '../apis/recipes.js'

// Track route
const route = useRoute()

const isRouterViewActive = computed(() =>
  [
    'NewRecipe',
    'CoverInfo',
    'NewRecipeUploadsBase',
    'NewRecipeUploadsWithId',
    'PublishRecipe',
    'PublishRecipeWithId',
    'RecipeId'
  ].includes(route.name)
)

// Fetch recipes
const recipes = ref([])

onMounted(async () => {
  recipes.value = await fetchRecipes()
  // console.log(recipes.value)
})
</script>
