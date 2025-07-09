import axios from 'axios';
import { B_URl } from './auth';

const BACKEND_URL = `${B_URl}/api`;

// Generic API fetcher
const fetchMeta = async (endpoint, token = null, queryParams = {}, fallback = []) => {
  try {
    const response = await axios.get(`${BACKEND_URL}${endpoint}`, {
      headers: token ? { Authorization: `Bearer ${token.token}` } : {},
      params: queryParams
    });

    if ([200, 201].includes(response.status)) {
      return { success: true, data: response.data };
    } else {
      return {
        success: false,
        message: `Unexpected response status: ${response.status}`,
        data: fallback
      };
    }
  } catch (error) {
    return {
      success: false,
      message: error?.response?.data?.detail || error.message || 'An error occurred',
      data: fallback
    };
  }
};

// Fetch followers of a recipe
export const fetchFollowers = async (token = null, recipeId, queryParams = {}) => {
  return await fetchMeta(`/recipes/${recipeId}/followers`, token, queryParams, []);
};

// Fetch comments of a recipe
export const fetchComments = async (token = null, recipeId, queryParams = {}) => {
  return await fetchMeta(`/recipes/comments`, token, queryParams, []);
};

// Fetch likes of a recipe
export const fetchLikes = async (token = null, recipeId, queryParams = {}) => {
  return await fetchMeta(`/recipes/${recipeId}/likes`, token, queryParams, []);
};


// Like or Unlike a recipe (toggle)
export const like_unlike = async (token = null, recipeId) => {
  if (!token || !recipeId) {
    return {
      success: false,
      message: 'Missing token or recipe ID',
      data: null
    };
  }

  try {
    const response = await axios.post(`${BACKEND_URL}/recipes/${recipeId}/like`, {}, {
      headers: {
        Authorization: `Bearer ${token.token}`
      }
    });

    if ([200, 201].includes(response.status)) {
      return { success: true, data: response.data };
    } else {
      return {
        success: false,
        message: `Unexpected response status: ${response.status}`,
        data: null
      };
    }
  } catch (error) {
    return {
      success: false,
      message: error?.response?.data?.detail || error.message || 'An error occurred',
      data: null
    };
  }
};


export const save_unsave_favourites = async (token = null, recipeId) => {
  if (!token || !recipeId) {
    return {
      success: false,
      message: 'Missing token or recipe ID',
      data: null
    };
  }

  try {
    const response = await axios.post(`${BACKEND_URL}/recipes/${recipeId}/favourite-recipe`, {}, {
      headers: {
        Authorization: `Bearer ${token.token}`
      }
    });

    if ([200, 201].includes(response.status)) {
      return { success: true, data: response.data };
    } else {
      return {
        success: false,
        message: `Unexpected response status: ${response.status}`,
        data: null
      };
    }
  } catch (error) {
    return {
      success: false,
      message: error?.response?.data?.detail || error.message || 'An error occurred',
      data: null
    };
  }
};

export const folow_unfollow = async (token = null, chefId) => {
  if (!token || !chefId) {
    return {
      success: false,
      message: 'Missing token or Chef !',
      data: null
    };
  }

  try {
    const response = await axios.post(`${BACKEND_URL}/users/${chefId}/follow`, {}, {
      headers: {
        Authorization: `Bearer ${token.token}`
      }
    });

    if ([200, 201].includes(response.status)) {
      return { success: true };
    } else {
      return {
        success: false,
        message: `Unexpected response status: ${response.status}`,
        data: null
      };
    }
  } catch (error) {
    return {
      success: false,
      message: error?.response?.data?.detail || error.message || 'An error occurred',
      data: null
    };
  }
};


export const make_a_post = async (
    endpoint = '',
    token = null,
    bodyContent = {},
    fallback = []
) => {
    if (!token) {
        return {
            success: false,
            message: 'Kindly login to make the request!',
            data: fallback,
        }
    }

    try {
        const response = await axios.post(
            `${BACKEND_URL}${endpoint}`,
            bodyContent,
            {
                headers: {
                    Authorization: `Bearer ${token.token}`,
                    'Content-Type': 'application/json',
                },
            }
        )

        if ([200, 201].includes(response.status)) {
            return {
                success: true,
                data: response.data,
            }
        } else {
            return {
                success: false,
                message: `Unexpected response status: ${response.status}`,
                data: fallback,
            }
        }
    } catch (error) {
        return {
            success: false,
            message:
                error?.response?.data?.detail ||
                error?.response?.data?.message ||
                error.message ||
                'An unexpected error occurred',
            data: fallback,
        }
    }
}
