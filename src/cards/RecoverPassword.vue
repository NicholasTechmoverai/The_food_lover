<template>
  <div class="min-h-screen flex flex-col items-center justify-center p-6 space-y-12 bg-gray-50 dark:bg-gray-900 text-gray-800 dark:text-gray-100">
    
    <!-- Step 1: Email Form -->
    <div v-if="step === 1" class="w-full max-w-sm bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
      <h2 class="text-xl font-bold mb-4">Enter Your Email</h2>
      <form @submit.prevent="submitEmail" class="flex flex-col gap-4">
        <InputText v-model="email" type="email" placeholder="Email" />
        <small v-if="emailError" class="text-red-500 text-sm">{{ emailError }}</small>
        <Button type="submit" label="Send OTP" class="w-full" />
      </form>
    </div>

    <!-- Step 2: OTP Verification -->
    <div v-if="step === 2" class="w-full max-w-sm bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
      <h2 class="text-xl font-bold mb-2">Verify OTP</h2>
      <p class="text-sm mb-4">Enter the 6-digit code sent to your email</p>
      <form @submit.prevent="submitOtp" class="flex flex-col gap-4">
        <InputOtp v-model="otp" :length="6" />
        <small v-if="otpError" class="text-red-500 text-sm">{{ otpError }}</small>
        <div class="flex justify-between items-center mt-4">
          <Button label="Resend" text class="text-sm" @click="resendOtp" />
          <Button type="submit" label="Verify OTP" class="text-sm" />
        </div>
      </form>
    </div>

    <!-- Step 3: Password Reset -->
    <div v-if="step === 3" class="w-full max-w-sm bg-white dark:bg-gray-800 rounded-xl shadow-md p-6">
      <h2 class="text-xl font-bold mb-2">Set New Password</h2>
      <p class="text-sm mb-4">Choose a strong password</p>
      <form @submit.prevent="submitPassword" class="flex flex-col gap-4">
        <Password v-model="password" placeholder="New Password" toggleMask />
        <Password v-model="confirmPassword" placeholder="Confirm Password" toggleMask />
        <small v-if="passwordError" class="text-red-500 text-sm">{{ passwordError }}</small>

        <!-- Password guidance -->
        <ul class="text-xs text-gray-600 dark:text-gray-300 mt-2 space-y-1">
          <li :class="checkRule(/[a-z]/) ? 'text-green-500' : ''">• At least one lowercase letter</li>
          <li :class="checkRule(/[A-Z]/) ? 'text-green-500' : ''">• At least one uppercase letter</li>
          <li :class="checkRule(/[0-9]/) ? 'text-green-500' : ''">• At least one number</li>
          <li :class="password.length >= 6 ? 'text-green-500' : ''">• Minimum 6 characters</li>
        </ul>

        <Button type="submit" label="Reset Password" class="w-full mt-2" />
      </form>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useToast } from 'primevue/usetoast';

const toast = useToast();
const step = ref(1);

// Step 1: Email
const email = ref('');
const emailError = ref('');
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

const submitEmail = () => {
  if (!email.value || !emailRegex.test(email.value)) {
    emailError.value = 'Please enter a valid email address.';
    return;
  }
  emailError.value = '';
  // TODO: Call backend to send OTP
  toast.add({ severity: 'info', summary: 'OTP Sent', detail: 'Check your email.', life: 3000 });
  step.value = 2;
};

// Step 2: OTP
const otp = ref('');
const otpError = ref('');

const submitOtp = () => {
  if (otp.value.length !== 6) {
    otpError.value = 'Please enter the 6-digit code.';
    return;
  }
  otpError.value = '';
  // TODO: Call backend to verify OTP
  toast.add({ severity: 'success', summary: 'Verified', detail: 'OTP verified. Proceed.', life: 3000 });
  step.value = 3;
};

const resendOtp = () => {
  toast.add({ severity: 'info', summary: 'Resent', detail: 'OTP has been resent.', life: 3000 });
  // TODO: Call backend to resend OTP
};

// Step 3: Password
const password = ref('');
const confirmPassword = ref('');
const passwordError = ref('');

const checkRule = (regex) => regex.test(password.value);

const submitPassword = () => {
  if (!checkRule(/[a-z]/) || !checkRule(/[A-Z]/) || !checkRule(/[0-9]/) || password.value.length < 6) {
    passwordError.value = 'Password does not meet requirements.';
    return;
  }
  if (password.value !== confirmPassword.value) {
    passwordError.value = 'Passwords do not match.';
    return;
  }
  passwordError.value = '';
  // TODO: Call backend to update password
  toast.add({ severity: 'success', summary: 'Password Changed', detail: 'You can now log in.', life: 3000 });
  resetForm();
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
    appearance: none;
    text-align: center;
    transition: all 0.2s;
    border-radius: 0;
    border: 1px solid var(--p-inputtext-border-color);
    background: transparent;
    outline-offset: -2px;
    outline-color: transparent;
    border-right: 0 none;
    transition: outline-color 0.3s;
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
    border-right-style: solid;
    border-color: var(--p-inputtext-border-color);
}
</style>
