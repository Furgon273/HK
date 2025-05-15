import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import ProfileView from '@/views/ProfileView.vue'
import DiscussionView from '@/views/DiscussionView.vue'
import LeaderboardView from '@/views/LeaderboardView.vue'
import RunSubmissionView from '@/views/RunSubmissionView.vue'
import AdminPanel from '@/views/AdminPanel.vue'

const routes = [
  { path: '/', name: 'home', component: HomeView },
  { path: '/login', name: 'login', component: LoginView },
  { path: '/register', name: 'register', component: RegisterView },
  { path: '/profile/:username', name: 'profile', component: ProfileView },
  { path: '/discussion/:id', name: 'discussion', component: DiscussionView },
  { path: '/leaderboard', name: 'leaderboard', component: LeaderboardView },
  { 
    path: '/submit-run', 
    name: 'submit-run', 
    component: RunSubmissionView, 
    meta: { requiresAuth: true } 
  },
  {
    path: '/admin',
    component: AdminPanel,
    meta: { requiresAdmin: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export const setupRouter = (app) => {
  // Теперь мы можем использовать Pinia здесь
  const authStore = app.config.globalProperties.$authStore
  
  router.beforeEach((to, from, next) => {
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
      next('/login')
    } else {
      next()
    }
  })
  router.beforeEach((to, from, next) => {    
    if (to.meta.requiresAdmin && authStore.user?.role !== 'admin') {
      next('/')
    } else {
      next()
    }
  })
  
  return router
}

export default router