<template>
  <button @click="onClick">
    {{ title }}
    <img :src="icon" :alt="title">
    <p><slot></slot></p>
  </button>
</template>

<script>
export default {
  name: 'HomeButton',
  props: { onClick: Function, icon: String, title: String},
}

</script>
