<template>
    <div>
        {{ recipe_type }}
        <h2>Development underway!</h2>
    </div>
    <div><PileCard /></div>
</template>

<script setup>
import PileCard from "../cards/PileCards.vue"
const props = defineProps({
    recipe_type: String,
})
</script>