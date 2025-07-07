<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-800 p-4 md:p-8">
    <!-- Main Container -->
    <div class="max-w-7xl mx-auto space-y-8">
      <!-- Sticky Header with Navigation and Save -->
      <header class="sticky top-0 z-20 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm p-4 rounded-lg shadow-sm mb-6">
        <div class="flex flex-wrap items-center justify-between gap-4">
          <h1 class="text-2xl font-bold text-gray-800 dark:text-white">Publish Your Recipe</h1>

          <div class="flex flex-wrap gap-2">
            <!-- <Button 
              label="Cover" 
              icon="pi pi-image" 
              @click="router.push('/recipes/new/cover')"
              class="!text-sm"
              :style="{ 
                backgroundColor: recipeCover.repiceColor, 
                borderColor: recipeCover.repiceColor,
                color: getContrastColor(recipeCover.repiceColor)
              }" 
              outlined
            />
            <Button 
              label="Steps" 
              icon="pi pi-list" 
              @click="router.push(`/recipes/new/e/${routeRecipeId}`)"
              class="!text-sm"
              :style="{ 
                backgroundColor: recipeCover.repiceColor, 
                borderColor: recipeCover.repiceColor,
                color: getContrastColor(recipeCover.repiceColor)
              }"
              outlined
            /> -->
            <Button :label="isPublishing ? 'Publishing...' : 'Publish Recipe'"
              :icon="isPublishing ? 'pi pi-spin pi-spinner' : 'pi pi-send'" class="!text-sm p-button-success"
              :disabled="isPublishing" @click="onSave" :style="{
                backgroundColor: recipeCover.repiceColor,
                borderColor: recipeCover.repiceColor,
                color: getContrastColor(recipeCover.repiceColor)
              }" />
          </div>
        </div>
      </header>

      <!-- Recipe Settings Card -->
      <div class=" bg-white dark:bg-gray-700 rounded-xl shadow-sm p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Recipe Settings</h2>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <!-- Visibility Toggle -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Recipe Visibility</label>
            <ToggleButton v-model="isPublic" onLabel="Public" offLabel="Private" onIcon="pi pi-globe"
              offIcon="pi pi-lock" class="w-full" />
          </div>

          <!-- Comments Toggle -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Allow Comments</label>
            <ToggleButton v-model="allowComments" onLabel="Enabled" offLabel="Disabled" onIcon="pi pi-comments"
              offIcon="pi pi-comment-slash" class="w-full" />
          </div>

          <!-- Copy Protection -->
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Copy Protection</label>
            <Dropdown v-model="copyProtection" :options="copyProtectionOptions" optionLabel="label"
              placeholder="Select protection level" class="w-full" />
          </div>
        </div>
      </div>

      <!-- Recipe Preview Grid -->
      <div class="relative grid grid-cols-1 xl:grid-cols-2 gap-8">
        <!-- Cover Preview -->
        <section class="sticky top-1 bg-white dark:bg-gray-700 rounded-xl shadow-sm p-6 h-fit xl:sticky xl:top-28">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-semibold text-gray-800 dark:text-white">Recipe Cover</h2>
            <Button label="Edit Cover" icon="pi pi-pencil" @click="router.push('/recipes/new/cover')" text
              size="small" />
          </div>
          <RecipeCard :recipe="recipeCover" />
        </section>

        <!-- Steps Preview -->
        <section class="bg-white dark:bg-gray-700 rounded-xl shadow-sm p-6">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-4 gap-4">
            <h2 class="text-xl font-semibold text-gray-800 dark:text-white">Steps Preview</h2>

            <div class="flex items-center gap-4">
              <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Preview Layout</label>
                <SelectButton v-model="listType" :options="listTypeOptions" optionLabel="label" optionValue="value"
                  class="flex-wrap" />
              </div>

              <Button label="Edit Steps" icon="pi pi-pencil" @click="router.push(`/recipes/new/e/${routeRecipeId}`)"
                text size="small" />
            </div>
          </div>

          <div class="mt-6">
            <FlowGalleryViewer v-if="listType === 'flow'" :recipe="recipe_steps" :activeIndex="0" />
            <GridStepsView v-else-if="listType === 'grid'" :recipe="recipe_steps" />
          </div>
        </section>
      </div>

      <!-- Share Options (Below the grid) -->
      <section class="bg-white dark:bg-gray-700 rounded-xl shadow-sm p-6">
        <h2 class="text-xl font-semibold mb-4 text-gray-800 dark:text-white">Share Options</h2>

        <div class="space-y-4">
          <div class="flex items-center gap-4">
            <InputText v-model="recipeUrl" readonly class="flex-1" placeholder="Generating URL..." />
            <Button icon="pi pi-copy" @click="copyUrl" severity="secondary" :disabled="!recipeUrl"
              v-tooltip="'Copy URL'" />
          </div>

          <div class="flex gap-2 flex-wrap">
            <Button icon="pi pi-facebook" severity="secondary" outlined @click="shareOnSocial('facebook')" />
            <Button icon="pi pi-twitter" severity="secondary" outlined @click="shareOnSocial('twitter')" />
            <Button icon="pi pi-whatsapp" severity="secondary" outlined @click="shareOnSocial('whatsapp')" />
            <Button icon="pi pi-link" severity="secondary" outlined @click="copyUrl" label="Copy Link" />
          </div>
        </div>
      </section>
    </div>
  </div>
  <Toast />
  <ConfirmDialog />
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useConfirm } from 'primevue/useconfirm';
import { useToast } from 'primevue/usetoast';

import FlowGalleryViewer from './FlowGalleryViewer.vue';
import GridStepsView from './GridStepsView.vue';
import RecipeCard from './RecipeCard.vue';
import { useOngoingStore } from '../store/ongoing';
import { useIsMobile } from '../reusables';
import { saveRecipe } from '../apis/recipes';
import { useAuthStore } from '../store/user.js'


const auth = useAuthStore()
const router = useRouter();
const route = useRoute();
const confirm = useConfirm();
const toast = useToast();
const isMobile = useIsMobile();
const isPublishing = ref(false);

const ongoingStore = useOngoingStore();
const recipeCover = ref({
  user: {
    name: '',
    profilePic: '',
    id: '',
    totalRecipes: 0
  },
  id: null,
  recipeName: '',
  repiceColor: '#f97316',
  image: null,
  tags: [],
  cookTime: { hr: 0, min: 0 },
  description: '',
  cuisine: { name: 'Kenyan', region: 'East Africa' },
  complexityLevel: { name: 'Easy', value: 1 },
  category: []
});

const recipe_steps = ref([]);
const routeRecipeId = route.params.id;

const isPublic = ref(true);
const allowComments = ref(true);
const copyProtection = ref('basic');
const copyProtectionOptions = [
  { label: 'Basic (Allow with attribution)', value: 'basic' },
  { label: 'Restricted (No copying)', value: 'restricted' },
  { label: 'Custom (User must request)', value: 'custom' }
];

const listType = ref('flow');
const listTypeOptions = [
  { label: 'Flow View', value: 'flow' },
  { label: 'Grid View', value: 'grid' }
];

const recipeUrl = computed(() => {
  if (!recipeCover.value.id) return '';
  return `${window.location.origin}/recipes/${recipeCover.value.recipeName.replace(/\s+/g, '-').toLowerCase()}/${recipeCover.value.id}`;
});

// const recipeUrl = (name, id) => {
//   return `/recipes/${name.replace(/\s+/g, '-').toLowerCase()}/${id}`;
// };


const getContrastColor = (hexColor) => {
  if (!hexColor) return '#ffffff';
  const r = parseInt(hexColor.substr(1, 2), 16);
  const g = parseInt(hexColor.substr(3, 2), 16);
  const b = parseInt(hexColor.substr(5, 2), 16);
  const brightness = (r * 299 + g * 587 + b * 114) / 1000;
  return brightness > 128 ? '#000000' : '#ffffff';
};

const copyUrl = () => {
  if (!recipeUrl.value) return;
  navigator.clipboard.writeText(recipeUrl.value);
  toast.add({
    severity: 'success',
    summary: 'Copied!',
    detail: 'Recipe URL copied to clipboard',
    life: 2000
  });
};

const shareOnSocial = (platform) => {
  if (!recipeUrl.value) return;

  let url = '';
  const text = `Check out my recipe for ${recipeCover.value.recipeName}`;

  switch (platform) {
    case 'facebook':
      url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(recipeUrl.value)}`;
      break;
    case 'twitter':
      url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(recipeUrl.value)}`;
      break;
    case 'whatsapp':
      url = `https://wa.me/?text=${encodeURIComponent(`${text} ${recipeUrl.value}`)}`;
      break;
  }

  window.open(url, '_blank', 'noopener,noreferrer');
};

const onSave = async () => {
  isPublishing.value = true;

  toast.add({
    severity: 'info',
    summary: 'Publishing...',
    detail: 'Your recipe is being published...',
    life: 2000,
  });

  const token = auth.token;
  const res = await saveRecipe(token, {
    recipeCover: recipeCover.value,
    recipeSteps: recipe_steps.value,
    isPublic:isPublic.value,
    allowComments:allowComments.value,
    copyProtection:copyProtection.value,
  });

  isPublishing.value = false;

  if (!res) return;

  if (res.success) {
    toast.add({
      severity: 'success',
      summary: 'Published!',
      detail: 'Your recipe is now live.',
      life: 3000,
    });

    setTimeout(() => {
      ongoingStore.clearCoverRecipe();
      ongoingStore.clearRecipeSteps();
      router.push('/recipes');
    }, 2500);
  } else {
    toast.add({
      severity: 'error',
      summary: 'Publish Failed!',
      detail: `Failed: ${res.message}`,
      life: 6000,
    });
  }
};

onMounted(() => {
  const cover = ongoingStore.coverRecipe;
  const steps = ongoingStore.recipeSteps;

  if (!cover) {
    MissingCover('Info');
    return;
  }

  if (cover.id !== routeRecipeId) {
    MissingRecipeId(routeRecipeId);
    return;
  }

  if (!cover.recipeName) {
    MissingCover('Recipe Name');
  } else if (!cover.image) {
    MissingCover('Image');
  } else if (!cover.description) {
    MissingCover('Description / Editor Content');
  }

  recipeCover.value = { ...cover };
  recipe_steps.value = steps || [];
});

function MissingCover(msg) {
  confirm.require({
    message: 'You have an incomplete Recipe Cover page. Would you like to complete it?',
    header: `Missing Cover: ${msg}`,
    icon: 'pi pi-exclamation-triangle',
    rejectLabel: 'Skip',
    rejectProps: { label: 'Skip', severity: 'secondary', outlined: true },
    acceptProps: { label: `Set Cover`, severity: 'primary' },
    accept: () => router.push('/recipes/new/cover'),
    reject: () => {
      if (ongoingStore.coverRecipe) {
        recipeCover.value = { ...ongoingStore.coverRecipe };
      }
    }
  });
}

function MissingRecipeId(id) {
  confirm.require({
    message: `No recipe found with ID: ${id}.`,
    header: 'Recipe Not Found',
    icon: 'pi pi-info-circle',
    acceptLabel: 'Go Back',
    rejectLabel: 'Stay',
    accept: () => router.back()
  });
}
</script>


<style scoped>
/* Responsive adjustments */
@media (min-width: 1280px) {
  .recipe-grid {
    grid-template-columns: minmax(0, 1fr) minmax(0, 1.5fr);
    gap: 2rem;
  }

  .sticky-cover {
    position: sticky;
    top: 7rem;
    /* Adjust based on your header height */
    align-self: start;
  }
}

/* Smooth transitions for layout changes */
.recipe-grid {
  transition: grid-template-columns 0.3s ease;
}
</style>