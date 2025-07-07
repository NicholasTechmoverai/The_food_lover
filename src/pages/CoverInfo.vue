<template>
    <div class="min-h-[80%] relative bg-gray-50 dark:bg-gray-900 p-4 md:p-8">
        <!-- Sticky Header -->
        <div class="sticky -top-4 z-50 rounded-lg shadow-sm mb-6 bg-white/80 dark:bg-gray-800/80 backdrop-blur-sm">
            <div
                class="max-w-7xl mx-auto p-4 md:p-6 flex justify-between items-start border-gray-200 dark:border-gray-700">
                <div>
                    <h1 class="text-2xl font-bold text-gray-800 dark:text-white">Create New Recipe</h1>
                    <p class="text-gray-600 dark:text-gray-300">Share your culinary masterpiece with the world</p>
                </div>

                <!-- Mobile Controls -->
                <div class="card flex justify-center md:hidden">
                    <SplitButton label="Next" icon="pi pi-arrow-right" @click="submitForm" :model="morebuttonItems"
                        v-tooltip="!isFormValid ? 'Add cover photo, recipe name, and description to proceed' : 'Next'"
                        :style="{ backgroundColor: recipeCover.repiceColor, borderColor: recipeCover.repiceColor }" />

                </div>

                <!-- Desktop Controls -->
                <div class="hidden md:flex flex-row gap-2 pt-4">
                    <Button @click="showPreview = !showPreview" severity="secondary"
                        :label="showPreview ? 'Hide' : 'Preview'" icon="pi pi-eye"
                        class="hover:opacity-90 transition-opacity bg-gray-700 text-white dark:bg-gray-700" />
                    <Button label="Next Step" icon="pi pi-arrow-right" @click="submitForm" :disabled="!isFormValid"
                        v-tooltip="!isFormValid ? 'Complete required fields to proceed' : 'Next'"
                        class="hover:opacity-90 transition-opacity"
                        :style="{ backgroundColor: recipeCover.repiceColor, borderColor: recipeCover.repiceColor }" />
                </div>
            </div>
        </div>

        <!-- Main Content -->
        <div class="max-w-7xl mx-auto bg-white dark:bg-gray-800 rounded-xl shadow-md overflow-hidden p-6 space-y-6">
            <!-- Essential Info Section -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Left Column - Most important inputs -->
                <div class="space-y-6">
                    <!-- Recipe Name - Top priority -->
                    <div class="space-y-2">
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                            Recipe Name *
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

                    <!-- Recipe Editor with Toggle -->
                    <div class="space-y-3">
                        <div>
                            <label class="block text-sm font-semibold text-gray-800 dark:text-gray-200">
                                Recipe Description / Instructions *
                            </label>
                            <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                                Provide a short introduction or instructions for your recipe.
                            </p>
                        </div>

                        <!-- Input Type Switcher -->
                        <div class="max-w-xl space-y-2">
                            <div class="flex justify-between items-center">
                                <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Input Type</label>
                                <SelectButton v-model="instructionsInput" :options="instructionsInputList"
                                    optionLabel="label" optionValue="value" class="text-sm" size="small" />
                            </div>

                            <!-- Description Editor -->
                            <div>
                                <Textarea v-if="instructionsInput === 'text_area'" v-model="recipeCover.description"
                                    rows="5" placeholder="Briefly describe your recipe..."
                                    class="w-full rounded-md border-gray-300 dark:bg-gray-800 dark:border-gray-600 dark:text-white focus:ring-2 focus:ring-primary-500" />
                                <Editor v-else v-model="recipeCover.description" editorStyle="min-height:200px"
                                    placeholder="Briefly describe your recipe..."
                                    class="dark:!bg-gray-800 dark:!text-white" />
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Right Column - Visual elements -->
                <div class="space-y-6">
                    <!-- Cover Image - High priority -->
                    <div class="space-y-4">
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                            Cover Image *
                            <span class="text-xs text-gray-500 dark:text-gray-400 ml-2">(Recommended: 16:9 ratio)</span>
                        </label>

                        <!-- Upload Area -->
                        <div v-if="!recipeCover.image"
                            class="relative border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-6 text-center hover:border-primary-500 transition-colors cursor-pointer"
                            @click="triggerFileInput" :style="{ borderColor: recipeCover.repiceColor }">
                            <input ref="fileInput" type="file" accept="image/jpeg, image/png, image/webp" class="hidden"
                                @change="handleImageUpload" />
                            <div class="flex flex-col items-center justify-center space-y-2">
                                <i class="pi pi-image text-4xl" :style="{ color: recipeCover.repiceColor }"></i>
                                <p class="text-sm text-gray-600 dark:text-gray-400">
                                    <span class="font-medium" :style="{ color: recipeCover.repiceColor }">Click to
                                        upload</span>
                                </p>
                                <p class="text-xs text-gray-500 dark:text-gray-500">JPG, PNG, or WEBP (max 5MB)</p>
                            </div>
                        </div>

                        <!-- Image Preview -->
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
                        </div>
                    </div>

                    <!-- Theme Color - Medium priority -->
                    <div class="space-y-2">
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                            Recipe Theme Color
                        </label>
                        <ColorPicker v-model="color" format="hex" class="z-10 w-full" />
                    </div>
                </div>
            </div>

            <!-- Secondary Sections -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
                <!-- Left Column -->
                <div class="space-y-6">
                    <!-- Category Selection -->
                    <div class="space-y-2">
                        <CategorySelectPage v-model="recipeCover.category" />
                        <Chip v-for="(tag, index) in recipeCover.category" :key="index" :label="tag" removable
                            @remove="removeCatogry(index)" class="dark:bg-gray-700"
                            :style="{ backgroundColor: recipeCover.repiceColor, borderColor: recipeCover.repiceColor }" />
                    </div>

                    <!-- Cuisine Selection -->
                    <div class="space-y-4 flex flex-col justify-start">
                        <h3 class="text-sm font-semibold text-gray-700 dark:text-gray-300">Cuisine Type</h3>
                        <CuisineSelector v-model="recipeCover.cuisine" class=" mr-auto" />
                    </div>

                    <!-- Complexity Level -->
                    <div class="space-y-2">
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                            Difficulty Level
                        </label>
                        <SelectButton v-model="recipeCover.complexityLevel" :options="complexityLevels"
                            optionLabel="name" class="w-full" aria-labelledby="multiple" />
                    </div>
                </div>

                <!-- Right Column -->
                <div class="space-y-6">
                    <!-- Cook Time -->
                    <div class="space-y-2 bg-gray-200/10 flex flex-col justify-between p-2 items-center">
                        <label class="block text-sm font-semibold text-gray-700 dark:text-gray-300">
                            Preparation Time
                        </label>
                        <div class="flex flex-row gap-8 items-center justify-between ">
                            <div class="flex-1 flex flex-col items-center">
                                <label class="text-xs text-gray-500 dark:text-gray-400 mb-1">Hours</label>
                                <Knob v-model="recipeCover.cookTime.hr" valueTemplate="{value} hr" :min="0" :max="12"
                                    :step="1" class="w-16 h-16" />
                            </div>
                            <div class="flex-1 flex flex-col items-center">
                                <label class="text-xs text-gray-500 dark:text-gray-400 mb-1">Minutes</label>
                                <Knob v-model="recipeCover.cookTime.min" valueTemplate="{value} min" :min="0" :max="55"
                                    :step="5" class="w-16 h-16" />
                            </div>
                        </div>
                        <div class="text-sm text-center text-gray-600 dark:text-gray-300 mt-2">
                            Total: {{ recipeCover.cookTime.hr }} hr {{ recipeCover.cookTime.min }} min
                        </div>
                    </div>
                </div>
            </div>

            <!-- Tags Section - Lower priority -->
            <div class="space-y-6 mt-6">
                <div class="space-y-2">
                    <div class="flex justify-between items-center">
                        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
                            Tags
                            <span class="text-xs text-gray-500 dark:text-gray-400 ml-1">(Optional)</span>
                        </label>
                        <span class="text-xs text-gray-500 dark:text-gray-400">
                            {{ recipeCover.tags.length }}/5 tags
                        </span>
                    </div>

                    <div class="flex flex-wrap gap-2 mb-2">
                        <Chip v-for="(tag, index) in recipeCover.tags" :key="index" :label="`#${tag}`" removable
                            @remove="removeTag(index)" class="dark:bg-gray-700 cursor-pointer"
                            :style="{ backgroundColor: tagBackground(tag) }" />
                    </div>

                    <div class="space-y-2">
                        <div class="flex gap-2">
                            <AutoComplete v-model="tagSearch" :suggestions="filteredTags" @complete="searchTags"
                                @keydown.enter.prevent="addCustomTag" @item-select="addCustomTag"
                                placeholder="Search tags..." class="flex-1" />
                            <Button icon="pi pi-plus" @click="addCustomTag"
                                :disabled="!tagSearch || recipeCover.tags.length >= 5"
                                :style="{ backgroundColor: recipeCover.repiceColor, borderColor: recipeCover.repiceColor }" />
                        </div>
                    </div>

                    <div>
                        <p class="text-xs text-gray-500 dark:text-gray-400 mb-1">Popular tags:</p>
                        <div class="flex flex-wrap gap-2">
                            <Chip v-for="tag in popularTags" :key="tag.value" :label="`#${tag}`" :class="{
                                'bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200 cursor-not-allowed decoration line-through': isTagSelected(tag),
                                'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-200 cursor-pointer': !isTagSelected(tag)
                            }" @click="toggleTag(tag)" />
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Image Editor Dialog -->
        <Dialog v-model:visible="showImageEditor" header="Edit Cover Image"
            :style="{ width: '90vw', maxWidth: '800px' }" :modal="true" class="dark:bg-gray-800">
            <div class="space-y-4">
                <div class="relative h-[70vh] min-h-[400px] bg-gray-100 dark:bg-gray-700 rounded-lg">
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
import { useIsMobile } from '../reusables';
import CuisineSelector from '../cards/CuisineSelector.vue';
import CategorySelectPage from './CategorySelectPage.vue';
const confirm = useConfirm();
const toast = useToast();
const isMobile = useIsMobile()
const instructionsInput = ref('text_area');

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
    cuisine: { name: 'Kenyan', region: 'East Africa' },
    complexityLevel: { name: 'Easy', value: 'easy' },
    category: []
});

const complexityLevels = ref([
    { name: 'Easy', value: 'easy' },
    { name: 'Medium', value: 'medium' },
    { name: 'Hard', value: 'hard' }
]);
const instructionsInputList = ref([
    { label: 'Text', value: 'text_area' },
    { label: 'Editor', value: 'editor' },
]);

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
    recipeCover.value.image
);

watch(color, (val) => {
    recipeCover.value.repiceColor = val.startsWith('#') ? val : `#${val}`;
});

const tagBackground = (tag) => {
    return isTagSelected(tag) ? `${recipeCover.value.repiceColor}25` : '';
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

const removeCatogry = (index) => {
    recipeCover.value.category.splice(index, 1);
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
const morebuttonItems = [
    {
        label: 'Preview',
        icon: "pi pi-eye",
        command: () => {
            showPreview.value = !showPreview.value
        }
    },
    {
        separator: true
    },
    //     {
    //     label: 'reset',
    //     icon: 'pi-refresh',
    //     command: () => {
    //       reset()
    //       toast.add({ severity: 'warn', summary: 'Reset!', detail: 'Page reset!', life: 3000 });
    //     }
    //   }

];
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
<!-- 
        <div class="card flex justify-center">
            <Toast position="bottom-center" group="bc" @close="onClose">
                <template #message="slotProps">
                    <div class="flex flex-col items-start flex-auto">
                        <div class="flex items-center gap-2">
                            <Avatar image="https://avatars.githubusercontent.com/u/184249562?v=4" shape="circle" />
                            <span class="font-bold">Developer</span>
                        </div>
                        <div class="font-medium text-lg my-4">
                            {{ slotProps.message.summary }}
                        </div>
                    </div>
                </template>
            </Toast>
        </div> -->