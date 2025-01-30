<template>
  <div class="control">
    <button @click="toggleVisibility"><font-awesome-icon :icon="icon" /></button>
    <slot></slot>
    <input type="range" v-model="opacity" min="0" max="1" step="0.01">
    <input class="small-input" type="text" v-model="opacity">
  </div>

</template>

<script>

import { faEyeSlash } from '@fortawesome/free-solid-svg-icons';
import { faEye } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';

export default {
  name: 'xSSABComponent',
  data() {
    return {
      opacity: 1,
      isVisible: true,
    }
  },
  components: { FontAwesomeIcon },
  methods: {
    toggleVisibility() {
      this.isVisible = !this.isVisible;
      this.$emit('toggle-visibility', this.isVisible)
    },
  },
  emits: ['toggle-visibility', 'opacity-change'],
  computed: {
    icon() {
      return this.isVisible ? faEye : faEyeSlash;
    }
  },
  watch: {
    opacity: function() {
      this.$emit('opacity-change', this.opacity);
    }
  }
}

</script>

<style>
.control {
  display: flex;
  justify-content: center;
  align-items: center;
}

</style>