<template>
    <div
        class="min-h-screen bg-gradient-to-br   from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-4 md:p-8 overflow-auto">
        <div class="max-w-6xl mx-auto">

            <!-- Recipe Header -->
            <header class="mb-10 animate-fade-in">
                <!-- Main Hero Container -->
                <div class="relative overflow-hidden rounded-3xl p-1  flex flex-col md:flex-row items-center gap-6 "
                    :style="{ borderLeft: `6px solid ${recipe?.repiceColor || '#f97316'}` }">
                    <!-- Dish Image -->
                    <img v-if="recipe?.image" :src="recipe.image" :alt="recipe.recipeName || 'Meal cover'"
                        class="w-full md:w-[320px] h-[220px] md:h-[280px] object-cover rounded-2xl shadow-md" />

                    <!-- Text Content -->
                    <div class="flex-1 space-y-4 text-center md:text-left">
                        <!-- Title -->
                        <h1 :style="{ color: recipe?.repiceColor }"
                            class="text-3xl md:text-4xl lg:text-5xl font-extrabold text-transparent bg-gradient-to-r from-amber-500 to-yellow-600 bg-clip-text leading-tight">
                            {{ formattedRecipeName }}
                        </h1>

                        <!-- Fun Description -->
                        <p v-if="recipe?.description"
                            class="text-gray-600 dark:text-gray-300 text-base leading-relaxed italic"
                            v-html="recipe.description">
                        </p>

                        <!-- Metadata: Time, Difficulty, Category -->
                        <div class="flex flex-wrap gap-2 justify-center md:justify-start">
                            <span v-if="recipe?.cookTime"
                                class="flex items-center gap-1 px-3 py-1 text-xs md:text-sm rounded-full bg-amber-100 dark:bg-amber-900/50 text-amber-800 dark:text-amber-200">
                                <i class="pi pi-clock"></i> {{ formatTime(recipe.cookTime) }}
                            </span>

                            <span v-if="recipe?.complexityLevel"
                                class="flex items-center gap-1 px-3 py-1 text-xs md:text-sm rounded-full bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-200">
                                <i class="pi pi-cog"></i> {{ recipe.complexityLevel.name }}
                            </span>

                            <span v-for="cat in recipe?.category || []" :key="cat"
                                class="px-3 py-1 text-xs md:text-sm rounded-full bg-green-100 dark:bg-green-900/50 text-green-800 dark:text-green-200">
                                {{ cat }}
                            </span>
                        </div>

                        <!-- Tags -->
                        <div v-if="recipe?.tags?.length" class="mt-2 flex flex-wrap gap-2">
                            <span v-for="tag in recipe.tags" :key="tag"
                                class="px-3 py-1 text-xs md:text-sm rounded-full bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-200">
                                #{{ tag }}
                            </span>
                        </div>
                    </div>
                </div>
            </header>


            <!-- Loading State -->
            <div v-if="isLoading" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div v-for="i in 2" :key="i" class="bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
                    <Skeleton class="w-full h-48 rounded-t-xl" />
                    <div class="p-4 space-y-3">
                        <Skeleton class="w-3/4 h-6" />
                        <Skeleton class="w-full h-4" />
                        <Skeleton class="w-full h-4" />
                        <Skeleton class="w-1/2 h-4" />
                    </div>
                </div>
                <div v-for="i in 4">
                    <RecipeStepCard />
                </div>
            </div>

            <!-- Main Content -->
            <template v-else-if="recipe">
                <!-- User + View Toggle -->
                <section class="flex flex-col md:flex-row justify-between items-center gap-6 mb-8">
                    <!-- User Info -->
                    <div class="flex items-center gap-4">
                        <img :src="recipe.user?.profilePic || defaultAvatar" alt="User"
                            class="w-12 h-12 md:w-14 md:h-14 rounded-full border-2 border-white dark:border-gray-700 shadow-md object-cover" />
                        <div>
                            <h4 class="text-base font-semibold text-gray-900 dark:text-white">
                                {{ recipe.user?.name || 'Anonymous Chef' }}
                            </h4>
                            <p class="text-sm text-gray-500 dark:text-gray-400">
                                {{ recipe.user?.totalRecipes || 0 }} recipes • {{ formatDate(recipe.updatedAt) }}
                            </p>
                        </div>
                    </div>

                    <!-- Toggle Buttons -->
                    <div
                        class="flex items-center gap-1 bg-white dark:bg-gray-800 p-1 rounded-full shadow-inner border border-gray-100 dark:border-gray-700">
                        <button v-for="option in listTypeOptions" :key="option.value" @click="listType = option.value"
                            :class="[
                                'flex items-center gap-2 px-3 py-1.5 md:px-4 md:py-2 text-xs md:text-sm font-medium rounded-full transition-all',
                                listType === option.value
                                    ? 'bg-amber-500/10 text-amber-700 dark:bg-amber-700/30 dark:text-amber-200 shadow-sm'
                                    : 'text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200'
                            ]">
                            <i :class="option.icon" class="text-base"></i>
                            <span class="hidden sm:inline">{{ option.label }}</span>
                        </button>
                    </div>
                </section>

                <!-- Tags -->
                <div v-if="recipe.tags?.length" class="flex flex-wrap gap-2 mb-6">
                    <span v-for="tag in recipe.tags" :key="tag"
                        class="px-2.5 py-1 text-xs rounded-full bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 transition cursor-pointer">
                        #{{ tag }}
                    </span>
                </div>

                <!-- Step Viewer -->
                <div class="bg-white dark:bg-gray-800 rounded-2xl md:rounded-3xl shadow-lg overflow-hidden">
                    <FlowGalleryViewer v-if="listType === 'flow' && steps" :recipe="steps" :activeIndex="0" />
                    <GridStepsView v-else-if="steps" :recipe="steps" />
                    <div v-else class="p-8 text-center text-gray-500 dark:text-gray-400">
                        No steps available for this recipe
                    </div>
                </div>

                <!-- Recipe Meta Footer -->
                <footer v-if="!isLoadingMeta"
                    class="mt-10 sticky bottom-0 z-10 backdrop-blur-md border-t border-gray-200 dark:border-gray-700 rounded-t-xl  px-0 md:px-6 py-1 md:py-4 shadow-lg"
                    :style="{ borderTop: `4px solid ${recipe?.repiceColor || '#f59e0b'}` }">
                    <div class="flex flex-col md:flex-row justify-between items-center gap-1 md:gap-4">
                        <!-- Actions (Like, Save, Share) -->
                        <div class="flex flex-wrap items-center gap-4">
                            <button @click="toggleLike" class="flex items-center gap-1.5 text-sm font-medium transition"
                                :class="recipeMeta.isLiked
                                    ? 'text-white bg-[color:var(--like-color)] px-3 py-1.5 rounded-full shadow'
                                    : 'text-gray-600 dark:text-gray-300 hover:text-white hover:bg-[color:var(--like-color)] px-3 py-1.5 rounded-full transition'"
                                :style="{
                                    '--like-color': recipe?.repiceColor || '#f97316'
                                }">
                                <i :class="recipeMeta.isLiked ? 'pi pi-heart-fill' : 'pi pi-heart'"></i>
                                <span>{{ recipeMeta.likeCount || 0 }}</span>
                            </button>

                            <button @click="toggleSave" class="flex items-center gap-1.5 text-sm font-medium transition"
                                :class="recipeMeta.isSaved
                                    ? 'text-white bg-[color:var(--save-color)] px-3 py-1.5 rounded-full shadow'
                                    : 'text-gray-600 dark:text-gray-300 hover:text-white hover:bg-[color:var(--save-color)] px-3 py-1.5 rounded-full transition'"
                                :style="{
                                    '--save-color': recipe.repiceColor || '#f97316'
                                }">
                                <i :class="recipeMeta.isSaved ? 'pi pi-bookmark-fill' : 'pi pi-bookmark'"></i>
                                <span>{{ recipeMeta.isSaved ? 'Saved' : 'Save' }}</span>
                            </button>

                            <div class="card flex justify-center">
                                <Button type="button" icon="pi pi-share-alt" severity="success" label="Share"
                                    @click="share" variant="outlined" size="small" rounded />

                                <Popover ref="op">
                                    <div class="flex flex-col gap-4 w-[25rem]">
                                        <!-- Copy Link Section -->
                                        <div>
                                            <span class="font-medium block mb-2">Share this recipe</span>
                                            <InputGroup>
                                                <InputText :value="recipeUrl" readonly class="w-[25rem]" />
                                                <InputGroupAddon class="cursor-pointer" @click="copyUrl()">
                                                    <i class="pi pi-copy" />
                                                </InputGroupAddon>
                                            </InputGroup>
                                        </div>

                                        <!-- Share Buttons -->
                                        <div>
                                            <span class="font-medium block mb-2">Share on</span>
                                            <ul class="list-none p-0 m-0 flex flex-col gap-3">
                                                <li v-for="site in shares" :key="site.name"
                                                    class="flex items-center gap-3 hover:bg-gray-100 dark:hover:bg-gray-800 rounded px-2 py-1 cursor-pointer"
                                                    @click="shareOnSocial(site.name.toLowerCase())">
                                                    <i :class="site.icon" :style="{ color: site.color }"
                                                        class="text-xl w-6 text-center" />
                                                    <span class="font-medium text-sm">{{ site.name }}</span>
                                                </li>
                                            </ul>
                                        </div>
                                    </div>
                                </Popover>
                            </div>

                        </div>

                        <!-- Extra Info -->
                        <div class="flex flex-col">
                            <p class="text-[12px]">{{ recipe?.recipeName }}</p>
                            <div class="flex items-center gap-3 text-xs text-gray-500 dark:text-gray-400">
                                <span><i class="pi pi-eye"></i> {{ recipeMeta.views || 0 }} views</span>
                                <span><i class="pi pi-comment"></i> {{ recipeMeta.comments || 0 }} comments</span>
                                <span><i class="pi pi-calendar"></i> {{ formatDate(recipe.updatedAt) }}</span>
                            </div>
                        </div>

                    </div>
                </footer>

                <div v-if="!isLoadingComments">
                    comments
                    <div>
                        <ChatsPage />
                    </div>
                </div>

            </template>

            <!-- Empty State -->
            <div v-else class="text-center py-20">
                <div class="max-w-md mx-auto">
                    <i class="pi pi-book text-5xl text-gray-300 dark:text-gray-600 mb-4"></i>
                    <h3 class="text-xl font-medium text-gray-700 dark:text-gray-300 mb-2">Recipe Not Found</h3>
                    <p class="text-gray-500 dark:text-gray-400 mb-6">We couldn't find the recipe you're looking for.</p>
                    <button class="px-4 py-2 bg-amber-500 hover:bg-amber-600 text-white rounded-full transition">
                        Browse Other Recipes
                    </button>
                </div>
            </div>
            <div v-if="isLoadingMeta">
                <div class="w-full h-[50px] bg-gray-400/30 animate-pulse">loading meta...</div>
            </div>

            <div v-if="isLoadingComments">
                <div class="w-full h-[50px] bg-gray-400/30 animate-pulse">loading meta...</div>
            </div>

        </div>
        <Toast position="bottom-center" group="bc" />

    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useAuthStore } from '../store/user.js'
import { useToast } from 'primevue/usetoast'
import FlowGalleryViewer from '../cards/FlowGalleryViewer.vue'
import GridStepsView from '../cards/GridStepsView.vue'
import { fetchRecipeMeta, fetchRecipeSteps } from '../apis/recipes.js'
import ChatsPage from '../cards/ChatsPage.vue'
import { like_unlike, save_unsave_favourites } from '../apis/index.js'
import RecipeStepCard from '../loaders/Skeleton1.vue'

const auth = useAuthStore()


const listType = ref('grid')
const listTypeOptions = [
    { label: 'Step-by-Step', value: 'flow', icon: 'pi pi-list' },
    { label: 'Gallery View', value: 'grid', icon: 'pi pi-th-large' }
]

const isLoading = ref(false)
const isLoadingMeta = ref(false)
const isLoadingComments = ref(false)

const recipe = ref(null)
const steps = ref(null)
const recipeMeta = ref({
    likeCount: 10,
    isSaved: false,
    isLiked: false,
    views: 74,
    comments: 12,
})

const defaultAvatar = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'

const props = defineProps({
    recipe_id: [String, Number],
    recipe_name: String
})

watch(() => props.recipe_id, async (newId, oldId) => {
    if (newId !== oldId) {
        await fetchRecipe()
    }
})

const recipeUrl = computed(() => {
    if (!props.recipe_id || !recipe.value) return '';
    return `${window.location.origin}/recipes/${recipe.value.recipeName}/${recipe.value.id}`;
});


const fetchRecipe = async () => {
    isLoading.value = true;

    try {
        const res = await fetchRecipeSteps(auth.token, props.recipe_name, props.recipe_id);

        if (res?.message && !res.success) {
            toast.add({
                severity: 'error',
                summary: `Failed to load recipe`,
                detail: res.message,
                group: 'bc',
                life: 5000,
            });
        }

        if (res?.data) {
            recipe.value = res.data.cover;
            steps.value = res.data.steps;
        }
    } catch (error) {
        console.error('Unexpected error fetching recipe:', error);
        toast.add({
            severity: 'error',
            summary: 'Unexpected Error',
            detail: 'An unexpected error occurred while fetching recipe details.',
            group: 'bc',
            life: 5000,
        });
    } finally {
        isLoading.value = false;
    }
};

const fetchMeta = async () => {
    isLoadingMeta.value = true;

    try {
        const res = await fetchRecipeMeta(
            '/recipes/meta',
            auth.token,
            { name: props.recipe_name, recipe_id: props.recipe_id },
            recipeMeta.value
        );

        if (res?.message && !res.success) {
            toast.add({
                severity: 'error',
                summary: 'Failed to fetch meta info',
                detail: res.message,
                group: 'bc',
                life: 5000,
            });
        }

        if (res?.data) {
            recipeMeta.value = res.data;
        }
    } catch (error) {
        console.error('Unexpected error fetching meta:', error);
        toast.add({
            severity: 'error',
            summary: 'Unexpected Error',
            detail: 'An unexpected error occurred while fetching metadata.',
            group: 'bc',
            life: 5000,
        });
    } finally {
        isLoadingMeta.value = false;
    }
};


onMounted(async () => {
    await Promise.all([fetchRecipe(), fetchMeta()]);
});

const op = ref();
const shares = ref([
    {
        name: 'WhatsApp',
        icon: 'pi pi-whatsapp',
        color: '#25D366',
        url: `https://wa.me/?text=${encodeURIComponent(recipeUrl.value)}`
    },
    {
        name: 'Facebook',
        icon: 'pi pi-facebook',
        color: '#3b5998',
        url: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(recipeUrl.value)}`
    },
    {
        name: 'Twitter',
        icon: 'pi pi-twitter',
        color: '#1DA1F2',
        url: `https://twitter.com/intent/tweet?url=${encodeURIComponent(recipeUrl.value)}&text=Check this recipe!`
    },
    {
        name: 'Email',
        icon: 'pi pi-envelope',
        color: '#EA4335',
        url: `mailto:?subject=Check this recipe&body=${encodeURIComponent(recipeUrl.value)}`
    }
]);


const share = (event) => {
    op.value.toggle(event);
}

const shareOnSocial = (platform) => {
    if (!recipeUrl.value) return;

    let url = '';
    const text = `Check out my recipe for ${recipe.value.recipeName}`;

    switch (platform) {
        case 'facebook':
            url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(recipeUrl.value)}`;
            break;
        case 'twitter':
            url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(recipeUrl.value)}`;
            break;
        case 'whatsapp':
            url = `https://wa.me/?text=${encodeURIComponent(`${text} ${recipeUrl.value}`)}`;
            break;
    }

    window.open(url, '_blank', 'noopener,noreferrer');
};

const formattedRecipeName = computed(() => {
    return props.recipe_name ? props.recipe_name.replace(/-/g, ' ') : 'Untitled Recipe'
})

const formatTime = (timeObj) => {
    if (!timeObj) return '0m'
    const parts = []
    if (timeObj.hr && timeObj.hr > 0) parts.push(`${timeObj.hr}h`)
    if (timeObj.min && timeObj.min > 0) parts.push(`${timeObj.min}m`)
    return parts.join(' ') || '0m'
}
const copyUrl = () => {
    if (!recipeUrl.value) return;
    navigator.clipboard.writeText(recipeUrl.value);
    toast.add({
        severity: 'success',
        summary: 'Copied!',
        detail: 'Recipe URL copied to clipboard',
        life: 2000
    });
};

const toggleLike = async () => {
    const res = await like_unlike(auth.token, props.recipe_id)
    if (res.success) {
        recipeMeta.value.isLiked = !recipeMeta.value.isLiked
        recipeMeta.value.likeCount += recipeMeta.value.isLiked ? 1 : -1
    } else {
        toast.add({
            severity: 'error',
            summary: 'Failed to like',
            detail: `${res.message} || 'failed!!'`,
            group: 'bc',
            life: 2000
        });
    }
}

const toggleSave = async () => {
    const res = await save_unsave_favourites(auth.token, props.recipe_id);

    if (res.success) {
        const isNowSaved = !recipeMeta.value.isSaved;

        toast.add({
            severity: isNowSaved ? 'success' : 'info',
            summary: isNowSaved ? 'Recipe Saved' : 'Recipe Removed',
            detail: isNowSaved
                ? `You’ve saved “${props.recipe_name}” to your favorites.`
                : `You’ve removed “${props.recipe_name}” from your favorites.`,
            group: 'bc',
            life: 2500,
        });

        recipeMeta.value.isSaved = isNowSaved;
    } else {
        toast.add({
            severity: 'error',
            summary: 'Action Failed',
            detail: res.message || `Something went wrong while updating favorites.`,
            group: 'bc',
            life: 2500,
        });
    }
};


const formatDate = (dateString) => {
    if (!dateString) return 'Unknown date'
    const options = { year: 'numeric', month: 'long', day: 'numeric' }
    return new Date(dateString).toLocaleDateString(undefined, options)
}

const toast = useToast()
const showTemplate = () => {
    toast.add({
        severity: 'warn',
        summary: 'Feature Preview',
        detail: 'This feature is still in development',
        life: 3000
    })
}
</script>

<style>
.animate-fade-in {
    animation: fadeIn 0.5s ease-out;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.shadow-inner {
    box-shadow: inset 0 2px 4px 0 rgb(0 0 0 / 0.05);
}
</style>