<template>
  <div class="home">
    <h1>What is Face Recognition? </h1>
    <p>
      Face recognition is a technology that enables computers to identify and verify individuals based on their facial features. Nowadays, these systems often utilize Deep Learning models, a subset of artificial intelligence, to extract and analyze facial features from images or videos with remarkable accuracy and speed. These models learn from large datasets of labeled facial images, continuously improving their performance over time. Face recognition technology finds applications in various fields, including security, surveillance and access control.
    </p>
    <h2> Try it yourself! </h2>
    <HomeButton id="h-step-0" title="Identification" :icon="require('@/assets/identification.png')" :onClick="openIdentification" >
      Determine the identity of an individual comparing their face to those on  a database
    </HomeButton>
    <HomeButton id="h-step-1" title="Verification" :icon="require('@/assets/verification.png')" :onClick="openVerification" >
      Verify if two images belong to the same individual
    </HomeButton>
    <HomeButton id="h-step-2" title="Authentication" :icon="require('@/assets/authentication.png')" :onClick="openAuthentication" >
      Verify if a face belongs to a specific identity on the database
    </HomeButton>
  </div>
</template>

<script>
import HomeButton from '@/components/HomeButton.vue';

export default {
  name: 'HomeView',
  methods: {
    openIdentification() {
      this.$router.push({ name: 'identification' });
    },
    openVerification() {
      this.$router.push({ name: 'verification' });
    },
    openAuthentication() {
      this.$router.push({ name: 'authentication' });
    }
  },
  components: { HomeButton }
}
</script>

<style>
h1 {
  font-size: 2em;
  margin: 0;
}
h3 {
  margin: 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: var(--accent-color);
}

button {
  background-color: white;
  color: var(--primary-color);
  border: none;
  padding: 10px 20px;
  margin: 20px 20px;
  cursor: pointer;
  font-weight: bold;
  font-size: 0.9em;
  letter-spacing: 1px;
  border-radius: 40px;
}

button:hover {
  background-color: var(--accent-color);
  color: white;
}

button img {
  max-width: 200px;
  max-height: 100px;
  margin: 10px auto;
  display: block;
}

button p {
  font-size: 0.8em;
  font-weight: normal;
  max-width: 200px;
  margin: 0 auto;
  padding: 0;
  letter-spacing: normal;
}

.home button {
  padding-top: 20px;
  padding-bottom: 20px;
}

.green {
  color: var(--accent-color);
}
.red {
  color: var(--wrong-color);
}
</style>