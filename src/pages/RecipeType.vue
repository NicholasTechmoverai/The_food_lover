<template>
    <section class="space-y-10 md:space-y-12 px-4 sm:px-6 lg:px-8">
        <!-- Header with loading state -->
        <header>
            <div class="flex items-center gap-4">
                <h2 class="text-2xl font-bold capitalize text-gray-800 dark:text-white">
                    {{ recipe_type || '...' }}
                </h2>
                <Skeleton v-if="loadingHeader" width="8rem" height="2rem" />
            </div>
        </header>

        <!-- About Section -->
        <section>
            <h3 class="text-xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
                More about {{ recipe_type }}
            </h3>

            <div v-if="loadingSuggestions" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                <Card v-for="n in 3" :key="n">
                    <template #content>
                        <div class="space-y-3">
                            <Skeleton width="100%" height="150px" />
                            <Skeleton width="80%" />
                            <div class="flex items-center gap-2">
                                <Skeleton shape="circle" size="2rem" />
                                <Skeleton width="60%" height="1rem" />
                            </div>
                            <div class="flex gap-4">
                                <Skeleton width="4rem" height="1rem" />
                                <Skeleton width="4rem" height="1rem" />
                            </div>
                        </div>
                    </template>
                </Card>
            </div>
            <PileCard v-else :recipes="recipes" />
        </section>

        <!-- Recipes List Section -->
        <section>
            <h3 class="text-xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
                {{ recipe_type }} recipes
            </h3>
            <div v-if="loadingMain" class="space-y-6">
                loading...
            </div>
            <ManyRecipesParent v-else :recipe_name="recipe_type" :category="[recipe_type]" :tags="[recipe_type]"
                @loading="handleChildLoading" />
        </section>
    </section>
</template>

<script setup>
import PileCard from "../cards/PileCards.vue"
import ManyRecipesParent from "../cards/ManyReipesParent.vue"
import { ref, watch, onMounted } from "vue";
import { useAuthStore } from "../store/user";
import { make_a_post } from "../apis";
import { useToast } from 'primevue/usetoast'
import { useRoute } from 'vue-router'

const toast = useToast()
const auth = useAuthStore()
const route = useRoute()

const props = defineProps({
    recipe_type: {
        type: String,
        default: () => null
    }
});

const loadingHeader = ref(true)
const loadingSuggestions = ref(false)
const loadingMain = ref(false)
const childLoading = ref(false)

const recipes = ref([])

// Watch for route changes to refetch data
watch(() => props.recipe_type, (newVal, oldVal) => {
    if (newVal && newVal !== oldVal) {
        fetchAllData()
    }
})

// Watch for child loading state
const handleChildLoading = (isLoading) => {
    childLoading.value = isLoading
}

const fetchAllData = async () => {
    loadingHeader.value = true
    loadingMain.value = true
    await Promise.all([
        fetch_recipe_suggestions(),
        setTimeout(() => {
            loadingMain.value = false
        }, 50)])

    loadingHeader.value = false
}

const fetch_recipe_suggestions = async () => {
    loadingSuggestions.value = true
    try {
        const res = await make_a_post(
            `/recipes/${props.recipe_type}/suggestions`,
            auth.token,
            {},
            { timeout: 10000 } // 10 second timeout
        )

        if (res.data) {
            recipes.value = res.data.map(recipe => ({
                ...recipe,
                // Ensure default values
                views: recipe.views || 0,
                likes: recipe.likes || 0,
                chef: recipe.chef || {
                    id: 0,
                    name: 'Unknown Chef',
                    avatar: '',
                    theme: ''
                }
            }))
        }
    } catch (error) {
        console.error('Error fetching recipe suggestions:', error)
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Failed to load recipe suggestions',
            life: 3000
        })
        // Fallback to default recipes if API fails
        recipes.value = [{
            title: `${props.recipe_type} Recipe`,
            image: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c',
            alt: `Delicious ${props.recipe_type}`,
            views: 1000,
            likes: 150,
            chef: {
                id: 1,
                name: 'Chef Special',
                avatar: 'https://i.pravatar.cc/40?img=3',
                theme: ""
            }
        }]
    } finally {
        loadingSuggestions.value = false
    }
}

// Initial load
onMounted(() => {
    fetchAllData()
})
</script>

<style scoped>
/* Smooth transitions for loading states */
.skeleton-enter-active,
.skeleton-leave-active {
    transition: opacity 0.3s ease;
}

.skeleton-enter-from,
.skeleton-leave-to {
    opacity: 0;
}

/* Pulse animation for loading elements */
@keyframes pulse {

    0%,
    100% {
        opacity: 1;
    }

    50% {
        opacity: 0.5;
    }
}

.pulse {
    animation: pulse 1.5s ease-in-out infinite;
}
</style>