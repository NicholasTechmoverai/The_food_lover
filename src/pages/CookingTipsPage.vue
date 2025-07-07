<template>
    <div class="min-h-screen px-4 py-6 md:px-8">

        <div v-if="!isRouterViewActive" class="flex flex-col gap-15 my-10">
            <ShufflingCard  />

            <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6  m-auto">
                <CookingTipCard v-for="i in 4" :key="i"
                    class="rounded-lg shadow-md hover:shadow-lg transition duration-300" />
            </div>
        </div>

        <!-- Router View (Dynamic Pages) -->
        <div v-else class="flex flex-col justify-center items-center mt-10">
            <router-view />
        </div>

    </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import ShufflingCard from '../cards/ShufflingCard.vue'
import CookingTipCard from '../cards/CookingTipCard.vue'

const route = useRoute()


const isRouterViewActive = computed(() =>
    ['CookingTipCard'].includes(route.name)
)
</script>
