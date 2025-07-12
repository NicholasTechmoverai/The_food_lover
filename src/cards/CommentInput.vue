<template>
  <div class="flex gap-3">
    <!-- User Avatar -->
    <div class="flex-shrink-0">
      <Avatar :image="currentUser.profilePic" shape="circle" class="w-8 h-8" />
    </div>

    <!-- Input Area -->
    <div class="flex-1 relative">
      <!-- Main Textarea -->
      <Textarea 
        ref="commentTextarea"
        :modelValue="modelValue"
        @update:modelValue="$emit('update:modelValue', $event)"
        :placeholder="placeholderText" 
        rows="2"
        class="w-full px-3 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md focus:ring-1 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"
        autoResize 
      />

      <!-- Mention Preview -->
      <div v-if="replyingTo" class="mt-1 inline-flex items-center px-2 py-0.5 bg-blue-50 dark:bg-blue-900/30 rounded-full text-xs">
        <span class="font-medium text-blue-600 dark:text-blue-300">@{{ replyingTo }}</span>
        <span class="ml-1 text-gray-500 dark:text-gray-400">will be notified</span>
      </div>

      <!-- Emoji Picker -->
      <div v-if="showEmojiPicker" class="absolute bottom-full left-0 mb-1 z-10">
        <Picker :data="emojiData" @select="handleEmojiSelect" :showPreview="false" :showSearch="true"
          title="Pick an emoji" />
      </div>

      <!-- File Previews -->
      <div v-if="attachedFiles.length > 0" class="mt-2 flex flex-wrap gap-1">
        <div v-for="(file, index) in attachedFiles" :key="index"
          class="flex items-center gap-1 px-2 py-1 bg-gray-50 dark:bg-gray-700 rounded-full text-xs">
          <span class="max-w-[100px] truncate text-gray-700 dark:text-gray-300">{{ file.name }}</span>
          <button @click="handleRemoveFile(index)"
            class="text-gray-400 hover:text-red-500 transition-colors">
            <i class="pi pi-times text-xs"></i>
          </button>
        </div>
      </div>

      <!-- Action Bar -->
      <div class="mt-3 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
        <div class="flex items-center gap-1">
          <button @click="toggleEmojiPicker"
            class="p-1.5 text-gray-500 hover:text-blue-500 dark:hover:text-blue-400 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            title="Add emoji">
            <i class="pi pi-smile text-sm"></i>
          </button>
          <button @click="triggerFileInput"
            class="p-1.5 text-gray-500 hover:text-blue-500 dark:hover:text-blue-400 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            title="Attach files">
            <i class="pi pi-paperclip text-sm"></i>
          </button>
          <input type="file" ref="fileInput" class="hidden" @change="handleFileChange"
            accept="image/*,.pdf,.doc,.docx" multiple />

          <button v-if="replyingTo" @click="insertMention"
            class="p-1.5 text-gray-500 hover:text-blue-500 dark:hover:text-blue-400 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            title="Mention user">
            <i class="pi pi-at text-sm"></i>
          </button>
        </div>

        <div class="flex items-center gap-2">
          <button v-if="showCancel" @click="cancel"
            class="px-3 py-1 text-xs font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors">
            Cancel
          </button>
          <button @click="submit" :disabled="!canSubmit" :class="{
            'bg-blue-600 hover:bg-blue-700': canSubmit,
            'bg-blue-300 cursor-not-allowed': !canSubmit
          }" class="px-3 py-1 text-xs font-medium text-white rounded transition-colors flex items-center gap-1"
            :style="{ backgroundColor: theme }">
            <i class="pi pi-send text-xs"></i>
            {{ submitButtonText }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import Avatar from 'primevue/avatar'
import Textarea from 'primevue/textarea'
import { Picker } from 'emoji-mart-vue-fast'
import data from '@emoji-mart/data'
import { useAuthStore } from '../store/user'

const auth = useAuthStore()
const emojiData = data

const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  attachedFiles: {
    type: Array,
    default: () => []
  },
  showEmojiPicker: Boolean,
  submitButtonText: {
    type: String,
    default: 'Post Comment'
  },
  canSubmit: Boolean,
  theme: {
    type: String,
    default: '#3b82f6' // blue-500
  },
  replyingTo: {
    type: String,
    default: ''
  },
  placeholder: {
    type: String,
    required: false
  }
})

const emit = defineEmits([
  'update:modelValue',
  'toggle-emoji-picker',
  'file-upload',
  'remove-file',
  'submit',
  'cancel',
  'add-emoji',
  'insert-mention'
])

const fileInput = ref(null)
const commentTextarea = ref(null)

const currentUser = computed(() => auth.user)
const showCancel = computed(() => !!props.replyingTo)
const placeholderText = computed(() => 
  props.placeholder || (props.replyingTo ? 'Write your reply...' : 'Share your thoughts...')
)

const toggleEmojiPicker = () => {
  emit('toggle-emoji-picker')
}

const triggerFileInput = () => {
  fileInput.value.click()
}

const handleRemoveFile = (index) => {
  emit('remove-file', index)
}

const submit = () => {
  emit('submit')
}

const cancel = () => {
  emit('cancel')
}

const handleEmojiSelect = (emoji) => {
  emit('add-emoji', emoji)
}

const handleFileChange = (event) => {
  const files = Array.from(event.target.files)
  emit('file-upload', files)
  event.target.value = '' // Reset input to allow selecting same file again
}

const insertMention = () => {
  emit('insert-mention')
}

defineExpose({
  focus: () => commentTextarea.value?.$el?.focus()
})
</script>