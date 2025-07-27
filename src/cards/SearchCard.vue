<template>
    <div
        class="w-full md:w-fit md:max-w-[900px] mx-auto mt-12 p-4 bg-white dark:bg-gray-900 md:rounded-xl shadow-md border border-gray-200 dark:border-gray-700">
        <div class="flex flex-col space-y-4">
            <!-- Header with Search Title and Toggle -->
            <div class="flex items-center gap-3 justify-between">
                <h3 class="text-lg font-semibold">Search Recipes / Cooking Tips / Chefs</h3>
                <div class="card flex justify-center">
                    <ToggleButton v-model="return_unsimilar" onLabel="DisableUnsimilar" offLabel="AllowUnsimilar"
                        onIcon="pi pi-filter-slash" offIcon="pi pi-filter" class="w-44 whitespace-nowrap"
                        aria-label="Toggle unsimilar results" size="small" />
                </div>

            </div>

            <!-- Search Field -->
            <div>
                <IconField class="w-full">
                    <InputIcon class="pi pi-search" />
                    <InputText v-model="search_val" placeholder="Search..." class="w-full rounded-2xl" style="border-radius: 25px;"
                        @input="debouncedLiveSuggestion"  size="large"/>
                    <InputIcon v-if="search_val_loading" class="pi pi-spin pi-spinner" />
                </IconField>
            </div>
        </div>


        <!-- Suggestions -->
        <div>
            <h4>Recipes Suggestions</h4>
            <div class="space-y-3 max-h-[400px] overflow-y-auto scrollbar-thin pr-1">
                <div v-for="(recipe, index) in recipes_suggestions" :key="index" @click="router.push(recipe.url)"
                    class="flex items-center gap-4 cursor-pointer hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg p-2 transition">
                    <img :src="recipe.image" alt="Recipe"
                        class="w-16 h-16 rounded-lg object-cover border border-gray-200 dark:border-gray-600" />
                    <div>
                        <p class="font-medium text-gray-800 dark:text-gray-100 text-sm">
                            {{ recipe.title }}
                        </p>
                    </div>
                </div>

                <p v-if="!recipes_suggestions.length && !search_val_loading"
                    class="text-gray-500 dark:text-gray-400 text-sm text-center">
                    No recipes found.
                </p>
            </div>

        </div>

    </div>
</template>

<script setup>
import { ref } from 'vue';
import router from '../router';
import { recipesSocket } from '../a_websocket';
import { useAuthStore } from '../store/user';
import debounce from 'lodash/debounce'; // ✅ Correct

const auth = useAuthStore();
const return_unsimilar = ref(false);
const search_val = ref('');
const search_val_loading = ref(false);
const recipes_suggestions = ref([]);

const fetchRecipes = async () => {
    if (!search_val.value) {
        recipes_suggestions.value = [];
        return;
    }

    search_val_loading.value = true;
    recipesSocket.emit("search_recipes_suggestion", {
        token: auth.token?.token,
        search_val: search_val.value,
        return_unsimilar: return_unsimilar.value
    });

    const handler = (data) => {
        search_val_loading.value = false;

        recipes_suggestions.value = data;
        recipesSocket.off("response_search_recipes_suggestion", handler);
    };

    recipesSocket.on("response_search_recipes_suggestion", handler);
};

const debouncedLiveSuggestion = debounce(fetchRecipes, 400);
</script>
