import axios from 'axios'
import { ref } from "vue";

import { B_URl } from './auth';
const BACKEND_URL = `${B_URl}/api`


const runtime_recipes = [
    {
        id: 1,
        recipeName: 'Beef, Potato, minji stew paired with chapati',
        repiceColor: '#4CAF50',
        image: 'https://scontent-mba2-1.xx.fbcdn.net/v/t39.30808-6/515074318_3827249284085807_3021664056451603544_n.jpg?stp=dst-jpg_s600x600_tt6&_nc_cat=109&ccb=1-7&_nc_sid=833d8c&_nc_ohc=bDdTIWO-B80Q7kNvwFjH2Gw&_nc_oc=Admzd9mhnHOUYprhS_rTPFuMBh6gQkJvbXAKjPITPVrnCeNfv59OYk_l_Ff4xsyty953O3tiRwhwVcDL2L_3_zH-&_nc_zt=23&_nc_ht=scontent-mba2-1.xx&_nc_gid=89IYoSHZDH7VEWb7mmFqHQ&oh=00_AfPPi6ER1ZhpvsIwNrK8zmk1L36zDAcxQAPSjtJ2TrUhYA&oe=686AF17D',
        tags: ['staple', 'vegetarian', 'quick'],
        cookTime: { hr: 0, min: 30 },
        description: `Mko??ka lunch kameiva 🥰🥰🥰
Beef, Potato, minji stew paired with chapat😋😋
Stew Procedure step by step `,
        cuisine: { name: 'Kenyan', region: 'East Africa' },
        complexityLevel: { name: 'Easy', value: 1 },
        category: ['Main Dish', 'Vegetarian'],
        user: {
            name: 'Ruth Larry',
            profilePic: 'https://scontent-mba2-1.xx.fbcdn.net/v/t39.30808-1/481276179_3648159808661423_1019282035979287835_n.jpg?stp=cp0_dst-jpg_s40x40_tt6&_nc_cat=1&ccb=1-7&_nc_sid=1d2534&_nc_ohc=14YrcRVGBxEQ7kNvwGRSjnM&_nc_oc=Adnn2g2NBZSJEBvKh6Qbq9xfe2fJ_sXk9acTLqlus5ilGnLeVuH091I5Bn2eNxMyCMUDJR4VnjEO4c0wwGek62Po&_nc_zt=24&_nc_ht=scontent-mba2-1.xx&_nc_gid=7TrIHQcmXeV_rsgc32U0iQ&oh=00_AfNs54D65wXvQwKhHAV2wooFtweuN93MJEux9VJAwusPiw&oe=686ADF24',
            id: 'user_001',
            totalRecipes: 27,
            isVerified: true
        }
    },
    {
        id: 2,
        recipeName: 'Nyama Choma',
        repiceColor: '#8B0000',
        image: 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1',
        tags: ['grilled', 'meat', 'festive'],
        cookTime: { hr: 2, min: 30 },
        description: `<p>Kenya's famous <b>charcoal-grilled meat</b>, typically goat or beef. The meat is first boiled with spices then finished over charcoal for maximum flavor.</p><p>Served with <i>kachumbari</i> (tomato-onion salad) and cold Tusker beer for the full Kenyan experience.</p>`,
        cuisine: { name: 'Kenyan', region: 'East Africa' },
        complexityLevel: { name: 'Medium', value: 2 },
        category: ['Main Dish', 'Meat'],
        user: {
            name: 'Chef Mwangi',
            profilePic: 'https://randomuser.me/api/portraits/men/32.jpg',
            id: 'user_002',
            totalRecipes: 42,
            isVerified: true
        }
    }
];

const recipeTypes = [
    {
        title: "Breakfast",
        description: "Start your day right",
        gradient: "#ff7e5f, #feb47b",
        image: "https://images.unsplash.com/photo-1557142046-c704a3adf364?w=200&h=200&fit=crop",
    },
    {
        title: "Vegan",
        description: "Plant-powered goodness",
        gradient: "#6a11cb, #2575fc",
        image: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=200&h=200&fit=crop",
    },
    {
        title: "Desserts",
        description: "Sweet tooth treats",
        gradient: "#00c6ff, #0072ff",
        image: "https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=200&h=200&fit=crop",
    },
    {
        title: "Grilled",
        description: "Smoky & savory",
        gradient: "#ff512f, #dd2476",
        image: "https://images.unsplash.com/photo-1558030006-450675393462?w=200&h=200&fit=crop",
    },
    {
        title: "Soups",
        description: "Warm & comforting",
        gradient: "#ffb6c1, #ff69b4",
        image: "https://images.unsplash.com/photo-1547592180-85f173990554?w=200&h=200&fit=crop",
    },
    {
        title: "Salads",
        description: "Crisp & fresh",
        gradient: "#ff9a8b, #ffc3a0",
        image: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=200&h=200&fit=crop",
    },
    {
        title: "Pasta",
        description: "Italian favorites",
        gradient: "#a1c4fd, #c2e9fb",
        image: "https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?w=200&h=200&fit=crop",
    },
    {
        title: "Seafood",
        description: "Ocean delights",
        gradient: "#fbc2eb, #a18cd1",
        image: "https://images.unsplash.com/photo-1585238342024-78d387f4a707?w=200&h=200&fit=crop",
    },
    {
        title: "Snacks",
        description: "Quick bites",
        gradient: "#84fab0, #8fd3f4",
        image: "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=200&h=200&fit=crop",
    },
];
const liveRecipes = [
    {
        live: true,
        date: '2025-07-20',
        meal: 'Ugali Pasta with Special Sauce and Extra Toppings',
        chef: {
            profilePic: '',
            name: 'Chef John Doe',
            id: '1',
        }
    },
    {
        live: true,
        date: '2025-07-20',
        meal: 'Chapati Beans',
        chef: {
            profilePic: 'https://randomuser.me/api/portraits/men/32.jpg',
            name: 'Chef Maria',
            id: '2',
        }
    },
    {
        live: false,
        date: '2025-07-21',
        meal: 'Pilau with Kachumbari',
        chef: {
            profilePic: 'https://randomuser.me/api/portraits/women/44.jpg',
            name: 'Chef Amina',
            id: '3',
        }
    },
    {
        live: true,
        date: '2025-07-22',
        meal: 'Nyama Choma Special',
        chef: {
            profilePic: 'https://randomuser.me/api/portraits/men/75.jpg',
            name: 'Chef Kamau',
            id: '4',
        }
    },
    {
        live: false,
        date: '2025-07-23',
        meal: 'Mukimo with Greens',
        chef: {
            profilePic: 'https://randomuser.me/api/portraits/women/68.jpg',
            name: 'Chef Wanjiku',
            id: '5',
        }
    },
    {
        live: true,
        date: '2025-07-24',
        meal: 'Fish Curry with Coconut Rice',
        chef: {
            profilePic: 'https://randomuser.me/api/portraits/men/90.jpg',
            name: 'Chef Ali',
            id: '6',
        }
    },
    {
        live: false,
        date: '2025-07-25',
        meal: 'Vegetable Stir Fry with Noodles',
        chef: {
            profilePic: 'https://randomuser.me/api/portraits/women/33.jpg',
            name: 'Chef Lin',
            id: '7',
        }
    },
    {
        live: true,
        date: '2025-07-26',
        meal: 'Mandazi with Chai',
        chef: {
            profilePic: 'https://randomuser.me/api/portraits/men/22.jpg',
            name: 'Chef Bakari',
            id: '8',
        }
    },
    {
        live: false,
        date: '2025-07-27',
        meal: 'Githeri Special',
        chef: {
            profilePic: 'https://randomuser.me/api/portraits/women/29.jpg',
            name: 'Chef Njeri',
            id: '9',
        }
    },
    {
        live: true,
        date: '2025-07-28',
        meal: 'Bhajia with Tamarind Sauce',
        chef: {
            profilePic: 'https://randomuser.me/api/portraits/men/45.jpg',
            name: 'Chef Raj',
            id: '10',
        }
    }
];
export const recipesSteps = ref([
    {
        id: 1,
        name: 'Beef, Potato, minji stew',
        description: 'Beef, Potato, minji stew paired with chapat😋😋\
Stew Procedure step by step ',
        category: 'dinner',
        ingredients: [
            { name: 'Maize flour', amount: '2', unit: 'cups' },
            { name: 'Sukuma wiki', amount: '1', unit: 'bunch' },
            { name: 'Onion', amount: '1', unit: 'medium' },
            { name: 'Tomatoes', amount: '2', unit: '' },
            { name: 'Vegetable oil', amount: '2', unit: 'tbsp' }
        ],
        steps: [
            {
                no: 1,
                timeRequired: { hr: 0, min: 5 },
                ingredientsUsed: ['Onion', 'Vegetable oil'],
                instructions: 'Ingredients beef, Potato, onions, tomatoes, carrots, paprika, curry powder, salt, seasoning cubes and cooking oil',
                image: 'https://scontent-mba2-1.xx.fbcdn.net/v/t39.30808-6/515292989_3827251494085586_6149290803587200447_n.jpg?stp=dst-jpg_s600x600_tt6&_nc_cat=110&ccb=1-7&_nc_sid=833d8c&_nc_ohc=kujPOSKJMCoQ7kNvwE2Rqie&_nc_oc=AdkRyliG2dFqTzuHHt5fepq7-42pLW1GpLxv6YPF1yd1GIefDshKa5g8JPH9fWywlJNQj1-91YCVPZX5ywN7LtOS&_nc_zt=23&_nc_ht=scontent-mba2-1.xx&_nc_gid=89IYoSHZDH7VEWb7mmFqHQ&oh=00_AfNZLPzzTbVmiHehI7rj2i_BHY357iqmPJBruaqLlMvHiQ&oe=686B0719',
                videoUrl: ''
            },
            {
                no: 2,
                timeRequired: { hr: 0, min: 8 },
                ingredientsUsed: ['onions'],
                instructions: 'Sautee onions',
                image: 'https://scontent-mba2-1.xx.fbcdn.net/v/t39.30808-6/514948818_3827252327418836_5476940899897752525_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=833d8c&_nc_ohc=chT1MxtoDNgQ7kNvwGvh7Op&_nc_oc=AdkdWrz0_MYvq1BQcTR_WydjLTR-TdEm5JguEu7nH4XX9lff1grU2eAZ0eCd_Lt1ilAdFLUqDCUgSU7gDrUOTLzM&_nc_zt=23&_nc_ht=scontent-mba2-1.xx&_nc_gid=Ukd9fmZjKTNGl9BrVFbS8A&oh=00_AfM_otaQch7021beGbA-ZM2AiWVPIaKAwl4255A7hZX0Mw&oe=686B116B',
                videoUrl: ''
            },
            {
                no: 3,
                timeRequired: { hr: 0, min: 15 },
                tempRequired: 100,
                ingredientsUsed: ['paprika', 'curry powder'],
                instructions: `Add paprika,curry powder stir and let it cook until fragrant`,
                image: 'https://scontent-mba2-1.xx.fbcdn.net/v/t39.30808-6/514688919_3827252700752132_5416736835830599229_n.jpg?stp=dst-jpg_tt6&cstp=mx2048x1761&ctp=s2048x1761&_nc_cat=103&ccb=1-7&_nc_sid=833d8c&_nc_ohc=C8JYkLirYoQQ7kNvwGRw5jq&_nc_oc=AdkPITfI7W3iEwdM-EsuyYWUrLNeuphhOtHrY_2KaYIhvsTx1lBV5oeDISxFzRgI-J9EeU4G_DOFsdVKznyke_XY&_nc_zt=23&_nc_ht=scontent-mba2-1.xx&_nc_gid=mdU1i0fEklY8x--AX9jOYA&oh=00_AfPL3-5QWxiQftT12AX-2tz0IwxK6K6q6pumR2b1RlGgdw&oe=686AE2DC',
                videoUrl: ''
            },
            {
                no: 4,
                timeRequired: { hr: 0, min: 15 },
                tempRequired: 100,
                ingredientsUsed: ['preboiled beef'],
                instructions: `Add preboiled beef stir and let it cook until golden`,
                image: 'https://scontent-mba2-1.xx.fbcdn.net/v/t39.30808-6/514530503_3827253807418688_7802296055289028848_n.jpg?_nc_cat=107&ccb=1-7&_nc_sid=833d8c&_nc_ohc=gfHkFkOCqBAQ7kNvwEu5xuC&_nc_oc=AdkzaihNSq8BgebFmb2Cvm3PTPH1W-dCqlj66G5THKtYhl3LPKB1BcuLOVffttR8n5cV5wddK-hCGqSiebk4QG2a&_nc_zt=23&_nc_ht=scontent-mba2-1.xx&_nc_gid=NjEwe_iB-KBn7LuoF2tHPg&oh=00_AfN_XA6XBcF6RyEDX551yY_wyPh5eu45R4Pe-_LK04UVxg&oe=686AF090',
                videoUrl: ''
            }, {
                no: 5,
                timeRequired: { hr: 0, min: 15 },
                tempRequired: 10,
                ingredientsUsed: ['paprika', 'curry powder'],
                instructions: `Like so`,
                image: 'https://scontent-mba2-1.xx.fbcdn.net/v/t39.30808-6/514534584_3827254644085271_7552588726397617678_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=833d8c&_nc_ohc=LFnozi3kc2EQ7kNvwER0Rrq&_nc_oc=Adm_u-OjSNSDInylVMhgMiz0ckFZv-W8KTFP2lBinvgN-xXv-MwiJLLX59OAkHALrTmNA7aQHnYuev9-U4kNhEKu&_nc_zt=23&_nc_ht=scontent-mba2-1.xx&_nc_gid=KT-ZPXOO1ZSFXStL1okW5A&oh=00_AfMKb98unI4gasdhF9BGDKgH0TdXtnACdzQA3yUJk41sNw&oe=686AE65E',
                videoUrl: ''
            }, {
                no: 6,
                timeRequired: { hr: 0, min: 15 },
                tempRequired: 100,
                ingredientsUsed: ['paprika', 'curry powder'],
                instructions: `Potato, beef,minji stew `,
                image: 'https://scontent-mba2-1.xx.fbcdn.net/v/t39.30808-6/515046553_3827250017419067_1296367899331253428_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=833d8c&_nc_ohc=HY21yfQJ75EQ7kNvwGhOHz9&_nc_oc=AdnjJE9MSEtInLj07TkwBkEDoA1xFNVd07tBmaCuT7m7tmXVLZFA0TBLmJQk0gPXmGMcJvx8eBZE3HJSnxvN91HP&_nc_zt=23&_nc_ht=scontent-mba2-1.xx&_nc_gid=FAU8dW_8ieK4iM3o2y_gwg&oh=00_AfMQ3zL95OuTRdM2B5qDdAwD1Ri4rjdfExIKRF1fG6Xrpw&oe=686AFFE8',
                videoUrl: ''
            }
        ],
        tags: ['staple', 'vegetarian', 'quick']
    },
    {
        id: 2,
        name: 'Nyama Choma',
        description: 'Kenyan-style charcoal-grilled meat, traditionally goat or beef',
        category: 'dinner',
        ingredients: [
            { name: 'Goat meat', amount: '1', unit: 'kg' },
            { name: 'Garlic', amount: '4', unit: 'cloves' },
            { name: 'Ginger', amount: '1', unit: 'tbsp' },
            { name: 'Salt', amount: '', unit: 'to taste' }
        ],
        steps: [
            {
                no: 1,
                timeRequired: { hr: 1, min: 0 },
                tempRequired: 100,
                ingredientsUsed: ['Goat meat', 'Garlic', 'Ginger'],
                instructions: 'Boil meat with garlic and ginger until tender',
                image: 'choma-step1.jpg',
                videoUrl: ''
            },
            {
                no: 2,
                timeRequired: { hr: 0, min: 45 },
                tempRequired: 200,
                ingredientsUsed: ['Salt'],
                instructions: 'Grill over charcoal, turning occasionally',
                image: 'choma-step2.jpg',
                videoUrl: ''
            }
        ],
        tags: ['grilled', 'meat', 'festive']
    }
]);



export const fetchRecipes = async (token = null, filters = null) => {
  try {
    const response = await axios.post(
      `${BACKEND_URL}/recipes/get`,
      filters || {}, // ✅ this is the body
      {
        headers: token
          ? { Authorization: `Bearer ${token.token}` }
          : {},
      }
    );

    if (response.status === 200 || response.status === 201) {
      return { success: true, data: response.data };
    } else {
      return {
        success: false,
        message: `Unexpected response status: ${response.status}`,
        data: runtime_recipes,
      };
    }
  } catch (error) {
    return {
      success: false,
      message: error?.response?.data?.detail || error.message || 'An error occurred',
      data: runtime_recipes,
    };
  }
};


export const fetchRecipeSteps = async (token = null, name = null, id = null) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/recipes/${name}/${id}`, {
            headers: token ? { Authorization: `Bearer ${token.token}` } : {},
        });

        if ([200, 201].includes(response.status)) {
            return {
                success: true,
                data: {
                    cover: response.data.cover,
                    steps: response.data.steps,
                },
            };
        } else {
            return handleFetchFallback(id, `Unexpected response status: ${response.status}`);
        }
    } catch (error) {
        return handleFetchFallback(
            id,
            error?.response?.data?.detail || error.message || 'An error occurred while fetching the recipe.'
        );
    }
};

const handleFetchFallback = (id, message) => {
    const { cover, steps } = getRuntimeRecipeSteps(id);
    return {
        success: false,
        message,
        data: {
            cover,
            steps,
        },
    };
};

const getRuntimeRecipeSteps = (id) => {
    const cover = runtime_recipes.find(item => item.id === Number(id)) || {};
    const steps = recipesSteps.value.find(item => item.id === Number(id)) || [];
    return { cover, steps };
};



export const fetchRecipeTypes = async (token = null, filters = null) => {
    try {
        const response = await axios.get(`${BACKEND_URL}/recipes/types`, {
            headers: token ? { Authorization: `Bearer ${token.token}` } : {},
            params: filters || {},
        })

        if (response.status === 200 || response.status === 201) {
            return { success: true, data: response.data }
        } else {
            return {
                success: false,
                message: `Unexpected response status: ${response.status}`,
                data: recipeTypes,
            }
        }
    } catch (error) {
        return {
            success: false,
            message: error?.response?.data?.detail || error.message || 'An error occurred',
            data: recipeTypes,
        }
    }

}
export const fetchLiveRecipes = async () => {
    return liveRecipes;
}
/**
 * Save a new recipe to the backend
 * @param {Object} recipe - The recipe object to save
 * @returns {Promise<{ success: boolean, message?: string, data?: any }>}
 */

export const saveRecipe = async (token = null, recipe) => {
    if (!token) {
        return {
            success: false,
            message: 'Failed to detect user. Please login and try publishing your recipe!',
        }
    }

    console.log("TOKEN::", token)

    if (!recipe || typeof recipe !== 'object') {
        return { success: false, message: 'Invalid recipe data' }
    }

    try {
        const response = await axios.post(
            `${BACKEND_URL}/recipes/`,
            recipe,
            {
                headers: {
                    Authorization: `Bearer ${token.token}`,
                },
            }
        )

        if (response.status === 200 || response.status === 201) {
            return { success: true, data: response.data }
        } else if (response.status === 422) {
            return {
                success: false,
                message: 'Invalid data format / empty fields. Please check your input and fill basic fields.',
            };
        } else {
            return {
                success: false,
                message: `Unexpected response status: ${response.status}`,
            }
        }
    } catch (error) {
        return {
            success: false,
            message:
                error?.response?.data?.detail || // Most DRF/FastAPI backends use `detail`
                error?.response?.data?.message || // Optional fallback
                error.message ||
                'An error occurred',
        }
    }
}

export const fetchRecipeMeta = async (endpoint = '/recipes/meta', token = null, queryParams = {}, fallback = []) => {
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
}


