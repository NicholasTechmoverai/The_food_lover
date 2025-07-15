<template>
    <div class="py-4">
        <h1 class="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-100 text-center">
            ⟵ Scroll ⟶
        </h1>

        <ul class="flex gap-4 overflow-x-auto pb-4">
            <li v-for="recipe in recipes" :key="recipe.title"
                class="relative min-w-[250px]  overflow-hidden shadow hover:shadow-lg transition duration-300 bg-white dark:bg-gray-800">
                <!-- Recipe Image -->
                <img :src="recipe.image" :alt="recipe.alt" class="w-full h-64 object-cover" />

                <!-- Overlay Content -->
                <div class="absolute inset-0 bg-black/40  text-white flex flex-col justify-end p-3">
                    <div class="flex justify-between items-center text-xs text-white/90">
                        <span class="font-bold text-xl">{{ recipe.title }}</span>
                        <!-- <span><i class="pi pi-heart-fill text-red-400 mr-1"></i>{{ recipe.likes }}</span> -->
                    </div>
                    <div class="flex items-center gap-2 mb-2">
                        <img :src="recipe.chef.avatar" :alt="recipe.chef.name"
                            class="w-8 h-8 rounded-full border-2 border-white" />
                        <div class="text-sm">
                            <p class="font-semibold leading-tight">{{ recipe.chef.name }}</p>
                            <p class="text-xs opacity-80">{{ recipe.views }} views</p>
                        </div>
                    </div>


                </div>
            </li>
        </ul>
    </div>



</template>


<script setup>
const props = defineProps({
    recipes: String,
});

</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap");

*,
*:before,
*:after {
    box-sizing: border-box;
}

*::-webkit-scrollbar,
body::-webkit-scrollbar,
html::-webkit-scrollbar {
    background-color: #1e1f26;
    height: 20px;
    width: 20px;
}

*::-webkit-scrollbar-thumb,
body::-webkit-scrollbar-thumb,
html::-webkit-scrollbar-thumb {
    background: #383d4d;
    border-radius: 99em;
    border: 6px solid #1e1f26;
}


h1 {
    font-size: clamp(20px, 2.5vw, 36px);
    color: rgba(255, 255, 255, 0.8);
    font-weight: 600;
    text-align: center;
}

li img :nth-child(1) {
    display: block;
    width: 100%;
    max-width: 100%;
    margin-bottom: 1.5rem;
}

ul {
    padding: 0;
    margin: 0;
    display: block;
    width: 100%;
    overflow-y: hidden;
    overflow-x: auto;
    white-space: nowrap;
    text-align: center;
    scroll-behavior: smooth;
}

li {
    position: sticky;
    left: 0;
    width: min(50vw, 350px);
    display: inline-block;
    text-align: center;
    background-color: #16171f;
    color: #9b9dad;
    padding-bottom: 1.5rem;
    font-size: clamp(18px, 2.5vw, 22px);
    box-shadow: -10px 0 30px 0 rgba(0, 0, 0, 0.25);
    margin-left: -4px;
}
</style>