<template>
  <div
    class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700/70 overflow-hidden transition-all hover:shadow-md relative backdrop-blur-sm group"
    :class="{ 
      'bg-blue-50/30 dark:bg-blue-900/10 border-blue-100 dark:border-blue-800/50': comment.user?.id === currentUser.id,
      'ml-10 border-l-2 border-l-blue-200 dark:border-l-blue-800/50': isReply 
    }"
    ref="commentCard"
    @click="showOptions = false"
  >
    <!-- Header -->
    <div class="px-4 py-3 flex items-start gap-3 relative">
      <Avatar 
        :image="comment.user?.profilePic || defaultAvatar" 
        shape="circle"
        class="w-9 h-9 flex-shrink-0 border-2 border-white dark:border-gray-700 shadow-sm hover:shadow transition-all"
        :class="{ 'w-8 h-8': isReply }" 
      />

      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-2">
          <h3 class="text-sm font-semibold text-gray-800 dark:text-gray-100 truncate flex items-center">
            <span v-if="comment.user?.id === currentUser.id" class="text-blue-600 dark:text-blue-400">You</span>
            <span v-else>{{ comment.user?.name || 'Anonymous' }}</span>
            <span 
              v-if="isMentioned(comment.user?.name)"
              class="ml-2 px-2 py-0.5 text-xs font-medium bg-blue-100/70 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 rounded-full flex items-center gap-1"
            >
              <i class="pi pi-at text-[0.65rem]"></i>
              <span>Mentioned</span>
            </span>
          </h3>
          
          <span 
            v-if="comment.user?.verified"
            class="text-blue-500 dark:text-blue-400"
            title="Verified user"
          >
            <i class="pi pi-verified text-sm"></i>
          </span>
        </div>

        <div class="flex items-center gap-2 mt-0.5">
          <time 
            :datetime="comment.created_at"
            class="text-xs text-gray-500 dark:text-gray-400/80"
            :title="new Date(comment.created_at).toLocaleString()"
          >
            {{ formatTimeAgo(comment.created_at) }}
          </time>
          
          <span 
            v-if="comment.is_edited" 
            class="text-xs text-amber-600 dark:text-amber-400/80 italic"
          >
            • edited
          </span>
        </div>
      </div>
      
      <button 
        v-if="showOptions"
        @click.stop="toggleOptions"
        class="p-1.5 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700/50 rounded-full transition-colors cursor-pointer"
        ref="optionsButton"
      >
        <i class="pi pi-ellipsis-h text-sm"></i>
      </button>
    </div>

    <!-- Content -->
    <div class="px-4 pb-3 -mt-1">
      <div class="text-sm text-gray-800 dark:text-gray-200 whitespace-pre-wrap break-words leading-relaxed"
        v-html="renderMentions(comment.content)">
      </div>

      <!-- Attachments -->
      <div v-if="comment.attachments?.length" class="mt-3 flex flex-wrap gap-2">
        <a 
          v-for="(attachment, idx) in comment.attachments" 
          :key="idx" 
          :href="attachment.url" 
          target="_blank"
          class="flex items-center gap-2 px-3 py-1.5 bg-gray-50 dark:bg-gray-700/50 rounded-lg text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors border border-gray-100 dark:border-gray-700/50 hover:shadow-sm"
          :class="attachment.type === 'image' ? 'p-0 overflow-hidden' : ''"
        >
          <template v-if="attachment.type === 'file'">
            <i class="pi text-gray-500 dark:text-gray-400" :class="getFileIcon(attachment)"></i>
            <span class="max-w-[160px] truncate font-medium">{{ attachment.name }}</span>
            <span class="text-xs text-gray-400 dark:text-gray-500 ml-auto">
              {{ formatFileSize(attachment.size) }}
            </span>
          </template>
          <img 
            v-else 
            :src="attachment.url" 
            class="h-24 w-auto rounded-lg object-cover border border-gray-100 dark:border-gray-700/50 hover:shadow-sm transition-all cursor-zoom-in"
            :alt="attachment.name || 'Attachment'"
            @click.stop="openImagePreview(attachment.url)"
          >
        </a>
      </div>
    </div>

    <!-- Footer -->
    <div class="px-4 py-2.5 border-t border-gray-100 dark:border-gray-700/50 bg-gray-50/30 dark:bg-gray-800/30">
      <div class="flex justify-between items-center flex-wrap gap-2">
        <div class="flex flex-wrap gap-1.5">
          <button 
            @click.stop="emit('like', comment)"
            class="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700/50 rounded-lg transition-colors"
            :class="{ 'text-blue-600 dark:text-blue-400': comment.isLiked }"
          >
            <i class="pi" :class="comment.isLiked ? 'pi-thumbs-up-fill' : 'pi-thumbs-up'"></i>
            <span v-if="comment.likes > 0">{{ comment.likes }}</span>
            <span class="sr-only">Like</span>
          </button>

          <button 
            @click.stop="emit('reply', comment)"
            class="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700/50 rounded-lg transition-colors"
          >
            <i class="pi pi-reply"></i>
            <span>Reply</span>
          </button>

          <button 
            v-if="!comment.parent_id && comment.replyCount > 0" 
            @click.stop="emit('get_replies', comment.id)"
            class="flex items-center gap-1.5 px-3 py-1.5 text-sm font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700/50 rounded-lg transition-colors"
          >
            <i class="pi pi-comments"></i>
            <span>{{ comment.replyCount }} {{ comment.replyCount === 1 ? 'reply' : 'replies' }}</span>
          </button>
        </div>

        <!-- More Options Dropdown -->
        <div 
          v-if="showOptions && optionsOpen" 
          class="absolute right-4 bottom-12 z-10 shadow-xl"
          ref="dropdownMenu"
        >
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-100 dark:border-gray-700/70 overflow-hidden min-w-[160px]">
            <button 
              v-for="(option, index) in MoreButtons"
              :key="index"
              @click.stop="handleOptionClick(option)"
              class="w-full px-4 py-2.5 text-sm text-left flex items-center gap-2 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
              :class="{
                'text-red-500 hover:text-red-600 dark:hover:text-red-400': option.severity === 'danger'
              }"
            >
              <i :class="option.icon"></i>
              <span>{{ option.label }}</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import Avatar from 'primevue/avatar'
import { formatDistanceToNow } from 'date-fns'

const props = defineProps({
  comment: {
    type: Object,
    required: true
  },
  isReply: {
    type: Boolean,
    default: false
  },
  currentUser: {
    type: Object,
    required: true
  },
  showOptions: {
    type: Boolean,
    default: true
  },
  MoreButtons: {
    type: Array,
    default: () => [
      { label: 'Edit', icon: 'pi pi-pencil', command: 'edit' },
      { label: 'Delete', icon: 'pi pi-trash', command: 'delete', severity: 'danger' },
    ]
  }
})

const emit = defineEmits(['like', 'reply', 'edit', 'delete', 'get_replies'])

const defaultAvatar = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'
const optionsOpen = ref(false)
const commentCard = ref(null)
const optionsButton = ref(null)
const dropdownMenu = ref(null)

const formatTimeAgo = (date) => formatDistanceToNow(new Date(date), { addSuffix: true })

const renderMentions = (text) => {
  if (!text) return ''
  return text.replace(/@(\w+)/g, '<span class="text-blue-500 dark:text-blue-400 font-medium">@$1</span>')
}

const isMentioned = (username) => {
  if (!username || !props.currentUser) return false
  return username.toLowerCase() === props.currentUser.name?.toLowerCase()
}

const toggleOptions = () => {
  optionsOpen.value = !optionsOpen.value
}

const handleOptionClick = (option) => {
  optionsOpen.value = false
  emit(option.command, props.comment)
}

const handleClickOutside = (event) => {
  if (optionsOpen.value && 
      !commentCard.value.contains(event.target) && 
      !dropdownMenu.value?.contains(event.target)) {
    optionsOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})

const getFileIcon = (file) => {
  const extension = file.name.split('.').pop().toLowerCase()
  const iconMap = {
    image: ['jpg', 'jpeg', 'png', 'gif', 'svg', 'webp'],
    pdf: ['pdf'],
    word: ['doc', 'docx'],
    excel: ['xls', 'xlsx'],
    powerpoint: ['ppt', 'pptx'],
    archive: ['zip', 'rar', '7z'],
    audio: ['mp3', 'wav', 'ogg'],
    video: ['mp4', 'mov', 'avi']
  }
  
  for (const [type, exts] of Object.entries(iconMap)) {
    if (exts.includes(extension)) return `pi-file-${type}`
  }
  return 'pi-file'
}

const formatFileSize = (bytes) => {
  if (!bytes) return ''
  const units = ['B', 'KB', 'MB', 'GB']
  let size = bytes
  let unitIndex = 0
  
  while (size >= 1024 && unitIndex < units.length - 1) {
    size /= 1024
    unitIndex++
  }
  
  return `${size.toFixed(unitIndex > 0 ? 1 : 0)} ${units[unitIndex]}`
}

const openImagePreview = (url) => {
  // Implement image preview logic
  console.log('Open image preview:', url)
}
</script>

<style scoped>
/* Smooth transitions */
button, a, .avatar {
  transition: all 0.2s ease;
}

/* Better hover states */
button:hover {
  transform: translateY(-1px);
}

/* Subtle pulse animation for new comments */
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0.4); }
  70% { box-shadow: 0 0 0 6px rgba(59, 130, 246, 0); }
  100% { box-shadow: 0 0 0 0 rgba(59, 130, 246, 0); }
}

/* Apply to new comments */
.new-comment {
  animation: pulse 1.5s ease-out;
}

/* Ensure proper spacing for mentions */
[class*="pi-at"] {
  margin-top: -1px;
}

/* Better image attachment display */
img {
  max-height: 150px;
  max-width: 100%;
}
</style>