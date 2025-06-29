<template>
  <div class="flex justify-center">
<Button
  type="button"
  icon="pi pi-utensils"
  severity="secondary"
  :label="selectedCuisine ? selectedCuisine.name : 'Select Cuisine'"
  @click="toggle"
  class="min-w-48"
/>

    <Popover ref="op">
      <div class="flex flex-col gap-4 p-3">
        <div>
          <span class="font-medium block mb-2">East African Cuisines</span>
          <ul class="list-none p-0 m-0 flex flex-col max-h-64 overflow-y-auto">
            <li
              v-for="cuisine in cuisines"
              :key="cuisine.name"
              class="flex items-center gap-2 px-3 py-2 hover:bg-emphasis cursor-pointer rounded-lg"
              @click="selectCuisine(cuisine)"
            >
              <span class="font-medium">{{ cuisine.name }}</span>
              <div class="text-sm text-surface-500 dark:text-surface-400">{{ cuisine.region }}</div>
            </li>
          </ul>
        </div>
      </div>
    </Popover>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const emit = defineEmits(['update:modelValue'])
const props = defineProps({
  modelValue: Object
})

const op = ref()
const selectedCuisine = ref(props.modelValue || { name: 'Kenyan', region: 'East Africa' })

const cuisines = ref([
  { name: 'Kenyan', region: 'East Africa' },
  { name: 'Ugandan', region: 'East Africa' },
  { name: 'Tanzanian', region: 'East Africa' },
  { name: 'Rwandan', region: 'East Africa' },
  { name: 'Burundian', region: 'East Africa' },
  { name: 'Somali', region: 'Horn of Africa' },
  { name: 'Ethiopian', region: 'Horn of Africa' },
  { name: 'South Sudanese', region: 'East Africa' },
  { name: 'Congolese', region: 'Central Africa' },
])

const toggle = (event) => {
  op.value.toggle(event)
}

const selectCuisine = (cuisine) => {
  selectedCuisine.value = cuisine
  emit('update:modelValue', cuisine)
  op.value.hide()
}
</script>
