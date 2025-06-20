<template>
  <div>
    <component :is="WelcomeNoteComponent" />
  </div>
</template>

<script setup>
import { siteConfig } from '../config/siteConfig.js';
import { computed } from 'vue';

import WelcomeNote1 from '../cards/WelcomeNote1.vue';
import WelcomeNote2 from '../cards/WelcomeNote2.vue';

const welcomeCards = {
  1: WelcomeNote1,
  2: WelcomeNote2,
};
const WelcomeNoteComponent = computed(() => {
  const selected = siteConfig.welcomeMessage?.card;
  return welcomeCards[selected] || WelcomeNote2; // default fallback
});
</script>
