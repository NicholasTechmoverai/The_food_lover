<template>
    <div class="space-y-8 p-2 dark:bg-gray-900/70" :style="{ '--theme-color': auth.user?.theme || '#f97316' }">
        <!-- Header with gradient background -->
        <div class="bg-gradient-to-r from-[var(--theme-color)]/10 to-transparent p-6 rounded-xl sticky top-0">
            <div class="flex items-center justify-between flex-col md:flex-row gap-1">
                <div>
                    <h2 class="text-3xl font-bold text-gray-900 dark:text-white">
                        Our Culinary Experts
                    </h2>
                    <p class="text-gray-600 dark:text-gray-300 mt-2">
                        Discover and connect with talented chefs from around the world
                    </p>
                </div>
                <div class="flex flex-row gap-1">
                                    <button v-if="auth.user && !auth.user.isChef" @click="requestChefRole()"
                    class="flex items-center gap-2 text-sm font-medium text-[var(--theme-color)] hover:text-[var(--theme-color)]/80 transition-colors bg-white dark:bg-gray-800 px-4 py-2 rounded-lg shadow-sm">
                    <i class="pi pi-user-plus text-sm sm:text-base"></i>
                    <span>Request Chef Access</span>
                    <span
                        class="ml-auto text-xs bg-[var(--theme-color)] text-white px-2 py-0.5 sm:px-2 sm:py-1 rounded-full group-hover:bg-[var(--theme-color)]/90">Pro</span>
                </button>
                <button @click="refreshChefs"
                    class="flex items-center gap-2 text-sm font-medium text-[var(--theme-color)] hover:text-[var(--theme-color)]/80 transition-colors bg-white dark:bg-gray-800 px-4 py-2 rounded-lg shadow-sm">
                    <i class="pi pi-refresh" :class="{ 'animate-spin': loading_chefs }"></i>
                    Refresh
                </button>
                </div>

            </div>
        </div>

        <!-- Stats Overview Section -->
        <div class="space-y-2 mb-6">
            <h3 class="text-sm font-medium text-gray-500 dark:text-gray-400 px-1">
                Community Overview
            </h3>

            <!-- Loading State -->
            <div v-if="loading_chefs_stats" class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div v-for="i in 3" :key="`stats-loading-${i}`"
                    class="bg-white dark:bg-gray-800 p-5 rounded-xl shadow-xs border border-gray-100 dark:border-gray-700/60 animate-pulse">
                    <div class="h-4 w-24 bg-gray-200 dark:bg-gray-700 rounded mb-3"></div>
                    <div class="flex items-baseline gap-2">
                        <div class="h-8 w-16 bg-gray-200 dark:bg-gray-700 rounded"></div>
                        <div class="h-5 w-10 bg-gray-200 dark:bg-gray-700 rounded"></div>
                    </div>
                </div>
            </div>

            <!-- Loaded State -->
            <div v-else class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div v-for="(stat, index) in stats" :key="`stat-${index}`"
                    class="bg-white dark:bg-gray-800 p-5 rounded-xl shadow-xs border border-gray-100 dark:border-gray-700/60 hover:shadow-sm transition-all duration-200 group"
                    :class="{
                        'hover:border-[var(--theme-color)]/30': !loading_chefs_stats
                    }">
                    <p
                        class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2 transition-colors duration-200 group-hover:text-[var(--theme-color)]">
                        {{ stat.label }}
                    </p>
                    <div class="flex items-baseline gap-2">
                        <p class="text-2xl font-bold text-gray-900 dark:text-white">
                            {{ stat.value }}
                        </p>
                        <span v-if="stat.change" class="text-xs font-medium px-2 py-0.5 rounded-full" :class="{
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
                    <div v-if="index === 0" class="mt-3 h-1 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div class="h-full bg-[var(--theme-color)]" style="width: 85%"></div>
                    </div>
                </div>
                <div class="relative bg-white dark:bg-gray-800 p-5 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-700/60 hover:shadow-md transition-all duration-200 group"
                    :class="{ 'hover:border-[var(--theme-color)]/40': !loading_chefs_stats }">
                    <p
                        class="text-sm font-medium text-gray-500 dark:text-gray-400 mb-3 group-hover:text-[var(--theme-color)] transition-colors">
                        Most Popular
                    </p>

                    <div class="flex items-center gap-4">
                        <img :src="popular_chef.avatar" alt="Chef Avatar"
                            class="w-14 h-14 rounded-full ring-2 ring-[var(--theme-color)]/90 object-cover" />
                        <div class="flex-1">
                            <router-link :to="`/${popular_chef.username}`"
                                class="text-lg font-semibold text-gray-900 dark:text-white hover:text-[var(--theme-color)] transition">
                                {{ popular_chef.name }}
                            </router-link><br>
                            <router-link :to="`/${popular_chef.username}`"
                                class="text-sm text-[var(--theme-color)]/70 hover:text-[var(--theme-color)] transition">
                                {{ popular_chef.username }}
                            </router-link>
                            <div class="mt-0 text-sm text-gray-500 dark:text-gray-400">
                                <span>{{ popular_chef.views }} views</span> ·
                                <span>{{ popular_chef.likes }} likes</span> ·
                                <span>{{ popular_chef.recipes_count }} recipes</span>
                            </div>
                        </div>
                    </div>

                    <div v-if="index === 0" class="mt-4 h-2 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden">
                        <div class="h-full bg-[var(--theme-color)]" style="width: 85%"></div>
                    </div>
                </div>

            </div>
        </div>


        <!-- Loading State -->
        <div v-if="loading_chefs" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <div v-for="n in 4" :key="n"
                class="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1">
                <div class="p-5 space-y-4">
                    <div class="flex items-center gap-4">
                        <div class="w-16 h-16 rounded-full bg-gray-200 dark:bg-gray-700 animate-pulse"></div>
                        <div class="space-y-2 flex-1">
                            <div class="h-5 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-3/4"></div>
                            <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-1/2"></div>
                        </div>
                    </div>
                    <div class="grid grid-cols-3 gap-4 text-center">
                        <div v-for="n in 3" :key="n" class="space-y-1">
                            <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                            <div class="h-3 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-3/4 mx-auto"></div>
                        </div>
                    </div>
                    <div class="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-full"></div>
                    <div class="h-10 bg-gray-200 dark:bg-gray-700 rounded-lg animate-pulse mt-2"></div>
                </div>
            </div>
        </div>

        <!-- Chef Cards -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <div v-for="chef in chefs" :key="chef.id"
                class="bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-gray-100 dark:border-gray-700"
                :style="{ '--chef-theme': chef.theme || '#f97316' }">
                <!-- Chef Header with theme-based gradient -->
                <div class="h-2 bg-gradient-to-r from-[var(--chef-theme)] to-[var(--theme-color)]"></div>

                <div class="p-5">
                    <div class="flex items-start gap-4">
                        <router-link :to="`/${chef.username}`" class="flex-shrink-0 relative group">
                            <img :src="chef.avatar || 'https://ui-avatars.com/api/?background=random&name=' + encodeURIComponent(chef.name)"
                                :alt="chef.name"
                                class="w-16 h-16 rounded-full object-cover border-2 border-[var(--chef-theme)]/30 group-hover:border-[var(--chef-theme)] transition-colors duration-300" />
                            <div v-if="chef.is_following"
                                class="absolute -bottom-1 -right-1 bg-[var(--chef-theme)] text-white rounded-full w-5 h-5 flex items-center justify-center text-xs"
                                title="Following">
                                <i class="pi pi-check"></i>
                            </div>
                        </router-link>

                        <div class="flex-1 min-w-0">
                            <router-link :to="`/${chef.username}`" class="block">
                                <h3 class="text-lg font-bold text-gray-900 dark:text-white truncate">{{ chef.name }}
                                </h3>
                                <p class="text-sm text-gray-500 dark:text-gray-400">@{{ chef.username }}</p>
                            </router-link>

                            <!-- Stats -->
                            <div class="flex justify-between mt-3 text-sm">
                                <div class="text-center" v-tooltip="'Total recipes'">
                                    <p class="font-bold text-gray-900 dark:text-white">{{ chef.recipes_count }}</p>
                                    <p class="text-gray-500 dark:text-gray-400 text-xs">Recipes</p>
                                </div>
                                <div class="text-center" v-tooltip="'Total followers'">
                                    <p class="font-bold text-gray-900 dark:text-white">{{ chef.follower_count }}</p>
                                    <p class="text-gray-500 dark:text-gray-400 text-xs">Followers</p>
                                </div>
                                <div class="text-center" v-tooltip="'Total likes received'">
                                    <p class="font-bold text-gray-900 dark:text-white">{{ chef.likes_count }}</p>
                                    <p class="text-gray-500 dark:text-gray-400 text-xs">Likes</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Bio -->
                    <div v-if="chef.bio" class="mt-4">
                        <p class="text-sm text-gray-600 dark:text-gray-300 line-clamp-3 break-words" v-html="chef.bio">
                        </p>
                    </div>

                    <!-- Follow Button -->
                    <div class="mt-4" v-if="chef.id != auth?.user?.id">
                        <button @click.stop="toggleFollow(chef)"
                            class="w-full py-2 px-4 rounded-lg transition-all duration-200 font-medium flex items-center justify-center gap-2"
                            :class="{
                                'bg-[var(--chef-theme)] text-white hover:bg-[var(--chef-theme)]/90 shadow-[var(--chef-theme)]/30 hover:shadow-md': !chef.is_following,
                                'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600': chef.is_following
                            }">
                            <i :class="chef.is_following ? 'pi pi-user-minus' : 'pi pi-user-plus'"></i>
                            {{ chef.is_following ? 'Following' : 'Follow Chef' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Empty State -->
        <div v-if="!loading_chefs && chefs?.length === 0"
            class="text-center py-16 rounded-xl bg-gradient-to-br from-[var(--theme-color)]/5 to-transparent">
            <div
                class="mx-auto w-28 h-28 bg-[var(--theme-color)]/10 text-[var(--theme-color)] rounded-full flex items-center justify-center mb-6">
                <i class="pi pi-users text-4xl"></i>
            </div>
            <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">No Chefs Found</h3>
            <p class="text-gray-600 dark:text-gray-400 max-w-md mx-auto mb-6">
                We couldn't find any chefs matching your criteria. Try adjusting your search or check back later.
            </p>
            <button @click="refreshChefs"
                class="bg-[var(--theme-color)] text-white px-6 py-2 rounded-lg hover:bg-[var(--theme-color)]/90 transition-colors">
                <i class="pi pi-refresh mr-2"></i>
                Refresh List
            </button>
        </div>

        <!-- Pagination -->
        <div v-if="chefs?.length > 0" class="flex justify-center mt-8">
            <div class="flex items-center gap-2">
                <button @click="prevPage" :disabled="currentPage === 1"
                    class="p-2 rounded-full disabled:opacity-50 disabled:cursor-not-allowed" :class="{
                        'text-[var(--theme-color)] hover:bg-[var(--theme-color)]/10': currentPage > 1,
                        'text-gray-400': currentPage === 1
                    }">
                    <i class="pi pi-chevron-left"></i>
                </button>

                <div class="flex items-center gap-1">
                    <button v-for="page in visiblePages" :key="page" @click="goToPage(page)"
                        class="w-10 h-10 rounded-full flex items-center justify-center" :class="{
                            'bg-[var(--theme-color)] text-white': page === currentPage,
                            'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700': page !== currentPage
                        }">
                        {{ page }}
                    </button>
                </div>

                <button @click="nextPage" :disabled="currentPage === totalPages"
                    class="p-2 rounded-full disabled:opacity-50 disabled:cursor-not-allowed" :class="{
                        'text-[var(--theme-color)] hover:bg-[var(--theme-color)]/10': currentPage < totalPages,
                        'text-gray-400': currentPage === totalPages
                    }">
                    <i class="pi pi-chevron-right"></i>
                </button>
            </div>
        </div>
        <Toast/>

    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { make_a_post } from '../apis';
import { useAuthStore } from '../store/user';
import { useToast } from 'primevue/usetoast';

const toast = useToast();
const auth = useAuthStore();
const loading_chefs = ref(false);
const loading_chefs_stats = ref(false);
const chefs = ref(null);
const currentPage = ref(1);
const itemsPerPage = 12;
const totalItems = ref(0);

// Sample stats - replace with real data
const stats = ref([
    { label: 'Total Chefs', value: '0', change: '+0' },
    { label: 'New This Month', value: '0', change: '+0' },
    { label: 'Most Popular', value: 'None', change: null }
]);
const popular_chef = ref([])

const totalPages = computed(() => Math.ceil(totalItems.value / itemsPerPage));

const visiblePages = computed(() => {
    const pages = [];
    const maxVisible = 5;
    let start = Math.max(1, currentPage.value - Math.floor(maxVisible / 2));
    let end = Math.min(totalPages.value, start + maxVisible - 1);

    if (end - start + 1 < maxVisible) {
        start = Math.max(1, end - maxVisible + 1);
    }

    for (let i = start; i <= end; i++) {
        pages.push(i);
    }

    return pages;
});

const get_chefs = async () => {
    try {
        loading_chefs.value = true;
        const res = await make_a_post(
            "/users/get-chefs",
            auth.token,
            { page: currentPage.value, limit: itemsPerPage }
        );

        if (res.data) {
            chefs.value = res.data.chefs || [];
            totalItems.value = res.data.total || chefs.value.length;
        }
    } catch (error) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to load chefs',
            life: 3000
        });
        chefs.value = [];
    } finally {
        loading_chefs.value = false;
    }
};


const get_chef_stats = async () => {
    try {
        loading_chefs_stats.value = true;
        const res = await make_a_post(
            "/users/get-chefs-stats",
            auth.token,
        );

        if (res.data) {
            stats.value = res.data.stats || [];
            popular_chef.value = res.data.popular_chef || [];
        }
    } catch (error) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to load chef statistics',
            life: 3000
        });
    } finally {
        loading_chefs_stats.value = false;
    }
};
const refreshChefs = async () => {
    currentPage.value = 1;
    await Promise.all([
        get_chefs(),
        get_chef_stats()
    ]);
};


const toggleFollow = async (chef) => {
    try {
        const res = await make_a_post(
            `/users/${chef.id}/follow`,
            auth.token,
            {}
        );

        if (res.success) {
            chef.is_following = !chef.is_following;
            chef.follower_count += chef.is_following ? 1 : -1;

            toast.add({
                severity: 'success',
                summary: chef.is_following ? 'Following' : 'Unfollowed',
                detail: chef.is_following
                    ? `You're now following ${chef.name}`
                    : `You've unfollowed ${chef.name}`,
                life: 3000
            });
        }
    } catch (error) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to update follow status',
            life: 3000
        });
    }
};


const requestChefRole = async () => {
    if (!auth.user.id) return
    const res = await make_a_post(`/users/chef-request/${auth.user.name}`, auth.token, { chef_id: auth.user.id })
    if (res.success) {
        toast.add({
            severity: 'info',
            summary: 'Chef request sent!!',
            detail: 'You\'ll be notified once your requset has been approved!',
            life: 5000,
        })
    }
};

const nextPage = () => {
    if (currentPage.value < totalPages.value) {
        currentPage.value++;
        get_chefs();
    }
};

const prevPage = () => {
    if (currentPage.value > 1) {
        currentPage.value--;
        get_chefs();
    }
};

const goToPage = (page) => {
    currentPage.value = page;
    get_chefs();
};

onMounted(async () => {
    await Promise.all([
        get_chefs(),
        get_chef_stats()
    ]);
});
</script>

<style scoped>
/* Custom transitions */
.line-clamp-3 {
    display: -webkit-box;
    -webkit-line-clamp: 4;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

/* Animation for follow button */
@keyframes pulse {

    0%,
    100% {
        transform: scale(1);
        box-shadow: 0 0 0 0 rgba(var(--theme-color-rgb), 0.4);
    }

    50% {
        transform: scale(1.02);
        box-shadow: 0 0 0 6px rgba(var(--theme-color-rgb), 0);
    }
}

.follow-pulse {
    animation: pulse 1.5s infinite;
}
</style>