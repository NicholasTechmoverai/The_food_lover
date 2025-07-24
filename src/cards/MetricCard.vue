<template>
  <div class="bg-gray-50 dark:bg-gray-700/50 p-4 rounded-lg transition-all duration-200 hover:shadow-sm" :class="{
    'hover:border-[var(--theme-color)]/30': change !== undefined
  }">
    <div class="flex flex-col items-center text-center">
      <!-- Icon and Title -->
      <div class="flex items-center gap-2 mb-1">
        <i :class="[icon, color]" class="text-lg"></i>
        <p class="text-sm font-medium text-gray-500 dark:text-gray-400">{{ title }}</p>
      </div>
      
      <!-- Value -->
      <p class="text-xl font-bold text-gray-900 dark:text-white my-1">
        {{ typeof value === 'number' ? value.toLocaleString() : value }}
      </p>
      
      <!-- Change Indicator -->
      <div v-if="change !== undefined" class="flex items-center justify-center mt-1">
        <span class="text-xs font-medium px-2 py-0.5 rounded-full flex items-center" :class="{
          'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300': change > 0,
          'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300': change < 0,
          'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300': change === 0
        }">
          <i class="pi mr-1 text-xs" :class="{
            'pi-arrow-up': change > 0,
            'pi-arrow-down': change < 0,
            'pi-minus': change === 0
          }"></i>
          {{ Math.abs(change) }}%
        </span>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [Number, String],
    required: true
  },
  change: {
    type: Number,
    default: undefined
  },
  icon: {
    type: String,
    default: 'pi pi-info-circle'
  },
  color: {
    type: String,
    default: 'text-[var(--theme-color)]'
  }
});
</script>

<style scoped>
/* Smooth transition for hover effects */
.metric-card {
  transition: all 0.2s ease;
}
</style>