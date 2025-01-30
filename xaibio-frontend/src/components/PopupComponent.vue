<template>
  <div class="popup">
    <p>{{message}}</p>
    <div v-if="is_custom">
      <slot></slot>
      <div><button @click="$emit('cancel')">Cancel</button> <button @click="$emit('submit')">Confirm</button></div>  
    </div>
    <button v-else @click="$emit('cancel')">OK</button>
  </div>
</template>

<script>

export default {
  name: 'PopupComponent',
  props: ['message', 'is_custom'],
  emits: ['cancel', 'submit']
}
</script>

<style>
.popup {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: white;
  padding: 10px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  z-index: 100;
  width: 500px;
}

.popup p {
  margin: 5px;
  text-align: center;
}

</style>