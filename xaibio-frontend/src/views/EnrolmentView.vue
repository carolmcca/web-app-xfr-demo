<template>
  <div>
    <button id="logout-button" @click="logout"><font-awesome-icon :icon="logoutIcon" /></button>
    <h1>Enrolment</h1>
    <p>The enrolment task allows you to link some photos to your identity in our database. This task is essential for creating your profile and enabling our system to recognize you in future verifications. Please add pictures of your identity only.</p>
    <ImageUploadComponent label="Upload your images" @submit-images="onUpload" :images="images"/>
    <SpinnerComponent v-if="loading" :visible="loading"/>
    <PopupComponent v-if="openPopup" :message="popupMessage" :is_custom="false" @cancel="openPopup = false" />
    <PopupComponent v-if="openConfirmPopup" :message="popupMessage" :is_custom="true" @cancel="openConfirmPopup = false" @submit="handleSubmit" />
    <div v-if="databaseImages.length > 0" id="my-images">
      <h3>Your Images</h3>
      <div class="image-gallery">
        <div v-for="(image, index) in databaseImages" :key="index">
          <img :src="image" />
          <span class="delete" @click="confirmDeleteImage(index)">&times;</span>
        </div>
      </div>
    </div>
    <button class="delete-button" @click="confirmDeleteAccount">Delete my account</button>
  </div>
</template>

<script>
  import ImageUploadComponent from '@/components/ImageUploadComponent.vue';
  import PopupComponent from '@/components/PopupComponent.vue';
  import SpinnerComponent from '@/components/SpinnerComponent.vue';
  import backendApi from '../api/backend.js';
  import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
  import { faArrowRightFromBracket } from '@fortawesome/free-solid-svg-icons';

  export default {
    name: 'EnrolmentView',
    data() {
      return {
        images: [],
        openPopup: false,
        popupMessage: "",
        openConfirmPopup: false,
        imgToDelete: "",
        username: "",
        loading: false,
        logoutIcon: faArrowRightFromBracket,
        databaseImages: [],
        confirmPopupType: ""
      }
    },
    components: { ImageUploadComponent, PopupComponent, SpinnerComponent, FontAwesomeIcon },
    created() {
      const token = this.$cookies.get("jwt_token");
      if (!token) {
        this.$router.push("/login");
      } else {
        backendApi.get("/users/auth/", { headers: { Authorization: "Bearer " + token } })
          .then(response => console.log(response.data))
          .catch(error => this.$router.push("/login"));
      }
    },
    mounted() {
      backendApi.get("users/images/", { headers: { Authorization: "Bearer " + this.$cookies.get("jwt_token") } })
        .then(response => response.data)
        .then(data => {
          this.databaseImages = data.image_urls;
        })
        .catch(error => {
          console.error("Error:", error);
        });
    },
    methods: {
      onUpload(images) {
        this.images = images;

        if (this.images.length < 1) {
          this.popup("info", "Please upload at least one image.");
          return;
        }

        this.uploadImages();
      },
      uploadImages(force=false) {
        this.loading = true;
        this.openPopup = false;
        this.openConfirmPopup = false;
        const formData = new FormData();
        this.images.forEach((image, index) => {
          formData.append(`image${index + 1}`, image.file);
        });
        formData.append("force", force);

        backendApi.post("/users/images/", formData, { headers: { Authorization: "Bearer " + this.$cookies.get("jwt_token") } })
        .then(response => response.data)
        .then(data => {
          this.loading = false;
          if (data.error) {
            if (data.error.type) {
              console.log(data.error.type)
              this.openConfirmPopup = true;
              this.confirmPopupType = "add-images";
              this.popupMessage = "The images don't appear to be all yours. Are you sure you want to add them to your identity?";
            } else {
              this.popup(data.error);
            }
          } else {
            location.reload();
          }
        })
        .catch(error => {
          this.loading = false;
          console.error("Error:", error);
        });
      },
      confirmDeleteImage(index) {
        this.openConfirmPopup = true;
        this.imgToDelete = this.databaseImages[index]
        this.confirmPopupType = "delete-image";
        this.popupMessage = "Are you sure you want to delete this image? This operation cannot be reversed.";
      },
      confirmDeleteAccount() {
        this.openConfirmPopup = true;
        this.confirmPopupType = "delete-account";
        this.popupMessage = "Are you sure you want to delete your account? This operation cannot be reversed.";
      },
      handleSubmit() {
        if (this.confirmPopupType == "delete-account") {
          this.deleteAccount();
        } else if (this.confirmPopupType == "delete-image"){
          this.deleteImage();
        } else {
          this.uploadImages(true);
        }
      },
      deleteImage() {
        this.closePopup();
        backendApi.post('users/images/delete/', {path: this.imgToDelete}, { headers: { Authorization: "Bearer " + this.$cookies.get("jwt_token")} })
        .then(response => response.data)
        .then(data => {
          if (data.error) {
            this.popup(data.error);
          } else {
            location.reload();
          }
        })
        .catch(error => {
          console.log('Error', error)
        })
      },
      deleteAccount() {
        this.closePopup();
        backendApi.delete("users/", { headers: { Authorization: "Bearer " + this.$cookies.get("jwt_token")} })
        .then(response => response.data)
        .then(data => {
          if (data.error) {
            this.popup(data.error);
          } else {
            this.$cookies.remove('jwt_token')
            this.$router.push({name: 'home'})
          }
        })
        .catch(error => {
          console.log('Error', error)
        })
      },
      popup(message) {
        this.popupMessage = message;
        this.openPopup = true;
      },
      closePopup() {
        this.openPopup = false;
        this.openDeleteConfirm = false;
        this.popupMessage = "";
      },
      logout() {
        this.$cookies.remove("jwt_token");
        this.$router.push({name: "home"});
      }
    }
  }
</script>

<style>

  .radio-group {
    margin-bottom: 10px;
  }

  input {
    padding: 10px;
    border-radius: 20px;
    border: none;
    background-color: var(--background-color);
  }

  .custom-radio {
    display: none;
  }

  .custom-radio + label {
    position: relative;
    padding-left: 35px;
    cursor: pointer;
    font-size: 18px;
    user-select: none;
  }

  .custom-radio + label::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    width: 1em;
    height: 1em;
    border-radius: 50%;
    border: 2px solid var(--primary-color);
    background: white;
  }

  .custom-radio:checked + label::after {
    content: "";
    position: absolute;
    left: 0.25em;
    top: 0.25em;
    width: 0.7em;
    height: 0.7em;
    border-radius: 50%;
    background: var(--primary-color);
  }

  .custom-radio:focus + label::before {
    outline: none;
    border: 2px solid var(--primary-color);
  }

  p.error {
    color: var(--wrong-color);
    font-size: small;
    padding: 0px;
  }

  #logout-button {
    background-color: var(--primary-color);
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 20px;
    margin-top: 20px;
    position: absolute;
    right: 0px;
    top: 0px;
  }

  #logout-button:hover {
    background-color: var(--accent-color);
  }

  .image-gallery {
    display: flex;
    flex-direction: row;
    width: 100%;
    flex-wrap: wrap;
    justify-content: center;
    margin-top: 2em;
  }

  .image-gallery div {
    margin: 10px;
    border-radius: 20px;
    position: relative;
  }

  .image-gallery div img {
    width: 8em;
    height: 8em;
    border-radius: 20px;
    object-fit: cover;
  }

  .delete {
    position: absolute;
    top: 2%;
    right: 10%;
    font-size: 20px;
    cursor: pointer;
    z-index: 999;
    color: var(--wrong-color);
  }

  #my-images {
    margin-top: 2em;
  }

  .delete-button {  
    color: var(--wrong-color)
  }

  .delete-button:hover {
    background-color: var(--wrong-color);
    color: white;
  }

</style>
