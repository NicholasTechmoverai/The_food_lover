<template>
  <div>
    <img v-if="isImage" :src="src" class="preview-img" />
    <video v-else-if="isVideo" :src="src" class="preview-img" controls />
  </div>
</template>

<script setup>
const props = defineProps({ src: String });
const isImage = /\.(jpg|jpeg|png|gif|webp|svg)$/i.test(props.src || '');
const isVideo = /\.(mp4|webm|ogg)$/i.test(props.src || '');
</script>

<style scoped>
.preview-img {
  max-width: 180px;
  max-height: 150px;
  border-radius: 0.375rem;
  border: 1px solid #ccc;
  margin-top: 0.5rem;
}
</style>

