<template>
  <div class="recipe-galleria">
    <Galleria
      ref="galleria"
      :value="recipe.steps"
      :numVisible="5"
      :circular="true"
      :autoPlay="isAutoPlay"
      :transitionInterval="3000"
      :activeIndex="activeIndex"
      :showThumbnails="showThumbnails"
      :showIndicators="true"
      :showItemNavigators="true"
      :responsiveOptions="responsiveOptions"
      @activeIndexChange="onIndexChange"
      :pt="{
        root: {
          class: [{ 'flex flex-col': fullScreen }]
        },
        content: {
          class: ['relative', { 'flex-1 justify-center': fullScreen }]
        },
        thumbnails: 'absolute w-full left-0 bottom-0'
      }"
    >
      <!-- Slide Item View -->
      <template #item="{ item, index }">
        <div class="relative h-full flex flex-col md:flex-row gap-4 p-4">
          <!-- Media Column -->
          <div class="w-full md:w-1/2 h-96 flex-shrink-0">
            <!-- Media: YouTube / video / image -->
            <div v-if="item.videoUrl" class="media-container bg-black rounded-lg h-full">
              <iframe
                v-if="isYoutubeUrl(item.videoUrl)"
                :src="getYoutubeEmbedUrl(item.videoUrl)"
                frameborder="0"
                allowfullscreen
                class="w-full h-full"
                title="Step Video"
              ></iframe>
              <video
                v-else
                :src="item.videoUrl"
                controls
                class="w-full h-full object-contain"
              ></video>
            </div>

            <div v-else-if="item.image" class="h-full">
              <img
                :src="item.image"
                :alt="`Step ${item.no || index + 1} image`"
                class="w-full h-full object-cover rounded-lg"
              />
            </div>

            <div v-else class="w-full h-full bg-gray-100 dark:bg-gray-800 flex items-center justify-center rounded-lg">
              <div class="text-center text-gray-500 dark:text-gray-400">
                <i class="pi pi-image text-4xl mb-2"></i>
                <p>No media available</p>
              </div>
            </div>
          </div>

          <!-- Content Column -->
          <div class="w-full md:w-1/2 flex flex-col border rounded border-gray-200 dark:border-gray-700">
            <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm flex-1 flex flex-col">
              <!-- Step Header -->
              <div class="flex justify-between items-start mb-4">
                <h3 class="text-xl font-bold text-gray-900 dark:text-white">
                  Step {{ item.no || index + 1 }}
                </h3>
                <div class="flex gap-2">
                  <div v-if="getTotalTime(item.timeRequired) > 0" class="bg-primary-100 dark:bg-primary-900 text-primary-800 dark:text-primary-100 px-3 py-1 rounded-full text-sm">
                    <i class="pi pi-clock mr-1"></i>{{ formatTime(item.timeRequired) }}
                  </div>
                  <div v-if="item.tempRequired > 0" class="bg-amber-100 dark:bg-amber-900 text-amber-800 dark:text-amber-100 px-3 py-1 rounded-full text-sm">
                    <i class="pi pi-thermometer mr-1"></i>{{ item.tempRequired }}°C
                  </div>
                </div>
              </div>

              <!-- Instructions -->
              <div class="flex-1 mb-4 overflow-y-auto">
                <div 
                  class="text-gray-700 dark:text-gray-300 break-words whitespace-pre-line leading-relaxed" 
                  v-html="formatInstructions(item.instructions || 'No instructions provided')"
                ></div>
              </div>

              <!-- Ingredients -->
              <div v-if="item.ingredientsUsed?.length" class="mt-auto pt-4 border-t border-gray-200 dark:border-gray-700">
                <h4 class="text-sm font-semibold text-gray-500 dark:text-gray-400 mb-2">INGREDIENTS FOR THIS STEP</h4>
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="(ingredient, i) in item.ingredientsUsed"
                    :key="i"
                    class="text-xs bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 px-3 py-1.5 rounded-full flex items-center hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
                  >
                    <i class="pi pi-circle-fill text-[8px] mr-2 text-primary-500"></i>
                    {{ formatIngredient(ingredient) }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>

      <!-- Thumbnail View -->
      <template #thumbnail="{ item, index }">
        <div class="relative w-24 h-16 rounded-md overflow-hidden border-2 border-transparent hover:border-primary-400 transition-all">
          <img
            v-if="item.image"
            :src="item.image"
            :alt="`Step ${item.no || index + 1} thumbnail`"
            class="w-full h-full object-cover"
          />
          <div
            v-else-if="item.videoUrl"
            class="w-full h-full bg-blue-900/80 flex items-center justify-center"
          >
            <i class="pi pi-video text-white text-lg"></i>
          </div>
          <div
            v-else
            class="w-full h-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center"
          >
            <i class="pi pi-image text-gray-500 dark:text-gray-400"></i>
          </div>
          <span class="absolute bottom-1 right-1 bg-black/80 text-white text-xs px-1.5 py-0.5 rounded-full">
            {{ item.no || index + 1 }}
          </span>
        </div>
      </template>

      <!-- Caption (Recipe Name) -->
      <!-- <template #caption v-if="recipe.name">
        <div class="bg-gradient-to-r from-primary-600 to-primary-800 text-white text-xl md:text-2xl font-bold text-center p-3 rounded-t-lg shadow-md">
          <div class="flex items-center justify-center gap-2">
            <i class="pi pi-bookmark"></i>
            <span>{{ recipe.name }}</span>
          </div>
          <div v-if="recipe.description" class="text-sm font-normal mt-1 opacity-90">
            {{ recipe.description }}
          </div>
        </div>
      </template> -->

      <!-- Footer with controls -->
      <template #footer>
        <div class="flex items-stretch bg-surface-900 text-gray-600 dark:text-white h-12 rounded-b-lg overflow-hidden">
          <button 
            type="button" 
            @click="onThumbnailButtonClick" 
            class="bg-transparent border-none hover:bg-white/10  text-gray-600 dark:text-white inline-flex justify-center items-center cursor-pointer px-4 transition-colors"
            :title="showThumbnails ? 'Hide thumbnails' : 'Show thumbnails'"
          >
            <i class="pi pi-th-large"></i>
          </button>
          <button 
            type="button" 
            @click="toggleAutoSlide" 
            class="bg-transparent border-none hover:bg-white/10 text-gray-600 dark:text-white inline-flex justify-center items-center cursor-pointer px-4 transition-colors"
            :title="isAutoPlay ? 'Pause slideshow' : 'Play slideshow'"
          >
            <i :class="slideButtonIcon"></i>
          </button>
          <span v-if="recipe.steps" class="flex items-center gap-4 ml-3 text-sm">
            <span class="bg-white/10 px-3 py-1 rounded-full">{{ activeIndex + 1 }}/{{ recipe.steps.length }}</span>
            <span class="font-bold">Step {{ recipe.steps[activeIndex].no || activeIndex + 1 }}</span>
          </span>
          <button 
            type="button" 
            @click="toggleFullScreen" 
            class="bg-transparent border-none hover:bg-white/10  text-gray-600 dark:text-white inline-flex justify-center items-center cursor-pointer px-4 ml-auto transition-colors"
            :title="fullScreen ? 'Exit fullscreen' : 'Enter fullscreen'"
          >
            <i :class="fullScreenIcon"></i>
          </button>
        </div>
      </template>
    </Galleria>
  </div>
</template>

<script setup>
import Galleria from 'primevue/galleria';
import { ref, computed, onMounted ,onUnmounted} from 'vue';

const props = defineProps({
  recipe: {
    type: Object,
    required: true
  },
  activeIndex: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(['update:activeIndex']);

const galleria = ref();
const showThumbnails = ref(false);
const fullScreen = ref(false);
const isAutoPlay = ref(true);

const responsiveOptions = ref([
  { breakpoint: '1024px', numVisible: 3 },
  { breakpoint: '768px', numVisible: 2 },
  { breakpoint: '560px', numVisible: 1 }
]);

const onIndexChange = (val) => {
  emit('update:activeIndex', val);
};

const toggleAutoSlide = () => {
  isAutoPlay.value = !isAutoPlay.value;
};

const onThumbnailButtonClick = () => {
  showThumbnails.value = !showThumbnails.value;
};

const toggleFullScreen = () => {
  if (fullScreen.value) {
    closeFullScreen();
  } else {
    openFullScreen();
  }
};

const onFullScreenChange = () => {
  fullScreen.value = !fullScreen.value;
};

const openFullScreen = () => {
  let elem = galleria.value.$el;

  if (elem.requestFullscreen) {
    elem.requestFullscreen();
  } else if (elem.mozRequestFullScreen) {
    elem.mozRequestFullScreen();
  } else if (elem.webkitRequestFullscreen) {
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) {
    elem.msRequestFullscreen();
  }
};

const closeFullScreen = () => {
  if (document.exitFullscreen) {
    document.exitFullscreen();
  } else if (document.mozCancelFullScreen) {
    document.mozCancelFullScreen();
  } else if (document.webkitExitFullscreen) {
    document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) {
    document.msExitFullscreen();
  }
};

const bindDocumentListeners = () => {
  document.addEventListener('fullscreenchange', onFullScreenChange);
  document.addEventListener('mozfullscreenchange', onFullScreenChange);
  document.addEventListener('webkitfullscreenchange', onFullScreenChange);
  document.addEventListener('msfullscreenchange', onFullScreenChange);
};

const unbindDocumentListeners = () => {
  document.removeEventListener('fullscreenchange', onFullScreenChange);
  document.removeEventListener('mozfullscreenchange', onFullScreenChange);
  document.removeEventListener('webkitfullscreenchange', onFullScreenChange);
  document.removeEventListener('msfullscreenchange', onFullScreenChange);
};

const fullScreenIcon = computed(() => {
  return `pi ${fullScreen.value ? 'pi-window-minimize' : 'pi-window-maximize'}`;
});

const slideButtonIcon = computed(() => {
  return `pi ${isAutoPlay.value ? 'pi-pause' : 'pi-play'}`;
});

const getTotalTime = (timeObj) => {
  if (!timeObj) return 0;
  return (timeObj.hr || 0) * 60 + (timeObj.min || 0);
};

const formatTime = (timeObj) => {
  if (!timeObj) return '';
  const total = getTotalTime(timeObj);
  const hr = Math.floor(total / 60);
  const min = total % 60;
  return hr > 0 ? `${hr}h ${min > 0 ? min + 'm' : ''}` : `${min}m`;
};

const formatIngredient = (ingredient) => {
  if (typeof ingredient === 'string') return ingredient;
  if (!ingredient.amount) return ingredient.name;
  return `${ingredient.name} (${ingredient.amount}${ingredient.unit ? ` ${ingredient.unit}` : ''})`;
};

const isYoutubeUrl = (url) =>
  url?.includes('youtube.com') || url?.includes('youtu.be');

const getYoutubeEmbedUrl = (url) => {
  const regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|&v=)([^#&?]*).*/;
  const match = url.match(regExp);
  const videoId = (match && match[2].length === 11) ? match[2] : null;
  return videoId ? `https://www.youtube.com/embed/${videoId}?modestbranding=1` : '';
};

// Format instructions with basic HTML support
const formatInstructions = (text) => {
  if (!text) return 'No instructions';
  
  // Basic sanitization (in a real app, use a proper sanitizer library)
  const sanitized = text
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/\n/g, '<br>')
    // Allow some basic formatting
    .replace(/&lt;b&gt;(.*?)&lt;\/b&gt;/g, '<strong>$1</strong>')
    .replace(/&lt;i&gt;(.*?)&lt;\/i&gt;/g, '<em>$1</em>')
    .replace(/&lt;u&gt;(.*?)&lt;\/u&gt;/g, '<u>$1</u>')
    // Support markdown-style formatting
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/_(.*?)_/g, '<u>$1</u>');
    
  return sanitized;
};

// Lifecycle hooks
onMounted(() => {
  bindDocumentListeners();
});

onUnmounted(() => {
  unbindDocumentListeners();
});
</script>

<style scoped>
.recipe-galleria {
  /* max-width: 900px; */
  margin: 0 auto;
  border-radius: 0.5rem;
}

:deep(.p-galleria-thumbnail-item) {
  opacity: 0.7;
  transition: all 0.3s ease;
}
:deep(.p-galleria-thumbnail-item:hover),
:deep(.p-galleria-thumbnail-item.p-highlight) {
  opacity: 1;
  transform: scale(1.05);
}

/* Fullscreen styles */
:deep(.p-galleria.p-galleria-fullscreen) {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
  background: black;
}

:deep(.p-galleria.p-galleria-fullscreen .p-galleria-content) {
  height: calc(100vh - 120px);
}

:deep(.p-galleria.p-galleria-fullscreen .p-galleria-item-wrapper) {
  height: 100%;
}

/* Custom scrollbar for content */
:deep(.p-galleria-item) {
  overflow-y: auto;
}

:deep(.p-galleria-item::-webkit-scrollbar) {
  width: 6px;
}

:deep(.p-galleria-item::-webkit-scrollbar-track) {
  background: rgba(0, 0, 0, 0.1);
}

:deep(.p-galleria-item::-webkit-scrollbar-thumb) {
  background-color: var(--primary-500);
  border-radius: 3px;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  :deep(.p-galleria-item-wrapper) {
    flex-direction: column;
  }
  
  :deep(.p-galleria-item) > div {
    width: 100% !important;
  }
}
</style>