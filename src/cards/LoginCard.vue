<template>
  <div
    class="min-h-screen bg-gradient-to-br from-gray-50 to-gray-200 dark:from-gray-800 dark:to-gray-900 flex items-center justify-center p-4">
    <div class="w-full max-w-md bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
      <!-- Header with Logo -->
      <div class="bg-primary-500 dark:bg-primary-600 p-6 text-center">
        <div class="mx-auto w-32 h-32 md:w-40 md:h-40 mb-4">
          <img :src="siteConfig.assets.logo" :alt="siteConfig.assets.logoAlt"
            class="w-full h-full object-contain drop-shadow-md" />
        </div>
        <h2 class="text-2xl font-bold text-white">Welcome Back</h2>
        <p class="text-primary-100 mt-1">Sign in</p>
      </div>

      <!-- Form Container -->
      <div class="p-6 md:p-8">
        <Form v-slot="$form" :resolver="resolver" :initialValues="initialValues" @submit="onFormSubmit"
          class="flex flex-col gap-5">
          <!-- Email Field -->
          <div class="space-y-1">
            <FloatLabel variant="on">
              <IconField class="relative">
                <InputIcon class="pi pi-envelope" />
                <InputText id="email" name="email" placeholder="Email"
                  class="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white" />
              </IconField>
              <label for="email" class="text-gray-700 dark:text-gray-300">Email</label>
            </FloatLabel>
            <Message v-if="$form.email?.invalid" severity="error" size="small" variant="simple"
              class="text-sm text-red-600 dark:text-red-400 mt-1">
              {{ $form.email.error?.message }}
            </Message>
          </div>

          <!-- Password Field -->
          <div class="space-y-1">
            <FloatLabel variant="on">
              <IconField class="relative">
                <InputIcon class="pi pi-lock" />
                <Password id="password" name="password" placeholder="Password" toggleMask :feedback="false"
                  inputClass="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white" />
              </IconField>
              <label for="password" class="text-gray-700 dark:text-gray-300">Password</label>
            </FloatLabel>
            <Message v-if="$form.password?.invalid" severity="error" size="small" variant="simple"
              class="text-sm text-red-600 dark:text-red-400 mt-1">
              {{ $form.password.error?.message }}
            </Message>
          </div>

          <!-- Remember Me & Forgot Password -->
          <div class="flex items-center justify-between">
            <div class="flex items-center">
              <Checkbox id="remember" name="remember" binary />
              <label for="remember" class="ml-2 text-sm text-gray-600 dark:text-gray-400">Remember me</label>
            </div>
            <router-link to="/register/recover-password"
              class="text-sm text-primary-600 dark:text-primary-400 hover:underline">Forgot password?</router-link>
          </div>

          <!-- Submit Button -->
          <Button type="submit" v-if="!loading" :disabled="loading" :label="loading ? 'Signing in...' : 'Sign In'"
            class="w-full py-3 bg-primary-500 hover:bg-primary-600 dark:bg-primary-600 dark:hover:bg-primary-700 text-white font-medium rounded-lg transition-colors duration-200 shadow-md" />

          <div v-if="loading" class="flex flex-row items-center justify-center">
            <Button :disabled="loading" label="Signing in..."
              class="max-w-[200px] py-3 bg-primary-500 hover:bg-primary-600 dark:bg-primary-600 dark:hover:bg-primary-700 text-white font-medium rounded-lg transition-colors duration-200 shadow-md" />
            <Clock />
          </div>
          <!-- Sign Up Link -->
          <div class="text-center text-sm text-gray-600 dark:text-gray-400 mt-4">
            Don't have an account?
            <router-link to="/register/signup"
              class="text-primary-600 dark:text-primary-400 font-medium hover:underline ml-1">Sign up</router-link>
          </div>
        </Form>
      </div>
    </div>
    <Toast />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Form } from '@primevue/forms';
import Clock from '../loaders/Clock.vue';
import FloatLabel from 'primevue/floatlabel';
import Button from 'primevue/button';
import Message from 'primevue/message';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import { zodResolver } from '@primevue/forms/resolvers/zod';
import { useToast } from 'primevue/usetoast';
import { z } from 'zod';
import { useSiteStore } from '../config/siteConfig';
import { Login } from '../apis/auth';
import router from '../router';

const { siteConfig } = useSiteStore()

const toast = useToast();
const loading = ref(false)
const initialValues = ref({
  email: '',
  password: ''
});

const resolver = ref(
  zodResolver(
    z.object({
      email: z
        .string()
        .min(1, { message: 'Email is required.' })
        .email({ message: 'Invalid email address.' }),
      password: z
        .string()
        .min(6, { message: 'Password must be at least 6 characters.' })
    })
  )
);

const onFormSubmit = async ({ valid, values }) => {
  if (valid) {
    loading.value = true
    const res = await Login(values);
    if (res) {
      loading.value = false
      if (res.message) {
        toast.add({
          severity: res.success ? 'success' : 'error',
          summary: res.success ? 'Login successful' : 'Error logging in!',
          detail: `${res.message}`,
          life: 5000
        });
      }
      if (res.success) {
        router.push('/recipes')
      }
    }

  }
};
</script>
