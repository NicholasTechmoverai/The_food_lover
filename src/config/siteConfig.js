import splashLogo from '../assets/logo.png';
import favicon from '../assets/logo.ico';
import desktopBg from '../assets/blob-scene-landscape.svg';
import mobileBg from '../assets/blob-scene-potrait.svg';
import welcomeVideo from '../assets/3196344-uhd_3840_2160_25fps-compress.mp4'
// import welcomeImage from '../assets/2530-white-kitchen.png';
import welcomeImage from '../assets/kitchen1.jpg';
// import welcomeImage from '../assets/kitchen2.jpg';
import design_video from '../assets/3255109-uhd_3840_2160_25fps-compress.mp4'
import design_image from '../assets/chips1.jpg';



export const siteConfig = {
    // Site Identity
    author: 'Ruth larry\'s Kitchen',
    meta: {
        siteName: 'The Food Lover',
        by:'Ruth larry\'s Kitchen',
        titleTemplate: '%s | The Food Lover',
        description: 'Discover delicious recipes and culinary inspiration',
        keywords: ['food', 'recipes', 'cooking', 'culinary'],
        charset: 'UTF-8',
        viewport: 'width=device-width, initial-scale=1.0',
    },
    contactInfo:{
  address: '89 Culinary Avenue, Food District, FD 89101',
  phone: '+1 (555) 987-6543',
  hours: 'Daily: 8:00 AM - 10:00 PM',
  email: 'reservations@gourmethaven.com',
},
    welcomeMessage: {
        card:2,
        note: `Welcome to The Food Lover! Explore our delicious recipes and culinary tips.`,
        fontFamily: "'Telma', cursive",
        image: welcomeImage,
        video:welcomeVideo,
    },
    servicesOffred: {
        card: 2,
        image: {
            desktop: desktopBg,
            mobile: mobileBg,
        },
        title: 'What We Offer',
        description: 'Explore a wide range of culinary delights, from quick meals to gourmet dishes. Our recipes are designed for all skill levels, ensuring everyone can enjoy the art of cooking.',
        buttonText: 'Explore Our Services',
        buttonLink: '/services',
        buttonIcon: 'fas fa-utensils',
        features: [
            {
                title: 'Quick Recipes',
                description: 'Delicious meals in under 30 minutes.',
                icon: 'fas fa-clock'
            },
            {
                title: 'Gourmet Dishes',
                description: 'Elevate your cooking with gourmet recipes.',
                icon: 'fas fa-star'
            },
            {
                title: 'Healthy Options',
                description: 'Nutritious meals for a balanced diet.',
                icon: 'fas fa-apple-alt'
            },
            {
                title: 'Baking Delights',
                description: 'From bread to pastries, we have it all.',
                icon: 'fas fa-bread-slice'
            }
        ]
    },
    reachOut: {
        card:1,
        video:design_video,
        image: design_image,
        title: 'Join Our Flavorful Journey',
        note: 'Discover over 1,000 curated recipes, hands-on tips, and endless culinary inspiration. Whether you’re new to the kitchen or a seasoned pro, there’s something delicious waiting for you.',
        tools: [
            {
                name: 'Explore 1,000+ Recipes',
                description: 'Dive into a diverse library of dishes—from comfort food classics to global cuisine favorites, all tailored to your taste and dietary needs.',
                icon: 'fas fa-utensils'
            },
            {
                name: 'Master 500+ Pro Tips',
                description: 'Upgrade your skills with practical, chef-approved techniques that make everyday cooking easier and more fun.',
                icon: 'fas fa-lightbulb'
            },
            {
                name: 'Spark Culinary Creativity',
                description: 'Get inspired with fresh ideas for meals, plating, and ingredient pairings that awaken your inner chef.',
                icon: 'fas fa-fire-alt'
            },
            {
                name: 'Join 500+ Food Enthusiasts',
                description: 'Be part of a passionate food-loving community—swap stories, share dishes, and grow together.',
                icon: 'fas fa-users'
            },
            {
                name: 'Watch 250+ Step-by-Step Videos',
                description: 'Visual learner? Follow along with guided videos for recipes, skills, and pro techniques.',
                icon: 'fas fa-play-circle'
            },
            {
                name: 'Weekly Recipe Drops',
                description: 'Subscribe and get 10+ fresh, handpicked recipes every week—straight to your inbox or phone.',
                icon: 'fas fa-envelope-open-text'
            },
            {
                name: 'Share Your Signature Dishes',
                description: 'Got a family favorite or personal creation? Share it with the world and inspire others.',
                icon: 'fas fa-share-alt'
            }
        ]
    },
    // Site Metadata

    // Brand Assets
    assets: {
        logo: splashLogo,
        logoAlt: 'The Food Lover Logo',
        icon: favicon,
        logoMaxWidth: '300px',
    },

    // Color Scheme
    colors: {
        primary: 'rgb(70, 12, 70)',
        secondary: '#5DADE2',
        accent: '#00BFFF',
        highlight: '#4FC3F7',
        info: '#0d6efd',
        light: '#e3f2fd',
        dark: '#0b3d91',
        background: 'pink',
        surface: '#fff8f0',
        text: {
            primary: '#212529',
            secondary: '#495057',
            inverted: '#f8f9fa'
        },
        gradients: {
            primary: 'linear-gradient(135deg, #007BFF 0%, #00BFFF 100%)',
            wave: 'linear-gradient(to bottom, #0066ff 0%, #0f223f 100%)'
        }
    },


    // Background Configuration
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
            parallax: true
        },
        video: null, // Can add video background option later
    },

    // Social Media Links
    social: {
        links: [
            {
                name: 'facebook',
                url: 'https://www.facebook.com/thefoodlover',
                icon: 'fab fa-facebook-f'
            },
            {
                name: 'twitter',
                url: 'https://twitter.com/thefoodlover',
                icon: 'fab fa-twitter'
            },
            {
                name: 'instagram',
                url: 'https://www.instagram.com/thefoodlover',
                icon: 'fab fa-instagram'
            },
            {
                name: 'youtube',
                url: 'https://www.youtube.com/thefoodlover',
                icon: 'fab fa-youtube'
            },
            {
                name: 'pinterest',
                url: 'https://www.pinterest.com/thefoodlover',
                icon: 'fab fa-pinterest'
            },
        ],
        shareButtons: true,
        shareText: 'Follow Us on our social Media Platforms!'
    },

    // Splash Screen Configuration
    splash: {
        enabled: true,
        duration: 2000,
        backgroundColor: '#fff8f0',
        animation: 'fade', // Options: fade, slide-up, zoom
        minimumShowTime: 1500 // Even if loaded faster, show for this time
    },

    components: {
        searchBar: 4,
        menuBar:1,
        footer:1,
    },


    // Performance Options
    performance: {
        lazyLoadImages: true,
        prefetchAssets: true,
        criticalCSS: true
    },

    // Analytics
    analytics: {
        googleAnalyticsID: null, // 'UA-XXXXX-Y'
        facebookPixelID: null    // 'XXXXXXX'
    },

    // Default SEO Settings
    seo: {
        canonicalUrl: 'https://thefoodlover.com',
        openGraph: {
            type: 'website',
            siteName: 'The Food Lover'
        },
        twitterCard: {
            cardType: 'summary_large_image'
        }
    },
    // Wave Animation Configuration
    wave: {
        enabled: false,  // More semantic than showWaves
        count: 5,        // Renamed from waveCount for consistency
        speed: 0.05,
        amplitude: {
            desktop: 10,
            mobile: 30,
            ratio: 0.6    // Mobile reduction ratio
        },
        dimensions: {
            width: 900,
            height: 200,
            mobileHeightRatio: 0.7
        },
        depthIntensity: 1,
        colors: ['#0f223f', '#05346c', '#00459c', '#0056cd', '#0066ff'],
        blendMode: 'multiply',
        parallaxIntensity: 0.3
    },
};



// Helper function to get responsive values
export const getResponsiveValue = (config, key, isMobile) => {
    if (isMobile && config[key]?.mobile !== undefined) {
        return config[key].mobile;
    }
    if (isMobile && config[key]?.ratio !== undefined) {
        return config[key].desktop * config[key].ratio;
    }
    return config[key]?.desktop || config[key];
};

import { ref, onMounted, onBeforeUnmount } from 'vue';

const isMobile = ref(window.innerWidth < 768);

const checkIsMobile = () => {
    isMobile.value = window.innerWidth < 768;
};

export const useIsMobile = () => {
    onMounted(() => {
        window.addEventListener('resize', checkIsMobile);
    });

    onBeforeUnmount(() => {
        window.removeEventListener('resize', checkIsMobile);
    });

    return isMobile;
};
