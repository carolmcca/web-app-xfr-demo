 <template> 
  <ImageSelectionComponent :imageNumber="imageNumber" :label="optionsLabel" @submit-images="onSelect"/>
  <h3 style="margin: 20px 0">OR</h3>
  <ImageUploadComponent :imageNumber="imageNumber" :label="uploadLabel" @submit-images="onUpload" :images="images"/>
  <PopupComponent v-if="activatePopup" :message="popupMessage" :has_input="false" :has_confirm="false" @cancel="activatePopup = false"/>
</template>

<script>

import ImageUploadComponent from '@/components/ImageUploadComponent.vue';
import ImageSelectionComponent from '@/components/ImageSelectionComponent.vue';
import PopupComponent from '@/components/PopupComponent.vue';

export default {
  name: 'ImageInputComponent',
  components: { ImageUploadComponent, ImageSelectionComponent, PopupComponent },
  props: { imageNumber: Number, requestPredictions: Function},
  emits: ['upload-images', 'select-images'],
  data() {
    return {
      activatePopup: false,
      popupMessage: "",
      images: []
    }
  },
  computed: {
    optionsLabel() {
      return this.imageNumber == 1 ? 'Choose one of our faces' : 'Choose two of our faces';
    },
    uploadLabel() {
      return this.imageNumber == 1 ? 'Upload your own image' : 'Upload two images';
    }
  },
  methods: {
    onUpload(images) {
      if ( images.length != this.imageNumber ) {
        this.popupMessage = `Please upload ${this.imageNumber} image(s)`;
        this.activatePopup = true;
        return;
      } else {
        this.$emit('upload-images', images);
      }
    },
    onSelect(images) {
      if ( images.length != this.imageNumber ) {
        this.popupMessage = `Please select ${this.imageNumber} image(s)`;
        this.activatePopup = true;
        return;
      } else {
        this.$emit('select-images', images);
      }
    }
  }
}

</script>
