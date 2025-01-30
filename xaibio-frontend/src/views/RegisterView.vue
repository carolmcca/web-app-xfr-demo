<template>
  <div class="form-card">
    <h3>Register</h3>
    <div class="form-container">
      <div class="label-div">
        <label>username</label>
        <label>password</label>
        <label>confirm password</label>
      </div>
      <div class="input-div">
        <input type="text" v-model="username" required>
        <input type="password" v-model="password" required>
        <input type="password" v-model="confirmPassword" required>
      </div>
    </div>
    <p v-if="errorMessage!=''" class="error">{{ errorMessage }}</p>
    <p v-if="!passwordsMatch" class="error">The passwords should match</p>
    <button @click="login">Register</button>
  </div>
</template>

<script>
import backendApi from '../api/backend.js';

export default {
  data() {
    return {
      username: '',
      password: '',
      confirmPassword: '',
      errorMessage: ''
    }
  },
  computed: {
    passwordsMatch() {
      return this.password === this.confirmPassword;
    }
  },
  methods: {
    login() {
      backendApi.post('/users/register/', {username: this.username, password: this.password})
        .then((response) => {
          this.$cookies.set("jwt_token", response.data.token, "expiring time");
          this.$router.push({name: 'enrolment'});
        })
        .catch((error) => {
          console.log(error.response.data);
          this.errorMessage = error.response.data.detail;
        });
    }
  }
}
</script>

<style>
.form-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 2em 0em;
  max-width: 50em;
  margin: auto;
  margin-top: 50px;
  border-radius: 2em;
  background-color: white;
}

.form-container {
  display: flex;
  flex-direction: row;
  width: 75%;
  padding: 2em 2em 1em 2em;
}

.label-div, .input-div {
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}

.label-div {
  align-items: flex-end;
  width: fit-content;
}

.input-div {
  flex-grow: 1; 
}

.form-container input {
  margin: 2em 1em 0em 1em;
}

.form-container label {
  margin: 2em 1em 10px 1em;
}

.form-card button {
  background-color: var(--primary-color);
  color: white;
  margin-top: 2em;
}

.form-card button:hover {
  background-color: var(--accent-color);
}

.form-container h3 {
  margin-bottom: 1em;
}

.form-card .error {
  margin:0em;
}
</style>
