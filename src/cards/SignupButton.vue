<template>
  <div class="buttons">
    <button
      class="btn"
      :style="{ '--theme': theme }"
      :class="{ start: isStart }"
      @mouseenter="isStart = false"
    >
      <span></span>
      <p
        data-start="Good Luck!"
        data-text="Create Account"
        data-title="Sign Up"
      ></p>
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  theme: {
    type: String,
    default: '#00ad54'
  }
})

const isStart = ref(false)
</script>

<style scoped>
.buttons {
  display: flex;
  justify-content: center;
  align-items: center;
}

/* Button base */
.btn {
  width: 155px;
  height: 40px;
  font-size: 14px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1px;
  background-color: #fff;
  color: var(--theme);
  border: none;
  border-radius: 0;
  cursor: pointer;
  overflow: hidden;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.btn::before,
.btn::after,
.btn span::before,
.btn span::after {
  content: "";
  position: absolute;
  background-color: var(--theme);
  transition: all 0.3s cubic-bezier(0.35, 0.1, 0.25, 1);
    border-radius: 1.5rem;

}

/* Border top/bottom animation */
.btn::before,
.btn::after {
  width: 0;
  height: 2px;
}

.btn::before {
  top: 0;
  right: 0;
  transition-duration: 0.5s;
}

.btn::after {
  bottom: 0;
  left: 0;
}

/* Border left/right animation */
.btn span::before,
.btn span::after {
  width: 2px;
  height: 0;
}

.btn span::before {
  top: 0;
  right: 0;
  transition-duration: 0.5s;
}

.btn span::after {
  bottom: 0;
  left: 0;
}

/* Hover animations */
.btn:hover::before,
.btn:hover::after {
  width: 100%;
}

.btn:hover span::before,
.btn:hover span::after {
  height: 100%;
}

.btn span {
  width: 100%;
  height: 100%;
  position: absolute;
  inset: 0;
  z-index: 1;
}

/* Text container */
.btn p {
  position: absolute;
  width: 100%;
  height: 100%;
  margin: 0;
  padding: 0;
  z-index: 2;
  transition: all 0.4s cubic-bezier(0.35, 0.1, 0.25, 1);
}

/* Text content */
.btn p::before,
.btn p::after {
  content: '';
  position: absolute;
  width: 100%;
  left: 0;
  transition: all 0.4s cubic-bezier(0.35, 0.1, 0.25, 1);
}

.btn p::before {
  content: attr(data-title);
  top: 50%;
  transform: translateY(-50%);
}

.btn p::after {
  content: attr(data-text);
  top: 150%;
  color: var(--theme);
}

.btn:hover p::before {
  top: -50%;
  transform: rotate(5deg);
}

.btn:hover p::after {
  top: 50%;
  transform: translateY(-50%);
}

/* Start animation state */
.btn.start {
  background-color: var(--theme);
  box-shadow: 0px 5px 10px -10px rgba(0, 0, 0, 0.2);
}

.btn.start p::before {
  top: -50%;
  transform: rotate(5deg);
}

.btn.start p::after {
  content: attr(data-start);
  top: 50%;
  transform: translateY(-50%);
  color: #fff;
  animation: fadeIn 0.3s ease forwards;
}

@keyframes fadeIn {
  from {
    top: -50%;
  }
}

/* Accessibility */
.btn:focus {
  outline: 2px solid var(--theme);
  outline-offset: 2px;
}
</style>
