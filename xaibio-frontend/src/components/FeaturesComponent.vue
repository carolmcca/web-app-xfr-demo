<template>
  <div>
    <h3>Your results</h3>
    <div class="results-container">
      <div class="image-container row">
        <img :src="images[0].url" />
        <div class="feature-container">
          <h3>Features present in the image</h3>
          <ChipComponent v-for="feature in data.features.positive" color="green" selected="">{{feature}}</ChipComponent>
          <ChipComponent v-for="feature in data.features.neutral" color="orange" selected="">{{feature}}</ChipComponent>
          <h3>Features not present in the image</h3>
          <ChipComponent v-for="feature in data.features.negative" color="red" selected="">{{feature}}</ChipComponent>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ChartComponent from '@/components/ChartComponent.vue';
import ChipComponent from '@/components/ChipComponent.vue'; 

export default {
  name: 'ResultsComponent',
  components: { ChartComponent, ChipComponent },
  props: ['data', 'images'],
  computed: {
  },
}
</script>

<style scoped>
  .image-container {
    height: auto;
  }
  .image-container img {
    height: 15em;
  }
  .feature-container {
    margin-left: 3em;
    display: flex;
    justify-content: left;
    align-items: left;
    flex-wrap: wrap;
  }
  .feature-container h3 {
    width:100%;
    text-align: left;
    margin-top: 1em;
    margin-bottom: 0.5em;
  }
</style>
