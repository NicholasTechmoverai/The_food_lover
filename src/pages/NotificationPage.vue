<template>
  <div class="flex flex-col md:flex-row min-h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Vertical Navigation -->
    <div class="w-full md:w-64 bg-white dark:bg-gray-800 border-b md:border-b-0 md:border-r border-gray-200 dark:border-gray-700 flex-shrink-0">
      <div class="p-4 flex items-center space-x-3 md:block md:space-x-0 md:space-y-4">
        <!-- Navigation Tabs -->
        <nav class="flex md:block space-x-4 md:space-x-0 md:space-y-1 overflow-x-auto scrollbar-hide md:mt-6">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="activateTab(tab)"
            :class="{
              'bg-[var(--theme-color)]/10 text-[var(--theme-color)]': activeTab === tab.id,
              'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700': activeTab !== tab.id
            }"
            class="px-3 py-2 rounded-lg md:rounded-none md:rounded-r-lg text-sm font-medium flex items-center transition-colors whitespace-nowrap"
          >
            <i :class="tab.icon" class="mr-2"></i>
            <span>{{ tab.label }}</span>
            <span 
              v-if="tab.badgeCount > 0"
              class="ml-auto bg-[var(--theme-color)] text-white text-xs px-2 py-0.5 rounded-full"
            >
              {{ tab.badgeCount }}
            </span>
          </button>
        </nav>
      </div>
    </div>

    <!-- Main Content -->
    <div class="flex-1 overflow-hidden">
      <!-- Header -->
      <div class="sticky top-0 z-10 bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm p-4 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
        <h1 class="text-xl font-bold text-gray-900 dark:text-white">
          <i :class="activeTabIcon" class="mr-2"></i>
          {{ activeTabLabel }}
        </h1>
        <div class="flex space-x-2">
          <button 
            @click="markAllAsRead"
            class="p-2 text-gray-500 dark:text-gray-400 hover:text-[var(--theme-color)] dark:hover:text-[var(--theme-color)] transition-colors"
            title="Mark all as read"
            v-if="unreadCount > 0"
          >
            <i class="pi pi-check-circle"></i>
          </button>
          <button 
            @click="fetchNotifications"
            class="p-2 text-gray-500 dark:text-gray-400 hover:text-[var(--theme-color)] dark:hover:text-[var(--theme-color)] transition-colors"
            title="Refresh"
          >
            <i class="pi pi-refresh" :class="{ 'animate-spin': loading }"></i>
          </button>
        </div>
      </div>

      <!-- Notification Content -->
      <div class="h-[calc(100vh-64px)] overflow-y-auto p-4">
        <template v-if="!loading">
          <!-- Grouped Notifications -->
          <div v-if="groupedNotifications.length > 0" class="space-y-4">
            <div 
              v-for="group in groupedNotifications" 
              :key="group.id" 
              class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 overflow-hidden"
              :class="{
                'ring-1 ring-[var(--theme-color)]/30': group.hasUnread,
                'hover:shadow-md transition-shadow duration-200': true
              }"
            >
              <!-- Group Header -->
              <div 
                class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center cursor-pointer"
                :class="{
                  'bg-gray-50 dark:bg-gray-700/50': !group.hasUnread,
                  'bg-blue-50/50 dark:bg-blue-900/20': group.hasUnread
                }"
                @click="toggleGroup(group.id)"
              >
                <div class="flex-shrink-0 relative">
                  <img 
                    :src="group.avatar" 
                    class="w-10 h-10 rounded-full object-cover"
                    :alt="`${group.actor}'s avatar`"
                  >
                  <div v-if="group.multipleActors" class="absolute -bottom-1 -right-1 bg-white dark:bg-gray-800 p-0.5 rounded-full">
                    <div class="bg-[var(--theme-color)]/10 text-[var(--theme-color)] text-xs px-1 rounded-full">
                      +{{ group.actorCount - 1 }}
                    </div>
                  </div>
                </div>
                <div class="ml-3 flex-1 min-w-0">
                  <h3 class="font-medium text-gray-900 dark:text-white">
                    <span v-if="group.multipleActors">{{ group.actorCount }} people</span>
                    <span v-else>{{ group.actor }}</span>
                    {{ group.action }}
                    <span v-if="group.target" class="font-medium text-[var(--theme-color)]">{{ group.target }}</span>
                  </h3>
                  <div class="flex items-center mt-1">
                    <p class="text-xs text-gray-500 dark:text-gray-400">
                      {{ formatDate(group.latestDate) }}
                    </p>
                    <span 
                      v-if="group.notifications.length > 1"
                      class="ml-2 text-xs px-1.5 py-0.5 rounded bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300"
                    >
                      {{ group.notifications.length }} events
                    </span>
                  </div>
                </div>
                <button 
                  @click.stop="toggleGroup(group.id)"
                  class="ml-2 text-gray-400 hover:text-gray-500 dark:hover:text-gray-300 transition-colors p-1"
                >
                  <i :class="isGroupExpanded(group.id) ? 'pi pi-chevron-down' : 'pi pi-chevron-right'"></i>
                </button>
              </div>

              <!-- Grouped Notifications (collapsible) -->
              <transition
                enter-active-class="transition duration-100 ease-out"
                enter-from-class="transform opacity-0"
                enter-to-class="transform opacity-100"
                leave-active-class="transition duration-75 ease-in"
                leave-from-class="transform opacity-100"
                leave-to-class="transform opacity-0"
              >
                <div v-show="isGroupExpanded(group.id)" class="divide-y divide-gray-200 dark:divide-gray-700">
                  <div 
                    v-for="notification in group.notifications"
                    :key="notification.id"
                    :class="{
                      'bg-blue-50/50 dark:bg-blue-900/10': !notification.read,
                      'hover:bg-gray-50 dark:hover:bg-gray-700/50': true
                    }"
                    class="px-4 py-3 transition-colors duration-150 flex items-start"
                  >
                    <div class="flex-shrink-0 mt-1">
                      <div :class="getNotificationIconClass(notification.type)" class="w-8 h-8 rounded-full flex items-center justify-center">
                        <i :class="getNotificationIcon(notification.type)" class="text-sm"></i>
                      </div>
                    </div>
                    <div class="ml-3 flex-1 min-w-0">
                      <p class="text-sm text-gray-800 dark:text-gray-200">
                        <span class="font-medium">{{ notification.actor }}</span> {{ notification.action }}
                        <span v-if="notification.target" class="font-medium text-[var(--theme-color)]">{{ notification.target }}</span>
                      </p>
                      <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                        {{ formatTime(notification.created_at) }}
                      </p>
                      <div v-if="notification.preview" class="mt-2 text-sm text-gray-600 dark:text-gray-300 bg-gray-100 dark:bg-gray-700/30 p-2 rounded">
                        {{ notification.preview }}
                      </div>
                      <div v-if="notification.actions" class="mt-2 flex space-x-2">
                        <button
                          v-for="action in notification.actions"
                          :key="action.label"
                          @click.stop="handleAction(notification, action)"
                          class="text-xs px-2 py-1 rounded border border-gray-200 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                        >
                          {{ action.label }}
                        </button>
                      </div>
                    </div>
                    <div class="flex flex-col items-center gap-2 ml-2">
                      <button 
                        @click.stop="toggleReadStatus(notification)"
                        class="text-gray-400 hover:text-[var(--theme-color)] dark:hover:text-[var(--theme-color)] transition-colors p-1"
                        :title="notification.read ? 'Mark as unread' : 'Mark as read'"
                      >
                        <i :class="notification.read ? 'pi pi-eye-slash text-xs' : 'pi pi-check text-xs'"></i>
                      </button>
                    </div>
                  </div>
                </div>
              </transition>
            </div>
          </div>

          <!-- Empty State -->
          <div v-else class="h-full flex flex-col items-center justify-center text-center py-12">
            <div class="w-48 h-48 bg-gradient-to-br from-[var(--theme-color)]/5 to-transparent rounded-full flex items-center justify-center mb-6">
              <i :class="activeTabIcon" class="text-5xl text-[var(--theme-color)] opacity-70"></i>
            </div>
            <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">
              {{ emptyState.title }}
            </h3>
            <p class="text-gray-500 dark:text-gray-400 mb-6 max-w-md mx-auto">
              {{ emptyState.description }}
            </p>
            <button 
              @click="fetchNotifications"
              class="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-[var(--theme-color)] hover:bg-[var(--theme-color)]/90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--theme-color)] transition-all"
            >
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
  </div>
</template>

<script setup>
import { ref, computed, onMounted,watch } from 'vue'
import { format, formatDistanceToNow, isToday, isYesterday, parseISO } from 'date-fns'
import { useAuthStore } from '../store/user'
import router from '../router'
import { useRoute } from 'vue-router';

const route = useRoute();
const props = defineProps({
  userTheme: {
    type: String,
    default: '#f97316'
  }
})

// Stores
const userStore = useAuthStore()

// Reactive state
const activeTab = ref(route.query.tab || 'all');
const loading = ref(true)
const notifications = ref([])
const expandedGroups = ref([])

// Tabs configuration
const tabs = computed(() => [
  { id: 'all', label: 'All Notifications', icon: 'pi pi-bell', badgeCount: unreadCount.value },
  { id: 'mentions', label: 'Mentions', icon: 'pi pi-at', badgeCount: notifications.value.filter(n => n.type === 'mention' && !n.read).length },
  { id: 'follows', label: 'Followers', icon: 'pi pi-users', badgeCount: notifications.value.filter(n => n.type === 'follow' && !n.read).length },
  { id: 'likes', label: 'Likes', icon: 'pi pi-heart', badgeCount: notifications.value.filter(n => n.type === 'like' && !n.read).length },
  { id: 'comments', label: 'Comments', icon: 'pi pi-comments', badgeCount: notifications.value.filter(n => n.type === 'comment' && !n.read).length },
  { id: 'system', label: 'System', icon: 'pi pi-cog', badgeCount: notifications.value.filter(n => n.type === 'system' && !n.read).length }
])

const activateTab = (tab) => {
  if (activeTab.value === tab.id) return; // Avoid unnecessary push
  activeTab.value= tab.id
  router.push({
    path: "/notifications",
    query: { tab: tab.id },
  });
};

onMounted(() => {
  if (!route.query.tab) {
    router.replace({
      path: '/notifications',
      query: { tab: 'all' }
    });
  }
});




const activeTabLabel = computed(() => {
  return tabs.value.find(tab => tab.id === activeTab.value)?.label || ''
})

const activeTabIcon = computed(() => {
  return tabs.value.find(tab => tab.id === activeTab.value)?.icon || 'pi pi-bell'
})

const unreadCount = computed(() => {
  return notifications.value.filter(n => !n.read).length
})

// Enhanced notification grouping
const groupedNotifications = computed(() => {
  const groups = {}
  const filteredNotifications = notifications.value.filter(n => 
    activeTab.value === 'all' || n.type === activeTab.value
  )
  
  filteredNotifications.forEach(notification => {
    // Create a more intelligent grouping key
    const groupKey = notification.contextId || `${notification.type}-${notification.target || notification.actor}`
    
    if (!groups[groupKey]) {
      groups[groupKey] = {
        id: groupKey,
        title: notification.groupTitle || getDefaultGroupTitle(notification),
        avatar: notification.avatar || getDefaultAvatar(notification),
        actor: notification.actor,
        actorCount: 1,
        multipleActors: false,
        action: notification.action,
        target: notification.target,
        type: notification.type,
        notifications: [],
        latestDate: notification.created_at,
        hasUnread: false
      }
    }
    
    // Check if this is a new actor for this group
    if (!groups[groupKey].notifications.some(n => n.actor === notification.actor)) {
      if (groups[groupKey].actorCount >= 1) {
        groups[groupKey].multipleActors = true
      }
      groups[groupKey].actorCount++
    }
    
    groups[groupKey].notifications.push(notification)
    
    // Update latest date
    if (new Date(notification.created_at) > new Date(groups[groupKey].latestDate)) {
      groups[groupKey].latestDate = notification.created_at
    }
    
    // Update read status
    if (!notification.read) {
      groups[groupKey].hasUnread = true
    }
  })
  
  // Convert to array and sort
  return Object.values(groups)
    .sort((a, b) => {
      // Sort unread groups first
      if (a.hasUnread !== b.hasUnread) {
        return a.hasUnread ? -1 : 1
      }
      // Then by date
      return new Date(b.latestDate) - new Date(a.latestDate)
    })
    .map(group => {
      // Sort notifications within each group
      group.notifications.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      return group
    })
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

// Fetch notifications
const fetchNotifications = async () => {
  try {
    loading.value = true
    const response = await mockApiGetNotifications()
    notifications.value = response.data
    expandedGroups.value = [] // Reset expanded groups
  } catch (error) {
    console.error('Error fetching notifications:', error)
  } finally {
    loading.value = false
  }
}

// Notification type handling
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

const getDefaultGroupTitle = (notification) => {
  const titles = {
    like: `Likes for "${notification.target}"`,
    comment: `Comments on "${notification.target}"`,
    mention: `Mentions from ${notification.actor}`,
    follow: `New followers`,
    system: `System notifications`
  }
  return titles[notification.type] || `${notification.actor}'s ${notification.type}`
}

const getDefaultAvatar = (notification) => {
  if (notification.type === 'system') {
    return 'https://cdn-icons-png.flaticon.com/512/149/149071.png'
  }
  return `https://ui-avatars.com/api/?name=${encodeURIComponent(notification.actor)}&background=random`
}


// Enhanced date formatting
const formatDate = (dateString) => {
  const date = parseISO(dateString)
  if (isToday(date)) {
    return format(date, 'h:mm a')
  } else if (isYesterday(date)) {
    return 'Yesterday'
  }
  return formatDistanceToNow(date, { addSuffix: true })
}

const formatTime = (dateString) => {
  return format(parseISO(dateString), 'h:mm a')
}

// Group management
const isGroupExpanded = (groupId) => {
  return expandedGroups.value.includes(groupId)
}

const toggleGroup = (groupId) => {
  if (isGroupExpanded(groupId)) {
    expandedGroups.value = expandedGroups.value.filter(id => id !== groupId)
  } else {
    expandedGroups.value.push(groupId)
    // Mark as read when expanded
    const group = groupedNotifications.value.find(g => g.id === groupId)
    if (group && group.hasUnread) {
      group.notifications.forEach(n => { n.read = true })
      group.hasUnread = false
    }
  }
}

// Notification actions
const toggleReadStatus = (notification) => {
  notification.read = !notification.read
  // API call would go here
}

const markAllAsRead = () => {
  notifications.value.forEach(n => { n.read = true })
  // API call would go here
}

const handleAction = (notification, action) => {
  console.log('Action:', action.label, 'on notification:', notification.id)
  // Handle specific actions (reply, view, etc.)
  if (action.label === 'View') {
    // Navigate to the relevant content
  }
}

// Enhanced mock data with better grouping examples
const mockApiGetNotifications = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        data: [
          {
            id: 1,
            type: 'like',
            actor: 'John Doe',
            avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
            action: 'liked your recipe',
            target: 'Spaghetti Carbonara',
            contextId: 'recipe-123',
            created_at: new Date(Date.now() - 1000 * 60 * 5).toISOString(),
            read: false,
            actions: [
              { label: 'View', action: 'view' }
            ]
          },
          {
            id: 2,
            type: 'like',
            actor: 'Sarah Smith',
            avatar: 'https://randomuser.me/api/portraits/women/44.jpg',
            action: 'liked your recipe',
            target: 'Spaghetti Carbonara',
            contextId: 'recipe-123',
            created_at: new Date(Date.now() - 1000 * 60 * 15).toISOString(),
            read: false
          },
          {
            id: 3,
            type: 'like',
            actor: 'Michael Chen',
            avatar: 'https://randomuser.me/api/portraits/men/22.jpg',
            action: 'liked your recipe',
            target: 'Spaghetti Carbonara',
            contextId: 'recipe-123',
            created_at: new Date(Date.now() - 1000 * 60 * 30).toISOString(),
            read: true
          },
          {
            id: 4,
            type: 'comment',
            actor: 'Emma Wilson',
            avatar: 'https://randomuser.me/api/portraits/women/68.jpg',
            action: 'commented on your post',
            target: 'Knife Skills 101',
            contextId: 'post-456',
            created_at: new Date(Date.now() - 1000 * 60 * 60 * 2).toISOString(),
            read: false,
            preview: 'Great tutorial! Do you have any recommendations for beginner knives?',
            actions: [
              { label: 'Reply', action: 'reply' },
              { label: 'View', action: 'view' }
            ]
          },
          {
            id: 5,
            type: 'comment',
            actor: 'David Kim',
            avatar: 'https://randomuser.me/api/portraits/men/75.jpg',
            action: 'replied to your comment',
            target: 'Knife Skills 101',
            contextId: 'post-456',
            created_at: new Date(Date.now() - 1000 * 60 * 60 * 3).toISOString(),
            read: false,
            preview: 'I found this brand works really well for beginners'
          },
          {
            id: 6,
            type: 'follow',
            actor: 'Lisa Ray',
            avatar: 'https://randomuser.me/api/portraits/women/63.jpg',
            action: 'started following you',
            created_at: new Date(Date.now() - 1000 * 60 * 60 * 24).toISOString(),
            read: false,
            actions: [
              { label: 'Follow back', action: 'follow' },
              { label: 'View profile', action: 'view' }
            ]
          },
          {
            id: 7,
            type: 'system',
            actor: 'System',
            action: 'Your recipe was featured',
            target: 'Perfect Pasta Al Dente',
            created_at: new Date(Date.now() - 1000 * 60 * 60 * 48).toISOString(),
            read: false,
            actions: [
              { label: 'View', action: 'view' },
              { label: 'Share', action: 'share' }
            ]
          }
        ]
      })
    }, 800)
  })
}

// Lifecycle hooks
onMounted(() => {
  fetchNotifications()
  // Auto-expand groups with unread notifications
  setTimeout(() => {
    expandedGroups.value = groupedNotifications.value
      .filter(group => group.hasUnread)
      .map(group => group.id)
  }, 1000)
})
</script>

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
  0% { opacity: 0.6; }
  50% { opacity: 1; }
  100% { opacity: 0.6; }
}
.highlight-pulse {
  animation: pulse 2s infinite;
}
</style>