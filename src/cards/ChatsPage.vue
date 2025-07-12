<template>
  <div class="w-full mx-auto py-1 px-2 ">
    <!-- Main Comment Input Section (only shown when not replying) -->
    <section v-if="!replyTarget" class="mb-6">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-100 dark:border-gray-700">
        <!-- Card Header -->
        <div class="px-4 py-3 border-b border-gray-100 dark:border-gray-700">
          <h2 class="text-base font-semibold text-gray-800 dark:text-gray-100">
            Leave a comment
          </h2>
        </div>

        <!-- Card Content -->
        <div ref="MainCommentInput" class="p-4">
          <CommentInput v-model="commentContent" :attached-files="attachedFiles" :show-emoji-picker="showEmojiPicker"
            :submit-button-text="submitButtonText" :can-submit="canSubmit" :theme="theme"
            @toggle-emoji-picker="toggleEmojiPicker" @trigger-file-upload="triggerFileUpload" @remove-file="removeFile"
            @submit="submitComment" @add-emoji="addEmoji" />
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
            @edit="editComment" @like="likeComment" @delete="deleteComment" @mention="mentionUser"
            @get_replies="fetchCommentReplies" />

          <!-- Reply Input Section (shown when replying to this comment) -->
          <div v-if="replyTarget?.id === comment.id" class="ml-5 mt-3">
            <div class="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-100 dark:border-gray-700">
              <!-- Card Header -->
              <div class="px-4 py-3 border-b border-gray-100 dark:border-gray-700">
                <h2 class="text-base font-semibold text-gray-800 dark:text-gray-100">
                  Replying to {{ replyTarget.user?.name }}
                </h2>
              </div>

              <!-- Card Content -->
              <div class="p-4">
                <CommentInput v-model="commentContent" :attached-files="attachedFiles"
                  :show-emoji-picker="showEmojiPicker" :submit-button-text="submitButtonText" :can-submit="canSubmit"
                  :theme="theme" :is-reply="true" @toggle-emoji-picker="toggleEmojiPicker"
                  @trigger-file-upload="triggerFileUpload" @remove-file="removeFile" @submit="submitComment"
                  @cancel="cancelComment" @add-emoji="addEmoji" />
              </div>
            </div>
          </div>

          <!-- Replies Section -->
          <div v-if="comment.replies?.length"
            class="ml-5 mt-1 pl-4 border-l border-gray-100 dark:border-gray-700 space-y-2">
            <article v-for="reply in comment.replies" :key="reply.id" class="group">
              <CommentCard :comment="reply" :current-user="currentUser" :theme="theme" :is-reply="true"
                @reply="startReply" @edit="editComment" @like="likeComment" @mention="mentionUser"
                @get_replies="fetchCommentReplies" @delete="deleteComment" />

              <!-- Reply Input Section (shown when replying to this reply) -->
              <div v-if="replyTarget?.id === reply.id" class="ml-5 mt-3">
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow border border-gray-100 dark:border-gray-700">
                  <!-- Card Header -->
                  <div class="px-4 py-3 border-b border-gray-100 dark:border-gray-700">
                    <h2 class="text-base font-semibold text-gray-800 dark:text-gray-100">
                      Replying to {{ replyTarget.user?.name }}
                    </h2>
                  </div>

                  <!-- Card Content -->
                  <div class="p-4">
                    <!-- In the reply sections of your parent component -->
                    <CommentInput v-model="commentContent" :attached-files="attachedFiles"
                      :show-emoji-picker="showEmojiPicker" :submit-button-text="submitButtonText"
                      :can-submit="canSubmit" :theme="theme" :is-reply="true" :replying-to="replyTarget?.user?.name"
                      @toggle-emoji-picker="toggleEmojiPicker" @trigger-file-upload="triggerFileUpload"
                      @remove-file="removeFile" @submit="submitComment" @add-emoji="addEmoji" @cancel="cancelComment" />
                  </div>
                </div>
              </div>
            </article>
          </div>
        </article>
      </div>
    </section>
  </div>
  <div v-if="isLoadingComments">
    <div class="w-full h-[40px] bg-gray-400/30 animate-pulse">loading...</div>
  </div>
          <Toast position="bottom-center" group="bc" />

</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'
import { formatDistanceToNow } from 'date-fns'
import Avatar from 'primevue/avatar'
import Textarea from 'primevue/textarea'
import data from '@emoji-mart/data'
import { Picker } from 'emoji-mart-vue-fast'
import CommentCard from './CommentCard.vue'
import CommentInput from './CommentInput.vue' // New component
import { useAuthStore } from '../store/user'
import { fetchComments, make_a_delete, make_a_post } from '../apis'
import { useToast } from 'primevue/usetoast'

const auth = useAuthStore()
const toast = useToast()

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
  const textarea = commentTextarea.value?.$el
  if (!textarea) return

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
  const textarea = commentTextarea.value?.$el
  if (!textarea) return

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
  console.log("REPLYING COMMENT: ", comment)

  replyTarget.value = comment
  editTarget.value = null
  commentContent.value = ''
  attachedFiles.value = []

  nextTick(() => {
    if (commentTextarea.value?.$el) {
      commentTextarea.value.$el.focus()
    }
  })
}

const MainCommentInput = ref(null)

const editComment = comment => {
  MainCommentInput.value.scrollIntoView({ behavior: 'smooth' ,block: 'center'})
  editTarget.value = comment
  replyTarget.value = null
  commentContent.value = comment.content
  attachedFiles.value = comment.attachments || []
  nextTick(() => {
    if (commentTextarea.value?.$el) {
      commentTextarea.value.$el.focus()
    }
  })
}

const deleteComment = async (comment) => {
  const response = await make_a_delete(
    `/recipes/${props.recipe_id}/comments/${comment.id}`,
    auth.token,
    {  }
  )
  if (!response.success) {
    toast.add({
      severity: 'error',
      summary: `Failed to delete comment`,
      detail: response.message || 'An error occurred while deleting the comment.',
      group: 'bc',
      life: 5000,
    });
  }else {
    // Remove comment from local state
    comments.value = comments.value.filter(c => c.id !== comment.id)
    toast.add({
      severity: 'success',
      summary: `Comment deleted`,
      // detail: 'The comment has been successfully deleted.',
      group: 'bc',
      life: 2000,
    });
  }
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

// Submit logic
const submitComment = async () => {
  if (!canSubmit.value) return
  isSubmitting.value = true

  const isEditing = Boolean(editTarget.value)
  const isReplying = Boolean(replyTarget.value)

  const payload = {
    content: commentContent.value,
    edited: isEditing,
    parent: isReplying ? (replyTarget.value.parent_id || replyTarget.value.id) : null,
    file: null,// Optional file handling
    comment_id: isEditing ? editTarget.value.id : null
  }

  console.log("COMMENTing: ", payload)

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

  console.log("message response: ", submittedComment)

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