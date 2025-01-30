<template>
  <div>
    <h1>Verification</h1>
    <p>The verification task enables you to confirm whether two images belong to the same person by analyzing their facial features. Simply provide two images—either by selecting from our options or uploading your own—and our system will compare them. If the facial features closely match, our app will indicate that the images likely depict the same person. This task can be used in scenarios like identity confirmation for online transactions and access control at secure facilities.</p>
    <ImageInputComponent v-if="isInput" :image-number="2" @upload-images="onUpload" @select-images="onSelect"/>
    <SpinnerComponent v-if="loading" :visible="loading"/>
    <ResultsComponent v-if="isOutput" :data="result" :images="images" :message="message" :showPair="true" v-model="images"/> 
    <PopupComponent v-if="showPopup" :message="popupMessage" @cancel="showPopup = false"/>
  </div>
</template>

<script>
  import ImageInputComponent from '@/components/ImageInputComponent.vue';
  import ResultsComponent from '@/components/ResultsComponent.vue';
  import SpinnerComponent from '@/components/SpinnerComponent.vue';
  import backendApi from '../api/backend.js';
  import PopupComponent from '@/components/PopupComponent.vue';

  export default {
    name: 'VerificationView',
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
        return this.result.prediction ? "The provided images likelly depict the same person" : "The provided images likely depict different people";
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
        this.requestPredictions(formData);
      },
      onSelect(images) {
        this.images = [{"url": images[0]}, {"url": images[1]}];

        const formData = new FormData();
        images.forEach((image, index) => {
          formData.append(`image${index + 1}`, image);
        });
        
        this.requestPredictions(formData);
      },
      requestPredictions(formData) {
        this.isInput = false;
        this.loading = true;
        const startTime = performance.now();

        backendApi.post("/images/verify/", formData)
        .then(response => response.data)
        .then(data => {
          if (data.error) {
            this.loading = false;
            this.showPopup = true;
            this.popupMessage = data.error;
            this.isInput = true;
          } else {
            const endTime = performance.now()
            console.log("Verification time: ", endTime-startTime)
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
