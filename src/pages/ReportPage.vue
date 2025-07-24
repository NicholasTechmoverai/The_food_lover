<template>
    <div :style="{ '--theme-color': auth.user?.theme || '#f97316' }" class="min-h-screen bg-gray-50 dark:bg-gray-900 p-1 md:p-2 lg:p-4">
        <!-- Header Section -->
        <header class="sticky top-0 z-10 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
            <div
                class="bg-gradient-to-r from-[var(--theme-color)]/10 to-transparent p-4 md:p-6 rounded-none md:rounded-xl">
                <div class="container mx-auto flex items-center justify-between flex-col md:flex-row gap-3 md:gap-4">
                    <div class="text-center md:text-left">
                        <h2 class="text-2xl md:text-3xl font-bold text-gray-900 dark:text-white">
                            Recipe Analytics
                        </h2>
                        <p class="text-sm md:text-base text-gray-600 dark:text-gray-300 mt-1 md:mt-2">
                            Track performance metrics for your culinary creations
                        </p>
                    </div>
                    <div class="flex flex-row gap-2">
                        <button @click="toggleSidebar"
                            class="flex items-center gap-2 px-3 py-1.5 md:px-4 md:py-2 rounded-lg bg-[var(--theme-color)]/10 hover:bg-[var(--theme-color)]/20 transition-colors text-sm md:text-base">
                            <i class="pi" :class="sidebarOpen ? 'pi-times' : 'pi-book'"></i>
                            <span>{{ sidebarOpen ? 'Hide Recipes' : 'Show Recipes' }}</span>
                        </button>
                    </div>
                </div>
            </div>
        </header>

        <!-- Main Content Area -->
        <main class="mx-auto  py-6 gap-4 relative">
            <div class="flex flex-col lg:flex-row gap-4">
                <!-- Recipe Sidebar -->
                <transition name="slide">
                    <div v-if="sidebarOpen"
                        class="w-72 bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 h-fit sticky top-24 border border-gray-200 dark:border-gray-700 transition-all duration-300">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="font-semibold text-lg text-gray-900 dark:text-white flex items-center gap-2">
                                <i class="pi pi-book"></i>
                                Your Recipes
                            </h3>
                            <button @click="sidebarOpen = false"
                                class="p-1.5 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors">
                                <i class="pi pi-chevron-left text-sm"></i>
                            </button>
                        </div>

                        <div class="space-y-2 max-h-[calc(100vh-180px)] overflow-y-auto pr-2">
                            <div v-for="recipe in recipes" :key="recipe.id" @click="selectRecipe(recipe)"
                                class="p-3 rounded-lg cursor-pointer transition-all duration-200" :class="{
                                    'bg-[var(--theme-color)]/10 border-l-4 border-[var(--theme-color)] shadow-[var(--theme-color)]/5': selectedRecipe?.id === recipe.id,
                                    'hover:bg-gray-100 dark:hover:bg-gray-700/50': selectedRecipe?.id !== recipe.id
                                }">
                                <div class="flex items-center gap-3">
                                    <div class="relative">
                                        <img :src="recipe.image" class="w-12 h-12 rounded-lg object-cover" />
                                        <span v-if="recipe.id === 0"
                                            class="absolute -top-2 -right-2 bg-[var(--theme-color)] text-white text-xs px-1.5 py-0.5 rounded-full">
                                            <i class="pi pi-chart-line"></i>
                                        </span>
                                    </div>
                                    <div class="flex-1 min-w-0">
                                        <h4 class="font-medium text-gray-900 dark:text-white truncate">
                                            {{ recipe.title }}
                                        </h4>
                                        <div v-if="recipe.id !== 0"
                                            class="flex items-center gap-3 text-xs text-gray-500 dark:text-gray-400 mt-1">
                                            <span class="flex items-center"><i class="pi pi-eye mr-1"></i>{{
                                                formatNumber(recipe.views) }}</span>
                                            <span class="flex items-center"><i class="pi pi-heart mr-1"></i>{{
                                                formatNumber(recipe.likes) }}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </transition>

                <!-- Analytics Dashboard -->
                <div class="flex-1 space-y-6 transition-all duration-300">
                    <!-- Summary Stats Cards -->
                    <section class="space-y-2">
                        <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 px-1 flex items-center gap-2">
                            <i class="pi pi-chart-bar"></i>
                            Performance Overview
                        </h3>

                        <div v-if="loading_chefs_stats"
                            class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 md:gap-4">
                            <div v-for="i in 3" :key="`stats-loading-${i}`"
                                class="bg-white dark:bg-gray-800 p-4 md:p-5 rounded-xl shadow-xs border border-gray-100 dark:border-gray-700/60 animate-pulse">
                                <div class="h-4 w-24 bg-gray-200 dark:bg-gray-700 rounded mb-3"></div>
                                <div class="flex items-baseline gap-2">
                                    <div class="h-8 w-16 bg-gray-200 dark:bg-gray-700 rounded"></div>
                                    <div class="h-5 w-10 bg-gray-200 dark:bg-gray-700 rounded"></div>
                                </div>
                            </div>
                        </div>

                        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 md:gap-4">
                            <div v-for="(stat, index) in stats" :key="`stat-${index}`"
                                class="bg-white dark:bg-gray-800 p-4 md:p-5 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700/60 hover:shadow-md transition-all duration-200 group hover:border-[var(--theme-color)]/30">
                                <p
                                    class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2 transition-colors duration-200 group-hover:text-[var(--theme-color)] flex items-center gap-2">
                                    <i :class="stat.icon" class="text-[var(--theme-color)]/80"></i>
                                    {{ stat.label }}
                                </p>
                                <div class="flex items-baseline gap-2">
                                    <p class="text-xl md:text-2xl font-bold text-gray-900 dark:text-white">
                                        {{ stat.value }}
                                    </p>
                                    <span v-if="stat.change" class="text-xs font-medium px-2 py-0.5 rounded-full"
                                        :class="{
                                            'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300': stat.change > 0,
                                            'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300': stat.change < 0,
                                            'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300': stat.change === 0
                                        }">
                                        <i class="pi mr-0.5 text-xs" :class="{
                                            'pi-arrow-up': stat.change > 0,
                                            'pi-arrow-down': stat.change < 0,
                                            'pi-minus': stat.change === 0
                                        }"></i>
                                        {{ Math.abs(stat.change) }}%
                                    </span>
                                </div>
                                <div v-if="index === 0"
                                    class="mt-3 h-1.5 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                                    <div class="h-full bg-[var(--theme-color)]" :style="{ width: `${stat.percent}%` }">
                                    </div>
                                </div>
                            </div>
                        </div>
                    </section>

                    <!-- Detailed Recipe Analytics -->
                    <section v-if="selectedRecipe">
                        <!-- Recipe Header -->
                        <article
                            class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 md:p-6 border border-gray-200 dark:border-gray-700/60">
                            <div class="flex flex-col md:flex-row gap-4 md:gap-6">
                                <div class="md:w-1/3">
                                    <div class="relative">
                                        <img :src="selectedRecipe.image"
                                            class="w-full h-40 md:h-56 lg:h-64 rounded-xl object-cover shadow-lg" />
                                        <span
                                            class="absolute top-2 right-2 md:top-3 md:right-3 bg-white/90 dark:bg-gray-800/90 text-xs px-2 py-1 rounded-full shadow">
                                            {{ selectedRecipe.category }}
                                        </span>
                                    </div>
                                </div>
                                <div class="md:w-2/3 space-y-3 md:space-y-4">
                                    <div>
                                        <h3 class="text-xl md:text-2xl font-bold text-gray-900 dark:text-white">{{
                                            selectedRecipe.title }}</h3>
                                        <p class="text-sm md:text-base text-gray-600 dark:text-gray-300 mt-1">{{
                                            selectedRecipe.description }}</p>
                                    </div>

                                    <!-- Key Metrics Grid -->
                                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 md:gap-3">
                                        <MetricCard v-for="metric in keyMetrics" :key="metric.key" :title="metric.title"
                                            :value="selectedRecipe[metric.key]"
                                            :change="selectedRecipe[`${metric.key}_change`]" :icon="metric.icon"
                                            :color="metric.color" />
                                    </div>

                                    <!-- Engagement Metrics -->
                                    <div class="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-4 mt-3 md:mt-4">
                                        <div class="space-y-2">
                                            <p
                                                class="text-sm font-medium text-gray-500 dark:text-gray-400 flex items-center gap-2">
                                                <i class="pi pi-clock text-[var(--theme-color)]"></i>
                                                Average Active Time
                                            </p>
                                            <div class="flex items-center gap-2 md:gap-3">
                                                <div
                                                    class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 flex-1">
                                                    <div class="bg-[var(--theme-color)] h-2.5 rounded-full transition-all duration-500"
                                                        :style="{ width: `${Math.min(selectedRecipe.active_time, 100)}%` }">
                                                    </div>
                                                </div>
                                                <span
                                                    class="text-xs md:text-sm font-medium text-gray-900 dark:text-white min-w-[35px] md:min-w-[40px]">
                                                    {{ selectedRecipe.active_time }}%
                                                </span>
                                            </div>
                                        </div>
                                        <div class="space-y-2">
                                            <p
                                                class="text-sm font-medium text-gray-500 dark:text-gray-400 flex items-center gap-2">
                                                <i class="pi pi-check-circle text-[var(--theme-color)]"></i>
                                                Completion Rate
                                            </p>
                                            <div class="flex items-center gap-2 md:gap-3">
                                                <div
                                                    class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 flex-1">
                                                    <div class="bg-[var(--theme-color)] h-2.5 rounded-full transition-all duration-500"
                                                        :style="{ width: `${Math.min(selectedRecipe.completion_rate, 100)}%` }">
                                                    </div>
                                                </div>
                                                <span
                                                    class="text-xs md:text-sm font-medium text-gray-900 dark:text-white min-w-[35px] md:min-w-[40px]">
                                                    {{ selectedRecipe.completion_rate }}%
                                                </span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </article>

                        <!-- Data Visualization Section -->
                        <div class="mt-4 md:mt-6 grid grid-cols-1 lg:grid-cols-2 gap-4 md:gap-6">
                            <div
                                class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 md:p-6 border border-gray-200 dark:border-gray-700/60">
                                <h4
                                    class="font-medium text-gray-900 dark:text-white mb-3 md:mb-4 flex items-center gap-2">
                                    <i class="pi pi-chart-bar text-[var(--theme-color)]"></i>
                                    Engagement Trends
                                </h4>
                                <VerticalBarGraph :data="engagementData" />
                            </div>
                            <div
                                class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 md:p-6 border border-gray-200 dark:border-gray-700/60">
                                <h4
                                    class="font-medium text-gray-900 dark:text-white mb-3 md:mb-4 flex items-center gap-2">
                                    <i class="pi pi-chart-line text-[var(--theme-color)]"></i>
                                    Performance Metrics
                                </h4>
                                <MultiAxisGraph :data="performanceData" />
                            </div>
                            <div v-if="selectedRecipe.id === 0"
                                class="lg:col-span-2 bg-white dark:bg-gray-800 rounded-xl shadow-sm p-4 md:p-6 border border-gray-200 dark:border-gray-700/60">
                                <h4
                                    class="font-medium text-gray-900 dark:text-white mb-3 md:mb-4 flex items-center gap-2">
                                    <i class="pi pi-chart-pie text-[var(--theme-color)]"></i>
                                    Recipe Distribution
                                </h4>
                                <PolarAreaGraph :data="distributionData" />
                            </div>
                        </div>
                    </section>

                    <!-- Empty State -->
                    <section v-else
                        class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 md:p-12 text-center border border-gray-200 dark:border-gray-700/60">
                        <div class="max-w-md mx-auto">
                            <div
                                class="w-16 h-16 md:w-24 md:h-24 mx-auto mb-4 md:mb-6 rounded-full bg-[var(--theme-color)]/10 flex items-center justify-center">
                                <i class="pi pi-chart-line text-2xl md:text-4xl text-[var(--theme-color)]"></i>
                            </div>
                            <h3 class="text-lg md:text-xl font-medium text-gray-900 dark:text-white mb-2">No Recipe
                                Selected</h3>
                            <p class="text-sm md:text-base text-gray-500 dark:text-gray-400 mb-4 md:mb-6">
                                Select a recipe from the sidebar to view detailed analytics and performance metrics.
                            </p>
                            <button @click="toggleSidebar"
                                class="px-4 py-2 md:px-5 md:py-2.5 bg-[var(--theme-color)] text-white rounded-lg hover:bg-[var(--theme-color)]/90 transition flex items-center gap-2 mx-auto text-sm md:text-base">
                                <i class="pi pi-book"></i>
                                Browse Recipes
                            </button>
                        </div>
                    </section>
                </div>
            </div>
        </main>
    </div>
</template>

<script setup>
import { useAuthStore } from '../store/user';
import { useToast } from 'primevue/usetoast';
import { ref, computed } from 'vue';
import VerticalBarGraph from '../cards/VerticalBarGraph.vue';
import PolarAreaGraph from '../cards/PolarAreaGraph.vue';
import MultiAxisGraph from '../cards/MultiAxisGraph.vue';
import MetricCard from '../cards/MetricCard.vue';

const toast = useToast();
const auth = useAuthStore();

const sidebarOpen = ref(true);
const selectedRecipe = ref(null);

const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value;
};

const selectRecipe = (recipe) => {
    selectedRecipe.value = recipe.id === 0 ? null : recipe;
};

const formatNumber = (num) => {
    return new Intl.NumberFormat('en-US').format(num);
};

// Sample data
const recipes = [
    {
        id: 0,
        title: "General Overview",
        description: "Aggregate analytics across all your recipes",
        category: "Dashboard",
        image: "https://images.unsplash.com/photo-1490645935967-10de6ba17061",
    },
    {
        id: 1,
        title: "Spicy Garlic Shrimp Pasta",
        description: "A delicious pasta dish with a spicy garlic kick and fresh shrimp",
        category: "Pasta",
        image: "https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb",
        views: 12543,
        views_change: 12.5,
        likes: 892,
        likes_change: 8.2,
        shares: 324,
        shares_change: 5.7,
        saves: 567,
        saves_change: 15.3,
        active_time: 78,
        completion_rate: 65
    },
    {
        id: 2,
        title: "Avocado Toast",
        description: "Healthy breakfast with creamy avocado and poached eggs",
        category: "Breakfast",
        image: "https://images.unsplash.com/photo-1511690656952-34342bb7c2f2",
        views: 8765,
        views_change: -3.2,
        likes: 654,
        likes_change: 2.1,
        shares: 198,
        shares_change: -1.5,
        saves: 432,
        saves_change: 7.8,
        active_time: 65,
        completion_rate: 72
    },
    {
        id: 3,
        title: "Chocolate Lava Cake",
        description: "Decadent chocolate dessert with a molten center",
        category: "Dessert",
        image: "https://images.unsplash.com/photo-1571115177098-24ec42ed204d",
        views: 15321,
        views_change: 18.7,
        likes: 1243,
        likes_change: 22.4,
        shares: 512,
        shares_change: 14.6,
        saves: 876,
        saves_change: 19.2,
        active_time: 82,
        completion_rate: 58
    }
];

const stats = [
    { label: "Total Views", value: "36,629", change: 12.5, percent: 85, icon: "pi pi-eye" },
    { label: "Total Engagements", value: "2,789", change: 8.2, percent: 65, icon: "pi pi-heart" },
    { label: "New Followers", value: "324", change: 5.7, percent: 45, icon: "pi pi-users" }
];

const keyMetrics = [
    { key: 'views', title: 'Views', icon: 'pi pi-eye', color: 'text-blue-500' },
    { key: 'likes', title: 'Likes', icon: 'pi pi-heart', color: 'text-red-500' },
    { key: 'shares', title: 'Shares', icon: 'pi pi-share-alt', color: 'text-green-500' },
    { key: 'saves', title: 'Saves', icon: 'pi pi-bookmark', color: 'text-purple-500' }
];

const engagementData = computed(() => ({
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
        {
            label: 'Views',
            backgroundColor: 'rgba(249, 115, 22, 0.7)',
            data: [65, 59, 80, 81, 56, 55]
        },
        {
            label: 'Engagements',
            backgroundColor: 'rgba(249, 115, 22, 0.4)',
            data: [28, 48, 40, 19, 86, 27]
        }
    ]
}));

const performanceData = computed(() => ({
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
        {
            label: 'Completion Rate',
            borderColor: 'rgba(249, 115, 22, 1)',
            backgroundColor: 'rgba(249, 115, 22, 0.2)',
            data: [65, 59, 80, 81, 56, 55, 40],
            yAxisID: 'y'
        },
        {
            label: 'Active Time (min)',
            borderColor: 'rgba(59, 130, 246, 1)',
            backgroundColor: 'rgba(59, 130, 246, 0.2)',
            data: [28, 48, 40, 19, 86, 27, 90],
            yAxisID: 'y1'
        }
    ]
}));

const distributionData = computed(() => ({
    labels: ['Pasta', 'Breakfast', 'Dessert', 'Salad', 'Soup'],
    datasets: [{
        data: [11, 16, 7, 3, 14],
        backgroundColor: [
            'rgba(249, 115, 22, 0.7)',
            'rgba(249, 115, 22, 0.6)',
            'rgba(249, 115, 22, 0.5)',
            'rgba(249, 115, 22, 0.4)',
            'rgba(249, 115, 22, 0.3)'
        ]
    }]
}));

const loading_chefs_stats = ref(false);
</script>

<style scoped>
.slide-enter-active,
.slide-leave-active {
    transition: all 0.3s ease;
}

.slide-enter-from,
.slide-leave-to {
    transform: translateX(-100%);
    opacity: 0;
}

/* Custom scrollbar for sidebar */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: #888;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: #555;
}

.dark ::-webkit-scrollbar-track {
    background: #2d3748;
}

.dark ::-webkit-scrollbar-thumb {
    background: #4a5568;
}

.dark ::-webkit-scrollbar-thumb:hover {
    background: #718096;
}
</style>