<template>
    <div>
      <!-- Main Recipe List -->
      <section class="order-2 lg:order-1 lg:col-span-2 space-y-6 md:space-y-8">
        <!-- Recipe Cards Grid -->
        <div>
        
          <!-- Loaded State -->
          <div >
            <!-- Empty State -->
            <div v-if="recipes.length === 0" class="text-center py-12 md:py-16 lg:py-20">
              <div class="mx-auto w-24 h-24 md:w-32 md:h-32 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-6">
                <i class="pi pi-book text-4xl md:text-5xl text-gray-400 dark:text-gray-500"></i>
              </div>
              <h3 class="text-lg md:text-xl font-semibold text-gray-800 dark:text-gray-100 mb-3">
                No recipes found
              </h3>
              <p class="text-gray-500 dark:text-gray-400 max-w-md mx-auto text-sm md:text-base">
                Try adjusting your search or create a new recipe
              </p>
            </div>

            <!-- Recipe Grid -->
            <div v-else 
                 class="grid gap-4 sm:gap-5 md:gap-6"
                 style="grid-template-columns: repeat(auto-fill, minmax(320px, 1fr))">
              <RecipeCard 
                v-for="recipe in recipes" 
                :key="recipe.id" 
                :recipe="recipe"
                class="min-w-[300px] border border-gray-200/80 dark:border-gray-700/50 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1"
              />
            </div>
          </div>
            <!-- Loading State -->
          <div v-if="recipes_loading" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 2xl:grid-cols-5 gap-4 sm:gap-5 md:gap-6"
               style="grid-template-columns: repeat(auto-fill, minmax(350px, 1fr))">
            <RecipeLoader 
              v-for="i in 2" 
              :key="'loader-'+i" 
              class="min-w-[300px] border border-gray-200/80 dark:border-gray-700/50 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow duration-300"
            />
          </div>


          <!-- Pagination/Show More -->
          <div v-if="recipes.length > 0 && recipes.length >= limit && !recipes_loading" class="pt-6 md:pt-8 flex justify-center">
            <button 
              @click="getRecipes(limit, offset + limit)"
              class="inline-flex items-center gap-2 px-5 py-2.5 md:px-6 md:py-3 bg-white dark:bg-gray-800 border border-gray-300 dark:border-gray-600 rounded-full text-sm md:text-base font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-gray-700/60 transition-all duration-200 hover:shadow-md"
            >
              Show more recipes
              <i class="pi pi-arrow-right text-xs md:text-sm"></i>
            </button>
          </div>
        </div>
      </section>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import RecipeCard from '../cards/RecipeCard.vue'
import { fetchRecipes } from '../apis/recipes.js'
import { useAuthStore } from '../store/user.js'
import { useToast } from 'primevue/usetoast'
import RecipeLoader from '../loaders/Skeleton3.vue'
import { make_a_post } from '../apis/index.js'
import { boolean } from 'zod'

const props = defineProps({
  user_id: {
    type: String,
    default: () => null
  },
   saved: {
    type: Boolean,
    default: () => false
  },
  recipe_name:{
    type:String,
    default:()=>null
  },
  categgory:{
    type:Array,
    default:()=>[]
  },
  tags:{
    type:Array,
    default:()=>[]
  }
});



const auth = useAuthStore()
const toast = useToast()
const recipes_loading = ref(false)
const offset = ref(0)
const limit = ref(10)





// Fetch recipes
const recipes = ref([])

const getRecipes = async (
  pageLimit = 10,
  pageOffset = 0
) => {
  recipes_loading.value = true
  const token = auth.token
  const res = await fetchRecipes(token, { limit: pageLimit, 
    offset: pageOffset,
    user_id:props.user_id,
    recipe_name:props.recipe_name,
    categgory:props.categgory,
    tags:props.tags,
    saved:props.saved
   })

  if (res) {
    recipes_loading.value = false
    if (res.message && !res.success) {
      toast.add({
        severity: 'error',
        summary: 'Error fetching Recipes!',
        detail: `${res.message}`,
        life: 5000
      })
    }

    if (res.data) {
      if (res.data.recipes) {
        // recipes.value = [...res.data.recipes]
        recipes.value.push(...res.data.recipes);
        offset.value = res.data.offset ?? pageOffset
        limit.value = res.data.limit ?? pageLimit
        // Fetch meta for the newly fetched recipes
        await fetchRecipeMeta(res.data.recipes.map(r => r.id))
      } else {
        recipes.value = res.data
      }
    }
  }
}

const emit = defineEmits([ 'recipes_count'])

const fetchRecipeMeta = async (recipe_ids) => {
  const res = await make_a_post('/recipes/meta', auth.token, { recipe_ids: recipe_ids }, null)
  if (res) {
    if (res.message && !res.success) {
      toast.add({
        severity: 'error',
        summary: `Error fetching Recipe Meta!`,
        detail: `${res.message}`,
        life: 5000
      })
    }
    if (res.data) {
      const metaMap = res.data;

      recipes.value = recipes.value.map(recipe => ({
        ...recipe,
        recipeMeta: {
          likeCount: 0,
          comments: 0,
          isFollowing: false,
          isFollowed: false,
          views: 0,
          shareCount: 0,
          isLiked: false,
          isSaved: false,
          ...(metaMap[recipe.id] || {})  // safely override defaults
        }
      }))
      emit('recipes_count',recipes.value.length)
    }

  }
}



onMounted(async () => {
  recipes_loading.value = true
  await Promise.all([getRecipes()]);
});
watch(
  () => props.user_id,
  (newUserId, oldUserId) => {
    if (newUserId !== oldUserId) {
      fetchRecipes(newUserId, props.saved);
    }
  },
  { immediate: true }
);

watch(
  () => props.saved,
  (newSaved, oldSaved) => {
    if (newSaved !== oldSaved) {
      fetchRecipes(props.user_id, newSaved);
    }
  },
  { immediate: true }
);
</script>