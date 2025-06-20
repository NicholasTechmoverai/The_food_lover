<template>
  <div class="relative   bg-cover bg-center bg-fixed" :style="{ backgroundImage: `url(${background_image})` }">
    <div
      class="relative z-10  flex md:flex-row flex-col justify-between  items-center gap-10 bg-black/80"
    >
      <StepperPage />
      <ClockPage class="scale-155 mb-[70px] md:mr-[50px] lg:mr-[150px]" />
    </div>
  </div>
</template>


<script setup>
import ClockPage from '../cards/Clock.vue'
import StepperPage from '../cards/StepperPage.vue';
import background_image from '../assets/pexels-falling4utah-2724748.jpg'
// import background_image from '../assets/pexels-vanmalidate-784633.jpg'

</script>
