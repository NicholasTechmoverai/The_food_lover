<template>
  <div>
    <!-- Grid Gallery -->
    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
      <div
        v-for="(step, index) in recipe.steps"
        :key="index"
        class="relative cursor-pointer group"
        @click="imageClick(index)"
      >
        <img
          :src="step.image"
          class="w-full h-36 object-cover rounded-lg transition duration-200 group-hover:opacity-90"
          alt="Step Image"
        />
        <div class="absolute top-2 left-2 text-xs bg-green-600 text-white px-2 py-1 rounded-full shadow-md">
          Step {{ index + 1 }}
        </div>
      </div>
    </div>

    <!-- Fullscreen Preview -->
    <Galleria
      v-model:visible="displayCustom"
      :value="recipe.steps"
      :activeIndex="activeIndex"
      :fullScreen="true"
      :showThumbnails="false"
      :showItemNavigators="true"
      @activeIndexChange="onIndexChange"
    >
      <template #item="slotProps">
        <div class="relative">
          <img
            :src="slotProps.item.image"
            class="w-full max-h-[90vh] object-contain mx-auto"
            alt="Step Image"
          />
          <div class="absolute bottom-0 left-0 right-0 bg-black/70 text-white p-4">
            <div class="text-xl font-bold">{{ slotProps.item.instructions }}</div>
            <div class="text-md">Step {{ slotProps.index + 1 }}</div>
          </div>
        </div>
      </template>
    </Galleria>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import Galleria from 'primevue/galleria';

const props = defineProps({
  recipe: Object,
  activeIndex: Number,
});
const emit = defineEmits(['update:activeIndex']);

const displayCustom = ref(false);
const internalIndex = ref(props.activeIndex);

watch(() => props.activeIndex, (val) => {
  internalIndex.value = val;
});

function imageClick(index) {
  emit('update:activeIndex', index);
  displayCustom.value = true;
}

function onIndexChange(val) {
  emit('update:activeIndex', val);
}
</script>
