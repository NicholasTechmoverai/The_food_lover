<template>
  <div>
    <component :is="MenuBar" :user="user" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useSiteStore } from '../config/siteConfig.js'
import { useAuthStore } from '../store/user.js'

import MenuBar1 from "../menubars/menubar1.vue"

const { siteConfig } = useSiteStore()
const auth = useAuthStore()

const user = computed(() => auth.user)

const MenuBar = computed(() => {
  const bar = siteConfig.components.menuBar
  if (bar === 1) return MenuBar1
  return MenuBar1 
})
</script>
