<template>
    <div class="z-50 bg-white  shadow-md overflow-hidden ">
        <Splitter style="height: 100%;max-height: 600px;" class="border-0">
            <!-- Panel 1 -->
            <SplitterPanel :size="sidebarSize" :minSize="10"
                class="flex items-center justify-center bg-indigo-100">
                <img :src="sidebarImage" alt="Sidebar Icon" class="w-full h-full object-cover bg-blue-200" />

            </SplitterPanel>

            <!-- Main Panel -->
            <SplitterPanel :size="100 - sidebarSize" class="bg-white">
                <Splitter layout="vertical" class="border-0">
                    <!-- Panel 2 -->
                    <SplitterPanel :size="headerSize"
                        class="flex items-center justify-center bg-teal-100 ">
                        <img :src="headerImage" alt="Header" class="w-full h-full object-cover bg-teal-200" />

                    </SplitterPanel>

                    <!-- Panel 3 & 4 -->
                    <SplitterPanel :size="100 - headerSize" class="bg-white">
                        <Splitter class="border-0">
                            <!-- Panel 3 -->
                            <SplitterPanel :size="menuSize"
                                class="flex items-center justify-center bg-orange-100 ">
                                <img :src="menuImage" alt="Menu" class="w-full h-full object-cover bg-orange-200" />
                            </SplitterPanel>

                            <!-- Panel 4 -->
                            <SplitterPanel :size="100 - menuSize"
                                class="flex items-center justify-center bg-violet-100">
                                <img :src="contentImage" alt="Main Content"
                                    class="w-full h-full object-cover bg-violet-200" />

                            </SplitterPanel>
                        </Splitter>
                    </SplitterPanel>
                </Splitter>
            </SplitterPanel>
        </Splitter>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'

// Images defined as constants
import sidebarImage from '../assets/lemon.jpg'
import headerImage from '../assets/chips1.jpg'
import menuImage from '../assets/meat1.jpg'
import contentImage from '../assets/chiken.jpg'

// Reactive sizes
const sidebarSize = ref(20)
const headerSize = ref(15)
const menuSize = ref(20)

let interval

onMounted(() => {
    interval = setInterval(() => {
        sidebarSize.value = Math.floor(Math.random() * 20) + 10 // 10–30%
        headerSize.value = Math.floor(Math.random() * 20) + 10
        menuSize.value = Math.floor(Math.random() * 20) + 10
    }, 1000)
})

onBeforeUnmount(() => {
    clearInterval(interval)
})
</script>
