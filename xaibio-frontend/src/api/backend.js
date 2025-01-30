import axios from 'axios';

const backend = axios.create({
  baseURL: process.env.VUE_APP_BACKEND_SERVER ?? 'http://localhost:8000/api',
});

export default backend;