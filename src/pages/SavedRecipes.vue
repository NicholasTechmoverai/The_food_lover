<template>
    <div>
<h4 class="flex items-center gap-2 m-4 text-lg font-bold text-gray-800 dark:text-white">
  <i class="pi pi-bookmark text-xl"  :style="{ color: auth.user?.theme || '#f97316' }"></i>
  Saved Recipes
</h4>
        <div class="p-2">
            <ManyReipesParent :user_id="auth.user?auth.user.id:null" :saved="true"/>
        </div>
    </div>
</template>
<script setup>
import ManyReipesParent from '../cards/ManyReipesParent.vue';
import { useAuthStore } from '../store/user';
const auth = useAuthStore()
</script>