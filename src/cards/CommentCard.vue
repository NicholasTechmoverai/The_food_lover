<template>
  <div class="bg-white/50 dark:bg-gray-800/50 rounded-md shadow border border-gray-100/50 dark:border-gray-700/50 overflow-hidden transition-all hover:shadow-sm"
    :class="{ 'bg-gray-50 dark:bg-gray-700/50': isReply, 'ml-10': isReply }"
    :style="comment.user?.id === currentUser.id ? { backgroundColor: theme + '30' } : {}">
    <!-- Header -->
    <div class="px-3 py-2 flex items-start gap-2">
      <Avatar :image="comment.user?.profilePic || defaultAvatar" shape="circle" class="w-8 h-8 flex-shrink-0"
        :class="{ 'w-7 h-7': isReply }" />

      <div class="flex-1 min-w-0">
        <div class="flex items-center gap-1">
          <h3 class="text-xs font-semibold text-gray-800 dark:text-gray-100 truncate">
            {{ comment.user?.name || 'Anonymous' }}
            <span v-if="isMentioned(comment.user?.name)"
              class="ml-1 px-1.5 py-0.5 text-xs font-medium bg-blue-100 dark:bg-blue-900/50 text-blue-800 dark:text-blue-200 rounded-full">
              Mentioned
            </span>
          </h3>
        </div>

        <p class="text-xs text-gray-500 dark:text-gray-400">
          <time :datetime="comment.created_at">
            {{ formatTimeAgo(comment.created_at) }}
          </time>
          <span v-if="comment.is_edited" class="text-amber-500 dark:text-amber-400 italic"> • edited</span>
        </p>
      </div>
    </div>

    <!-- Content -->
    <div class="px-3 pb-2 -mt-1">
      <p class="text-sm text-gray-700 dark:text-gray-300 whitespace-pre-wrap break-words"
        v-html="renderMentions(comment.content)"></p>

      <!-- Attachments -->
      <div v-if="comment.attachments?.length" class="mt-2 flex flex-wrap gap-1">
        <a v-for="(attachment, idx) in comment.attachments" :key="idx" :href="attachment.url" target="_blank"
          class="flex items-center gap-1 px-2 py-1 bg-gray-50 dark:bg-gray-700 rounded text-xs text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
          <template v-if="attachment.type === 'file'">
            <i class="pi pi-file text-gray-400"></i>
            <span class="max-w-[150px] truncate">{{ attachment.name }}</span>
          </template>
          <img v-else :src="attachment.url" class="h-10 rounded object-cover" alt="Attachment">
        </a>
      </div>
    </div>

    <!-- Footer -->
    <div class="px-3 py-2 border-t border-gray-100 dark:border-gray-700 [&_button]:cursor-pointer">
      <div class="flex flex-wrap gap-1">
        <button @click="$emit('like', comment)"
          class="flex items-center gap-1 px-2 py-1 text-xs font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors">
          <i class="pi pi-thumbs-up text-xs"></i>
          <span>{{ comment.likes > 0 ? `Like (${comment.likes})` : 'Like' }}</span>
        </button>

        <button @click="$emit('reply', comment)"
          class="flex items-center gap-1 px-2 py-1 text-xs font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors">
          <i class="pi pi-reply text-xs"></i>
          <span>Reply</span>
        </button>
        
        <button v-if="!comment.parent_id" @click="$emit('get_replies', comment.id)"
          class="flex items-center gap-1 px-2 py-1 text-xs font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors">
          replies({{ comment.replyCount}})
        </button>

        <button v-if="comment.user?.id === currentUser.id" @click="$emit('edit', comment)"
          class="flex items-center gap-1 px-2 py-1 text-xs font-medium text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors">
          <i class="pi pi-pencil text-xs"></i>
          <span>Edit</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import Avatar from 'primevue/avatar'
import { formatDistanceToNow } from 'date-fns'

const props = defineProps({
    comment: {
        type: Object,
        required: true
    },
    currentUser: {
        type: Object,
        required: true
    },
    isReply: {
        type: Boolean,
        default: false
    },
    theme: String,
})

const defaultAvatar = 'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'

const formatTimeAgo = (date) => formatDistanceToNow(new Date(date), { addSuffix: true })


const renderMentions = (text) => {
    return text.replace(/@(\w+)/g, '<span class="text-blue-500 dark:text-blue-400 font-medium">@$1</span>')
}

const isMentioned = (username) => {
    if (!username) return false
    // This would check against all comments in the parent component
    return false
}
</script>