import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import ProfileView from '../views/ProfileView.vue'
import WritingView from '../views/WritingView.vue'
import PublishView from '../views/PublishView.vue'
import RegisterView from '../views/RegisterView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/users/:username',
    name: 'user',
    component: ProfileView
  },
  {
    path: '/users/:username/:id',
    name: 'writing',
    component: WritingView
  }, 
  {
    path: '/register',
    name: 'register',
    component: RegisterView
  },
  {
    path: '/publish',
    name: 'publish',
    component: PublishView
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
