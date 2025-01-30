<template>
  <nav>
    <router-link to="/">Home</router-link>
    <router-link id="h-step-3" :to="{name: 'enrolment'}">Enrolment</router-link>
    <DropDown id="h-step-4" title="Face Recognition" :items="[{title: 'Identification', routerName: 'identification'}, {title: 'Verification', routerName: 'verification'}, {title: 'Authentication', routerName: 'authentication'}]"/>
  </nav>
  <router-view/>

  <v-tour name="homeTour" :steps="steps"></v-tour>
  
</template>

<script>

import DropDown from '@/components/DropDown.vue';

export default {
  data () {
    return {
      steps: [
        {
          target: '#h-step-0',
          content: `Perform face identification. Provide an image, and the system will compare it to the database and verify if the face belongs to a specific identity on the database!`,
          params: {
            placement: 'bottom'
          }
        },
        {
          target: '#h-step-1',
          content: 'Perform face verification. Provide two images, and the system will verify if the two images belong to the same individual!',
          params: {
            placement: 'top'
          }
        },
        {
          target: '#h-step-2',
          content: 'Perform face authentication. Provide an image and an identity claim and the system will verify if the face belongs to the claimed identity!',
          params: {
            placement: 'bottom'
          }
        },
        {
          target: '#h-step-3',
          content: 'Add your identity along with images of your face to the database, or update your information!',
          params: {
            placement: 'bottom'
          }
        },
        {
          target: '#h-step-4',
          content: 'You can also navigate to the face recognition tasks on the buttons from the navigation bar! Try them out!',
          params: {
            placement: 'bottom'
          }
        },
      ]
    }
  },
  mounted: function () {
    this.$tours['homeTour'].start()
  },
  components: { DropDown },
}

</script>


<style>
:root {
  --primary-color: #2c3e50;
  --accent-color: #42b983;
  --right-color: var(--accent-color);
  --wrong-color: #e74c3c;
  --background-color: #f8f8f8;
}

body {
  margin: 0;
  padding: 0 10%;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  background-color: var(--background-color);
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: var(--primary-color);
}

nav {
  padding: 30px;
  margin-bottom: 20px;
}

nav a, nav span {
  font-weight: bold;
  color: var(--primary-color);
  text-decoration: none;
  margin: 0 10px;
  cursor: pointer;
}

nav a.router-link-exact-active {
  color: var(--accent-color);
}

p {
  padding: 20px;
  text-align: justify;
}
</style>
