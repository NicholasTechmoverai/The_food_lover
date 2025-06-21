<template>
  <div class="max-w-2xl mx-auto mt-20 text-center px-4">
    <h1 class="text-3xl font-bold text-amber-700 mb-2">
      🍳 {{ recipe_name.replace(/-/g, ' ') }}
    </h1>
    <p class="text-sm text-gray-500 mb-6">Recipe ID: {{ recipe_id }}</p>

    <div class="bg-yellow-100 p-6 rounded-xl shadow-md border border-yellow-300">
      <h2 class="text-xl font-semibold text-yellow-800 mb-2">Page is cooking... 👨‍🍳</h2>
      <p class="text-gray-700">Hang tight! This recipe page is still being prepared and will be served hot and fresh soon.</p>
    </div>

    <router-view />
  </div>
</template>

<script setup>
const props = defineProps({
  recipe_id: [String, Number],
  recipe_name: String
})
</script>
