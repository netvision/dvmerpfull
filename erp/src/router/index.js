import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', redirect: '/students' },
  { path: '/login', component: () => import('../views/Login.vue') },
  { path: '/students', component: () => import('../views/Students.vue'), meta: { requiresAuth: true } },
  { path: '/attendance', component: () => import('../views/Attendance.vue'), meta: { requiresAuth: true } },
  { path: '/fees', component: () => import('../views/Fees.vue'), meta: { requiresAuth: true } },
  { path: '/audit', component: () => import('../views/Audit.vue'), meta: { requiresAuth: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && auth.isLoggedIn && !auth.user) {
    try { await auth.fetchMe() } catch (_) {}
  }
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return next('/login')
  }
  next()
})

export default router
