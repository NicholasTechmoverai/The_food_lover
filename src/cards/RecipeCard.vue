<template>
  <div 
    class="max-w-sm mx-auto bg-white dark:bg-gray-900 rounded-2xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1 group"
    :style="{ '--theme-color': recipe.repiceColor || '#f97316' }"
  >
    <!-- Image with theme-colored overlay -->
    <div class="relative overflow-hidden h-56">
      <Image 
        :src="recipe.image" 
        :alt="recipe.name" 
        preview 
        class=" object-cover transition-transform duration-500 group-hover:scale-105" 
      />
      <div class="absolute inset-0 bg-gradient-to-t from-[var(--theme-color)]/80 to-transparent flex flex-col justify-end p-4">
        <div class="flex items-center justify-between">
          <span class="text-white bg-[var(--theme-color)]/90 px-3 py-1 rounded-full text-xs font-medium">
            {{ recipe.cookTime.hr }}h {{ recipe.cookTime.min }}m
          </span>
          <button class="text-white hover:text-white/80 transition-colors" aria-label="Save recipe">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z" />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <div class="p-5">
      <!-- Recipe title -->
      <h2 class="text-xl font-bold text-gray-800 dark:text-white line-clamp-1 mb-2">
        {{ recipe.recipeName }}
      </h2>

      <!-- Description with show more -->
      <div class="mb-3 relative">
        <p 
          ref="description"
          class="text-gray-600 dark:text-gray-300 text-sm transition-all duration-200"
          :class="showFullDescription ? '' : 'line-clamp-2'"
        >
          {{ recipe.description }}
        </p>
        <button 
          v-if="shouldShowToggle"
          @click="showFullDescription = !showFullDescription"
          class="text-xs mt-1 text-[var(--theme-color)] hover:text-[var(--theme-color)]/80 font-medium flex items-center gap-1"
        >
          {{ showFullDescription ? 'Show less' : 'Show more' }}
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="h-3 w-3 transition-transform duration-200" 
            :class="{ 'rotate-180': showFullDescription }"
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>

      <!-- Recipe preview content -->
      <div class="mb-4 relative">
        <div 
          class="prose dark:prose-invert max-w-none text-sm text-gray-600 dark:text-gray-300 transition-all duration-200"
          :class="showFullContent ? '' : 'line-clamp-3'"
          
        >
        <div v-html="recipe.recipeContent" class="w-full break-words"></div>
          <!-- Simple text extraction from HTML content -->
          <!-- {{ stripHtml(recipe.recipeContent) }} -->
        </div>
        <button 
          v-if="recipe.recipeContent && recipe.recipeContent.length > 100"
          @click="showFullContent = !showFullContent"
          class="text-xs mt-1 text-[var(--theme-color)] hover:text-[var(--theme-color)]/80 font-medium flex items-center gap-1"
        >
          {{ showFullContent ? 'Show less' : 'Show more steps' }}
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="h-3 w-3 transition-transform duration-200" 
            :class="{ 'rotate-180': showFullContent }"
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>

      <!-- Tags -->
      <div class="flex flex-wrap gap-2 mb-4">
        <span 
          v-for="tag in recipe.tags" 
          :key="tag.name"
          class="text-xs px-2.5 py-1 bg-[var(--theme-color)]/10 text-[var(--theme-color)] dark:bg-[var(--theme-color)]/20 dark:text-[var(--theme-color)]/90 rounded-full hover:bg-[var(--theme-color)]/20 dark:hover:bg-[var(--theme-color)]/30 transition-colors"
        >
          #{{ tag }}
        </span>
      </div>

      <!-- Action buttons -->
      <div class="flex justify-between items-center border-t border-gray-100 dark:border-gray-700 pt-4">
        <button class="text-sm font-medium text-[var(--theme-color)] hover:text-[var(--theme-color)]/80 flex items-center gap-1 transition-colors">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
          </svg>
          Preview
        </button>
        <button 
          class="px-4 py-2 bg-[var(--theme-color)] hover:bg-[var(--theme-color)]/90 text-white text-sm font-medium rounded-lg transition-colors flex items-center gap-1"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          Cook This
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const props = defineProps({
  recipe: {
    type: Object,
    required: true
  }
});

const showFullDescription = ref(false);
const showFullContent = ref(false);
const description = ref(null);
const shouldShowToggle = ref(false);

// Check if description needs toggle
onMounted(() => {
  if (description.value) {
    shouldShowToggle.value = description.value.scrollHeight > description.value.clientHeight;
  }
});

// Simple HTML stripper for recipe content preview
const stripHtml = (html) => {
  if (!html) return '';
  return html.replace(/<[^>]*>/g, ' ');
};
</script>

<style>
/* Fallback for older browsers */
:root {
  --theme-color: #f97316;
}
</style>