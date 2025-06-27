<!-- 
<template>
  <router-view class="fixed pt-15 w-full h-[80%] md:h-full z-60" />
    <div class="card">
        <Galleria
            ref="galleria"
            v-model:activeIndex="activeIndex"
            :value="recipes"
            :numVisible="5"
            containerStyle="max-width: 640px"
            :showThumbnails="showThumbnails"
            :showItemNavigators="true"
            :showItemNavigatorsOnHover="true"
            :circular="true"
            :autoPlay="isAutoPlay"
            :transitionInterval="3000"
            :responsiveOptions="responsiveOptions"
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
            <template #item="slotProps">
                <img :src="slotProps.item.itemImageSrc" :alt="slotProps.item.alt" :style="[{ width: !fullScreen ? '100%' : '', display: !fullScreen ? 'block' : '' }]" />
            </template>
            <template #thumbnail="slotProps">
                <div class="grid gap-4 justify-center">
                    <img :src="slotProps.item.thumbnailImageSrc" :alt="slotProps.item.alt" style="display: block" />
                </div>
            </template>
            <template #footer>
                <div class="flex items-stretch bg-surface-950 text-white h-10">
                    <button type="button" @click="onThumbnailButtonClick" class="bg-transparent border-none rounded-none hover:bg-white/10 text-white inline-flex justify-center items-center cursor-pointer px-3">
                        <i class="pi pi-th-large"></i>
                    </button>
                    <button type="button" @click="toggleAutoSlide" class="bg-transparent border-none rounded-none hover:bg-white/10 text-white inline-flex justify-center items-center cursor-pointer px-3"><i :class="slideButtonIcon"></i></button>
                    <span v-if="images" class="flex items-center gap-4 ml-3">
                        <span class="text-sm">{{ activeIndex + 1 }}/{{ images.length }}</span>
                        <span class="font-bold text-sm">{{ images[activeIndex].title }}</span>
                        <span class="text-sm">{{ images[activeIndex].alt }}</span>
                    </span>
                    <button type="button" @click="toggleFullScreen" class="bg-transparent border-none rounded-none hover:bg-white/10 text-white inline-flex justify-center items-center cursor-pointer px-3 ml-auto">
                        <i :class="fullScreenIcon"></i>
                    </button>
                </div>
            </template>
        </Galleria>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";

const galleria = ref();
const recipes = ref([
  {
    itemImageSrc: 'https://picsum.photos/id/1018/1920/1080',
    thumbnailImageSrc: 'https://picsum.photos/id/1018/250/150',
    alt: 'Mountain landscape',
    title: 'Scenic View 1'
  },
  {
    itemImageSrc: 'https://picsum.photos/id/1015/1920/1080',
    thumbnailImageSrc: 'https://picsum.photos/id/1015/250/150',
    alt: 'Cliff by the ocean',
    title: 'Coastal Scene'
  },
  {
    itemImageSrc: 'https://picsum.photos/id/1019/1920/1080',
    thumbnailImageSrc: 'https://picsum.photos/id/1019/250/150',
    alt: 'Snowy peaks',
    title: 'Winter Mountains'
  },
  {
    itemImageSrc: 'https://picsum.photos/id/1020/1920/1080',
    thumbnailImageSrc: 'https://picsum.photos/id/1020/250/150',
    alt: 'Bear in the forest',
    title: 'Wildlife'
  },
  {
    itemImageSrc: 'https://picsum.photos/id/1021/1920/1080',
    thumbnailImageSrc: 'https://picsum.photos/id/1021/250/150',
    alt: 'Desert canyon',
    title: 'Arid Landscape'
  }
]);
const activeIndex = ref(0);
const showThumbnails = ref(false);
const fullScreen = ref(false);
const isAutoPlay = ref(true);

const toggleAutoSlide = () => {
    isAutoPlay.value  = !isAutoPlay.value ;
};
const onThumbnailButtonClick = () => {
    showThumbnails.value  = !showThumbnails.value ;
};

const responsiveOptions = ref([
    {
        breakpoint: '1300px',
        numVisible: 4
    },
    {
        breakpoint: '575px',
        numVisible: 1
    }
]);

const toggleFullScreen = () => {
    if (fullScreen.value ) {
        closeFullScreen();
    } else {
        openFullScreen();
    }
};
const onFullScreenChange = () => {
    fullScreen.value  = !fullScreen.value ;
};
const openFullScreen = () =>{
    let elem = galleria.value.$el;

    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.mozRequestFullScreen) {
        /* Firefox */
        elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) {
        /* Chrome, Safari & Opera */
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) {
        /* IE/Edge */
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
</script>
 -->

 <template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-100">Browse Recipes</h1>

    <div class="grid gap-6 grid-cols-1 sm:grid-cols-2 md:grid-cols-3 xl:grid-cols-4">
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

const recipes = ref([
  {
    id: '1',
    recipeName: 'Spaghetti Bolognese',
    repiceColor: '#FF7043',
    image: 'https://source.unsplash.com/400x300/?spaghetti',
    tags: ['pasta', 'beef'],
    cookTime: {
      hr: 1,
      min: 30
    },
    description: 'A classic Italian dish with rich tomato and meat sauce.',
    recipeContent: 'Steps and ingredients for spaghetti...',
  },
  {
    id: '2',
    recipeName: 'Avocado Toast',
    repiceColor: '#66BB6A',
    image: 'https://source.unsplash.com/400x300/?avocado-toast',
    tags: ['vegan', 'quick'],
    cookTime: {
      hr: 0,
      min: 10
    },
    description: 'Quick and healthy breakfast with smashed avocado.',
    recipeContent: 'Instructions for preparing avocado toast...',
  },
  // Add more recipes here...
])
</script>
