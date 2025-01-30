<template>
  <div class="form-card">
    <h3>Login</h3>
    <div class="form-container">
      <div class="label-div">
        <label>username</label>
        <label>password</label>
      </div>
      <div class="input-div">
        <input type="text" v-model="username" required>
        <input type="password" v-model="password" required>
      </div>
    </div>
    <p v-if="errorMessage!=''" class="error">{{ errorMessage }}</p>
    <button @click="login">Login</button>
    <p class="right">Not registered yet? <router-link :to="{name: 'register'}">Sign Up</router-link></p>
  </div>
</template>

<script>
import backendApi from '../api/backend.js';

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: ''
    }
  },
  methods: {
    login() {
      backendApi.post('/token/', {username: this.username, password: this.password})
        .then(response => response.data)  
        .then(data => {
          this.$cookies.set("jwt_token", data.access, "expiring time");
          this.$router.push({name: 'enrolment'});
        })
        .catch((error) => {
          console.log(error);
          this.errorMessage = error.response.data.detail;
        });
    }
  }
}
</script>

<style>

.right {
  text-align: right;
  width: 75%;
}

</style>