import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import PageOne from '../views/PageOne.vue'
import PageTwo from '../views/PageTwo.vue'

const routes = [
  {
    path: '/',
    name: 'pageOne',
    component: PageOne
  },
  {
    path: '/page-two',
    name: 'pageTwo',
    component: PageTwo
  },
  {
    path: '/home',
    name: 'home',
    component: HomePage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
