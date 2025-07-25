<template>
    <div v-for="video in videos" :key="video.id">
        <video-play-card :video="video" />
    </div>
</template>
<script setup>
import { ref } from 'vue';
import VideoPlayCard from '../cards/VideoPlayCard.vue';

const videos = ref([
  {
    id: '1',
    title: 'Perfect Homemade Pizza in 30 Minutes',
    description: 'Learn how to make restaurant-quality pizza at home with this simple recipe that comes together in just 30 minutes!',
    thumbnail: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=800',
                video:"",

    duration: '12:45',
    difficulty: 'Easy',
    rating: '4.8',
    views: '1.2M',
    category: 'Italian',
    chef: {
      name: 'Marco Rossi',
      avatar: 'https://randomuser.me/api/portraits/men/32.jpg'
    }
  },
  {
    id: '2',
    title: 'Fluffy Japanese Pancakes',
    description: 'These jiggly soufflé pancakes are a viral sensation for good reason - light, airy and delicious!',
    thumbnail: 'https://images.unsplash.com/photo-1557142046-c704a3adf364?q=80&w=800',
    duration: '15:20',
    difficulty: 'Medium',
    rating: '4.9',
    views: '2.4M',
    category: 'Breakfast',
    chef: {
      name: 'Yuki Tanaka',
      avatar: 'https://randomuser.me/api/portraits/women/44.jpg'
    }
  },
  {
    id: '3',
    title: 'Authentic Beef Bourguignon',
    description: 'Julia Child\'s classic French stew made with tender beef, mushrooms, and red wine',
    thumbnail: 'https://images.unsplash.com/photo-1603105037880-880cd4edfb0d?q=80&w=800',
    duration: '42:15',
    difficulty: 'Hard',
    rating: '4.7',
    views: '856K',
    category: 'French',
    chef: {
      name: 'Pierre Leclerc',
      avatar: 'https://randomuser.me/api/portraits/men/68.jpg'
    }
  },
  {
    id: '4',
    title: 'Vegan Buddha Bowl',
    description: 'Colorful, nutritious and packed with plant-based protein - the perfect healthy meal!',
    thumbnail: 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?q=80&w=800',
    duration: '08:30',
    difficulty: 'Easy',
    rating: '4.5',
    views: '1.8M',
    category: 'Vegan',
    chef: {
      name: 'Sophie Green',
      avatar: 'https://randomuser.me/api/portraits/women/65.jpg'
    }
  }
]);
</script>