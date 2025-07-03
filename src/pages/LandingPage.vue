<template>
    <div class="relative w-full overflow-x-hidden max-w-[2500px] mx-auto">
        <WelcomeMessage class="z-40 relative" />

        <!-- Services Section -->
        <section class="relative flex flex-col lg:flex-row lg:items-center lg:justify-center w-full">
            <img :src="servicesImage" alt="Services Background"
                class="absolute inset-0 w-full h-full object-cover brightness-75 grayscale-0 blur-0 z-0 select-none pointer-events-none"
                draggable="false" />

            <DishCard class="z-30 relative" />
            <ServicesOffered class="z-50 w-full mt-auto flex items-end justify-end p-8 lg:p-[50px]" />
        </section>
        <div class="flex relative flex-col justify-around gap-2 lg:flex-row p-5 z-60" :style="backgroundStyle">
            <TiltedRecipeCard />
            <CookingCard class="relative z-50" />
        </div>
        <TimePage />
        <div class="flex relative flex-col justify-around md:flex-row bg-gray-100  z-50 pt-5">
            <InhandPhone class=" max-h-[400px] w-full max-w-[600px]" />
            <HealthyDescription class="m-5" />
        </div>
        <ReachOut class="relative z-40" />
        <WhoAreWe />
    </div>
</template>

<script setup>
import { computed } from 'vue'
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
import {  useIsMobile } from '../reusables';
import { useSiteStore } from '../config/siteConfig.js'

const { siteConfig, getResponsiveValue } = useSiteStore()


const isMobile = useIsMobile();
const servicesImage = isMobile
    ? siteConfig.servicesOffred.image.mobile
    : siteConfig.servicesOffred.image.desktop;

// Convert hex to rgba with optional alpha
function hexToRgba(hex, alpha = 1) {
  const bigint = parseInt(hex.replace('#', ''), 16)
  const r = (bigint >> 16) & 255
  const g = (bigint >> 8) & 255
  const b = bigint & 255
  return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

const backgroundStyle = computed(() => ({
  background: hexToRgba(siteConfig.colors.primary, 0.7),
}))    
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