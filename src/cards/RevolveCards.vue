<style scoped>
@keyframes autoRun3d {
  from {
    transform: perspective(800px) rotateY(-360deg);
  }

  to {
    transform: perspective(800px) rotateY(0deg);
  }
}

@keyframes animateBrightness {
  10% {
    filter: brightness(1);
  }

  50% {
    filter: brightness(0.1);
  }

  90% {
    filter: brightness(1);
  }
}

.card-3d {
  position: relative;
  width: 420px;
  height: 200px;
  transform-style: preserve-3d;
  transform: perspective(800px);
  animation: autoRun3d 20s linear infinite;
  will-change: transform;
}

.card-3d div {
  position: absolute;
  width: 90px;
  height: 120px;
  background-color: rgb(199, 199, 199);
  border: solid 2px lightgray;
  border-radius: 0.5rem;
  top: 50%;
  left: 50%;
  transform-origin: center center;
  animation: animateBrightness 20s linear infinite;
  transition-duration: 200ms;
  will-change: transform, filter;
}

.card-3d:hover {
  animation-play-state: paused !important;
}

.card-3d:hover div {
  animation-play-state: paused !important;
}

.card-3d div:nth-child(1) {
  transform: translate(-50%, -50%) rotateY(0deg) translateZ(150px);
  animation-delay: -0s;
}

.card-3d div:nth-child(2) {
  transform: translate(-50%, -50%) rotateY(36deg) translateZ(150px);
  animation-delay: -2s;
}

.card-3d div:nth-child(3) {
  transform: translate(-50%, -50%) rotateY(72deg) translateZ(150px);
  animation-delay: -4s;
}

.card-3d div:nth-child(4) {
  transform: translate(-50%, -50%) rotateY(108deg) translateZ(150px);
  animation-delay: -6s;
}

.card-3d div:nth-child(5) {
  transform: translate(-50%, -50%) rotateY(144deg) translateZ(150px);
  animation-delay: -8s;
}

.card-3d div:nth-child(6) {
  transform: translate(-50%, -50%) rotateY(180deg) translateZ(150px);
  animation-delay: -10s;
}

.card-3d div:nth-child(7) {
  transform: translate(-50%, -50%) rotateY(216deg) translateZ(150px);
  animation-delay: -12s;
}

.card-3d div:nth-child(8) {
  transform: translate(-50%, -50%) rotateY(252deg) translateZ(150px);
  animation-delay: -14s;
}

.card-3d div:nth-child(9) {
  transform: translate(-50%, -50%) rotateY(288deg) translateZ(150px);
  animation-delay: -16s;
}

.card-3d div:nth-child(10) {
  transform: translate(-50%, -50%) rotateY(324deg) translateZ(150px);
  animation-delay: -18s;
}
</style>

<template>
  <div class="card-3d grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3 p-4">
    <div
      v-for="(c, i) in staff"
      :key="i"
      class="bg-white dark:bg-gray-800 shadow-md rounded-xl p-2 flex flex-col items-center text-center text-[10px] whitespace-nowrap overflow-hidden"
    >
      <p v-if="c.live" class="text-green-500 font-semibold text-[9px] mb-1 uppercase tracking-wide">Live</p>
      <img
        :src="c.chef.profilePic || 'https://via.placeholder.com/40'"
        :alt="c.chef.name || 'Chef'"
        class="w-10 h-10 rounded-full object-cover mb-1"
      />
      <p class="font-medium text-gray-800 truncate w-full">{{ c.meal }}</p>
      <p class="text-gray-500  text-[9px] mt-0.5">{{formatDate( c.date) }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const formatDate = (date) => {
  if (typeof date === 'string') return date;
  return new Date(date).toLocaleDateString('en-US', { day: 'numeric', month: 'short', year: 'numeric' });
};

const staff = ref([
  {
    live: true,
    date: '2025-07-20',
    meal: 'Ugali Pasta with Special Sauce and Extra Toppings',
    chef: {
      profilePic: '',
      name: 'Chef John Doe',
      id: '1',
    }
  },
  {
    live: true,
    date: '2025-07-20',
    meal: 'Chapati Beans',
    chef: {
      profilePic: 'https://randomuser.me/api/portraits/men/32.jpg',
      name: 'Chef Maria',
      id: '2',
    }
  },
  {
    live: false,
    date: '2025-07-21',
    meal: 'Pilau with Kachumbari',
    chef: {
      profilePic: 'https://randomuser.me/api/portraits/women/44.jpg',
      name: 'Chef Amina',
      id: '3',
    }
  },
  {
    live: true,
    date: '2025-07-22',
    meal: 'Nyama Choma Special',
    chef: {
      profilePic: 'https://randomuser.me/api/portraits/men/75.jpg',
      name: 'Chef Kamau',
      id: '4',
    }
  },
  {
    live: false,
    date: '2025-07-23',
    meal: 'Mukimo with Greens',
    chef: {
      profilePic: 'https://randomuser.me/api/portraits/women/68.jpg',
      name: 'Chef Wanjiku',
      id: '5',
    }
  },
  {
    live: true,
    date: '2025-07-24',
    meal: 'Fish Curry with Coconut Rice',
    chef: {
      profilePic: 'https://randomuser.me/api/portraits/men/90.jpg',
      name: 'Chef Ali',
      id: '6',
    }
  },
  {
    live: false,
    date: '2025-07-25',
    meal: 'Vegetable Stir Fry with Noodles',
    chef: {
      profilePic: 'https://randomuser.me/api/portraits/women/33.jpg',
      name: 'Chef Lin',
      id: '7',
    }
  },
  {
    live: true,
    date: '2025-07-26',
    meal: 'Mandazi with Chai',
    chef: {
      profilePic: 'https://randomuser.me/api/portraits/men/22.jpg',
      name: 'Chef Bakari',
      id: '8',
    }
  },
  {
    live: false,
    date: '2025-07-27',
    meal: 'Githeri Special',
    chef: {
      profilePic: 'https://randomuser.me/api/portraits/women/29.jpg',
      name: 'Chef Njeri',
      id: '9',
    }
  },
  {
    live: true,
    date: '2025-07-28',
    meal: 'Bhajia with Tamarind Sauce',
    chef: {
      profilePic: 'https://randomuser.me/api/portraits/men/45.jpg',
      name: 'Chef Raj',
      id: '10',
    }
  }
]);
</script>