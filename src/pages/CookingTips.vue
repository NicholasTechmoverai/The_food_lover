<template>
  <div class="slider-wrapper">
    <div
      class="slider"
      style="--width: 240px; --height: 280px; --quantity: 9"
    >
      <div class="list">
        <div
          v-for="(recipe, index) in recipeTypes"
          :key="index"
          class="item"
          :style="`--i: ${index}`"
        >
          <div
            class="card flex flex-col items-center justify-center relative overflow-hidden"
          >
            <div class="gradient-bg" :style="`background: linear-gradient(to bottom right, ${recipe.gradient})`"></div>
            <img
              :src="recipe.image"
              :alt="recipe.title"
              class="w-24 h-24 rounded-full object-cover mb-4 border-2 border-white shadow-lg z-10"
            />
            <h3 class="text-lg font-bold text-white z-10">{{ recipe.title }}</h3>
            <p class="text-sm text-white/90 z-10 px-2">{{ recipe.description }}</p>
            <div class="absolute bottom-0 left-0 right-0 h-1 bg-white/30 z-10"></div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const recipeTypes = [
  {
    title: "Breakfast",
    description: "Start your day right",
    gradient: "#ff7e5f, #feb47b",
    image: "https://images.unsplash.com/photo-1557142046-c704a3adf364?w=200&h=200&fit=crop",
  },
  {
    title: "Vegan",
    description: "Plant-powered goodness",
    gradient: "#6a11cb, #2575fc",
    image: "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?w=200&h=200&fit=crop",
  },
  {
    title: "Desserts",
    description: "Sweet tooth treats",
    gradient: "#00c6ff, #0072ff",
    image: "https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=200&h=200&fit=crop",
  },
  {
    title: "Grilled",
    description: "Smoky & savory",
    gradient: "#ff512f, #dd2476",
    image: "https://images.unsplash.com/photo-1558030006-450675393462?w=200&h=200&fit=crop",
  },
  {
    title: "Soups",
    description: "Warm & comforting",
    gradient: "#ffb6c1, #ff69b4",
    image: "https://images.unsplash.com/photo-1547592180-85f173990554?w=200&h=200&fit=crop",
  },
  {
    title: "Salads",
    description: "Crisp & fresh",
    gradient: "#ff9a8b, #ffc3a0",
    image: "https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=200&h=200&fit=crop",
  },
  {
    title: "Pasta",
    description: "Italian favorites",
    gradient: "#a1c4fd, #c2e9fb",
    image: "https://images.unsplash.com/photo-1555949258-eb67b1ef0ceb?w=200&h=200&fit=crop",
  },
  {
    title: "Seafood",
    description: "Ocean delights",
    gradient: "#fbc2eb, #a18cd1",
    image: "https://images.unsplash.com/photo-1585238342024-78d387f4a707?w=200&h=200&fit=crop",
  },
  {
    title: "Snacks",
    description: "Quick bites",
    gradient: "#84fab0, #8fd3f4",
    image: "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=200&h=200&fit=crop",
  },
];
</script>

<style scoped>
.slider-wrapper {
  padding: 2rem 0;
  position: relative;
}

.slider {
  width: 100%;
  height: var(--height);
  position: relative;
  overflow: hidden;
  mask-image: linear-gradient(
    to right,
    transparent,
    black 5%,
    black 95%,
    transparent
  );
  -webkit-mask-image: linear-gradient(
    to right,
    transparent,
    black 5%,
    black 95%,
    transparent
  );
}

.slider .list {
  display: flex;
  position: absolute;
  left: 0;
  top: 0;
  height: 100%;
  width: calc(var(--width) * var(--quantity) * 2);
  animation: slide 30s linear infinite;
}

.slider:hover .list {
  animation-play-state: paused;
}

.card {
  width: calc(var(--width) - 20px);
  height: calc(var(--height) - 20px);
  margin: 0 10px;
  border-radius: 12px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  transition: transform 0.3s ease;
  position: relative;
  overflow: hidden;
}

.card:hover {
  transform: translateY(-8px) scale(1.03);
}

.gradient-bg {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

@keyframes slide {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(calc(var(--width) * var(--quantity) * -1));
  }
}

.item {
  width: var(--width);
  height: var(--height);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
}

@media (max-width: 768px) {
  .slider {
    mask-image: linear-gradient(
      to right,
      transparent,
      black 2%,
      black 98%,
      transparent
    );
    -webkit-mask-image: linear-gradient(
      to right,
      transparent,
      black 2%,
      black 98%,
      transparent
    );
  }
}

</style>