import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../App.vue'
import KitchenManager from '../views/KitchenManager.vue'
import GroupManagement from '../views/GroupManagement.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage
  },
  {
    path: '/admin',
    name: 'Admin',
    component: KitchenManager
  },
  {
    path: '/group-management',
    name: 'GroupManagement',
    component: GroupManagement
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router