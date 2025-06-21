import { createRouter, createWebHistory } from 'vue-router'

// Page components
import LandingPage from '../pages/LandingPage.vue'
import SettingsPage from '../pages/Settings.vue'
import AdminPage from '../pages/AdminPage.vue'
import PreferenceSettings from '../pages/PreferenceSestting.vue'
import NotFoundPage from '../pages/404Page.vue'
import RecipesPage from '../pages/RecipesPage.vue'
import NewRecipe from '../pages/NewRecipe.vue'
import RecipeId from '../pages/RecipeId.vue'
const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
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
      },
      {
        path: ':recipe_name/:recipe_id',
        name: 'RecipeId',
        component: RecipeId,
        props: true
      },
    ]
  },
  {
    path: '/settings',
    name: 'SettingsPage',
    component: SettingsPage,
    children: [
      {
        path: '',
        redirect: '/settings/preferences', // Default redirect
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
