<template>
  <div>
    <h1>Authentication</h1>
    <p>The authentication task enables you to provide an image and an identity claim, in the form of a username, and confirm whether the provided image belongs to the claimed identity.</p>
    <div class="section" v-if="isInput">
      <label class="bold">Identity Claim:</label>
      <input type="text" id="id-claim" v-model="username" placeholder="insert your username">
    </div>
    <ImageInputComponent v-if="isInput" :image-number="1" @upload-images="onUpload" @select-images="onSelect"/>
    <SpinnerComponent v-if="loading" :visible="loading"/>
    <ResultsComponent v-if="isOutput" :data="result" :images="images" :message="message" :showPair="result.prediction" v-model="images"/> 
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
    name: 'AuthenticationView',
    data() {
      return {
        result: {},
        isInput: true,
        isOutput: false,
        images: [],
        loading: false,
        showPopup: false,
        popupMessage: "",
        username: ""
      }
    },
    computed: {
      message() {
        return this.result.prediction ? `The provided image likely bellongs to the identity ${this.username}` : `The provided image does not belong to the claimed identity ${this.username}`;
      }
    },
    components: { ImageInputComponent, ResultsComponent, SpinnerComponent, PopupComponent },
    methods: {
      onUpload(images) {
        if (this.username == "") {
          this.showPopup = true;
          this.popupMessage = "Please insert your username";
          return;
        }
        this.images = images;

        const formData = new FormData();
        images.forEach((image, index) => {
          formData.append(`image${index + 1}`, image.file);
        });
        formData.append("from_files", true);
        formData.append("username", this.username);
        this.requestPredictions(formData);
      },
      onSelect(images) {
        if (this.username == "") {
          this.showPopup = true;
          this.popupMessage = "Please insert your username";
          return;
        }
        this.images = [{"url": images[0]}, {"url": images[1]}];

        const formData = new FormData();
        images.forEach((image, index) => {
          formData.append(`image${index + 1}`, image);
        });
        formData.append("username", this.username)
        
        this.requestPredictions(formData);
      },
      requestPredictions(formData) {
        this.isInput = false;
        this.loading = true;
        const startTime = performance.now();

        backendApi.post("/users/verify/", formData)
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
            this.images[1] = {"url": data.pair_image};
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

<style>
  .bold {
    font-weight: bold;
    font-size: 1.17em;
  }

  #id-claim {
    margin-bottom: 1em;
    margin-left: 1em;
    background-color: white;
    text-align: center;
  }

  .section {
    margin-bottom: 2em;
  }

</style>
