<template>
  <footer class="bg-gray-950 text-gray-100 border-t border-gray-800">
    <!-- Main Footer Content -->
    <div class="container mx-auto px-4 py-12 grid grid-cols-1 lg:grid-cols-4 gap-10">
      <!-- Brand Column -->
      <div class="space-y-5">
        <RouterLink to="/" class="flex items-center gap-3 group" aria-label="Return to homepage">
          <div class="h-10 w-10 bg-gradient-to-br from-amber-400 to-orange-500 rounded-lg flex items-center justify-center text-white font-bold text-xl transition-transform group-hover:scale-105">
            <i class="pi pi-utensils"></i>
          </div>
          <span class="text-2xl font-bold bg-gradient-to-r from-amber-400 to-orange-500 bg-clip-text text-transparent">
            {{ brand.name }}
          </span>
        </RouterLink>
        
        <p class="text-gray-400">{{ brand.description }}</p>
        
        <div class="flex gap-4">
          <a 
            v-for="social in socialLinks" 
            :key="social.name"
            :href="social.url" 
            :aria-label="social.name"
            class="p-2 rounded-full bg-gray-800 hover:bg-gray-700 transition-all hover:-translate-y-1 hover:text-amber-400"
            target="_blank"
            rel="noopener noreferrer"
          >
            <i :class="social.icon" class="text-lg"></i>
          </a>
        </div>
      </div>

      <!-- Quick Links -->
      <div v-for="(linkGroup, index) in footerLinks" :key="index">
        <h3 class="text-lg font-semibold mb-5 flex items-center gap-2">
          <i :class="linkGroup.icon" class="text-amber-400"></i>
          {{ linkGroup.title }}
        </h3>
        <ul class="space-y-3">
          <li v-for="link in linkGroup.links" :key="link.name">
            <RouterLink 
              :to="link.path" 
              class="text-gray-400 hover:text-amber-300 transition-colors flex items-center gap-2 group"
              active-class="text-amber-400 font-medium"
            >
              <span class="w-2 h-2 rounded-full bg-transparent group-hover:bg-amber-400 transition-all"></span>
              {{ link.name }}
            </RouterLink>
          </li>
        </ul>
      </div>

      <!-- Hotel/Shop Location + Newsletter -->
      <div class="space-y-8">
        <!-- Animated Hotel/Shop Map Section -->
        <div>
          <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
            <i class="pi pi-map-marker text-amber-400"></i>
            Visit Our Food Haven
          </h3>
          <div 
            class="aspect-video rounded-xl overflow-hidden border border-gray-800 hover:border-amber-400 transition-colors relative"
            @mouseenter="startMapAnimation"
            @mouseleave="stopMapAnimation"
          >
            <!-- Static preview of hotel/shop -->
            <img 
              v-if="!showInteractiveMap"
              :src="hotelPreviewImage" 
              alt="Our food hotel/shop location"
              class="w-full h-full object-cover brightness-90"
              :class="{'animate-pulse': mapAnimating}"
            >
            
            <!-- Interactive map centered on hotel/shop -->
            <iframe
              v-if="showInteractiveMap"
              :src="hotelMapEmbedUrl"
              class="w-full h-full"
              title="Interactive map showing our food hotel/shop location"
              aria-label="Interactive map of our establishment"
              allowfullscreen
              loading="lazy"
              referrerpolicy="no-referrer-when-downgrade"
            ></iframe>
            
            <!-- Overlay with "Explore Location" text -->
            <div 
              v-if="!showInteractiveMap"
              class="absolute inset-0 bg-black bg-opacity-30 flex items-center justify-center transition-opacity"
              :class="{'opacity-0': mapAnimating}"
            >
              <span class="bg-amber-500 text-white px-4 py-2 rounded-lg font-medium flex items-center gap-2">
                <i class="pi pi-compass"></i>
                Explore Location
              </span>
            </div>
          </div>
          <address class="mt-3 text-sm text-gray-400 not-italic">
            <div class="flex items-start gap-2">
              <i class="pi pi-home mt-0.5 text-amber-400"></i>
              {{ contactInfo.address }}
            </div>
            <div class="mt-2 flex items-center gap-2 text-amber-400">
              <i class="pi pi-phone"></i>
              {{ contactInfo.phone }}
            </div>
            <div class="mt-2 flex items-center gap-2 text-amber-400">
              <i class="pi pi-clock"></i>
              {{ contactInfo.hours }}
            </div>
          </address>
        </div>

        <!-- Foodie Newsletter -->
        <div>
          <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
            <i class="pi pi-inbox text-amber-400"></i>
            Foodie Newsletter
          </h3>
          <p class="text-gray-400 mb-4">Get weekly recipes, special offers, and dining tips</p>
          
          <form @submit.prevent="subscribe" class="space-y-3">
            <InputText
              v-model="email"
              type="email"
              required
              placeholder="Your email address"
              aria-label="Email for food newsletter subscription"
              class="w-full bg-gray-800 border-gray-700 placeholder-gray-500 focus:ring-2 focus:ring-amber-400 focus:border-transparent"
            />
            <Button
              type="submit"
              :label="isSubmitting ? 'Subscribing...' : 'Get Food Updates'"
              :icon="isSubmitting ? 'pi pi-spinner pi-spin' : 'pi pi-send'"
              iconPos="right"
              :disabled="isSubmitting"
              class="w-full bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 border-none shadow-lg hover:shadow-amber-500/20 transition-all"
            />
          </form>
          <p v-if="subscriptionMessage" class="mt-2 text-sm animate-fade-in" :class="subscriptionSuccess ? 'text-green-400' : 'text-red-400'">
            <i :class="subscriptionSuccess ? 'pi pi-check-circle' : 'pi pi-exclamation-circle'" class="mr-1"></i>
            {{ subscriptionMessage }}
          </p>
        </div>
      </div>
    </div>

    <!-- Footer Bottom -->
    <div class="border-t border-gray-800 py-6 bg-gray-900/50">
      <div class="container mx-auto px-4 flex flex-col md:flex-row justify-between items-center gap-4">
        <p class="text-gray-500 text-sm">
          &copy; {{ new Date().getFullYear() }} {{ brand.name }}. All culinary rights reserved.
        </p>
        
        <div class="flex items-center gap-6">
          <RouterLink 
            v-for="legal in legalLinks" 
            :key="legal.name"
            :to="legal.path" 
            class="text-gray-500 hover:text-gray-300 text-sm transition-colors hover:underline"
          >
            {{ legal.name }}
          </RouterLink>
        </div>
        
        <div class="flex items-center gap-4">
          <span class="text-gray-500 text-sm">Dine with us:</span>
          <a 
            v-for="reservation in reservationPlatforms" 
            :key="reservation.name"
            :href="reservation.url"
            class="hover:opacity-80 transition-opacity hover:-translate-y-0.5"
            target="_blank"
            rel="noopener noreferrer"
          >
            <div class="h-8 px-3 bg-gray-800 rounded flex items-center justify-center text-xs font-medium text-gray-300 border border-gray-700">
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

// Constants
const brand = {
  name: 'The food lovers',
  description: 'Where every meal is a celebration of flavors',
}

const contactInfo = {
  address: '89 Culinary Avenue, Food District, FD 89101',
  phone: '+1 (555) 987-6543',
  hours: 'Daily: 8:00 AM - 10:00 PM',
  email: 'reservations@gourmethaven.com',
}

const hotelPreviewImage = 'http://localhost:5173/src/assets/chiken.jpg' // Replace with your actual image
const hotelMapEmbedUrl = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3022.215209132713!2d-73.98832068459382!3d40.74844097932881!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c259a9b3117469%3A0xd134e199a405a163!2sEmpire%20State%20Building!5e0!3m2!1sen!2sus!4v1620000000000!5m2!1sen!2sus'

const socialLinks = [
  { name: 'Instagram', url: '#', icon: 'pi pi-instagram' },
  { name: 'Facebook', url: '#', icon: 'pi pi-facebook' },
  { name: 'TikTok', url: '#', icon: 'pi pi-video' },
  { name: 'YouTube', url: '#', icon: 'pi pi-youtube' },
  { name: 'Pinterest', url: '#', icon: 'pi pi-pinterest' }
]

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
      { name: 'Cooking Classes', path: '/classes' },
      { name: 'Food Tours', path: '/tours' },
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

<!-- <style scoped>
/* Custom animations */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fadeIn 0.3s ease-out;
}

/* Smooth transitions */
a, button, .transition-all {
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 200ms;
}

/* Gradient animation */
.bg-gradient-to-r {
  background-size: 200% auto;
  background-position: left center;
}

.bg-gradient-to-r:hover {
  background-position: right center;
}

/* Custom focus styles */
:focus-visible {
  outline: 2px solid theme('colors.amber.400');
  outline-offset: 2px;
}

/* PrimeVue overrides */
:deep(.p-inputtext) {
  background-color: theme('colors.gray.800');
  border-color: theme('colors.gray.700');
  color: theme('colors.gray.100');
}

:deep(.p-inputtext:enabled:hover) {
  border-color: theme('colors.gray.600');
}

:deep(.p-inputtext:enabled:focus) {
  box-shadow: 0 0 0 0.2rem rgba(251, 191, 36, 0.2);
  border-color: theme('colors.amber.400');
}

:deep(.p-button) {
  transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
}

:deep(.p-button:disabled) {
  opacity: 0.7;
  cursor: not-allowed;
}

/* Map container animation */
.animate-pulse {
  animation: pulse 1.5s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.8; }
}
</style> -->