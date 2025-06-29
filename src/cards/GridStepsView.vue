<template>
  <div class="recipe-gallery">
    <!-- Grid Gallery with Enhanced Details -->
    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6 p-4">
      <div
        v-for="(step, index) in recipe.steps"
        :key="index"
        class="relative cursor-pointer group bg-white dark:bg-gray-800 rounded-xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-300 border border-gray-100 dark:border-gray-700"
        @click="openPreview(index)"
      >
        <!-- Media Container -->
        <div class="aspect-video relative">
          <!-- Video Thumbnail -->
          <div v-if="step.videoUrl" class="h-full w-full bg-gray-900 flex items-center justify-center">
            <div class="absolute inset-0 flex items-center justify-center">
              <div class="absolute inset-0 bg-black/30 group-hover:bg-black/10 transition-all flex items-center justify-center">
                <div class="w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm flex items-center justify-center">
                  <i class="pi pi-play text-white text-xl"></i>
                </div>
              </div>
            </div>
            <img 
              v-if="getVideoThumbnail(step.videoUrl)" 
              :src="getVideoThumbnail(step.videoUrl)" 
              class="w-full h-full object-cover opacity-80 group-hover:opacity-60 transition-opacity duration-300"
              alt="Video thumbnail"
            />
          </div>

          <!-- Image Thumbnail -->
          <img
            v-else-if="step.image"
            :src="step.image"
            class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            :alt="`Step ${index + 1}`"
            loading="lazy"
          />
          <div v-else class="w-full h-full bg-gradient-to-br from-gray-200 to-gray-300 dark:from-gray-700 dark:to-gray-600 flex items-center justify-center">
            <i class="pi pi-image text-gray-400 dark:text-gray-500 text-4xl"></i>
          </div>
          
          <!-- Step Badge -->
          <div class="absolute top-3 left-3 bg-white dark:bg-gray-900 text-gray-800 dark:text-white font-bold px-3 py-1 rounded-full text-sm shadow-sm">
            Step {{ index + 1 }}
          </div>
        </div>

        <!-- Step Info -->
        <div class="p-5">
          <!-- Time and Temp Indicators -->
          <div class="flex gap-2 mb-3">
            <span 
              v-if="getTotalTime(step.timeRequired) > 0"
              class="text-xs bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-200 px-3 py-1.5 rounded-full flex items-center"
            >
              <i class="pi pi-clock text-xs mr-1.5"></i>
              {{ formatShortTime(step.timeRequired) }}
            </span>
            <span 
              v-if="step.tempRequired > 0"
              class="text-xs bg-amber-100 dark:bg-amber-900/30 text-amber-800 dark:text-amber-200 px-3 py-1.5 rounded-full flex items-center"
            >
              <i class="pi pi-thermometer text-xs mr-1.5"></i>
              {{ step.tempRequired }}°C
            </span>
          </div>

          <!-- Instructions (with v-html) -->
          <div 
            class="text-gray-700 dark:text-gray-300 text-sm mb-4 line-clamp-3 prose dark:prose-invert prose-sm max-w-none"
            v-html="formatInstructions(step.instructions)"
          ></div>

          <!-- Ingredients -->
          <div v-if="step.ingredientsUsed?.length" class="mt-auto pt-3 border-t border-gray-100 dark:border-gray-700">
            <div class="text-xs font-semibold text-gray-500 dark:text-gray-400 mb-2 uppercase tracking-wider">
              Ingredients
            </div>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="(ingredient, idx) in step.ingredientsUsed"
                :key="idx"
                class="text-xs bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1 rounded-full flex items-center"
              >
                <i class="pi pi-circle-fill text-[6px] mr-2"></i>
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
      :showIndicators="true"
      :showThumbnailNavigators="true"
      :responsiveOptions="responsiveOptions"
      :circular="true"
      :autoPlay="false"
      :transitionInterval="3000"
      containerClass="fullscreen-galleria"
      @activeIndexChange="onIndexChange"
    >
      <template #item="slotProps">
        <div class="relative h-full w-full flex flex-col bg-gray-50 dark:bg-gray-900">
          <!-- Media Viewer -->
          <div class="flex-grow flex items-center justify-center bg-black relative">
            <!-- Video Player -->
            <div v-if="slotProps.item.videoUrl" class="w-full h-full">
              <iframe 
                v-if="isYoutubeUrl(slotProps.item.videoUrl)"
                :src="getYoutubeEmbedUrl(slotProps.item.videoUrl)" 
                class="w-full h-full"
                frameborder="0" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen
              ></iframe>
              <video 
                v-else 
                :src="slotProps.item.videoUrl" 
                controls 
                class="w-full h-full object-contain"
                autoplay
              ></video>
            </div>
            
            <!-- Image Viewer -->
            <img
              v-else-if="slotProps.item.image"
              :src="slotProps.item.image"
              class="max-w-full max-h-[70vh] object-contain"
              :alt="`Step ${slotProps.index + 1}`"
              loading="lazy"
            />
            
            <!-- Placeholder -->
            <div v-else class="w-full h-96 bg-gradient-to-br from-gray-200 to-gray-300 dark:from-gray-700 dark:to-gray-800 flex items-center justify-center">
              <div class="text-gray-500 dark:text-gray-400 text-center p-4">
                <i class="pi pi-image text-5xl mb-3 opacity-50"></i>
                <p class="text-sm">No media for this step</p>
              </div>
            </div>
            
            <!-- Step Counter -->
            <div class="absolute top-4 left-4 bg-black/50 text-white px-3 py-1 rounded-full text-sm">
              Step {{ slotProps.index + 1 }} of {{ recipe.steps.length }}
            </div>
          </div>

          <!-- Detailed Info Panel -->
          <div class="bg-white dark:bg-gray-800 p-6 shadow-inner overflow-y-auto" style="max-height: 40vh;">
            <div class="max-w-4xl mx-auto">
              <div class="flex flex-wrap justify-between items-start gap-4 mb-6">
                <h3 class="text-2xl font-bold text-gray-800 dark:text-white">
                  Step {{ slotProps.index + 1 }}
                </h3>
                <div class="flex gap-4">
                  <div v-if="getTotalTime(slotProps.item.timeRequired) > 0" class="flex items-center text-gray-600 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 px-3 py-1.5 rounded-full">
                    <i class="pi pi-clock mr-2 text-blue-500"></i>
                    <span class="text-sm font-medium">{{ formatTime(slotProps.item.timeRequired) }}</span>
                  </div>
                  <div v-if="slotProps.item.tempRequired > 0" class="flex items-center text-gray-600 dark:text-gray-300 bg-gray-100 dark:bg-gray-700 px-3 py-1.5 rounded-full">
                    <i class="pi pi-thermometer mr-2 text-amber-500"></i>
                    <span class="text-sm font-medium">{{ slotProps.item.tempRequired }}°C</span>
                  </div>
                </div>
              </div>

              <!-- Instructions with v-html -->
              <div 
                class="text-gray-700 dark:text-gray-300 mb-8 prose dark:prose-invert max-w-none"
                v-html="formatInstructions(slotProps.item.instructions)"
              ></div>

              <div v-if="slotProps.item.ingredientsUsed?.length" class="mb-8">
                <h4 class="text-lg font-semibold text-gray-800 dark:text-white mb-4 flex items-center">
                  <i class="pi pi-list mr-2 text-gray-500"></i>
                  Ingredients Used
                </h4>
                <ul class="grid grid-cols-1 sm:grid-cols-2 gap-3">
                  <li 
                    v-for="(ingredient, idx) in slotProps.item.ingredientsUsed"
                    :key="idx"
                    class="flex items-start py-2 px-4 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                  >
                    <i class="pi pi-circle-fill text-[8px] mt-2 mr-3 text-gray-500 flex-shrink-0"></i>
                    <span class="text-gray-700 dark:text-gray-300">
                      {{ formatIngredient(ingredient) }}
                    </span>
                  </li>
                </ul>
              </div>

              <div v-if="slotProps.item.notes" class="bg-blue-50 dark:bg-blue-900/20 p-5 rounded-xl border border-blue-100 dark:border-blue-900/30">
                <h4 class="font-semibold text-blue-800 dark:text-blue-200 mb-3 flex items-center">
                  <i class="pi pi-info-circle mr-2"></i>
                  Chef's Notes
                </h4>
                <div 
                  class="text-blue-700 dark:text-blue-300 prose dark:prose-invert prose-sm max-w-none"
                  v-html="formatInstructions(slotProps.item.notes)"
                ></div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <template #thumbnail="slotProps">
        <div class="relative w-20 h-20 overflow-hidden">
          <img 
            v-if="slotProps.item.image" 
            :src="slotProps.item.image" 
            class="w-full h-full object-cover rounded-lg transition-transform duration-300 hover:scale-110"
            :alt="`Step ${slotProps.index + 1}`"
            loading="lazy"
          />
          <div v-else-if="slotProps.item.videoUrl" class="w-full h-full bg-blue-900 flex items-center justify-center rounded-lg">
            <i class="pi pi-video text-white/80 text-xl"></i>
          </div>
          <div v-else class="w-full h-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center rounded-lg">
            <i class="pi pi-image text-gray-500 text-xl"></i>
          </div>
          <div class="absolute bottom-2 right-2 bg-black/80 text-white text-xs font-bold px-2 py-0.5 rounded-full">
            {{ slotProps.index + 1 }}
          </div>
        </div>
      </template>
      
      <template #indicator="slotProps">
        <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 flex gap-2">
          <button 
            v-for="(_, idx) in recipe.steps"
            :key="idx"
            @click="onIndexChange(idx)"
            class="w-3 h-3 rounded-full transition-all"
            :class="{
              'bg-white scale-125': idx === slotProps.index,
              'bg-white/40 hover:bg-white/60': idx !== slotProps.index
            }"
            aria-label="Go to slide"
          ></button>
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
    breakpoint: '1536px',
    numVisible: 7
  },
  {
    breakpoint: '1280px',
    numVisible: 5
  },
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
  if (totalMinutes < 60) return `${totalMinutes} min`;
  
  const hours = Math.floor(totalMinutes / 60);
  const minutes = totalMinutes % 60;
  return `${hours}h${minutes > 0 ? ` ${minutes}min` : ''}`;
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

function formatInstructions(text) {
  if (!text) return '';
  // Basic sanitization and formatting
  return text
    .replace(/\n/g, '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>');
}

function isYoutubeUrl(url) {
  return url?.includes('youtube.com') || url?.includes('youtu.be');
}

function getYoutubeEmbedUrl(url) {
  if (!url) return '';
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
  const match = url.match(regExp);
  const videoId = (match && match[2].length === 11) ? match[2] : null;
  return `https://www.youtube.com/embed/${videoId}?autoplay=1&modestbranding=1&rel=0`;
}

function getVideoThumbnail(url) {
  if (isYoutubeUrl(url)) {
    const videoId = url.match(/(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))([^&?]+)/)?.[1];
    return videoId ? `https://img.youtube.com/vi/${videoId}/hqdefault.jpg` : null;
  }
  return null;
}
</script>

<style scoped>
.recipe-gallery {
  --gallery-gap: 1.5rem;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

:deep(.fullscreen-galleria) {
  /* --galleria-bg: theme('colors.gray.900'); */
  background-color: rgba(86, 83, 83, 0.761);
}

:deep(.p-galleria-thumbnail-wrapper) {
  background: rgba(0, 0, 0, 0.9);
  padding: 1.5rem;
  /* border-top: 1px solid theme('colors.gray.800'); */
}

:deep(.p-galleria-thumbnail-container) {
  padding: 0.5rem;
}

:deep(.p-galleria-thumbnail-item) {
  opacity: 0.6;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  margin: 0 0.25rem;
}

:deep(.p-galleria-thumbnail-item:hover),
:deep(.p-galleria-thumbnail-item.p-highlight) {
  opacity: 1;
  /* border-color: theme('colors.blue.500'); */
  transform: translateY(-4px);
}

:deep(.p-galleria-thumbnail-prev),
:deep(.p-galleria-thumbnail-next) {
  color: white;
  background: rgba(0, 0, 0, 0.5);
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  margin: 0 1rem;
}

:deep(.p-galleria-thumbnail-prev:hover),
:deep(.p-galleria-thumbnail-next:hover) {
  background: rgba(0, 0, 0, 0.8);
}

:deep(.p-galleria-item-nav) {
  background: rgba(0, 0, 0, 0.5);
  color: white;
  width: 3rem;
  height: 3rem;
  border-radius: 50%;
  transition: all 0.3s;
}

:deep(.p-galleria-item-nav:hover) {
  background: rgba(0, 0, 0, 0.8);
  transform: scale(1.1);
}

:deep(.p-galleria-close) {
  color: white;
  background: rgba(0, 0, 0, 0.5);
  width: 2.5rem;
  height: 2.5rem;
  border-radius: 50%;
  top: 1rem;
  right: 1rem;
  transition: all 0.3s;
}

:deep(.p-galleria-close:hover) {
  background: rgba(0, 0, 0, 0.8);
  transform: rotate(90deg);
}
</style>