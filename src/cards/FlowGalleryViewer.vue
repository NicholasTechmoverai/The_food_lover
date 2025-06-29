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
        <div class="relative h-full">
          <!-- Media: YouTube / video / image -->
          <div v-if="item.videoUrl" class="media-container bg-black rounded-lg">
            <iframe
              v-if="isYoutubeUrl(item.videoUrl)"
              :src="getYoutubeEmbedUrl(item.videoUrl)"
              frameborder="0"
              allowfullscreen
              class="w-full h-96"
              title="Step Video"
            ></iframe>
            <video
              v-else
              :src="item.videoUrl"
              controls
              class="w-full h-96 object-contain"
            ></video>
          </div>

          <div v-else-if="item.image">
            <img
              :src="item.image"
              :alt="`Step ${item.no || index + 1} image`"
              class="w-full h-96 object-cover rounded-lg"
            />
          </div>

          <div v-else class="w-full h-96 bg-gray-200 dark:bg-gray-700 flex items-center justify-center rounded-lg">
            <div class="text-center text-gray-500 dark:text-gray-400">
              <i class="pi pi-image text-4xl mb-2"></i>
              <p>No media available</p>
            </div>
          </div>

          <!-- Info Overlay -->
          <div class="absolute bottom-0 inset-x-0 bg-gradient-to-t from-black/70 to-transparent p-4 text-white">
            <div class="flex justify-between items-start">
              <div>
                <div class="text-lg font-semibold">Step {{ item.no || index + 1 }}</div>
                <div 
                  class="text-sm mt-1 break-words whitespace-pre-line" 
                  v-html="formatInstructions(item.instructions || 'No instructions')"
                ></div>
              </div>
              <div class="text-xs space-y-1 text-right">
                <div v-if="getTotalTime(item.timeRequired) > 0" class="bg-white/20 px-2 py-1 rounded-full inline-block">
                  <i class="pi pi-clock mr-1"></i>{{ formatTime(item.timeRequired) }}
                </div>
                <div v-if="item.tempRequired > 0" class="bg-white/20 px-2 py-1 rounded-full inline-block">
                  <i class="pi pi-thermometer mr-1"></i>{{ item.tempRequired }}°C
                </div>
              </div>
            </div>

            <!-- Ingredients -->
            <div class="flex flex-wrap gap-1 mt-3" v-if="item.ingredientsUsed?.length">
              <span
                v-for="(ingredient, i) in item.ingredientsUsed"
                :key="i"
                class="text-xs bg-white/20 px-2 py-1 rounded-full flex items-center"
              >
                <i class="pi pi-circle-fill text-[8px] mr-1"></i>
                {{ formatIngredient(ingredient) }}
              </span>
            </div>
          </div>
        </div>
      </template>

      <!-- Thumbnail View -->
      <template #thumbnail="{ item, index }">
        <div class="relative w-24 h-16 rounded-md overflow-hidden">
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
            class="w-full h-full bg-gray-300 dark:bg-gray-600 flex items-center justify-center"
          >
            <i class="pi pi-image text-gray-500 dark:text-gray-400"></i>
          </div>
          <span class="absolute bottom-1 right-1 bg-black/70 text-white text-xs px-1 rounded">
            {{ item.no || index + 1 }}
          </span>
        </div>
      </template>

      <!-- Caption (Recipe Name) -->
      <template #caption v-if="recipe.name">
        <div class="text-lg font-bold text-center p-2">
          {{ recipe.name }}
        </div>
      </template>

      <!-- Footer with controls -->
      <template #footer>
        <div class="flex items-stretch bg-surface-950 text-white h-10">
          <button 
            type="button" 
            @click="onThumbnailButtonClick" 
            class="bg-transparent border-none rounded-none hover:bg-white/10 text-white inline-flex justify-center items-center cursor-pointer px-3"
          >
            <i class="pi pi-th-large"></i>
          </button>
          <button 
            type="button" 
            @click="toggleAutoSlide" 
            class="bg-transparent border-none rounded-none hover:bg-white/10 text-white inline-flex justify-center items-center cursor-pointer px-3"
          >
            <i :class="slideButtonIcon"></i>
          </button>
          <span v-if="recipe.steps" class="flex items-center gap-4 ml-3">
            <span class="text-sm">{{ activeIndex + 1 }}/{{ recipe.steps.length }}</span>
            <span class="font-bold text-sm">Step {{ recipe.steps[activeIndex].no || activeIndex + 1 }}</span>
          </span>
          <button 
            type="button" 
            @click="toggleFullScreen" 
            class="bg-transparent border-none rounded-none hover:bg-white/10 text-white inline-flex justify-center items-center cursor-pointer px-3 ml-auto"
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
.p-galleria-caption{
  background: transparent !important;
}
.recipe-galleria {
  max-width: 900px;
  margin: 0 auto;
}

:deep(.p-galleria-thumbnail-item) {
  opacity: 0.5;
  transition: all 0.3s ease;
}
:deep(.p-galleria-thumbnail-item:hover),
:deep(.p-galleria-thumbnail-item.p-highlight) {
  opacity: 1;
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
  height: calc(100vh - 100px);
}

:deep(.p-galleria.p-galleria-fullscreen .p-galleria-item-wrapper) {
  height: 100%;
}

/* Instruction text styling */
.instruction-text {
  word-break: break-word;
  white-space: pre-line;
}
</style>