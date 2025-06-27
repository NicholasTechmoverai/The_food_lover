<template>
    <div class="min-h-[80%] bg-gray-50 dark:bg-gray-900 p-4 md:p-8">
        <div class="max-w-7xl mx-auto bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden p-6 space-y-6">
            <!-- Header with Preview Button -->
            <div class="flex justify-between items-start border-b border-gray-200 dark:border-gray-700 pb-4">
                <div>
                    <h1 class="text-2xl font-bold text-gray-800 dark:text-white">Create New Recipe</h1>
                    <p class="text-gray-600 dark:text-gray-300">Share your culinary masterpiece with the world</p>
                </div>
                <Button @click="showPreview = !showPreview" :label="showPreview ? 'Hide' : 'Preview'"
                    icon="pi pi-eye"
                    :style="{ backgroundColor: recipeCover.repiceColor, borderColor: recipeCover.repiceColor }"
                    class="hover:opacity-90 transition-opacity" />
            </div>

            <!-- Grid Layout for Landscape Screens -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Left Column -->
                <div class="space-y-6">
                    <!-- Recipe Name Section -->
                    <div class="space-y-2">
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                            Recipe Name
                            <span class="text-gray-500 dark:text-gray-400 text-xs ml-1">
                                {{ recipeCover.recipeName?.length || 0 }}/50
                            </span>
                        </label>
                        <InputText v-model="recipeCover.recipeName" maxlength="50"
                            placeholder="e.g. Spicy Chicken Tacos" class="w-full"
                            :class="{ 'p-invalid': !isRecipeNameValid }" />
                        <small v-if="!isRecipeNameValid" class="p-error block">
                            Please enter a recipe name (max 50 characters)
                        </small>
                    </div>

                    <!-- Cover Image Section -->
                    <div class="space-y-4">
                        <div class="flex items-center justify-between">
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                Cover Image
                            </label>
                            <span class="text-xs text-gray-500 dark:text-gray-400">Recommended: 16:9 aspect ratio</span>
                        </div>

                        <!-- Upload Area -->
                        <div v-if="!recipeCover.image"
                            class="relative border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center hover:border-primary-500 transition-colors cursor-pointer"
                            @click="triggerFileInput" :style="{ borderColor: recipeCover.repiceColor }">
                            <input ref="fileInput" type="file" accept="image/jpeg, image/png, image/webp" class="hidden"
                                @change="handleImageUpload" />
                            <div class="flex flex-col items-center justify-center space-y-2">
                                <i class="pi pi-image text-4xl" :style="{ color: recipeCover.repiceColor }"></i>
                                <p class="text-sm text-gray-600 dark:text-gray-400">
                                    <span class="font-medium" :style="{ color: recipeCover.repiceColor }">Click to
                                        upload</span> or drag and drop
                                </p>
                                <p class="text-xs text-gray-500 dark:text-gray-500">JPG, PNG, or WEBP (max 5MB)</p>
                            </div>
                        </div>

                        <!-- Cover Image Preview -->
                        <div v-if="recipeCover.image" class="relative group">
                            <div class="relative rounded-lg overflow-hidden" :style="{ aspectRatio: '16/9' }">
                                <img :src="recipeCover.image" class="w-full h-full object-cover" />
                                <div
                                    class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-30 transition-all duration-300 flex items-center justify-center gap-2 opacity-0 group-hover:opacity-100">
                                    <Button icon="pi pi-cog" rounded @click="openImageEditor"
                                        class="dark:bg-gray-700" />
                                    <Button icon="pi pi-trash" rounded severity="danger" @click="removeCoverImage"
                                        class="dark:bg-red-600" />
                                </div>
                            </div>
                            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1 text-center">Cover image selected
                            </p>
                        </div>
                    </div>

                    <!-- Theme Color Picker -->
                    <div class="space-y-2">
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                            Recipe Theme Color
                        </label>
                        <ColorPicker v-model="color" format="hex" class="z-10" :style="{ width: '100%' }" />
                    </div>
                </div>

                <!-- Right Column -->
                <div class="space-y-6">
                    <!-- Tags Section -->
                    <div class="space-y-2">
                        <div class="flex justify-between items-center">
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                Tags
                            </label>
                            <span class="text-xs text-gray-500 dark:text-gray-400">
                                {{ recipeCover.tags.length }}/5 tags
                                <span v-if="recipeCover.tags.length >= 5" class="text-red-500 ml-1">(Max reached)</span>
                            </span>
                        </div>

                        <div class="flex flex-wrap gap-2 mb-2">
                            <Chip v-for="(tag, index) in recipeCover.tags" :key="index" :label="`#${tag}`" removable
                                @remove="removeTag(index)" class="dark:bg-gray-700 cursor-pointer"
                                :style="{ backgroundColor: tagBackground(tag) }" />
                        </div>

                        <!-- Tag Search and Selection -->
                        <div class="space-y-2">
                            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                                Search Popular Tags
                            </label>
                            <div class="flex gap-2">
                                <AutoComplete v-model="tagSearch" :suggestions="filteredTags" @complete="searchTags"
                                    @keydown.enter.prevent="addCustomTag" @item-select="addCustomTag"
                                    placeholder="Type and press enter to add tag..." class="flex-1" />
                                <Button icon="pi pi-plus" @click="addCustomTag" :disabled="!tagSearch" />

                            </div>
                        </div>

                        <!-- Popular Tags -->
                        <div class="mb-2">
                            <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Popular tags:</p>
                            <div class="flex flex-wrap gap-2">
                                <Chip v-for="tag in popularTags" :key="tag.value" :label="`#${tag}`" :class="{
                                    'bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200 cursor-not-allowed text-decoration: line-through': isTagSelected(tag),
                                    'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200 cursor-pointer': !isTagSelected(tag)
                                }" @click="toggleTag(tag)" />
                            </div>
                        </div>
                    </div>

                    <!-- Estimated Cook Time -->
                    <div class="space-y-2 flex flex-col justify-center ">
                        <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300">
                            Estimated Total meal preparation Time
                        </label>
                        <div class="flex flex-row items-center gap-4">
                            <div class="flex flex-col items-center">
                                <label class="text-xs text-gray-500 dark:text-gray-400 mb-1">Hours</label>
                                <Knob v-model="recipeCover.cookTime.hr" valueTemplate="{value} hr" :min="0" :max="12"
                                    :step="1" class="w-16 h-16" />
                            </div>
                            <div class="flex flex-col items-center ml-3">
                                <label class="text-xs text-gray-500 dark:text-gray-400 mb-1">Minutes</label>
                                <Knob v-model="recipeCover.cookTime.min" valueTemplate="{value} min" :min="0" :max="55"
                                    :step="5" class="w-16 h-16" />
                            </div>
                        </div>
                        <div class="text-sm text-gray-600 dark:text-gray-300 mt-5">
                            Total: {{ recipeCover.cookTime.hr }} hr {{ recipeCover.cookTime.min }} min
                        </div>
                    </div>
                </div>
            </div>

            <!-- Description Section -->
            <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Description
                    <span class="text-gray-500 dark:text-gray-400 text-xs ml-1">
                        {{ recipeCover.description?.length || 0 }}/200
                    </span>
                </label>
                <Textarea v-model="recipeCover.description" rows="3" maxlength="200"
                    placeholder="Briefly describe your recipe..." class="w-full" />
                <small class="text-xs text-gray-500 dark:text-gray-400">Keep it short and enticing</small>
            </div>

            <!-- Recipe Editor -->
            <div class="space-y-2">
                <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                    Recipe Instructions
                </label>
                <small class="text-xs text-gray-500 dark:text-gray-400 block mb-2">
                    Write cover info about your recipe
                </small>

                <Editor v-model="recipeCover.recipeContent" editorStyle="min-height:200px" placeholder="Example: 
1. Preheat oven to 475°F (245°C)
2. Roll out the pizza dough on a floured surface
3. Spread tomato sauce evenly over the dough
4. Add fresh mozzarella slices
5. Bake for 10-12 minutes until crust is golden
6. Add fresh basil leaves before serving" class="border rounded-lg overflow-hidden dark:border-gray-600" />
            </div>

            <!-- Submit Button -->
            <div class="flex justify-end pt-4 sticky bottom-1">
                <Button label="Next Step" icon="pi pi-arrow-right" @click="submitForm" :disabled="!isFormValid"
                    :style="{ backgroundColor: recipeCover.repiceColor, borderColor: recipeCover.repiceColor }"
                    class="hover:opacity-90 transition-opacity" />
            </div>
        </div>

        <!-- Image Editor Dialog -->
        <Dialog v-model:visible="showImageEditor" header="Edit Cover Image"
            :style="{ width: '90vw', maxWidth: '800px' }" :modal="true" class="dark:bg-gray-800">
            <div class="space-y-4">
                <div class="relative h-[70vh] min-h-[400px] bg-gray-100 dark:bg-gray-700 rounded-lg">
                    <!-- <Cropper ref="cropper" :src="imageToEdit"
                        :stencil-props="{ aspectRatio: 16 / 9, handlers: {}, movable: true, resizable: true }"
                        class="cropper" /> -->
                    <Cropper ref="cropper" :src="imageToEdit" :stencil-props="{ aspectRatio: 16 / 9 }"
                        class="w-full h-full" />


                </div>

                <div class="flex flex-wrap gap-2 justify-center">
                    <Button label="Rotate Left" icon="pi pi-undo" severity="secondary" @click="rotateImage(-90)"
                        class="dark:bg-gray-700" />
                    <Button label="Rotate Right" icon="pi pi-redo" severity="secondary" @click="rotateImage(90)"
                        class="dark:bg-gray-700" />
                    <Button label="Use Original" icon="pi pi-image" severity="secondary" @click="useOriginalImage"
                        class="dark:bg-gray-700" />
                    <Button label="Crop & Save" icon="pi pi-check" @click="saveEditedImage"
                        :style="{ backgroundColor: recipeCover.repiceColor, borderColor: recipeCover.repiceColor }"
                        class="hover:opacity-90 transition-opacity" />
                    <Button label="Cancel" icon="pi pi-times" severity="secondary" @click="showImageEditor = false"
                        class="dark:bg-gray-700" />
                </div>
            </div>
        </Dialog>

        <!-- Preview Dialog -->
        <Dialog v-model:visible="showPreview" header="Recipe Preview" :style="{ width: '90vw', maxWidth: '800px' }"
            :modal="true" class="dark:bg-gray-800">
            <RecipeCard :recipe="recipeCover" />
        </Dialog>
        <Toast />
        <ConfirmDialog></ConfirmDialog>
    </div>
</template>

<script setup>
import { ref, nextTick, computed, watch, onMounted, onBeforeUnmount } from 'vue';
import { Cropper } from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css';
import RecipeCard from '../cards/RecipeCard.vue';
import router from '../router';
import { useOngoingStore } from '../store/ongoing'
import { generateUUID } from '../reusables';
import { useConfirm } from "primevue/useconfirm";
import { useToast } from "primevue/usetoast";

const confirm = useConfirm();
const toast = useToast();


// Store & PrimeVue
const ongoingStore = useOngoingStore()

const showPreview = ref(false);
const showImageEditor = ref(false);
const color = ref('#4CAF50');
const imageToEdit = ref('');
const fileInput = ref(null);
const cropper = ref(null);
const tagInput = ref('');
const tagSearch = ref('');
const selectedTag = ref(null);
const filteredTags = ref([]);

const recipeCover = ref({
    id: null,
    recipeName: '',
    repiceColor: color.value,
    image: null,
    tags: [],
    cookTime: {
        hr: 0,
        min: 0
    },
    description: '',
    recipeContent: ''
});

// On mount, restore unfinished recipe if exists
onMounted(async () => {
  await nextTick() // ensure ConfirmDialog is rendered
  if (ongoingStore.coverRecipe) {
    const nameOrId = ongoingStore.coverRecipe.recipeName || ongoingStore.coverRecipe.id || 'Unnamed'
    continueConfirm(nameOrId)
  }
})



// Before unmount, save the current state to the store
onBeforeUnmount(() => {
    // Auto-generate ID if missing
    if (!recipeCover.value.id) {
        recipeCover.value.id = generateUUID()
    }
    ongoingStore.setCoverRecipe({ ...recipeCover.value })
})

// Confirmation logic
const continueConfirm = (header) => {
    confirm.require({
        message: 'Unfinished recipe has been detected. Continue editing?',
        header: `Recipe: ${header}`,
        icon: 'pi pi-exclamation-triangle',
        rejectProps: {
            label: 'Cancel',
            severity: 'secondary',
            outlined: true,
        },
        acceptProps: {
            label: 'Continue',
        },
        accept: () => {
            recipeCover.value = { ...ongoingStore.coverRecipe }
            toast.add({ severity: 'info', summary: 'Loaded', detail: 'Recipe restored.', life: 3000 })
        },
        reject: () => {
            ongoingStore.clearCoverRecipe()
            toast.add({
                severity: 'warn',
                summary: 'Dismissed',
                detail: 'Unfinished recipe discarded.',
                life: 3000,
            })
        },
    })
}


// Simulated backend tags
const backendTags = ref([
    'vegetarian',
    'vegan',
    'gluten-free',
    'dairy-free',
    'quick',
    'healthy',
    'dessert',
    'dinner',
    'breakfast',
    'low-carb',
    'high-protein',
    'keto',
    'paleo',
    'comfort-food',
    'meal-prep'
]);


const popularTags = computed(() => backendTags.value.slice(0, 12));

const isRecipeNameValid = computed(() =>
    recipeCover.value.recipeName && recipeCover.value.recipeName.length <= 50
);

const isFormValid = computed(() =>
    isRecipeNameValid.value &&
    recipeCover.value.description &&
    recipeCover.value.recipeContent
);

watch(color, (val) => {
    recipeCover.value.repiceColor = val.startsWith('#') ? val : `#${val}`;
});

const tagBackground = (tag) => {
    return isTagSelected(tag) ? `${recipeCover.value.repiceColor}20` : '';
};

const triggerFileInput = () => {
    fileInput.value.click();
};

const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
        alert('Image size should be less than 5MB');
        return;
    }

    // Check file type
    if (!file.type.match('image.(jpeg|png|webp)')) {
        alert('Please upload a JPG, PNG, or WEBP image');
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        imageToEdit.value = e.target.result;
        showImageEditor.value = true;
    };
    reader.readAsDataURL(file);
};

const openImageEditor = () => {
    if (recipeCover.value.image) {
        imageToEdit.value = recipeCover.value.image;
        showImageEditor.value = true;
    }
};

const rotateImage = (degrees) => {
    if (cropper.value) {
        cropper.value.rotate(degrees);
    }
};

const useOriginalImage = () => {
    recipeCover.value.image = imageToEdit.value;
    showImageEditor.value = false;
};

const saveEditedImage = () => {
    if (cropper.value) {
        const { canvas } = cropper.value.getResult();
        if (canvas) {
            recipeCover.value.image = canvas.toDataURL('image/webp', 0.9);
        } else {
            recipeCover.value.image = imageToEdit.value;
        }
        showImageEditor.value = false;
    }
};

const removeCoverImage = () => {
    recipeCover.value.image = null;
};

const searchTags = (event) => {
    const query = event.query?.trim().toLowerCase() || '';
    filteredTags.value = query
        ? backendTags.value.filter(tag => tag.toLowerCase().includes(query))
        : backendTags.value.slice(0, 7); // default suggestions
};


const addCustomTag = () => {
    const tagText = tagSearch.value?.trim().toLowerCase();
    if (!tagText) return;

    // Check if tag already exists
    if (!recipeCover.value.tags.includes(tagText) && recipeCover.value.tags.length < 5) {
        recipeCover.value.tags.push(tagText);

        // Add to backend tags if it's new
        if (!backendTags.value.includes(tagText)) {
            backendTags.value.push(tagText);
        }

        tagSearch.value = '';
        filteredTags.value = [];
    }
};

const isTagSelected = (tag) => {
    return recipeCover.value.tags.includes(tag);
};

const toggleTag = (tag) => {
    if (isTagSelected(tag)) {
        const index = recipeCover.value.tags.indexOf(tag);
        removeTag(index);
    } else if (recipeCover.value.tags.length < 5) {
        recipeCover.value.tags.push(tag);
    }
};


const removeTag = (index) => {
    recipeCover.value.tags.splice(index, 1);
};

const submitForm = () => {
    if (isFormValid.value) {
        if (!recipeCover.value.id) {
            recipeCover.value.id = generateUUID()
        }
        ongoingStore.setCoverRecipe({ ...recipeCover.value })
        console.log('Recipe submitted:', recipeCover.value);
        router.push(`/recipes/new/e/${recipeCover.value.id}`)
    }
};
</script>

<style scoped>
.cropper {
    width: 100%;
    height: 100%;
}

/* Responsive adjustments for landscape screens */
@media (orientation: landscape) {
    .cropper {
        height: 70vh;
    }

    .p-dialog-content {
        max-height: 80vh;
    }

    .grid-cols-1.lg\:grid-cols-2 {
        grid-template-columns: 1fr 1fr;
        gap: 2rem;
    }
}

/* Dark mode transitions */
.dark .p-card {
    transition: background-color 0.3s ease;
}

/* Knob styling */
.p-knob-text {
    font-size: 0.8rem !important;
    fill: var(--text-color) !important;
}

/* Tag chips with theme color */
.p-chip {
    transition: background-color 0.2s ease;
}

/* AutoComplete dropdown */
.p-autocomplete-panel {
    z-index: 1100 !important;
}
</style>