<template>
    <div>
        {{ recipe_type }}
        <h2>Development underway!</h2>
    </div>
</template>

<script setup>
const props = defineProps({
    recipe_type: String,
})
</script>