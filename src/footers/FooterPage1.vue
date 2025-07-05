<template>
  <footer
    class="border-t backdrop-blur-xl text-white dark:text-gray-300"
    :style="{
      backgroundColor: siteConfig.colors.secondary + '70',
      borderColor: siteConfig.colors.secondary + '30'
    }"
  >
    <!-- Main Footer Content -->
    <div class="container mx-auto px-4 py-12 grid grid-cols-1 lg:grid-cols-4 gap-10">
      
      <!-- Brand Column -->
      <div class="space-y-5">
        <RouterLink to="/" class="flex items-center gap-3 group" aria-label="Return to homepage">
         <img @click="goHome" :src="siteConfig.assets.logo" :alt="siteConfig.assets.logoAlt"
                        class="w-14 h-14 object-contain cursor-pointer" />
          <span
            class="text-2xl font-bold bg-clip-text text-transparent"
            :style="{ backgroundImage: `linear-gradient(to right, ${siteConfig.colors.primary}, ${siteConfig.colors.secondary})` }"
          >
            {{ siteConfig.meta.siteName }}
          </span>
        </RouterLink>

        <p class="text-white dark:text-gray-400">{{ brand.description }}</p>

        <div class="flex gap-4">
          <a
            v-for="social in socialLinks"
            :key="social.name"
            :href="social.url"
            class="p-2 rounded-full transition-all hover:-translate-y-1 hover:bg-white/10"
            target="_blank"
            rel="noopener noreferrer"
          >
            <i :class="social.icon" class="text-lg text-white dark:text-gray-300"></i>
          </a>
        </div>
      </div>

      <!-- Quick Links -->
      <div v-for="(linkGroup, index) in footerLinks" :key="index">
        <h3 class="text-lg font-semibold mb-5 flex items-center gap-2" :style="{ color: siteConfig.colors.primary }">
          <i :class="linkGroup.icon"></i>
          {{ linkGroup.title }}
        </h3>
        <ul class="space-y-3">
          <li v-for="link in linkGroup.links" :key="link.name">
            <RouterLink
              :to="link.path"
              class="flex items-center gap-2 group transition-colors"
              active-class="font-medium"
            >
              <span class="w-2 h-2 rounded-full group-hover:scale-125 transition-all"
                :style="{ backgroundColor: siteConfig.colors.primary + '70' }"
              ></span>
              <span class="text-white dark:text-gray-300 group-hover:text-white dark:group-hover:text-gray-100">
                {{ link.name }}
              </span>
            </RouterLink>
          </li>
        </ul>
      </div>

      <!-- Location & Newsletter -->
      <div class="space-y-8">
        
        <!-- Map & Address -->
        <div>
          <h3 class="text-lg font-semibold mb-4 flex items-center gap-2" :style="{ color: siteConfig.colors.primary }">
            <i class="pi pi-map-marker"></i>
            Visit Our Food Haven
          </h3>

          <div
            class="aspect-video rounded-xl overflow-hidden border relative transition-colors"
            :style="{ borderColor: siteConfig.colors.primary + '30' }"
            @mouseenter="startMapAnimation"
            @mouseleave="stopMapAnimation"
          >
            <img
              v-if="!showInteractiveMap"
              :src="hotelPreviewImage"
              class="w-full h-full object-cover"
              :class="{ 'animate-pulse': mapAnimating }"
            />
            <iframe
              v-if="showInteractiveMap"
              :src="hotelMapEmbedUrl"
              class="w-full h-full"
              allowfullscreen
              loading="lazy"
            ></iframe>

            <div
              v-if="!showInteractiveMap"
              class="absolute inset-0 flex items-center justify-center bg-black/30"
              :class="{ 'opacity-0': mapAnimating }"
            >
              <span class="px-4 py-2 rounded-lg font-medium flex items-center gap-2 text-white"
                :style="{ backgroundColor: siteConfig.colors.primary }"
              >
                <i class="pi pi-compass"></i> Explore Location
              </span>
            </div>
          </div>

          <address class="mt-3 text-sm not-italic space-y-2">
            <div class="flex items-start gap-2">
              <i class="pi pi-home" :style="{ color: siteConfig.colors.primary }"></i>
              <span class="text-white dark:text-gray-400">{{ contactInfo.address }}</span>
            </div>
            <div class="flex items-center gap-2">
              <i class="pi pi-phone" :style="{ color: siteConfig.colors.primary }"></i>
              <span class="text-white dark:text-gray-400">{{ contactInfo.phone }}</span>
            </div>
            <div class="flex items-center gap-2">
              <i class="pi pi-clock" :style="{ color: siteConfig.colors.primary }"></i>
              <span class="text-white dark:text-gray-400">{{ contactInfo.hours }}</span>
            </div>
          </address>
        </div>

        <!-- Newsletter -->
        <div>
          <h3 class="text-lg font-semibold mb-4 flex items-center gap-2" :style="{ color: siteConfig.colors.primary }">
            <i class="pi pi-inbox"></i>
            Foodie Newsletter
          </h3>
          <p class="text-white dark:text-gray-300 mb-4">
            Get weekly recipes, special offers, and dining tips.
          </p>
          <form @submit.prevent="subscribe" class="space-y-3">
            <InputText
              v-model="email"
              type="email"
              required
              placeholder="Your email address"
              class="w-full bg-white/5 border-gray-400/30 text-white dark:text-gray-200 placeholder-gray-400/70"
            />
            <Button
              type="submit"
              :label="isSubmitting ? 'Subscribing...' : 'Get Updates'"
              :icon="isSubmitting ? 'pi pi-spinner pi-spin' : 'pi pi-send'"
              iconPos="right"
              :disabled="isSubmitting"
              class="w-full"
              :style="{
                backgroundImage: `linear-gradient(to right, ${siteConfig.colors.primary}, ${siteConfig.colors.secondary})`,
                border: 'none',
                color: 'white',
              }"
            />
          </form>
          <p
            v-if="subscriptionMessage"
            class="mt-2 text-sm animate-fade-in"
            :class="subscriptionSuccess ? 'text-green-400' : 'text-red-400'"
          >
            <i :class="subscriptionSuccess ? 'pi pi-check-circle' : 'pi pi-exclamation-circle'" class="mr-1"></i>
            {{ subscriptionMessage }}
          </p>
        </div>
      </div>
    </div>

    <!-- Footer Bottom -->
    <div class="py-6 border-t border-white/10 bg-white/5 dark:bg-black/10">
      <div class="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-4">
        <p class="text-sm text-white dark:text-gray-400">
          &copy; {{ new Date().getFullYear() }} {{ brand.name }}. All culinary rights reserved.
        </p>
        <div class="flex items-center gap-6">
          <RouterLink
            v-for="legal in legalLinks"
            :key="legal.name"
            :to="legal.path"
            class="text-sm hover:underline text-white dark:text-gray-400 hover:text-gray-200"
          >
            {{ legal.name }}
          </RouterLink>
        </div>
        <div class="flex items-center gap-4">
          <span class="text-sm text-white dark:text-gray-400">Dine with us:</span>
          <a
            v-for="reservation in reservationPlatforms"
            :key="reservation.name"
            :href="reservation.url"
            target="_blank"
            class="hover:opacity-80 transition-opacity hover:-translate-y-0.5"
          >
            <div
              class="h-8 px-3 rounded flex items-center justify-center text-xs font-medium border border-white/10 bg-white/10 dark:bg-black/10 text-white dark:text-gray-300"
            >
              <i :class="reservation.icon" class="mr-1"></i>
              {{ reservation.name }}
            </div>
          </a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
// import {  useIsMobile } from '../reusables';
import { useSiteStore } from '../config/siteConfig.js'

const { siteConfig, getResponsiveValue } = useSiteStore()

// Constants
const brand = {
  name: 'The food lovers',
  description: 'Where every meal is a celebration of flavors',
}

const contactInfo = siteConfig.contactInfo

const hotelPreviewImage = 'http://localhost:5173/src/assets/chiken.jpg' // Replace with your actual image
const hotelMapEmbedUrl = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3022.215209132713!2d-73.98832068459382!3d40.74844097932881!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c259a9b3117469%3A0xd134e199a405a163!2sEmpire%20State%20Building!5e0!3m2!1sen!2sus!4v1620000000000!5m2!1sen!2sus'

const socialLinks = siteConfig.social

const footerLinks = [
  {
    title: 'Our Offerings',
    icon: 'pi pi-book',
    links: [
      { name: 'Signature Dishes', path: '/menu/signature' },
      { name: 'Seasonal Menu', path: '/menu/seasonal' },
      { name: 'Wine Pairings', path: '/wine-list' },
      { name: 'Private Dining', path: '/private-events' }
    ]
  },
  {
    title: 'Experience',
    icon: 'pi pi-star',
    links: [
      { name: 'Meet Our Chefs', path: '/chefs' },
      { name: 'Cooking Tips', path: '/cooking-tips' },
      { name: 'Receips', path: '/receips' },
      { name: 'Cooking Classes', path: '/classes' },
      { name: 'Food Tours', path: '/tours' },
      { name: 'videos', path: '/videos' },
      { name: 'Gallery', path: '/gallery' }

    ]
  },
  {
    title: 'Information',
    icon: 'pi pi-info-circle',
    links: [
      { name: 'Reservations', path: '/reservations' },
      { name: 'Gift Cards', path: '/gift-cards' },
      { name: 'FAQs', path: '/faqs' },
      { name: 'Contact Us', path: '/contact' }
    ]
  }
]

const legalLinks = [
  { name: 'Privacy Policy', path: '/privacy' },
  { name: 'Terms of Service', path: '/terms' },
  { name: 'Accessibility', path: '/accessibility' }
]

const reservationPlatforms = [
  { name: 'OpenTable', url: '#', icon: 'pi pi-calendar-plus' },
  { name: 'Resy', url: '#', icon: 'pi pi-bookmark' }
]

// Reactive state
const email = ref('')
const isSubmitting = ref(false)
const subscriptionMessage = ref('')
const subscriptionSuccess = ref(false)
const showInteractiveMap = ref(false)
const mapAnimating = ref(false)

// Map animation
let animationTimeout = null

const startMapAnimation = () => {
  mapAnimating.value = true
  animationTimeout = setTimeout(() => {
    showInteractiveMap.value = true
  }, 800) // Shorter delay for better UX
}

const stopMapAnimation = () => {
  clearTimeout(animationTimeout)
  mapAnimating.value = false
  showInteractiveMap.value = false
}

// Methods
const subscribe = async () => {
  if (!email.value) return

  isSubmitting.value = true
  subscriptionMessage.value = ''

  try {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500))

    subscriptionSuccess.value = true
    subscriptionMessage.value = 'Welcome to our foodie family! Check your inbox for delicious updates.'
    email.value = ''
  } catch (error) {
    subscriptionSuccess.value = false
    subscriptionMessage.value = 'Subscription failed. Please try again later.'
  } finally {
    isSubmitting.value = false

    setTimeout(() => {
      subscriptionMessage.value = ''
    }, 5000)
  }
}
</script>

