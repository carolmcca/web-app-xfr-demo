<template>
  <div class="top">
      <h3>{{ label }}</h3>
    </div>
  <div class="card">
    <div class="drop-area" @dragover.prevent="onDragOver" @dragleave.prevent="onDragLeave" @drop.prevent="onDrop" @click.self="selectFiles">
      <span v-if="!isDragging">
        Drag & Drop image here or click to browse
      </span>
      <div class="select" v-else>Drop image here</div>
      <input type="file" name="file" class="file" accept=".png, .jpg, .jpeg" ref="ImageUploadComponent" :multiple="imageNumber!=1" @change="onFileSelect" />
      <div class="container" @click.self="selectFiles">
      <div class="image" v-for="(image, index) in images" :key="index" >
        <span class="delete" @click="deleteImage(index)">&times;</span>
        <img :src="image.url"/>
      </div>
    </div>
    </div>
  </div>
  <button type="button" @click="onSubmit">Upload</button>
</template>

<script>

export default {
  data() {
    return {
      isDragging: false
    };
  },
  props: ['label', 'images', 'imageNumber'],
  emits: ['submit-images'],
  methods: {
    selectFiles() {
      this.$refs.ImageUploadComponent.click();
    },
    onFileSelect(e) {
      const files = e.target.files;
      if (files) {
        this.handleFiles(files);
      }
    },
    handleFiles(files) {
      for (let i = 0; i < files.length; i++) {
        if (!files[i].type.startsWith('image/')) {
          continue;
        }
        if (!this.images.some(e => e.name === files[i].name)) {
          this.images.push({ name: files[i].name, url: URL.createObjectURL(files[i]), file: files[i] });
        }
      }
    },
    deleteImage(index) {
      this.images.splice(index, 1);
    },
    onDragOver(e) {
      e.preventDefault();
      this.isDragging = true;
      e.dataTransfer.dropEffect = 'copy';
    },
    onDragLeave(e) {
      e.preventDefault();
      this.isDragging = false;
    },
    onDrop(e) {
      e.preventDefault();
      this.isDragging = false;
      this.handleFiles(e.dataTransfer.files);
    },
    onSubmit() {
      this.$emit('submit-images', this.images);
    },
  },
}
</script>

<style scoped>

.card {
  width: 100%;
  border: 2px dashed var(--primary-color);
  border-radius: 5px;
  overflow: hidden;
  height: 10em;
}

.top {
  text-align: center;
  padding-bottom: 1.5em;
}

.card .drop-area {
  cursor: pointer;
  height: 100%;
  padding-top: 1em;
}

.card .drop-area span {
  height: 20%;
}

.card .select {
  margin-left: 5px;
  cursor: pointer;
  transition: 0.4s;
  color: var(--primary-color);
}

.card .select:hover {
  opacity: 0.6;
}

.card .container {
  width: 80%;
  height: 70%;
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
  align-items: flex-end;
  flex-wrap: wrap;
  max-height: 200px;
  position: relative;
  margin-top: 8px;
  margin-bottom: 8px;
}

.card .container .image {
  width: 75px;
  height: 75px;
  position: relative;
  margin: 5px 0 5px 5px;
}

.card .container .image img {
  width: 100%;
  height: 100%;
  border-radius: 5px;
  object-fit: cover;
}

.card .container .image span {
  position: absolute;
  top: -2px;
  right: 9px;
  font-size: 20px;
  cursor: pointer;
}

.card input, 
.card .drop-area .on-drop,
.card .drop-area.dragover .visible {
  display: none;
}

.delete {
  z-index: 999;
  color: var(--wrong-color);
}

input {
  display: block;
  margin: 20px auto;
  padding: 10px;
  width: 80%;
  height: 10em;
  border: 2px dashed var(--primary-color);
  border-radius: 5px;
  color: var(--primary-color);
  font-weight: bold;
  cursor: pointer;
}

</style>
