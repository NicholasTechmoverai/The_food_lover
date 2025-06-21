<template>
  <div class="relative min-h-screen p-4">
    <!-- Main Grid -->
    <div class="grid gap-6 md:grid-cols-2 max-w-6xl mx-auto z-10 relative">
      <!-- Left Skeleton Block -->
      <div class="rounded-lg border p-6 shadow-sm">
        <div class="flex mb-4">
          <Skeleton shape="circle" size="4rem" class="mr-4" />
          <div class="flex flex-col justify-center flex-1">
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

      <!-- Right List Skeletons -->
      <div class="rounded-lg border p-6 shadow-sm">
        <ul class="space-y-4">
          <li v-for="i in 4" :key="i">
            <div class="flex">
              <Skeleton shape="circle" size="4rem" class="mr-4" />
              <div class="flex-1 self-center">
                <Skeleton width="100%" class="mb-2" />
                <Skeleton width="75%" />
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <!-- Toast Message -->
    <div class="flex justify-center mt-6">
      <Toast position="bottom-center" group="bc" @close="onClose">
        <template #message="slotProps">
          <div class="flex flex-col items-start flex-auto">
            <div class="flex items-center gap-2">
              <Avatar
                image="https://avatars.githubusercontent.com/u/184249562?v=4"
                shape="circle"
              />
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

    <!-- Child route content (simulated as overlay) -->
    <router-view
      class="absolute inset-0 z-50 w-full h-full bg-black/20 backdrop-blur-md"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import Skeleton from 'primevue/skeleton'
import Toast from 'primevue/toast'
import Button from 'primevue/button'
import Avatar from 'primevue/avatar'

const props = defineProps({
  recipe_id: [String, Number],
  recipe_name: String
})

const formattedRecipeName = computed(() =>
  props.recipe_name ? props.recipe_name.replace(/-/g, ' ') : ''
)

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

onMounted(() => {
  setTimeout(showTemplate, 2000)
})
</script>
