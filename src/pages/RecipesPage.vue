<template>
  <div class="max-w-2xl mx-auto mt-20 text-center px-4">
    <h1 class="text-3xl font-bold text-purple-700 mb-2">
      <i class="pi pi-book mr-2 text-purple-600"></i>
      All Recipes
    </h1>

    <div class="bg-purple-50 p-6 rounded-xl shadow-md border border-purple-200 mt-4">
      <h2 class="text-xl font-semibold text-purple-800 mb-2">
        Page is cooking... 🍽️
      </h2>
      <p class="text-gray-700">
        A full menu of delicious recipes will be served here very soon. Stay tuned!
      </p>
    </div>

    <router-view />
  </div>
</template>

<script setup>
// No props needed here
</script>
