<template>
  <div>
    <component :is="ReachOut" />
  </div>
</template>

<script setup>
import { siteConfig } from '../config/siteConfig.js';
import { computed } from 'vue';
import ReachOutCard1 from "../cards/ReachOutCard1.vue";
import ReachOutCard2 from '../cards/ReachOutCard2.vue';
import ReachOutCard3 from '../cards/ReachOutCard3.vue';
import ReachOutCard4 from '../cards/ReachOutCard4.vue';
const ReachOut = computed(() => {
  const card = siteConfig.reachOut.card;

  if (card === 1) return ReachOutCard1;
  else if (card === 2) return ReachOutCard2;
  else if (card === 3) return ReachOutCard3;
  else if (card === 4) return ReachOutCard4;
  else return ReachOutCard1; // Fallback
});
</script>
