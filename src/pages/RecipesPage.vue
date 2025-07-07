<template>
  <div class="min-h-screen overflow-hidden relative bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    <!-- Hero Section -->
    <section class="relative h-96 overflow-hidden">
      <img
        src="https://images.unsplash.com/photo-1546069901-d5bfd2cbfb1f?ixlib=rb-1.2.1&auto=format&fit=crop&w=1600&h=600&q=80"
        alt="Delicious recipes" class="w-full h-full object-cover" />
      <div class="absolute inset-0 bg-black/40 flex items-center justify-center">
        <div class="text-center px-4">
          <h1 class="text-4xl md:text-5xl font-bold text-white mb-4">Discover Culinary Delights</h1>
          <p class="text-xl text-white mb-8 max-w-2xl mx-auto">Explore thousands of recipes from around the world,
            curated by professional chefs and home cooks alike</p>
          <div class="relative max-w-md mx-auto">
            <input type="text" placeholder="Search for recipes..."
              class="w-full py-3 px-5 rounded-full shadow-lg focus:outline-none focus:ring-2 focus:ring-primary-500">
            <button
              class="absolute right-2 top-1/2 transform -translate-y-1/2 bg-primary-500 text-white p-2 rounded-full">
              <i class="pi pi-search"></i>
            </button>
          </div>
        </div>
      </div>
    </section>

    <!-- Recipe and Sidebar Layout -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 px-6 py-10">

      <!-- Left: Recipe List (2/3 width) -->
      <section v-if="!isRouterViewActive" class="lg:col-span-2 space-y-6">
        <section>
          <h2 class="text-xl font-semibold mb-4">Explore Recipes type</h2>
          <div v-if="recipes_types_loading" class="flex flex-row gap-2">
            <div v-for="i in 4">
              <RecipeTypesLoader />
            </div>
          </div>
          <div v-else>
            <RecipeTypes :render="'recipes'" :loop_through="recipeTypes" />

          </div>


        </section>
        <h2 class="text-3xl font-bold text-gray-800 dark:text-gray-100">
          Browse Recipes
        </h2>

        <div v-if="recipes_loading" class="grid grid-cols-1 md:grid-cols-2 gap-4 ">
          <RecipeLoader v-for="i in 2" :key="i" />
        </div>


        <div v-else class="grid gap-2 grid-cols-1 sm:grid-cols-2 ">
          <RecipeCard v-for="recipe in recipes.slice(0, 4)" :key="recipe.id" :recipe="recipe"
            class="border border-gray-300 dark:border-gray-700/50" />
          <button class="underlined cursor-pointer ">Show more <i class="pi pi-arrow-right"></i></button>
        </div>
      </section>

      <!-- Right: Sidebar with Tips and Video -->
      <aside class="space-y-12 lg:sticky lg:top-20 flex flex-col ">

        <!-- Cooking Tips Section -->
        <section>
          <h2 class="text-xl font-semibold mb-4">Live recipes & live in the kitcen</h2>
          <RevolveCards :render="'live'" :loop_through="liveRecipes" />
        </section>

        <!-- Featured Video Section -->
        <section class="w-full bg-amber-500/0">
          <h2 class=" text-xl font-semibold mb-4">Watch & Learn</h2>
          <VideoPage />
        </section>
        <section>
          <h2 class="text-xl font-semibold mb-4">Trending recipes this week</h2>
          <TrendingDishesCard class="mt-0 mb-80" />
        </section>
      </aside>

    </div>
    <Toast />
    <!-- Router View for Dynamic Pages -->
    <router-view v-if="isRouterViewActive"
      class="absolute inset-0 bg-white dark:bg-gray-900 z-50 overflow-y-auto transition-all duration-300" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import RecipeCard from '../cards/RecipeCard.vue'
import RevolveCards from '../cards/RevolveCards.vue'
import TrendingDishesCard from '../cards/TrendingDishesCard.vue'
import { fetchLiveRecipes, fetchRecipes, fetchRecipeTypes } from '../apis/recipes.js'
import VideoPage from './VideoPage.vue'
import RecipeTypes from '../cards/HorizonScroll.vue'// Track route
import { useAuthStore } from '../store/user.js'
import { useToast } from 'primevue/usetoast'
import RecipeLoader from '../loaders/Skeleton3.vue'
import RecipeTypesLoader from '../loaders/Skeleton1.vue'

const auth = useAuthStore()
const toast = useToast()
const recipes_loading = ref(false)
const recipes_types_loading = ref(false)


const route = useRoute()

const isRouterViewActive = computed(() =>
  [
    'NewRecipe',
    'CoverInfo',
    'NewRecipeUploadsBase',
    'NewRecipeUploadsWithId',
    'PublishRecipe',
    'PublishRecipeWithId',
    'RecipeId',
    'RecipeType'
  ].includes(route.name)
)



// Fetch recipes
const recipes = ref([])
const recipeTypes = ref([])
const liveRecipes = ref([])

const getRecipes = async () => {
  recipes_loading.value = true
  const token = auth.token
  const res = await fetchRecipes(token, { limit: 10, offset: 0 })
  if (res) {
    recipes_loading.value = false
    if (res.message && !res.success) {
      toast.add({
        severity: 'error',
        summary: 'Error fetcing Recipes !',
        detail: `${res.message}`,
        life: 5000
      });
    }
    if (res.data) {
      recipes.value = res.data
    }
  }
}
const getRecipeTypes = async () => {
  recipes_types_loading.value = true
  const token = auth.token
  const res = await fetchRecipeTypes(token, null)
  if (res) {
    recipes_types_loading.value = false
    if (res.message && !res.success) {
      toast.add({
        severity: 'error',
        summary: 'Error fetcing Recipes Types !',
        detail: `${res.message}`,
        life: 5000
      });
    }
    if (res.data) {
      recipeTypes.value = res.data
    }
  }
}

onMounted(async () => {
  await getRecipes()
  await getRecipeTypes()
  liveRecipes.value = await fetchLiveRecipes()
  // console.log(recipes.value)
})
</script>
