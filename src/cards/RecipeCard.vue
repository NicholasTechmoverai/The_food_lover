<template>
  <div
    class="min-w-[300px] bg-white dark:bg-gray-900 shadow-md hover:shadow-xl rounded-lg overflow-hidden transition-transform duration-300 hover:-translate-y-1"
    :style="{ '--theme-color': recipe?.repiceColor || '#f97316' }"
  >
    <!-- 👤 User Header -->
    <div class="flex justify-between items-center px-4 py-3 border-b border-gray-300 dark:border-gray-700">
      <div class="flex items-center gap-3">
        <img
          :src="recipe.user?.profilePic || defaultAvatar"
          :alt="recipe.user?.name"
          class="w-10 h-10 rounded-full object-cover"
        />
        <div>
          <h4 class="text-sm font-semibold text-gray-800 dark:text-white">{{ recipe.user?.name }}</h4>
          <p class="text-xs text-gray-500 dark:text-gray-400">{{ recipe.user?.totalRecipes }} recipes shared</p>
        </div>
      </div>
      <button
        v-if="!isFollowed && !isFollowing"
        @click="follow(recipe.user.id)"
        class="text-xs px-3 py-1 rounded-full border border-[var(--theme-color)] text-[var(--theme-color)] hover:bg-[var(--theme-color)] hover:text-white transition"
      >
        Follow
      </button>
      <span
        v-else-if="isFollowing"
        class="text-xs px-3 py-1 rounded-full border border-[var(--theme-color)] text-[var(--theme-color)] opacity-70 cursor-not-allowed"
      >
        Following...
      </span>
    </div>

    <!-- 📷 Recipe Image -->
    <div class="relative h-52 overflow-hidden">
      <img
        :src="recipe.image || placeholderImage"
        :alt="recipe.recipeName"
        class="w-full h-full object-cover transition-transform duration-500 hover:scale-105"
        loading="lazy"
        @error="(e) => e.target.src = onerrorImage"
      />
      <div class="absolute bottom-2 left-2 flex gap-2">
        <span class="badge">{{ recipe?.complexityLevel?.name }}</span>
        <span class="badge flex items-center gap-1">
          <ClockIcon class="w-4 h-4" /> {{ formatCookTime(recipe?.cookTime) }}
        </span>
      </div>
    </div>

    <!-- 📝 Content -->
    <div class="p-4 space-y-2">
      <h3 class="text-lg font-semibold text-gray-800 dark:text-white">{{ recipe.recipeName }}</h3>
      <div class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-2">
        <GlobeIcon class="w-4 h-4" />
        <span>{{ recipe.cuisine.name }} • {{ recipe.cuisine.region }}</span>
      </div>

      <p class="text-sm text-gray-600 dark:text-gray-300">
        {{ truncateDescription(recipe.description) }}
        <button
          v-if="shouldShowMore"
          class="ml-1 text-[var(--theme-color)] font-medium"
          @click="showFullDescription = !showFullDescription"
        >
          {{ showFullDescription ? 'Show less' : 'Read more' }}
        </button>
      </p>

      <!-- 🏷️ Tags -->
      <div class="flex flex-wrap gap-2 pt-2">
        <span
          v-for="tag in recipe.tags.slice(0, 3)"
          :key="tag"
          class="text-xs px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-full"
        >
          #{{ tag }}
        </span>
      </div>
    </div>

    <!-- 📦 Footer -->
    <div class="flex justify-between items-center px-4 py-3 border-t border-gray-300 dark:border-gray-700">
      <div class="flex flex-wrap gap-2">
        <span
          v-for="cat in recipe.category"
          :key="cat"
          class="text-xs font-medium px-2 py-1 rounded-full"
          :style="{ backgroundColor: recipe.repiceColor + '33', color: recipe.repiceColor }"
        >
          {{ cat }}
        </span>
      </div>
      <router-link :to="recipeUrl(recipe.recipeName, recipe.id)">
        <RecipeButton :theme="recipe.repiceColor" />
      </router-link>
    </div>

    <!-- 🔍 Full Description Modal -->
    <div
      v-if="showFullDescription"
      class="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex justify-center items-center"
      @click.self="showFullDescription = false"
    >
      <div class="max-w-xl w-full bg-white dark:bg-gray-900 p-6 rounded-xl relative overflow-y-auto max-h-[80vh]">
        <button class="absolute top-4 right-4 text-xl font-bold" @click="showFullDescription = false">&times;</button>
        <h3 class="text-xl font-bold mb-4">About {{ recipe.recipeName }}</h3>
        <div v-html="recipe.description" class="prose dark:prose-invert"></div>
      </div>
    </div>

    <Toast position="bottom-center" group="bc" />
  </div>
</template>



<script setup>
import { ref, computed } from 'vue';
import onerrorImage from '../assets/onerrorimage.png'
import { useAuthStore } from '../store/user.js'
import { useToast } from 'primevue/usetoast'


// import { ClockIcon, GlobeIcon, ArrowRightIcon } from 'your-icon-library';
import RecipeButton from './RecipeViewButton.vue'
import { folow_unfollow } from '../apis';
import { boolean } from 'zod';
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
const toast = useToast()
const isFollowed = ref(false)


const auth = useAuthStore()
const isFollowing = ref(false)
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


const follow = async (chefId) => {
  isFollowing.value = true
  const res = await folow_unfollow(auth.token, chefId)

  isFollowing.value = false

  if (!res?.success) {
    toast.add({
      severity: 'error',
      summary: 'Follow Failed',
      detail: res.message || 'Unable to follow the user. Please try again.',
      group: 'bc',
      life: 4000
    })
    return
  }

  toast.add({
    severity: 'success',
    summary: 'Following',
    detail: `You're now following ${props.recipe.user?.name}`,
    group: 'bc',
    life: 3000
  })

  isFollowed.value = true
}

</script>