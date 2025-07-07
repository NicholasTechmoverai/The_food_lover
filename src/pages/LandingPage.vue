<template>
    <div class="relative w-full overflow-x-hidden max-w-[2500px] mx-auto">
        <WelcomeMessage class="z-40 relative" />

        <!-- Services Section -->
        <section class="relative flex flex-col items-center justify-center w-full">
            
            <img :src="servicesImage" alt="Services Background"
                class="absolute inset-0 w-full h-full object-cover brightness-75 grayscale-0 blur-0 z-0 select-none pointer-events-none"
                draggable="false" />

            <p :style="{ fontFamily: siteConfig.welcomeMessage.fontFamily }"
                class="z-40 p-5  text-5xl font-extrabold text-purple-800 font-cursive drop-shadow-sm animate-text-gradient">
                {{ recipe_message }}</p>

            <div class="flex flex-col lg:flex-row lg:items-center lg:justify-center w-full">
                <DishCard class="z-30 relative" />
                <ServicesOffered class="z-50 w-full mt-auto flex items-end justify-end p-8 lg:p-[50px]" />
            </div>

        </section>
        <div class="flex relative flex-col justify-around gap-2 lg:flex-row p-5 z-60" :style="backgroundStyle">
            <TiltedRecipeCard />
            <CookingCard class="relative z-50" />
        </div>
        <TimePage />
        <div class="flex relative flex-col justify-around lg:flex-row bg-gray-100  z-50 pt-5">
            <InhandPhone class=" max-h-[400px] w-full max-w-[600px]" />
            <HealthyDescription class="m-5" />
        </div>
        <ReachOut class="relative z-40" />
        <WhoAreWe />
    </div>
</template>

<script setup>
import { computed,ref } from 'vue'
import WelcomeMessage from './WelcomeNote.vue';
import ServicesOffered from './ServicesOffered.vue';
import SplitterCard from '../cards/Splitter.vue';
import WhoAreWe from '../cards/WhoAreWe.vue';
import CookingCard from '../cards/CookingCard.vue';
// import ServicesOfferedDescription from './pages/RecipesCard.vue';
import ReachOut from './ReachOut.vue';
import TimePage from './TimePage.vue';
import TiltedRecipeCard from '../cards/TiltedRecipeCard.vue'
import DishCard from '../cards/DishCard.vue';
import InhandPhone from '../cards/InHandPhone.vue'
import HealthyDescription from '../cards/HealthyDescription.vue';
import { useIsMobile } from '../reusables';
import { useSiteStore } from '../config/siteConfig.js'
import socket from '../a_websocket/index.js';
const { siteConfig, getResponsiveValue } = useSiteStore()
const recipe_message = ref('Access 1000+ recipes,250+ East African dishes')


const isMobile = useIsMobile();
// const servicesImage = isMobile
//     ? siteConfig.servicesOffred.image.mobile
//     : siteConfig.servicesOffred.image.desktop;

// Convert hex to rgba with optional alpha


const backgroundStyle = computed(() => ({
    background: `${siteConfig.colors.primary}60`
}))

const servicesImage = computed(() => {
  const rawSvg = `<svg id="visual" viewBox="0 0 960 540" width="960" height="540" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">
    <rect x="0" y="0" width="960" height="540" fill="#ebedee"></rect>
    <defs>
      <linearGradient id="grad1_0" x1="43.8%" y1="100%" x2="100%" y2="0%">
        <stop offset="14.444444444444446%" stop-color="${siteConfig.colors.primary}" stop-opacity="1"></stop>
        <stop offset="85.55555555555554%" stop-color="${siteConfig.colors.secondary}" stop-opacity="1"></stop>
      </linearGradient>
    </defs>
    <defs>
      <linearGradient id="grad1_1" x1="43.8%" y1="100%" x2="100%" y2="0%">
        <stop offset="14.444444444444446%" stop-color="${siteConfig.colors.secondary}" stop-opacity="1"></stop>
        <stop offset="85.55555555555554%" stop-color="#ebedee" stop-opacity="1"></stop>
      </linearGradient>
    </defs>
    <defs>
      <linearGradient id="grad2_0" x1="0%" y1="100%" x2="56.3%" y2="0%">
        <stop offset="14.444444444444446%" stop-color="${siteConfig.colors.secondary}" stop-opacity="1"></stop>
        <stop offset="85.55555555555554%" stop-color="${siteConfig.colors.secondary}" stop-opacity="1"></stop>
      </linearGradient>
    </defs>
    <defs>
      <linearGradient id="grad2_1" x1="0%" y1="100%" x2="56.3%" y2="0%">
        <stop offset="14.444444444444446%" stop-color="#ebedee" stop-opacity="1"></stop>
        <stop offset="85.55555555555554%" stop-color="${siteConfig.colors.secondary}" stop-opacity="1"></stop>
      </linearGradient>
    </defs>
    <g transform="translate(960, 540)">
      <path d="M-394 0C-402.5 -17.8 -410.9 -35.6 -416.4 -54.8C-421.9 -74 -424.3 -94.6 -416.3 -111.6C-408.3 -128.5 -389.9 -141.7 -376 -155.8C-362.2 -169.8 -352.9 -184.6 -341.2 -197C-329.6 -209.4 -315.6 -219.6 -308.6 -236.8C-301.7 -254 -301.8 -278.4 -289.9 -289.9C-278.1 -301.4 -254.2 -300.1 -242.3 -315.8C-230.3 -331.4 -230.3 -364.2 -216 -374.1C-201.7 -384.1 -173.3 -371.2 -151.9 -366.8C-130.6 -362.4 -116.3 -366.4 -101.7 -379.6C-87.2 -392.8 -72.3 -415.3 -55.3 -420.4C-38.3 -425.5 -19.2 -413.2 0 -401L0 0Z" fill="${siteConfig.colors.primary}"></path>
      <path d="M-197 0C-201.2 -8.9 -205.5 -17.8 -208.2 -27.4C-210.9 -37 -212.2 -47.3 -208.2 -55.8C-204.2 -64.2 -194.9 -70.9 -188 -77.9C-181.1 -84.9 -176.4 -92.3 -170.6 -98.5C-164.8 -104.7 -157.8 -109.8 -154.3 -118.4C-150.8 -127 -150.9 -139.2 -145 -145C-139 -150.7 -127.1 -150 -121.1 -157.9C-115.2 -165.7 -115.1 -182.1 -108 -187.1C-100.9 -192 -86.6 -185.6 -76 -183.4C-65.3 -181.2 -58.1 -183.2 -50.9 -189.8C-43.6 -196.4 -36.2 -207.6 -27.7 -210.2C-19.2 -212.7 -9.6 -206.6 0 -200.5L0 0Z" fill="${siteConfig.colors.secondary}"></path>
    </g>
    <g transform="translate(0, 0)">
      <path d="M420 0C417.7 17.9 415.3 35.7 416.4 54.8C417.5 73.9 422 94.2 417.3 111.8C412.5 129.4 398.5 144.3 390.8 161.9C383.1 179.5 381.8 199.9 368.9 213C356.1 226.1 331.7 232 315.8 242.3C299.8 252.6 292.4 267.4 285.7 285.7C278.9 303.9 272.8 325.6 260.5 339.6C248.3 353.5 229.8 359.7 212.5 368.1C195.2 376.5 179 387.1 160 386.2C140.9 385.3 118.9 373 101.5 378.6C84 384.3 71.2 408 55.1 418.4C38.9 428.8 19.5 425.9 0 423L0 0Z" fill="${siteConfig.colors.primary}"></path>
      <path d="M210 0C208.8 8.9 207.7 17.9 208.2 27.4C208.8 37 211 47.1 208.6 55.9C206.3 64.7 199.2 72.1 195.4 80.9C191.6 89.7 190.9 99.9 184.5 106.5C178 113.1 165.8 116 157.9 121.1C149.9 126.3 146.2 133.7 142.8 142.8C139.5 152 136.4 162.8 130.3 169.8C124.1 176.7 114.9 179.8 106.3 184C97.6 188.2 89.5 193.5 80 193.1C70.4 192.7 59.4 186.5 50.7 189.3C42 192.2 35.6 204 27.5 209.2C19.5 214.4 9.7 212.9 0 211.5L0 0Z" fill="${siteConfig.colors.secondary}"></path>
    </g>
  </svg>`;
   const encoded = btoa(unescape(encodeURIComponent(rawSvg)));
  return `data:image/svg+xml;base64,${encoded}`;
});

</script>



<style scoped>
.nav {
    position: sticky !important;
    top: 0;
}
</style>

<!-- <template>
    <div>
        <div class="max-w-2xl mx-auto mt-20 text-center px-4">
            <h1 class="text-3xl font-bold text-amber-700 mb-2">
                Add New Recipe
            </h1>

            <div class="rounded border p-6">
                <div class="flex mb-4">
                    <Skeleton shape="circle" size="4rem" class="mr-2" />
                    <div>
                        <Skeleton width="10rem" class="mb-2" />
                        <Skeleton width="5rem" class="mb-2" />
                        <Skeleton height=".5rem" />
                    </div>
                </div>
                <Skeleton width="100%" height="150px" />
                <div class="flex justify-between mt-4">
                    <Skeleton width="4rem" height="2rem" />
                    <Skeleton width="4rem" height="2rem" />
                </div>
            </div>

            <router-view />
        </div>

        <div class="card flex justify-center">
            <Toast position="bottom-center" group="bc" @close="onClose">
                <template #message="slotProps">
                    <div class="flex flex-col items-start flex-auto">
                        <div class="flex items-center gap-2">
                            <Avatar image="https://avatars.githubusercontent.com/u/184249562?v=4" shape="circle" />
                            <span class="font-bold">Developer</span>
                        </div>
                        <div class="font-medium text-lg my-4">
                            {{ slotProps.message.summary }}
                        </div>
                    </div>
                </template>
            </Toast>

            <Button @click="showTemplate" label="??" />
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import Skeleton from 'primevue/skeleton'
import Toast from 'primevue/toast'
import Button from 'primevue/button'
import Avatar from 'primevue/avatar'
import Skeleton2 from '../loaders/Skeleton2.vue'
import Skeleton3 from '../loaders/Skeleton3.vue';

const props = defineProps({
    recipe_id: [String, Number],
    recipe_name: String
})

const formattedRecipeName = computed(() => {
    return props.recipe_name ? props.recipe_name.replace(/-/g, ' ') : ''
})

const toast = useToast()
const visible = ref(false)

const showTemplate = () => {
    if (!visible.value) {
        toast.add({
            severity: 'error',
            summary: 'Not Fully Developed!',
            group: 'bc'
        })
        visible.value = true
    }
}


const onClose = () => {
    visible.value = false
}

onMounted(()=>{
    setTimeout(() => {
        showTemplate()
    }, 3000);
})
</script> -->