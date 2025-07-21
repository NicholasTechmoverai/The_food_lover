<template>
    <div class=" font-[Gill Sans]">
        <MegaMenu :model="menuItems" class="p-4 border-0 rounded-none"
            style="z-index: 1000; width: 100%; top: 0; border: 0; border-radius: 0%;"
            :style="{ background: `linear-gradient(to right, ${siteConfig?.colors?.secondary || '#f97316'} 10%, transparent)` }">

            <!-- Logo -->
            <template #start>
                <div class="flex items-center gap-3">
                    <img @click="goHome" :src="siteConfig.assets.logo" :alt="siteConfig.assets.logoAlt"
                        class="w-14 h-14 object-contain cursor-pointer" />
                    <span
                        class="hidden md:block text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-amber-400 via-purple-300 to-gray-200 dark:from-yellow-400 dark:to-gray-100"
                        style="font-family: 'Caprasimo', sans-serif;">
                        {{ siteConfig.meta.siteName }}
                    </span>
                </div>
            </template>



            <!-- Menu Items -->
            <template #item="{ item }" style="background-color: #d97706;">
                <!-- Root Link -->
                <a v-if="item.root"
                    class="flex items-center text-gray-300 dark:text-gray-100  font-semibold cursor-pointer px-5 py-3 text-lg transition-all duration-300 hover:border-b hover:border-purple-400 rounded-lg font-gill-sans"
                    :class="{
                        'text-amber-400 border-b-2 border-amber-400': item.isActive,
                        'text-gray-700 dark:text-gray-100': !item.isActive,
                        'dark:hover:text-amber-300': !item.isActive
                    }">
                    <span>{{ item.label }}</span>
                    <i class="pi pi-angle-down text-gray-400 ml-2 dark:text-purple-200"></i>
                </a>

                <!-- <div class="max-h-[70vh] overflow-y-auto"> 
\                     
                </div> -->
                <!-- Simple Item -->
                <a v-else-if="!item.image"
                    class="flex items-center  p-4 gap-3 rounded-lg cursor-pointer transition-all hover:bg-white/10 dark:hover:bg-white/5 group">
                    <span
                        class="flex items-center justify-center w-12 h-12 rounded-full shadow transition-transform group-hover:scale-110"
                        :style="{ backgroundColor: item.color, border: `2px solid ${item.borderColor || '#fff'}` }">
                        <i :class="[item.icon, 'text-white text-xl']"></i>
                    </span>
                    <div class="flex flex-col">
                        <span class="text-gray-900 dark:text-white font-bold text-lg">{{ item.label }}</span>
                        <span class="text-sm text-gray-600 dark:text-gray-300">{{ item.subtext }}</span>
                        <div class="flex items-center gap-2 mt-1">
                            <span v-if="item.time"
                                class="text-xs px-2 py-0.5 bg-gray-200 dark:bg-gray-700 text-amber-600 dark:text-amber-300 rounded-full flex items-center gap-1">
                                <i class="pi pi-clock text-[0.6rem]"></i> {{ item.time }}
                            </span>
                            <span v-if="item.tip"
                                class="text-xs flex items-center gap-1 text-amber-500 dark:text-amber-400">
                                <i class="pi pi-info-circle"></i> {{ item.tip }}
                            </span>
                        </div>
                    </div>
                </a>

                <!-- Recipe Card -->
                <div v-else
                    class="flex flex-col gap-3 p-3  bg-white/10 dark:bg-black/30 rounded-lg shadow-inner hover:shadow-lg transition-all border border-gray-300 dark:border-gray-600 hover:border-amber-400/40">
                    <div class="relative">
                        <img :src="item.image" alt="food" class="w-full h-[180px] object-cover rounded-lg" />
                        <span v-if="item.difficulty"
                            class="absolute top-2 right-2 text-xs px-2 py-1 rounded-full font-bold capitalize" :class="{
                                'bg-green-600/90 text-white': item.difficulty === 'Easy',
                                'bg-amber-500/90 text-white': item.difficulty === 'Medium',
                                'bg-red-600/90 text-white': item.difficulty === 'Hard'
                            }">
                            {{ item.difficulty }}
                        </span>
                    </div>

                    <div class="text-gray-800 dark:text-gray-200 space-y-2">
                        <h3 class="font-bold text-lg text-gray-900 dark:text-white">{{ item.subtext }}</h3>
                        <div class="flex justify-between items-center">
                            <div class="flex items-center gap-1">
                                <i v-for="star in 5" :key="star" :class="[
                                    'pi',
                                    star <= item.rating ? 'pi-star-fill text-amber-400' : 'pi-star text-gray-400 dark:text-gray-600'
                                ]"></i>
                                <span class="text-sm text-gray-500 dark:text-gray-400 ml-1">({{ item.reviews }})</span>
                            </div>
                            <div class="flex items-center gap-2">
                                <span v-if="item.time"
                                    class="text-xs px-2 py-1 bg-gray-200 dark:bg-gray-700 text-amber-600 dark:text-amber-300 rounded-full flex items-center gap-1">
                                    <i class="pi pi-clock text-[0.6rem]"></i> {{ item.time }}
                                </span>
                                <span v-if="item.calories"
                                    class="text-xs px-2 py-1 bg-gray-200 dark:bg-gray-700 text-purple-600 dark:text-purple-300 rounded-full flex items-center gap-1">
                                    <i class="pi pi-bolt text-[0.6rem]"></i> {{ item.calories }} kcal
                                </span>
                            </div>
                        </div>
                    </div>

                    <Button :label="item.label"
                        class="w-full text-amber-500 dark:text-amber-400 border-amber-500 dark:border-amber-400 hover:bg-amber-500/10 dark:hover:bg-amber-400/10 font-bold mt-2"
                        outlined />
                </div>

            </template>

            <!-- Right Icons -->
            <template #end>
                <div v-if="user && user.id" class="flex items-center gap-3">
                    <Button @click="router.push('/saved')" icon="pi pi-bookmark" severity="secondary" rounded
                        aria-label="Saved"
                        class="border-purple-400 dark:border-purple-300 text-purple-400 dark:text-purple-300 hover:bg-purple-400/10 dark:hover:bg-purple-300/10 w-10 h-10" />
                    <div class="relative">
                        <router-link to="/notifications">
                            <Button icon="pi pi-bell" aria-haspopup="true" severity="secondary" rounded
                                aria-label="Notifications"
                                class="border-amber-400 dark:border-amber-300 text-amber-400 dark:text-amber-300 hover:bg-amber-400/10 dark:hover:bg-amber-300/10 w-10 h-10" />


                            <span
                                class="absolute -top-1 -right-1 w-4 h-4 bg-red-500 text-white text-xs rounded-full flex items-center justify-center">
                                {{ notifications.notificationsCount.all }}
                            </span>
                        </router-link>
                        <!-- <TieredMenu ref="noty_menu" id="overlay_tmenu" :model="noty_menu_items" popup /> -->
                    </div>
                    <div class="card flex justify-center">
                        <Avatar :image="user.profilePic" aria-haspopup="true" @click="toggle" shape="circle"
                            size="large"
                            class="border-2 border-amber-500 dark:border-amber-400 cursor-pointer hover:scale-105 transition-transform" />
                        <TieredMenu ref="menu" id="overlay_tmenu" :model="Menu_items" popup />
                    </div>
                </div>
                <div v-else class="flex items-center space-x-3 shrink-0">
                    <router-link to="/register/login">
                        <component :is="LoginButton" :theme="siteConfig.colors.secondary"
                            class="transition duration-150 ease-in-out hover:opacity-90" aria-label="Login" />
                    </router-link>

                    <router-link to="/register/signup">
                        <component :is="SignupButton" :theme="siteConfig.colors.secondary"
                            class="transition duration-150 ease-in-out hover:opacity-90" aria-label="Sign up" />
                    </router-link>


                    <i class="pi pi-spin pi-cog" :style="{ color: siteConfig.colors.secondary }"
                        @click="router.push('/settings/preferences')" style="font-size: 1rem; cursor: pointer;"></i>

                </div>

            </template>

        </MegaMenu>

    </div>
</template>


<script setup>
import { ref } from "vue";
// import {  useIsMobile } from '../reusables';
import { useSiteStore } from '../config/siteConfig.js'
import SignupButton from "../cards/SignupButton.vue";
import LoginButton from "../cards/LoginButton.vue";
import { useAuthStore, useNotificationStore } from '../store/user.js'
import router from "../router/index.js";
import { goHome, polishUrlName } from "../reusables/index.js"
import { Logout } from "../apis/auth.js";

const auth = useAuthStore()
const notifications = useNotificationStore()
const { siteConfig, getResponsiveValue } = useSiteStore()

const menu = ref();
const noty_menu = ref();
const props = defineProps({
    user: {
        type: Object,
        default: () => ({
            profilePic: 'https://cdn-icons-png.flaticon.com/512/3135/3135715.png',
            id: null,
            name: null
        })
    }
})




const noty_menu_items = ref([
    {
        label: () => `Likes (${notifications.notificationsCount.likes})`,
        icon: 'pi pi-heart',
        command: () => {
            router.push('/notifications?tab=likes')
        }
    },
    {
        label: () => `Messages (${notifications.notificationsCount.comment})`,
        icon: 'pi pi-comments',
        command: () => {
            router.push('/notifications?tab=mentions')
        }
    },
    {
        label: () => `Mentions (${notifications.notificationsCount.system})`,
        icon: 'pi pi-at',
        command: () => {
            router.push('/notifications?tab=mentions')
        }
    }
]);

const Menu_items = ref([

    {
        label: 'Recipes',
        icon: 'pi pi-book',
        command: () => {
            router.push('/recipes');
        }
    },
    {
        label: 'Cooking Tips',
        icon: 'pi pi-list',
        command: () => {
            router.push('/cooking-tips');
        }
    },
    {
        label: 'Settings',
        icon: 'pi pi-cog',
        items: [
            {
                label: 'Preferences',
                icon: 'pi pi-sliders-h',
                command: () => {
                    router.push('/settings/preferences');
                }
            },
            {
                label: 'Admin Panel',
                icon: 'pi pi-shield',
                command: () => {
                    router.push('/settings/admin')
                }
            }
        ]
    },
    {
        label: 'Reports',
        icon: 'pi pi-chart-bar',
        command: () => {
            console.log('📊 Opening reports dashboard...');
        }
    },
    {
        separator: true
    },
    {
        label: 'New recipe',
        icon: 'pi pi-plus',
        command: () => {
            router.push('/recipes/new/cover'); // ✅ clean, avoids redirect
        }
    },
    {
        label: auth.user?.name ? auth.user.name : 'Login',
        icon: auth.user?.name ? 'pi pi-user' : 'pi pi-sign-in',
        command: async () => {
            if (!auth.user?.id) {
                router.push('/register/login');
                return;
            }
            router.push(`/${auth.user.name}`);
        }
    }
]);


const toggle = (event) => {
    menu.value.toggle(event);
};
const Notytoggle = (event) => {
    noty_menu.value.toggle(event);
};


// Recipe categories
const rawRecipes = {
    label: 'Recipes',
    root: true,
    items: [
        [
            {
                items: [
                    {
                        label: 'Italian Classics',
                        icon: 'pi pi-pizza-slice',
                        subtext: 'Authentic pasta & pizza recipes',
                        color: '#7e22ce',
                        tip: 'Use 00 flour for perfect pizza dough',
                        titleColor: '#7e22ce',
                        command: () => {
                            console.log(`opening ${label}`);
                            router.push(`/recipes/${polishUrlName(label)}`)
                        }
                    },
                    {
                        label: 'Asian Delights',
                        icon: 'pi pi-utensils',
                        subtext: 'Sushi, stir-fry & more',
                        color: '#d946ef',
                        tip: 'Marinate proteins for at least 30 minutes'
                    },
                    {
                        label: 'Mediterranean',
                        icon: 'pi pi-leaf',
                        subtext: 'Healthy & flavorful dishes',
                        color: '#8b5cf6',
                        tip: 'Use extra virgin olive oil for best flavor'
                    }
                ]
            }
        ],
        [
            {
                items: [
                    {
                        label: 'Quick Meals',
                        icon: 'pi pi-clock',
                        subtext: 'Under 30 minutes',
                        color: '#f59e0b',
                        tip: 'Prep ingredients before starting',
                        titleColor: '#b45309'
                    },
                    {
                        label: 'Baking',
                        icon: 'pi pi-pie-chart',
                        subtext: 'Breads & desserts',
                        color: '#f97316',
                        tip: 'Room temperature ingredients mix better'
                    },
                    {
                        label: 'Vegetarian',
                        icon: 'pi pi-carrot',
                        subtext: 'Plant-based goodness',
                        color: '#10b981',
                        tip: 'Combine proteins for complete amino acids'
                    }
                ]
            }
        ],
        [
            {
                items: [
                    {
                        label: 'Seasonal Specials',
                        icon: 'pi pi-sun',
                        subtext: 'Fresh seasonal recipes',
                        color: '#ec4899',
                        tip: 'Buy produce in season for best flavor'
                    },
                    {
                        label: 'Cocktails',
                        icon: 'pi pi-wine-glass',
                        subtext: 'Drinks & pairings',
                        color: '#6366f1',
                        tip: 'Chill glasses before serving'
                    },
                    {
                        label: 'Meal Prep',
                        icon: 'pi pi-calendar',
                        subtext: 'Weekly planning',
                        color: '#3b82f6',
                        tip: 'Cook grains and proteins in bulk'
                    }
                ]
            }
        ],
        [
            {
                items: [{
                    image: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    label: 'VIEW ALL RECIPES',
                    subtext: 'Over 500 chef-approved recipes',
                    rating: 4,
                    reviews: 1284
                }]
            }
        ]
    ]
};


function enhanceRecipeItems(data) {
    return {
        ...data,
        items: data.items.map(group =>
            group.map(section => ({
                ...section,
                items: section.items.map(item => ({
                    ...item,
                    command: item.label
                        ? () => {
                            const url = `/recipes/${polishUrlName(item.label)}`;
                            url.includes('view-all-recipes') ? router.push('/recipes') : router.push(url);
                        }
                        : undefined
                }))
            }))
        )
    };
}

const recipes = enhanceRecipeItems(rawRecipes);


// Cooking Tips
const rawCookingTips = {
    label: 'Cooking Tips',
    root: true,
    items: [
        [
            {
                items: [
                    {
                        label: 'KnifeSkills',
                        icon: 'pi pi-cut',
                        subtext: 'Master chopping techniques',
                        color: '#6b7280',
                        tip: 'Keep knives sharp for safety'
                    },
                    {
                        label: 'FlavourPairing',
                        icon: 'pi pi-heart',
                        subtext: 'Perfect combinations',
                        color: '#6b7280',
                        tip: 'Balance sweet, salty, sour, bitter'
                    }
                ]
            }
        ],
        [
            {
                items: [
                    {
                        label: 'TimeSaving',
                        icon: 'pi pi-stopwatch',
                        subtext: 'Efficiency in kitchen',
                        color: '#6b7280',
                        tip: 'Clean as you cook'
                    },
                    {
                        label: 'Substitutions',
                        icon: 'pi pi-sync',
                        subtext: 'Ingredient alternatives',
                        color: '#6b7280',
                        tip: 'Greek yogurt for sour cream'
                    }
                ]
            }
        ],
        [
            {
                items: [
                    {
                        label: 'Presentation',
                        icon: 'pi pi-palette',
                        subtext: 'Plate like a pro',
                        color: '#6b7280',
                        tip: 'Odd numbers look more appealing'
                    },
                    {
                        label: 'Equipment',
                        icon: 'pi pi-box',
                        subtext: 'Essential tools',
                        color: '#6b7280',
                        tip: 'Invest in a good chef knife'
                    }
                ]
            }
        ],
        [
            {
                items: [{
                    image: 'https://images.unsplash.com/photo-1606787366850-de6330128bfc?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
                    label: 'MORE TIPS',
                    subtext: 'Become a kitchen expert',
                    rating: 5,
                    reviews: 892
                }]
            }
        ]
    ]
};

function enhanceCookingTipsItems(data) {
    return {
        ...data,
        items: data.items.map(group =>
            group.map(section => ({
                ...section,
                items: section.items.map(item => ({
                    ...item,
                    command: item.label
                        ? () => {
                            const url = `/cooking-tips/${polishUrlName(item.label).replace()}`;
                            url.includes('more-tips') ? router.push('/cooking-tips') : router.push(url);
                        }
                        : undefined
                }))
            }))
        )
    };
}

const cookingTips = enhanceCookingTipsItems(rawCookingTips);

// For Food Lovers
const foodLovers = {
    label: 'For Food Lovers',
    root: true,
    items: [
        // First column - Featured recipes
        [
            {
                label: 'Featured Recipes',
                items: [
                    // {
                    //     image: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c',
                    //     label: 'VIEW RECIPE',
                    //     subtext: 'Rainbow Buddha Bowl with Tahini Dressing',
                    //     rating: 4.8,
                    //     reviews: 5243,
                    //     time: '25 mins',
                    //     difficulty: 'Easy',
                    //     calories: 420
                    // },
                    {
                        image: 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd',
                        label: 'LEARN TECHNIQUE',
                        subtext: 'Perfect Pan-Seared Salmon with Crispy Skin',
                        rating: 4.7,
                        reviews: 3891,
                        time: '15 mins',
                        difficulty: 'Medium',
                        calories: 320
                    }
                ]
            }
        ],

        // Second column - Quick meals
        [
            {
                label: 'Quick Meals',
                items: [
                    {
                        label: '15-Minute Pasta',
                        icon: 'pi pi-clock',
                        subtext: 'Creamy garlic mushroom pasta',
                        color: '#8b5cf6',
                        tip: 'Use pasta water to thicken sauce',
                        borderColor: '#ddd6fe',
                        time: '15 mins'
                    },
                    {
                        label: 'Avocado Toast',
                        icon: 'pi pi-heart',
                        subtext: '5 delicious variations',
                        color: '#10b981',
                        tip: 'Sprinkle with chili flakes',
                        borderColor: '#a7f3d0',
                        time: '5 mins'
                    }
                ]
            }
        ],

        // Third column - Global favorites
        [
            {
                label: 'Global Favorites',
                items: [
                    {
                        label: 'Tacos Al Pastor',
                        icon: 'pi pi-star',
                        subtext: 'Marinated pork with pineapple',
                        color: '#ea580c',
                        tip: 'Use achiote paste for authentic flavor',
                        borderColor: '#fed7aa',
                        time: '45 mins'
                    },
                    {
                        label: 'Japanese Ramen',
                        icon: 'pi pi-star',
                        subtext: 'Rich tonkotsu broth',
                        color: '#3b82f6',
                        tip: 'Simmer bones for 12+ hours',
                        borderColor: '#bfdbfe',
                        time: '14 hrs'
                    }
                ]
            }
        ],

        // Fourth column - Seasonal picks
        [
            {
                label: 'Seasonal Picks',
                items: [
                    // {
                    //     image: 'https://images.unsplash.com/photo-1490645935967-10de6ba17061',
                    //     label: 'COOK NOW',
                    //     subtext: 'Summer Berry Pavlova with Whipped Cream',
                    //     rating: 4.9,
                    //     reviews: 2104,
                    //     time: '1.5 hrs',
                    //     difficulty: 'Medium',
                    //     calories: 280
                    // },
                    {
                        image: 'https://images.unsplash.com/photo-1473093295043-cdd812d0e601',
                        label: 'SAVE RECIPE',
                        subtext: 'Hearty Winter Beef Stew with Root Vegetables',
                        rating: 4.8,
                        reviews: 4321,
                        time: '3 hrs',
                        difficulty: 'Easy',
                        calories: 380
                    }
                ]
            }
        ]
    ]
};
const menuItems = ref([recipes, cookingTips, foodLovers]);
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Caprasimo&display=swap');

.font-caprasimo {
    font-family: 'Caprasimo', sans-serif;
}

.font-gill-sans {
    font-family: 'Gill Sans', 'Gill Sans MT', Calibri, 'Trebuchet MS', sans-serif;
}

.card {
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    z-index: 1000;
    position: sticky !important;
    top: 0 !important;
}

/* Smooth transitions */
a {
    transition: all 0.2s ease;
}

/* Gradient text for active items */
.mega-menu-item-active {
    background: linear-gradient(90deg, #7e22ce 0%, #f59e0b 100%);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
</style>