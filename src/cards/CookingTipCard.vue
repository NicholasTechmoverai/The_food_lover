<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Fira+Sans:wght@300;400;600&display=swap");

*,
*:before,
*:after {
  box-sizing: inherit;
}

img {
  max-width: 100%;
  height: auto;
}

body {
  -webkit-text-size-adjust: 100%;
  font-variant-ligatures: none;
  text-rendering: optimizeLegibility;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  font-size: 100%;
  font-family: "Fira Sans", sans-serif;
}

h1,
h2,
h3,
h4,
h5 {
  font-weight: 800;
  margin-top: 0;
  margin-bottom: 0;
}


.card-hover {
  min-width: 300px;
  width: 100%;
  max-width: 400px;
  height: 500px;
  position: relative;
  overflow: hidden;
  box-shadow: 0 0 32px -10px rgba(0, 0, 0, 0.08);
}

.card-hover:has(.card-hover__link:hover) .card-hover__extra {
  transform: translateY(0);
  transition: transform 0.35s;
}

.card-hover:hover .card-hover__content {
  background-color: #DEE8C2;
  bottom: 100%;
  transform: translateY(100%);
  padding: 50px 60px;
  transition: all 0.35s cubic-bezier(0.1, 0.72, 0.4, 0.97);
}

.card-hover:hover .card-hover__link {
  opacity: 1;
  transform: translate(-50%, 0);
  transition: all 0.3s 0.35s cubic-bezier(0.1, 0.72, 0.4, 0.97);
}

.card-hover:hover img {
  transform: scale(1);
  transition: 0.35s 0.1s transform cubic-bezier(0.1, 0.72, 0.4, 0.97);
}

.card-hover__content {
  width: 100%;
  text-align: center;
  background-color: #86B971;
  padding: 0 60px 50px;
  position: absolute;
  bottom: 0;
  left: 0;
  transform: translateY(0);
  transition: all 0.35s 0.35s cubic-bezier(0.1, 0.72, 0.4, 0.97);
  will-change: bottom, background-color, transform, padding;
  z-index: 1;
}

.card-hover__content::before,
.card-hover__content::after {
  content: "";
  width: 100%;
  height: 120px;
  background-color: inherit;
  position: absolute;
  left: 0;
  z-index: -1;
}

.card-hover__content::before {
  top: -80px;
  -webkit-clip-path: ellipse(60% 80px at bottom center);
  clip-path: ellipse(60% 80px at bottom center);
}

.card-hover__content::after {
  bottom: -80px;
  -webkit-clip-path: ellipse(60% 80px at top center);
  clip-path: ellipse(60% 80px at top center);
}

.card-hover__title {
  font-size: 1.5rem;
  margin-bottom: 1em;
}

.card-hover__title span {
  color: #2d7f0b;
}

.card-hover__text {
  font-size: 0.75rem;
}

.card-hover__link {
  position: absolute;
  bottom: 1rem;
  left: 50%;
  transform: translate(-50%, 10%);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  text-decoration: none;
  color: #2d7f0b;
  opacity: 0;
  padding: 10px;
  transition: all 0.35s;
}

.card-hover__link:hover svg {
  transform: translateX(4px);
}

.card-hover__link svg {
  width: 18px;
  margin-left: 4px;
  transition: transform 0.3s;
}

.card-hover__extra {
  height: 50%;
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 100%;
  font-size: 1.5rem;
  text-align: center;
  background-color: #86b971;
  padding: 80px;
  bottom: 0;
  z-index: 0;
  color: #dee8c2;
  transform: translateY(100%);
  will-change: transform;
  transition: transform 0.35s;
}

.card-hover__extra span {
  color: #2d7f0b;
}

.card-hover img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  -o-object-fit: cover;
  object-fit: cover;
  -o-object-position: center;
  object-position: center;
  z-index: -1;
  transform: scale(1.2);
  transition: 0.35s 0.35s transform cubic-bezier(0.1, 0.72, 0.4, 0.97);
}
</style>

<template>
  <div class="card-hover w-full max-w-[400px]">
    <div class="card-hover__content">
      <h4> <span class="inline-block px-3 py-1 mb-3 text-xs font-bold tracking-wider uppercase rounded-full"
          :class="categoryColorMap[tip.category]">
          {{ formatCategoryName(tip.category) }}
        </span></h4>
      <h3 class="card-hover__title">
        {{ tip.title }}
      </h3>
      <p class="card-hover__text">{{ tip.description }}</p>
      <a href="#" class="card-hover__link">
        <span>About</span>
        <svg fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
        </svg>
      </a>
    </div>
    <div class="card-hover__extra">
      <h4>:: <span>{{ tip.category }}</span> </h4>
      <div class="relative">
        <img :src="tip.user.avatar" alt="" class="w-30 h-30 rounded-full"
          style="height: 50px;width: 50px; border-radius:50%">
        <p class="relative"><span>@{{ tip.user.username }}</span></p>
      </div>
    </div>
    <div class="flex flex-row" style="z-index: 999999;">
      <p>{{ formatDate(tip.createdAt) }}</p>
      <span v-if="tip.isPopular">🔥</span>
    </div>
    <img :src="tip.image" :alt="tip.title" @error="(e) => e.target.src = default_image">
  </div>
</template>

<script setup>

const props = defineProps({
  tip: {
    type: Object,
    default: () => null
  }
})

const default_image = "https://images.unsplash.com/photo-1586511925558-a4c6376fe65f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=60"

const categoryColorMap = {
  'knife skills': 'bg-rose-100 text-rose-800 dark:bg-rose-900/30 dark:text-rose-300',
  'flavourpairing': 'bg-indigo-100 text-indigo-800 dark:bg-indigo-900/30 dark:text-indigo-300',
  'timesaving': 'bg-amber-100 text-amber-800 dark:bg-amber-900/30 dark:text-amber-300',
  'substitutions': 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/30 dark:text-emerald-300',
  'presentation': 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300',
  'equipment': 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300'
};

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

const formatCategoryName = (category) => {
  return category.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
};
</script>