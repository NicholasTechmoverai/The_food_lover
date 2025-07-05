<template>
    <div
        class="min-h-screen bg-gradient-to-br mx-5 from-gray-50 to-gray-200 dark:from-gray-800 dark:to-gray-900 flex items-center justify-center p-4">
        <div class="w-full max-w-md bg-white dark:bg-gray-800 rounded-xl shadow-lg overflow-hidden">
            <!-- Header with Logo -->
            <div
                class="bg-gradient-to-r from-primary-500 to-primary-600 dark:from-primary-600 dark:to-primary-700 p-6 text-center">
                <div class="mx-auto w-32 h-32 md:w-40 md:h-40 mb-4">
                    <img :src="siteConfig.assets.logo" :alt="siteConfig.assets.logoAlt"
                        class="w-full h-full object-contain drop-shadow-md" />
                </div>
                <h2 class="text-2xl font-bold text-white">Create an Account</h2>
                <p class="text-primary-100 dark:text-primary-200 mt-2">Join our community today</p>
            </div>

            <!-- Form Container -->
            <div class="p-6 md:p-8">
                <!-- Social Login Buttons -->
                <div class="flex flex-col gap-3 mb-6">
                    <Button @click="loginWithGoogle" severity="secondary" outlined
                        class="w-full py-3 border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                        <span class="flex items-center justify-center gap-2">
                            <img src="https://www.google.com/favicon.ico" alt="Google" class="w-5 h-5" />
                            <span>Continue with Google</span>
                        </span>
                    </Button>
                    <Button @click="loginWithFacebook" severity="secondary" outlined
                        class="w-full py-3 border-gray-300 dark:border-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
                        <span class="flex items-center justify-center gap-2">
                            <img src="https://www.facebook.com/favicon.ico" alt="Facebook" class="w-5 h-5" />
                            <span>Continue with Facebook</span>
                        </span>
                    </Button>
                </div>

                <!-- Divider -->
                <div class="flex items-center my-4">
                    <div class="flex-1 border-t border-gray-300 dark:border-gray-600"></div>
                    <span class="px-3 text-gray-500 dark:text-gray-400 text-sm">OR</span>
                    <div class="flex-1 border-t border-gray-300 dark:border-gray-600"></div>
                </div>

                <Form v-slot="$form" :resolver="resolver" :initialValues="initialValues" @submit="onFormSubmit"
                    class="flex flex-col gap-5">
                    <!-- Email Field -->
                    <div class="space-y-1">
                        <FloatLabel variant="on">
                            <IconField class="relative">
                                <InputIcon class="pi pi-envelope " />
                                <InputText id="email" name="email" placeholder="Email"
                                    class="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white" />
                            </IconField>
                            <label for="email">Email</label>
                        </FloatLabel>
                        <Message v-if="$form.email?.invalid" severity="error" size="small" variant="simple"
                            class="text-sm text-red-600 dark:text-red-400 mt-1">
                            {{ $form.email.error?.message }}
                        </Message>
                    </div>
                    <div class="space-y-1">
                        <FloatLabel variant="on">
                            <IconField class="relative">
                                <InputIcon class="pi pi-envelope " />
                                <InputText id="name" name="name" placeholder="Name"
                                    class="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 focus:border-transparent" />
                            </IconField>
                            <label for="name">Name</label>
                        </FloatLabel>
                        <Message v-if="$form.name?.invalid" severity="error" size="small" variant="simple"
                            class="text-sm text-red-600 dark:text-red-400 mt-1">
                            {{ $form.name.error?.message }}
                        </Message>
                    </div>

                    <!-- Password Field -->
                    <div class="space-y-1">
                        <FloatLabel variant="on">
                            <IconField class="relative">
                                <InputIcon class="pi pi-lock " />
                                <Password id="password" name="password" placeholder="Password" toggleMask
                                    :feedback="false"
                                    inputClass="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white" />
                            </IconField>
                            <label for="password">Password</label>
                        </FloatLabel>
                        <Message v-if="$form.password?.invalid" severity="error" size="small" variant="simple"
                            class="text-sm text-red-600 dark:text-red-400 mt-1">
                            {{ $form.password.error?.message }}
                        </Message>
                    </div>

                    <!-- Confirm Password Field -->
                    <div v-if="$form.password?.value && !$form.password?.invalid" class="space-y-1">
                        <FloatLabel variant="on">
                            <IconField class="relative">
                                <InputIcon class="pi pi-lock " />
                                <Password id="confirm_password" name="confirm_password" placeholder="Confirm Password"
                                    toggleMask :feedback="false"
                                    inputClass="w-full pl-10 pr-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white" />
                            </IconField>
                            <label for="confirm_password">Confirm
                                Password</label>
                        </FloatLabel>
                        <Message v-if="$form.confirm_password?.invalid" severity="error" size="small" variant="simple"
                            class="text-sm text-red-600 dark:text-red-400 mt-1">
                            {{ $form.confirm_password.error?.message }}
                        </Message>
                    </div>

                    <!-- Terms Agreement -->
                    <div class="flex  flex-col items-start">
                        <div>
                            <Checkbox id="terms" name="terms" binary />
                            <label for="terms" class="ml-2 text-sm text-gray-700 dark:text-gray-400">
                                I agree to the
                                <a href="#" class="text-primary-600 dark:text-primary-400 underline">Terms</a> and
                                <a href="#" class="text-primary-600 dark:text-primary-400 underline">Privacy</a>
                            </label>
                        </div>
                        <Message v-if="$form.terms?.invalid" severity="error" size="small" variant="simple"
                            class="text-sm text-red-600 dark:text-red-400 mt-1">
                            {{ $form.terms.error?.message }}
                        </Message>
                    </div>


                    <!-- Submit Button -->
                    <Button v-if="!loading"  type="submit" label="Sign Up"
                        class="w-full py-3 bg-gradient-to-r from-primary-500 to-primary-600 dark:from-primary-600 dark:to-primary-700 hover:from-primary-600 hover:to-primary-700 dark:hover:from-primary-700 dark:hover:to-primary-800 text-white font-medium rounded-lg transition-all duration-200 shadow-md hover:shadow-lg mt-2" />
                    <div v-if="loading" class="flex flex-row gap-3 items-center justify-center">
                        <Button :disabled="loading" label="Creating account..."
                            class="max-w-[200px] py-3 bg-primary-500 hover:bg-primary-600 dark:bg-primary-600 dark:hover:bg-primary-700 text-white font-medium rounded-lg transition-colors duration-200 shadow-md" />
                        <Clock />
                    </div>
                    <!-- Login Link -->
                    <div class="text-center text-sm text-gray-600 dark:text-gray-400 mt-4">
                        Already have an account?
                        <router-link to="/register/login"
                            class="text-primary-600 dark:text-primary-400 font-medium hover:underline ml-1">Log
                            in</router-link>
                    </div>
                </Form>
            </div>
        </div>
        <Toast />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import { Form } from '@primevue/forms'
import FloatLabel from 'primevue/floatlabel'
import Button from 'primevue/button'
import Message from 'primevue/message'
import IconField from 'primevue/iconfield'
import InputIcon from 'primevue/inputicon'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Checkbox from 'primevue/checkbox'
import { zodResolver } from '@primevue/forms/resolvers/zod'
import { useToast } from 'primevue/usetoast'
import { z } from 'zod'
import { useSiteStore } from '../config/siteConfig'
import { Signup } from '../apis/auth'
import Clock from '../loaders/Clock.vue'

const { siteConfig } = useSiteStore()
const toast = useToast()
const loading = ref(false)

const initialValues = ref({
    email: '',
    name: '',
    password: '',
    confirm_password: '',
    terms: false,

})

const resolver = zodResolver(
    z
        .object({
            email: z.string().min(5, { message: 'Email is required.' }).email({ message: 'Invalid email address.' }),
            name: z.string().min(3, { message: 'user name too short!' }),
            password: z
                .string()
                .min(6, { message: 'Minimum 6 characters.' })
                // .max(8, { message: 'Maximum 8 characters.' })
                .refine((val) => /[a-z]/.test(val), { message: 'Must include a lowercase letter.' })
                .refine((val) => /[A-Z]/.test(val), { message: 'Must include an uppercase letter.' })
                .refine((val) => /\d/.test(val), { message: 'Must include a number.' }),
            confirm_password: z.string(),
            terms: z.literal(true, { errorMap: () => ({ message: 'Please accept terms' }) }),

        })
        .refine((data) => data.password === data.confirm_password, {
            message: "Passwords don't match",
            path: ['confirm_password']
        })
)
const loginWithGoogle = () => {
    // Implement Google login logic
    console.log('Logging in with Google');
};

const loginWithFacebook = () => {
    // Implement Facebook login logic
    console.log('Logging in with Facebook');
};
const onFormSubmit = async ({ valid, values }) => {
    if (valid) {
        loading.value = true
        const res = await Signup(values);
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
