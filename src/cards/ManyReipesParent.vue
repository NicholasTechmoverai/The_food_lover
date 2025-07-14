<template>
    <div>
        
      <!-- Main Recipe List -->
      <section class="order-2 lg:order-1 lg:col-span-2 space-y-8">

        <!-- Recipe Cards -->
        <div>

          <div v-if="recipes_loading" class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <RecipeLoader v-for="i in 2" :key="i" />
          </div>

          <div v-else class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <RecipeCard v-for="recipe in recipes" :key="recipe.id" :recipe="recipe"
              class="border border-gray-300 dark:border-gray-700/50 rounded-md" />
          </div>

          <div class="pt-4" v-if="recipes.length > (limit-offset)">
            <button @click="getRecipes(limit + 10, offset + 10)"
              class="inline-flex items-center gap-2 text-primary-600 hover:underline text-sm font-medium">
              Show more <i class="pi pi-arrow-right"></i>
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
  const res = await fetchRecipes(token, { limit: pageLimit, offset: pageOffset,user_id:props.user_id,saved:props.saved })

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