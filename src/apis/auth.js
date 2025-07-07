import axios from 'axios'
import { ref } from "vue";


export const B_URl = 'http://localhost:8000'
const BACKEND_URL = `${B_URl}/api`

export const Login = async (form) => {
    if (!form || typeof form !== 'object') {
        return { success: false, message: 'Invalid Login data' }
    }

    try {
        const response = await axios.post(`${BACKEND_URL}/auth/login`, form)

        if (response.status === 200 || response.status === 201) {
            return { success: true, data: response.data }
        } else {
            return {
                success: false,
                message: `Unexpected response status: ${response.detail}`
            }
        }
    } catch (error) {
        return {
            success: false,
            message: error?.response?.data?.detail || error.message || 'An error occurred,try again later',
            data: error?.response?.data
        }
    }
}

export const Signup = async (form) => {
    if (!form || typeof form !== 'object') {
        return { success: false, message: 'Invalid Signup data' }
    }

    try {
        const response = await axios.post(`${BACKEND_URL}/auth/sign-up`, form)

        if (response.status === 200 || response.status === 201) {
            return { success: true, data: response.data }
        } else {
            return {
                success: false,
                message: `Unexpected response status: ${response.detail}`
            }
        }
    } catch (error) {
        return {
            success: false,
            message: error?.response?.data?.detail || error.message || 'An error occurred',
            data: error?.response?.data
        }
    }
}

export const Logout = async () => {
    authStore.setToken(null)
    authStore.setUser(null)

    try {
        const response = await axios.post(`${BACKEND_URL}/auth/logout`, form)

        if (response.status === 200 || response.status === 201) {
            return { success: true }
        } else {
            return {
                success: false,
                message: `Unexpected response status: ${response.detail}`
            }
        }
    } catch (error) {
        return {
            success: false,
            message: error?.response?.data?.detail || error.message || 'An error occurred,try again later',
            data: error?.response?.data
        }
    }
}


export const resetPassword = async (form) => {
    if (!form || typeof form !== 'object') {
        return { success: false, message: 'Invalid Login data' }
    }

    try {
        const response = await axios.post(`${BACKEND_URL}/reset-password`, form)

        if (response.status === 200 || response.status === 201) {
            return { success: true, data: response.data }
        } else {
            return {
                success: false,
                message: `Unexpected response status: ${response.status}`
            }
        }
    } catch (error) {
        return {
            success: false,
            message: error?.response?.data?.message || error.message || 'An error occurred',
            data: error?.response?.data
        }
    }
}