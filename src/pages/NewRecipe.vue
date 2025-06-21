<template>
    <div>
        <div class="max-w-2xl mx-auto mt-20 text-center px-4">
            <h1 class="text-3xl font-bold text-amber-700 mb-2">
                Add New Recipe
            </h1>

            <div class="rounded border p-6">
                <div class="flex mb-4">
                    <Skeleton shape="circle" size="4rem" class="mr-2" />
                    <div>
                        <Skeleton width="10rem" class="mb-2" />
                        <Skeleton width="5rem" class="mb-2" />
                        <Skeleton height=".5rem" />
                    </div>
                </div>
                <Skeleton width="100%" height="150px" />
                <div class="flex justify-between mt-4">
                    <Skeleton width="4rem" height="2rem" />
                    <Skeleton width="4rem" height="2rem" />
                </div>
            </div>

            <router-view />
        </div>

        <!-- Toast Message Card -->
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

            <Button @click="showTemplate" label="??" />
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import Skeleton from 'primevue/skeleton'
import Toast from 'primevue/toast'
import Button from 'primevue/button'
import Avatar from 'primevue/avatar'
import Skeleton2 from '../loaders/Skeleton2.vue'
import Skeleton3 from '../loaders/Skeleton3.vue';

const props = defineProps({
    recipe_id: [String, Number],
    recipe_name: String
})

const formattedRecipeName = computed(() => {
    return props.recipe_name ? props.recipe_name.replace(/-/g, ' ') : ''
})

const toast = useToast()
const visible = ref(false)

const showTemplate = () => {
    if (!visible.value) {
        toast.add({
            severity: 'error',
            summary: 'Not Fully Developed!',
            group: 'bc'
        })
        visible.value = true
    }
}


const onClose = () => {
    visible.value = false
}

onMounted(()=>{
    setTimeout(() => {
        showTemplate()
    }, 3000);
})
</script>
