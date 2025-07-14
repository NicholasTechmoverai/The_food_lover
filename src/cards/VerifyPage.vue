<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-100 dark:bg-gray-900 px-4">
    <div class="max-w-md w-full bg-white dark:bg-gray-800 rounded-lg shadow-md p-6">
      <div class="text-center mb-6">
        <img
          :src="siteConfig.assets.logo"
          :alt="siteConfig.assets.logoAlt"
          class="w-16 h-16 mx-auto mb-3"
        />
        <h2 class="text-2xl font-bold text-gray-800 dark:text-gray-100">Verify Your Account</h2>
        <p class="text-sm text-gray-500 dark:text-gray-400">
          Verifying your email for <strong>{{ type }}</strong> verification.
        </p>
      </div>

      <div class="space-y-4">
        <input
          v-model="code"
          type="text"
          maxlength="6"
          placeholder="Enter 6-digit code"
          class="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-gray-50 dark:bg-gray-700 text-gray-800 dark:text-gray-100 focus:ring-2 focus:ring-blue-500 focus:outline-none"
        />

        <button
          :disabled="!code || loading"
          @click="submitCode"
          class="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white py-3 rounded-lg font-semibold transition-colors"
        >
          <span v-if="loading">
            <i class="pi pi-spin pi-spinner mr-2"></i> Verifying...
          </span>
          <span v-else>Verify</span>
        </button>

        <p v-if="error" class="text-red-500 text-sm text-center">{{ error }}</p>
        <p v-if="success" class="text-green-500 text-sm text-center">✅ Verified successfully!</p>
      </div>

      <div class="mt-6 text-center text-sm text-gray-500 dark:text-gray-400">
        Didn’t get a code?
        <button @click="resendCode" class="text-blue-600 hover:underline ml-1" :disabled="resending">
          {{ resending ? 'Resending...' : 'Resend' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useSiteStore } from '../config/siteConfig'
import { send_verify, verifyCodeAPI } from '../apis/auth' // Your actual API call
import { useToast } from 'primevue/usetoast'
import { useAuthStore } from '../store/user'
const auth = useAuthStore()
const { siteConfig } = useSiteStore()
const route = useRoute()
const router = useRouter()

const code = ref('')
const user_id = ref('')
const codeId = ref('')
const type = ref('')
const loading = ref(false)
const error = ref('')
const success = ref(false)
const resending = ref(false)
const method = ref('')

onMounted(() => {
  code.value = route.query.code || null
  codeId.value = route.query.id || null
  type.value = route.query.type || 'email'
  user_id.value = route.query.u_id || null
  method.value = route.query.method || 'link'
})

const submitCode = async () => {
  error.value = '';
  success.value = false;
  loading.value = true;

  try {
    const res = await verifyCodeAPI(codeId.value, code.value, type.value);

    if (res?.success) {
      success.value = true;

      if (res.data) {
        const { user, access_token, expires_in } = res.data;

        console.log("Verified User:", user);
        auth.setUser(user);
        auth.setToken({ token: access_token, expires_in });

        setTimeout(() => router.push(`/${user.name}`), 2500);
      }
    } else {
      error.value = res.message || 'Invalid or expired verification link.';
    }
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Verification failed. Please try again.';
    console.warn("Verification Error:", e);
  } finally {
    loading.value = false;
  }
};


const resendCode = async () => {
  resending.value = true
    try {
    const res = await send_verify(codeId.value,method.value, type.value,user_id.value);

    if (res?.success) {
      success.value = true;

      if (res.data) {
        const { id,type } = res.data;
        codeId.value = id,
        type.value = type
       
      }
    } else {
      error.value = res.message || 'Invalid or expired verification link.';
    }
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Verification failed. Please try again.';
    console.warn("Verification Error:", e);
  } finally {
    loading.value = false;
  }
  resending.value = false
}
</script>
