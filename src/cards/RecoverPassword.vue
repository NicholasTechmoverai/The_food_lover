<template>
  <div
    class="min-h-screen flex flex-col items-center justify-center p-6 space-y-12 bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    <!-- Step 1: Email Entry -->
    <div v-if="step === 1" class="w-full max-w-sm bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
      <h2 class="text-xl font-bold mb-4">Recover Your Account</h2>
      <form @submit.prevent="submitEmail" class="flex flex-col gap-4">
        <InputText v-model="email" type="email" placeholder="Enter your email" />
        <small v-if="emailError" class="text-red-500 text-sm">{{ emailError }}</small>
        <Button type="submit" label="Send Verification Code" class="w-full" :loading="loading" />
      </form>
    </div>

    <!-- Step 2: OTP Verification -->
    <div v-if="step === 2" class="w-full max-w-sm bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
      <h2 class="text-xl font-bold mb-2">Enter Verification Code</h2>
      <p class="text-sm mb-4">Check your email for the 6-digit code</p>
      <form @submit.prevent="submitOtp" class="flex flex-col gap-4">
        <InputOtp v-model="otp" :length="6" />
        <small v-if="otpError" class="text-red-500 text-sm">{{ otpError }}</small>
        <div class="flex justify-between items-center mt-4">
          <Button label="Resend Code" text class="text-sm" @click="resendOtp" :loading="resending" />
          <Button type="submit" label="Verify" class="text-sm" :loading="loading" />
        </div>
      </form>
    </div>

    <!-- Step 3: Password Reset -->
    <div v-if="step === 3" class="w-full max-w-sm bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
      <h2 class="text-xl font-bold mb-2">Set New Password</h2>
      <p class="text-sm mb-4">Make sure it's strong and secure</p>
      <form @submit.prevent="submitPassword" class="flex flex-col gap-4">
        <Password v-model="password" placeholder="New Password" toggleMask />
        <Password v-model="confirmPassword" placeholder="Confirm Password" toggleMask />
        <small v-if="passwordError" class="text-red-500 text-sm">{{ passwordError }}</small>

        <ul class="text-xs text-gray-600 dark:text-gray-300 mt-2 space-y-1">
          <li :class="checkRule(/[a-z]/) ? 'text-green-500' : ''">• At least one lowercase letter</li>
          <li :class="checkRule(/[A-Z]/) ? 'text-green-500' : ''">• At least one uppercase letter</li>
          <li :class="checkRule(/[0-9]/) ? 'text-green-500' : ''">• At least one number</li>
          <li :class="password.length >= 6 ? 'text-green-500' : ''">• Minimum 6 characters</li>
        </ul>

        <Button type="submit" label="Reset Password" class="w-full mt-2" :loading="loading" />
      </form>
    </div>
  </div>
  <Toast />

</template>

<script setup>
import { ref } from 'vue';
import { useToast } from 'primevue/usetoast';
import router from '../router';
import { is_user_exists, resetPassword, send_verify, verifyCodeAPI } from '../apis/auth';
import { useAuthStore } from '../store/user';
const auth = useAuthStore()
const toast = useToast();
const step = ref(1);
const codeId = ref(null);
const type = ref('recover-password');
const loading = ref(false);
const resending = ref(false);
const success = ref(false);
const error = ref('');

// Step 1
const email = ref('');
const emailError = ref('');
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const submitEmail = async () => {
  if (!email.value || !emailRegex.test(email.value)) {
    emailError.value = 'Please enter a valid email address.';
    return;
  }
  emailError.value = '';
  loading.value = true;

  try {
    const res = await is_user_exists(email.value);
    toast.add({
      severity: res.success ? 'success' : 'error',
      summary: res.success ? 'Email Found' : 'Error',
      detail: res.message,
      life: 5000
    });
    if (res.success) {
      await resendCode();
      step.value = 2;
    }
  } finally {
    loading.value = false;
  }
};

// Step 2
const otp = ref('');
const otpError = ref('');

const submitOtp = async () => {
  if (otp.value.length !== 6) {
    otpError.value = 'Enter the 6-digit code.';
    return;
  }
  otpError.value = '';
  loading.value = true;

  try {
    const res = await verifyCodeAPI(codeId.value, otp.value, type.value);
    if (res?.success && res.data) {
      const { user, access_token, expires_in } = res.data;
      auth.setUser(user);
      auth.setToken({ token: access_token, expires_in });
      toast.add({ severity: 'success', summary: 'Verified', detail: 'OTP confirmed.', life: 3000 });
      step.value = 3;
    } else {
      otp.value = ''
      toast.add({ severity: 'error', summary: 'Failed authentication', detail: 'Invalid or expired OTP.', life: 3000 });
      error.value = res.message || 'Invalid or expired code.';
    }
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Failed authentication', detail: 'Invalid or expired OTP.', life: 3000 });
    error.value = e?.response?.data?.detail || 'Verification failed.';
  } finally {
    loading.value = false;
  }
};

const resendOtp = async () => {
  await resendCode();
};

// Step 3
const password = ref('');
const confirmPassword = ref('');
const passwordError = ref('');

const checkRule = (regex) => regex.test(password.value);

const submitPassword = async () => {
  if (!checkRule(/[a-z]/) || !checkRule(/[A-Z]/) || !checkRule(/[0-9]/) || password.value.length < 6) {
    passwordError.value = 'Password does not meet the requirements.';
    return;
  }
  if (password.value !== confirmPassword.value) {
    passwordError.value = 'Passwords do not match.';
    return;
  }

  loading.value = true;
  try {
    const res = await resetPassword({ password: password.value, confirmPassword: confirmPassword.value, verifier: email.value });
    toast.add({
      severity: res.success ? 'success' : 'error',
      summary: res.success ? 'Success' : 'Failed',
      detail: res.message,
      life: 5000
    });
    if (res.success) {
      toast.add({ severity: 'success', summary: 'Password changed', detail: 'Password changed successfully!', life: 3000 });
      router.push('/recipes');
      resetForm();
    }
  } finally {
    loading.value = false;
  }
};

const resendCode = async () => {
  resending.value = true;
  try {
    const res = await send_verify(codeId.value, 'code', type.value, email.value);
    if (res?.success && res.data) {
      codeId.value = res.data.id;
      type.value = res.data.type;
      toast.add({ severity: 'info', summary: 'Resent', detail: 'Code has been resent.', life: 3000 });
    } else {
      error.value = res.message || 'Failed to resend code.';
    }
  } catch (e) {
    error.value = e?.response?.data?.detail || 'Resend failed.';
  } finally {
    resending.value = false;
  }
};

const resetForm = () => {
  email.value = '';
  otp.value = '';
  password.value = '';
  confirmPassword.value = '';
  step.value = 1;
};
</script>

<style scoped>
.custom-otp-input {
  width: 48px;
  height: 48px;
  font-size: 24px;
  text-align: center;
  border: 1px solid var(--p-inputtext-border-color);
  background: transparent;
  border-radius: 0;
  border-right: none;
  color: var(--p-inputtext-color);
}

.custom-otp-input:focus {
  outline: 2px solid var(--p-focus-ring-color);
}

.custom-otp-input:first-child,
.custom-otp-input:nth-child(5) {
  border-top-left-radius: 12px;
  border-bottom-left-radius: 12px;
}

.custom-otp-input:nth-child(3),
.custom-otp-input:last-child {
  border-top-right-radius: 12px;
  border-bottom-right-radius: 12px;
  border-right-width: 1px;
  border-color: var(--p-inputtext-border-color);
}
</style>
