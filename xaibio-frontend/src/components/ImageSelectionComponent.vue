<template>
  <h3>{{ label }}</h3>
  <div class="image-selection">
    <img v-for="(image, index) in images" :class="selected[index] ? 'selected' : ''" :src="image" alt="image" @click="onSelectImage(index)">
  </div>
  <button type="button" @click="onSubmit">Select</button>
</template>

<script>
import backendApi from '../api/backend';

export default {
  data() {
    return {
      images: [],
      selected: []
    }
  },
  props: ['label', 'imageNumber'],
  emits: ['submit-images'],
  mounted() {
    this.fetchImages();
  },
  methods: {
    onSelectImage(index) {
      if (this.imageNumber === 1) {
        this.selected = new Array(this.images.length).fill(false);
        this.selected[index] = true;
      } else if (this.imageNumber === 2) {
        const selectedCount = this.selected.filter(Boolean).length;
        if (selectedCount < 2 || (selectedCount === 2 && this.selected[index])) {
          this.selected[index] = !this.selected[index];
        }
      }
    },
    onSubmit() {
      let selectedImages = this.images.filter((image, index) => this.selected[index]);
      this.$emit('submit-images', selectedImages);
    },
    fetchImages() {
      backendApi.get('/images/examples/')
        .then(response => response.data)
        .then(data => {
          this.images = data;
          this.selected = new Array(data.length).fill(false);
        })
        .catch(error => {
          console.error('Error fetching images:', error);
        });
    },
  }
}
</script>

<style>
  .image-selection {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    margin: 0 auto;
  }
  .image-selection img {
    max-width: 400px;
    max-height: 250px;
    margin: 20px;
    object-fit: cover;
    cursor: pointer;
  }
  .image-selection img.selected {
    opacity: 50%;
  }
</style>