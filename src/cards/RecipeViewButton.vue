<template>
  <button class="learn-more border rounded-3xl pt-1 border-gray-500/20" :style="{ '--theme': theme || '#FF5722' }">
    <span class="circle" aria-hidden="true">
      <span class="icon arrow"></span>
    </span>
    <span class="button-text">Open recipe</span>
  </button>
</template>

<script setup>
const props = defineProps({
  theme: String
})
</script>

<style scoped>
button {
  position: relative;
  display: inline-block;
  cursor: pointer;
  outline: none;
  background: transparent;
  padding: 0;
  font-size: inherit;
  font-family: inherit;
}

button.learn-more {
  width: 10rem;
  height: auto;
  --theme: #FF5722; /* fallback if prop is not passed */
}

button.learn-more .circle {
  transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
  position: relative;
  display: block;
  margin: 0;
  width: 2.5rem;
  height: 2.5rem;
  background: var(--theme);
  border-radius: 1.25rem;
}

button.learn-more .circle .icon {
  transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
  position: absolute;
  top: 0;
  bottom: 0;
  margin: auto;
  background: #fff;
}

button.learn-more .circle .icon.arrow {
  left: 0.5rem;
  width: 1rem;
  height: 0.125rem;
  background: none;
}

button.learn-more .circle .icon.arrow::before {
  content: "";
  position: absolute;
  top: -0.25rem;
  right: 0.05rem;
  width: 0.5rem;
  height: 0.5rem;
  border-top: 0.125rem solid #fff;
  border-right: 0.125rem solid #fff;
  transform: rotate(45deg);
}

button.learn-more .button-text {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 0.5rem 0;
  margin-left: 1.6rem;
  color: var(--theme);
  font-weight: 700;
  font-size: 0.85rem;
  line-height: 1.4;
  text-align: center;
  text-transform: uppercase;
  transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
}

button:hover .circle {
  width: 100%;
}

button:hover .circle .icon.arrow {
  background: #fff;
  transform: translate(0.8rem, 0);
}

button:hover .button-text {
  color: #fff;
}
</style>
