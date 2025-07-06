<template>
    <div class="card w-full max-w-[450px] md:w-[350px]">
  <Carousel
    :value="recipeVideos"
    :numVisible="1"
    :numScroll="1"
    :orientation="isMobile?null:'vertical'"
    :verticalViewPortHeight="'425px'"
    :autoplayInterval="7000"
    :responsiveOptions="responsiveOptions"
    circular
    :showNavigators="true"
  >
    <template #item="slotProps">
      <div
        class="border border-gray-200 dark:border-gray-700 rounded-xl m-2 p-4 bg-white dark:bg-gray-900 shadow-sm hover:shadow-xl transition-all duration-300"
      >
        <!-- Video Thumbnail -->
        <div class="mb-4 relative group">
          <div class="relative overflow-hidden rounded-lg aspect-video">
            <img
              :src="slotProps.data.thumbnail"
              :alt="slotProps.data.title"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            />
            <!-- Hover Play Icon -->
            <div
              class="absolute inset-0 bg-black/30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300"
            >
              <i class="pi pi-play text-4xl text-white bg-primary-500/90 rounded-full p-4 shadow-lg"></i>
            </div>
            <!-- Difficulty Tag -->
            <Tag
              :value="slotProps.data.difficulty"
              :severity="getDifficultyLevel(slotProps.data.difficulty)"
              class="absolute left-3 top-3"
            />
            <!-- Duration -->
            <span
              class="absolute right-3 top-3 bg-black/70 text-white px-2 py-1 rounded text-xs"
            >
              {{ slotProps.data.duration }}
            </span>
          </div>
        </div>

        <!-- Title & Description -->
        <div class="mb-3">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-1">
            {{ slotProps.data.title }}
          </h3>
          <p class="text-gray-600 dark:text-gray-300 text-sm line-clamp-2">
            {{ slotProps.data.description }}
          </p>
        </div>

        <!-- Author + Actions -->
        <div class="flex justify-between items-center">
          <div class="flex items-center">
            <Avatar
              :image="slotProps.data.chef.avatar"
              :label="slotProps.data.chef.name[0]"
              size="small"
              shape="circle"
              class="mr-2"
            />
            <span class="text-sm text-gray-700 dark:text-gray-300">
              {{ slotProps.data.chef.name }}
            </span>
          </div>
          <div class="flex space-x-2">
            <Button
              icon="pi pi-heart"
              severity="secondary"
              outlined
              class="hover:bg-red-50 dark:hover:bg-gray-800"
            />
            <Button
              icon="pi pi-bookmark"
              severity="secondary"
              outlined
              class="hover:bg-blue-50 dark:hover:bg-gray-800"
            />
            <Button
              icon="pi pi-share-alt"
              severity="secondary"
              outlined
              class="hover:bg-green-50 dark:hover:bg-gray-800"
            />
          </div>
        </div>

        <!-- Footer Info -->
        <div
          class="mt-3 flex items-center justify-between text-sm text-gray-500 dark:text-gray-400"
        >
          <div class="flex items-center">
            <i class="pi pi-star-fill text-yellow-500 mr-1"></i>
            <span>{{ slotProps.data.rating }}</span>
            <span class="mx-2">•</span>
            <i class="pi pi-users mr-1"></i>
            <span>{{ slotProps.data.views }} views</span>
          </div>
          <span>{{ slotProps.data.category }}</span>
        </div>
      </div>
    </template>
  </Carousel>
    </div>
</template>

<script setup>
import { ref } from "vue";
import { useIsMobile } from '../reusables';
const isMobile = useIsMobile();

const recipeVideos = ref([
    {
        id: '1',
        title: 'Perfect Homemade Pizza in 30 Minutes',
        description: 'Learn how to make restaurant-quality pizza at home with this simple recipe that comes together in just 30 minutes!',
        thumbnail: 'https://images.unsplash.com/photo-1565299624946-b28f40a0ae38?q=80&w=800',
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

const getDifficultyLevel = (difficulty) => {
    switch (difficulty.toLowerCase()) {
        case 'easy':
            return 'success';
        case 'medium':
            return 'warning';
        case 'hard':
            return 'danger';
        default:
            return 'info';
    }
};


const responsiveOptions = ref([
    {
        breakpoint: '1400px',
        numVisible: 1,
        numScroll: 1
    },
    {
        breakpoint: '1199px',
        numVisible: 1,
        numScroll: 1
    },
    {
        breakpoint: '767px',
        numVisible: 1,
        numScroll: 1
    },
    {
        breakpoint: '575px',
        numVisible: 1,
        numScroll: 1
    }
]);


</script>

<style scoped>
.p-carousel-prev-button	{
    position: absolute !important;
}
.card {
    margin: 0 auto;
}

:deep(.p-carousel-prev),
:deep(.p-carousel-next) {
    background: rgba(255, 255, 255, 0.8) !important;
    color: #333 !important;
    width: 2.5rem !important;
    height: 2.5rem !important;
    border-radius: 50% !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15) !important;
    position:absolute;
}

:deep(.p-carousel-prev:hover),
:deep(.p-carousel-next:hover) {
    background: white !important;
}
.p-carousel-next-button{
    position:absolute;

}
:deep(.p-carousel-indicators) {
    display: none;
}
</style>