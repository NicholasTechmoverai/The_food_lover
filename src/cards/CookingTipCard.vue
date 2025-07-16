<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Fira+Sans:wght@300;400;600;800&display=swap");

.card-hover {
  min-width: 300px;
  width: 100%;
  max-width: 400px;
  height: 500px;
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.card-hover:hover {
  box-shadow: 0 15px 40px -5px rgba(0, 0, 0, 0.15);
  transform: translateY(-5px);
}

.card-hover:has(.card-hover__link:hover) .card-hover__extra {
  transform: translateY(0);
  transition: transform 0.35s;
}

.card-hover:hover .card-hover__content {
  background-color: #E8F4D9;
  bottom: 100%;
  transform: translateY(100%);
  padding: 40px 30px;
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
  padding: 0 30px 40px;
  position: absolute;
  bottom: 0;
  left: 0;
  transform: translateY(0);
  transition: all 0.35s 0.35s cubic-bezier(0.1, 0.72, 0.4, 0.97);
  will-change: bottom, background-color, transform, padding;
  z-index: 1;
  border-radius: 0 0 12px 12px;
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
  clip-path: ellipse(60% 80px at bottom center);
}

.card-hover__content::after {
  bottom: -80px;
  clip-path: ellipse(60% 80px at top center);
}

.card-hover__title {
  font-size: 1.5rem;
  margin-bottom: 1em;
  line-height: 1.3;
  color: #2A3F1E;
}

.card-hover__title span {
  color: #2d7f0b;
}

.card-hover__text {
  font-size: 0.9rem;
  line-height: 1.5;
  color: #3E5034;
  margin-bottom: 1.5em;
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
  color: #2A3F1E;
  font-weight: 600;
  opacity: 0;
  padding: 10px 15px;
  background-color: rgba(255, 255, 255, 0.2);
  border-radius: 50px;
  backdrop-filter: blur(5px);
  transition: all 0.35s;
}

.card-hover__link:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.card-hover__link:hover svg {
  transform: translateX(4px);
}

.card-hover__link svg {
  width: 18px;
  margin-left: 8px;
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
  padding: 30px;
  bottom: 0;
  z-index: 0;
  color: #F0F7E6;
  transform: translateY(100%);
  will-change: transform;
  transition: transform 0.35s;
  border-radius: 0 0 12px 12px;
}

.card-hover__extra h4 {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #F0F7E6;
}

.card-hover__extra span {
  color: #E8F4D9;
  font-weight: 800;
}

.card-hover img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  z-index: -1;
  transform: scale(1.2);
  transition: 0.35s 0.35s transform cubic-bezier(0.1, 0.72, 0.4, 0.97);
}

.card-meta {
  position: absolute;
  top: 20px;
  left: 20px;
  right: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 2;
}

.card-category {
  display: inline-block;
  padding: 4px 8px;
  margin-bottom: 15px;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-radius: 50px;
}

.card-date {
  font-size: 0.8rem;
  color: white;
  background-color: rgba(0, 0, 0, 0.4);
  padding: 4px 10px;
  border-radius: 50px;
  backdrop-filter: blur(5px);
}

.card-popular {
  font-size: 0.8rem;
  color: white;
  background-color: rgba(255, 100, 0, 0.4);
  padding: 4px 10px;
  border-radius: 50px;
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  gap: 4px;
}

.user-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 1rem;
}

.user-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid #E8F4D9;
  margin-bottom: 0.5rem;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: #F0F7E6;
}

.user-username {
  font-size: 0.8rem;
  color: #DEE8C2;
}
</style>

<template>
  <div class="card-hover w-full max-w-[400px]">
    <div class="card-meta">
      <span class="card-category" :class="categoryColorMap[tip.category]">
        {{ formatCategoryName(tip.category) }}
      </span>
      <div class="flex items-center gap-2">
        <span class="card-date">{{ formatDate(tip.createdAt) }}</span>
        <span v-if="tip.isPopular" class="card-popular">🔥</span>
      </div>
    </div>
    
    <div class="card-hover__content">
      <h3 class="card-hover__title">
        {{ tip.title }}
      </h3>
      <p class="card-hover__text">{{ tip.description }}</p>
      <a href="#" class="card-hover__link">
        <span>Read more</span>
        <svg fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
        </svg>
      </a>
    </div>
    
    <div class="card-hover__extra">
      <h4>:: <span>{{ tip.category }}</span> ::</h4>
      <div class="user-info">
        <img :src="tip.user.avatar" :alt="tip.user.name" class="user-avatar">
        <p class="user-name">{{ tip.user.name }}</p>
        <p class="user-username">@{{ tip.user.username }}</p>
      </div>
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