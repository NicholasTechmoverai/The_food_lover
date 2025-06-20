<template>
    <div class="relative sm:w-full lg:w-[1000px] bg-gray-300/0 h-auto max-h-[900px] perspective-1000">
        <img :src="image_design" alt="Mobile frame"
            class="pointer-events-none w-full h-full object-cover drop-shadow-2xl z-100" />


        <div ref="healthCards"
            class="custom-scrollbar absolute bg-amber-800/10 backdrop-blur-sm left-[39.5%] top-[11.5%] w-[43.5%] h-[58.5%] overflow-y-auto border border-amber-800/20 p-3 space-y-4">
        
            <div v-for="(benefit, index) in healthBenefits" :key="index"
                class="card relative group flex items-center gap-3 bg-white/80 rounded-lg p-3 shadow-sm overflow-hidden transition-all duration-300">
                <component :is="benefit.icon" class="w-6 h-6 text-amber-800 z-10" />
                <div class="z-10">
                    <h3 class="text-sm font-semibold text-amber-900">{{ benefit.title }}</h3>
                    <p class="text-xs text-gray-700">{{ benefit.description }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import image_design from '../assets/phoneinhand.png';
import { ref, onMounted, nextTick } from 'vue';
import { ShieldCheck, HeartPulse, Flame, Smile, Leaf } from 'lucide-vue-next';
import { siteConfig } from '../config/siteConfig.js'


// console.log(healthTitle)
const healthBenefits = ref([
    { title: 'Boosted Immunity', description: 'Nutrients like Vitamin C and Zinc support a strong immune system.', icon: ShieldCheck },
    { title: 'Improved Heart Health', description: 'Fiber-rich meals help lower cholesterol and blood pressure.', icon: HeartPulse },
    { title: 'More Energy', description: 'Whole foods fuel your body with long-lasting energy.', icon: Flame },
    { title: 'Clearer Skin', description: 'Antioxidants and hydration improve skin appearance.', icon: Smile },
    { title: 'Better Digestion', description: 'Probiotics and fiber promote a healthy gut.', icon: Leaf },
    { title: 'Improved Focus', description: 'Healthy fats and hydration support brain function.', icon: Flame },
    { title: 'Healthy Weight', description: 'Balanced meals promote metabolism and fullness.', icon: Leaf }
]);

const healthCards = ref(null);

const updateActiveCardOnScroll = () => {
    const container = healthCards.value;
    if (!container) return;

    const containerRect = container.getBoundingClientRect();
    const containerCenter = containerRect.top + containerRect.height / 2;

    let closestCard = null;
    let minDistance = Infinity;

    Array.from(container.children).forEach(card => {
        const rect = card.getBoundingClientRect();
        const cardCenter = rect.top + rect.height / 2;
        const distance = Math.abs(containerCenter - cardCenter);

        if (distance < minDistance) {
            minDistance = distance;
            closestCard = card;
        }
    });

    if (closestCard) {
        Array.from(container.children).forEach(card => card.classList.remove('active'));
        closestCard.classList.add('active');
    }
};


let currentIndex = 0;
let scrollDirection = 'down';

const scrollByOneCard = (direction = 'down') => {
    const offset = 112; // approx height (e.g., 96px card + 16px gap)
    if (healthCards.value) {
        healthCards.value.scrollBy({
            top: direction === 'down' ? offset : -offset,
            behavior: 'smooth'
        });
    }
};

onMounted(() => {
    nextTick(() => {
        const cards = healthCards.value?.children;
        if (healthCards.value) {
            healthCards.value.addEventListener('scroll', updateActiveCardOnScroll);
            updateActiveCardOnScroll(); // call once on load
        }
        setInterval(() => {
            // Clear old active states
            for (let i = 0; i < cards.length; i++) {
                cards[i].classList.remove('active');
            }

            // Set current active
            const currentCard = cards[currentIndex];
            currentCard.classList.add('active');

            currentIndex = (currentIndex + 1) % cards.length;

            // Handle scroll
            scrollByOneCard(scrollDirection);

            const { scrollTop, scrollHeight, clientHeight } = healthCards.value;

            if (scrollTop + clientHeight >= scrollHeight) {
                scrollDirection = 'up';
            } else if (scrollTop <= 0) {
                scrollDirection = 'down';
            }

        }, 2000);
    });
});
</script>


<style scoped>
.card {
    transition: transform 0.3s ease, background-color 0.3s ease;
}

.card.active {
    transform: scale(1.05);
    background-color: rgba(163, 21, 163, 0.397);
    /* subtle purple highlight */
}

/* Custom Scrollbar */
.custom-scrollbar::-webkit-scrollbar {
    width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
    background-color: rgba(168, 6, 217, 0.3);
    border-radius: 3px;
}

.custom-scrollbar::-webkit-scrollbar-track {
    background-color: rgba(54, 54, 52, 0.877);
    border-radius: 3px;
}
</style>
