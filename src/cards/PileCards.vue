<template>
    <div class="py-4">
        <h1 class="text-lg font-semibold mb-4 text-gray-800 dark:text-gray-100 text-center">
            ⟵ Scroll ⟶
        </h1>

        <ul class="flex gap-4 overflow-x-auto pb-4">
            <li v-for="recipe in recipes" :key="recipe.title"
                class="relative min-w-[250px]  overflow-hidden shadow hover:shadow-lg transition duration-300 bg-white dark:bg-gray-800">
                <!-- Recipe Image -->
                <img :src="recipe.image" :alt="recipe.alt" class="w-full h-64 object-cover" />

                <!-- Overlay Content -->
                <div class="absolute inset-0 bg-black/40  text-white flex flex-col justify-end p-3">
                    <div class="flex justify-between items-center text-xs text-white/90">
                        <span class="font-bold text-xl">{{ recipe.title }}</span>
                        <!-- <span><i class="pi pi-heart-fill text-red-400 mr-1"></i>{{ recipe.likes }}</span> -->
                    </div>
                    <div class="flex items-center gap-2 mb-2">
                        <img :src="recipe.chef.avatar" :alt="recipe.chef.name"
                            class="w-8 h-8 rounded-full border-2 border-white" />
                        <div class="text-sm">
                            <p class="font-semibold leading-tight">{{ recipe.chef.name }}</p>
                            <p class="text-xs opacity-80">{{ recipe.views }} views</p>
                        </div>
                    </div>


                </div>
            </li>
        </ul>
    </div>



</template>


<script setup>
import { ref } from 'vue';
const props = defineProps({
    recipe_type: String,
});
const recipes = [
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
]
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap");

*,
*:before,
*:after {
    box-sizing: border-box;
}

*::-webkit-scrollbar,
body::-webkit-scrollbar,
html::-webkit-scrollbar {
    background-color: #1e1f26;
    height: 20px;
    width: 20px;
}

*::-webkit-scrollbar-thumb,
body::-webkit-scrollbar-thumb,
html::-webkit-scrollbar-thumb {
    background: #383d4d;
    border-radius: 99em;
    border: 6px solid #1e1f26;
}


h1 {
    font-size: clamp(20px, 2.5vw, 36px);
    color: rgba(255, 255, 255, 0.8);
    font-weight: 600;
    text-align: center;
}

li img :nth-child(1) {
    display: block;
    width: 100%;
    max-width: 100%;
    margin-bottom: 1.5rem;
}

ul {
    padding: 0;
    margin: 0;
    display: block;
    width: 100%;
    overflow-y: hidden;
    overflow-x: auto;
    white-space: nowrap;
    text-align: center;
    scroll-behavior: smooth;
}

li {
    position: sticky;
    left: 0;
    width: min(50vw, 350px);
    display: inline-block;
    text-align: center;
    background-color: #16171f;
    color: #9b9dad;
    padding-bottom: 1.5rem;
    font-size: clamp(18px, 2.5vw, 22px);
    box-shadow: -10px 0 30px 0 rgba(0, 0, 0, 0.25);
    margin-left: -4px;
}
</style>