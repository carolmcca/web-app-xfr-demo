<template>
  <div>
    <h1>Identification</h1>
    <p>The identification task allows you to determine a person's identity by comparing facial features. Choose an image from our provided options or upload your own, and our system will search for the most similar face in our database and let you know if it's the same person. This task is used in a variety of contexts, such as law enforcement investigations, access control in buildings or events, and personalized user experiences in applications like social media.</p>
    <ImageInputComponent v-if="isInput" :image-number="1" @upload-images="onUpload" @select-images="onSelect"/>
    <SpinnerComponent v-if="loading" :visible="loading"/>
    <ResultsComponent v-if="isOutput" :data="result" :images="images" :message="message" :showPair="result.prediction"/>
    <PopupComponent v-if="showPopup" :message="popupMessage" :is_custom="false" @cancel="showPopup = false" />
  </div>
</template>

<script>
  import ImageInputComponent from '@/components/ImageInputComponent.vue';
  import ResultsComponent from '@/components/ResultsComponent.vue';
  import SpinnerComponent from '@/components/SpinnerComponent.vue';
  import backendApi from '../api/backend.js';
  import PopupComponent from '@/components/PopupComponent.vue';

  export default {
    name: 'IdentificationView',
    data() {
      return {
        result: {},
        isInput: true,
        isOutput: false,
        images: [],
        loading: false,
        showPopup: false,
        popupMessage: ""
      }
    },
    computed: {
      message() {
        return this.result.prediction ? "The provided identity was found on the database!" : "The provided identity wasn't found on the database.";
      }
    },
    components: { ImageInputComponent, ResultsComponent, SpinnerComponent, PopupComponent },
    methods: {
      onUpload(images) {
        this.images = images;
        const formData = new FormData(); 
        images.forEach((image, index) => {
          formData.append(`image${index + 1}`, image.file);
        });
        formData.append("from_files", true);
        
        this.requestPredictions(formData)
      },
      onSelect(images) {
        this.images = [{url: images[0]}];

        const formData = new FormData(); 
        images.forEach((image, index) => {
          formData.append(`image${index + 1}`, image);
        });

        this.requestPredictions(formData)
      },
      requestPredictions(formData) {
        this.isInput = false;
        this.loading = true;
        const startTime = performance.now();

        backendApi.post("/images/identify/", formData)
        .then(response => response.data)
        .then(data => {
          if (data.error) {
            this.showPopup = true;
            this.popupMessage = data.error;
            this.loading = false;
            this.isInput = true;
          } else {
            const endTime = performance.now()
            console.log("Identification time: ", endTime-startTime)
            this.images[1] = {"url": data.pair_image};
            this.result = data;
            this.loading = false;
            this.isOutput = true;
          }
        })
        .catch(error => {
          this.loading = false;
          console.error("Error:", error);
        });
      }
    }
  }
</script>