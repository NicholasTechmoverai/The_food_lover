<template>
  <div
    class="min-w-[300px] overflow-hidden shadow-md  transition-transform duration-300 hover:-translate-y-1 hover:shadow-xl bg-white dark:bg-gray-900"
    :style="{ '--theme-color': recipe?.repiceColor || '#f97316' }">
    <!-- User Profile -->
    <div class="flex justify-between items-center border-b px-4 py-3 border-gray-300 dark:border-gray-700">
      <div class="flex items-center gap-3">
        <img :src="recipe.user?.profilePic || defaultAvatar" :alt="recipe.user?.name"
          class="w-10 h-10 rounded-full object-cover" />
        <div>
          <h4 class="text-sm font-semibold text-gray-800 dark:text-white">{{ recipe.user?.name }}</h4>
          <p class="text-xs text-gray-500 dark:text-gray-400">{{ recipe.user?.totalRecipes }} recipes shared</p>
        </div>
      </div>
      <button
        class="text-xs px-3 py-1 border border-[var(--theme-color)] text-[var(--theme-color)] rounded-full hover:bg-[var(--theme-color)] hover:text-white">
        Follow
      </button>
    </div>

    <!-- Recipe Image -->
    <div class="relative h-52 overflow-hidden">
      <img :src="recipe.image || placeholderImage" :alt="recipe.recipeName"
        class="w-full h-full object-cover transition-transform duration-500 hover:scale-105" loading="lazy"
        @error="(e) => e.target.src = onerrorImage" />
      <div class="absolute bottom-2 left-2 flex gap-2">
        <span class="text-xs px-2 py-1 rounded-full bg-black/70 text-white backdrop-blur-sm">
          {{ recipe?.complexityLevel?.name }}
        </span>
        <span class="text-xs px-2 py-1 rounded-full bg-black/70 text-white backdrop-blur-sm flex items-center gap-1">
          <ClockIcon class="w-4 h-4" /> {{ formatCookTime(recipe?.cookTime) }}
        </span>
      </div>
    </div>

    <!-- Recipe Content -->
    <div class="p-4 space-y-2">
      <div>
        <h3 class="text-lg font-semibold text-gray-800 dark:text-white">{{ recipe.recipeName }}</h3>
        <div class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-2">
          <GlobeIcon class="w-4 h-4" />
          <span>{{ recipe.cuisine.name }} • {{ recipe.cuisine.region }}</span>
        </div>
      </div>

      <p class="text-sm text-gray-600 dark:text-gray-300">
        {{ truncateDescription(recipe.description) }}
        <button v-if="shouldShowMore" class="text-[var(--theme-color)] font-medium ml-1"
          @click="showFullDescription = !showFullDescription">
          {{ showFullDescription ? 'Show less' : 'Read more' }}
        </button>
      </p>

      <div class="flex flex-wrap gap-2 pt-2">
        <span v-for="tag in recipe.tags.slice(0, 3)" :key="tag"
          class="bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 px-2 py-1 text-xs rounded-full">
          #{{ tag }}
        </span>
      </div>
    </div>

    <!-- Footer -->
    <div class="flex justify-between items-center px-4 py-3 border-t border-gray-300 dark:border-gray-700">
      <div class="flex gap-2 flex-wrap">
        <span v-for="cat in recipe.category" :key="cat"
          class="bg-[color:var(--theme-color-light)] text-[color:var(--theme-color-dark)] px-2 py-1 text-xs font-medium rounded-full">
          {{ cat }}
        </span>
      </div>
      <router-link :to="recipeUrl(recipe.recipeName, recipe.id)">
        <RecipeButton :theme="recipe.repiceColor" />
      </router-link>
    </div>

    <!-- Modal -->
    <div v-if="showFullDescription"
      class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex justify-center items-center"
      @click.self="showFullDescription = false">
      <div
        class="bg-white dark:bg-gray-900 text-gray-900 dark:text-gray-100 rounded-xl p-6 max-w-xl w-full relative max-h-[80vh] overflow-y-auto">
        <button class="absolute top-4 right-4 text-2xl" @click="showFullDescription = false">&times;</button>
        <h3 class="text-xl font-bold mb-4">About {{ recipe.recipeName }}</h3>
        <div v-html="recipe.description" class="prose dark:prose-invert"></div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref, computed } from 'vue';
import onerrorImage from '../assets/onerrorimage.png'

// import { ClockIcon, GlobeIcon, ArrowRightIcon } from 'your-icon-library';
import RecipeButton from './RecipeViewButton.vue'
const props = defineProps({
  recipe: {
    type: Object,
    required: true,
    default: () => ({
      user: {
        name: '',
        profilePic: '',
        id: '',
        totalRecipes: 0
      },
      id: null,
      recipeName: '',
      repiceColor: '#f97316',
      image: null,
      tags: [],
      cookTime: { hr: 0, min: 0 },
      description: '',
      cuisine: { name: 'Kenyan', region: 'East Africa' },
      complexityLevel: { name: 'Easy', value: 1 },
      category: []
    })
  }
});

const showFullDescription = ref(false);
const defaultAvatar = 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png';
const placeholderImage = 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-4.0.3&auto=format&fit=crop&w=880&q=80';

const formatCookTime = (cookTime) => {
  if (cookTime.hr > 0 && cookTime.min > 0) {
    return `${cookTime.hr}h ${cookTime.min}m`;
  } else if (cookTime.hr > 0) {
    return `${cookTime.hr}h`;
  }
  return `${cookTime.min}m`;
};

const truncateDescription = (desc) => {
  if (!desc) return '';
  const text = desc.replace(/<[^>]*>/g, '');
  return text.length > 100 ? `${text.substring(0, 100)}...` : text;
};

const shouldShowMore = computed(() => {
  return props.recipe.description?.replace(/<[^>]*>/g, '').length > 100;
});

const recipeUrl = (name, id) => {
  return `/recipes/${name.replace(/\s+/g, '-').toLowerCase()}/${id}`;
};

</script>