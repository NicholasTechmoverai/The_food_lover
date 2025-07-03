<template>
    <div class="relative flex-col p-10 py-25 bg-gray-100 flex items-center justify-center bg-cover bg-center bg-fixed" :style="{ backgroundImage: `url(${background_image})`}">
        <h2
        :style="{ fontFamily: siteConfig.welcomeMessage.fontFamily }" 
            class="px-4 backdrop-blur-[5px] text-4xl md:text-6xl lg:text-7xl font-extrabold  font-cursive drop-shadow-sm text-purple-700 font-serif animate-text-gradient">
            {{ who_are_we }}
        </h2>
            from <p :style="{ color: siteConfig.colors.text.secondary }"   class=" b-0 left-[90%] text-gray-500">{{ siteConfig.meta.by }}</p>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import { useSiteStore } from '../config/siteConfig.js'

const { siteConfig, getResponsiveValue } = useSiteStore()

import background_image from '../assets/pexels-rajesh-tp-749235-1633525.jpg'
const who_are_we = ref(`We are ${siteConfig.meta.siteName}`)
</script>