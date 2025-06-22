<template>
  <div>
    <component :is="MenuBar"/>
  </div>
</template>

<script setup>
import { siteConfig } from '../config/siteConfig.js';
import { computed } from 'vue';
import MenuBar1 from "../menubars/menubar1.vue";

const MenuBar = computed(() => {
  const card = siteConfig.components.menuBar;

  if (card === 1) return MenuBar1;
  else return MenuBar1; // Fallback
});
</script>
