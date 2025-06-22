<template>
        <div class="relative  h-auto perspective-1000 p-2">
              <p class="z-40 p-5  text-5xl font-extrabold text-purple-800 font-cursive drop-shadow-sm">{{recipe_message}}</p>

        <div class="relative  h-auto perspective-1000 ">
            <img :src="image_design" alt="Mobile frame"
                class="pointer-events-none select-none w-full h-full object-cover drop-shadow-2xl z-100" />
            <div
                class="absolute bg-amber-800/10 backdrop-blur-sm left-[15%] top-[5.5%] w-[70%] h-[52%]  overflow-hidden border border-amber-800/20">
                <div ref="recipeCard"
                    class="flex flex-row gap-4 p-4 overflow-x-auto w-full h-full custom-scrollbar snap-x snap-mandatory">
                    <div v-for="(dish, index) in dishes" :key="dish.name + index"
                        class="w-[160px] min-w-[160px] h-full overflow-hidden snap-center transition-all duration-300 hover:scale-105">
                        <div class="relative w-full h-full group">
                            <!-- Dish Image with Overlay -->
                            <div class="relative w-full h-[75%] overflow-hidden rounded-xl shadow-md">
                                <img :src="dish.image || 'https://source.unsplash.com/random/300x300/?food,' + dish.name.split(' ')[0]"
                                    :alt="dish.name"
                                    class="w-full h-full object-cover transition-transform duration-500 group-hover:scale-110">
                                <!-- Popular Badge -->
                                <div v-if="dish.popular"
                                    class="absolute top-2 left-2 bg-amber-500 text-white text-xs px-2 py-1 rounded-full flex items-center">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-3 w-3 mr-1" viewBox="0 0 20 20"
                                        fill="currentColor">
                                        <path fill-rule="evenodd"
                                            d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z"
                                            clip-rule="evenodd" />
                                    </svg>
                                    Popular
                                </div>
                                <!-- Time Badge -->
                                <div
                                    class="absolute bottom-2 right-2 bg-black/60 text-white text-xs px-2 py-1 rounded-full">
                                    {{ dish.time || '15 min' }}
                                </div>
                            </div>

                            <!-- Dish Info -->
                            <div class="mt-2 px-1">
                                <h3 class="font-medium text-gray-800 truncate">{{ dish.name }}</h3>
                                <div class="flex items-center justify-between mt-1">
                                    <div class="flex items-center">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 text-amber-500"
                                            viewBox="0 0 20 20" fill="currentColor">
                                            <path
                                                d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                        </svg>
                                        <span class="text-xs text-gray-600 ml-1">{{ dish.rating || '4.5' }}</span>
                                    </div>
                                    <button class="text-amber-600 hover:text-amber-800">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                                            viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M12 4v16m8-8H4" />
                                        </svg>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Navigation Arrows -->
                <button @click="scrollByOneCard('left')"
                    class="absolute left-2 top-1/2 -translate-y-1/2 bg-white/80 rounded-full p-2 shadow-md hover:bg-white z-10">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-amber-800" fill="none"
                        viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                    </svg>
                </button>
                <button @click="scrollByOneCard('right')"
                    class="absolute right-2 top-1/2 -translate-y-1/2 bg-white/80 rounded-full p-2 shadow-md hover:bg-white z-10">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-amber-800" fill="none"
                        viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                    </svg>
                </button>
            </div>

        </div>
    </div>


</template>
<script setup>
import image_design from '../assets/laptop.png';
import { ref, onMounted, nextTick } from 'vue';
const recipe_message = ref('Access 1000+ recipes,250+ East African dishes')
const dishes = ref([
    {
        name: "Ugali",
        popular: true,
        time: "45 min",
        rating: "4.9",
        image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/508163279_3795774807233255_4365000591668445711_n.jpg?stp=dst-jpg_s600x600_tt6&_nc_cat=1&ccb=1-7&_nc_sid=833d8c&_nc_eui2=AeF8L3LvLRs0jQ6_vj42dwC1E4533h20NtQTjnfeHbQ21NNATtmn3daSHG-WhGvrmU87cGyPvu6C447I3ZD4U3Xg&_nc_ohc=273NdazOcBMQ7kNvwEQOBZN&_nc_oc=Adl_vUlUXoLTATKYQznw-eHBTGbvpIwciKcFoMETB5azLn8a5KLqeLs6e7kfCyc7TZ8&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=q1dChMqRyjkKnkqpedZ6rA&oh=00_AfPppe0PQUlLTWcrCmB0Vq8bIdez9riYPIrKVRiFKcOr2A&oe=68560563", description: "Traditional Kenyan cornmeal dish served with sukuma wiki"
    },
    {
        name: "Nyama Choma", popular: true,
        time: "45 min",
        rating: "4.9", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/506791634_3795772030566866_3829375738567937542_n.jpg?stp=c69.0.1143.1143a_dst-jpg_s206x206_tt6&_nc_cat=1&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeH-BewlfnEoE-ugeZ8zZBBLacoYkerSrsdpyhiR6tKux3qzqCQS1biyqYn1KHqh8spsN_rnVjQKh5V0KISMmeK1&_nc_ohc=DpaRuZZPvdYQ7kNvwHFBohn&_nc_oc=AdlqFSHqgeNRIPBuE8LNFWTpYXjzmTN0n5TFfmNq-ECKZgwLnH-O0fLRa9FjB8TBm-M&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=McCAslocLA7mi3jCmXmuqg&oh=00_AfNXqjMrdZkiVWsikX9-FOiaVGUmEQ6PdWMM4qSO0cwbkA&oe=68560BC7", description: "Grilled meat, usually goat or beef, with kachumbari"
    },
    {
        name: "Sukuma Wiki", popular: true,
        time: "45 min",
        rating: "4.9", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/495753410_3749110831899653_8142894592600150040_n.jpg?stp=c126.0.1796.1796a_dst-jpg_s206x206_tt6&_nc_cat=111&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeGjA7RW4abMqlbZp1aQrFUIkFFipKdPS9SQUWKkp09L1Pr60wvAzK73Xk3KvdLBgt0DeUOG3E9FgMRaaA8dNzD4&_nc_ohc=Ye_2dXqUM-cQ7kNvwEiXFIw&_nc_oc=AdnHtgl-DdRvqMmBwBdRPXEMQA5T2r9QvFFT7qwdjcdE79TkQQOI5UlH8UBUEWIRQqQ&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=ffm5uewgKENyubsmcU4nuw&oh=00_AfNP_X77EZPNdG2Ax8_yLQ_AYXnLyNQ_MZ5Uf66DfYll_w&oe=68562786", description: "Healthy collard greens sautéed with onions and tomatoes"
    },
    {
        name: "Chapati", popular: true,
        time: "45 min",
        rating: "4.9", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/499713346_3755711811239555_6987134326908912586_n.jpg?stp=c60.0.600.600a_dst-jpg_s206x206_tt6&_nc_cat=110&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeFUE8zMb_2LXPBlQfNJ9llcWjH2O35z6lpaMfY7fnPqWvW17VpiY4b4aOKwlH4yav16-edR7Vd6fg7dKzGoW5Pc&_nc_ohc=X2jLJ0XJ75QQ7kNvwFGKN4V&_nc_oc=Adn57aqjMKOs12HPg2P0NTsaRum0PK9Mt_H1Jfwkyf9FkZ7Uz7lsSQiqUaTWtCC38AY&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=pAsEaJY8QFFm8H5R-kXf2A&oh=00_AfNaNIeQ1egmgfSW5XNHwIP_P3_18l-EgMh8VwcGxZMBJg&oe=685634F7", description: "Flaky flatbread perfect with stews and curries"
    },
    {
        name: "Pilau", popular: true,
        time: "45 min",
        rating: "4.9", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/501301960_3767978516679551_2743587262151830436_n.jpg?stp=c137.0.446.446a_dst-jpg_s206x206_tt6&_nc_cat=106&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeEYE5Cl2-qMWmB7jwCmeqAp5Q2E8EVd9y_lDYTwRV33L6kBj0ORnKCdqhOXCDuo7Bf8dPQlvDwQSSle8TEg9R5p&_nc_ohc=df3n5dd4Re4Q7kNvwGBl-ec&_nc_oc=AdnzRAlCLCKz-t22CUl0gbuO_yLXtR6rj1NQ7QzY-66-Bi71G5WET3MapjQh6LZJw-8&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=OuHlrzWecSn_qsXX5bXedA&oh=00_AfMhVl3wWKiJInD4MesZqCeI1u4HBBkfWUhBcBKi4nvN6Q&oe=68561709", description: "Fragrant rice dish cooked with spices and meat"
    },
    {
        name: "Mandazi", popular: true,
        time: "45 min",
        rating: "4.9", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/505576389_3784897544987648_471162606617541962_n.jpg?stp=c47.0.627.627a_dst-jpg_s206x206_tt6&_nc_cat=100&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeEmSagr8s8RJNwucDlTZSo0PHY79GiQBBQ8djv0aJAEFLTO5QYAddoB4UKqAXKchDVJV7Dn1jhtSVzodHMXVdV9&_nc_ohc=wg9McYqmQMUQ7kNvwFPFr6X&_nc_oc=AdkhxaHcE5LscwIkTsChIEnR_w-ZLftXd8XMrPa1Dipz67FgISOS_8xteJJ6ic9gp7g&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=UXByZ-3zkUZd_H9MZmLzyg&oh=00_AfO_DIzp30omtsWAJ6fvxd0uh26ofPzmKg5QEPESIuLkZg&oe=68562BDD", description: "Sweet East African doughnuts for breakfast or snacks"
    },
    {
        name: "Githeri", popular: true,
        time: "45 min",
        rating: "4.9", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/499577307_3756959647781438_8534541446090865718_n.jpg?stp=c87.0.547.547a_dst-jpg_s206x206_tt6&_nc_cat=109&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeHNzkWbcAWpjmXsrincMu239bNNJOjUHQD1s00k6NQdACTC7YK1Ubs6qXVgdYBvbxlD1Chfu0s16PjyNQaSd_eN&_nc_ohc=AVKNGtF12zgQ7kNvwGmiBsC&_nc_oc=AdnULGGoSbKPEHoHRA2-XKhyttijDOhBkshf6ue33PXOgnlZVHaCgYQMXaDNOP_xP7c&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=c-2IQSItRnELkUpAJwyFvA&oh=00_AfMvPe_pYrH_XxUd7vAGPe0wqvhVyAhy9xpmCCZ6GfL6Wg&oe=68563632", description: "Hearty mix of beans and corn, a Kenyan staple"
    },
    {
        name: "Mukimo", popular: true,
        time: "45 min",
        rating: "4.9", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/503470376_3776273255850077_4856351217690965912_n.jpg?stp=c55.0.610.610a_dst-jpg_s206x206_tt6&_nc_cat=107&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeHUl2_VQond90w5zWC9fVX7-SvQt4A2jkz5K9C3gDaOTC82fV8PDTVpaKBwWJiCEG7dHe8QQfXfFsVPkmgbx37j&_nc_ohc=eYbHq62s-t4Q7kNvwETmfSA&_nc_oc=AdnWhqluRPnEgjxaWNJRmjamuQ0bR5GK5ahJaKRaNgiKNATzL5M1YWIsihpYRE1UI7Q&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=w2eQkfDvdZHIf3erL2CWkw&oh=00_AfMBMxJlJqMn0lWFsJCRwvtYIaJ6kc2RymStw06ZIFKTHw&oe=68561151", description: "Mashed potatoes with greens and corn"
    },
    {
        name: "Fish Curry", popular: true,
        time: "45 min",
        rating: "4.9", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/506791736_3790246521119417_1294429913833372673_n.jpg?stp=c219.0.1610.1610a_dst-jpg_s206x206_tt6&_nc_cat=109&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeFDFtm-hnh2CH-OkTqKsC7FV2cGyfUqJk1XZwbJ9SomTe3pmOalsNHyEaG5-Y9IY5QCwBOWBeqYELo-h377eo9c&_nc_ohc=D0dsMBEsD-MQ7kNvwHNSkkc&_nc_oc=AdlgcIvJLavpukk13z8_qNIDDpYr6-hwvqdezU-6SLkPDQI7kNMvezfjGy86cAOnGTk&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=HS3FarPdQxq3hPvn1sc4pw&oh=00_AfPmTcPz36489SilkZvqGlPyQuzjowxGS9CFg_aTiWCMdg&oe=68562750", description: "Coastal favorite with coconut milk and spices"
    },
    {
        name: "Samosa", popular: true,
        time: "45 min",
        rating: "4.9", image: "https://scontent.fnuu1-1.fna.fbcdn.net/v/t39.30808-6/502583193_3773136239497112_367231739265218194_n.jpg?stp=c90.0.540.540a_dst-jpg_s206x206_tt6&_nc_cat=100&ccb=1-7&_nc_sid=50ad20&_nc_eui2=AeHV04oCZQpGfIASFK8w9NujtqzCNecgW4a2rMI15yBbhnJ4ueaNhZqim5t_BCTViXf5wOCUrEWvwaVgI9k03RmT&_nc_ohc=jQluisixWhgQ7kNvwFe7Mwk&_nc_oc=AdkjFJ6x-7Qu36gLbADa3jCOsNDhNChEkP2hxX-yokKdIcAcJgQob5DUgph8HwVyEpA&_nc_zt=23&_nc_ht=scontent.fnuu1-1.fna&_nc_gid=j1L2E9LiEngphU697n7d7Q&oh=00_AfP0chI6FJT2R0qZoiC6lyem48co1XxKHy1AnKaOI7O59g&oe=6856087D", description: "Crispy pastry filled with spiced meat or vegetables"
    }
]);

const recipeCard = ref(null);

const scrollByOneCard = (direction = 'right') => {
    const offset = 200; // adjust based on card width
    if (recipeCard.value) {
        recipeCard.value.scrollBy({
            left: direction === 'right' ? offset : -offset,
            behavior: 'smooth'
        });
    }
};


let direction = 'right';
onMounted(() => {
    nextTick(() => {
        setInterval(() => {
            scrollByOneCard(direction);

            if (recipeCard.value) {
                const { scrollLeft, scrollWidth, clientWidth } = recipeCard.value;

                if (scrollLeft + clientWidth >= scrollWidth) {
                    direction = 'left';
                } else if (scrollLeft <= 0) {
                    direction = 'right';
                }
            }
        }, 2000); // slower for a better UX
    });
});

</script>

<style scoped>

.font-cursive {
  font-family: 'Pacifico', cursive;
}
</style>