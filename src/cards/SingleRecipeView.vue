<template>
    <div>
        <!-- Recipe Header -->
        <article
            class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 md:p-6 border border-gray-200 dark:border-gray-700/60">
            <div class="flex flex-col md:flex-row gap-4 md:gap-6">
                <div class="md:w-1/3">
                    <div class="relative">
                        <img :src="recipe.image"
                            class="w-full h-40 md:h-56 lg:h-64 rounded-xl object-cover shadow-lg" />
                        <span
                            class="absolute top-2 right-2 md:top-3 md:right-3 bg-white/90 dark:bg-gray-800/90 text-xs px-2 py-1 rounded-full shadow">
                            {{ recipe.category }}
                        </span>
                    </div>
                    <div class="mt-3 grid grid-cols-2 gap-2">
                        <div class="bg-gray-50 dark:bg-gray-700/50 p-2 rounded-lg">
                            <p class="text-xs text-gray-500 dark:text-gray-400">Prep Time</p>
                            <p class="font-medium text-gray-900 dark:text-white">{{ recipe.prep_time }} min</p>
                        </div>
                        <div class="bg-gray-50 dark:bg-gray-700/50 p-2 rounded-lg">
                            <p class="text-xs text-gray-500 dark:text-gray-400">Cook Time</p>
                            <p class="font-medium text-gray-900 dark:text-white">{{ recipe.cook_time }} min</p>
                        </div>
                        <div class="bg-gray-50 dark:bg-gray-700/50 p-2 rounded-lg">
                            <p class="text-xs text-gray-500 dark:text-gray-400">Difficulty</p>
                            <p class="font-medium text-gray-900 dark:text-white">{{ recipe.difficulty }}</p>
                        </div>
                        <div class="bg-gray-50 dark:bg-gray-700/50 p-2 rounded-lg">
                            <p class="text-xs text-gray-500 dark:text-gray-400">Ingredients</p>
                            <p class="font-medium text-gray-900 dark:text-white">{{ recipe.ingredients_count }}</p>
                        </div>
                    </div>
                </div>
                <div class="md:w-2/3 space-y-3 md:space-y-4">
                    <div>
                        <h3 class="text-xl md:text-2xl font-bold text-gray-900 dark:text-white">{{ recipe.title }}</h3>
                        <p class="text-sm md:text-base text-gray-600 dark:text-gray-300 mt-1">{{ recipe.description }}</p>
                    </div>

                    <!-- Key Metrics Grid -->
                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 md:gap-3">
                        <MetricCard v-for="metric in keyMetrics" :key="metric.key" :title="metric.title"
                            :value="recipe[metric.key]" :change="recipe[`${metric.key}_change`]" :icon="metric.icon"
                            :color="metric.color" />
                    </div>

                    <!-- Engagement Metrics -->
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-4 mt-3 md:mt-4">
                        <div class="space-y-2">
                            <p class="text-sm font-medium text-gray-500 dark:text-gray-400 flex items-center gap-2">
                                <i class="pi pi-clock text-[var(--theme-color)]"></i>
                                Average Active Time
                            </p>
                            <div class="flex items-center gap-2 md:gap-3">
                                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 flex-1">
                                    <div class="bg-[var(--theme-color)] h-2.5 rounded-full transition-all duration-500"
                                        :style="{ width: `${Math.min(recipe.active_time, 100)}%` }">
                                    </div>
                                </div>
                                <span
                                    class="text-xs md:text-sm font-medium text-gray-900 dark:text-white min-w-[35px] md:min-w-[40px]">
                                    {{ recipe.active_time }}%
                                </span>
                            </div>
                        </div>
                        <div class="space-y-2">
                            <p class="text-sm font-medium text-gray-500 dark:text-gray-400 flex items-center gap-2">
                                <i class="pi pi-check-circle text-[var(--theme-color)]"></i>
                                Completion Rate
                            </p>
                            <div class="flex items-center gap-2 md:gap-3">
                                <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 flex-1">
                                    <div class="bg-[var(--theme-color)] h-2.5 rounded-full transition-all duration-500"
                                        :style="{ width: `${Math.min(recipe.completion_rate, 100)}%` }">
                                    </div>
                                </div>
                                <span
                                    class="text-xs md:text-sm font-medium text-gray-900 dark:text-white min-w-[35px] md:min-w-[40px]">
                                    {{ recipe.completion_rate }}%
                                </span>
                            </div>
                        </div>
                    </div>

                    <!-- Additional Stats -->
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-2 md:gap-3 mt-3">
                        <div class="bg-gray-50 dark:bg-gray-700/50 p-2 rounded-lg">
                            <p class="text-xs text-gray-500 dark:text-gray-400">Avg. Rating</p>
                            <div class="flex items-center gap-1">
                                <i class="pi pi-star-fill text-yellow-500 text-sm"></i>
                                <p class="font-medium text-gray-900 dark:text-white">4.7</p>
                                <span class="text-xs text-gray-500 dark:text-gray-400">(128)</span>
                            </div>
                        </div>
                        <div class="bg-gray-50 dark:bg-gray-700/50 p-2 rounded-lg">
                            <p class="text-xs text-gray-500 dark:text-gray-400">Comments</p>
                            <p class="font-medium text-gray-900 dark:text-white">42</p>
                        </div>
                        <div class="bg-gray-50 dark:bg-gray-700/50 p-2 rounded-lg">
                            <p class="text-xs text-gray-500 dark:text-gray-400">Cooked</p>
                            <p class="font-medium text-gray-900 dark:text-white">1.2k</p>
                        </div>
                        <div class="bg-gray-50 dark:bg-gray-700/50 p-2 rounded-lg">
                            <p class="text-xs text-gray-500 dark:text-gray-400">Created</p>
                            <p class="font-medium text-gray-900 dark:text-white">3 months ago</p>
                        </div>
                    </div>
                </div>
            </div>
        </article>

        <!-- Data Visualization Section -->
        <div class="mt-4 md:mt-6 grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6">
            <div
                class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 md:p-6 border border-gray-200 dark:border-gray-700/60">
                <h4 class="font-medium text-gray-900 dark:text-white mb-3 md:mb-4 flex items-center gap-2">
                    <i class="pi pi-chart-bar text-[var(--theme-color)]"></i>
                    Engagement Trends
                </h4>
                <VerticalBarGraph :data="engagementData" />
            </div>
            <div
                class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 md:p-6 border border-gray-200 dark:border-gray-700/60">
                <h4 class="font-medium text-gray-900 dark:text-white mb-3 md:mb-4 flex items-center gap-2">
                    <i class="pi pi-chart-line text-[var(--theme-color)]"></i>
                    Performance Metrics
                </h4>
                <MultiAxisGraph :data="performanceData" />
            </div>
            <div
                class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 md:p-6 border border-gray-200 dark:border-gray-700/60">
                <h4 class="font-medium text-gray-900 dark:text-white mb-3 md:mb-4 flex items-center gap-2">
                    <i class="pi pi-chart-pie text-[var(--theme-color)]"></i>
                    Audience Demographics
                </h4>
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                        <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">By Age</h5>
                        <DoughnutChart :data="ageData" />
                    </div>
                    <div>
                        <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">By Gender</h5>
                        <DoughnutChart :data="genderData" />
                    </div>
                    <div>
                        <h5 class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">By Location</h5>
                        <DoughnutChart :data="locationData" />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import MetricCard from '../cards/MetricCard.vue';
import VerticalBarGraph from '../cards/VerticalBarGraph.vue';
import MultiAxisGraph from '../cards/MultiAxisGraph.vue';
import DoughnutChart from '../charts/DoughnutChart.vue';

const props = defineProps({
    recipe: {
        type: Object,
        required: true
    },
    keyMetrics: {
        type: Array,
        required: true
    },
    engagementData: {
        type: Object,
        required: true
    },
    performanceData: {
        type: Object,
        required: true
    }
});

// Demographic data for the recipe
const ageData = {
    labels: ['18-24', '25-34', '35-44', '45-54', '55+'],
    datasets: [{
        data: [15, 35, 25, 15, 10],
        backgroundColor: [
            'rgba(249, 115, 22, 0.7)',
            'rgba(249, 115, 22, 0.6)',
            'rgba(249, 115, 22, 0.5)',
            'rgba(249, 115, 22, 0.4)',
            'rgba(249, 115, 22, 0.3)'
        ]
    }]
};

const genderData = {
    labels: ['Female', 'Male', 'Other'],
    datasets: [{
        data: [65, 32, 3],
        backgroundColor: [
            'rgba(249, 115, 22, 0.7)',
            'rgba(59, 130, 246, 0.7)',
            'rgba(16, 185, 129, 0.7)'
        ]
    }]
};

const locationData = {
    labels: ['North America', 'Europe', 'Asia', 'Other'],
    datasets: [{
        data: [45, 30, 15, 10],
        backgroundColor: [
            'rgba(249, 115, 22, 0.7)',
            'rgba(59, 130, 246, 0.7)',
            'rgba(16, 185, 129, 0.7)',
            'rgba(139, 92, 246, 0.7)'
        ]
    }]
};
</script>