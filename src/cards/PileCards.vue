<template>
    <div class="py-4">
        <h1 class="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-100 text-center">
            ⟵ Scroll ⟶
        </h1>

        <ul class="flex gap-4 overflow-x-auto pb-4">
            <li v-for="recipe in recipes" :key="recipe.title"
                class="relative min-w-[250px]  overflow-hidden shadow hover:shadow-lg transition duration-300 bg-white dark:bg-gray-800">
                <!-- Recipe Image -->
                <img @click="router.push(recipe.url)" :src="recipe.image" :alt="recipe.alt"
                    class="w-full h-64 object-cover" />

                <!-- Overlay Content -->
                <div class="absolute inset-0 bg-black/40  text-white flex flex-col justify-end p-3">
                    <div class="flex justify-start items-center text-xs text-white/90">
                        <router-link :to="recipe.url"><span class="underline font-bold text-2xl">{{ recipe.title
                        }}</span></router-link>

                        <span class="ml-2 flex justify-center items-center"><i
                                class="pi pi-heart-fill text-red-400 mr-1"></i>{{ recipe.likes }}</span>
                    </div>
                    <div class="flex items-center gap-2 mb-2">
                        <router-link :to="`/${recipe.chef.name}`"> <img :src="recipe.chef.avatar"
                                :alt="recipe.chef.name"
                                class="w-8 h-8 rounded-full border-2 border-white" /></router-link>
                        <div class="text-sm flex flex-col justify-baseline items-start">
                            <router-link :to="`/${recipe.chef.name}`">
                                <p class="font-semibold leading-tight ">{{ recipe.chef.name }}</p>
                            </router-link>
                            <div class="flex flex-row items-center gap-2">
                                <p class="text-xs opacity-80">{{ recipe.views }} views</p>
                                <p class="text-xs opacity-80"> {{ recipe.difficulty_level }}</p>
                                <p class="text-xs opacity-80"> <span v-if="recipe.cook_time.hr">{{ recipe.cook_time.hr }}hr</span>.<span>{{ recipe.cook_time.min }}min</span></p>
                            </div>

                        </div>
                    </div>


                </div>
            </li>
        </ul>
    </div>



</template>


<script setup>
import router from '../router';

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
    font-weight: 700;
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