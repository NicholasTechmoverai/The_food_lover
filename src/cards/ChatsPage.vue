<template>
  <div class="w-full mx-auto px-2 py-4">
    <!-- Comment Input Section -->
    <section class="mb-6">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-100 dark:border-gray-700">
        <!-- Card Header -->
        <div class="px-4 py-3 border-b border-gray-100 dark:border-gray-700">
          <h2 class="text-base font-semibold text-gray-800 dark:text-gray-100">
            {{ replyTarget ? `Replying to ${replyTarget.user?.name}` : 'Leave a comment' }}
          </h2>
        </div>

        <!-- Card Content -->
        <div class="p-4">
          <div class="flex gap-3">
            <!-- User Avatar -->
            <div class="flex-shrink-0">
              <Avatar :image="currentUser.profilePic" shape="circle" class="w-8 h-8" />
            </div>

            <!-- Input Area -->
            <div class="flex-1 relative">
              <!-- Main Textarea -->
              <Textarea v-model="commentContent"
                :placeholder="replyTarget ? 'Write your reply...' : 'Share your thoughts...'" rows="2"
                class="w-full px-3 py-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-md focus:ring-1 focus:ring-blue-500 focus:border-blue-500 outline-none transition-colors"
                autoResize ref="commentTextarea" />

              <!-- Mention Preview -->
              <div v-if="replyTarget"
                class="mt-1 inline-flex items-center px-2 py-0.5 bg-blue-50 dark:bg-blue-900/30 rounded-full text-xs">
                <span class="font-medium text-blue-600 dark:text-blue-300">@{{ replyTarget.user?.name }}</span>
                <span class="ml-1 text-gray-500 dark:text-gray-400">will be notified</span>
              </div>

              <!-- Emoji Picker -->
              <div v-if="showEmojiPicker" class="absolute bottom-full left-0 mb-1 z-10">
                <Picker :data="emojiData" @select="addEmoji" :showPreview="false" :showSearch="true"
                  title="Pick an emoji" />
              </div>

              <!-- File Previews -->
              <div v-if="attachedFiles.length > 0" class="mt-2 flex flex-wrap gap-1">
                <div v-for="(file, index) in attachedFiles" :key="index"
                  class="flex items-center gap-1 px-2 py-1 bg-gray-50 dark:bg-gray-700 rounded-full text-xs">
                  <span class="max-w-[100px] truncate text-gray-700 dark:text-gray-300">{{ file.name }}</span>
                  <button @click="removeFile(index)"
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
                  <button @click="triggerFileUpload"
                    class="p-1.5 text-gray-500 hover:text-blue-500 dark:hover:text-blue-400 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    title="Attach files">
                    <i class="pi pi-paperclip text-sm"></i>
                  </button>
                  <input type="file" ref="fileInput" class="hidden" @change="handleFileUpload"
                    accept="image/*,.pdf,.doc,.docx" multiple />

                  <button v-if="replyTarget" @click="insertMention"
                    class="p-1.5 text-gray-500 hover:text-blue-500 dark:hover:text-blue-400 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    title="Mention user">
                    <i class="pi pi-at text-sm"></i>
                  </button>
                </div>

                <div class="flex items-center gap-2">
                  <button v-if="replyTarget || editTarget" @click="cancelComment"
                    class="px-3 py-1 text-xs font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors">
                    Cancel
                  </button>
                  <button @click="submitComment" :disabled="!canSubmit" :class="{
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
        </div>
      </div>
    </section>

    <!-- Comments List -->
    <section>
      <div v-if="comments.length === 0" class="flex flex-col items-center justify-center py-8 text-center">
        <div class="w-12 h-12 flex items-center justify-center bg-gray-100 dark:bg-gray-700 rounded-full mb-3">
          <i class="pi pi-comments text-xl text-gray-400"></i>
        </div>
        <p class="text-sm text-gray-500 dark:text-gray-400">No comments yet. Be the first to share your thoughts!</p>
      </div>

      <div v-else class="space-y-2">
        <article v-for="comment in comments" :key="comment.id" class="group">
          <CommentCard :comment="comment" :current-user="currentUser" :theme="theme" @reply="startReply"
            @edit="editComment" @like="likeComment" @mention="mentionUser" @get_replies="fetchCommentReplies"/>

          <!-- Replies Section -->
          <div v-if="comment.replies?.length"
            class="ml-10 mt-1 pl-4 border-l border-gray-100 dark:border-gray-700 space-y-2">
            <article v-for="reply in comment.replies" :key="reply.id" class="group">
              <CommentCard :comment="reply" :current-user="currentUser" :theme="theme" :is-reply="true"
                @reply="startReply" @edit="editComment" @like="likeComment" @mention="mentionUser"
                @get_replies="fetchCommentReplies" />
            </article>
          </div>
        </article>
      </div>
    </section>
  </div>
  <div v-if="isLoadingComments">
    <div class="w-full h-[40px] bg-gray-400/30 animate-pulse">loading...</div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'
import { formatDistanceToNow } from 'date-fns'
import Avatar from 'primevue/avatar'
import Textarea from 'primevue/textarea'
import data from '@emoji-mart/data'
import { Picker } from 'emoji-mart-vue-fast'
import CommentCard from './CommentCard.vue'
import { useAuthStore } from '../store/user'
import { fetchComments, make_a_post } from '../apis'

const auth = useAuthStore()

const defaultAvatar =
    'https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png'

const props = defineProps({
    theme: String,
    recipe_id: {
        type: String,
        required: true
    }
})

// UI state
const isLoadingComments = ref(false)
const isSubmitting = ref(false)

// Comment input state
const emojiData = data
const commentContent = ref('')
const replyTarget = ref(null)
const editTarget = ref(null)
const showEmojiPicker = ref(false)
const attachedFiles = ref([])
const fileInput = ref(null)
const commentTextarea = ref(null)
const comments = ref([])

// Computed states
const currentUser = auth.user

const canSubmit = computed(() => {
    return commentContent.value.trim().length > 0 || attachedFiles.value.length > 0
})

const submitButtonText = computed(() => {
    if (editTarget.value) return 'Update'
    if (replyTarget.value) return 'Post Reply'
    return 'Post Comment'
})

// Format time
const formatTimeAgo = date => formatDistanceToNow(new Date(date), { addSuffix: true })

// Emoji
const toggleEmojiPicker = () => {
    showEmojiPicker.value = !showEmojiPicker.value
}

const addEmoji = emoji => {
    const textarea = commentTextarea.value.$el
    const start = textarea.selectionStart
    const end = textarea.selectionEnd

    const before = commentContent.value.substring(0, start)
    const after = commentContent.value.substring(end)

    commentContent.value = before + emoji.native + after

    nextTick(() => {
        textarea.focus()
        textarea.selectionStart = start + emoji.native.length
        textarea.selectionEnd = start + emoji.native.length
    })

    showEmojiPicker.value = false
}

// File upload
const triggerFileUpload = () => fileInput.value.click()

const handleFileUpload = event => {
    const files = Array.from(event.target.files)
    attachedFiles.value.push(
        ...files.map(file => ({
            name: file.name,
            size: file.size,
            type: file.type.startsWith('image') ? 'image' : 'file',
            file
        }))
    )
    event.target.value = ''
}

const removeFile = index => attachedFiles.value.splice(index, 1)

// Mentions
const insertMention = () => {
    if (replyTarget.value) {
        const mention = `@${replyTarget.value.user.name} `
        insertAtCursor(mention)
    }
}

const mentionUser = user => {
    if (user) {
        const mention = `@${user.name} `
        insertAtCursor(mention)
    }
}

const insertAtCursor = text => {
    const textarea = commentTextarea.value.$el
    const start = textarea.selectionStart
    const end = textarea.selectionEnd

    commentContent.value =
        commentContent.value.substring(0, start) + text + commentContent.value.substring(end)

    nextTick(() => {
        textarea.focus()
        textarea.selectionStart = start + text.length
        textarea.selectionEnd = start + text.length
    })
}

// Reply/edit logic
const startReply = comment => {
    console.log("REPLING COMMENT: ", comment)

    replyTarget.value = comment
    editTarget.value = null
    nextTick(() => commentTextarea.value.$el.focus())
    insertMention()
}

const editComment = comment => {
    editTarget.value = comment
    replyTarget.value = null
    commentContent.value = comment.content
    attachedFiles.value = comment.attachments || []
    nextTick(() => commentTextarea.value.$el.focus())
}

const cancelComment = () => {
    replyTarget.value = null
    editTarget.value = null
    commentContent.value = ''
    attachedFiles.value = []
    showEmojiPicker.value = false
}

// Like action (demo)
const likeComment = comment => {
    comment.likes += 1
}

const fetchCommentReplies = async (parent_id) => {
  const { success, data, message } = await fetchComments(auth.token, props.recipe_id, {
    parent: parent_id,
    recipe_id: props.recipe_id,
  });

  if (success && data.replies) {
    const parent = comments.value.find(c => c.id === parent_id);
    if (parent) {
      parent.replies = data.replies; // Replace preview reply with full thread
      parent.replyCount = data.replies.length; // Optional: update total
    }
  } else {
    console.error('Failed to load replies:', message);
  }
};


// 🧠 SUBMIT LOGIC
const submitComment = async () => {
    if (!canSubmit.value) return
    isSubmitting.value = true

    const isEditing = Boolean(editTarget.value)
    const isReplying = Boolean(replyTarget.value)

    const payload = {
        content: commentContent.value,
        edited: isEditing,
        parent: isReplying ? (replyTarget.value.parent_id || replyTarget.value.id) : null,
        file: null // Optional file handling
    }

    console.log(" COMMENTing: ", payload)


    const response = await make_a_post(
        `/recipes/${props.recipe_id}/comments`,
        auth.token,
        payload
    )

    if (!response.success) {
        isSubmitting.value = false
        return alert(response.message || 'Failed to submit comment')
    }

    const submittedComment = {
        ...response.data,
        user: { ...currentUser },
        replies: [],
        attachments: attachedFiles.value.map(file => ({
            name: file.name,
            url: URL.createObjectURL(file.file),
            type: file.type
        }))
    }

    console.log(" message rsponce: ", submittedComment)

    if (isEditing) {
        editTarget.value.content = submittedComment.content
        editTarget.value.is_edited = true
        editTarget.value.attachments = submittedComment.attachments
    } else if (isReplying) {
        const parentId = replyTarget.value.parent_id || replyTarget.value.id
        const parent = comments.value.find(c => c.id === parentId)
        parent?.replies?.push(submittedComment)
    } else {
        comments.value.unshift(submittedComment)
    }

    cancelComment()
    isSubmitting.value = false
}

onMounted(async () => {
    isLoadingComments.value = true;

    const { success, data, message } = await fetchComments(auth.token, props.recipe_id, { recipe_id: props.recipe_id });
    if (success) {
        comments.value = data.comments;

    } else {
        console.error('Failed to load comments:', message);
        comments.value = [];
    }

    isLoadingComments.value = false;
});

</script>
