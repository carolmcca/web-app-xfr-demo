<template>
  <ChipComponent color="blue" :selected="isFirst?'selected':''" @click="isFirst=true">{{ option1 }}</ChipComponent>
  <ChipComponent color="blue" :selected="isFirst?'':'selected'" @click="isFirst=false">{{ option2 }}</ChipComponent>
</template>

<script>
import ChipComponent from '@/components/ChipComponent.vue';

export default {
  name: 'SelectionChipsComponent',
  components: { ChipComponent },
  data() {
    return {
      isFirst: true,
    }
  },
  props: ['option1', 'option2'],
  emits: ['input'],
  watch: {
    isFirst: function() {
      this.$emit('input', this.isFirst);
    }
  }
}
</script>

<style scoped>
  .chip {
    cursor: pointer;
    margin-top: 1em;
  }

  .chip.selected {
    background-color: var(--primary-color);
    color: white;
  }

  .blue {
    color: var(--primary-color);
  }

</style>