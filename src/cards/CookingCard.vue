<template>
    <div class="overflow-visible h-full relative flex flex-col items-center justify-center z-50">
        <p class="text-center leading-relaxed mt-6">
            <span :style="{ fontFamily: siteConfig.welcomeMessage.fontFamily }" class="p-1 font-cursive drop-shadow-sm animate-text-gradient">{{ cookingHeadline }}</span>
            <span :style="{color:siteConfig.colors.text.secondary}" class="block mt-2 text-lg text-gray-700 font-sans">
                {{ cookinngMotto }}
            </span>
            <span :style="{color:siteConfig.colors.text.primary}" class=" block text-md mt-1 text-purple-500 font-sans italic">
                {{ cookingDescription }}
            </span>
        </p>

        <div class="perspective-1000 relative h-full mt-[200px] ">
            <div
                class="absolute left-[-15%] w-full h-[400px] bg-transparent overflow-visible flex items-start justify-center z-30">

                <!-- Falling Ingredient -->
                <div v-if="phase === 'falling' && currentThing"
                    class="absolute text-6xl font-black animate-fall select-none pointer-events-none"
                    :style="{ color: currentThing.fallColor }">
                    <img :src="currentThing.fallSymbol" alt="ingredient falling" srcset=""
                        class="objects w-[250px] z-40">
                </div>

                <!-- Rising Cooked Result -->
                <div v-if="phase === 'returning' && currentThing"
                    class="absolute text-6xl font-black animate-rise-fade select-none pointer-events-none"
                    :style="{ color: currentThing.riseColor }">
                    <img :src="currentThing.riseSymbol" alt="ingredient rising" srcset=""
                        class="objects w-[250px] z-40">
                </div>
            </div>

            <img :class="lidClosed ? 'lid-close' : 'lid-open'"
                class="close-open pointer-events-none select-none z-50 absolute" :src="lid_image" alt="Cooking Pot Lid"
                srcset="">
            <img class="pointer-events-none select-none z-20" :src="pot_image" alt="Cooking Pot" srcset="">
            <div
                class="inpot  z-0 absolute inset-0 rounded-[60%] w-[55%] h-[35%] left-[10%] top-[30%] flex items-center justify-center">
            </div>
        </div>
    </div>
</template>
<script setup>
import pot_image from '../assets/5c3227c8a97bc40295eb8431.png';
import lid_image from '../assets/lid-removebg-preview.png';
import eggs from '../assets/eggs-removebg-preview.png';
import cookedeggs from '../assets/cookedegg-removebg-preview.png'
import potatoes from '../assets/potatoes-removebg-preview.png';
import fries from '../assets/pexels-photo-2498440-removebg-preview.png'
import lemonfruit from '../assets/lemonfruit-removebg-preview.png';
// import sodacan from '../assets/sodacan-removebg-preview.png'
import lemonjuice from '../assets/pexels-photo-96620-removebg-preview.png'
import mixedbeans from '../assets/mixedbeans-removebg-preview.png';
import beansstew from '../assets/githeristew-removebg-preview.png';
import flour from '../assets/flour-removebg-preview.png';
import chapati from '../assets/chapati-removebg-preview.png';
import boxedtea from '../assets/boxedtea-removebg-preview.png';
import tea from '../assets/servedtea-removebg-preview.png'
import rooster from '../assets/roster-removebg-preview.png';
import chickenwings from '../assets/pexels-babydov-7788311-removebg-preview.png';
import chihuahua from '../assets/pexels-goochie-poochie-3299908-removebg-preview.png';
import dogfood from '../assets/0nqx8qas-removebg-preview.png';
import { ref, onMounted } from 'vue';
import { useSiteStore } from '../config/siteConfig';
const { siteConfig, getResponsiveValue } = useSiteStore()

const sequence = [
    { fallSymbol: eggs, fallColor: '#facc15', riseSymbol: cookedeggs, riseColor: '#fbbf24' },
    { fallSymbol: potatoes, fallColor: '#fb923c', riseSymbol: fries, riseColor: '#f97316' },
    { fallSymbol: lemonfruit, fallColor: '#fcd34d', riseSymbol: lemonjuice, riseColor: '#fde68a' },
    { fallSymbol: mixedbeans, fallColor: '#60a5fa', riseSymbol: beansstew, riseColor: '#3b82f6' },
    { fallSymbol: flour, fallColor: '#d97706', riseSymbol: chapati, riseColor: '#92400e' },
    { fallSymbol: boxedtea, fallColor: '#facc15', riseSymbol: tea, riseColor: '#fbbf24' },
    { fallSymbol: rooster, fallColor: '#f87171', riseSymbol: chickenwings, riseColor: '#ef4444' },
    // { fallSymbol: chihuahua, fallColor: '#fbbf24', riseSymbol: dogfood, riseColor: '#f97316' }
];
const cookingHeadline = ref('Cooking tips right in your phone');
const cookinngMotto = ref('Cooking is an art, and we are your canvas!');
const cookingDescription = ref('Watch your ingredients transform into delicious dishes!!!')

const currentThing = ref(null);
const phase = ref('falling');
const lidClosed = ref(false);
let index = 0;

const dropSequence = () => {
    currentThing.value = sequence[index % sequence.length];
    phase.value = 'falling';
    lidClosed.value = false;
    index++;

    // ⏱️ Lid closes earlier — before fall ends
    setTimeout(() => {
        lidClosed.value = true;

        // Hide falling item slightly after lid closes
        setTimeout(() => {
            phase.value = 'waiting';
        }, 400); // reduced to avoid abrupt disappearance

        // Start rise after short lid-closed pause
        setTimeout(() => {
            lidClosed.value = false;
            phase.value = 'returning';

            setTimeout(() => {
                phase.value = 'waiting';
                currentThing.value = null;
                setTimeout(dropSequence, 300);
            }, 3000); // rise duration

        }, 1000); // wait while lid stays closed

    }, 1200); // << earlier lid close (used to be 1500)
};


onMounted(() => {
    dropSequence();
});
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Pacifico&display=swap');

.font-cursive {
  font-family: 'Pacifico', cursive;
}

.font-sans {
  font-family: 'Inter', sans-serif;
}
.objects {
    z-index: 100 !important;
}

.perspective-1000 {
    perspective: 1000px;
}

.close-open {
    position: absolute;
    transform-origin: bottom center;
    animation-fill-mode: forwards;
    top: 25%;
}


.inpot {
    transform: rotateY(0deg) rotateX(40deg);
    transform-style: preserve-3d;
    transition: transform 0.4s ease;
    z-index: 0 !important;

    background: rgba(22, 17, 17, 0.842);
    /* Light gray for contrast */
    box-shadow:
        inset 0 6px 12px rgba(0, 0, 0, 0.3),
        /* Top inner shadow */
        inset 0 -6px 16px rgba(255, 255, 255, 0.2),
        /* Bottom inner highlight */
        inset 6px 0 10px rgba(0, 0, 0, 0.1),
        /* Left side light shadow */
        inset -6px 0 10px rgba(0, 0, 0, 0.1),
        /* Right side light shadow */
        0 8px 20px rgba(0, 0, 0, 0.15);
    /* Outer soft shadow for lift */
}

@keyframes fall {
    0% {
        top: -100px;
        opacity: 0;
        transform: scale(1);
    }

    75% {
        opacity: 1;
        transform: scale(1.15);
    }

    85% {
        opacity: 0.5;
    }

    90% {
        top: 30%;
        opacity: 0;
        transform: scale(1.15);
    }

    100% {
        top: 40%;
        opacity: 0;
        transform: scale(1.15);
    }
}

.animate-fall {
    position: absolute;
    top: 0;
    animation: fall 1.8s ease-in forwards;
}

@keyframes rise-fade {
    0% {
        top: 55%;
        opacity: 0;
        transform: scale(1);
    }

    5% {
        opacity: 1;
    }

    50% {
        opacity: 1;
    }

    100% {
        top: -45%;
        opacity: 0;
        transform: scale(0.85);
    }
}

.animate-rise-fade {
    position: absolute;
    top: 75%;
    animation: rise-fade 3s ease-out forwards;
}

.lid-open {

    animation: slidein 0.5s ease-in forwards;
    transition: transform 0.5s ease-in;
}

.lid-close {
    animation: slideoff 0.5s ease-in forwards;
    transition: transform 0.5s ease-in;

}

@keyframes slidein {
    0% {
        transform: translateX(-12%) translateY(-20%) scale(0.9) rotateX(0deg) rotateZ(0deg);
        opacity: 1;
    }

    100% {
        transform: translateX(50%) translateY(20%) scale(0.8) rotateX(0deg) rotateZ(-20deg);
        opacity: 0.85;
    }
}

@keyframes slideoff {
    0% {
        transform: translateX(50%) translateY(20%) scale(0.8) rotateZ(-20deg);
        opacity: 0.85;
    }

    100% {
        transform: translateX(-12%) translateY(-20%) scale(0.9) rotateZ(0deg);
        opacity: 1;
    }
}
</style>
