<template>
  <div class="p-6 max-w-xl mx-auto space-y-4">
    <div class="space-y-1">
      <h2 class="text-xl font-semibold text-gray-800 dark:text-gray-100">
        Meal Categories
      </h2>
      <p class="text-sm text-gray-500 dark:text-gray-400">
        Select up to 3 categories that best describe your recipe (e.g. breakfast, dinner, dessert)
      </p>
    </div>

    <!-- Enhanced MultiSelect Component -->
    <div class="space-y-2">
      <div class="flex justify-between items-center">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
          Recipe Categories
        </label>
        <span class="text-xs text-gray-500 dark:text-gray-400">
          {{ selectedCategories.length }}/3 selected
        </span>
      </div>

      <MultiSelect
        v-model="selectedCategories"
        :options="filteredCategoryOptions"
        optionLabel="label"
        optionValue="value"
        placeholder="Search or type to add..."
        display="chip"
        class="w-full"
        :maxSelectedLabels="3"
        :selectionLimit="3"
        :addTag="true"
        :filter="true"
        @add="onAddCategory"
        @before-select="validateSelection"
      >
        <template #value="slotProps">
          <div v-if="slotProps.value" class="flex flex-wrap gap-1.5">
            <span
              v-for="(item, index) in slotProps.value"
              :key="index"
              class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
              :class="[
                selectedCategories.includes(item) ? 
                'bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200' :
                'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200'
              ]"
            >
              {{ getCategoryLabel(item) }}
              <button
                type="button"
                @click.stop="removeCategory(index)"
                class="ml-1.5 inline-flex items-center justify-center w-3.5 h-3.5 rounded-full"
              >
                <span class="sr-only">Remove</span>
                <svg class="w-2 h-2" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            </span>
          </div>
        </template>
      </MultiSelect>

      <div class="flex items-center justify-between">
        <small class="text-xs" :class="
          selectedCategories.length >= 3 ? 
          'text-red-600 dark:text-red-400' : 
          'text-gray-500 dark:text-gray-400'
        ">
          {{ selectionFeedback }}
        </small>
        <button 
          v-if="selectedCategories.length > 0"
          @click="clearAll"
          class="text-xs text-gray-500 hover:text-gray-700 dark:hover:text-gray-300"
        >
          Clear all
        </button>
      </div>
    </div>

    <!-- Popular Categories Suggestions -->
    <div v-if="selectedCategories.length < 3" class="pt-2">
      <p class="text-xs text-gray-500 dark:text-gray-400 mb-2">Popular choices:</p>
      <div class="flex flex-wrap gap-2">
        <span
          v-for="category in popularCategories"
          :key="category.value"
          @click="toggleCategory(category)"
          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium cursor-pointer"
          :class="
            selectedCategories.includes(category.value) ?
            'bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200' :
            'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600'
          "
        >
          {{ category.label }}
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  modelValue: {
    type: Array,
    default: () => []
  }
});
const emit = defineEmits(['update:modelValue']);

const selectedCategories = ref([...props.modelValue]);

watch(selectedCategories, (val) => {
  emit('update:modelValue', val);
});

const categoryOptions = ref([
  { label: 'Breakfast', value: 'breakfast' },
  { label: 'Brunch', value: 'brunch' },
  { label: 'Lunch', value: 'lunch' },
  { label: 'Dinner', value: 'dinner' },
  { label: 'Dessert', value: 'dessert' },
  { label: 'Appetizer', value: 'appetizer' },
  { label: 'Snack', value: 'snack' },
  { label: 'Holiday', value: 'holiday' },
  { label: 'Party', value: 'party' },
  { label: 'Healthy', value: 'healthy' },
  { label: 'Vegetarian', value: 'vegetarian' },
  { label: 'Vegan', value: 'vegan' },
  { label: 'Keto', value: 'keto' },
  { label: 'Gluten-Free', value: 'gluten-free' },
  { label: 'Comfort Food', value: 'comfort-food' },
  { label: 'Quick Meal', value: 'quick-meal' }
]);

const popularCategories = computed(() =>
  categoryOptions.value.filter(opt =>
    ['breakfast', 'lunch', 'dinner', 'dessert', 'snack'].includes(opt.value)
  )
);

const filteredCategoryOptions = computed(() =>
  categoryOptions.value.filter(opt =>
    !selectedCategories.value.includes(opt.value)
  )
);

const selectionFeedback = computed(() => {
  const remaining = 3 - selectedCategories.value.length;
  return remaining > 0
    ? `${remaining} more can be selected`
    : 'Maximum 3 categories selected';
});

function getCategoryLabel(value) {
  const found = categoryOptions.value.find(opt => opt.value === value);
  return found ? found.label : value;
}

function onAddCategory(newCategory) {
  const newValue = newCategory.toLowerCase().replace(/\s+/g, '-');
  if (!categoryOptions.value.some(opt => opt.value === newValue)) {
    categoryOptions.value.push({
      label: newCategory,
      value: newValue
    });
  }
  if (
    !selectedCategories.value.includes(newValue) &&
    selectedCategories.value.length < 3
  ) {
    selectedCategories.value.push(newValue);
  }
}

function toggleCategory(category) {
  if (selectedCategories.value.includes(category.value)) {
    selectedCategories.value = selectedCategories.value.filter(
      c => c !== category.value
    );
  } else if (selectedCategories.value.length < 3) {
    selectedCategories.value.push(category.value);
  }
}

function removeCategory(index) {
  selectedCategories.value.splice(index, 1);
}

function clearAll() {
  selectedCategories.value = [];
}

function validateSelection(event) {
  if (selectedCategories.value.length >= 3) {
    event.preventDefault();
  }
}
</script>

<style scoped>
/* Smooth transitions for interactive elements */
span[class*="bg-"] {
  transition: background-color 0.2s ease, color 0.2s ease;
}
</style>