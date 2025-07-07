<template>
  <div>
    <!-- Fallback Display When No ID -->
    <div v-if="!id" class="temporary__storage flex items-center justify-center min-h-screen">
      <div class="card relative max-w-md w-full shadow-xl rounded-xl overflow-hidden bg-white dark:bg-gray-800">

        <!-- Background/Placeholder -->
        <div class="image bg-gray-200 h-64 flex items-center justify-center">
          <p class="text-3xl font-bold text-gray-600 dark:text-gray-300">Coming Soon!!</p>
        </div>

        <!-- Overlay Layer -->
        <div class="image__overlay absolute inset-0 bg-gradient-to-t from-black/70 to-transparent"></div>

        <!-- Content Area -->
        <div class="content p-6 relative z-10 text-white">
          <div class="avatar w-12 h-12 bg-gray-400 rounded-full mb-3"></div>

          <div class="content__text">
            <h2 class="stream__title text-xl font-semibold">{{ name }}</h2>

            <div class="content__body mt-1 text-sm">
              <p class="streamer__name">{{ author }}</p>
              <p class="event text-yellow-400">Happening now</p>
            </div>

            <div class="categories mt-4 flex gap-2 flex-wrap">
              <a class="categories__btn bg-purple-500 hover:bg-purple-600 px-3 py-1 rounded-full text-sm">Español</a>
              <a class="categories__btn bg-blue-500 hover:bg-blue-600 px-3 py-1 rounded-full text-sm">KOI</a>
              <a class="categories__btn bg-green-500 hover:bg-green-600 px-3 py-1 rounded-full text-sm">LOL</a>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Stream View When ID is Present -->
    <div v-else>
      <router-view />
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  name: {
    type: String,
    default: 'Untitled',
  },
  author: {
    type: String,
    default: 'Anonymous',
  },
  id: {
    type: [String, Number],
    required: true,
  }
});
</script>

<style>
.image {
    width: 100%;
    height: 180px;
    position: absolute;
    background-color: rgb(144, 197, 47);
    cursor: pointer;
    transition: all .2s ease;
}

.image::before {
    content: "LIVE";
    position: absolute;
    top: 7px;
    left: 7px;
    font-weight: 900;
    font-size: .8em;
    background-color: rgb(228, 33, 33);
    border-radius: 5px;
    padding: 3px 5px;
}

.image::after {
    content: "102.2k viewers";
    position: absolute;
    bottom: 7px;
    left: 7px;
    font-weight: 300;
    font-size: .7em;
    background-color: rgb(59, 53, 53);
    border-radius: 2px;
    padding: 3px 5px;
}

.image__overlay {
    width: 100%;
    height: 180px;
}

.image:hover {
    transform: translate(8px, -8px);
    box-shadow: -1px 1px 0px 0px violet, -2px 2px 0px 0px violet, -3px 3px 0px 0px violet, -4px 4px 0px 0px violet, -5px 5px 0px 0px violet, -6px 6px 0px 0px violet, -7px 7px 0px 0px violet, -8px 8px 0px 0px violet;
}
</style>