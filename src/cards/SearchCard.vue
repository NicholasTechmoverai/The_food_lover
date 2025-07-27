<template>
  <div 
    class="w-full max-w-4xl mx-auto mt-12 p-6 px-3 bg-white dark:bg-gray-900 md:rounded-xl shadow-lg border border-gray-200 dark:border-gray-700 transition-all duration-300"
    :style="{ maxHeight: 'calc(100vh - 50px)' }"
  >
    <!-- Scrollable content wrapper -->
    <div class="overflow-y-auto max-h-[calc(100vh-120px)] space-y-6">
      <!-- Header -->
      <div class="flex flex-col gap-4">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <h2 class="text-2xl font-bold text-gray-800 dark:text-white">
            Discover Recipes, Tips & Chefs
          </h2>
          <ToggleButton 
            v-model="return_unsimilar" 
            onLabel="Hide Unsimilar" 
            offLabel="Show All"
            onIcon="pi pi-filter-slash" 
            offIcon="pi pi-filter" 
            class="w-44 whitespace-nowrap"
            aria-label="Toggle unsimilar results" 
            size="small"
            @change="handleFilterChange"
          />
        </div>

        <!-- Search Input -->
        <div class="relative">
          <IconField class="w-full">
            <InputIcon class="pi pi-search text-gray-500" />
            <InputText 
              v-model="search_val" 
              placeholder="Search recipes, cooking tips, or chefs..." 
              class="w-full border-gray-300 dark:border-gray-600 focus:border-[var(--primary-color)] focus:ring-2 focus:ring-[var(--primary-color)]/20 transition-all rounded-full"
              @input="debouncedLiveSuggestion" 
              size="large"
               style="border-radius: 25px; "
            />
            <InputIcon 
              v-if="search_val_loading" 
              class="pi pi-spin pi-spinner text-gray-500 absolute right-3 top-1/2 transform -translate-y-1/2" 
            />
          </IconField>
        </div>
      </div>

      <!-- Tabs -->
      <div class="border-b border-gray-200 dark:border-gray-700">
        <ul class="flex flex-wrap -mb-px">
          <li 
            v-for="tab in tabs" 
            :key="tab.id"
            class="mr-2"
            @click="activeTab = tab.id"
          >
            <button
              :class="[
                'inline-block p-2 border-b-2 font-medium rounded-t-md',
                activeTab === tab.id 
                  ? 'border-[var(--primary-color)] text-[var(--primary-color)] dark:text-[var(--primary-color)]'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300 dark:text-gray-400 dark:hover:text-white'
              ]"
              @click="handleFilterChange()"
            >
              {{ tab.label }}
              <span 
                class="ml-1 px-2 py-0.5 text-xs rounded-full"
                :class="{
                  'bg-[var(--primary-color)]/10 text-[var(--primary-color)]': activeTab === tab.id,
                  'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300': activeTab !== tab.id
                }"
              >
                {{ tab.count }}
              </span>
            </button>
          </li>
        </ul>
      </div>

    <!-- Suggestions Content -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 overflow-y-auto">
      <!-- Recipes -->
      <div 
        v-show="activeTab === 'all' || activeTab === 'recipes'"
        class="transition-all duration-300"
        :class="{
          'opacity-100': activeTab === 'recipes' || activeTab === 'all',
          'opacity-50 pointer-events-none': activeTab !== 'recipes' && activeTab !== 'all'
        }"
      >
        <h3 class="flex items-center gap-2 text-lg font-semibold mb-4 text-gray-800 dark:text-white">
          <i class="pi pi-book text-[var(--primary-color)]"></i>
          Recipes
        </h3>
        <div 
          v-if="search_val_loading && !recipes_suggestions.length"
          class="space-y-4"
        >
          <div v-for="i in 3" :key="`recipe-loading-${i}`" class="flex gap-3 p-3 rounded-lg bg-gray-100 dark:bg-gray-800 animate-pulse">
            <div class="w-16 h-16 rounded-lg bg-gray-300 dark:bg-gray-700"></div>
            <div class="flex-1 space-y-2">
              <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-3/4"></div>
              <div class="h-3 bg-gray-300 dark:bg-gray-700 rounded w-1/2"></div>
            </div>
          </div>
        </div>
        <div 
          v-else-if="recipes_suggestions.length"
          class="space-y-4 max-h-[500px] overflow-y-auto scrollbar-thin pr-2"
        >
          <div 
            v-for="(recipe, index) in recipes_suggestions" 
            :key="index" 
            @click="router.push(recipe.url)"
            class="flex items-center gap-4 p-3 rounded-lg cursor-pointer transition-all hover:bg-gray-100 dark:hover:bg-gray-800/50 border border-transparent hover:border-gray-200 dark:hover:border-gray-700"
          >
            <img 
              :src="recipe.image" 
              alt="Recipe"
              class="w-16 h-16 rounded-lg object-cover border border-gray-200 dark:border-gray-600 shadow-sm"
              loading="lazy"
            />
            <div class="flex-1 min-w-0">
              <p class="font-medium text-gray-800 dark:text-gray-100 truncate">
                {{ recipe.title }}
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-400 truncate">
                {{ recipe.category || 'General Recipe' }}
              </p>
            </div>
            <i class="pi pi-chevron-right text-gray-400"></i>
          </div>
        </div>
        <div v-else class="text-center py-8">
          <i class="pi pi-search text-3xl text-gray-400 mb-2"></i>
          <p class="text-gray-500 dark:text-gray-400">
            No recipes found matching your search
          </p>
        </div>
      </div>

      <!-- Cooking Tips -->
      <div 
        v-show="activeTab === 'all' || activeTab === 'tips'"
        class="transition-all duration-300"
        :class="{
          'opacity-100': activeTab === 'tips' || activeTab === 'all',
          'opacity-50 pointer-events-none': activeTab !== 'tips' && activeTab !== 'all'
        }"
      >
        <h3 class="flex items-center gap-2 text-lg font-semibold mb-4 text-gray-800 dark:text-white">
          <i class="pi pi-lightbulb text-[var(--primary-color)]"></i>
          Cooking Tips
        </h3>
        <div 
          v-if="search_val_loading && !cooking_tip_suggestions.length"
          class="space-y-4"
        >
          <div v-for="i in 3" :key="`tip-loading-${i}`" class="flex gap-3 p-3 rounded-lg bg-gray-100 dark:bg-gray-800 animate-pulse">
            <div class="w-16 h-16 rounded-full bg-gray-300 dark:bg-gray-700"></div>
            <div class="flex-1 space-y-2">
              <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-3/4"></div>
              <div class="h-3 bg-gray-300 dark:bg-gray-700 rounded w-1/2"></div>
            </div>
          </div>
        </div>
        <div 
          v-else-if="cooking_tip_suggestions.length"
          class="space-y-4 max-h-[500px] overflow-y-auto scrollbar-thin pr-2"
        >
          <div 
            v-for="(tip, index) in cooking_tip_suggestions" 
            :key="index"
            @click="router.push(`/cooking-tips/${tip.category}`)"
            class="flex items-center gap-4 p-3 rounded-lg cursor-pointer transition-all hover:bg-gray-100 dark:hover:bg-gray-800/50 border border-transparent hover:border-gray-200 dark:hover:border-gray-700"
          >
            <img 
              :src="tip.image" 
              :alt="tip.title"
              class="w-16 h-16 object-cover border border-gray-200 dark:border-gray-600 shadow-sm"
              loading="lazy"
              @error="(e) => e.target.src = default_image"
            />
            <div class="flex-1 min-w-0">
              <p class="font-medium text-gray-800 dark:text-gray-100 truncate">
                {{ tip.title || 'Cooking Tip' }}
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                {{ tip.category }}
              </p>
            </div>
            <i class="pi pi-chevron-right text-gray-400"></i>
          </div>
        </div>
        <div v-else class="text-center py-8">
          <i class="pi pi-search text-3xl text-gray-400 mb-2"></i>
          <p class="text-gray-500 dark:text-gray-400">
            No cooking tips found
          </p>
        </div>
      </div>

      <!-- Chefs -->
      <div 
        v-show="activeTab === 'all' || activeTab === 'chefs'"
        class="transition-all duration-300"
        :class="{
          'opacity-100': activeTab === 'chefs' || activeTab === 'all',
          'opacity-50 pointer-events-none': activeTab !== 'chefs' && activeTab !== 'all'
        }"
      >
        <h3 class="flex items-center gap-2 text-lg font-semibold mb-4 text-gray-800 dark:text-white">
          <i class="pi pi-users text-[var(--primary-color)]"></i>
          Chefs
        </h3>
        <div 
          v-if="search_val_loading && !chef_suggestions.length"
          class="space-y-4"
        >
          <div v-for="i in 3" :key="`chef-loading-${i}`" class="flex gap-3 p-3 rounded-lg bg-gray-100 dark:bg-gray-800 animate-pulse">
            <div class="w-16 h-16 rounded-full bg-gray-300 dark:bg-gray-700"></div>
            <div class="flex-1 space-y-2">
              <div class="h-4 bg-gray-300 dark:bg-gray-700 rounded w-3/4"></div>
              <div class="h-3 bg-gray-300 dark:bg-gray-700 rounded w-1/2"></div>
            </div>
          </div>
        </div>
        <div 
          v-else-if="chef_suggestions.length"
          class="space-y-4 max-h-[500px] overflow-y-auto scrollbar-thin pr-2"
        >
          <div 
            v-for="(chef, index) in chef_suggestions" 
            :key="index"
            @click="router.push(`/${chef.username}`)"
            class="flex items-center gap-4 p-3 rounded-lg cursor-pointer transition-all hover:bg-gray-100 dark:hover:bg-gray-800/50 border border-transparent hover:border-gray-200 dark:hover:border-gray-700"
          >
            <img 
              :src="chef.avatar" 
              :alt="chef.username"
              class="w-16 h-16 rounded-full object-cover border border-gray-200 dark:border-gray-600 shadow-sm"
              loading="lazy"
            />
            <div class="flex-1 min-w-0">
              <p class="font-medium text-gray-800 dark:text-gray-100 truncate">
                {{ chef.name }}
              </p>
              <p class="text-sm text-gray-500 dark:text-gray-400">
                @{{ chef.username }}
              </p>
            </div>
            <i class="pi pi-chevron-right text-gray-400"></i>
          </div>
        </div>
        <div v-else class="text-center py-8">
          <i class="pi pi-search text-3xl text-gray-400 mb-2"></i>
          <p class="text-gray-500 dark:text-gray-400">
            No chefs found
          </p>
        </div>
      </div>
    </div>

    <!-- Empty State (when no search has been made) -->
    <div 
      v-if="!search_val && !search_val_loading"
      class="text-center py-12"
    >
      <div class="mx-auto w-24 h-24 bg-gray-100 dark:bg-gray-800 rounded-full flex items-center justify-center mb-4">
        <i class="pi pi-search text-3xl text-gray-400"></i>
      </div>
      <h3 class="text-xl font-medium text-gray-700 dark:text-gray-300 mb-2">
        What are you looking for?
      </h3>
      <p class="text-gray-500 dark:text-gray-400 max-w-md mx-auto">
        Search for recipes, cooking tips, or chefs to get personalized suggestions.
      </p>
    </div>
  </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { recipesSocket, usersSocket } from '../a_websocket';
import { useAuthStore } from '../store/user';
import debounce from 'lodash/debounce';
import { useRouter } from 'vue-router';

const router = useRouter();
const auth = useAuthStore();

// Reactive state
const return_unsimilar = ref(false);
const search_val = ref('');
const search_val_loading = ref(false);
const recipes_suggestions = ref([]);
const chef_suggestions = ref([]);
const cooking_tip_suggestions = ref([]);
const activeTab = ref('all');
const default_image = "https://images.unsplash.com/photo-1586511925558-a4c6376fe65f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=60"

// Computed properties
const tabs = computed(() => [
  { 
    id: 'all', 
    label: 'All', 
    count: recipes_suggestions.value.length + 
           cooking_tip_suggestions.value.length + 
           chef_suggestions.value.length 
  },
  { 
    id: 'recipes', 
    label: 'Recipes', 
    count: recipes_suggestions.value.length 
  },
  { 
    id: 'tips', 
    label: 'Tips', 
    count: cooking_tip_suggestions.value.length 
  },
  { 
    id: 'chefs', 
    label: 'Chefs', 
    count: chef_suggestions.value.length 
  },
]);

// Watchers
watch(return_unsimilar, () => {
  triggerSuggestions();
});

// Methods
const fetchRecipes = async () => {
  if (!search_val.value) {
    recipes_suggestions.value = [];
    return;
  }

  return new Promise((resolve) => {
    recipesSocket.emit("search_recipes_suggestion", {
      token: auth.token?.token,
      search_val: search_val.value,
      return_unsimilar: return_unsimilar.value
    });

    const handler = (data) => {
      recipes_suggestions.value = data;
      recipesSocket.off("response_search_recipes_suggestion", handler);
      resolve();
    };

    recipesSocket.on("response_search_recipes_suggestion", handler);
  });
};

const fetchCookingTips = async () => {
  if (!search_val.value) {
    cooking_tip_suggestions.value = [];
    return;
  }

  return new Promise((resolve) => {
    recipesSocket.emit("search_cookingTip_suggestion", {
      token: auth.token?.token,
      search_val: search_val.value,
      return_unsimilar: return_unsimilar.value
    });

    const handler = (data) => {
      cooking_tip_suggestions.value = data.tips;
      recipesSocket.off("response_search_cookingTip_suggestion", handler);
      resolve();
    };

    recipesSocket.on("response_search_cookingTip_suggestion", handler);
  });
};

const fetchChefs = async () => {
  if (!search_val.value) {
    chef_suggestions.value = [];
    return;
  }

  return new Promise((resolve) => {
    usersSocket.emit("search_chef_suggestion", {
      token: auth.token?.token,
      search_val: search_val.value,
      return_unsimilar: return_unsimilar.value
    });

    const handler = (data) => {
      chef_suggestions.value = data.chefs;
      usersSocket.off("response_search_chef_suggestion", handler);
      resolve();
    };

    usersSocket.on("response_search_chef_suggestion", handler);
  });
};

const handleFilterChange = () => {
  triggerSuggestions();
};

const triggerSuggestions = async () => {
  if (!search_val.value) {
    search_val_loading.value = false;
    return;
  }

  search_val_loading.value = true;

  try {
    switch (activeTab.value) {
      case 'all':
        await Promise.all([fetchRecipes(), fetchCookingTips(), fetchChefs()]);
        break;
      case 'recipes':
        await fetchRecipes();
        break;
      case 'tips':
        await fetchCookingTips();
        break;
      case 'chefs':
        await fetchChefs();
        break;
    }
  } finally {
    search_val_loading.value = false;
  }
};

const debouncedLiveSuggestion = debounce(triggerSuggestions, 400);
</script>

<style>
.scrollbar-thin::-webkit-scrollbar {
  width: 4px;
  height: 4px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.dark .scrollbar-thin::-webkit-scrollbar-thumb {
  background: #4a5568;
}

.dark .scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background: #718096;
}
</style>