<template>
  <div class="cards">

  <input type="radio" id="radio-1" name="radio-card" checked>
  <article class="card" style="--angle:4deg">
    <img class="card-img" src="https://picsum.photos/id/21/200/300">
    <div class="card-data">
      <span class="card-num">1/7</span>
      <h2>Alejandro Escamilla</h2>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Natus maiores accusantium cumque atque? Ex voluptatem quisquam temporibus. Provident rerum quae nemo eligendi fugiat!</p>
        <footer>
          <label for="radio-7" aria-label="Previous">&#10094;</label>
          <label for="radio-2" aria-label="Next">&#10095;</label>
        </footer>
    </div>
  </article>

  <!-- card 2 -->
  <input type="radio" id="radio-2" name="radio-card">
  <article class="card" style="--angle:-8deg">
    <img class="card-img" src="https://picsum.photos/id/30/200/300">
    <div class="card-data">
      <span class="card-num">2/7</span>
      <h2>Shyamanta Baruah</h2>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Natus maiores accusantium cumque atque? Ex voluptatem quisquam temporibus. Provident rerum quae nemo eligendi fugiat!</p>
        <footer>
          <label for="radio-1" aria-label="Previous">&#10094;</label>
          <label for="radio-3" aria-label="Next">&#10095;</label>
        </footer>
    </div>
  </article>

  <!-- card 3 -->
  <input type="radio" id="radio-3" name="radio-card">
  <article class="card" style="--angle:-7deg">
    <img class="card-img" src="https://picsum.photos/id/39/200/300">
    <div class="card-data">
      <span class="card-num">3/7</span>
      <h2>Luke Chesser</h2>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Natus maiores accusantium cumque atque? Ex voluptatem quisquam temporibus. Provident rerum quae nemo eligendi fugiat!</p>
        <footer>
          <label for="radio-2" aria-label="Previous">&#10094;</label>
          <label for="radio-4" aria-label="Next">&#10095;</label>
        </footer>
    </div>
  </article>

  <!-- card 4 -->
  <input type="radio" id="radio-4" name="radio-card">
  <article class="card" style="--angle:11deg">
    <img class="card-img" src="https://picsum.photos/id/103/200/300">
    <div class="card-data">
      <span class="card-num">4/7</span>
      <h2>Ilham Rahmansyah</h2>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Natus maiores accusantium cumque atque? Ex voluptatem quisquam temporibus. Provident rerum quae nemo eligendi fugiat!</p>
        <footer>
          <label for="radio-3" aria-label="Previous">&#10094;</label>
          <label for="radio-5" aria-label="Next">&#10095;</label>
        </footer>
    </div>
  </article>

  <!-- card 5 -->
  <input type="radio" id="radio-5" name="radio-card">
  <article class="card" style="--angle:13deg">
    <img class="card-img" src="https://picsum.photos/id/175/200/300">
    <div class="card-data">
      <span class="card-num">5/7</span>
      <h2>petradr</h2>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Natus maiores accusantium cumque atque? Ex voluptatem quisquam temporibus. Provident rerum quae nemo eligendi fugiat!</p>
        <footer>
          <label for="radio-4" aria-label="Previous">&#10094;</label>
          <label for="radio-6" aria-label="Next">&#10095;</label>
        </footer>
    </div>
  </article>

  <!-- card 6 -->
  <input type="radio" id="radio-6" name="radio-card">
  <article class="card" style="--angle:-17deg">
    <img class="card-img" src="https://picsum.photos/id/349/200/300">
    <div class="card-data">
      <span class="card-num">6/7</span>
      <h2>Caleb George</h2>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Natus maiores accusantium cumque atque? Ex voluptatem quisquam temporibus. Provident rerum quae nemo eligendi fugiat!</p>
        <footer>
          <label for="radio-5" aria-label="Previous">&#10094;</label>
          <label for="radio-7" aria-label="Next">&#10095;</label>
        </footer>
    </div>
  </article>

  <!-- card 7 -->
  <input type="radio" id="radio-7" name="radio-card">
  <article class="card" style="--angle:20deg">
    <img class="card-img" src="https://picsum.photos/id/401/200/300">
    <div class="card-data">
      <span class="card-num">7/7</span>
      <h2>Austin Ban</h2>
        <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Natus maiores accusantium cumque atque? Ex voluptatem quisquam temporibus. Provident rerum quae nemo eligendi fugiat!</p>
        <footer>
          <label for="radio-6" aria-label="Previous">&#10094;</label>
          <label for="radio-1" aria-label="Next">&#10095;</label>
        </footer>
    </div>
  </article>
</div>
</template>
<style scoped>
*,
::before,
::after {
    margin: 0;
}

@property --angle {
    syntax: "<angle>";
    initial-value: 0deg;
    inherits: true;
}

/* general styling */
html {
    color-scheme: dark light;
}

img {
    max-width: 100%;
}

/* Hide radio buttons */
input[type="radio"] {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    margin: -1px;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    white-space: nowrap;
    border-width: 0;
}

body {

    min-height: 100svh;
    display: grid;
    place-content: center;
    margin: 0;
    padding: 1rem;
    font: 1rem system-ui;
}

.cards {
    --img-w: 200px;
    --duration: 300ms;
    --img-easing: cubic-bezier(0.34, 1.56, 0.64, 1);
    width: min(100% - 4rem, 800px);
    margin-inline: auto;
    display: grid;

    counter-reset: my-counter;
}

.card {
    --cards-grid-cols: auto;
    --cards-grid-rows: var(--img-w) auto;
    --cards-grid-gap: 2rem;
    --cards-footer-justify: center;

    grid-area: 1/1;
    display: grid;
    place-items: center;
    grid-template-columns: var(--cards-grid-cols);
    grid-template-rows: var(--cards-grid-rows);
    gap: var(--cards-grid-gap);

}

@media (600px < width) {
    .card {
        --cards-grid-cols: var(--img-w) auto;
        --cards-grid-rows: auto;
        --cards-grid-gap: 4rem;
        --cards-footer-justify: start;
    }
}


.card-img {
    width: 200px;
    height: 200px;
    aspect-ratio: 1 / 1;
    rotate: var(--angle, 0deg);
    border-radius: 10px;
    border: 3px solid #FFF;
    overflow: hidden;
    transform-origin: center;
    object-fit: cover;
    box-shadow: 0 0 5px 3px rgba(0 0 0 / .05);
}



input:nth-of-type(1):checked+.card~.card>.card-img {
    animation: straighten-img-1 calc(var(--duration) * 2) forwards;
    animation-timing-function: var(--img-easing);
}

.card:has(~input:nth-of-type(2):checked)>.card-img,
input:nth-of-type(2):checked+.card~.card>.card-img {
    animation: straighten-img-2 calc(var(--duration) * 2) forwards;
    animation-timing-function: var(--img-easing);
}

.card:has(~input:nth-of-type(3):checked)>.card-img,
input:nth-of-type(3):checked+.card~.card>.card-img {
    animation: straighten-img-3 calc(var(--duration) * 2) forwards;
    animation-timing-function: var(--img-easing);
}

.card:has(~input:nth-of-type(4):checked)>.card-img,
input:nth-of-type(4):checked+.card~.card>.card-img {
    animation: straighten-img-4 calc(var(--duration) * 2) forwards;
    animation-timing-function: var(--img-easing);
}

.card:has(~input:nth-of-type(5):checked)>.card-img,
input:nth-of-type(5):checked+.card~.card>.card-img {
    animation: straighten-img-5 calc(var(--duration) * 2) forwards;
    animation-timing-function: var(--img-easing);
}

.card:has(~input:nth-of-type(6):checked)>.card-img,
input:nth-of-type(6):checked+.card~.card>.card-img {
    animation: straighten-img-6 calc(var(--duration) * 2) forwards;
    animation-timing-function: var(--img-easing);
}

.card:has(~input:nth-of-type(7):checked)>.card-img,
input:nth-of-type(7):checked+.card~.card>.card-img {
    animation: straighten-img-7 calc(var(--duration) * 2) forwards;
    animation-timing-function: var(--img-easing);
}

/* as CSS can't remove animations, we change the animation according to which checkbox is checked  - all animations are the same (would be simpler with SCSS) */
@keyframes straighten-img-1 {
    50% {
        --angle: 0deg;
    }
}

@keyframes straighten-img-2 {
    50% {
        --angle: 0deg;
    }
}

@keyframes straighten-img-3 {
    50% {
        --angle: 0deg;
    }
}

@keyframes straighten-img-4 {
    50% {
        --angle: 0deg;
    }
}

@keyframes straighten-img-5 {
    50% {
        --angle: 0deg;
    }
}

@keyframes straighten-img-6 {
    50% {
        --angle: 0deg;
    }
}

@keyframes straighten-img-7 {
    50% {
        --angle: 0deg;
    }
}


/* stacking order - these are updated according to which card is selected */
.card {
    z-index: -1;
}

input:checked+.card {
    z-index: 10 !important;
}

/* next card checked - place behind */
.card:has(+input:checked) {
    z-index: 9;
}

/* next card +1 checked - place behind */
.card:has(+input + .card + input:checked) {
    z-index: 8;
}

/* next card +2 checked - place behind */
.card:has(+input + .card +input + .card + input:checked) {
    z-index: 7;
}

/* next card +3 checked - place behind */
.card:has(+input + .card +input + .card +input + .card + input:checked) {
    z-index: 6;
}

/* next card +4 checked - place behind */
.card:has(+input + .card +input + .card +input + .card +input + .card + input:checked) {
    z-index: 5;
}

/* next card +5 checked - place behind */
.card:has(+input + .card +input + .card +input +input + .card +input + .card +input + .card + input:checked) {
    z-index: 4;
}

/* next card +6 checked - place behind */
.card:has(+input + .card +input + .card +input + .card +input +input + .card +input + .card +input + .card + input:checked) {
    z-index: 3;
}

.card-data {
    display: grid;
    gap: 1rem;
}

.card-data>.card-num {
    opacity: var(--data-opacity, 0);
    font-size: .8rem;
    color: #666;
}

.card-data>p {
    font-size: 0.9rem;

}

.card-data>h2,
.card-data>p {
    transition: var(--duration) ease-in-out;
    transition-delay: var(--data-delay, 0ms);
    opacity: var(--data-opacity, 0);
    translate: 0 var(--data-y, 20px);
}

.card-data>footer {
    display: flex;
    justify-content: var(--cards-footer-justify);
    gap: 2rem;
}

.card-data>footer label {
    margin-block-start: auto;
    cursor: pointer;
    pointer-events: var(--card-events, none);
    opacity: var(--data-opacity, 0);
    transition: color var(--duration) ease-in-out;
    color: var(--label-clr-txt, #000);
    background-color: var(--label-clr-bg, #EEE);
    border-radius: 50%;
    width: 32px;
    height: 32px;
    aspect-ratio: 1/1;
    display: grid;
    place-content: center;
    transition: background-color 300ms ease-in-out, color 300ms ease-in-out;
}


input:checked:focus-visible+.card>.card-data>footer label,
.card-data>footer label:hover {
    --label-clr-txt: #FFF;
    --label-clr-bg: steelblue;
}

input:checked+.card {
    --data-opacity: 1;
    --data-y: 0;
    --data-delay: var(--duration);
    --card-events: auto;
    transition: z-index;
    transition-delay: 300ms;
    /*z-index: 1;*/
}

input:checked+.card>.card-img {
    animation: reveal-img calc(var(--duration) * 2) forwards;
}

@keyframes reveal-img {
    50% {
        translate: -150% 0;
        --angle: 0deg;
    }
}
</style>
