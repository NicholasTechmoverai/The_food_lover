import axios from 'axios'
import { ref } from "vue";


// export const B_URl = 'http://localhost:8000'
export const B_URl = 'https://dragon-brief-mayfly.ngrok-free.app'

const BACKEND_URL = `${B_URl}/api`

export async function verifyCodeAPI(codeId, code, type) {
  try {
    const response = await axios.post(`${BACKEND_URL}/auth/verify`, null, {
      params: { code_id: codeId, code, type }
    });

    if ([200, 201].includes(response.status)) {
      return { success: true, data: response.data };
    }

    return {
      success: false,
      message: `Unexpected response status: ${response.status}`
    };
  } catch (error) {
    return {
      success: false,
      message:
        error?.response?.data?.detail ||
        error?.message ||
        'An unexpected error occurred. Please try again.',
      data: error?.response?.data
    };
  }
}

export async function send_verify(codeId,method,type,u_id=null) {
  try {
    const response = await axios.post(`${BACKEND_URL}/auth/send-verification`, null, {
      params: { code_id:codeId, u_id, type,method }
    });

    if ([200, 201].includes(response.status)) {
      return { success: true, data: response.data };
    }

    return {
      success: false,
      message: `Unexpected response status: ${response.status}`
    };
  } catch (error) {
    return {
      success: false,
      message:
        error?.response?.data?.detail ||
        error?.message ||
        'An unexpected error occurred. Please try again.',
      data: error?.response?.data
    };
  }
}

export async function is_user_exists(verifier) {
  try {
    const response = await axios.post(`${BACKEND_URL}/auth/is-user-exists`, null, {
      params: {  verifier }
    });

    if ([200, 201].includes(response.status)) {
      return { success: true, data: response.data };
    }

    return {
      success: false,
      message: `Unexpected response status: ${response.status}`
    };
  } catch (error) {
    return {
      success: false,
      message:
        error?.response?.data?.detail ||
        error?.message ||
        'An unexpected error occurred. Please try again.',
      data: error?.response?.data
    };
  }
}

// Check if token is expired
export function isTokenExpired(token) {
    try {
        const [, payloadBase64] = token.split(".");
        const payload = JSON.parse(atob(payloadBase64));
        const exp = payload.exp;
        return Date.now() >= exp * 1000;
    } catch (e) {
        console.error("Failed to decode token:", e);
        return true; // Treat as expired if invalid
    }
}

// Attempt to refresh the token
export async function initializeSession(token, user_id) {
    if (!token?.token || !user_id) return null;

    const expired = isTokenExpired(token.expires_in);
    if (!expired) {
        return token; // Already valid
    }

    try {
        const response = await axios.post(
            `${BACKEND_URL}/auth/refresh`,
            { user_id: user_id },
            {
                headers: {
                    Authorization: `Bearer ${token.token}`,
                    "Content-Type": "application/json",
                },
            }
        );

        if (response.status !== 200 || !response.data.access_token) {

            console.warn("Invalid response during token refresh");
            return { success: false };
        }

        return { success: true, data: response.data }

    } catch (error) {
        console.error("Token refresh failed:", error.message);
        return { success: false };
    }
}



export const Login = async (form) => {
  if (!form || typeof form !== 'object') {
    return { success: false, message: 'Invalid login data provided.' };
  }

  try {
    const response = await axios.post(`${BACKEND_URL}/auth/login`, form, {
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if ([200, 201].includes(response.status)) {
      return { success: true, data: response.data };
    }

    return {
      success: false,
      message: `Unexpected response status: ${response.status}`
    };
  } catch (error) {
    return {
      success: false,
      message: error?.response?.data?.detail || error.message || 'Login failed. Please try again.',
      data: error?.response?.data
    };
  }
};


export const Signup = async (form) => {
  if (!form || typeof form !== 'object') {
    return { success: false, message: 'Invalid signup data provided.' };
  }

  try {
    const response = await axios.post(`${BACKEND_URL}/auth/sign-up`, form, {
      headers: {
        'Content-Type': 'application/json'
      }
    });

    if ([200, 201].includes(response.status)) {
      return { success: true, data: response.data };
    }

    return {
      success: false,
      message: `Unexpected response status: ${response.status}`
    };
  } catch (error) {
    return {
      success: false,
      message: error?.response?.data?.detail || error.message || 'Signup failed. Please try again.',
      data: error?.response?.data
    };
  }
};


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
        return { success: false, message: 'Invalid password data.' };
    }

    try {
        const response = await axios.post(`${BACKEND_URL}/auth/reset-password`, null, {
            params: {
                verifier: form.verifier,
                password: form.password,
                confirmPassword: form.confirmPassword
            }
        });

        if ([200, 201].includes(response.status)) {
            return { success: true, data: response.data };
        }

        return {
            success: false,
            message: `Unexpected response status: ${response.status}`
        };
    } catch (error) {
        return {
            success: false,
            message:
                error?.response?.data?.detail ||
                error?.message ||
                'An error occurred while resetting the password.',
            data: error?.response?.data
        };
    }
};
