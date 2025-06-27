<template>
    <div class="relative w-[400px] h-auto max-h-[750px] perspective-1000">
        <!-- Mobile Frame with Shadow -->
        <img :src="mobile_image" alt="Mobile frame"
            class="the-image select-none pointer-events-none w-full h-full object-cover drop-shadow-2xl z-100" />

        <!-- App Content (Simulated Screen) -->
        <div class="content-wrapper absolute w-[76%] h-[92%] top-[1%] left-[15%] z-0">
            <div class="content-body bg-white/20 backdrop-blur-md w-full h-full flex flex-col">
                <!-- App Header -->
                <div class="px-2 pt-5 pb-2">
                    <h1 class="text-xl font-bold text-gray-800 tracking-wide">RECIPES</h1>
                    <div class="flex items-center mt-3">
                        <input type="text" placeholder="Search recipes..."
                            class="flex-1 bg-white/60 placeholder:text-gray-600 text-sm rounded-full py-2 px-4 focus:outline-none focus:ring-2 focus:ring-purple-500" />
                        <button class="ml-2 p-2 text-purple-600 hover:text-purple-800 transition">
                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24"
                                stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                            </svg>
                        </button>
                    </div>
                </div>

                <!-- Recipe List -->
                <div ref="recipeCard"
                    class="flex-1 overflow-y-auto px-2 pb-6 space-y-3 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-transparent">
                    <div v-for="(recipe, index) in recipes" :key="index"
                        class="w-full h-24 rounded-xl bg-gray-100/80 shadow overflow-hidden hover:shadow-md hover:-translate-y-1 transition-all flex">
                        <div class="w-24 h-full flex-shrink-0 overflow-hidden">
                            <img :src="recipe.image || `https://via.placeholder.com/100?text=${recipe.name}`"
                                :alt="recipe.name" class="w-full h-full object-cover" />
                        </div>
                        <div class="p-3 flex-1">
                            <h3 class="font-semibold text-gray-800 text-sm">{{ recipe.name }}</h3>
                            <p class="text-xs text-gray-600 mt-1 line-clamp-2">
                                {{ recipe.description || 'Delicious traditional recipe with simple ingredients' }}
                            </p>

                        </div>
                    </div>
                </div>

                <!-- Bottom Navigation (Optional Placeholder) -->
                <div class="bg-white/30 border-t border-gray-200 p-2 flex justify-around">
                    <!-- Add icons/navigation if needed -->
                </div>
            </div>
        </div>
        <div :style="{ backgroundColor: siteConfig.colors.primary }" class="rotate-y-20 -rotate-x-5 absolute left-[15%] -bottom-10 rounded-2xl shadow-2xl w-[90%] h-[100px]">
            <img  class="w-full h-full object-contain" :src="imageLogo" alt="" srcset="">
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import mobile_image from '../assets/61d980464826740004290527.png';
import { useSiteStore } from '../config/siteConfig.js'

const { siteConfig, getResponsiveValue } = useSiteStore()
const imageLogo = siteConfig.assets.logo
const recipeCard = ref(null);

const recipes = ref([
    { name: "Ugali", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/508163279_3795774807233255_4365000591668445711_n.jpg?stp=dst-jpg_s600x600_tt6&_nc_cat=1&ccb=1-7&_nc_sid=833d8c&_nc_eui2=AeF8L3LvLRs0jQ6_vj42dwC1E4533h20NtQTjnfeHbQ21NNATtmn3daSHG-WhGvrmU87cGyPvu6C447I3ZD4U3Xg&_nc_ohc=273NdazOcBMQ7kNvwEQOBZN&_nc_oc=Adl_vUlUXoLTATKYQznw-eHBTGbvpIwciKcFoMETB5azLn8a5KLqeLs6e7kfCyc7TZ8&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=q1dChMqRyjkKnkqpedZ6rA&oh=00_AfPppe0PQUlLTWcrCmB0Vq8bIdez9riYPIrKVRiFKcOr2A&oe=68560563", description: "Traditional Kenyan cornmeal dish served with sukuma wiki" },
    { name: "Nyama Choma", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/506791634_3795772030566866_3829375738567937542_n.jpg?stp=c69.0.1143.1143a_dst-jpg_s206x206_tt6&_nc_cat=1&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeH-BewlfnEoE-ugeZ8zZBBLacoYkerSrsdpyhiR6tKux3qzqCQS1biyqYn1KHqh8spsN_rnVjQKh5V0KISMmeK1&_nc_ohc=DpaRuZZPvdYQ7kNvwHFBohn&_nc_oc=AdlqFSHqgeNRIPBuE8LNFWTpYXjzmTN0n5TFfmNq-ECKZgwLnH-O0fLRa9FjB8TBm-M&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=McCAslocLA7mi3jCmXmuqg&oh=00_AfNXqjMrdZkiVWsikX9-FOiaVGUmEQ6PdWMM4qSO0cwbkA&oe=68560BC7", description: "Grilled meat, usually goat or beef, with kachumbari" },
    { name: "Sukuma Wiki", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/495753410_3749110831899653_8142894592600150040_n.jpg?stp=c126.0.1796.1796a_dst-jpg_s206x206_tt6&_nc_cat=111&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeGjA7RW4abMqlbZp1aQrFUIkFFipKdPS9SQUWKkp09L1Pr60wvAzK73Xk3KvdLBgt0DeUOG3E9FgMRaaA8dNzD4&_nc_ohc=Ye_2dXqUM-cQ7kNvwEiXFIw&_nc_oc=AdnHtgl-DdRvqMmBwBdRPXEMQA5T2r9QvFFT7qwdjcdE79TkQQOI5UlH8UBUEWIRQqQ&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=ffm5uewgKENyubsmcU4nuw&oh=00_AfNP_X77EZPNdG2Ax8_yLQ_AYXnLyNQ_MZ5Uf66DfYll_w&oe=68562786", description: "Healthy collard greens sautéed with onions and tomatoes" },
    { name: "Chapati", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/499713346_3755711811239555_6987134326908912586_n.jpg?stp=c60.0.600.600a_dst-jpg_s206x206_tt6&_nc_cat=110&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeFUE8zMb_2LXPBlQfNJ9llcWjH2O35z6lpaMfY7fnPqWvW17VpiY4b4aOKwlH4yav16-edR7Vd6fg7dKzGoW5Pc&_nc_ohc=X2jLJ0XJ75QQ7kNvwFGKN4V&_nc_oc=Adn57aqjMKOs12HPg2P0NTsaRum0PK9Mt_H1Jfwkyf9FkZ7Uz7lsSQiqUaTWtCC38AY&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=pAsEaJY8QFFm8H5R-kXf2A&oh=00_AfNaNIeQ1egmgfSW5XNHwIP_P3_18l-EgMh8VwcGxZMBJg&oe=685634F7", description: "Flaky flatbread perfect with stews and curries" },
    { name: "Pilau", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/501301960_3767978516679551_2743587262151830436_n.jpg?stp=c137.0.446.446a_dst-jpg_s206x206_tt6&_nc_cat=106&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeEYE5Cl2-qMWmB7jwCmeqAp5Q2E8EVd9y_lDYTwRV33L6kBj0ORnKCdqhOXCDuo7Bf8dPQlvDwQSSle8TEg9R5p&_nc_ohc=df3n5dd4Re4Q7kNvwGBl-ec&_nc_oc=AdnzRAlCLCKz-t22CUl0gbuO_yLXtR6rj1NQ7QzY-66-Bi71G5WET3MapjQh6LZJw-8&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=OuHlrzWecSn_qsXX5bXedA&oh=00_AfMhVl3wWKiJInD4MesZqCeI1u4HBBkfWUhBcBKi4nvN6Q&oe=68561709", description: "Fragrant rice dish cooked with spices and meat" },
    { name: "Mandazi", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/505576389_3784897544987648_471162606617541962_n.jpg?stp=c47.0.627.627a_dst-jpg_s206x206_tt6&_nc_cat=100&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeEmSagr8s8RJNwucDlTZSo0PHY79GiQBBQ8djv0aJAEFLTO5QYAddoB4UKqAXKchDVJV7Dn1jhtSVzodHMXVdV9&_nc_ohc=wg9McYqmQMUQ7kNvwFPFr6X&_nc_oc=AdkhxaHcE5LscwIkTsChIEnR_w-ZLftXd8XMrPa1Dipz67FgISOS_8xteJJ6ic9gp7g&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=UXByZ-3zkUZd_H9MZmLzyg&oh=00_AfO_DIzp30omtsWAJ6fvxd0uh26ofPzmKg5QEPESIuLkZg&oe=68562BDD", description: "Sweet East African doughnuts for breakfast or snacks" },
    { name: "Githeri", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/499577307_3756959647781438_8534541446090865718_n.jpg?stp=c87.0.547.547a_dst-jpg_s206x206_tt6&_nc_cat=109&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeHNzkWbcAWpjmXsrincMu239bNNJOjUHQD1s00k6NQdACTC7YK1Ubs6qXVgdYBvbxlD1Chfu0s16PjyNQaSd_eN&_nc_ohc=AVKNGtF12zgQ7kNvwGmiBsC&_nc_oc=AdnULGGoSbKPEHoHRA2-XKhyttijDOhBkshf6ue33PXOgnlZVHaCgYQMXaDNOP_xP7c&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=c-2IQSItRnELkUpAJwyFvA&oh=00_AfMvPe_pYrH_XxUd7vAGPe0wqvhVyAhy9xpmCCZ6GfL6Wg&oe=68563632", description: "Hearty mix of beans and corn, a Kenyan staple" },
    { name: "Mukimo", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/503470376_3776273255850077_4856351217690965912_n.jpg?stp=c55.0.610.610a_dst-jpg_s206x206_tt6&_nc_cat=107&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeHUl2_VQond90w5zWC9fVX7-SvQt4A2jkz5K9C3gDaOTC82fV8PDTVpaKBwWJiCEG7dHe8QQfXfFsVPkmgbx37j&_nc_ohc=eYbHq62s-t4Q7kNvwETmfSA&_nc_oc=AdnWhqluRPnEgjxaWNJRmjamuQ0bR5GK5ahJaKRaNgiKNATzL5M1YWIsihpYRE1UI7Q&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=w2eQkfDvdZHIf3erL2CWkw&oh=00_AfMBMxJlJqMn0lWFsJCRwvtYIaJ6kc2RymStw06ZIFKTHw&oe=68561151", description: "Mashed potatoes with greens and corn" },
    { name: "Fish Curry", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/506791736_3790246521119417_1294429913833372673_n.jpg?stp=c219.0.1610.1610a_dst-jpg_s206x206_tt6&_nc_cat=109&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeFDFtm-hnh2CH-OkTqKsC7FV2cGyfUqJk1XZwbJ9SomTe3pmOalsNHyEaG5-Y9IY5QCwBOWBeqYELo-h377eo9c&_nc_ohc=D0dsMBEsD-MQ7kNvwHNSkkc&_nc_oc=AdlgcIvJLavpukk13z8_qNIDDpYr6-hwvqdezU-6SLkPDQI7kNMvezfjGy86cAOnGTk&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=HS3FarPdQxq3hPvn1sc4pw&oh=00_AfPmTcPz36489SilkZvqGlPyQuzjowxGS9CFg_aTiWCMdg&oe=68562750", description: "Coastal favorite with coconut milk and spices" },
    { name: "Samosa", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/502583193_3773136239497112_367231739265218194_n.jpg?stp=c90.0.540.540a_dst-jpg_s206x206_tt6&_nc_cat=100&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeHV04oCZQpGfIASFK8w9NujtqzCNecgW4a2rMI15yBbhnJ4ueaNhZqim5t_BCTViXf5wOCUrEWvwaVgI9k03RmT&_nc_ohc=jQluisixWhgQ7kNvwFe7Mwk&_nc_oc=AdkjFJ6x-7Qu36gLbADa3jCOsNDhNChEkP2hxX-yokKdIcAcJgQob5DUgph8HwVyEpA&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=j1L2E9LiEngphU697n7d7Q&oh=00_AfP0chI6FJT2R0qZoiC6lyem48co1XxKHy1AnKaOI7O59g&oe=6856087D", description: "Crispy pastry filled with spiced meat or vegetables" }
]);

const scrollByOneCard = (direction = 'down') => {
    const offset = 96 + 16; // card height + margin
    if (recipeCard.value) {
        recipeCard.value.scrollBy({
            top: direction === 'down' ? offset : -offset,
            behavior: 'smooth'
        });
    }
};

let direction = 'down';

onMounted(() => {
  nextTick(() => {
    setInterval(() => {
      scrollByOneCard(direction);

      // Toggle direction if needed (e.g., at bounds)
      if (recipeCard.value) {
        const { scrollTop, scrollHeight, clientHeight } = recipeCard.value;

        if (scrollTop + clientHeight >= scrollHeight) {
          direction = 'up';
        } else if (scrollTop <= 0) {
          direction = 'down';
        }
      }
    }, 1000);
  });
});

</script>

<style scoped>
.the-image {
    z-index: 100 !important;
}

.perspective-1000 {
    perspective: 1000px;
}

.content-wrapper {
    transform: rotateY(25deg) rotateX(15deg);
    transform-style: preserve-3d;
    transition: transform 0.4s ease;
    z-index: -1 !important;
}

.content-body {
    border-radius: 24px;
    overflow: hidden;
    backface-visibility: hidden;
    box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
}

.line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}

.scrollbar-thin::-webkit-scrollbar {
    width: 4px;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
    background-color: rgba(156, 163, 175, 0.5);
    border-radius: 2px;
}

.scrollbar-thin::-webkit-scrollbar-track {
    background-color: transparent;
}
</style>
