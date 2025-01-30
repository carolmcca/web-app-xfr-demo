<template>
  <div>
    <h1>Feature Extraction</h1>
    <p>Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quas ipsum nostrum error consequuntur voluptatibus temporibus, ipsa quisquam doloribus dolore eveniet ea amet facilis quasi, repellat velit voluptas cupiditate consectetur! Obcaecati voluptates eaque corporis veniam porro quam quae labore, enim sunt sapiente. Voluptate in quidem sequi inventore hic, earum atque magni explicabo pariatur itaque neque corrupti est laudantium perferendis at saepe, culpa ipsam suscipit. Blanditiis quibusdam fugit maxime asperiores esse eius iusto mollitia voluptates natus nam voluptatibus possimus doloremque nulla aspernatur hic dolorum temporibus ipsam consectetur voluptate, eaque perferendis placeat? Recusandae reiciendis atque ipsam magnam excepturi laudantium ab aliquam quae sequi!</p>
    <ImageInputComponent v-if="isInput" :image-number="1" @upload-images="onUpload" @select-images="onSelect"/>
    <SpinnerComponent v-if="loading" :visible="loading"/>
    <FeaturesComponent v-if="isOutput" :images="images" :data="result"></FeaturesComponent>  
  </div>
</template>

<script>
  import ImageInputComponent from '@/components/ImageInputComponent.vue';
  import FeaturesComponent from '@/components/FeaturesComponent.vue';
  import SpinnerComponent from '@/components/SpinnerComponent.vue';
  import backendApi from '../api/backend.js';

  export default {
    name: 'FeatureView',
    data() {
      return {
        result: {},
        isInput: true,
        isOutput: false,
        images: [],
        loading: false,
      }
    },
    components: { ImageInputComponent, FeaturesComponent, SpinnerComponent },
    methods: {
      onUpload(images) {
        this.requestFeatures(images);
      },
      onSelect(images) {
        alert("Not implemented yet!")
      },
      requestFeatures(images) {
        this.isInput = false;
        this.loading = true;
        this.images = images;
    
        const formData = new FormData();
        images.forEach((image, index) => {
          formData.append(`image${index + 1}`, image.file);
        });

        backendApi.post("/images/features/", formData)
        .then(response => response.data)
        .then(data => {
          this.result = data;
          this.loading = false;
          this.isOutput = true;
        })
        .catch(error => {
          this.loading = false;
          console.error("Error:", error);
        });
      }
    }
  }
</script>
