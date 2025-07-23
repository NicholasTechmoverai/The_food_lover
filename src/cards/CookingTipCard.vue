<template>
  <article class="card-hover":style="{ '--theme-color': auth.user?.theme || '#f97316' }">
    <div class="card-meta">
      <span class="card-category" :class="categoryClass">
        {{ formatCategoryName(tip.category) }}
      </span>
      <div class="meta-right">
        <span class="card-date">{{ formatDate(tip.createdAt) }}</span>
        <span v-if="tip.isPopular" class="card-popular">
          <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M12.395 2.553a1 1 0 00-1.45-.385c-.345.23-.614.558-.822.88-.214.33-.403.713-.57 1.116-.334.804-.614 1.768-.84 2.734a31.365 31.365 0 00-.613 3.58 2.64 2.64 0 01-.945-1.067c-.328-.68-.398-1.534-.398-2.654A1 1 0 005.05 6.05 6.981 6.981 0 003 11a7 7 0 1011.95-4.95c-.592-.591-.98-.985-1.348-1.467-.363-.476-.724-1.063-1.207-2.03zM12.12 15.12A3 3 0 017 13s.879.5 2.5.5c0-1 .5-4 1.25-4.5.5 1 .786 1.293 1.371 1.879A2.99 2.99 0 0113 13a2.99 2.99 0 01-.879 2.121z" clip-rule="evenodd" />
          </svg>
          Popular
        </span>
      </div>
    </div>
    
    <div class="card-content bg-[var(--theme-color)]">
      <h3 class="card-title">
        {{ tip.title }}
      </h3>
      <p class="card-text">{{ truncateDescription(tip.description, 120) }}</p>
      <a href="#" class="card-link" aria-label="Read more about this tip">
        <span>Read more</span>
        <svg fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
        </svg>
      </a>
    </div>
    
    <div class="card-extra bg-[var(--theme-color)]">
      <h4 class="extra-title">
        <span class="extra-delimiter">::</span> 
        <span class="extra-category">{{ tip.category }}</span> 
        <span class="extra-delimiter">::</span>
      </h4>
      <div class="user-info">
        <img 
          :src="tip.user.avatar" 
          :alt="tip.user.name" 
          class="user-avatar"
          loading="lazy"
          width="50"
          height="50"
        >
        <p class="user-name">{{ tip.user.name }}</p>
        <p class="user-username">@{{ tip.user.username }}</p>
      </div>
    </div>
    
    <img 
      :src="tip.image" 
      :alt="tip.title" 
      class="card-image"
      loading="lazy"
      @error="handleImageError"
    >
  </article>
</template>

<script setup>
import {ref ,computed} from 'vue'
import { useAuthStore } from '../store/user'
const auth = useAuthStore()
const props = defineProps({
  tip: {
    type: Object,
    required: true,
    validator: (value) => {
      return [
        'title',
        'description',
        'category',
        'createdAt',
        'image',
        'user'
      ].every(key => key in value)
    }
  }
})

const default_image = "https://images.unsplash.com/photo-1586511925558-a4c6376fe65f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=687&q=60"

const categoryClass = computed(() => {
  const classes = {
    'knife skills': 'category-knife',
    'flavourpairing': 'category-flavour',
    'timesaving': 'category-time',
    'substitutions': 'category-substitute',
    'presentation': 'category-presentation',
    'equipment': 'category-equipment'
  };
  return classes[props.tip.category] || '';
});

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric' };
  return new Date(dateString).toLocaleDateString(undefined, options);
};

const formatCategoryName = (category) => {
  return category.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase());
};

const truncateDescription = (text, maxLength) => {
  return text.length > maxLength ? `${text.substring(0, maxLength)}...` : text;
};

const handleImageError = (e) => {
  e.target.src = default_image;
};
</script>

<style scoped>
.card-hover {
  min-width: 300px;
  width: 100%;
  max-width: 400px;
  height: 500px;
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.1);
  transition: all 0.3s cubic-bezier(0.1, 0.72, 0.4, 0.97);
  /* border: 1px solid #e5e7eb; */
}

.card-hover:hover {
  box-shadow: 0 15px 40px -5px rgba(0, 0, 0, 0.15);
  transform: translateY(-5px);
}

.card-meta {
  position: absolute;
  top: 20px;
  left: 20px;
  right: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 30;
}

.card-category {
  display: inline-block;
  padding: 4px 12px;
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-radius: 50px;
}

.category-knife {
  background-color: rgba(251, 207, 232, 0.8);
  color: rgba(157, 23, 77, 0.9);
}

.category-flavour {
  background-color: rgba(224, 231, 255, 0.8);
  color: rgba(67, 56, 202, 0.9);
}

.category-time {
  background-color: rgba(254, 243, 199, 0.8);
  color: rgba(146, 64, 14, 0.9);
}

.category-substitute {
  background-color: rgba(209, 250, 229, 0.8);
  color: rgba(6, 95, 70, 0.9);
}

.category-presentation {
  background-color: rgba(233, 213, 255, 0.8);
  color: rgba(107, 33, 168, 0.9);
}

.category-equipment {
  background-color: rgba(219, 234, 254, 0.8);
  color: rgba(29, 78, 216, 0.9);
}

.card-date {
  font-size: 0.8rem;
  color: white;
  background-color: rgba(0, 0, 0, 0.4);
  padding: 4px 12px;
  border-radius: 50px;
  backdrop-filter: blur(5px);
}

.card-popular {
  font-size: 0.8rem;
  color: white;
  background-color: rgba(249, 115, 22, 0.8);
  padding: 4px 12px;
  border-radius: 50px;
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  gap: 4px;
}

.card-popular svg {
  width: 16px;
  height: 16px;
}

.card-content {
  width: 100%;
  text-align: center;
  /* background-color: #059669; */
  padding: 0 30px 50px;
  position: absolute;
  bottom: 0;
  left: 0;
  transform: translateY(0);
  transition: all 0.3s cubic-bezier(0.1, 0.72, 0.4, 0.97);
  transition-delay: 0.15s;
  will-change: bottom, background-color, transform, padding;
  z-index: 10;
  border-radius: 0 0 12px 12px;
}

.card-hover:hover .card-content {
  background-color: #ecfdf5;
  bottom: 100%;
  transform: translateY(100%);
  padding: 40px 30px;
}

.card-content::before,
.card-content::after {
  content: "";
  width: 100%;
  height: 120px;
  background-color: inherit;
  position: absolute;
  left: 0;
  z-index: -1;
}

.card-content::before {
  top: -80px;
  clip-path: ellipse(60% 80px at bottom center);
}

.card-content::after {
  bottom: -80px;
  clip-path: ellipse(60% 80px at top center);
}

.card-title {
  font-size: 1.5rem;
  margin-bottom: 1rem;
  line-height: 1.3;
  color: #1c1917;
  font-weight: 700;
}

.card-hover:hover .card-title {
  color: #1c1917;
}

.card-text {
  font-size: 0.95rem;
  line-height: 1.6;
  color: #1e293b;
  margin-bottom: 1.5rem;
}

.card-hover:hover .card-text {
  color: #334155;
}

.card-link {
  position: absolute;
  bottom: 1rem;
  left: 50%;
  transform: translate(-50%, 20%);
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  text-decoration: none;
  color: #064e3b;
  font-weight: 600;
  opacity: 0;
  padding: 8px 16px;
  background-color: rgba(255, 255, 255, 0.3);
  border-radius: 50px;
  backdrop-filter: blur(5px);
  transition: all 0.3s cubic-bezier(0.1, 0.72, 0.4, 0.97);
}

.card-hover:hover .card-link {
  opacity: 1;
  transform: translate(-50%, 0);
  transition-delay: 0.3s;
}

.card-link:hover {
  background-color: rgba(255, 255, 255, 0.4);
}

.card-link:hover svg {
  transform: translateX(4px);
}

.card-link svg {
  width: 20px;
  margin-left: 8px;
  transition: transform 0.3s;
}

.card-extra {
  height: 50%;
  position: absolute;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  width: 100%;
  font-size: 1.5rem;
  text-align: center;
  /* background-color: #14c08a; */
  padding: 30px;
  bottom: 0;
  z-index: 0;
  color: #ecfdf5;
  transform: translateY(100%);
  will-change: transform;
  transition: transform 0.3s cubic-bezier(0.1, 0.72, 0.4, 0.97);
  border-radius: 0 0 12px 12px;
}

.card-hover:has(.card-link:hover) .card-extra {
  transform: translateY(0);
}

.extra-title {
  font-size: 1.2rem;
  margin-bottom: 1rem;
  color: #ecfdf5;
}

.extra-delimiter {
  color: #a7f3d0;
}

.extra-category {
  font-weight: 600;
}

.card-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: center;
  z-index: -20;
  transform: scale(1.1);
  transition: transform 0.3s cubic-bezier(0.1, 0.72, 0.4, 0.97);
  transition-delay: 0.075s;
}

.card-hover:hover .card-image {
  transform: scale(1);
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
  border: 2px solid #a7f3d0;
  margin-bottom: 0.5rem;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.user-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: #ecfdf5;
}

.user-username {
  font-size: 0.85rem;
  color: #a7f3d0;
}

/* Dark mode styles */
@media (prefers-color-scheme: dark) {
  .card-hover {
    border-color: #3239445d;
  }
  
  /* .card-content {
    background-color: #065f46;
  }
  
  .card-hover:hover .card-content {
    background-color: #022c22;
  } */
  
  .card-title {
    color: #f3f4f6;
  }
  
  .card-text {
    color: #d1d5db;
  }
  
  .card-link {
    color: #6ee7b7;
  }
  
  /* .card-extra {
    background-color: #065f46;
  }
   */
  .user-avatar {
    border-color: #065f46;
  }
}
</style>