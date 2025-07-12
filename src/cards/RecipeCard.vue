<template>
  <div
    class="min-w-[300px] bg-white relative dark:bg-gray-900 shadow-md hover:shadow-xl rounded-lg overflow-hidden transition-all duration-300 hover:-translate-y-1 flex flex-col h-full"
    :style="{ '--theme-color': recipe?.repiceColor || '#f97316' }">
    <!-- 👤 User Header -->
    <div class="flex justify-between items-center px-4 py-3 border-b border-gray-300 dark:border-gray-700">
      <div class="flex items-center gap-3">
        <img :src="recipe.user?.profilePic || defaultAvatar" :alt="recipe.user?.name"
          class="w-10 h-10 rounded-full object-cover" />
        <div>
          <h4 class="text-sm font-semibold text-gray-800 dark:text-white">{{ recipe.user?.name }}</h4>
          <p class="text-xs text-gray-500 dark:text-gray-400">{{ recipe.user?.totalRecipes }} recipes shared</p>
        </div>
      </div>
      <button v-if="!NowFollowing" @click="follow(recipe.user.id)"
        class="text-xs px-3 py-1 rounded-full border border-[var(--theme-color)] text-[var(--theme-color)] hover:bg-[var(--theme-color)] hover:text-white transition">
        <span v-if="recipe?.recipeMeta?.isFollowing">Following</span><span v-else>Follow</span>
      </button>
      <span v-else-if="NowFollowing"
        class="text-xs px-3 py-1 rounded-full border border-[var(--theme-color)] text-[var(--theme-color)] opacity-70 cursor-not-allowed">
         <span v-if="recipe?.recipeMeta?.isFollowing">Unfollowing...</span><span v-else>Following...</span>
      </span>
    </div>

    <!-- 📷 Recipe Image with Action Buttons -->
    <div class="relative h-65 overflow-hidden group">
      <img :src="recipe.image || placeholderImage" :alt="recipe.recipeName"
        class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105" loading="lazy"
        @error="(e) => e.target.src = onerrorImage" />

      <!-- Image overlay buttons -->
      <div
        class="absolute bottom-2 right-2 flex gap-2 opacity-70 group-hover:opacity-100 transition-opacity duration-300">
        <button @click.stop="toggleLike"
          class="flex flex-row justify-center items-center gap-1 cursor-pointer text-xs px-3 py-1 rounded-full border border-[var(--theme-color)] text-[var(--theme-color)] hover:bg-[var(--theme-color)] hover:text-white transition"
          :class="{ 'bg-[var(--theme-color)] text-white': recipe?.recipeMeta?.isLiked }">
          <i :class="recipe?.recipeMeta?.isLiked ? 'pi pi-heart-fill' : 'pi pi-heart'"></i><span>{{ recipe?.recipeMeta?.likeCount }}</span>
        </button>
        <button @click.stop="toggleSave"
          class="cursor-pointer text-xs px-3 py-1 rounded-full border border-[var(--theme-color)] text-[var(--theme-color)] hover:bg-[var(--theme-color)] hover:text-white transition"
          :class="{ 'bg-[var(--theme-color)] text-white': recipe?.recipeMeta?.isSaved }">
          <i :class="recipe?.recipeMeta?.isSaved ? 'pi pi-bookmark-fill' : 'pi pi-bookmark'"></i>
        </button>
      </div>

      <div class="absolute bottom-2 left-2 flex gap-2">
        <span class="badge rounded-2xl bg-white/40 dark:bg-gray-800/40 px-2 border border-[var(--theme-color)]">{{ recipe?.complexityLevel?.name }}</span>
        <span class="badge flex items-center gap-1 px-2  bg-white/40 dark:bg-gray-800/40 rounded-2xl border border-[var(--theme-color)]" >
          <ClockIcon class="w-4 h-4" /> {{ formatCookTime(recipe?.cookTime) }}
        </span>
      </div>
    </div>

    <!-- 📝 Content -->
    <div class="p-4 space-y-2 flex-grow">
      <h3 class="text-lg font-semibold text-gray-800 dark:text-white">{{ recipe.recipeName }}</h3>
      <div class="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-2">
        <GlobeIcon class="w-4 h-4" />
        <span>{{ recipe.cuisine.name }} • {{ recipe.cuisine.region }}</span>
      </div>

      <p class="text-sm text-gray-600 dark:text-gray-300">
        {{ truncateDescription(recipe.description) }}
        <button v-if="shouldShowMore" class="ml-1 text-[var(--theme-color)] font-medium hover:underline"
          @click="showFullDescription = !showFullDescription">
          {{ showFullDescription ? 'Show less' : 'Read more' }}
        </button>
      </p>

      <!-- 🏷️ Tags -->
      <div class="flex flex-wrap gap-2 pt-2">
        <span v-for="tag in recipe.tags.slice(0, 3)" :key="tag"
          class="text-xs px-2 py-1 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-full">
          #{{ tag }}
        </span>
      </div>
    </div>

    <!-- 📦 Footer with Action Buttons -->
    <div class="flex justify-between items-center px-4 py-3 border-t border-gray-300 dark:border-gray-700">
      <div class="flex flex-wrap gap-2">
        <span v-for="cat in recipe.category" :key="cat" class="text-xs font-medium px-2 py-1 rounded-full"
          :style="{ backgroundColor: recipe.repiceColor + '33', color: recipe.repiceColor }">
          {{ cat }}
        </span>
      </div>

      <div class="flex gap-2">
        <button @click="toggleLike"
          class="flex items-center gap-1 text-sm p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition"
          :class="{ 'text-red-500': isLiked }">
          <HeartIcon class="w-5 h-5" :fill="isLiked ? 'currentColor' : 'none'" />
          <span class="sr-only">Like</span>
          <span v-if="likeCount > 0" class="text-xs">{{ likeCount }}</span>
        </button>

        <button @click="toggleSave"
          class="flex items-center gap-1 text-sm p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition"
          :class="{ 'text-[var(--theme-color)]': isSaved }">
          <BookmarkIcon class="w-5 h-5" :fill="isSaved ? 'currentColor' : 'none'" />
          <span class="sr-only">Save</span>
        </button>

        <router-link :to="recipeUrl(recipe.recipeName, recipe.id)">
          <RecipeButton :theme="recipe.repiceColor" />
        </router-link>
      </div>
    </div>

    <!-- 🔍 Full Description Modal - Now card-contained -->
    <div v-if="showFullDescription"
      class="absolute inset-0 z-10 bg-white dark:bg-gray-900 rounded-lg overflow-y-auto shadow-2xl border-2 border-[var(--theme-color)]/30"
      @click.self="showFullDescription = false">
      <div class="p-6">
        <button
          class="absolute top-4 right-4 text-xl font-bold text-gray-500 hover:text-gray-700 dark:hover:text-gray-300 transition"
          @click="showFullDescription = false">
          &times;
        </button>
        <h3 class="text-xl font-bold mb-4 text-[var(--theme-color)]">About {{ recipe.recipeName }}</h3>
        <div v-html="recipe.description" class="prose dark:prose-invert max-w-none"></div>

        <div class="mt-6 flex justify-end">
          <button @click="showFullDescription = false"
            class="px-4 py-2 rounded-full bg-[var(--theme-color)] text-white hover:opacity-90 transition">
            Close
          </button>
        </div>
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
import { like_unlike, save_unsave_favourites } from '../apis/index.js'


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
      recipeMeta: {
        isLiked: false,
        isSaved: false,
        likeCount: 0,
        isFollowing: false,
        views: 0,
        comments: 0
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


const NowFollowing = ref(false)
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
  NowFollowing.value = true
  const res = await folow_unfollow(auth.token, chefId)

  props.recipe.recipeMeta.isFollowing = !props.recipe.recipeMeta.isFollowing

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
    severity: res?.success ? 'info' : 'error',
    summary: res?.success && props.recipe.recipeMeta.isFollowing ? 'Followed' : 'Unfollowed',
    detail: res?.success && props.recipe.recipeMeta.isFollowing ? `You're now following ${props.recipe.user?.name}` : `You have unfollowed ${props.recipe.user?.name}` || 'Unable to follow the user. Please try again.',
    group: 'bc',
    life: 3000
  })

  NowFollowing.value = false
}


const toggleLike = async () => {
    const res = await like_unlike(auth.token, props.recipe.id)
    if (res.success) {
        props.recipe.recipeMeta.isLiked = !props.recipe.recipeMeta.isLiked
        props.recipe.recipeMeta.likeCount += props.recipe.recipeMeta.isLiked ? 1 : -1
    } else {
        toast.add({
            severity: 'error',
            summary: 'Failed to like',
            detail: `${res.message} || 'failed!!'`,
            group: 'bc',
            life: 2000
        });
    }
}

const toggleSave = async () => {
    const res = await save_unsave_favourites(auth.token, props.recipe.id);

    if (res.success) {
        const isNowSaved = !props.recipe.recipeMeta.value.isSaved;

        toast.add({
            severity: isNowSaved ? 'success' : 'info',
            summary: isNowSaved ? 'Recipe Saved' : 'Recipe Removed',
            detail: isNowSaved
                ? `You’ve saved “${props.recipe.recipeName}” to your favorites.`
                : `You’ve removed “${props.recipe.recipeName}” from your favorites.`,
            group: 'bc',
            life: 2500,
        });

        props.recipe.recipeMeta.isSaved = isNowSaved;
    } else {
        toast.add({
            severity: 'error',
            summary: 'Action Failed',
            detail: res.message || `Something went wrong while updating favorites.`,
            group: 'bc',
            life: 2500,
        });
    }
};


</script>