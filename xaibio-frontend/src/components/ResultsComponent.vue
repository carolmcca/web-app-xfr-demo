<template>
  <div>
    <h3>Your results</h3>
    <div v-if="showExplanations">
      <SelectionChipsComponent :option1="'xSSAB Explanation'" :option2="'SHAP Explanation'" @input="changeExplanation" />
    </div>
    <div class="results-container">
      <div :class="['image-container', showExplanations ? 'column' : 'row', data.prediction ? 'green' : 'red']">
        <img :src="images[0].url" />
        <font-awesome-icon :icon="icon" />
        <img v-if="showPair" :src="images[1].url" />
      </div>
      <div class="explanation-container" v-if="showExplanations">
        <xSSABComponent v-if="isSSAB" :gradPosImage="data.grad_pos" :gradNegImage="data.grad_neg" :image="data.croped_image"/>
        <ChartComponent v-else :data="data" :color="color"/> 
      </div>
    </div>
    <p v-if="!showExplanations" :class="['prediction', data.prediction ? 'green' : 'red']">{{ message }}</p>
    <button type="button" @click="toggleExplanations">{{ showExplanations ? "Hide" : "Show" }} Explanations</button>
    <div v-if="showExplanations" class="image-container row" style="width: 20%">
    </div>
  </div>
</template>

<script>
import ChartComponent from '@/components/ChartComponent.vue';
import SelectionChipsComponent from '@/components/SelectionChipsComponent.vue';
import xSSABComponent from '@/components/xSSABComponent.vue';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { faCircleCheck } from '@fortawesome/free-solid-svg-icons';
import { faCircleXmark } from '@fortawesome/free-solid-svg-icons';

export default {
  name: 'ResultsComponent',
  data() {
    return {
      showExplanations: false,
      isSSAB: true
    }
  },
  components: { ChartComponent, FontAwesomeIcon, SelectionChipsComponent, xSSABComponent },
  props: ['data', 'images', 'message', 'showPair', 'refreshExplanations'],
  computed: {
    icon() {
      return this.data.prediction ? faCircleCheck : faCircleXmark;
    },
    color() {
      const green = "#42b983"
      const red = "#e74c3c"
      return this.data.prediction ? green : red;
    },
  },
  methods: {
    toggleExplanations() {
      this.showExplanations = !this.showExplanations;
    },
    changeExplanation(isFirst) {
      this.isSSAB = isFirst;
    },
  },
}
</script>

<style>
  .explanation-container {
    width: 60%;
    height: auto;
    margin: 0;
    padding-left: 5em;
    justify-content: end;
  }
  .explanation-container img {
    width: 90%;
    height: auto;
    border-radius: 20px;
  }
  .results-container {
    margin-top: 20px;
    display: flex;
    justify-content: center;
  }
  .image-container {
    align-self: center;
    display: flex;
    align-items: center;
    justify-content: center;
    width: auto;
    height: auto;
    border-radius: 20px;
    margin: 0.5em 0;
  }
  .image-container.column {
    flex-direction: column;
    width: 20%;
  }
  .image-container.row {
    flex-direction: row;
    width: 80%;
    height: 15em;
  }
  .image-container img {
    border-radius: 20px;
    margin: 10px;
  }
  .image-container.row img {
    height: 100%;
  }
  .image-container.column img {
    width: 100%;
  }
  .image-container .svg-inline--fa {
    font-size: 4em;
    margin: 0.5em 0.5em;
  }
  .prediction {
    text-align: center;
    margin: 1em 0;
    font-weight: bold;
  }
</style>
