<template>
  <div class="recipe-gallery">
    <!-- Grid Gallery with Enhanced Details -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <div
        v-for="(step, index) in recipe.steps"
        :key="index"
        class="relative cursor-pointer group bg-white dark:bg-gray-800 rounded-lg overflow-hidden shadow-md hover:shadow-lg transition-all duration-300"
        @click="openPreview(index)"
      >
        <!-- Media Container -->
        <div class="aspect-video relative">
          <!-- Video Thumbnail -->
          <div v-if="step.videoUrl" class="h-full w-full bg-gray-900 flex items-center justify-center">
            <div class="absolute inset-0 flex items-center justify-center">
              <i class="pi pi-video text-white text-2xl z-10"></i>
              <div class="absolute inset-0 bg-black/30 group-hover:bg-black/10 transition-all"></div>
            </div>
            <img 
              v-if="getVideoThumbnail(step.videoUrl)" 
              :src="getVideoThumbnail(step.videoUrl)" 
              class="w-full h-full object-cover opacity-70 group-hover:opacity-50 transition-opacity"
              alt="Video thumbnail"
            />
          </div>

          <!-- Image Thumbnail -->
          <img
            v-else-if="step.image"
            :src="step.image"
            class="w-full h-full object-cover"
            :alt="`Step ${index + 1}`"
          />
          <div v-else class="w-full h-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
            <i class="pi pi-image text-gray-500 dark:text-gray-400 text-2xl"></i>
          </div>
        </div>

        <!-- Step Info Overlay -->
        <div class="p-4">
          <div class="flex justify-between items-start mb-2">
            <span class="font-bold text-lg text-gray-800 dark:text-white">
              Step {{ index + 1 }}
            </span>
            <div class="flex gap-2">
              <span 
                v-if="getTotalTime(step.timeRequired) > 0"
                class="text-xs bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-2 py-1 rounded-full flex items-center"
              >
                <i class="pi pi-clock text-xs mr-1"></i>
                {{ formatShortTime(step.timeRequired) }}
              </span>
              <span 
                v-if="step.tempRequired > 0"
                class="text-xs bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-2 py-1 rounded-full flex items-center"
              >
                <i class="pi pi-thermometer text-xs mr-1"></i>
                {{ step.tempRequired }}°C
              </span>
            </div>
          </div>

          <p class="text-gray-600 dark:text-gray-300 text-sm mb-3 line-clamp-2">
            {{ step.instructions }}
          </p>

          <div v-if="step.ingredientsUsed?.length" class="mt-2">
            <div class="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-1">
              INGREDIENTS:
            </div>
            <div class="flex flex-wrap gap-1">
              <span
                v-for="(ingredient, idx) in step.ingredientsUsed"
                :key="idx"
                class="text-xs bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-2 py-1 rounded-full"
              >
                {{ formatIngredient(ingredient) }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Fullscreen Preview with Complete Details -->
    <Galleria
      v-model:visible="displayFullscreen"
      :value="recipe.steps"
      :activeIndex="activeIndex"
      :fullScreen="true"
      :showThumbnails="true"
      :showItemNavigators="true"
      :responsiveOptions="responsiveOptions"
      @activeIndexChange="onIndexChange"
    >
      <template #item="slotProps">
        <div class="relative h-full w-full flex flex-col">
          <!-- Media Viewer -->
          <div class="flex-grow flex items-center justify-center bg-black">
            <!-- Video Player -->
            <div v-if="slotProps.item.videoUrl" class="w-full h-full">
              <iframe 
                v-if="isYoutubeUrl(slotProps.item.videoUrl)"
                :src="getYoutubeEmbedUrl(slotProps.item.videoUrl)" 
                class="w-full h-full"
                frameborder="0" 
                allowfullscreen
              ></iframe>
              <video v-else :src="slotProps.item.videoUrl" controls class="w-full h-full object-contain"></video>
            </div>
            
            <!-- Image Viewer -->
            <img
              v-else-if="slotProps.item.image"
              :src="slotProps.item.image"
              class="max-w-full max-h-[70vh] object-contain"
              :alt="`Step ${slotProps.index + 1}`"
            />
            
            <!-- Placeholder -->
            <div v-else class="w-full h-96 bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
              <div class="text-gray-500 dark:text-gray-400 text-center p-4">
                <i class="pi pi-image text-4xl mb-2"></i>
                <p>No media for this step</p>
              </div>
            </div>
          </div>

          <!-- Detailed Info Panel -->
          <div class="bg-white dark:bg-gray-800 p-6 shadow-lg">
            <div class="max-w-4xl mx-auto">
              <div class="flex justify-between items-start mb-4">
                <h3 class="text-2xl font-bold text-gray-800 dark:text-white">
                  Step {{ slotProps.index + 1 }}
                </h3>
                <div class="flex gap-3">
                  <div v-if="getTotalTime(slotProps.item.timeRequired) > 0" class="flex items-center text-gray-600 dark:text-gray-300">
                    <i class="pi pi-clock mr-2"></i>
                    <span>{{ formatTime(slotProps.item.timeRequired) }}</span>
                  </div>
                  <div v-if="slotProps.item.tempRequired > 0" class="flex items-center text-gray-600 dark:text-gray-300">
                    <i class="pi pi-thermometer mr-2"></i>
                    <span>{{ slotProps.item.tempRequired }}°C</span>
                  </div>
                </div>
              </div>

              <p class="text-gray-700 dark:text-gray-300 mb-6 whitespace-pre-line">
                {{ slotProps.item.instructions }}
              </p>

              <div v-if="slotProps.item.ingredientsUsed?.length" class="mb-6">
                <h4 class="text-lg font-semibold text-gray-800 dark:text-white mb-3">
                  Ingredients Used in This Step
                </h4>
                <ul class="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  <li 
                    v-for="(ingredient, idx) in slotProps.item.ingredientsUsed"
                    :key="idx"
                    class="flex items-center py-2 px-3 bg-gray-50 dark:bg-gray-700 rounded-lg"
                  >
                    <i class="pi pi-circle-fill text-[8px] mr-3 text-gray-500"></i>
                    <span class="text-gray-700 dark:text-gray-300">
                      {{ formatIngredient(ingredient) }}
                    </span>
                  </li>
                </ul>
              </div>

              <div v-if="slotProps.item.notes" class="bg-yellow-50 dark:bg-yellow-900/20 p-4 rounded-lg">
                <h4 class="font-semibold text-yellow-800 dark:text-yellow-200 mb-2">Chef's Notes</h4>
                <p class="text-yellow-700 dark:text-yellow-300 whitespace-pre-line">
                  {{ slotProps.item.notes }}
                </p>
              </div>
            </div>
          </div>
        </div>
      </template>

      <template #thumbnail="slotProps">
        <div class="relative w-16 h-16">
          <img 
            v-if="slotProps.item.image" 
            :src="slotProps.item.image" 
            class="w-full h-full object-cover rounded-sm"
            :alt="`Step ${slotProps.index + 1}`"
          />
          <div v-else-if="slotProps.item.videoUrl" class="w-full h-full bg-blue-900 flex items-center justify-center rounded-sm">
            <i class="pi pi-video text-white"></i>
          </div>
          <div v-else class="w-full h-full bg-gray-200 flex items-center justify-center rounded-sm">
            <i class="pi pi-image text-gray-500"></i>
          </div>
          <div class="absolute bottom-1 right-1 bg-black/70 text-white text-xs px-1 rounded">
            {{ slotProps.index + 1 }}
          </div>
        </div>
      </template>
    </Galleria>
  </div>
</template>

<script setup>
import Galleria from 'primevue/galleria';
import { ref, computed } from 'vue';

const props = defineProps({
  recipe: {
    type: Object,
    required: true,
    default: () => ({
      steps: []
    })
  },
  activeIndex: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['update:activeIndex']);

const displayFullscreen = ref(false);
const responsiveOptions = ref([
  {
    breakpoint: '1024px',
    numVisible: 5
  },
  {
    breakpoint: '768px',
    numVisible: 3
  },
  {
    breakpoint: '560px',
    numVisible: 1
  }
]);

function openPreview(index) {
  emit('update:activeIndex', index);
  displayFullscreen.value = true;
}

function onIndexChange(val) {
  emit('update:activeIndex', val);
}

function getTotalTime(timeObj) {
  if (!timeObj) return 0;
  return (timeObj.hr || 0) * 60 + (timeObj.min || 0);
}

function formatTime(timeObj) {
  if (!timeObj) return '';
  const totalMinutes = getTotalTime(timeObj);
  if (totalMinutes < 60) return `${totalMinutes} minutes`;
  
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  return `${hours} hour${hours !== 1 ? 's' : ''}${minutes > 0 ? ` ${minutes} minute${minutes !== 1 ? 's' : ''}` : ''}`;
}

function formatShortTime(timeObj) {
  if (!timeObj) return '';
  const totalMinutes = getTotalTime(timeObj);
  if (totalMinutes < 60) return `${totalMinutes}m`;
  return `${Math.floor(totalMinutes / 60)}h${totalMinutes % 60 > 0 ? `${totalMinutes % 60}m` : ''}`;
}

function formatIngredient(ingredient) {
  if (typeof ingredient === 'string') return ingredient;
  if (!ingredient.amount) return ingredient.name;
  return `${ingredient.name} (${ingredient.amount}${ingredient.unit ? ` ${ingredient.unit}` : ''})`;
}

function isYoutubeUrl(url) {
  return url?.includes('youtube.com') || url?.includes('youtu.be');
}

function getYoutubeEmbedUrl(url) {
  if (!url) return '';
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
  const match = url.match(regExp);
  const videoId = (match && match[2].length === 11) ? match[2] : null;
  return `https://www.youtube.com/embed/${videoId}?autoplay=0&modestbranding=1`;
}

function getVideoThumbnail(url) {
  if (isYoutubeUrl(url)) {
    const videoId = url.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([^&?]+)/)?.[1];
    return videoId ? `https://img.youtube.com/vi/${videoId}/mqdefault.jpg` : null;
  }
  return null;
}
</script>

<style scoped>
.recipe-gallery {
  --gallery-gap: 1rem;
}

:deep(.p-galleria-thumbnail-wrapper) {
  background: rgba(0, 0, 0, 0.8);
  padding: 1rem;
}

:deep(.p-galleria-thumbnail-item) {
  opacity: 0.7;
  transition: opacity 0.2s;
  border: 2px solid transparent;
}

:deep(.p-galleria-thumbnail-item:hover),
:deep(.p-galleria-thumbnail-item.p-highlight) {
  opacity: 1;
  border-color: var(--primary-color);
}

.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>