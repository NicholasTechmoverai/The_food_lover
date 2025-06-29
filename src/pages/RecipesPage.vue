

 <template>
      <router-view class="fixed pt-15 w-full h-[80%] md:h-full z-60" />

  <div class="p-6 z-50">
    <h1 class="text-2xl font-bold mb-6 text-gray-800 dark:text-gray-100">Browse Recipes</h1>

    <div class="grid gap-6 grid-cols-1 sm:grid-cols-1 md:grid-cols-3 xl:grid-cols-4">
      <RecipeCard
        v-for="recipe in recipes"
        :key="recipe.id"
        :recipe="recipe"
      />
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import RecipeCard from '../cards/RecipeCard.vue'

const recipes = ref([
  {
    id: 1,
    recipeName: 'Ugali with Sukuma Wiki',
    repiceColor: '#4CAF50',
    image: 'https://images.unsplash.com/photo-1635070041078-e363dbe005cb',
    tags: ['staple', 'vegetarian', 'quick'],
    cookTime: { hr: 0, min: 30 },
    description: `<p><b>Ugali</b> is Kenya's national dish - a stiff maize flour porridge served with <u>Sukuma Wiki</u> (collard greens). This hearty combination is eaten daily by millions.</p><p>The greens are sautéed with onions, tomatoes, and sometimes ground peanuts for extra nutrition.</p>`,
    cuisine: { name: 'Kenyan', region: 'East Africa' },
    complexityLevel: { name: 'Easy', value: 1 },
    category: ['Main Dish', 'Vegetarian'],
    user: {
      name: 'Mama Atieno',
      profilePic: 'https://randomuser.me/api/portraits/women/44.jpg',
      id: 'user_001',
      totalRecipes: 27,
      isVerified: true
    }
  },
  {
    id: 2,
    recipeName: 'Nyama Choma',
    repiceColor: '#8B0000',
    image: 'https://images.unsplash.com/photo-1555939594-58d7cb561ad1',
    tags: ['grilled', 'meat', 'festive'],
    cookTime: { hr: 2, min: 30 },
    description: `<p>Kenya's famous <b>charcoal-grilled meat</b>, typically goat or beef. The meat is first boiled with spices then finished over charcoal for maximum flavor.</p><p>Served with <i>kachumbari</i> (tomato-onion salad) and cold Tusker beer for the full Kenyan experience.</p>`,
    cuisine: { name: 'Kenyan', region: 'East Africa' },
    complexityLevel: { name: 'Medium', value: 2 },
    category: ['Main Dish', 'Meat'],
    user: {
      name: 'Chef Mwangi',
      profilePic: 'https://randomuser.me/api/portraits/men/32.jpg',
      id: 'user_002',
      totalRecipes: 42,
      isVerified: true
    }
  },
  {
    id: 3,
    recipeName: 'Mandazi',
    repiceColor: '#FFD700',
    image: 'https://images.unsplash.com/photo-1563805042-7684c019e1cb',
    tags: ['sweet', 'breakfast', 'snack'],
    cookTime: { hr: 0, min: 45 },
    description: `<p>East African <u>cardamom-spiced donuts</u> that are less sweet than Western versions. Perfect with morning chai or afternoon coffee.</p><p>Coastal versions use coconut milk for extra richness. Often shaped into triangles or circles.</p>`,
    cuisine: { name: 'Swahili', region: 'Coastal East Africa' },
    complexityLevel: { name: 'Easy', value: 1 },
    category: ['Dessert', 'Breakfast'],
    user: {
      name: 'Amina Swaleh',
      profilePic: 'https://randomuser.me/api/portraits/women/63.jpg',
      id: 'user_003',
      totalRecipes: 18,
      isVerified: false
    }
  },
  {
    id: 4,
    recipeName: 'Pilau',
    repiceColor: '#A0522D',
    image: 'https://images.unsplash.com/photo-1630012312541-839a1f3a6d13',
    tags: ['spiced', 'rice', 'festive'],
    cookTime: { hr: 1, min: 15 },
    description: `<p>Fragrant <b>spiced rice dish</b> showing Arab and Indian influences. The rice gets its golden color from caramelized onions and turmeric.</p><p>Traditionally served at weddings and special occasions with meat stew and kachumbari salad.</p>`,
    cuisine: { name: 'Swahili', region: 'Coastal East Africa' },
    complexityLevel: { name: 'Medium', value: 2 },
    category: ['Main Dish', 'Rice'],
    user: {
      name: 'Ali Hassan',
      profilePic: 'https://randomuser.me/api/portraits/men/22.jpg',
      id: 'user_004',
      totalRecipes: 35,
      isVerified: true
    }
  },
  {
    id: 5,
    recipeName: 'Chapati',
    repiceColor: '#F4A460',
    image: 'https://images.unsplash.com/photo-1633944094699-6a2c6fc37c68',
    tags: ['bread', 'staple', 'vegetarian'],
    cookTime: { hr: 0, min: 45 },
    description: `<p>Flaky <u>Kenyan-style flatbread</u> introduced by Indian immigrants but now thoroughly localized. Made with wheat flour, oil, and water.</p><p>Essential accompaniment to stews and curries. Street vendors sell them folded in newspaper.</p>`,
    cuisine: { name: 'Kenyan', region: 'Nationwide' },
    complexityLevel: { name: 'Medium', value: 2 },
    category: ['Side Dish', 'Bread'],
    user: {
      name: 'Priya Patel',
      profilePic: 'https://randomuser.me/api/portraits/women/33.jpg',
      id: 'user_005',
      totalRecipes: 29,
      isVerified: false
    }
  },
  {
    id: 6,
    recipeName: 'Githeri',
    repiceColor: '#CD853F',
    image: 'https://images.unsplash.com/photo-1547592180-85f173990554',
    tags: ['vegetarian', 'hearty', 'traditional'],
    cookTime: { hr: 1, min: 30 },
    description: `<p>Nutritious <b>bean and corn stew</b> originating from the Kikuyu people. Provides complete protein from the legume-grain combination.</p><p>Modern versions add potatoes, carrots, and sometimes meat. A staple in school feeding programs.</p>`,
    cuisine: { name: 'Kenyan', region: 'Central Highlands' },
    complexityLevel: { name: 'Easy', value: 1 },
    category: ['Main Dish', 'Vegetarian'],
    user: {
      name: 'Wanjiku Kariuki',
      profilePic: 'https://randomuser.me/api/portraits/women/71.jpg',
      id: 'user_006',
      totalRecipes: 15,
      isVerified: false
    }
  },
  {
    id: 7,
    recipeName: 'Mukimo',
    repiceColor: '#556B2F',
    image: 'https://images.pexels.com/photos/12737656/pexels-photo-12737656.jpeg',
    tags: ['mashed', 'vegetarian', 'traditional'],
    cookTime: { hr: 0, min: 50 },
    description: `<p>Kikuyu <u>mashed potato dish</u> with greens, corn and sometimes beans. The name comes from the Kikuyu word "kiuma" meaning to mash.</p><p>Traditionally served during important ceremonies and gatherings. Excellent with meat stews.</p>`,
    cuisine: { name: 'Kenyan', region: 'Central Kenya' },
    complexityLevel: { name: 'Easy', value: 1 },
    category: ['Side Dish', 'Vegetarian'],
    user: {
      name: 'Kamau Githinji',
      profilePic: 'https://randomuser.me/api/portraits/men/45.jpg',
      id: 'user_007',
      totalRecipes: 23,
      isVerified: true
    }
  },
  {
    id: 8,
    recipeName: 'Samaki wa Kupaka',
    repiceColor: '#1E90FF',
    image: 'https://images.pexels.com/photos/8503594/pexels-photo-8503594.jpeg',
    tags: ['seafood', 'coconut', 'coastal'],
    cookTime: { hr: 0, min: 40 },
    description: `<p>Swahili <b>coconut fish curry</b> featuring reef fish like snapper or parrotfish. The sauce is rich with coconut milk, turmeric, and cilantro.</p><p>Best enjoyed with steamed rice or chapati. A Mombasa specialty that showcases coastal flavors.</p>`,
    cuisine: { name: 'Swahili', region: 'Coast' },
    complexityLevel: { name: 'Medium', value: 2 },
    category: ['Main Dish', 'Seafood'],
    user: {
      name: 'Fatima Abdullah',
      profilePic: 'https://randomuser.me/api/portraits/women/68.jpg',
      id: 'user_008',
      totalRecipes: 31,
      isVerified: true
    }
  },
  {
    id: 9,
    recipeName: 'Viazi Karai',
    repiceColor: '#DAA520',
    image: 'https://images.unsplash.com/photo-1656618020911-1c7a937175fd',
    tags: ['streetfood', 'snack', 'vegetarian'],
    cookTime: { hr: 0, min: 25 },
    description: `<p>Crispy <u>deep-fried potato cubes</u> coated in chickpea flour batter. A popular street food snack across Kenya.</p><p>Often served with chili sauce or tamarind chutney. The perfect quick bite with afternoon tea.</p>`,
    cuisine: { name: 'Kenyan', region: 'Nationwide' },
    complexityLevel: { name: 'Easy', value: 1 },
    category: ['Snack', 'Vegetarian'],
    user: {
      name: 'Juma Omari',
      profilePic: 'https://randomuser.me/api/portraits/men/29.jpg',
      id: 'user_009',
      totalRecipes: 12,
      isVerified: false
    }
  },
  {
    id: 10,
    recipeName: 'Irio',
    repiceColor: '#2E8B57',
    image: 'https://images.pexels.com/photos/5394516/pexels-photo-5394516.jpeg',
    tags: ['mashed', 'traditional', 'vegetarian'],
    cookTime: { hr: 0, min: 45 },
    description: `<p>Kikuyu <b>mashed peas and potatoes</b>, sometimes with corn added. Simpler than mukimo but equally comforting.</p><p>Traditionally served in a wooden bowl. The green peas give it vibrant color and fresh flavor.</p>`,
    cuisine: { name: 'Kenyan', region: 'Central Kenya' },
    complexityLevel: { name: 'Easy', value: 1 },
    category: ['Side Dish', 'Vegetarian'],
    user: {
      name: 'Nyambura Wairimu',
      profilePic: 'https://randomuser.me/api/portraits/women/52.jpg',
      id: 'user_010',
      totalRecipes: 19,
      isVerified: false
    }
  },
  {
    id: 11,
    recipeName: 'Kuku Paka',
    repiceColor: '#FF8C00',
    image: 'https://images.unsplash.com/photo-1604329760661-e71dc83f8f26',
    tags: ['chicken', 'coconut', 'coastal'],
    cookTime: { hr: 1, min: 15 },
    description: `<p>Creamy <u>Swahili chicken curry</u> where the meat is first grilled then simmered in coconut sauce. Features warming spices like cardamom and cinnamon.</p><p>Paka means "to smear" in Swahili, referring to how the sauce coats the chicken. Best with fresh chapati.</p>`,
    cuisine: { name: 'Swahili', region: 'Coast' },
    complexityLevel: { name: 'Medium', value: 2 },
    category: ['Main Dish', 'Poultry'],
    user: {
      name: 'Salim Juma',
      profilePic: 'https://randomuser.me/api/portraits/men/36.jpg',
      id: 'user_011',
      totalRecipes: 26,
      isVerified: true
    }
  },
  {
    id: 12,
    recipeName: 'Mahamri',
    repiceColor: '#FFDEAD',
    image: 'https://images.pexels.com/photos/410648/pexels-photo-410648.jpeg',
    tags: ['sweet', 'breakfast', 'coconut'],
    cookTime: { hr: 0, min: 35 },
    description: `<p>Swahili <b>coconut doughnuts</b> that are slightly sweet and wonderfully aromatic. The dough rises overnight for perfect texture.</p><p>Traditionally shaped into triangles and served in sets of three - said to represent the Holy Trinity in coastal Christian communities.</p>`,
    cuisine: { name: 'Swahili', region: 'Coast' },
    complexityLevel: { name: 'Medium', value: 2 },
    category: ['Dessert', 'Breakfast'],
    user: {
      name: 'Zahara Mohamed',
      profilePic: 'https://randomuser.me/api/portraits/women/47.jpg',
      id: 'user_012',
      totalRecipes: 21,
      isVerified: false
    }
  }
]);
</script>
