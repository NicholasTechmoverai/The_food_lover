<template>
    <div class="p-6 max-w-2xl mx-auto space-y-6">
        <!-- Theme Color Picker -->
        <div class="relative group">
            <button @click="showColorPicker = !showColorPicker"
                class="px-4 py-1.5 sm:px-6 sm:py-2 bg-white dark:bg-gray-700 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 rounded-full font-medium hover:bg-gray-50 dark:hover:bg-gray-600 transition-all transform hover:scale-105 active:scale-95 shadow-sm flex items-center gap-1 sm:gap-2 text-sm sm:text-base">
                <i class="pi pi-palette text-sm sm:text-base"></i>
                Theme
            </button>

            <div v-if="showColorPicker"
                class="absolute z-20 mt-2 w-40 sm:w-48 p-2 sm:p-3 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700">
                <div class="grid grid-cols-5 gap-1 sm:gap-2">
                    <button v-for="color in themeColors" :key="color.value" @click="changeThemeColor(color)"
                        class="w-6 h-6 sm:w-8 sm:h-8 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--theme-color)]"
                        :class="[color.bg, user.theme === color.value ? 'ring-2 ring-offset-2 ring-[var(--theme-color)]' : '']"
                        :title="color.name">
                    </button>
                </div>
            </div>
        </div>
        <!-- Username -->
        <FloatLabel class="w-full" variant="in">
            <IconField>
                <InputIcon class="pi pi-user" />
                <InputText id="username" v-model="user.username" class="w-full" @input="checkUsername"
                    :maxlength="20" />
            </IconField>
            <label for="username">
                Username
                <span class="text-gray-500 text-xs">({{ user.username.length }}/20)</span>
                <span v-if="username_message.message" :class="{
                    'text-red-500': username_message.type === 'error',
                    'text-green-500': username_message.type === 'success'
                }" class="text-xs ml-1">
                    {{ username_message.message }}
                </span>
            </label>
        </FloatLabel>

        <!-- Full Name -->
        <FloatLabel class="w-full" variant="in">
            <IconField>
                <InputIcon class="pi pi-user" />
                <InputText id="name" v-model="user.name" class="w-full" :maxlength="50" />
            </IconField>
            <label for="name">
                Full Name
                <span class="text-gray-500 text-xs">({{ user.name.length }}/50)</span>
            </label>
        </FloatLabel>

        <!-- Bio -->
        <div class="space-y-2">
            <label class="text-gray-600 dark:text-gray-300 font-medium">
                Bio <span class="text-sm text-gray-400">(Optional)</span>
            </label>
            <Editor v-model="bioContent" editor-style="height: 160px" class="rounded-md overflow-hidden">
                <template #toolbar>
                    <span class="ql-formats">
                        <button class="ql-bold" v-tooltip.bottom="'Bold'" />
                        <button class="ql-italic" v-tooltip.bottom="'Italic'" />
                        <button class="ql-underline" v-tooltip.bottom="'Underline'" />
                        <button class="ql-list" value="bullet" v-tooltip.bottom="'Bullet List'" />
                        <button class="ql-list" value="ordered" v-tooltip.bottom="'Numbered List'" />
                    </span>
                </template>
            </Editor>
        </div>

        <!-- Divider -->
        <hr class="border-gray-200 dark:border-gray-700" />
        <h6 class="text-gray-600 dark:text-gray-300 font-medium">
            Personal Information
            <span class="text-sm text-gray-400">(Private)</span>
        </h6>

        <!-- Phone Number -->
        <FloatLabel class="w-full" variant="in">
            <IconField>
                <InputIcon class="pi pi-phone" />
                <InputMask id="phone" v-model="user.phone_number" mask="99-99999999" placeholder="07-0000000"
                    class="w-full" />
            </IconField>
            <label for="phone">Phone Number</label>
        </FloatLabel>

        <!-- Email Section -->
        <div class="space-y-2">
            <div class="flex gap-2 items-center">
                <FloatLabel class="w-full" variant="in">
                    <IconField>
                        <InputIcon class="pi pi-envelope" />
                        <InputText id="email" v-model="user.email" :disabled="!editEmail" class="w-full" />
                    </IconField>
                    <label for="email">Email <span class="text-red-500 text-xs">{{ emailError }}</span></label>
                </FloatLabel>
                <Button v-if="!editEmail" label="Edit" icon="pi pi-pencil" class="h-full" @click="editEmail = true"
                    outlined />
            </div>

            <div v-if="editEmail" class="flex flex-wrap gap-2">
                <Button :disabled="!verifiable" label="Save & Verify" icon="pi pi-check" @click="verifyEmail"
                    :loading="loading" />
                <Button label="Cancel" icon="pi pi-times" @click="cancelEmailEdit" outlined
                    class="p-button-secondary" />
            </div>

            <!-- OTP Modal -->
            <Transition name="fade">
                <div v-if="showOtpModal" class="bg-white dark:bg-gray-900 rounded-lg p-4 shadow mt-2 space-y-3">
                    <h3 class="text-lg font-semibold">Verify Email</h3>
                    <p class="text-sm text-gray-500">
                        Enter the 6-digit code sent to your email.
                    </p>
                    <InputOtp v-model="otp" :length="6" class="justify-center" />
                    <small v-if="otpError" class="text-red-500">{{ otpError }}</small>
                    <div class="flex justify-between items-center mt-2">
                        <Button label="Resend Code" text class="text-sm" @click="resendOtp" :loading="resending" />
                        <Button label="Verify" class="text-sm" @click="submitOtp" :loading="verifying" />
                    </div>
                </div>
            </Transition>

            <p v-if="saving_new_email"> saving new email...</p>
        </div>
        <Toast position="bottom-center" group="bc" />

    </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { useToast } from 'primevue/usetoast';

import FloatLabel from 'primevue/floatlabel';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';
import InputMask from 'primevue/inputmask';
import InputOtp from 'primevue/inputotp';
import Editor from 'primevue/editor';
import Button from 'primevue/button';

// External modules
import { usersSocket } from '../a_websocket';
import { send_verify, verifyCodeAPI } from '../apis/auth';
import { useAuthStore } from '../store/user';
import { set } from 'date-fns';
import { make_a_post } from '../apis';

// Store
const auth = useAuthStore();
const toast = useToast();

// Props
const props = defineProps({
    user: Object,
});




// -------------------- State --------------------

const untouched_user = ref({ ...props.user });
const user = ref({ ...props.user });
const bioContent = ref(user.value.bio || '');

const editEmail = ref(false);
const showOtpModal = ref(false);
const otp = ref('');
const otpError = ref('');

const username_message = ref({
    type: '',
    message: ''
});

const loading = ref(false);
const verifying = ref(false);
const resending = ref(false);

const codeId = ref('');
const codeType = ref('email');

// -------------------- Username Check --------------------
const showColorPicker = ref(false)
const themeColors = [
    { name: 'Emerald', value: '#10B981', bg: 'bg-emerald-500' },
    { name: 'Blue', value: '#3B82F6', bg: 'bg-blue-500' },
    { name: 'Indigo', value: '#6366F1', bg: 'bg-indigo-500' },
    { name: 'Purple', value: '#8B5CF6', bg: 'bg-purple-500' },
    { name: 'Pink', value: '#EC4899', bg: 'bg-pink-500' },
    { name: 'Red', value: '#EF4444', bg: 'bg-red-500' },
    { name: 'Orange', value: '#F97316', bg: 'bg-orange-500' },
    { name: 'Yellow', value: '#F59E0B', bg: 'bg-yellow-500' },
    { name: 'Teal', value: '#14B8A6', bg: 'bg-teal-500' },
    { name: 'Cyan', value: '#06B6D4', bg: 'bg-cyan-500' }
];

const changeThemeColor = (color) => {
    user.value.theme = color.value;
    props.user.theme = color.value
    showColorPicker.value = false;
    // Save to backend in real implementation
};
let usernameTimeout;
const checkUsername = () => {
    clearTimeout(usernameTimeout);

    const name = user.value.username.trim().toLowerCase().replace(/ /g, "_");
    user.value.username = name;


    if (!name) {
        username_message.value = { type: 'error', message: 'Cannot be empty' };
        setTimeout(() => {
            if (!user.value.username) {
                resetUsername();
            }

        }, 3000);
        return;
    }

    if (name.length < 3) {
        username_message.value = { type: 'error', message: 'At least 3 characters' };
        return;
    }

    if (name.length > 20) {
        username_message.value = { type: 'error', message: 'Max 20 characters' };
        user.value.username = name.slice(0, 20);
        return;
    }

    username_message.value = { type: '', message: 'Checking...' };

    usernameTimeout = setTimeout(async () => {
        try {
            usersSocket.emit('check_username_availability', { username: name, user_id: user.value.id });
            usersSocket.on('check_username_availability', (data) => {
                console.log('Username check response:', data);
                username_message.value = data.available
                    ? { type: 'success', message: 'Available' }
                    : { type: 'error', message: 'Unavailable' };
            });
        } catch {
            username_message.value = { type: 'error', message: 'Check failed' };
        }
    }, 500);
};

const resetUsername = () => {
    user.value.username = untouched_user.value.username;
    setTimeout(() => (username_message.value = { type: '', message: '' }), 2000);
};

const verifiable = ref(false);
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const emailError = ref('');
const saving_new_email = ref(false)
const updating_profile = ref(false)
// -------------------- Email Verification --------------------
watch(() => user.value.email, (newEmail) => {
    if (editEmail.value && newEmail !== untouched_user.value.email) {
        otp.value = '';
        otpError.value = '';
        showOtpModal.value = false;

        if (!emailRegex.test(newEmail)) {
            emailError.value = ' Invalid email address.';
            return;
        } else {
            emailError.value = '';
            verifiable.value = true;
        }
    }
    else {
        otp.value = '';
        otpError.value = '';
        showOtpModal.value = false;
        verifiable.value = false;
    }
}, { immediate: true });

const cancelEmailEdit = () => {
    user.value.email = untouched_user.value.email;
    editEmail.value = false;
    showOtpModal.value = false;
    otp.value = '';
    otpError.value = '';
    verifiable.value = false;
};

const verifyEmail = async () => {
    loading.value = true;
    try {
        const res = await send_verify(null, 'code', 'email', untouched_user.value.email, user.value.email);
        if (res?.success && res.data) {
            codeId.value = res.data.id;
            codeType.value = res.data.type;
            showOtpModal.value = true;

            toast.add({
                severity: 'info',
                summary: 'Code Sent',
                detail: 'Verification code sent to your email.',
                life: 3000,
                group: 'bc'
            });
            verifiable.value = false;
        } else {
            user.value.email = untouched_user.value.email;
            toast.add({
                severity: 'error',
                summary: 'Error',
                detail: res.message || 'Verification failed',
                life: 3000,
                group: 'bc'
            });
            throw new Error(res.message || 'Verification failed');
        }
    } catch (e) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: e.message || 'Failed to send code',
            life: 3000,
            group: 'bc'
        });
    } finally {
        loading.value = false;
    }
};

const submitOtp = async () => {
    if (otp.value.length !== 6) {
        otpError.value = 'Enter the 6-digit code';
        return;
    }

    verifying.value = true;
    otpError.value = '';

    try {
        const res = await verifyCodeAPI(codeId.value, otp.value, codeType.value);
        if (res?.success && res.data) {
            toast.add({
                severity: 'success',
                summary: 'Verified',
                detail: 'Your email has been verified',
                life: 3000,
                group: 'bc'
            });
            auth.setUser(res.data.user)
            auth.setToken({ token: res.data.access_token, expires_in: res.data.expires_in })
            await saveEmail()

            setTimeout(() => {
                showOtpModal.value = false;
                editEmail.value = false;
                untouched_user.value.email = user.value.email;
            }, 1000);

        } else {
            toast.add({
                severity: 'error',
                summary: 'Verification Failed',
                detail: res?.message || 'Invalid or expired OTP',
                life: 3000,
                group: 'bc'
            });
            throw new Error(res?.message || 'Invalid or expired OTP');
        }
    } catch (e) {
        otpError.value = 'Invalid or expired code';
        toast.add({
            severity: 'error',
            summary: 'Verification Failed',
            detail: otpError.value,
            life: 3000,
            group: 'bc'
        });
    } finally {
        verifying.value = false;
    }
};

const resendOtp = async () => {
    resending.value = true;
    try {
        const res = await send_verify(codeId.value, 'code', codeType.value, user.value.email);
        if (res?.success && res.data) {
            codeId.value = res.data.id;
            toast.add({
                severity: 'info',
                summary: 'Code Resent',
                detail: 'New verification code sent.',
                life: 3000,
                group: 'bc'
            });
        } else {
            toast.add({
                severity: 'error',
                summary: 'Resend Failed',
                detail: res.message || 'Failed to resend verification code',
                life: 3000,
                group: 'bc'
            });
            throw new Error(res.message || 'Failed to resend');
        }
    } catch (e) {
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: e.message || 'Resend failed',
            life: 3000,
            group: 'bc'
        });
    } finally {
        resending.value = false;
    }
};



const saveEmail = async () => {
    saving_new_email.value = true

    try {
        const res = await make_a_post(`/users/update/${untouched_user.value.username}`, auth.token, {
            new_email: user.value.email,
            old_email: untouched_user.value.email,
            user_id: user.value.id,
            email: untouched_user.value.email,
        });

        if (res?.success && res.data) {
            untouched_user.value = { ...user.value };
            toast.add({
                severity: 'success',
                summary: 'Email Updated successfully',
                detail: '',
                life: 3000,
                group: 'bc'
            });
        } else {
            toast.add({
                severity: 'error',
                summary: 'Update Failed',
                detail: res?.message || 'Failed to update email. Please try again later.',
                life: 3000,
                group: 'bc'
            });
        }
    } catch (error) {
        console.error('Error updating profile:', error);
        toast.add({
            severity: 'error',
            summary: 'Update Failed',
            detail: 'Failed to update profile. Please try again later.',
            life: 3000,
            group: 'bc'
        });
    } finally {
        saving_new_email.value = false
    }
};



const saveProfile = async () => {
    try {
        const res = await make_a_post(`/users/update/${untouched_user.value.username}`, auth.token, {
            user_id: untouched_user.value.id,
            email: untouched_user.value.email,
            username: user.value.username,
            name: user.value.name,
            bio: bioContent.value,
            phone_number: user.value.phone_number,
            theme:user.value.theme
        });
        return res
    } catch (error) {
        console.error('Error updating profile:', error);
        toast.add({
            severity: 'error',
            summary: 'Update Failed',
            detail: 'Failed to update profile. Please try again later.',
            life: 3000,
            group: 'bc'
        });
    }
};
defineExpose({ saveProfile });

</script>
