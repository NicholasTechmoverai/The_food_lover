<template>
  <div class="min-h-screen relative bg-gray-50 dark:bg-gray-900 p-4">
    <!-- Header -->
    <div
      class="max-w-6xl mx-auto  sticky -top-2 z-50 rounded-lg shadow-sm mb-6 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm p-4 ">
      <div class="flex justify-between items-center">
        <h1 class="text-3xl font-bold text-gray-800 dark:text-white">Recipe Builder</h1>
        <div class="flex gap-2 sticky top-0" v-if="!isMobile">
          <Button label="Preview" icon="pi pi-eye" severity="secondary" @click="showPreview = true"
            class="dark:bg-gray-700 dark:text-white" />
          <Button label="reset" icon="pi pi-refresh" severity="danger" @click="reset()"
            class="dark:bg-gray-700 dark:text-white" />
          <Button label="Recipe Cover" icon="pi pi-image" @click="router.push('/recipes/new/cover')"
            class="dark:bg-primary-600"
            :style="{ backgroundColor: recipeCover.repiceColor, borderColor: recipeCover.repiceColor }" />
          <Button label="Next" icon="pi pi-save" @click="saveRecipe" class="dark:bg-primary-600"
            :style="{ backgroundColor: recipeCover.repiceColor, borderColor: recipeCover.repiceColor }" />
        </div>
        <div class="card flex justify-center" v-else>
          <SplitButton label="Next" icon="pi pi-save" @click="saveRecipe" class="dark:bg-primary-600"
            :model="morebuttonItems"
            :style="{ backgroundColor: recipeCover.repiceColor, borderColor: recipeCover.repiceColor }" />
        </div>
      </div>
      <p class="text-gray-600 dark:text-gray-300 mt-2">Build your recipe step by step</p>
    </div>

    <div v-if="recipe" class="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Recipe Form -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Basic Information -->
        <Card class="dark:bg-gray-800">
          <template #title>
            <div class="flex items-center gap-2 text-gray-800 dark:text-white">
              <i class="pi pi-info-circle"></i>
              <span>Recipe cover Information</span>
            </div>
          </template>
          <template #content>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Recipe Name</label>
                <InputText v-model="recipe.name" placeholder="e.g. Classic Beef Bourguignon" disabled
                  class="w-full dark:bg-gray-700 dark:border-gray-600" />
              </div>

              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Description</label>
                <Textarea v-model="recipe.description" rows="3" placeholder="Briefly describe your recipe..." disabled
                  class="w-full dark:bg-gray-700 dark:border-gray-600" />
                <!-- <div
                  class="w-full dark:bg-gray-700 dark:border-gray-600 p-3 rounded-md text-sm text-gray-800 dark:text-gray-100 overflow-hidden"
                  :style="{ maxHeight: expanded ? 'none' : '6em' }" v-html="recipe.description"></div>-->

              </div>

            </div>
          </template>
        </Card>

        <!-- Ingredients -->
        <Card class="dark:bg-gray-800">
          <template #title>
            <div class="flex items-center gap-2 text-gray-800 dark:text-white">
              <i class="pi pi-list"></i>
              <span>Ingredients</span>
            </div>
          </template>
          <template #content>
            <div class="space-y-4">
              <div v-for="(ingredient, index) in recipe.ingredients" :key="index"
                class="grid grid-cols-12 gap-2 items-center">
                <div class="col-span-5">
                  <InputText v-model="ingredient.name" placeholder="Ingredient name"
                    class="w-full dark:bg-gray-700 dark:border-gray-600" />
                </div>
                <div class="col-span-3">
                  <InputText v-model="ingredient.amount" placeholder="Amount"
                    class="w-full dark:bg-gray-700 dark:border-gray-600" />
                </div>
                <div class="col-span-3">
                  <InputText v-model="ingredient.unit" placeholder="Unit (g, ml, etc)"
                    class="w-full dark:bg-gray-700 dark:border-gray-600" />
                </div>
                <div class="col-span-1 flex justify-end">
                  <Button icon="pi pi-trash" severity="danger" @click="removeIngredient(index)"
                    class="dark:bg-red-600 h-10" />
                </div>
              </div>
              <Button label="Add Ingredient" icon="pi pi-plus" severity="secondary" @click="addIngredient"
                class="w-full mt-2 dark:bg-gray-700"
                :style="{ backgroundColor: recipeCover.repiceColor, borderColor: recipeCover.repiceColor }" />
            </div>
          </template>
        </Card>

        <!-- Cooking Steps -->
        <Card class="dark:bg-gray-800">
          <template #title>
            <div class="flex items-center gap-2 text-gray-800 dark:text-white">
              <i class="pi pi-images"></i>
              <span>Cooking Steps</span>
            </div>
          </template>
          <template #content>
            <div v-for="(step, index) in recipe.steps" :key="index" class="mb-8">
              <div class="flex items-center justify-between mb-4 p-3 bg-gray-100 dark:bg-gray-700 rounded-lg">
                <h3 class="font-medium text-gray-800 dark:text-white">Step {{ index + 1 }}</h3>
                <input hidden type="number" v-model="step.no" >
                <div class="flex gap-2">
                  <Button icon="pi pi-arrow-up" severity="secondary" @click="moveStepUp(index)" :disabled="index === 0"
                    class="dark:bg-gray-700" />
                  <Button icon="pi pi-arrow-down" severity="secondary" @click="moveStepDown(index)"
                    :disabled="index === recipe.steps.length - 1" class="dark:bg-gray-700" />
                  <Button icon="pi pi-trash" severity="danger" @click="removeStep(index)" class="dark:bg-red-600" />
                </div>
              </div>

              <div class="space-y-4">
                <!-- Cooking Parameters -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <!-- <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Time Required</label>
                    <InputNumber v-model="step.timeRequired" mode="decimal" :min="0" suffix=" minutes"
                      class="w-full dark:bg-gray-700 dark:border-gray-600" />
                  </div> -->
                  <div class="space-y-2 flex flex-col justify-center ">
                    <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300">
                      Time Required
                    </label>
                    <div class="flex flex-row items-center gap-4">
                      <div class="flex flex-col items-center">
                        <label class="text-xs text-gray-500 dark:text-gray-400 mb-1">Hours</label>
                        <Knob v-model="step.timeRequired.hr" valueTemplate="{value} hr" :min="0" :max="12" :step="1"
                          class="w-16 h-16" />
                      </div>
                      <div class="flex flex-col items-center ml-3">
                        <label class="text-xs text-gray-500 dark:text-gray-400 mb-1">Minutes</label>
                        <Knob v-model="step.timeRequired.min" valueTemplate="{value} min" :min="0" :max="55" :step="5"
                          class="w-16 h-16" />
                      </div>
                    </div>
                    <div class="text-sm text-gray-600 dark:text-gray-300 mt-5">
                      Total: {{ step.timeRequired.hr }} hr {{ step.timeRequired.min }} min
                    </div>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Temperature</label>
                    <InputNumber v-model="step.tempRequired" :min="0" :max="300" suffix=" °C"
                      class="w-full dark:bg-gray-700 dark:border-gray-600" />
                    <Slider v-model="step.tempRequired" :min="0" :max="300" />

                  </div>
                </div>

                <!-- Ingredients Used -->
                <div>
                  <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Ingredients
                    Used</label>
                  <MultiSelect v-model="step.ingredientsUsed" :options="recipe.ingredients" optionLabel="name"
                    placeholder="Select ingredients" display="chip"
                    class="w-full dark:bg-gray-700 dark:border-gray-600" />
                </div>

                <!-- Instructions -->
                <div>
                  <div class="flex justify-between items-center mb-1">
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">Instructions</label>
                    <SelectButton v-model="instructionsInput" :options="instructionsInputList" optionLabel="label"
                      optionValue="value" size="small" />
                  </div>
                  <Textarea v-if="instructionsInput === 'text_area'" v-model="step.instructions" rows="5"
                    placeholder="Describe this step in detail..."
                    class="w-full dark:bg-gray-700 dark:border-gray-600" />
                  <Editor v-else v-model="step.instructions" editorStyle="min-height:200px" />
                </div>

                <!-- Media -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Step Image</label>



                    <div v-if="!step.image"
                      class="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-4 text-center cursor-pointer hover:border-primary-500 transition-colors"
                      @click="openImageUpload(index)" @dragover.prevent @dragenter.prevent @drop.prevent="handleDrop">

                      <i class="pi pi-image text-2xl text-gray-400 dark:text-gray-500 mb-2"></i>
                      <p class="text-sm text-gray-600 dark:text-gray-400">Click/drop to upload image</p>
                    </div>
                    <div v-else class="relative group">
                      <img :src="step.image" class="w-full h-40 object-cover rounded-lg" />
                      <div
                        class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 flex items-center justify-center gap-2 opacity-0 group-hover:opacity-100 transition-all">
                        <Button icon="pi pi-crop" rounded @click="openImageEditor(index)" class="dark:bg-gray-700" />
                        <Button icon="pi pi-trash" rounded severity="danger" @click="removeStepImage(index)"
                          class="dark:bg-red-600" />
                      </div>
                    </div>
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Video URL
                      (optional)</label>
                    <InputText v-model="step.videoUrl" placeholder="https://youtube.com/..."
                      class="w-full dark:bg-gray-700 dark:border-gray-600" />
                  </div>
                </div>
              </div>
            </div>

            <Button label="Add New Step" icon="pi pi-plus" severity="secondary" @click="addStep"
              class="w-full mt-2 dark:bg-gray-700"
              :style="{ backgroundColor: recipeCover.repiceColor, borderColor: recipeCover.repiceColor }" />

          </template>
        </Card>
      </div>

      <!-- Sidebar -->
      <div class="space-y-6">
        <!-- Recipe Metadata -->
        <Card class="dark:bg-gray-800">
          <template #title>
            <div class="flex items-center gap-2 text-gray-800 dark:text-white">
              <i class="pi pi-tags"></i>
              <span>Tags</span>
            </div>
          </template>
          <template #content>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Tags</label>
                <div class="flex flex-wrap gap-2 mb-2">
                  <Chip v-for="(tag, index) in recipe.tags" :key="index" :label="tag" removable
                    @remove="removeTag(index)" class="dark:bg-gray-700"
                    :style="{ backgroundColor: recipeCover.repiceColor, borderColor: recipeCover.repiceColor }" />

                </div>
                <div class="flex gap-2">
                  <AutoComplete v-model="newTag" :suggestions="filteredTags" @complete="searchTags"
                    @keydown.enter.prevent="addTag" placeholder="Add tag"
                    class="flex-1 dark:bg-gray-700 dark:border-gray-600" />
                  <Button icon="pi pi-plus" @click="addTag" class="dark:bg-gray-700"
                    :style="{ backgroundColor: recipeCover.repiceColor, borderColor: recipeCover.repiceColor }" />
                </div>
              </div>
            </div>
          </template>
        </Card>

        <!-- Cooking Summary -->
        <Card class="dark:bg-gray-800">
          <template #title>
            <div class="flex items-center gap-2 text-gray-800 dark:text-white">
              <i class="pi pi-clock"></i>
              <span>Cooking Summary</span>
            </div>
          </template>
          <template #content>
            <div class="space-y-2">
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-300">Total Steps:</span>
                <span class="font-medium">{{ recipe.steps.length }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-300">Total Ingredients:</span>
                <span class="font-medium">{{ recipe.ingredients.length }}</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-600 dark:text-gray-300">Estimated Time:</span>
                <span class="font-medium">{{ totalTime }} minutes</span>
              </div>
            </div>
          </template>
        </Card>

        <!-- Display Options -->
        <Card class="dark:bg-gray-800">
          <template #title>
            <div class="flex items-center gap-2 text-gray-800 dark:text-white">
              <i class="pi pi-sliders-h"></i>
              <span>Display Options</span>
            </div>
          </template>
          <template #content>
            <div class="space-y-2">
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">Preview Layout</label>
              <SelectButton v-model="listType" :options="listTypeOptions" optionLabel="label" optionValue="value"
                class="w-full" />
            </div>
          </template>
        </Card>
      </div>
    </div>

    <!-- Image Editor Dialog -->
    <Dialog v-model:visible="showImageEditor" header="Edit Image" :style="{ width: '90vw', maxWidth: '800px' }"
      :modal="true" class="dark:bg-gray-800">
      <div class="space-y-4">
        <div class="relative h-96 bg-gray-100 dark:bg-gray-700 rounded-lg">
          <Cropper ref="cropper" :src="imageToEdit.url" :stencil-props="{ aspectRatio: 4 / 3 }" class="cropper" />
        </div>
        <div class="flex flex-wrap gap-2 justify-center">
          <Button label="Rotate Left" icon="pi pi-undo" severity="secondary" @click="rotateImage(-90)"
            class="dark:bg-gray-700" />
          <Button label="Rotate Right" icon="pi pi-redo" severity="secondary" @click="rotateImage(90)"
            class="dark:bg-gray-700" />
          <Button label="Use Original" icon="pi pi-image" severity="secondary" @click="useOriginalImage"
            class="dark:bg-gray-700" />
          <Button label="Crop & Save" icon="pi pi-check" @click="saveEditedImage" class="dark:bg-primary-600" />
          <Button label="Cancel" icon="pi pi-times" severity="secondary" @click="showImageEditor = false"
            class="dark:bg-gray-700" />

        </div>

      </div>
    </Dialog>

    <!-- Preview Dialog -->
    <Dialog v-model:visible="showPreview" header="Recipe Preview" :style="{
      width: '90vw',
      maxWidth: '1000px',
      maxHeight: '90vh',
      overflow: 'auto'
    }" :modal="true" class="dark:bg-gray-800">
      <FlowGalleryViewer v-if="listType === 'flow'" :recipe="recipe" :activeIndex="0" />
      <GridStepsView v-else-if="listType === 'grid'" :recipe="recipe" />
    </Dialog>

    <Toast />
    <ConfirmDialog></ConfirmDialog>
    <!-- File Upload -->
    <input ref="fileInput" type="file" accept="image/*" class="hidden" multiple @change="handleImageUpload" />
  </div>
</template>
<script setup>
import { ref, computed, watchEffect,watch, nextTick, onMounted, onBeforeUnmount } from 'vue';
import { Cropper } from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css';
import RecipePreview from '../cards/RecipeCard.vue';
import FlowGalleryViewer from './FlowGalleryViewer.vue';
import GridStepsView from './GridStepsView.vue';
import { generateUUID } from '../reusables';
import { useRoute, useRouter } from 'vue-router'
import { useOngoingStore } from '../store/ongoing'
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";
import { useIsMobile } from '../reusables';
import router from '../router';

const confirm = useConfirm();
const toast = useToast();
const route = useRoute()
const routeRecipeId = route.params.id
const isMobile = useIsMobile()

const ongoingStore = useOngoingStore()
const recipeCover = ref([])
const listType = ref('flow');
const instructionsInput = ref('text_area');
const activeIndex = ref(0)
const listTypeOptions = ref([
  { label: 'Step-by-Step Flow', value: 'flow' },
  { label: 'Grid View', value: 'grid' },
]);
const instructionsInputList = ref([
  { label: 'Text', value: 'text_area' },
  { label: 'Editor', value: 'editor' },
]);

const filteredTags = ref([
  'vegetarian', 'vegan', 'gluten-free', 'dairy-free', 'quick', 'healthy', 'dessert',
  'dinner', 'breakfast', 'low-carb', 'high-protein', 'keto', 'paleo', 'comfort-food', 'meal-prep'
]);

const defaultRecipe = {
  id: null,
  name: '',
  description: '',
  category: null,
  ingredients: [{ name: '', amount: '', unit: '' }],
  steps: [{
    no: null,
    timeRequired: { hr: 0, min: 0 },
    tempRequired: 0,
    ingredientsUsed: [],
    instructions: '',
    image: null,
    videoUrl: ''
  }],
  tags: []
};

const recipe = ref(null);

onMounted(() => {
  const cover = ongoingStore.coverRecipe;
  const recipeSteps = ongoingStore.recipeSteps;

  if (!cover) {
    MissingCover('Info');
    return;
  }

  console.log("Recipe steps::", recipeSteps)

  if (recipeSteps && recipeSteps.id === routeRecipeId) {
    recipe.value = JSON.parse(JSON.stringify(recipeSteps));
  } else {
    recipe.value = {
      ...defaultRecipe,
      id: routeRecipeId,
    };
    console.warn('Route ID mismatch or missing recipeSteps in store. Using default.');
  }

  if (cover.id !== routeRecipeId) {
    console.warn('Route ID does not match current coverRecipe. Consider loading from backend.');
    return;
  }

  recipeCover.value = { ...cover };

  if (!recipe.value.name) {
    recipe.value.name = cover.recipeName || '';
  }

  if (!recipe.value.description) {
    recipe.value.description = cover.description || '';
  }

  if (!recipe.value.tags?.length) {
    recipe.value.tags = cover.tags || [];
  }

  if (!cover.recipeName) {
    MissingCover('Recipe Name');
  } else if (!cover.image) {
    MissingCover('Image');
  } else if (!cover.description) {
    MissingCover('Description / Editor Content');
  }
});

const handleDrop = (e) => {
  const files = Array.from(e.dataTransfer.files).filter(file => file.type.startsWith('image/'));
  appendStepsWithImages(files);
};

const defaultStep = () => ({
  no: null,
  instructions: '',
  image: null,
  videoUrl: '',
  tempRequired: 0,
  timeRequired: { hr: 0, min: 0 },
  ingredientsUsed: []
});

const appendStepsWithImages = (files) => {
  if (!files.length) return;

  if (recipe.value.steps.length === 0) {
    const step = defaultStep();
    recipe.value.steps.push(step);
  }

  let imagesLoaded = 0;
  const totalImages = files.length;

  files.forEach((file, index) => {
    const reader = new FileReader();
    reader.onload = (event) => {
      const imageData = event.target.result;

      if (index === 0) {
        recipe.value.steps[recipe.value.steps.length - 1].image = imageData;
      } else {
        const step = defaultStep();
        step.image = imageData;
        recipe.value.steps.push(step);
      }

      imagesLoaded++;
      if (imagesLoaded === totalImages) {
        ongoingStore.setRecipeSteps(JSON.parse(JSON.stringify(recipe.value)))
      }
    };
    reader.readAsDataURL(file);
  });
};

const MissingCover = (msg) => {
  confirm.require({
    message: 'You have an incomplete Recipe Cover page. Would you like to complete it?',
    header: `Missing Cover  ${msg}`,
    icon: 'pi pi-exclamation-triangle',
    rejectLabel: 'Skip',
    rejectProps: { label: 'Skip', severity: 'secondary', outlined: true },
    acceptProps: { label: `Set cover ${msg}`, severity: 'primary' },
    accept: () => { router.push('/recipes/new/cover') },
    reject: () => {
      if (!recipeCover.value.id) recipeCover.value.id = generateUUID();
      if (ongoingStore.coverRecipe) recipeCover.value = { ...ongoingStore.coverRecipe };
    },
  })
}

const morebuttonItems = [
  { label: 'recipe cover', icon: "pi pi-image", command: () => router.push('/recipes/new/cover') },
  { label: 'Preview', icon: "pi pi-eye", command: () => showPreview.value = !showPreview.value },
  { separator: true },
  { label: 'reset', icon: 'pi-refresh', command: () => { reset(); toast.add({ severity: 'warn', summary: 'Reset!', detail: 'Page reset!', life: 3000 }); } }
];

const isFormValid = computed(() => {
  return recipe.value.ingredients?.length > 0 &&
    recipe.value.steps.length > 0 &&
    !recipe.value.steps.some(step => !step.instructions.trim()) &&
    !recipe.value.ingredients.some(ing => !ing.name.trim());
});

const fileInput = ref(null);
const cropper = ref(null);
const showImageEditor = ref(false);
const imageToEdit = ref({ index: null, url: '' });

const openImageUpload = (index) => {
  imageToEdit.value = { index, url: '' };
  fileInput.value.click();
};

const openImageEditor = (index) => {
  if (!recipe.value.steps[index].image) {
    openImageUpload(index);
    return;
  }
  imageToEdit.value = { index, url: recipe.value.steps[index].image };
  showImageEditor.value = true;
};

const handleImageUpload = (e) => {
  const files = Array.from(e.target.files).filter(file => file.type.startsWith('image/'));
  if (!files.length) return;

  const reader = new FileReader();
  reader.onload = (event) => {
    imageToEdit.value.url = event.target.result;
    showImageEditor.value = true;
  };
  reader.readAsDataURL(files[0]);

  appendStepsWithImages(files);
};

const rotateImage = (degrees) => cropper.value?.rotate(degrees);

const useOriginalImage = () => {
  recipe.value.steps[imageToEdit.value.index].image = imageToEdit.value.url;
  showImageEditor.value = false;
};

const saveEditedImage = () => {
  const canvas = cropper.value.getResult().canvas;
  if (canvas) {
    recipe.value.steps[imageToEdit.value.index].image = canvas.toDataURL();
    showImageEditor.value = false;
  }
};

const removeStepImage = (index) => recipe.value.steps[index].image = null;

const addIngredient = () => recipe.value.ingredients.push({ name: '', amount: '' });

const removeIngredient = (index) => {
  if (recipe.value.ingredients.length > 1) {
    recipe.value.ingredients.splice(index, 1);
    recipe.value.steps.forEach(step => {
      step.ingredientsUsed = step.ingredientsUsed.filter(
        ing => ing !== recipe.value.ingredients[index]
      );
    });
  }
};

const addStep = () => recipe.value.steps.push(defaultStep());

const removeStep = (index) => {
  if (recipe.value.steps.length > 1) recipe.value.steps.splice(index, 1);
};

const moveStepUp = (index) => {
  if (index > 0) {
    const temp = recipe.value.steps[index];
    recipe.value.steps[index] = recipe.value.steps[index - 1];
    recipe.value.steps[index - 1] = temp;
  }
};

const moveStepDown = (index) => {
  if (index < recipe.value.steps.length - 1) {
    const temp = recipe.value.steps[index];
    recipe.value.steps[index] = recipe.value.steps[index + 1];
    recipe.value.steps[index + 1] = temp;
  }
};

const newTag = ref('');

const addTag = () => {
  const tag = newTag.value.trim().toLowerCase();
  if (tag && !recipe.value.tags.includes(tag)) {
    recipe.value.tags.push(tag);
    newTag.value = '';
  }
};

const removeTag = (index) => recipe.value.tags.splice(index, 1);

const showPreview = ref(false);

const reset = () => {
  Object.assign(recipe.value, JSON.parse(JSON.stringify(defaultRecipe)));
  ongoingStore.clearRecipeSteps();
};

const saveRecipe = () => {
  console.log('Recipe saved:', recipe.value);
  ongoingStore.setRecipeSteps({ ...recipe.value });
  router.push(`/recipes/new/p/${routeRecipeId}`);
};

onBeforeUnmount(() => {
  ongoingStore.setRecipeSteps({ ...recipe.value });
})

watch(
  () => recipe.value?.steps, // safely access steps
  (newSteps) => {
    if (newSteps) {
      newSteps.forEach((step, i) => {
        step.no = i + 1;
      });
    }
  },
  { deep: true, immediate: true }
);

</script>


<style scoped>
.dark .p-card {
  background-color: #1f2937;
  /* Tailwind's bg-gray-800 */
  transition: background-color 0.3s ease;
}

.dark .p-inputtext {
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.cropper {
  width: 100%;
  height: 100%;
}

.dark ::-webkit-scrollbar {
  width: 8px;
}

.dark ::-webkit-scrollbar-track {
  background: #374151;
}

.dark ::-webkit-scrollbar-thumb {
  background: #4b5563;
  border-radius: 4px;
}

.dark ::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}

.step-card {
  transition: all 0.3s ease;
}

.step-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.p-chip {
  cursor: pointer;
  transition: all 0.2s ease;
}

.p-chip:hover {
  opacity: 0.9;
  transform: scale(1.05);
}
</style>