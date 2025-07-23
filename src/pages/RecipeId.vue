<template>
    <div
        class=" min-h-screen bg-gradient-to-br   from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800 p-0 md:p-4 overflow-auto">
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
                                {{ recipe.user?.totalRecipes || 0 }} recipes • {{ formatTimeAgo(recipe.updatedAt) }}
                            </p>
                        </div>
                        <div v-if="recipe.user?.id !== auth.user?.id">
                            <button v-if="!NowFollowing" @click="follow(recipe.user.id)"
                                class="text-xs px-3 py-1 rounded-full border border-[var(--theme-color)] text-[var(--theme-color)] hover:bg-[var(--theme-color)] hover:text-white transition">
                                <span v-if="recipeMeta?.isFollowing">Following</span><span v-else>Follow</span>
                            </button>
                            <span v-else-if="NowFollowing"
                                class="text-xs px-3 py-1 rounded-full border border-[var(--theme-color)] text-[var(--theme-color)] opacity-70 cursor-not-allowed">
                                <span v-if="recipeMeta?.isFollowing">Unfollowing...</span><span
                                    v-else>Following...</span>
                            </span>
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
                            <button @click="toggleLike"
                                class="flex items-center gap-1.5 text-sm font-medium transition cursor-pointer"
                                :class="recipeMeta.isLiked
                                    ? 'text-white bg-[color:var(--like-color)] px-3 py-1.5 rounded-full shadow'
                                    : 'text-gray-600 dark:text-gray-300 hover:text-white hover:bg-[color:var(--like-color)] px-3 py-1.5 rounded-full transition'" :style="{
                                        '--like-color': recipe?.repiceColor || '#f97316'
                                    }">
                                <i :class="recipeMeta.isLiked ? 'pi pi-heart-fill' : 'pi pi-heart'"></i>
                                <span>{{ recipeMeta.likeCount || 0 }}</span>
                            </button>

                            <button @click="toggleSave"
                                class="flex items-center gap-1.5 text-sm font-medium transition cursor-pointer"
                                :class="recipeMeta.isSaved
                                    ? 'text-white bg-[color:var(--save-color)] px-3 py-1.5 rounded-full shadow'
                                    : 'text-gray-600 dark:text-gray-300 hover:text-white hover:bg-[color:var(--save-color)] px-3 py-1.5 rounded-full transition'" :style="{
                                        '--save-color': recipe.repiceColor || '#f97316'
                                    }">
                                <i :class="recipeMeta.isSaved ? 'pi pi-bookmark-fill' : 'pi pi-bookmark'"></i>
                                <span>{{ recipeMeta.isSaved ? 'Saved' : 'Save' }}</span>
                            </button>

                            <div class="card flex justify-center cursor-pointer">
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
                                <!-- viewers -->
                                <div class="text-center">
                                    <span class="cursor-pointer" @click="toggle_Views">
                                        <i class="pi pi-eye"></i> {{ recipeMeta.views || 0 }} views
                                    </span>

                                    <!-- Viewers Popover -->
                                    <Popover ref="show_viewers">
                                        <div
                                            class="flex flex-col max-h-96 overflow-y-auto p-4 w-72 bg-white dark:bg-gray-900 rounded-lg shadow-lg">
                                            <span class="font-semibold text-lg mb-3">Viewers</span>

                                            <!-- Loading Spinner -->
                                            <ul v-if="loading_views">
                                                <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
                                            </ul>

                                            <!-- Viewers List -->
                                            <ul v-else class="space-y-2">
                                                <li v-for="viewer in Viewers" :key="viewer.id"
                                                    class="flex items-center gap-3 p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer transition">
                                                    <img :src="viewer.avatar" alt="avatar"
                                                        class="w-10 h-10 rounded-full object-cover" />

                                                    <router-link :to="`/${viewer.username}`" class="flex-1">
                                                        <div class="font-medium text-sm text-gray-900 dark:text-white">
                                                            {{ viewer.name }}
                                                        </div>
                                                        <div class="text-xs text-gray-500 dark:text-gray-400">
                                                            @{{ viewer.username }}
                                                        </div>
                                                    </router-link>

                                                    <button v-if="viewer.id !== auth.user.id && viewer.isChef"
                                                        @click.stop="toggleFollow(viewer)"
                                                        class="text-xs px-3 py-1 rounded-full font-semibold transition duration-200"
                                                        :class="viewer.isFollowing ? 'bg-red-100 text-red-600 hover:bg-red-200' : 'bg-blue-100 text-blue-600 hover:bg-blue-200'">
                                                        {{ viewer.isFollowing ? 'Unfollow' : 'Follow' }}
                                                    </button>
                                                </li>
                                            </ul>

                                            <!-- Pagination -->
                                            <div class="flex justify-between items-center mt-4 gap-4">
                                                <button v-if="Viewers && viewers_offset >= viewers_limit"
                                                    @click="fetch_viewers(viewers_limit, viewers_offset - viewers_limit)"
                                                    class="px-4 py-1 text-sm rounded bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200">
                                                    Prev
                                                </button>

                                                <button v-if="viewers_offset + viewers_limit < recipeMeta.views"
                                                    @click="fetch_viewers(viewers_limit, viewers_offset + viewers_limit)"
                                                    class="px-4 py-1 text-sm rounded bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200">
                                                    Next
                                                </button>
                                            </div>
                                        </div>
                                    </Popover>
                                </div>

                                <span><i class="pi pi-comment"></i> {{ recipeMeta.comments || 0 }} comments</span>
                                <span><i class="pi pi-calendar"></i> {{ formatTimeAgo(recipe.updatedAt) }}</span>
                            </div>
                        </div>

                    </div>
                </footer>

                <div>
                    <h4 class="mx-2 font-semibold text-xl"><i class="pi pi-comments">Comments</i></h4>
                    <div>
                        <ChatsPage :theme="recipe?.repiceColor" :recipe_id="recipe_id"
                            :allow_comments="recipe?.allow_comments" />
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
            <div v-if="isLoadingMeta" class="mt-2 border-t border-gray-300/70">
                <div class="mt-1 p-4 bg-white dark:bg-gray-800 rounded-xl shadow flex space-x-4 animate-pulse w-full">
                    <div class="flex-1 space-y-2">
                        <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-2/3"></div>
                        <div class="h-3 bg-gray-200 dark:bg-gray-600 rounded w-1/2"></div>
                        <div class="h-8 w-20 bg-gray-200 dark:bg-gray-700 rounded-md mt-2"></div>
                    </div>
                    <div class="w-8 h-12 bg-gray-300 dark:bg-gray-700 rounded-w-2/3"></div>

                </div>
                <div class="w-full h-[50px] bg-gray-400/30 animate-pulse p-4 rounded">loading meta...</div>
            </div>



        </div>

        <Toast position="bottom-center" group="bc" />

    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onUnmounted } from 'vue'
import { useAuthStore } from '../store/user.js'
import { useToast } from 'primevue/usetoast'
import FlowGalleryViewer from '../cards/FlowGalleryViewer.vue'
import GridStepsView from '../cards/GridStepsView.vue'
import { fetchRecipeMeta, fetchRecipeSteps } from '../apis/recipes.js'
import ChatsPage from '../cards/ChatsPage.vue'
import { folow_unfollow, like_unlike, save_unsave_favourites } from '../apis/index.js'
import RecipeStepCard from '../loaders/Skeleton1.vue'
import { recipesSocket, usersSocket } from "../a_websocket/index.js";
import { formatDistanceToNow } from 'date-fns'
import InputChatBar from '../cards/CommentInput.vue'
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
    isFollowing: false,
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
            '/recipe/meta',
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

const NowFollowing = ref(false)
const follow = async (chefId) => {
    NowFollowing.value = true
    const res = await folow_unfollow(auth.token, chefId)

    recipeMeta.value.isFollowing = !recipeMeta.value.isFollowing

    if (!res?.success) {
        toast.add({
            severity: 'error',
            summary: 'Follow Failed',
            detail: res.message || 'Unable to follow the user. Please try again.',
            group: 'bc',
            life: 4000
        })
        return
    }
    toast.add({
        severity: res?.success ? 'info' : 'error',
        summary: res?.success && recipeMeta.value.isFollowing ? 'Followed' : 'Unfollowed',
        detail: res?.success && recipeMeta.value.isFollowing ? `You're now following ${recipe.value.user?.name}` : `You have unfollowed ${recipe.value.user?.name}` || 'Unable to follow the user. Please try again.',
        group: 'bc',
        life: 3000
    })

    NowFollowing.value = false
}

const show_viewers = ref(null)
const viewers_limit = ref(10)
const viewers_offset = ref(0)
const loading_views = ref(false)
const Viewers = ref([])
const likers= ref([])

const fetch_viewers = async (limit = 10, offset = 0) => {
    loading_views.value = true
    const res = await fetchRecipeMeta("/recipes/views",null, {
        recipe_id: props.recipe_id,
        user_id: auth.user?.id,
        limit: limit,
        offset: offset
    })
    if (res.data) {
        Viewers.value = res.data.viewers
        viewers_limit.value = res.data.limit
        viewers_offset.value = res.data.offset
    }
    loading_views.value = false
}


const toggle_Views = (event) => {
    show_viewers.value.toggle(event);

    fetch_viewers(viewers_limit.value, viewers_offset.value)
    //   refs.show_viewers.toggle() // or however your popover is triggered
}
const toggleFollow = async (follow) => {
    try {
        const res = await folow_unfollow(auth.token, follow.id);

        if (!res?.success) {
            toast.add({
                severity: 'error',
                summary: 'Follow Failed',
                detail: res.message || 'Unable to follow the user. Please try again.',
                group: 'bc',
                life: 4000,
            });
            return;
        }

        // Determine the new follow status
        const followerItem = Viewers.value?.find(f => f.id === follow.id);
        const newFollowStatus = followerItem ? !followerItem.isFollowing : true;

        // Update viewers list
        if (followerItem) {
            followerItem.isFollowing = newFollowStatus;
        }

        // Update likers list (if exists)
        const followingItem = likers.value?.find(f => f.id === follow.id);
        if (followingItem) {
            followingItem.isFollowing = newFollowStatus;
        }

        // Notify the user
        toast.add({
            severity: 'info',
            summary: newFollowStatus ? 'Followed' : 'Unfollowed',
            detail: `${newFollowStatus ? "You're now following" : "You have unfollowed"} ${follow.name}`,
            group: 'bc',
            life: 3000,
        });

    } catch (error) {
        console.error('Follow/Unfollow error:', error);
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Something went wrong. Please try again.',
            group: 'bc',
            life: 4000,
        });
    }
};



const formatTimeAgo = date => formatDistanceToNow(new Date(date), { addSuffix: true })


const toast = useToast()


onMounted(async () => {
    await Promise.all([fetchRecipe(), fetchMeta()]);
    update_view();
    IntervalledGetMeta();
});


const update_view = async () => {
    if (auth.token && props.recipe_id) {
        recipesSocket.emit("update_view", {
            token: auth.token.token,
            recipe_id: props.recipe_id,
        });
    }
}


let intervalId;
let metaListener;

const IntervalledGetMeta = () => {
    if (!props.recipe_id) return;

    // Emit every 10 seconds
    intervalId = setInterval(() => {
        recipesSocket.emit("get_meta", {
            token: auth.token.token,
            recipe_id: props.recipe_id,
        });
    }, 10000);

    // Define listener function separately
    metaListener = (data) => {

        if (data) {
            recipeMeta.value = data;
        }
    };

    // Attach only once
    recipesSocket.on("get_meta", metaListener);
};




watch(() => props.recipe_id, (newId) => {
    if (newId) {
        update_view();
    }
});

onUnmounted(() => {
    clearInterval(intervalId);
    if (metaListener) {
        recipesSocket.off("get_meta", metaListener);
    }
});
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