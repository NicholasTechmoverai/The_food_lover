<template>
    <div class="min-h-screen px-4 py-6 md:px-8 shrink-0 flex flex-col">
        <!-- Category Filter Buttons -->
        <div class="flex flex-wrap gap-3 justify-center mt-6">
            <button v-for="tip in categoryTypes" :key="tip.value" @click="changeTipCategory(tip.value)" :class="[
                'px-4 py-2 rounded-full border text-sm capitalize transition',
                normalizedSelectedTip === tip.value
                    ? 'bg-emerald-600 text-white border-emerald-600'
                    : 'bg-white dark:bg-gray-800 text-gray-800 dark:text-white border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700'
            ]">
                {{ tip.label }}
            </button>
        </div>

        <div v-if="popular_cooking_tips_loading" class="flex justify-center items-center h-60 w-full relative">
            <div class="flex justify-center items-center h-60 relative">
                <div class="absolute w-46 h-46 bg-gray-300 dark:bg-gray-700 rounded animate-pulse rotate-3"></div>
                <div class="absolute w-46 h-46 bg-gray-300 dark:bg-gray-700 rounded animate-pulse -rotate-6"></div>
            </div>
            <div>
                <div class="w-[100px] h-5 bg-gray-300  dark:bg-gray-700 animate-pulse ml-29 rounded-2xl mb-2"></div>
                <div class="w-[200px] h-5 bg-gray-300  dark:bg-gray-700 animate-pulse ml-29 rounded"></div>

            </div>

        </div>


        <!-- Tips Grid -->
        <div class="flex flex-col gap-12 my-10">
            <!-- Popular Shuffling Card -->
            <div v-if="!popular_cooking_tips_loading && popular_recipes.length">
                <ShufflingCard :tips="popular_recipes" />
            </div>

            <div class="flex flex-wrap justify-center gap-4 sm:gap-5 md:gap-6 max-w-[1000px] mx-auto">
                <CookingTipCard v-for="tip in cooking_tips" :key="tip.id" :tip="tip"
                    class="w-[300px] border border-gray-200/80 dark:border-gray-700/50 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1" />
            </div>


            <!-- Skeleton Loader -->
            <div v-if="cooking_tips_loading" class="flex flex-wrap justify-center gap-4">
                <div class="w-[300px] h-[400px] bg-gray-300 dark:bg-gray-700 rounded animate-pulse"></div>
                <div class="w-[300px] h-[400px] bg-gray-300 dark:bg-gray-700 rounded animate-pulse"></div>
            </div>

            <!-- Load More Button -->
            <div class="flex justify-center mt-4">
                <button @click="get_cooking_tips(limit, offset + limit)"
                    class="px-6 py-2 bg-emerald-600 text-white rounded-lg hover:bg-emerald-700 transition">
                    Load More
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import ShufflingCard from '../cards/ShufflingCard.vue'
import CookingTipCard from '../cards/CookingTipCard.vue'
import { fetch_cooking_tips } from '../apis'
import { useAuthStore } from '../store/user'

// Define categories with labels and values
const categoryTypes = [
    { label: 'Time Saving', value: 'timesaving' },
    { label: 'Substitutions', value: 'substitutions' },
    { label: 'Flavour Pairing', value: 'flavourpairing' },
    { label: 'Equipment', value: 'equipment' },
    { label: 'Knife Skills', value: 'knifeskills' },
    { label: 'Presentation', value: 'presentation' },
    { label: 'All', value: 'all' }
]

const auth = useAuthStore()
const route = useRoute()
const router = useRouter()

// Normalize tip param from route
const normalizedSelectedTip = computed(() => {
    const raw = route.params.tip || 'all'
    return raw.toLowerCase().replace(/\s+/g, '-')
})

const limit = ref(10)
const offset = ref(0)
const cooking_tips = ref([])
const popular_recipes = ref([])
const cooking_tips_loading = ref(false)
const popular_cooking_tips_loading = ref(false)

// Fetch main cooking tips
const get_cooking_tips = async (f_limit = 10, f_offset = 0) => {
    cooking_tips_loading.value = true

    const res = await fetch_cooking_tips(auth.token, {
        limit: f_limit,
        offset: f_offset,
        category: normalizedSelectedTip.value === 'all' ? undefined : normalizedSelectedTip.value
    })

    if (res.success) {
        cooking_tips.value = f_offset === 0
            ? res.data.tips
            : [...cooking_tips.value, ...res.data.tips]

        offset.value = res.data.offset
        limit.value = res.data.limit
    }

    cooking_tips_loading.value = false
}

// Fetch popular tips
const get_popular_cooking_tips = async () => {
    popular_cooking_tips_loading.value = true

    const res = await fetch_cooking_tips(auth.token, {
        limit: 7,
        offset: 0,
        is_popular: true,
        category: normalizedSelectedTip.value === 'all' ? undefined : normalizedSelectedTip.value
    })

    if (res.success) {
        popular_recipes.value = res.data.tips
    }

    popular_cooking_tips_loading.value = false
}

// Watch route change
watch(
    () => route.params.tip,
    () => {
        cooking_tips.value = []
        offset.value = 0
        get_cooking_tips()
        get_popular_cooking_tips()
    },
    { immediate: true }
)

// Category switch
const changeTipCategory = (tip) => {
    if (tip === normalizedSelectedTip.value) return

    if (tip === 'all') {
        router.push({ name: 'CookingTipsPage' })
    } else {
        router.push({ name: 'CookingTipTarget', params: { tip } })
    }
}

// Initial load (optional if using watch with immediate: true)
onMounted(() => {
    get_cooking_tips()
    get_popular_cooking_tips()
})
</script>
