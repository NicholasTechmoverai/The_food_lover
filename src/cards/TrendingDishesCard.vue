<template>
    <div class="wrapper  flex justify-center items-center px-4">
        <div class="carousel w-full max-w-md space-y-6">
            <div v-for="(dish, index) in data" :key="index" class="carousel__item  flex items-center  overflow-hidden">
                <div class="carousel__item-head w-24 h-24 flex-shrink-0 m-2" :style="{ backgroundColor: dish.theme }">
                    <img :src="dish.image" :alt="dish.alt"
                        class="w-full h-full object-cover rounded-full border border-gray-200 dark:border-gray-700"
                        @error="(e) => e.target.src = onerrorImage" />
                </div>
                <div
                    class="carousel__item-body hover:ring ring-gray-400/50 border-b duration-300 bg-white dark:bg-gray-900 flex flex-col justify-center pr-4">
                    <router-link :to="dish.url" class="title text-lg font-semibold text-gray-900 dark:text-white whitespace-nowrap">
                        {{ dish.title }}
                    </router-link>
                    <div
                        class="cook-info text-sm text-gray-600 dark:text-gray-400 space-x-1 flex flex-wrap items-center mb-1">
                        <span>{{ dish.cook_time?.hr }}hr</span>
                        <span>{{ dish.cook_time?.min }}min</span>
                        <span class="px-1">•</span>
                        <span>{{ dish.difficulty_level }}</span>
                    </div>

                    <div
                        class="cuisine-info text-sm text-gray-500 dark:text-gray-400 flex flex-wrap items-center gap-x-2">
                        <span v-if="dish.cuisine?.name">{{ dish.cuisine.name }}</span>
                        <span v-if="dish.cuisine?.region">({{ dish.cuisine.region }})</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>



<script setup>
import { ref } from 'vue';
import onerrorImage from '../assets/onerrorimage.png'

const props = defineProps({
    data: {
        type: Object
    }
})
const dishes = ref([
    {
        title: "Ugali & Sukuma Wiki",
        cook_time: "30 mins",
        description: "Kenya's staple food with collard greens",
        image: "https://images.unsplash.com/photo-1563805042-7684c019e1cb"
    },
    {
        title: "Nyama Choma",
        cook_time: "2-3 hours",
        description: "Grilled meat, Kenya's favorite delicacy",
        image: "https://images.unsplash.com/photo-1563805042-7684c019e1cb"
    },
    {
        title: "Githeri",
        cook_time: "1 hour",
        description: "Boiled maize and beans mixture",
        image: "https://www.kenyans.co.ke/files/styles/article_style/public/images/media/githeri.jpg"
    },
    {
        title: "Chapati",
        cook_time: "45 mins",
        description: "Flatbread with East African origins",
        image: "https://www.kenyans.co.ke/files/styles/article_style/public/images/media/chapati.jpg"
    },
    {
        title: "Pilau",
        cook_time: "1 hour",
        description: "Spiced rice dish with meat",
        image: "https://www.kenyans.co.ke/files/styles/article_style/public/images/media/pilau.jpg"
    },
    {
        title: "Mukimo",
        cook_time: "50 mins",
        description: "Mashed potatoes with greens and maize",
        image: "https://www.kenyans.co.ke/files/styles/article_style/public/images/media/mukimo.jpg"
    },
    {
        title: "Matoke",
        cook_time: "40 mins",
        description: "Stewed plantains with meat",
        image: "https://www.kenyans.co.ke/files/styles/article_style/public/images/media/matoke.jpg"
    },
    {
        title: "Mandazi",
        cook_time: "30 mins",
        description: "Swahili coconut doughnuts",
        image: "https://www.kenyans.co.ke/files/styles/article_style/public/images/media/mandazi.jpg"
    },
    {
        title: "Samaki Wa Kupaka",
        cook_time: "45 mins",
        description: "Coconut fish curry",
        image: "https://www.kenyans.co.ke/files/styles/article_style/public/images/media/samaki-wa-kupaka.jpg"
    }
]);
</script>




<style scoped>
*,
*::before,
*::after {
    box-sizing: border-box;
}

body {
    font-family: "Work Sans", sans-serif;
    font-weight: 400;
    height: 100vh;
}

.wrapper {
    height: 100%;
    width: 100%;
    display: flex;
    justify-content: center;
}

.carousel {
    position: relative;
    width: 100%;
    max-width: 500px;
    display: flex;
    justify-content: center;
    flex-direction: column;
}

.carousel__item {
    display: flex;
    align-items: center;
    position: absolute;
    width: 100%;
    padding: 0 12px;
    opacity: 0;
    filter: drop-shadow(0 2px 2px #555);
    will-change: transform, opacity;
    -webkit-animation: carousel-animate-vertical 27s linear infinite;
    animation: carousel-animate-vertical 27s linear infinite;
}

.carousel__item:nth-child(1) {
    -webkit-animation-delay: calc(3s * -1);
    animation-delay: calc(3s * -1);
}

.carousel__item:nth-child(2) {
    -webkit-animation-delay: calc(3s * 0);
    animation-delay: calc(3s * 0);
}

.carousel__item:nth-child(3) {
    -webkit-animation-delay: calc(3s * 1);
    animation-delay: calc(3s * 1);
}

.carousel__item:nth-child(4) {
    -webkit-animation-delay: calc(3s * 2);
    animation-delay: calc(3s * 2);
}

.carousel__item:nth-child(5) {
    -webkit-animation-delay: calc(3s * 3);
    animation-delay: calc(3s * 3);
}

.carousel__item:nth-child(6) {
    -webkit-animation-delay: calc(3s * 4);
    animation-delay: calc(3s * 4);
}

.carousel__item:nth-child(7) {
    -webkit-animation-delay: calc(3s * 5);
    animation-delay: calc(3s * 5);
}

.carousel__item:nth-child(8) {
    -webkit-animation-delay: calc(3s * 6);
    animation-delay: calc(3s * 6);
}

.carousel__item:last-child {
    -webkit-animation-delay: calc(-3s * 2);
    animation-delay: calc(-3s * 2);
}

.carousel__item-head {
    border-radius: 50%;
    width: 90px;
    height: 90px;
    padding: 7px;
    position: relative;
    margin-right: -45px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 50px;
}

.carousel__item-body {
    width: 100%;
    /* background-color: #fff; */
    border-radius: 8px;
    padding: 16px 20px 16px 70px;
}

.title {
    text-transform: uppercase;
    font-size: 20px;
    margin-top: 10px;
}

@-webkit-keyframes carousel-animate-vertical {
    0% {
        transform: translateY(100%) scale(0.5);
        opacity: 0;
        visibility: hidden;
    }

    3%,
    11.1111111111% {
        transform: translateY(100%) scale(0.7);
        opacity: 0.4;
        visibility: visible;
    }

    14.1111111111%,
    22.2222222222% {
        transform: translateY(0) scale(1);
        opacity: 1;
        visibility: visible;
    }

    25.2222222222%,
    33.3333333333% {
        transform: translateY(-100%) scale(0.7);
        opacity: 0.4;
        visibility: visible;
    }

    36.3333333333% {
        transform: translateY(-100%) scale(0.5);
        opacity: 0;
        visibility: visible;
    }

    100% {
        transform: translateY(-100%) scale(0.5);
        opacity: 0;
        visibility: hidden;
    }
}

@keyframes carousel-animate-vertical {
    0% {
        transform: translateY(100%) scale(0.5);
        opacity: 0;
        visibility: hidden;
    }

    3%,
    11.1111111111% {
        transform: translateY(100%) scale(0.7);
        opacity: 0.4;
        visibility: visible;
    }

    14.1111111111%,
    22.2222222222% {
        transform: translateY(0) scale(1);
        opacity: 1;
        visibility: visible;
    }

    25.2222222222%,
    33.3333333333% {
        transform: translateY(-100%) scale(0.7);
        opacity: 0.4;
        visibility: visible;
    }

    36.3333333333% {
        transform: translateY(-100%) scale(0.5);
        opacity: 0;
        visibility: visible;
    }

    100% {
        transform: translateY(-100%) scale(0.5);
        opacity: 0;
        visibility: hidden;
    }
}
</style>
