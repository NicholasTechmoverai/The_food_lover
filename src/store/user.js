import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  // Core state
  const user = ref(null)
  const token = ref(null)
  const authData = ref(null) // Optional: extra auth metadata

  // Derived state
  const isAuthenticated = computed(() => !!token.value)

  // Actions
  const setUser = (u) => {
    if (u && !u.profilePic) {
      u.profilePic = 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png'
    }
    user.value = u
  }


  const setToken = (t) => {
    token.value = t
  }

  const setAuthData = (data) => {
    authData.value = data
  }

  const logout = () => {
    user.value = null
    token.value = null
    authData.value = null
  }

  return {
    user,
    token,
    authData,
    isAuthenticated,
    setUser,
    setToken,
    setAuthData,
    logout
  }
}, {
  persist: {
    key: 'auth-store',
    storage: localStorage,
    afterRestore: () => {
      const maxAge = 7 * 24 * 60 * 60 * 1000 // 7 days
      const savedAt = localStorage.getItem('auth-store-timestamp')
      if (savedAt && Date.now() - parseInt(savedAt) > maxAge) {
        localStorage.removeItem('pinia-auth')
        localStorage.removeItem('auth-store-timestamp')
      }
    },
    beforeRestore: () => {
      if (!localStorage.getItem('auth-store-timestamp')) {
        localStorage.setItem('auth-store-timestamp', Date.now().toString())
      }
    }
  }
})



export const useNotificationStore = defineStore('noty', () => {
  // State
  const liveNotifications = ref(null)

  const notificationsCount = ref({
    likes: 0,
    comment: 0,
    mentions: 0,
    follows: 0,
    system: 0,
    all: 0,
  })

  // Actions
  const setLiveNotifications = (notifications) => {
    if(!notifications)return
    liveNotifications.value = [...notifications]
  }

  const setNotificationsCount = (count) => {
    notificationsCount.value = count
  }

  const clearLiveNotifications = () => {
    liveNotifications.value = null
  }

  return {
    liveNotifications,
    notificationsCount,
    setLiveNotifications,
    setNotificationsCount,
    clearLiveNotifications,
  }
})
