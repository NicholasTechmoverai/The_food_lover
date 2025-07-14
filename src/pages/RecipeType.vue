<template>
    <div>
        {{ recipe_type }}
        <h2>Development underway!</h2>
    </div>
    <div>
        <PileCard />
    </div>

    <div class=" ">
        <many-reipes-parent />
    </div>
</template>

<script setup>
import PileCard from "../cards/PileCards.vue"
import ManyReipesParent from '../cards/ManyReipesParent.vue';

const props = defineProps({
    recipe_type: String,
})
</script>