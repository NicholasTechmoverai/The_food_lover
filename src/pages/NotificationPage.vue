<template>
  <div :style="{ '--theme-color': auth.user?.theme || '#f97316' }"
    class="flex flex-col md:flex-row min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Vertical Navigation -->
    <div
      class="w-full md:w-64 bg-white dark:bg-gray-800 border-b md:border-b-0 md:border-r border-gray-200 dark:border-gray-700 flex-shrink-0">
      <div class="p-4 flex items-center space-x-3 md:block md:space-x-0 md:space-y-4">

        <!-- Navigation Tabs -->
        <nav
          class="flex w-full md:w-auto flex-row md:flex-col space-x-4 md:space-x-0 md:space-y-1 overflow-x-auto md:overflow-x-visible scrollbar-hide">
          <Button v-for="tab in tabs" :key="tab.id" @click="activateTab(tab)"
            :severity="activeTab === tab.id ? 'info' : 'secondary'" text
            class="flex-shrink-0 md:w-full justify-start !py-3 min-w-[140px] md:min-w-0" :class="{
              '!bg-[var(--theme-color)]/10 !text-[var(--theme-color)]': activeTab === tab.id,
              '!text-gray-700 dark:!text-gray-300': activeTab !== tab.id
            }">
            <i :class="tab.icon" class="mr-2"></i>
            <span>{{ tab.label }}</span>
            <Badge v-if="tab.badgeCount > 0" :value="tab.badgeCount" class="ml-auto"
              :style="{ backgroundColor: auth.user?.theme || '#f97316' }" />
          </Button>
        </nav>


        <!-- Notification Settings -->
        <div class="hidden md:block mt-8 pt-4 border-t border-gray-200 dark:border-gray-700">
          <Button @click="openSettings" icon="pi pi-cog" label="Notification Settings" text
            class="w-full justify-start !py-3 !text-gray-700 dark:!text-gray-300" />
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 overflow-hidden">
      <!-- Header -->
      <div
        class="sticky top-0 z-10 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm p-2 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
        <div class="flex items-center">
          <h1 class="text-xl font-bold text-gray-900 dark:text-white">
            <i :class="activeTabIcon" class="mr-2"></i>
            {{ activeTabLabel }}
          </h1>
          <Tag v-if="notifications.length > 0" :value="notifications.length" class="ml-2"
            :style="{ backgroundColor: auth.user?.theme || '#f97316' }" />
        </div>
        <div class="flex space-x-2">
          <Button v-if="unreadCount > 0" @click="markAllAsRead" icon="pi pi-check-circle" text rounded
            severity="secondary" v-tooltip="'Mark all as read'" />
          <Button @click="fetchNotifications()" icon="pi pi-refresh" text rounded severity="secondary"
            :loading="loading" v-tooltip="'Refresh'" />
        </div>
      </div>

      <!-- Notification Content -->
      <div class="h-[calc(100vh-64px)] overflow-y-auto p-0">
        <template v-if="!loading">
          <!-- Notifications List -->
          <div v-if="notifications.length > 0" class="space-y-1">
            <Card v-for="notification in notifications" :key="notification.id"
              class="cursor-pointer group " :class="{
                'border-l-4 border-r-2 border-[var(--theme-color)]': !notification.read,
                'hover:shadow-md transition-shadow duration-200': true
              }" @click="toggleReadStatus(notification)">
              <template #content>
                <div class="flex items-start">
                  <!-- Actor Avatar -->
                  <div class="flex-shrink-0 relative">
                    <router-link :to="`/${notification.actor?.username}`">
                      <Avatar v-if="notification.actor?.avatar" :image="notification.actor.avatar" shape="circle"
                        size="large" />
                      <Avatar v-else :label="notification.actor?.username?.charAt(0) || 'S'" shape="circle" size="large"
                        :class="getNotificationIconClass(notification.type)" />
                    </router-link>
                    <div v-if="notification.count > 1"
                      class="absolute -bottom-1 -right-1 bg-[var(--theme-color)] text-white rounded-full w-5 h-5 flex items-center justify-center text-xs font-bold">
                      {{ notification.count > 9 ? '9+' : notification.count }}
                    </div>
                  </div>

                  <div class="ml-3 flex-1 min-w-0">
                    <!-- Notification Content -->
                    <div class="text-sm">
                      <router-link :to="`/${notification.actor?.username}`">
                        <span class="font-medium">{{ notification.actor?.username || 'System' }}</span>
                      </router-link>
                      {{ notification.verb }}
                      <span v-if="notification.target" class="font-medium text-[var(--theme-color)]">
                        {{ notification.target.type }}
                      </span>
                    </div>

                    <!-- Timestamp -->
                    <div class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                      {{ formatDistanceToNow(notification.created_at) }}
                    </div>

                    <!-- Preview Text -->
                    <div v-if="notification.preview" @click="toTarget(notification)"
                      class="cursor-pointer flex flex-row justify-between items-center mt-2 text-sm text-gray-600 dark:text-gray-300 bg-gray-100 dark:bg-gray-700/30 p-2 rounded">
                      <div class="truncate">{{ notification.preview }}</div>
                      <!-- Target Image (if available) -->
                      <Avatar v-if="notification.target?.image" :image="notification.target.image" shape="square"
                        size="large" class="ml-2" />
                    </div>
                  </div>

                  <!-- Unread indicator -->
                  <div v-if="!notification.read"
                    class="w-2 h-2 rounded-full bg-[var(--theme-color)] ml-2 flex-shrink-0"></div>

                  <!-- Notification Controls -->
                  <div
                    class="flex flex-col items-center gap-2 ml-2 opacity-0 group-hover:opacity-100 group-active:opacity-100 transition-opacity">
                    <Button @click.stop="deleteNotification(notification)" icon="pi pi-trash" text rounded
                      severity="danger"  />
                  </div>
                </div>
              </template>
            </Card>

            <!-- Infinite loading indicator -->
            <div v-if="hasMoreNotifications" class="flex justify-center py-4">
              <Button @click="loadMore" :disabled="loadingMore" :label="loadingMore ? 'Loading...' : 'Load more'"
                icon="pi pi-chevron-down" text :loading="loadingMore" />
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
            <Button @click="fetchNotifications()" icon="pi pi-refresh" label="Refresh"
              :style="{ backgroundColor: auth.user?.theme || '#f97316' }" />
          </div>
        </template>

        <!-- Loading State -->
        <div v-else class="h-full flex flex-col items-center justify-center">
          <ProgressSpinner style="width: 50px; height: 50px" strokeWidth="4" :stroke="auth.user?.theme || '#f97316'"
            fill="transparent" animationDuration=".5s" class="mb-4" />
          <p class="text-gray-500 dark:text-gray-400">Loading notifications...</p>
        </div>
      </div>
    </div>

    <!-- Settings Dialog -->
    <Dialog v-model:visible="showSettings" header="Notification Settings" :style="{ width: '450px' }" :modal="true"
      :dismissableMask="true">
      <div v-if="loadingSettings">
        <p>loading settings...</p>
      </div>
      <div v-else class="space-y-4">
        <div class="flex items-center justify-between">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Email Notifications</label>
          <ToggleSwitch v-model="settings.email_notifications">
            <template #handle="{ checked }">
              <i :class="['!text-xs pi', { 'pi-check': checked, 'pi-times': !checked }]" />
            </template>
          </ToggleSwitch>
        </div>
        <div class="flex items-center justify-between">
          <label class="text-sm font-medium text-gray-700 dark:text-gray-300">Push Notifications</label>
          <ToggleSwitch v-model="settings.push_notifications ">
            <template #handle="{ checked }">
              <i :class="['!text-xs pi', { 'pi-check': checked, 'pi-times': !checked }]" />
            </template>
          </ToggleSwitch>
        </div>
        <div class="border-t border-gray-200 dark:border-gray-700 pt-4">
          <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Notification Types</h4>
          <div class="space-y-2">
            <div v-for="type in notificationTypes" :key="type.id" class="flex items-center">
              <Checkbox :id="`notification-type-${type.id}`" v-model="settings.notificationTypes[type.id]"
                :value="type.id" :binary="true" />
              <label :for="`notification-type-${type.id}`" class="ml-2 text-sm text-gray-700 dark:text-gray-300">
                {{ type.label }}
              </label>
            </div>
          </div>
        </div>
      </div>


      <template #footer>
        <Button @click="closeSettings" label="Cancel" text class="mr-2" />
        <Button v-if="!loadingSettings" @click="saveSettings" label="Save Settings"
          :style="{ backgroundColor: auth.user?.theme || '#f97316' }" />
      </template>
    </Dialog>
  </div>
</template>



<style scoped>
/* Custom scrollbar with theme color */
.dark ::-webkit-scrollbar-thumb {
  background-color: var(--theme-color);
  opacity: 0.3;
  border-radius: 3px;
}

/* Enhanced hover effects for notifications */
.card:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
}

/* Pulse animation for unread notifications */
@keyframes pulse {

  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0.6;
  }
}

/* .ring-[var(--theme-color)] {
  animation: pulse 2s infinite;
} */
</style>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { format } from 'date-fns'
import { useAuthStore,useNotificationStore } from '../store/user'
import router from '../router'
import { useRoute } from 'vue-router'
import { make_a_delete, make_a_post } from '../apis'
import { useToast } from 'primevue/usetoast'
import { formatDistanceToNow } from 'date-fns'

const toast = useToast()
const route = useRoute()
const props = defineProps({
  userTheme: {
    type: String,
    default: '#f97316'
  }
})

// Stores
const auth = useAuthStore()
const live_notification = useNotificationStore()

// Reactive state
const activeTab = ref(route.query.tab || 'all')
const loading = ref(true)
const loadingSettings = ref(false)
const loadingMore = ref(false)
const notifications = ref([])
const showSettings = ref(false)
const currentPage = ref(1)
const hasMoreNotifications = ref(true)


watch(
  () => live_notification.liveNotifications,
  (newVal) => {
    if (Array.isArray(newVal) && newVal.length > 0) {
      const newUnique = newVal.filter(
        (n) => !notifications.value.some((existing) => existing.id === n.id)
      )

      notifications.value = [...newUnique, ...notifications.value]

      live_notification.clearLiveNotifications()
    }
  },
  { deep: true, immediate: true }
)


// Settings
const settings = ref({
  email_notifications: true,
  push_notifications : true,
  notificationTypes: { like: true, comment: true, mention: true, follow: true, system: true }
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
  { id: 'all', label: 'All ', icon: 'pi pi-bell', badgeCount: live_notification.notificationsCount.all },
  { id: 'mentions', label: 'Mentions', icon: 'pi pi-at', badgeCount: live_notification.notificationsCount.mentions },
  { id: 'follows', label: 'Followers', icon: 'pi pi-users', badgeCount: live_notification.notificationsCount.follows },
  { id: 'likes', label: 'Likes', icon: 'pi pi-heart', badgeCount: live_notification.notificationsCount.likes },
  { id: 'comments', label: 'Comments', icon: 'pi pi-comments', badgeCount: live_notification.notificationsCount.comment },
  { id: 'system', label: 'System', icon: 'pi pi-cog', badgeCount: live_notification.notificationsCount.system }
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
        [activeTab.value]: true,
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
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to load notifications',
      life: 3000
    })
  } finally {
    loading.value = false
    loadingMore.value = false
    await getNotificationsCount()
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
  const colors = {
    like: 'bg-[var(--theme-color)]/10 text-[var(--theme-color)]',
    comment: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-300',
    mention: 'bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-300',
    follow: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-300',
    system: 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300'
  }
  return colors[type] || 'bg-[var(--theme-color)]/10 text-[var(--theme-color)]'
}


const formatTime = (dateString) => {
  return format(new Date(dateString), 'h:mm a')
}

const toggleReadStatus = async (notification) => {
  try {
    await make_a_post(
      `/notifications/${notification.id}/read`,
      auth.token,
      { read: true }
    )
    notification.read = true
    await getNotificationsCount()
  } catch (error) {
    console.error('Error updating read status:', error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to update notification status',
      life: 3000
    })
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
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'All notifications marked as read',
      life: 3000
    })
    await getNotificationsCount()
  } catch (error) {
    console.error('Error marking all as read:', error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to mark all as read',
      life: 3000
    })
  }
}
const getNotificationsCount = async () => {
  try {
    const res = await make_a_post(
      `/notifications/${auth.user.name}/counts`,
      auth.token, {}
    )

    if (res.data) {
      live_notification.notificationsCount = res.data
    }
  } catch (error) {
    console.error('Error Getting Notifications:', error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to Get notifications Counts',
      life: 3000
    })
  }

}


const getNotificationsSettings = async () => {
  loadingSettings.value = true
  try {
    const res = await make_a_post(
      `/notifications/settings/get`,
      auth.token, {}
    )

    if(res.data){
      settings.value = res.data
    }
  } catch (error) {
    console.error('Error Getting SEttings:', error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to Get notification settings',
      life: 3000
    })
  }
    loadingSettings.value = false

}
const deleteNotification = async (notification) => {
  try {
    await make_a_delete(
      `/notifications/${notification.id}/delete`,
      auth.token, {}
    )
    notifications.value = notifications.value.filter(n => n.id !== notification.id)
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Notification deleted',
      life: 3000
    })
        await getNotificationsCount()
  } catch (error) {
    console.error('Error deleting notification:', error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to delete notification',
      life: 3000
    })
  }
}

const toTarget = (notification) => {
  if (notification.url) {
    router.push(notification.url)
  }
}

const openSettings = () => {
  showSettings.value = true
  getNotificationsSettings()
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
    toast.add({
      severity: 'success',
      summary: 'Success',
      detail: 'Settings saved successfully',
      life: 3000
    })
  } catch (error) {
    console.error('Error saving settings:', error)
    toast.add({
      severity: 'error',
      summary: 'Error',
      detail: 'Failed to save settings',
      life: 3000
    })
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
/* Custom scrollbar for dark mode */
.dark ::-webkit-scrollbar {
  width: 6px;
}

.dark ::-webkit-scrollbar-track {
  background: #374151;
}

.dark ::-webkit-scrollbar-thumb {
  background: #4b5563;
  border-radius: 3px;
}

.dark ::-webkit-scrollbar-thumb:hover {
  background: #6b7280;
}

/* Smooth transitions */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.p-card{
  border-radius: 0;
    background-color: transparent !important;

}
</style>