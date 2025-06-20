<template>
    <div class="relative flex min-h-[70vh] h-fit w-full items-center justify-start overflow-hidden bg-gray-100">
        <!-- Enhanced Video Background -->
        <div class="absolute inset-0 z-0">
            <video autoplay loop muted playsinline class="h-full w-full object-cover">
                <source :src="welcomeMessage.video" type="video/mp4">

            </video>
            <!-- Fallback image with subtle animation -->
            <img :src="welcomeMessage.image" alt="Kitchen background"
                class="h-full w-full object-cover transition-opacity duration-1000"
                :class="{ 'opacity-0': !videoError }" @error="videoError = true">
            <div
                class="absolute inset-0 bg-gradient-to-r from-gray-900/30 via-gray-900/10 to-gray-900/40 backdrop-blur-[1px]">
            </div>
        </div>

        <!-- Content Container with Smooth Entrance Animation -->
        <div class="relative z-10 mf-auto h-full backdrop-blur-[1px] w-full max-w-4xl animate-fade-in-up">
            <!-- Refined Glass Card -->
            <div
                class="h-full  bg-gray-900/55 backdrop-blur-lg p-5 shadow-[5px_0_15px_rgba(0,0,0,0.1)] border-r  border-white/10">
                <!-- Main Heading with Improved Gradient -->
                <h1 :style="{ fontFamily: welcomeMessage.fontFamily }"
                    class="text-4xl font-bold leading-tight sm:text-5xl md:text-6xl mb-8 bg-clip-text text-transparent bg-gradient-to-r from-purple-800 via-amber-600 to-purple-800 bg-size-200 animate-text-gradient">
                    {{ welcomeMessage.note || 'Welcome to our website!' }}
                </h1>

                <!-- Author Credit -->
                <p class="text-lg text-gray-200 mb-10">
                    Brought to you by <span class="font-semibold text-purple-700 underline  decoration-purple-400/50">{{
                        siteConfig.author }}</span>
                </p>

                <!-- Social Links with Hover Effects -->
                <div v-if="siteConfig.social.links.length" class="mb-10 items-center flex flex-col justify-center ">
                    <p v-if="siteConfig.social.shareText"
                        class="p-2 text-sm text-gray-300/90 animate-fade-in delay-500">
                        {{ siteConfig.social.shareText }}
                    </p>
                    <div class="flex flex-row justify-center space-x-4">
                        <a v-for="link in siteConfig.social.links" :key="link.name" :href="link.url" target="_blank"
                            rel="noopener noreferrer"
                            class="text-2xl text-gray-700 hover:text-white transition-all duration-300 flex items-center justify-center h-12 w-12 rounded-full bg-white/80 hover:bg-purple-600/90 border border-gray-300/50 hover:border-purple-500 shadow-sm hover:shadow-purple-500/30"
                            aria-label="Social media link" :title="link.name">
                            <i :class="link.icon"></i>
                        </a>
                    </div>

                </div>

                <div class="mx-auto w-full max-w-md transform transition-all duration-500 hover:scale-[1.02]">
                    <component :is="SearchBar" />
                </div>

                <p v-if="siteConfig.social.shareText" class="mt-10 text-sm text-gray-300/90 animate-fade-in delay-500">
                    {{ siteConfig.social.shareText }}
                </p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { siteConfig } from '../config/siteConfig.js';
import { computed, ref } from 'vue';
import SearchBar1 from "../searchbar/SearchBar1.vue";
import SearchBar2 from "../searchbar/SearchBar2.vue";
import SearchBar3 from "../searchbar/SearchBar3.vue";
import SearchBar4 from "../searchbar/SearchBar4.vue";

const videoError = ref(false);

const SearchBar = computed(() => {
    const searchBars = {
        1: SearchBar1,
        2: SearchBar2,
        3: SearchBar3,
        4: SearchBar4
    };
    return searchBars[siteConfig.components.searchBar] || SearchBar1;
});

const welcomeMessage = siteConfig.welcomeMessage;
</script>

<style scoped>
/* Animations */
.animate-fade-in-up {
    animation: fadeInUp 0.8s ease-out forwards;
}

.animate-text-gradient {
    background-size: 200% auto;
    animation: gradientShift 3s ease infinite;
}

.animate-fade-in {
    animation: fadeIn 1s ease-out forwards;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes gradientShift {
    0% {
        background-position: 0% center;
    }

    50% {
        background-position: 100% center;
    }

    100% {
        background-position: 0% center;
    }
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

/* Glass Morphism Enhancement */
.backdrop-blur-lg {
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
}

/* Responsive Adjustments */
@media (max-width: 768px) {
    .rounded-r-2xl {
        border-radius: 1rem;
        padding: 2rem 1.5rem;
    }
}
</style>