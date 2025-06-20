<template>
    <div class="relative w-full overflow-x-hidden max-w-[2500px] mx-auto">
        <WelcomeMessage class="z-40 relative" />

        <!-- Services Section -->
        <section class="relative flex flex-col lg:flex-row lg:items-center lg:justify-center w-full">
            <img :src="servicesImage" alt="Services Background"
                class="absolute inset-0 w-full h-full object-cover brightness-75 grayscale-0 blur-0 z-0 select-none pointer-events-none"
                draggable="false" />

            <DishCard class="z-30 relative" />
            <ServicesOffered class="z-50 w-full flex items-end justify-end p-8 lg:p-[50px]" />
        </section>
        <div class="flex relative flex-col justify-around gap-2 lg:flex-row bg-amber-300 p-5">
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
import { siteConfig, useIsMobile } from '../config/siteConfig.js';

const isMobile = useIsMobile();
const servicesImage = isMobile
    ? siteConfig.servicesOffred.image.mobile
    : siteConfig.servicesOffred.image.desktop;
</script>

<style scoped>
.nav {
    position: sticky !important;
    top: 0;
}
</style>