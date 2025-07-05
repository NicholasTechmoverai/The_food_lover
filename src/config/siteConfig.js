import { defineStore } from 'pinia'
import { ref } from 'vue'

// Assets
import splashLogo from '../assets/logo.png'
import favicon from '../assets/logo.ico'
import desktopBg from '../assets/blob-scene-landscape.svg'
import mobileBg from '../assets/blob-scene-potrait.svg'
import welcomeVideo from '../assets/3196344-uhd_3840_2160_25fps-compress.mp4'
import welcomeImage from '../assets/kitchen1.jpg'
import design_video from '../assets/3255109-uhd_3840_2160_25fps-compress.mp4'
import design_image from '../assets/chips1.jpg'

export const useSiteStore = defineStore('site', () => {
  const defaultSiteName = "The Food Lover"
  const defaultAuthor = "Ruth larry's Kitchen"

  const siteConfig = ref({
    author: defaultAuthor,
    meta: {
      siteName: defaultSiteName,
      by: defaultAuthor,
      titleTemplate: '%s | ' + defaultSiteName,
      description: 'Discover delicious recipes and culinary inspiration',
      charset: 'UTF-8',
      viewport: 'width=device-width, initial-scale=1.0',
    },
    contactInfo: {
      address: '89 Culinary Avenue, Food District, FD 89101',
      phone: '+1 (555) 987-6543',
      hours: 'Daily: 8:00 AM - 10:00 PM',
      email: 'reservations@gourmethaven.com',
    },
    welcomeMessage: {
      card: 2,
      note: `Welcome to ${defaultSiteName}! Explore our delicious recipes and culinary tips.`,
      fontFamily: "'Telma', cursive",
      image: welcomeImage,
      video: welcomeVideo,
    },
    servicesOffred: {
      card: 2,
      image: {
        desktop: desktopBg,
        mobile: mobileBg,
      },
      title: 'What We Offer',
      description: 'Explore a wide range of culinary delights, from quick meals to gourmet dishes...',
      buttonText: 'Explore Our Services',
      buttonLink: '/services',
      buttonIcon: 'fas fa-utensils',
      features: [
        { title: 'Quick Recipes', description: 'Delicious meals in under 30 minutes.', icon: 'fas fa-clock' },
        { title: 'Gourmet Dishes', description: 'Elevate your cooking...', icon: 'fas fa-star' },
        { title: 'Healthy Options', description: 'Nutritious meals...', icon: 'fas fa-apple-alt' },
        { title: 'Baking Delights', description: 'From bread to pastries...', icon: 'fas fa-bread-slice' },
      ],
    },
    reachOut: {
      card: 1,
      video: design_video,
      image: design_image,
      title: 'Join Our Flavorful Journey',
      note: 'Discover over 1,000 curated recipes, hands-on tips...',
      tools: [
        { name: 'Explore 1,000+ Recipes', description: 'Dive into...', icon: 'fas fa-utensils' },
        { name: 'Master 500+ Pro Tips', description: 'Upgrade your skills...', icon: 'fas fa-lightbulb' },
        { name: 'Spark Culinary Creativity', description: 'Get inspired...', icon: 'fas fa-fire-alt' },
        { name: 'Join 500+ Food Enthusiasts', description: 'Be part of...', icon: 'fas fa-users' },
        { name: 'Watch 250+ Step-by-Step Videos', description: 'Visual learner?', icon: 'fas fa-play-circle' },
        { name: 'Weekly Recipe Drops', description: 'Subscribe and get...', icon: 'fas fa-envelope-open-text' },
        { name: 'Share Your Signature Dishes', description: 'Got a family favorite?', icon: 'fas fa-share-alt' },
      ],
    },
    assets: {
      logo: splashLogo,
      logoAlt: `${defaultSiteName} Logo`,
      icon: favicon,
      logoMaxWidth: '300px',
    },
    colors: {
      primary: '#800000',       // Maroon (core brand color)
      secondary: '#A52A2A',     // Brownish maroon (warm supporting)
      accent: '#D2691E',        // Chocolate (for subtle emphasis)
      highlight: '#B22222',     // Firebrick (vibrant highlight)
      info: '#8B0000',          // Dark red (alerts, links, etc.)
      light: '#FBEAEA',         // Light pink background shade
      dark: '#330000',          // Deep maroon-black
      background: '#FFF5F5',    // Very light rose for backgrounds
      surface: '#FAF0F0',       // Surface card color
      text: {
        primary: '#2C0A0A',
        secondary: '#5A3A3A',
        inverted: '#FAFAFA',
      },

      gradients: {
        primary: 'linear-gradient(135deg, #007BFF 0%, #00BFFF 100%)',
        wave: 'linear-gradient(to bottom, #0066ff 0%, #0f223f 100%)',
      },
    },
    background: {
      image: {
        enabled: true,
        desktop: desktopBg,
        mobile: mobileBg,
        alt: 'Decorative background pattern',
        opacity: 0.5,
        position: 'center center',
        size: 'cover',
        blendMode: 'overlay',
        parallax: true,
      },
      video: null,
    },
    social: {
      links: [
        { name: 'facebook', url: 'https://www.facebook.com/thefoodlover', icon: 'fab fa-facebook-f' },
        { name: 'twitter', url: 'https://twitter.com/thefoodlover', icon: 'fab fa-twitter' },
        { name: 'instagram', url: 'https://www.instagram.com/thefoodlover', icon: 'fab fa-instagram' },
        { name: 'youtube', url: 'https://www.youtube.com/thefoodlover', icon: 'fab fa-youtube' },
        { name: 'pinterest', url: 'https://www.pinterest.com/thefoodlover', icon: 'fab fa-pinterest' },
      ],
      shareButtons: true,
      shareText: 'Follow Us on our social Media Platforms!',
    },
    splash: {
      enabled: true,
      duration: 2000,
      backgroundColor: '#fff8f0',
      animation: 'fade',
      minimumShowTime: 1500,
    },
    components: {
      searchBar: 4,
      menuBar: 1,
      footer: 1,
    },
    performance: {
      lazyLoadImages: true,
      prefetchAssets: true,
      criticalCSS: true,
    },
    analytics: {
      googleAnalyticsID: null,
      facebookPixelID: null,
    },
    seo: {
      canonicalUrl: 'https://thefoodlover.com',
      openGraph: {
        type: 'website',
        siteName: defaultSiteName,
      },
      twitterCard: {
        cardType: 'summary_large_image',
      },
    },
    wave: {
      enabled: false,
      count: 5,
      speed: 0.05,
      amplitude: {
        desktop: 10,
        mobile: 30,
        ratio: 0.6,
      },
      dimensions: {
        width: 900,
        height: 200,
        mobileHeightRatio: 0.7,
      },
      depthIntensity: 1,
      colors: ['#0f223f', '#05346c', '#00459c', '#0056cd', '#0066ff'],
      blendMode: 'multiply',
      parallaxIntensity: 0.3,
    },
  })

  const getResponsiveValue = (config, key, isMobile) => {
    if (isMobile && config[key]?.mobile !== undefined) {
      return config[key].mobile
    }
    if (isMobile && config[key]?.ratio !== undefined) {
      return config[key].desktop * config[key].ratio
    }
    return config[key]?.desktop || config[key]
  }

const adjustThemesColor = (colors) => {
  if (!colors) return

  const target = siteConfig.value.colors

  // Top-level color fields
  if (colors.primary) target.primary = polishColor(colors.primary)
  if (colors.secondary) target.secondary = polishColor(colors.secondary)
  if (colors.accent) target.accent = colors.accent
  if (colors.highlight) target.highlight = colors.highlight
  if (colors.info) target.info = colors.info
  if (colors.light) target.light = colors.light
  if (colors.dark) target.dark = colors.dark
  if (colors.background) target.background = colors.background
  if (colors.surface) target.surface = colors.surface

  // Nested text colors
  if (colors.text) {
    if (colors.text.primary) target.text.primary = colors.text.primary
    if (colors.text.secondary) target.text.secondary = colors.text.secondary
    if (colors.text.inverted) target.text.inverted = colors.text.inverted
  }

  // Nested gradient colors
  if (colors.gradients) {
    if (colors.gradients.primary) target.gradients.primary = colors.gradients.primary
    if (colors.gradients.wave) target.gradients.wave = colors.gradients.wave
  }

  console.log('Updated theme colors:', colors ,'updated to',target)
}

const  polishColor = (nv) =>{
  return nv.startsWith('#') ? nv : `#${nv}`;
}


  return {
    adjustThemesColor,
    siteConfig,
    getResponsiveValue,
  }
})
