<template>
    <div>
        <h4 class="m-3">Saved Recipes</h4>
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