<template>
  <div>
    <component :is="ServiceCard" />
  </div>
</template>

<script setup>
import { siteConfig } from '../config/siteConfig.js';
import { computed } from 'vue';
import ServiceCard1 from "../cards/ServiceCard1.vue";
import ServiceCard2 from "../cards/MobileCard.vue";

const ServiceCard = computed(() => {
  const card = siteConfig.servicesOffred.card;
  if (card === 1) return ServiceCard1;
  else if (card === 2) return ServiceCard2;
  else return ServiceCard1; 
});
</script>
