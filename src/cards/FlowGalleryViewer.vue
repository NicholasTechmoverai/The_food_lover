<template>
  <div class="recipe-galleria">
    <Galleria
      :value="recipe.steps"
      :numVisible="5"
      :circular="true"
      :autoPlay="true"
      :transitionInterval="3000"
      :activeIndex="activeIndex"
      :showThumbnails="true"
      :showIndicators="true"
      :showItemNavigators="true"
      :responsiveOptions="responsiveOptions"
      @activeIndexChange="onIndexChange"
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
                <div class="text-sm mt-1">{{ item.instructions || 'No instructions' }}</div>
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
    </Galleria>
  </div>
</template>

<script setup>
import Galleria from 'primevue/galleria';
import { ref } from 'vue';

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

const responsiveOptions = ref([
  { breakpoint: '1024px', numVisible: 3 },
  { breakpoint: '768px', numVisible: 2 },
  { breakpoint: '560px', numVisible: 1 }
]);

const onIndexChange = (val) => {
  emit('update:activeIndex', val);
};

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
</script>

<style scoped>
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
</style>
