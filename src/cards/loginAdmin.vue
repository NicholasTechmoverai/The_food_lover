<template>
  <div class="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">Admin Configuration Page</h2>
      <p class="mt-2 text-center text-sm text-gray-600">Sign in to access configuration panel</p>
    </div>
    <div class=" absolute top-[10%] px-5 left-1/2 border border-gray-400 rounded-2xl text-gray-500">{{ noty }}</div>

    <div class="relative mt-8 sm:mx-auto sm:w-full sm:max-w-md border border-gray-300 rounded-md shadow">
      <div class="bg-white py-8 px-6 sm:px-10">
        <form class="space-y-6" @submit.prevent="handleLogin">
          <div>
            <label for="email" class="block text-sm font-medium text-gray-700">Email address</label>
            <input
              id="email"
              v-model="email"
              type="email"
              autocomplete="email"
              required
              class="mt-1 block w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              :class="{ 'border-red-500 text-red-600': emailError }"
            />
            <p v-if="emailError" class="mt-1 text-sm text-red-600">{{ emailError }}</p>
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              autocomplete="current-password"
              required
              class="mt-1 block w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              :class="{ 'border-red-500 text-red-600': passwordError }"
            />
            <p v-if="passwordError" class="mt-1 text-sm text-red-600">{{ passwordError }}</p>
          </div>

          <div>
            <label for="otp" class="block text-sm font-medium text-gray-700">One-time Password (OTP)</label>
            <input
              id="otp"
              v-model="otpInput"
              type="text"
              autocomplete="off"
              required
              class="mt-1 block w-full px-3 py-2 border rounded-md shadow-sm placeholder-gray-400 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              :class="{ 'border-red-500 text-red-600': otpError }"
            />
            <p v-if="otpError" class="mt-1 text-sm text-red-600">{{ otpError }}</p>
          </div>

          <div class="flex items-center justify-between">
            <label class="flex items-center">
              <input v-model="rememberMe" type="checkbox" class="h-4 w-4 text-indigo-600 border-gray-300 rounded" />
              <span class="ml-2 text-sm text-gray-900">Remember me</span>
            </label>
            <a href="#" @click.prevent="showForgotPassword = true" class="text-sm text-indigo-600 hover:text-indigo-500">
              Forgot your password?
            </a>
          </div>

          <div class="absolute top-0 right-0 m-4">
            <Button
              type="button"
              :label="selectedMember ? selectedMember.name : 'Generate OTP'"
              @click="toggle"
              class="min-w-48"
            />
            <Popover ref="op">
              <div class="p-4">
                <div class="font-semibold text-gray-700 mb-2">Temporary OTP</div>
                <div class="flex items-center gap-2">
                  <code class="px-3 py-1 bg-gray-100 text-indigo-600 rounded font-mono text-lg">
                    {{ OneTimePassword }}
                  </code>
                  <Button 
                    icon="pi pi-copy" 
                    size="small" 
                    text 
                    @click="ToClipboard(OneTimePassword)" 
                    v-tooltip="'Copy to clipboard'"
                  />
                </div>
                <p class="text-xs text-gray-400 mt-2">Use this code once to access the panel.</p>
              </div>
            </Popover>
          </div>

          <div>
            <button
              type="submit"
              class="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              :disabled="loading"
              :class="{ 'opacity-75 cursor-not-allowed': loading }"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" />
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.4 0 0 5.4 0 12h4z" />
              </svg>
              {{ loading ? 'Signing in...' : 'Sign in' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Forgot Password Modal -->
    <div v-if="showForgotPassword" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white p-6 rounded-md shadow-md w-full max-w-sm">
        <h3 class="text-lg font-medium text-gray-900 text-center">Reset your password</h3>
        <p class="text-sm text-gray-500 text-center mb-4">Enter your email to receive a reset link.</p>
        <input
          v-model="resetEmail"
          type="email"
          placeholder="Email address"
          class="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
        />
        <div class="mt-4 space-y-2">
          <button
            @click="handleResetPassword"
            :disabled="resetLoading"
            class="w-full bg-indigo-600 text-white py-2 px-4 rounded hover:bg-indigo-700 text-sm"
            :class="{ 'opacity-75 cursor-not-allowed': resetLoading }"
          >
            {{ resetLoading ? 'Sending...' : 'Send reset link' }}
          </button>
          <button @click="showForgotPassword = false" class="w-full py-2 px-4 border rounded text-sm text-gray-700 hover:bg-gray-100">
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {copyToClipboard} from '../reusables/index.js'
const emit = defineEmits(['verified'])

const email = ref('')
const password = ref('')
const otpInput = ref('')
const rememberMe = ref(false)
const resetEmail = ref('')

const loading = ref(false)
const resetLoading = ref(false)
const showForgotPassword = ref(false)

const emailError = ref('')
const passwordError = ref('')
const otpError = ref('')

const OneTimePassword = ref('')
const op = ref()
const selectedMember = ref(null)
const noty = ref(null)

const generateOTP = () => {
  OneTimePassword.value = String(Math.floor(100000 + Math.random() * 900000))
}

const toggle = (event) => {
  generateOTP()
  op.value.toggle(event)
}

const ToClipboard = async (msg) => {
  const isCopied = copyToClipboard(msg)
}



const validateForm = () => {
  emailError.value = ''
  passwordError.value = ''
  otpError.value = ''
  let valid = true

  if (!email.value) {
    emailError.value = 'Email is required'
    valid = false
  } else if (!/^\S+@\S+\.\S+$/.test(email.value)) {
    emailError.value = 'Invalid email format'
    valid = false
  }

  if (!password.value) {
    passwordError.value = 'Password is required'
    valid = false
  } else if (password.value.length < 6) {
    passwordError.value = 'Password must be at least 6 characters'
    valid = false
  }

  if (!otpInput.value) {
    otpError.value = 'OTP is required'
    valid = false
  } else if (otpInput.value !== OneTimePassword.value) {
    otpError.value = 'Invalid OTP'
    valid = false
  }

  return valid
}

const handleLogin = () => {
  if (!validateForm()) return
  loading.value = true
  
  // Here you would typically make an API call to verify credentials
  // For demo purposes, we're just checking the OTP
  setTimeout(() => {
    loading.value = false
    if (otpInput.value === OneTimePassword.value) {
      noty.value = 'Login successful!'
      OneTimePassword.value = ''
       emit('verified', true)
      // Generate a new OTP after successful login
      generateOTP()
    } else {
      otpError.value = 'Invalid OTP'
    }
  }, 1500)
}

const handleResetPassword = () => {
  if (!resetEmail.value) {
    alert('Enter your email')
    return
  }
  resetLoading.value = true
  setTimeout(() => {
    resetLoading.value = false
    showForgotPassword.value = false
    alert('Reset link sent!')
  }, 1500)
}

onMounted(() => generateOTP())
</script>

<style scoped>
input {
  color: rgb(75, 75, 75);
}
</style>