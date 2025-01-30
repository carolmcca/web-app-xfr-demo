<template>
  <span :class="['chip', color, selected]">
    <slot></slot>
  </span>
</template>

<script>  
  export default {
    name: 'ChipComponent',
    props: ['color', 'selected']
  }
</script>

<style>
  .chip {
    display: inline-block;
    padding: 0.5em 1em;
    margin: 0.5em;
    border-radius: 20px;
    background-color: white;
  }

  .chip.selected {
    background-color: var(--primary-color);
    color: white;
  }

  .blue {
    color: var(--primary-color);
  }

  .orange {
    color: #f39c12;
  }
</style>