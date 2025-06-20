<template>
    <div>
        <Footer />
    </div>
</template>
<script setup>
import Footer1 from '../footers/Footer1.vue';
import { siteConfig } from '../config/siteConfig.js';
import { computed } from 'vue';
const Footer = computed(() => {
    const footer = siteConfig.components.footer;
    if (footer === 1) return Footer1;
    else return Footer1; // Default to Footer1 if no specific footer is set
});
</script>