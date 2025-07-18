import { createRouter, createWebHistory } from 'vue-router'

// Static Imports (or use dynamic if needed)
import LandingPage from '../pages/LandingPage.vue'
import SettingsPage from '../pages/Settings.vue'
import AdminPage from '../pages/AdminPage.vue'
import PreferenceSettings from '../pages/PreferenceSettings.vue' // fixed typo
import NotFoundPage from '../pages/404Page.vue'
import RecipesPage from '../pages/RecipesPage.vue'
import NewRecipe from '../pages/NewRecipe.vue'
import RecipeId from '../pages/RecipeId.vue'
import CoverInfo from '../pages/CoverInfo.vue'
import NewRecipeUploads from '../cards/NewRecipeUploads.vue'
import PublishRecipe from '../cards/PublishRecipe.vue'
import RegisterPage from '../pages/RegisterPage.vue'
import LoginPage from '../cards/LoginCard.vue'
import SignupPage from '../cards/SignupCard.vue'
import RecoverPassword from '../cards/RecoverPassword.vue'
import RecipeType from '../pages/RecipeType.vue'
import LivePage from '../pages/livePage.vue'
import CookingTipCard from '../cards/CookingTipCard.vue'
import CookingTipsPage from '../pages/CookingTipsPage.vue'
import VerifyPage from '../cards/VerifyPage.vue'
import ProfilePage from '../pages/ProfilePage.vue'
import NotificationPage from '../pages/NotificationPage.vue'
import SavedRecipes from '../pages/SavedRecipes.vue'


const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
  },
    {
    path: '/:username',
    name: 'ProfilePage',
    component: ProfilePage,
    props: true
  },
  {
    path: '/recipes',
    name: 'RecipesPage',
    component: RecipesPage,
    children: [
      {
        path: 'new',
        name: 'NewRecipe',
        component: NewRecipe,
        children: [
          {
            path: '',
            redirect: 'cover',
          },
          {
            path: 'cover',
            name: 'CoverInfo',
            component: CoverInfo,
          },
          {
            path: 'e',
            name: 'NewRecipeUploadsBase',
            component: NewRecipeUploads,
            children: [
              {
                path: ':id',
                name: 'NewRecipeUploadsWithId',
                component: NewRecipeUploads,
                props: true
              }
            ]
          },
          {
            path: 'p',
            name: 'PublishRecipe',
            component: PublishRecipe,
            children: [
              {
                path: ':id',
                name: 'PublishRecipeWithId',
                component: PublishRecipe,
                props: true
              }
            ]
          },
        ],
      },
      {
        path: ':recipe_type',
        name: 'RecipeType',
        component: RecipeType,
        props: true,
      },
      {
        path: ':recipe_name/:recipe_id',
        name: 'RecipeId',
        component: RecipeId,
        props: true,
      },
    ],
  },
  {
    path: '/register',
    name: 'RegisterPage',
    component: RegisterPage,
    children: [
      {
        path: '',
        redirect: '/register/login',
      },
      {
        path: 'verify',
        name: 'VerifyPage',
        component: VerifyPage,
      },
      {
        path: 'login',
        name: 'LoginPage',
        component: LoginPage,
      },
      {
        path: 'signup',
        name: 'SignupPage',
        component: SignupPage,
      },
      {
        path: 'recover-password',
        name: 'RecoverPassword',
        component: RecoverPassword,
      },

    ],
  },
  {
    path: '/live',
    name: 'LivePage',
    component: LivePage,
    props: false, // parent route doesn’t need route props
    children: [
      {
        path: ':name/:author/:id',
        name: 'LiveIdPage',
        component: LivePage,
      }
    ]
  },
  {
    path: '/cooking-tips',
    name: 'CookingTipsPage',
    component: CookingTipsPage,
    props: false, // parent route doesn’t need route props
    children: [
      {
        path: ':tip/',
        name: 'CookingTipTarget',
        component: CookingTipsPage,
      }
    ]
  },
     {
    path: '/saved',
    name: 'Saved',
    component: SavedRecipes,
  },
    {
    path: '/notifications',
    name: 'Notifications',
    component: NotificationPage,
    props: false, // parent route doesn’t need route props
  },
  {
    path: '/settings',
    name: 'SettingsPage',
    component: SettingsPage,
    children: [
      {
        path: '',
        redirect: '/settings/preferences',
      },
      {
        path: 'preferences',
        name: 'PreferenceSettings',
        component: PreferenceSettings,
      },
      {
        path: 'admin',
        name: 'AdminSettings',
        component: AdminPage,
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundPage,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
