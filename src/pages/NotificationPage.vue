<template>
  <div class="flex flex-col md:flex-row min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Vertical Navigation -->
    <div
      class="w-full md:w-64 bg-white dark:bg-gray-800 border-b md:border-b-0 md:border-r border-gray-200 dark:border-gray-700 flex-shrink-0">
      <div class="p-4 flex items-center space-x-3 md:block md:space-x-0 md:space-y-4">
        <!-- Navigation Tabs -->
        <nav class="flex md:block space-x-4 md:space-x-0 md:space-y-1 overflow-x-auto scrollbar-hide md:mt-6">
          <button v-for="tab in tabs" :key="tab.id" @click="activateTab(tab)" :class="{
            'bg-[var(--theme-color)]/10 text-[var(--theme-color)]': activeTab === tab.id,
            'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700': activeTab !== tab.id
          }"
            class="px-3 py-2 rounded-lg md:rounded-none md:rounded-r-lg text-sm font-medium flex items-center transition-colors whitespace-nowrap">
            <i :class="tab.icon" class="mr-2"></i>
            <span>{{ tab.label }}</span>
            <span v-if="tab.badgeCount > 0"
              class="ml-auto bg-[var(--theme-color)] text-white text-xs px-2 py-0.5 rounded-full">
              {{ tab.badgeCount }}
            </span>
          </button>
        </nav>
        
        <!-- Notification Settings -->
        <div class="hidden md:block mt-8 pt-4 border-t border-gray-200 dark:border-gray-700">
          <button @click="openSettings" class="w-full text-left px-3 py-2 text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors flex items-center">
            <i class="pi pi-cog mr-2"></i>
            <span>Notification Settings</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 overflow-hidden">
      <!-- Header -->
      <div
        class="sticky top-0 z-10 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm p-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
        <div class="flex items-center">
          <h1 class="text-xl font-bold text-gray-900 dark:text-white">
            <i :class="activeTabIcon" class="mr-2"></i>
            {{ activeTabLabel }}
          </h1>
          <span v-if="notifications.length > 0" class="ml-2 text-sm text-gray-500 dark:text-gray-400">
            ({{ notifications.length }})
          </span>
        </div>
        <div class="flex space-x-2">
          <button @click="markAllAsRead"
            class="p-2 text-gray-500 dark:text-gray-400 hover:text-[var(--theme-color)] dark:hover:text-[var(--theme-color)] transition-colors"
            title="Mark all as read" v-if="unreadCount > 0">
            <i class="pi pi-check-circle"></i>
          </button>
          <button @click="fetchNotifications()"
            class="p-2 text-gray-500 dark:text-gray-400 hover:text-[var(--theme-color)] dark:hover:text-[var(--theme-color)] transition-colors"
            title="Refresh">
            <i class="pi pi-refresh" :class="{ 'animate-spin': loading }"></i>
          </button>
        </div>
      </div>

      <!-- Notification Content -->
      <div class="h-[calc(100vh-64px)] overflow-y-auto p-4">
        <template v-if="!loading">
          <!-- Notifications List -->
          <div v-if="notifications.length > 0" class="space-y-4">
            <div v-for="notification in notifications" :key="notification.id"
              class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden"
              :class="{
                'ring-1 ring-[var(--theme-color)]/30': !notification.read,
                'hover:shadow-md transition-shadow duration-200': true
              }">
              <div class="px-4 py-3 flex items-start">
                <!-- Actor Avatar -->
                <div class="flex-shrink-0">
                  <img v-if="notification.actor?.avatar" 
                       :src="notification.actor.avatar" 
                       class="w-10 h-10 rounded-full object-cover" 
                       :alt="notification.actor.username">
                  <div v-else 
                       :class="getNotificationIconClass(notification.type)"
                       class="w-10 h-10 rounded-full flex items-center justify-center">
                    <i :class="getNotificationIcon(notification.type)" class="text-sm"></i>
                  </div>
                </div>
                
                <div class="ml-3 flex-1 min-w-0">
                  <!-- Notification Content -->
                  <p class="text-sm text-gray-800 dark:text-gray-200">
                    <span class="font-medium">{{ notification.actor?.username || 'System' }}</span> 
                    {{ notification.verb }}
                    <span v-if="notification.target" class="font-medium text-[var(--theme-color)]">
                      {{ notification.target.type }}
                    </span>
                  </p>
                  
                  <!-- Timestamp -->
                  <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {{ formatTime(notification.created_at) }}
                  </p>
                  
                  <!-- Preview Text -->
                  <div v-if="notification.preview"
                    class="mt-2 text-sm text-gray-600 dark:text-gray-300 bg-gray-100 dark:bg-gray-700/30 p-2 rounded">
                    {{ notification.preview }}
                  </div>
                  
                  <!-- Target Image (if available) -->
                  <div v-if="notification.target?.image" class="mt-2">
                    <img :src="notification.target.image" 
                         class="max-w-[50px] h-auto rounded-md border border-gray-200 dark:border-gray-600"
                         :alt="'Preview of ' + notification.target.type">
                  </div>
                  
                  <!-- Actions -->
                  <div v-if="notification.actions" class="mt-2 flex space-x-2">
                    <button v-for="action in notification.actions" :key="action.label"
                      @click.stop="handleAction(notification, action)"
                      class="text-xs px-2 py-1 rounded border border-gray-200 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors">
                      {{ action.label }}
                    </button>
                  </div>
                </div>
                
                <!-- Notification Controls -->
                <div class="flex flex-col items-center gap-2 ml-2">
                  <button @click.stop="toggleReadStatus(notification)"
                    class="text-gray-400 hover:text-[var(--theme-color)] dark:hover:text-[var(--theme-color)] transition-colors p-1"
                    :title="notification.read ? 'Mark as unread' : 'Mark as read'">
                    <i :class="notification.read ? 'pi pi-eye-slash text-xs' : 'pi pi-check text-xs'"></i>
                  </button>
                  <button @click.stop="deleteNotification(notification)"
                    class="text-gray-400 hover:text-red-500 dark:hover:text-red-400 transition-colors p-1"
                    title="Delete notification">
                    <i class="pi pi-trash text-xs"></i>
                  </button>
                </div>
              </div>
            </div>
            
            <!-- Infinite loading indicator -->
            <div v-if="hasMoreNotifications" class="flex justify-center py-4">
              <button @click="loadMore" :disabled="loadingMore" class="text-sm text-[var(--theme-color)] hover:underline flex items-center">
                <i class="pi pi-chevron-down mr-1" :class="{ 'animate-bounce': loadingMore }"></i>
                {{ loadingMore ? 'Loading...' : 'Load more' }}
              </button>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="h-full flex flex-col items-center justify-center text-center py-12">
            <div
              class="w-48 h-48 bg-gradient-to-br from-[var(--theme-color)]/5 to-transparent rounded-full flex items-center justify-center mb-6">
              <i :class="activeTabIcon" class="text-5xl text-[var(--theme-color)] opacity-70"></i>
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">
              {{ emptyState.title }}
            </h3>
            <p class="text-gray-500 dark:text-gray-400 mb-6 max-w-md mx-auto">
              {{ emptyState.description }}
            </p>
            <button @click="fetchNotifications()"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-[var(--theme-color)] hover:bg-[var(--theme-color)]/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--theme-color)] transition-all">
              <i class="pi pi-sync mr-2"></i>
              Refresh
            </button>
          </div>
        </template>

        <!-- Loading State -->
        <div v-else class="h-full flex flex-col items-center justify-center">
          <div class="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-[var(--theme-color)] mb-4"></div>
          <p class="text-gray-500 dark:text-gray-400">Loading notifications...</p>
        </div>
      </div>
    </div>
    
    <!-- Settings Modal -->
    <transition name="fade">
      <div v-if="showSettings" class="fixed inset-0 z-50 overflow-y-auto">
        <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
          <div class="fixed inset-0 transition-opacity" aria-hidden="true">
            <div class="absolute inset-0 bg-gray-500 dark:bg-gray-900 opacity-75" @click="closeSettings"></div>
          </div>
          <span class="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
          <div class="inline-block align-bottom bg-white dark:bg-gray-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
            <div class="px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
              <div class="flex justify-between items-start">
                <h3 class="text-lg leading-6 font-medium text-gray-900 dark:text-white">
                  Notification Settings
                </h3>
                <button @click="closeSettings" class="text-gray-400 hover:text-gray-500 dark:hover:text-gray-300">
                  <i class="pi pi-times"></i>
                </button>
              </div>
              <div class="mt-4 space-y-4">
                <div class="flex items-center justify-between">
                  <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Email Notifications</label>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="settings.emailNotifications" class="sr-only peer">
                    <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-[var(--theme-color)]/30 dark:peer-focus:ring-[var(--theme-color)]/30 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-[var(--theme-color)]"></div>
                  </label>
                </div>
                <div class="flex items-center justify-between">
                  <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Push Notifications</label>
                  <label class="relative inline-flex items-center cursor-pointer">
                    <input type="checkbox" v-model="settings.pushNotifications" class="sr-only peer">
                    <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-[var(--theme-color)]/30 dark:peer-focus:ring-[var(--theme-color)]/30 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-[var(--theme-color)]"></div>
                  </label>
                </div>
                <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
                  <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Notification Types</h4>
                  <div class="space-y-2">
                    <div v-for="type in notificationTypes" :key="type.id" class="flex items-center">
                      <input :id="`notification-type-${type.id}`" v-model="settings.notificationTypes" type="checkbox" :value="type.id" class="h-4 w-4 text-[var(--theme-color)] focus:ring-[var(--theme-color)] border-gray-300 dark:border-gray-600 rounded">
                      <label :for="`notification-type-${type.id}`" class="ml-2 text-sm text-gray-700 dark:text-gray-300">
                        {{ type.label }}
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
              <button @click="saveSettings" type="button" class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-[var(--theme-color)] text-base font-medium text-white hover:bg-[var(--theme-color)]/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--theme-color)] sm:ml-3 sm:w-auto sm:text-sm transition-colors">
                Save Settings
              </button>
              <button @click="closeSettings" type="button" class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-600 shadow-sm px-4 py-2 bg-white dark:bg-gray-700 text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--theme-color)] sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm transition-colors">
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { format } from 'date-fns'
import { useAuthStore } from '../store/user'
import router from '../router'
import { useRoute } from 'vue-router'
import { make_a_delete, make_a_post } from '../apis'

const route = useRoute()
const props = defineProps({
  userTheme: {
    type: String,
    default: '#f97316'
  }
})

// Stores
const auth = useAuthStore()

// Reactive state
const activeTab = ref(route.query.tab || 'all')
const loading = ref(true)
const loadingMore = ref(false)
const notifications = ref([])
const showSettings = ref(false)
const currentPage = ref(1)
const hasMoreNotifications = ref(true)

// Settings
const settings = ref({
  emailNotifications: true,
  pushNotifications: true,
  notificationTypes: ['like', 'comment', 'mention', 'follow', 'system']
})

const notificationTypes = [
  { id: 'like', label: 'Likes' },
  { id: 'comment', label: 'Comments' },
  { id: 'mention', label: 'Mentions' },
  { id: 'follow', label: 'New Followers' },
  { id: 'system', label: 'System Notifications' }
]

// Computed properties
const userName = computed(() => auth.user?.name || 'User')
const userAvatar = computed(() => auth.user?.avatar || 'https://ui-avatars.com/api/?name=' + encodeURIComponent(userName.value))

const tabs = computed(() => [
  { id: 'all', label: 'All Notifications', icon: 'pi pi-bell', badgeCount: unreadCount.value },
  { id: 'mentions', label: 'Mentions', icon: 'pi pi-at', badgeCount: notifications.value.filter(n => n.type === 'mention' && !n.read).length },
  { id: 'follows', label: 'Followers', icon: 'pi pi-users', badgeCount: notifications.value.filter(n => n.type === 'follow' && !n.read).length },
  { id: 'likes', label: 'Likes', icon: 'pi pi-heart', badgeCount: notifications.value.filter(n => n.type === 'like' && !n.read).length },
  { id: 'comments', label: 'Comments', icon: 'pi pi-comments', badgeCount: notifications.value.filter(n => n.type === 'comment' && !n.read).length },
  { id: 'system', label: 'System', icon: 'pi pi-cog', badgeCount: notifications.value.filter(n => n.type === 'system' && !n.read).length }
])

const activeTabLabel = computed(() => {
  return tabs.value.find(tab => tab.id === activeTab.value)?.label || ''
})

const activeTabIcon = computed(() => {
  return tabs.value.find(tab => tab.id === activeTab.value)?.icon || 'pi pi-bell'
})

const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.read).length
})

const emptyState = computed(() => {
  const states = {
    all: {
      title: "No notifications yet",
      description: "Your notifications will appear here when you receive them"
    },
    mentions: {
      title: "No mentions yet",
      description: "When someone mentions you, it will appear here"
    },
    follows: {
      title: "No new followers",
      description: "Your new followers will appear here"
    },
    likes: {
      title: "No likes yet",
      description: "When someone likes your content, it will appear here"
    },
    comments: {
      title: "No comments yet",
      description: "Comments on your posts will appear here"
    },
    system: {
      title: "No system messages",
      description: "System notifications will appear here"
    }
  }
  
  return states[activeTab.value] || states.all
})

// Methods
const activateTab = async (tab) => {
  if (activeTab.value === tab.id) return
  activeTab.value = tab.id
  currentPage.value = 1
  hasMoreNotifications.value = true
  router.push({
    path: "/notifications",
    query: { tab: tab.id },
  })
  await fetchNotifications()
}

const fetchNotifications = async () => {
  try {
    loading.value = true
    const response = await make_a_post(
      `/notifications/${auth.user.name}/fetch`, 
      auth.token, 
      { 
        [activeTab.value]:true,
        page: currentPage.value,
        per_page: 20
      }
    )
    
    if (response.success) {
      if (currentPage.value === 1) {
        notifications.value = response.data || []
      } else {
        notifications.value = [...notifications.value, ...(response.data || [])]
      }
      
      hasMoreNotifications.value = response.has_more || false
    }
  } catch (error) {
    console.error('Error fetching notifications:', error)
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

const loadMore = async () => {
  if (loadingMore.value || !hasMoreNotifications.value) return
  
  loadingMore.value = true
  currentPage.value += 1
  await fetchNotifications()
}

const getNotificationIcon = (type) => {
  const icons = {
    like: 'pi pi-heart',
    comment: 'pi pi-comment',
    mention: 'pi pi-at',
    follow: 'pi pi-user-plus',
    recipe: 'pi pi-book',
    system: 'pi pi-info-circle',
    message: 'pi pi-envelope',
    share: 'pi pi-share-alt'
  }
  return icons[type] || 'pi pi-bell'
}

const getNotificationIconClass = (type) => {
  return `bg-[var(--theme-color)]/10 text-[var(--theme-color)]`
}

const formatTime = (dateString) => {
  return format(new Date(dateString), 'h:mm a')
}

const toggleReadStatus = async (notification) => {
  try {
    const newReadStatus = !notification.read
    await make_a_post(
      `/notifications/${notification.id}/read`, 
      auth.token, 
      { read: newReadStatus }
    )
    notification.read = newReadStatus
  } catch (error) {
    console.error('Error updating read status:', error)
  }
}

const markAllAsRead = async () => {
  try {
    await make_a_post(
      `/notifications/mark-all-read`, 
      auth.token, 
      { type: activeTab.value }
    )
    // Update local state
    notifications.value.forEach(n => { n.read = true })
  } catch (error) {
    console.error('Error marking all as read:', error)
  }
}

const deleteNotification = async (notification) => {
  try {
    await make_a_delete(
      `/notifications/${notification.id}/delete`, 
      auth.token,{}
    )
    notifications.value = notifications.value.filter(n => n.id !== notification.id)
  } catch (error) {
    console.error('Error deleting notification:', error)
  }
}

const handleAction = (notification, action) => {
  console.log('Action:', action.label, 'on notification:', notification.id)
  if (action.url) {
    router.push(action.url)
  }
}

const openSettings = () => {
  showSettings.value = true
}

const closeSettings = () => {
  showSettings.value = false
}

const saveSettings = async () => {
  try {
    await make_a_post(
      `/notifications/settings`, 
      auth.token, 
      settings.value
    )
    closeSettings()
  } catch (error) {
    console.error('Error saving settings:', error)
  }
}

// Lifecycle hooks
onMounted(async () => {
  if (!route.query.tab) {
    router.replace({
      path: '/notifications',
      query: { tab: 'all' }
    })
  }
  await fetchNotifications()
})

watch(() => route.query.tab, (newTab) => {
  if (newTab && newTab !== activeTab.value) {
    activeTab.value = newTab
    currentPage.value = 1
    fetchNotifications()
  }
})
</script>
<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.2s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>

<style scoped>
/* Custom scrollbar */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 3px;
}

.dark ::-webkit-scrollbar-thumb {
  background: #4b5563;
}

/* Smooth transitions */
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from,
.notification-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* Highlight pulse for new notifications */
@keyframes pulse {
  0% {
    opacity: 0.6;
  }

  50% {
    opacity: 1;
  }

  100% {
    opacity: 0.6;
  }
}

.highlight-pulse {
  animation: pulse 2s infinite;
}
</style>