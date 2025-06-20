<template>
    <div class="m-20 ">
        <h1> Receipe id {{ recipe_id }}</h1>
        <h2>{{ receipe_name }}</h2>
        <h3>Page cooking!! tobe served soon!</h3>
        <router-view/>
    </div>
</template>
<script setup>

const props = defineProps({ recipe_id: [String, Number],receipe_name: String})

</script>