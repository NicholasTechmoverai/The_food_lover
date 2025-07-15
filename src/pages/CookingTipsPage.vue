<template>
  <div class="min-h-screen px-4 py-6 md:px-8">
    <!-- Normal View -->
    <div v-if="!isRouterViewActive" class="flex flex-col gap-15 my-10">
      <ShufflingCard :tips="popular_recipes" />

      <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6 m-auto">
        <CookingTipCard
          v-for="tip in cooking_tips"
          :key="tip.id"
          :tip="tip"
          class="rounded-lg shadow-md hover:shadow-lg transition duration-300"
        />
      </div>
    </div>

    <!-- Route View -->
    <div v-else class="flex flex-col justify-center items-center mt-10">
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

const auth = useAuthStore()
const route = useRoute()

const limit = ref(10)
const offset = ref(0)

const isRouterViewActive = computed(() =>
  ['tip-details'].includes(route.name) // Adjust with actual dynamic route name
)

const cooking_tips = ref([])
const popular_recipes = ref([])

const get_cooking_tips = async (f_limit, f_offset) => {
  const res = await fetch_cooking_tips(auth.token, {
    limit: f_limit,
    offset: f_offset
  })

  if (res.success) {
    cooking_tips.value = res.data.tips
    offset.value = res.data.offset
    limit.value = res.data.limit
  }
}

const get_popular_cooking_tips = async () => {
  const res = await fetch_cooking_tips(auth.token, {
    limit: 7,
    offset: 0,
    is_popular: true
  })

  if (res.success) {
    popular_recipes.value = res.data.tips
  }
}

onMounted(() => {
  get_cooking_tips(limit.value, offset.value)
  get_popular_cooking_tips()
})
</script>
