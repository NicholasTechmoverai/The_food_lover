<template>
    <div>
        <Galleria :value="recipe.steps" :numVisible="5" :circular="true" :autoPlay="true" :transitionInterval="3000"
            :activeIndex="activeIndex" :showThumbnails="true" :showIndicators="true" @activeIndexChange="onIndexChange">
            <template #item="slotProps">
                <div class="relative">
                    <!-- Main step image or placeholder -->
                    <img v-if="slotProps.item.image" :src="slotProps.item.image" :alt="'Step ' + slotProps.item.no"
                        class="w-full h-96 object-cover rounded-lg" />
                    <div v-else
                        class="w-full h-96 bg-gray-200 dark:bg-gray-700 flex items-center justify-center rounded-lg">
                        <div class="text-gray-500 dark:text-gray-400 text-center p-4">
                            <i class="pi pi-image text-4xl mb-2"></i>
                            <p>No image for this step</p>
                        </div>
                    </div>

                    <!-- Step information overlay -->
                    <div
                        class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-4 text-white">
                        <div class="text-lg font-bold">Step {{ slotProps.item.no }}</div>
                        <div class="text-sm mt-1">{{ slotProps.item.instructions }}</div>
                        <div class="text-xs mt-2" v-if="slotProps.item.timeRequired > 0">
                            <i class="pi pi-clock mr-1"></i> {{ slotProps.item.timeRequired }} minutes
                        </div>
                        <div class="flex flex-wrap gap-1 mt-2" v-if="slotProps.item.ingredientsUsed.length > 0">
                            <span v-for="(ingredient, idx) in slotProps.item.ingredientsUsed" :key="idx"
                                class="text-xs bg-white/20 px-2 py-1 rounded-full">
                                {{ ingredient.name }}
                            </span>
                        </div>
                    </div>
                </div>
            </template>

            <template #thumbnail="slotProps">
                <!-- Thumbnail image or placeholder -->
                <div class="relative w-24 h-16">
                    <img v-if="slotProps.item.image" :src="slotProps.item.image" :alt="'Step ' + slotProps.item.no"
                        class="w-full h-full object-cover rounded-md" />
                    <div v-else
                        class="w-full h-full bg-gray-200 dark:bg-gray-600 flex items-center justify-center rounded-md">
                        <i class="pi pi-image text-gray-500 dark:text-gray-400"></i>
                    </div>
                    <div class="absolute bottom-1 right-1 bg-black/70 text-white text-xs px-1 rounded">
                        {{ slotProps.item.no }}
                    </div>
                </div>
            </template>
        </Galleria>
    </div>

</template>

<script setup>
import Galleria from 'primevue/galleria';
import { watch } from 'vue';

const props = defineProps({
    recipe: Array,
    activeIndex: Number
});

console.log(props.value)

const emit = defineEmits(['update:activeIndex']);

function onIndexChange(val) {
    emit('update:activeIndex', val);
}
</script>

<style scoped>
/**** Add any scoped styles here if needed ****/
</style>
