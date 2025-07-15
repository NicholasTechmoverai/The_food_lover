<template>
  <section class="space-y-10 md:space-y-12 px-4 sm:px-6 lg:px-8">
    <!-- Header -->
    <header>
      <h2 class="text-2xl font-bold capitalize text-gray-800 dark:text-white">
        {{ recipe_type }}
      </h2>
    </header>

    <!-- About Section -->
    <section>
      <h3 class="text-xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
        More about {{ recipe_type }}
      </h3>
      <PileCard :recipes="recipes" />
    </section>

    <!-- Recipes List Section -->
    <section>
      <h3 class="text-xl font-semibold mb-4 text-gray-700 dark:text-gray-300">
        {{ recipe_type }} recipes
      </h3>
      <ManyRecipesParent />
    </section>
  </section>
</template>

<script setup>
import PileCard from "../cards/PileCards.vue"
import ManyRecipesParent from "../cards/ManyReipesParent.vue" // fix if actual file uses 'Reipes'
import { ref } from "vue";

const props = defineProps({
  recipe_type: {
    type: String,
    default: 'recipe'
  }
});

const recipes = ref([
    {
        title: `${props.meal_type} Pasta Carbonara`,
        image: 'https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb',
        alt: 'creamy pasta carbonara with bacon and parsley',
        views: 4280,
        likes: 645,
        chef: {
            id: 1,
            name: 'Chef Antonio',
            avatar: 'https://i.pravatar.cc/40?img=1'
        }
    },
    {
        title: `${props.meal_type} Beef Burger`,
        image: 'https://images.unsplash.com/photo-1568901346375-23c9450c58cd',
        alt: 'juicy beef burger with cheese and vegetables',
        views: 5340,
        likes: 798,
        chef: {
            id: 2,
            name: 'Chef Maria',
            avatar: 'https://i.pravatar.cc/40?img=2'
        }
    },
    {
        title: `${props.meal_type} Chicken Curry`,
        image: 'https://images.unsplash.com/photo-1585937421612-70a008356fbe',
        alt: 'spicy chicken curry in a bowl',
        views: 3980,
        likes: 588,
        chef: {
            id: 3,
            name: 'Chef Raj',
            avatar: 'https://i.pravatar.cc/40?img=3'
        }
    },
    {
        title: `${props.meal_type} Vegetable Stir Fry`,
        image: 'https://images.unsplash.com/photo-1626700051175-6818013e1d4f',
        alt: 'colorful vegetable stir fry in a wok',
        views: 3120,
        likes: 410,
        chef: {
            id: 4,
            name: 'Chef Lin',
            avatar: 'https://i.pravatar.cc/40?img=4'
        }
    },
    {
        title: `${props.meal_type} Grilled Salmon`,
        image: 'https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2',
        alt: 'grilled salmon with lemon and herbs',
        views: 3750,
        likes: 560,
        chef: {
            id: 5,
            name: 'Chef Sofia',
            avatar: 'https://i.pravatar.cc/40?img=5'
        }
    },
    {
        title: 'Margherita Pizza',
        image: 'https://images.unsplash.com/photo-1574071318508-1cdbab80d002',
        alt: 'classic margherita pizza with fresh basil',
        views: 4890,
        likes: 773,
        chef: {
            id: 6,
            name: 'Chef Giovanni',
            avatar: 'https://i.pravatar.cc/40?img=6'
        }
    },
    {
        title: 'Beef Tacos',
        image: 'https://images.unsplash.com/photo-1565299585323-38d6b0865b47',
        alt: 'three beef tacos with toppings',
        views: 4200,
        likes: 700,
        chef: {
            id: 7,
            name: 'Chef Carlos',
            avatar: 'https://i.pravatar.cc/40?img=7'
        }
    },
    {
        title: 'Vegetable Lasagna',
        image: 'https://images.unsplash.com/photo-1611270629569-8b357cb88da9',
        alt: 'slice of vegetable lasagna with melted cheese',
        views: 2950,
        likes: 457,
        chef: {
            id: 8,
            name: 'Chef Emma',
            avatar: 'https://i.pravatar.cc/40?img=8'
        }
    },
    {
        title: 'Chicken Parmesan',
        image: 'https://images.unsplash.com/photo-1607923432728-1b6b2b1b1b1b',
        alt: 'crispy chicken parmesan with pasta',
        views: 3475,
        likes: 538,
        chef: {
            id: 9,
            name: 'Chef Luca',
            avatar: 'https://i.pravatar.cc/40?img=9'
        }
    },
    {
        title: 'Beef Stew',
        image: 'https://images.unsplash.com/photo-1476718406336-bb5a9690ee2a',
        alt: 'hearty beef stew in a bowl',
        views: 3040,
        likes: 496,
        chef: {
            id: 10,
            name: 'Chef Pierre',
            avatar: 'https://i.pravatar.cc/40?img=10'
        }
    }
])
</script>
