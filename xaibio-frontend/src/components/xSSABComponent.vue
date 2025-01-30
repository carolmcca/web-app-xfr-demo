<template>
  <div class="image-explanation">
    <div class="image-container">
      <img :src="`data:image/png;base64,${image}`" class="base-image" :style="{ opacity: baseOpacity, visibility: showBase ? 'visible' : 'hidden' }"/>
      <img :src="`data:image/png;base64,${gradPosImage}`" class="overlay-image" :style="{ opacity: positiveOpacity, visibility: showPositive ? 'visible' : 'hidden' }" />
      <img :src="`data:image/png;base64,${gradNegImage}`" class="overlay-image" :style="{ opacity: negativeOpacity, visibility: showNegative ? 'visible' : 'hidden' }" />
    </div>
    <div>
      <LayerControlsComponent @toggle-visibility="toggleBase" @opacity-change="updateBaseOpacity">
        <p class="label">Original Image (croped)</p>
      </LayerControlsComponent>
      <LayerControlsComponent @toggle-visibility="togglePositive" @opacity-change="updatePositiveOpacity">
        <p class="label">Positive Contributions</p>
      </LayerControlsComponent>
      <LayerControlsComponent @toggle-visibility="toggleNegative" @opacity-change="updateNegativeOpacity">
        <p class="label">Negative Contributions</p>
      </LayerControlsComponent>
    </div>
  </div>
  
</template>

<script>
import LayerControlsComponent from '@/components/LayerControlsComponent.vue';

export default {
  name: 'xSSABComponent',
  props: ['gradPosImage', 'gradNegImage', 'image'],
  components: { LayerControlsComponent },
  data() {
    return {
      showPositive: true,
      positiveOpacity: 1,
      showNegative: true,
      negativeOpacity: 1,
      showBase: true,
      baseOpacity: 1,
    }
  },
  methods: {
    togglePositive(showPositive) {
      this.showPositive = showPositive
    },
    toggleNegative(showNegative) {
      this.showNegative = showNegative
    },
    updatePositiveOpacity(opacity) {
      this.positiveOpacity = opacity;
    },
    updateNegativeOpacity(opacity) {
      this.negativeOpacity = opacity;
    },
    toggleBase(showBase) {
      this.showBase = showBase
    },
    updateBaseOpacity(opacity) {
      this.baseOpacity = opacity;
    }
  },
}

</script>

<style>

.control .label {
  flex-grow: 1;
}

.control button {
  width: 4em;
}

.image-explanation {
  display: flex;
  justify-content: center;
  flex-direction: column;
  align-items: center;
}

.image-explanation .image-container {
  position: relative;
  display: flex;
  justify-content: center; 
  width: 80%;
}

.base-image .overlay-image {
  display: block;
}

.overlay-image {
  position: absolute;
  width: 100%;
  height: 100%;
}

input[type="text"].small-input {
  width: 3em;
  background-color: white;
  text-align: center;
}

/* === range theme and appearance === */
input[type="range"] {
  -webkit-appearance: none;
  appearance: none;
  width: 12.5em;
  height: 0.125em;
  background: white;
  cursor: pointer;
  padding: 0.8em;
  margin: 2em;
  transition: background 0.15s ease-in-out;
}

input[type="range"]:hover {
  background: rgba(0, 0, 0, 0.05);
}

input[type="range"]::-webkit-slider-thumb {
  -webkit-appearance: none;
  appearance: none;
  width: 1.125em;
  height: 1.125em;
  background: var(--accent-color);
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.15s ease-in-out;
}

input[type="range"]:hover::-webkit-slider-thumb {
  background: var(--accent-color);
}

input[type="range"]::-moz-range-thumb {
  width: 1.125em;
  height: 1.125em;
  background: var(--accent-color);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.15s ease-in-out;
}

input[type="range"]:hover::-moz-range-thumb {
  background: var(--accent-color);
}

input[type="range"]::-ms-thumb {
  width: 1.125em;
  height: 1.125em;
  background: var(--accent-color);
  border: none;
  border-radius: 50%;
  cursor: pointer;
  transition: background 0.15s ease-in-out;
}

input[type="range"]:hover::-ms-thumb {
  background: var(--accent-color);
}

input[type="range"]:focus {
  outline: none;
}

input[type="range"]:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>