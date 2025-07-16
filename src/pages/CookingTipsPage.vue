<template>
    <div class="min-h-screen px-4 py-6 md:px-8">
        <!-- Loading Skeleton for Popular Tips -->
        <div v-if="popular_cooking_tips_loading" class="relative flex justify-center items-center h-60">
            <div class="absolute w-36 h-36 bg-gray-300 rounded animate-pulse rotate-3"></div>
            <div class="absolute w-36 h-36 bg-gray-300 rounded animate-pulse -rotate-6"></div>
        </div>

        <!-- Main View -->
        <div v-if="!isRouterViewActive" class="flex flex-col gap-12 my-10">
            <!-- Shuffling Card (Popular Tips) -->
            <div v-if="!popular_cooking_tips_loading && popular_recipes.length">
                <ShufflingCard :tips="popular_recipes" />
            </div>


            <!-- Recipe Grid -->
     <div
  class="grid gap-4 sm:gap-5 md:gap-6 justify-center"
  style="grid-template-columns: repeat(auto-fill, minmax(300px, 1fr))"
>
  <CookingTipCard
    v-for="tip in cooking_tips"
    :key="tip.id"
    :tip="tip"
    class="min-w-[300px] border border-gray-200/80 dark:border-gray-700/50 rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-all duration-300 hover:-translate-y-1"
  />
</div>

            <div v-if="cooking_tips_loading"
                class="relative flex gap-2 flex-col md:flex-row  justify-center items-center h-fit">
                <div class=" w-full min-w-[300px] h-[400px] bg-gray-300 rounded animate-pulse "></div>
                <div class="  w-full min-w-[300px] h-[400px] bg-gray-300 rounded animate-pulse "></div>
            </div>

            <button @click="get_cooking_tips(limit, offset + limit)">More</button>
        </div>



        <!-- Router View -->
        <div v-else class="flex flex-col justify-center items-center mt-10 w-full">
            <router-view />
        </div>
    </div>
</template>
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'

import ShufflingCard from '../cards/ShufflingCard.vue'
import CookingTipCard from '../cards/CookingTipCard.vue'
import { fetch_cooking_tips } from '../apis'
import { useAuthStore } from '../store/user'

// State & Utilities
const auth = useAuthStore()
const route = useRoute()

const limit = ref(10)
const offset = ref(0)

const cooking_tips = ref([])
const popular_recipes = ref([])

const cooking_tips_loading = ref(false)
const popular_cooking_tips_loading = ref(false)

const isRouterViewActive = computed(() =>
    route.name === 'tip-details' // Adjust to match dynamic route name
)

// Fetch all tips
const get_cooking_tips = async (f_limit, f_offset) => {
    cooking_tips_loading.value = true
    const res = await fetch_cooking_tips(auth.token, {
        limit: f_limit,
        offset: f_offset
    })

    if (res.success) {
        cooking_tips.value =[ ...res.data.tips]
        offset.value = res.data.offset
        limit.value = res.data.limit
    }

    cooking_tips_loading.value = false
}

// Fetch only popular tips
const get_popular_cooking_tips = async () => {
    popular_cooking_tips_loading.value = true
    const res = await fetch_cooking_tips(auth.token, {
        limit: 7,
        offset: 0,
        is_popular: true
    })

    if (res.success) {
        popular_recipes.value = res.data.tips
    }

    popular_cooking_tips_loading.value = false
}

// On load
onMounted(() => {
    get_cooking_tips(limit.value, offset.value)
    get_popular_cooking_tips()
})
</script>
