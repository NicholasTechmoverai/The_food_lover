<template>
    <div :style="{ '--theme-color': auth.user?.theme || '#f97316' }"
        class="min-h-screen bg-gray-50 dark:bg-gray-900 p-1 md:p-2 lg:p-4">
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
        <main class="mx-auto py-6 gap-4 relative">
            <div class="flex flex-col lg:flex-row gap-4">
                <!-- Recipe Sidebar -->
                <transition name="slide">
                    <div v-if="sidebarOpen"
                        class="w-full xs:w-72 md:max-w-[300px] bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 h-fit sticky top-24 border border-gray-200 dark:border-gray-700 transition-all duration-300">
                        <div class="flex justify-between items-center mb-4">
                            <h3 class="font-semibold text-lg text-gray-900 dark:text-white flex items-center gap-2">
                                <i class="pi pi-book"></i>
                                Your Recipes
                            </h3>
                            <button @click="sidebarOpen = false"
                                class="p-1.5 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors md:hidden">
                                <i class="pi pi-chevron-left text-sm"></i>
                            </button>
                        </div>

                        <div class="space-y-2 max-h-[calc(100vh-180px)] overflow-y-auto pr-2">
                            <div v-if="loadingRecipes" class="space-y-2">
                                <div v-for="i in 3" :key="`recipe-loading-${i}`" class="p-3 rounded-lg">
                                    <div class="flex items-center gap-3">
                                        <div class="w-12 h-12 rounded-lg bg-gray-200 dark:bg-gray-700 animate-pulse">
                                        </div>
                                        <div class="flex-1 min-w-0">
                                            <div
                                                class="h-4 w-3/4 bg-gray-200 dark:bg-gray-700 rounded mb-2 animate-pulse">
                                            </div>
                                            <div class="h-3 w-1/2 bg-gray-200 dark:bg-gray-700 rounded animate-pulse">
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            <div v-else v-for="recipe in recipes" :key="recipe.id" @click="selectRecipe(recipe.id)"
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
                                            {{ recipe.name }}
                                        </h4>
                                        <div v-if="recipe.id !== 0"
                                            class="flex items-center gap-3 text-xs text-gray-500 dark:text-gray-400 mt-1">
                                            <span class="flex items-center"><i class="pi pi-calendar mr-1"></i>{{
                                                formatDistanceToNow(recipe.created_at) }}</span>
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
                            Performance Overview{{ ismobile }}
                        </h3>

                        <div v-if="loadingStats" class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 md:gap-4">
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
                                            {{ selectedRecipe.name }}
                                        </span>
                                    </div>
                                </div>
                                <div class="md:w-2/3 space-y-3 md:space-y-4">
                                    <div>
                                        <h3 class="text-xl md:text-2xl font-bold text-gray-900 dark:text-white">
                                            {{ selectedRecipe.title || selectedRecipe.name }}
                                        </h3>
                                        <p v-if="selectedRecipe.description"
                                            class="text-sm md:text-base text-gray-600 dark:text-gray-300 mt-1">
                                            {{ selectedRecipe.description }}
                                        </p>
                                    </div>

                                    <!-- Key Metrics Grid -->
                                    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 md:gap-3">
                                        <div v-if="loadingReports" v-for="i in 4" :key="`metric-loading-${i}`"
                                            class="p-3 rounded-lg bg-gray-100 dark:bg-gray-700/50 animate-pulse">
                                            <div class="h-4 w-3/4 bg-gray-200 dark:bg-gray-600 rounded mb-2"></div>
                                            <div class="h-6 w-1/2 bg-gray-200 dark:bg-gray-600 rounded"></div>
                                        </div>
                                        <MetricCard v-else v-for="metric in keyMetrics" :key="metric.key"
                                            :title="metric.title" :value="selectedRecipe[metric.key]"
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
                                            <div v-if="loadingReports"
                                                class="h-2.5 bg-gray-200 dark:bg-gray-700 rounded-full animate-pulse">
                                            </div>
                                            <div v-else class="flex items-center gap-2 md:gap-3">
                                                <div
                                                    class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 flex-1">
                                                    <div class="bg-[var(--theme-color)] h-2.5 rounded-full transition-all duration-500"
                                                        :style="{ width: `${Math.min(selectedRecipe.active_time || 0, 100)}%` }">
                                                    </div>
                                                </div>
                                                <span
                                                    class="text-xs md:text-sm font-medium text-gray-900 dark:text-white min-w-[35px] md:min-w-[40px]">
                                                    {{ selectedRecipe.active_time || 0 }}%
                                                </span>
                                            </div>
                                        </div>
                                        <div class="space-y-2">
                                            <p
                                                class="text-sm font-medium text-gray-500 dark:text-gray-400 flex items-center gap-2">
                                                <i class="pi pi-check-circle text-[var(--theme-color)]"></i>
                                                Completion Rate
                                            </p>
                                            <div v-if="loadingReports"
                                                class="h-2.5 bg-gray-200 dark:bg-gray-700 rounded-full animate-pulse">
                                            </div>
                                            <div v-else class="flex items-center gap-2 md:gap-3">
                                                <div
                                                    class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5 flex-1">
                                                    <div class="bg-[var(--theme-color)] h-2.5 rounded-full transition-all duration-500"
                                                        :style="{ width: `${Math.min(selectedRecipe.completion_rate || 0, 100)}%` }">
                                                    </div>
                                                </div>
                                                <span
                                                    class="text-xs md:text-sm font-medium text-gray-900 dark:text-white min-w-[35px] md:min-w-[40px]">
                                                    {{ selectedRecipe.completion_rate || 0 }}%
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
                                class="bg-white dark:bg-gray-800 shrink-0 rounded-xl shadow-sm p-4 md:p-6 border border-gray-200 dark:border-gray-700/60">
                                <h4
                                    class="font-medium text-gray-900 dark:text-white mb-3 md:mb-4 flex items-center gap-2">
                                    <i class="pi pi-chart-bar text-[var(--theme-color)]"></i>
                                    Engagement Trends
                                </h4>
                                <div v-if="loadingReports"
                                    class="h-64 bg-gray-100 dark:bg-gray-700 rounded-xl animate-pulse"></div>
                                <VerticalBarGraph v-else :data="engagementData" />       
                            </div>
                            <div
                                class="bg-white dark:bg-gray-800 rounded-xl shrink-0 shadow-sm p-4 md:p-6 border border-gray-200 dark:border-gray-700/60">
                                <h4
                                    class="font-medium text-gray-900 dark:text-white mb-3 md:mb-4 flex items-center gap-2">
                                    <i class="pi pi-chart-line text-[var(--theme-color)]"></i>
                                    Performance Metrics
                                </h4>
                                <div v-if="loadingPerformance"
                                    class="h-64 bg-gray-100 dark:bg-gray-700 rounded-xl animate-pulse"></div>
                                <MultiAxisGraph v-else :data="performanceData" />
                            </div>

                        </div>
                    </section>
                    <!-- Empty State -->
                    <section v-if="!selectedRecipe" class="grid grid-cols-1 md:grid-cols-2 gap-2 ">
                        <div
                            class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 md:p-12 text-center border border-gray-200 dark:border-gray-700/60 max-w-md mx-auto">
                            <PolarAreaGraph :data="distributionData" />
                        </div>
                        <div
                            class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-6 md:p-12 text-center border border-gray-200 dark:border-gray-700/60 max-w-md mx-auto">
                            <VerticalBarGraph :data="distributionData" />
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
import { ref, computed, onMounted ,watch} from 'vue';
import VerticalBarGraph from '../cards/VerticalBarGraph.vue';
import PolarAreaGraph from '../cards/PolarAreaGraph.vue';
import MultiAxisGraph from '../cards/MultiAxisGraph.vue';
import MetricCard from '../cards/MetricCard.vue';
import { recipesSocket } from '../a_websocket';
import { formatDistanceToNow } from 'date-fns';
import { useIsMobile } from '../reusables';
import router from '../router';
import { useRoute } from 'vue-router'
const route = useRoute()


const ismobile = useIsMobile()

// Stores and utilities
const toast = useToast();
const auth = useAuthStore();

// UI State
const sidebarOpen = ref(true);
const selectedRecipe = ref(null);

// Loading States
const loadingRecipes = ref(false);
const loadingStats = ref(false);
const loadingReports = ref(false);
const loadingPerformance = ref(false);

// Data Refs
const recipes = ref([{
    id: 0,
    name: "General Overview",
    image: "https://images.unsplash.com/photo-1490645935967-10de6ba17061",
    created_at: ""
}]);

const stats = ref([
    { label: "Total Views", value: "0", change: 0, percent: 0, icon: "pi pi-eye" },
    { label: "Total Engagements", value: "0", change: 0, percent: 0, icon: "pi pi-heart" },
    { label: "Total ActiveTime", value: "0", change: 0, percent: 0, icon: "pi pi-users" }
]);

const keyMetrics = [
    { key: 'views', title: 'Views', icon: 'pi pi-eye', color: 'text-blue-500' },
    { key: 'likes', title: 'Likes', icon: 'pi pi-heart', color: 'text-red-500' },
    { key: 'shares', title: 'Shares', icon: 'pi pi-share-alt', color: 'text-green-500' },
    { key: 'saves', title: 'Saves', icon: 'pi pi-bookmark', color: 'text-purple-500' }
];

const distributionData = ref({
    labels: [],
    datasets: [{
        data: [],
        backgroundColor: [],
        label: 'recipe:',
    }]
});



const engagementData = ref(null);
const performanceData = ref(null);

// Methods
const toggleSidebar = () => {
    sidebarOpen.value = !sidebarOpen.value;
};

const active_recpe = ref(0)

const selectRecipe = async (recipe_id) => {
    if (recipe_id !== 0) {
        router.push({
            path: "/reports",
            query: { recipe: recipe_id },
        })
        await Promise.all([
            fetchRecipeReports(recipe_id),
            fetchRecipePerformance(recipe_id)
        ]);
    } else {
        selectedRecipe.value = null;

        router.push({
            path: "/reports",
            query: { recipe: 0 },
        })
        fetchStats();
    }
    if (ismobile.value) {
        toggleSidebar()
    }
};

const fetchRecipes = async () => {
    loadingRecipes.value = true;
    recipesSocket.emit("get_all_recipes", { token: auth.token.token });

    const handler = (data) => {
        recipes.value = [
            {
                id: 0,
                name: "General Overview",
                image: "https://images.unsplash.com/photo-1490645935967-10de6ba17061",
                created_at: ""
            },
            ...data.all_recipes
        ];
        loadingRecipes.value = false;
        recipesSocket.off("response_get_all_recipes", handler);
    };

    recipesSocket.on("response_get_all_recipes", handler);
};

const fetchStats = async () => {
    loadingStats.value = true;
    recipesSocket.emit("get_all_recipes_stats", { token: auth.token.token });

    const handler = (data) => {
        stats.value = data.stats;

        distributionData.value = {
            labels: data.stats_graph_meta.labels,
            datasets: [{
                ...distributionData.value.datasets[0],
                data: data.stats_graph_meta.data,
                backgroundColor: data.stats_graph_meta.colors
            }]
        };

        loadingStats.value = false;
        recipesSocket.off("response_get_all_recipes_stats", handler);
    };

    recipesSocket.on("response_get_all_recipes_stats", handler);
};

const fetchRecipeReports = async (recipeId) => {
    if (!recipeId) return;

    loadingReports.value = true;
    recipesSocket.emit("get_recipe_report", {
        token: auth.token.token,
        recipe_id: recipeId,
    });

    const handler = (data) => {
        selectedRecipe.value = data.recipe_meta;
        engagementData.value = data.chart_meta_data;
        loadingReports.value = false;
        recipesSocket.off("response_get_recipe_report", handler);
    };

    recipesSocket.on("response_get_recipe_report", handler);
};

const fetchRecipePerformance = async (recipeId) => {
    if (!recipeId) return;

    loadingPerformance.value = true;
    recipesSocket.emit("get_recipe_performance", {
        token: auth.token.token,
        recipe_id: recipeId,
    });

    const handler = (data) => {
        performanceData.value = data;
        loadingPerformance.value = false;
        recipesSocket.off("response_get_recipe_performance", handler);
    };

    recipesSocket.on("response_get_recipe_performance", handler);
};

const init = async () => {
  const recipeId = route.query.recipe;

  if (!recipeId || recipeId == 0) {
    if (route.query.recipe !== '0') {
      router.replace({
        path: '/reports',
        query: { recipe: 0 }
      });
    }

    await Promise.all([
      fetchStats(),
      fetchRecipes()
    ]);
  } else {
    await Promise.all([
      fetchRecipeReports(recipeId),
      fetchRecipePerformance(recipeId),
      fetchRecipes()
    ]);
  }
};

watch(() => route.query.recipe, () => {
  init();
});

onMounted(() => {
  init();
});
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

/* Custom scrollbar */
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