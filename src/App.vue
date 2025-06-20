<template>
  <div class="relative w-full overflow-x-hidden max-w-[2500px] mx-auto">
    <Menubar class="nav z-100 h-fit sticky top-0" />
    <router-view />
    <footer>
      <Footer />
    </footer>
  </div>
</template>

<script setup>
import Menubar from './components/menubar.vue';
import Footer from './pages/footer.vue';

// import { siteConfig, useIsMobile } from './config/siteConfig.js';
</script>

<style scoped>
.nav {
  position: sticky !important;
  top: 0;
}
</style>