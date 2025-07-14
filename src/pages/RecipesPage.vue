<template>
  <div v-if="!isRouterViewActive"
    class="min-h-screen overflow-hidden relative bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
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
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8 px-4 md:px-6 py-10">

      <!-- Sidebar: Visible first on small screens, second on large screens -->
      <aside class="order-1 lg:order-2 space-y-10 lg:sticky top-16 self-start">

        <!-- Live Recipes -->
        <section>
          <h2 class="text-xl font-semibold mb-4">Live Recipes & In the Kitchen</h2>
          <RevolveCards :render="'live'" :loop_through="liveRecipes" />
        </section>

        <!-- Featured Video -->
        <section>
          <h2 class=" text-xl font-semibold mb-4">Watch & Learn</h2>
          <VideoPage />
        </section>

        <!-- Trending Recipes -->
        <section>
          <h2 class="text-xl font-semibold mb-4">Trending Recipes This Week</h2>
          <TrendingDishesCard class="mt-45 mb-45" />
        </section>
      </aside>

      <!-- Main Recipe List -->
      <section class="order-2 lg:order-1 lg:col-span-2 space-y-8">

        <!-- Recipe Types -->
        <div>
          <h2 class="text-xl font-semibold mb-4">Explore Recipe Types</h2>
          <div v-if="recipes_types_loading" class="flex flex-wrap gap-3">
            <RecipeTypesLoader v-for="i in 4" :key="i" />
          </div>
          <div v-else>
            <RecipeTypes :render="'recipes'" :loop_through="recipeTypes" />
          </div>
        </div>

        <!-- Recipe Cards -->
        <div>
          <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100 mb-4">Browse Recipes</h2>
          <MainRecipeCardsParent />
        </div>

      </section>
    </div>

    <Toast />

  </div>
  <!-- Router View for Dynamic Pages -->
  <transition name="slide-fade" mode="out-in">
    <router-view v-if="isRouterViewActive" class="inset-0 bg-white dark:bg-gray-900 z-50 overflow-y-auto" />
  </transition>

</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import RevolveCards from '../cards/RevolveCards.vue'
import TrendingDishesCard from '../cards/TrendingDishesCard.vue'
import { fetchLiveRecipes, fetchRecipes, fetchRecipeTypes } from '../apis/recipes.js'
import VideoPage from './VideoPage.vue'
import RecipeTypes from '../cards/HorizonScroll.vue'// Track route
import { useAuthStore } from '../store/user.js'
import { useToast } from 'primevue/usetoast'
import RecipeTypesLoader from '../loaders/Skeleton1.vue'
import MainRecipeCardsParent from "../cards/ManyReipesParent.vue"

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
const recipeTypes = ref([])
const liveRecipes = ref([])





const getRecipeTypes = async (params = null) => {
  recipes_types_loading.value = true
  const token = auth.token
  const res = await fetchRecipeTypes(token, params)
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
  recipes_types_loading.value = true
  recipes_loading.value = true
  liveRecipes.value = await fetchLiveRecipes()

  await Promise.all([getRecipeTypes()]);
});

</script>
<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.4s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateX(50px);
}

.slide-fade-enter-to {
  opacity: 1;
  transform: translateX(0);
}

.slide-fade-leave-from {
  opacity: 1;
  transform: translateX(0);
}

.slide-fade-leave-to {
  opacity: 0;
  transform: translateX(-50px);
}
</style>
