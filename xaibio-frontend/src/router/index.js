import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import IdentificationView from '../views/IdentificationView.vue'
import AuthenticationView from '@/views/AuthenticationView.vue'
import VerificationView from '@/views/VerificationView.vue'
import FeatureView from '@/views/FeatureView.vue'
import EnrolmentView from '@/views/EnrolmentView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/identification',
    name: 'identification',
    component: IdentificationView
  },
  {
    path: '/authentication',
    name: 'authentication',
    component: AuthenticationView
  },
  {
    path: '/verification',
    name: 'verification',
    component: VerificationView
  },
  {
    path: '/feature_extraction',
    name: 'feature_extraction',
    component: FeatureView
  },
  {
    path: '/enrolment',
    name: 'enrolment',
    component: EnrolmentView
  },
  { 
    path: '/login',
    name: 'login',
    component: LoginView
  },
  { 
    path: '/register',
    name: 'register',
    component: RegisterView
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
