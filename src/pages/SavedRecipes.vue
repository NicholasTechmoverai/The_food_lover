<template>
    <div>
        <h4 class="flex items-center gap-2 m-4 text-lg font-bold text-gray-800 dark:text-white">
            <i class="pi pi-bookmark text-xl" :style="{ color: auth.user?.theme || '#f97316' }"></i>
            Saved Recipes
        </h4>
        <div class="p-2">
            <ManyReipesParent :user_id="auth.user ? auth.user.id : null" :saved="true" />
        </div>
    </div>
    <Transition enter-active-class="transition transform duration-300 ease-out"
        enter-from-class="translate-y-10 opacity-0" enter-to-class="translate-y-0 opacity-100"
        leave-active-class="transition transform duration-200 ease-in" leave-from-class="translate-y-0 opacity-100"
        leave-to-class="translate-y-10 opacity-0">

        <div v-if="control.showSearch"
            class="fixed z-100 w-full h-screen inset-0 bg-white/70 dark:bg-gray-900/70 backdrop-blur-sm   md:rounded-lg shadow-2xl !overflow-hidden"
            @click.self="control.setShowSearch(false)">
            <div class="py-6 md:p-6">
                <SearchCard />
            </div>
        </div>
    </Transition>
</template>
<script setup>
import ManyReipesParent from '../cards/ManyReipesParent.vue';
import SearchCard from '../cards/SearchCard.vue';
import { useAuthStore } from '../store/user';
import { useControl } from "../store/control.js";
const control = useControl()
const auth = useAuthStore()
</script>