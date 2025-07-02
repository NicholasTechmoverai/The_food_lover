

 <template>
      <router-view class="fixed pt-15 w-full h-[80%] md:h-full z-70" />

  <div class="p-6 z-50">
    <h1 class="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-100">Browse Recipes</h1>

    <div class="grid gap-6 grid-cols-1 sm:grid-cols-1 md:grid-cols-3 xl:grid-cols-4">
      <RecipeCard
        v-for="recipe in recipes"
        :key="recipe.id"
        :recipe="recipe"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import RecipeCard from '../cards/RecipeCard.vue'
import {fetchRecipes } from '../apis/recipes.js'

const recipes  = fetchRecipes()
</script>
