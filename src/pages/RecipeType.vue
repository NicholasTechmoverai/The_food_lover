<template>
    <div>
        {{ recipe_type }}
    </div>
    <div>
         <h5>More about {{ recipe_type }}</h5>
        <PileCard />
    </div>

    <div class=" ">
        <h5>{{ recipe_type }} recipes</h5>
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