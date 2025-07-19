<script setup>
import Menubar from './components/menubar.vue'
import Footer from './pages/MainFooter.vue'
import { applyTheme } from './reusables'
import { onMounted, ref, computed, onBeforeUnmount, watch } from 'vue'
import { useControl } from './store/control.js'
import { useConfirm } from 'primevue/useconfirm'
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from './store/user.js'
import { initializeSession, isTokenExpired, send_verify } from './apis/auth.js'
import { useRoute } from 'vue-router'
import ClockLoad from './loaders/ClockLoad.vue'
import BusyFingersLoader from './loaders/BusyFingersLoader.vue'
import { notificationsSocket, usersSocket } from './a_websocket/index.js'


const auth = useAuthStore()
const control = useControl()
const confirm = useConfirm()
const toast = useToast()

const blocked = ref(false)
const route = useRoute()

let tokenInterval
let themeMediaQuery

// List of routes where user must be verified
const protectedRoutes = [
  'RecipesPage', 'RecipeType', 'RecipeId',
  'NewRecipe', 'CoverInfo', 'NewRecipeUploadsBase', 'NewRecipeUploadsWithId',
  'PublishRecipe', 'PublishRecipeWithId',
  'LivePage', 'LiveIdPage',
  'CookingTipsPage', 'CookingTipCard',
  'SettingsPage', 'PreferenceSettings', 'AdminSettings'
]

const isProtected = computed(() => protectedRoutes.includes(route.name))

// --- Refresh token ---
const refreshToken = async () => {
  try {
    const res = await initializeSession(auth.token, auth.user.id)
    if (res?.success && res.data) {
      auth.setUser(res.data.user)
      auth.setToken({
        token: res.data.access_token,
        expires_in: res.data.expires_in
      })
      return true
    }
    return false
  } catch (error) {
    console.error('Token refresh error:', error)
    return false
  }
}

// --- User verification check ---
const checkUserVerification = async () => {
  try {
    if (!isProtected.value || !auth.user) {
      blocked.value = false
      return
    }

    if (!auth.user.isVerified) {
      blocked.value = true

      const sendResult = await send_verify(null, 'link', 'email', auth.user.id)
      if (!sendResult?.success) {
        toast.add({
          severity: 'warn',
          summary: 'Verification Issue',
          detail: 'Could not send verification email.',
          group: 'bl',
          life: 5000
        })
      }

      confirm.require({
        group: 'headless',
        header: 'Verify Account',
        message: 'A verification link has been sent to your email. Please verify your account.',
        icon: 'pi pi-envelope',
        rejectProps: {
          label: 'OK',
          icon: 'pi pi-check',
          size: 'small',
          severity: 'primary'
        },
        acceptProps: {
          label: 'Resend Link',
          icon: 'pi pi-refresh',
          size: 'small',
          severity: 'secondary'
        },
        reject: () => {
          toast.add({
            severity: 'info',
            summary: 'Awaiting Verification',
            detail: 'Check your email for the verification link.',
            group: 'bl'
          })
        },
        accept: async () => {
          toast.add({
            severity: 'info',
            summary: 'Awaiting Verification',
            detail: 'Check your email for the verification link.',
            group: 'bl'
          })
          const res = await send_verify(null, 'link', 'email', auth.user.id)
          if (res?.success) {
            toast.add({
              severity: 'success',
              summary: 'Resent Successfully',
              detail: 'A new verification link has been sent to your email.',
              group: 'bl',
              life: 5000
            })
          } else {
            toast.add({
              severity: 'error',
              summary: 'Failed to Resend',
              detail: 'Could not send verification email. Please try again later.',
              group: 'bl',
              life: 5000
            })
          }
        }
      })
    } else {
      blocked.value = false
    }
  } catch (error) {
    console.error('Verification check error:', error)
    blocked.value = false
  }
}

// --- Session Expiry Dialog ---
const promptTokenRefresh = () => {
  if (!isProtected.value) return

  confirm.require({
    group: 'headless',
    header: 'Session Check',
    message: 'We noticed some inactivity. Are you still with us?',
    icon: 'pi pi-clock',
    acceptProps: {
      label: 'Yes, I’m here',
      icon: 'pi pi-check',
      size: 'small',
      severity: 'primary'
    },
    accept: async () => {
      const success = await refreshToken()
      toast.add({
        severity: success ? 'success' : 'error',
        summary: success ? 'Session Extended' : 'Session Failed',
        detail: success 
          ? ''
          : 'Unable to extend session. Please try again.',
        life: 3000,
        group: 'bl'
      })
    }
  })
}


// Call this once after login or on app init
const startTokenCheck = () => {
  if (tokenInterval) clearInterval(tokenInterval)

  tokenInterval = setInterval(async () => {
    const token = auth.token

    if (!token) return

    if (isTokenExpired(token)) {
      // If user is active, refresh automatically
      if (document.hasFocus()) {
        const success = await refreshToken()
        if (!success) {
          toast.add({
            severity: 'error',
            summary: 'Session Failed',
            detail: 'Unable to extend session. Please log in again.',
            life: 5000,
            group: 'bl'
          })
          return
        }

      } else {
        // If inactive or blurred, prompt for confirmation
        promptTokenRefresh()
      }
    }
  }, 300000) // every 5 minutes
}


// --- Theme and auth on load ---
onMounted(async () => {
  try {
    const savedTheme = localStorage.getItem('theme') || 'system'
    applyTheme(savedTheme)

    if (savedTheme === 'system') {
      themeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
      const handleTheme = () => applyTheme('system')
      themeMediaQuery.addEventListener('change', handleTheme)
      onBeforeUnmount(() => themeMediaQuery.removeEventListener('change', handleTheme))
    }

    await refreshToken()
    await checkUserVerification()

    startTokenCheck()
    if(auth.user.id){
      usersSocket.emit("join_respective",{user_id:auth.user.id})
      notificationsSocket.emit("join_respective",{user_id:auth.user.id})
    }

  } catch (error) {
    console.error('App init error:', error)
  }
})


notificationsSocket.on("new_notifications", (data) => {
  console.log("New notifications received:", data);

  // Optionally show a toast popup
  // showToast(data.notifications[0]?.action || "You have a new notification!");
});
usersSocket.on("new_notifications", (data) => {
  console.log("New notifications received:", data);
});


// --- Reactively check route changes (e.g. from login to recipes) ---
watch(() => route.name, async () => {
  await checkUserVerification()
})

// --- Cleanup ---
onBeforeUnmount(() => {
  if (tokenInterval) clearInterval(tokenInterval)
})
</script>


<template>
  <ConfirmDialog group="headless">
    <template #container="{ message, acceptCallback, rejectCallback }">
      <div class="flex flex-col items-center p-8 bg-surface-0 dark:bg-surface-900 rounded">
        <div
          class="rounded-full bg-primary text-primary-contrast inline-flex justify-center items-center h-24 w-24 -mt-20">
          <i :class="message.icon" class="!text-4xl"></i>
        </div>
        <span class="font-bold text-2xl block mb-2 mt-6">{{ message.header }}</span>
        <p class="mb-0 text-center px-2">{{ message.message }}</p>
        <div class="flex items-center gap-2 mt-6">
          <Button :label="message.acceptProps.label" :icon="message.acceptProps.icon" @click="acceptCallback"
            class="w-fit" />
          <Button v-if="message.rejectProps" :label="message.rejectProps.label" :icon="message.rejectProps.icon"
            @click="rejectCallback" class="w-fit" />
        </div>

      </div>
    </template>
  </ConfirmDialog>

  <div v-if="blocked" class="fixed top-[30%] left-1/2 -translate-x-1/2 z-[1100] bg-gray-600/100 backdrop-blur-2xl h-[200px] w-fit flex flex-col justify-center items-center rounded-2xl p-3">
    <BusyFingersLoader />
    <p class="mt-10 flex gap-2 flex-row justify-center items-center">Waiting  for acount verification...<span>
        <ClockLoad />
      </span></p>
  </div>

  <BlockUI :blocked="blocked" fullScreen />
  <Toast position="bottom-left" group="bl" />

  <div class="min-h-screen flex flex-col transition-colors duration-300">
    <div v-if="control.showNav" class="sticky top-0 z-400 backdrop-blur-sm">
      <Menubar />
    </div>
    <div class="relative w-full overflow-x-hidden max-w-[2500px] mx-auto">
      <router-view />
    </div>
    <Footer v-if="control.showNav" />
  </div>
</template>
