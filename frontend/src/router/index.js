import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', component: () => import('../views/Home.vue') },
  { path: '/class/:classId', component: () => import('../views/SubjectDashboard.vue') },
  { path: '/class/:classId/:subjectId', component: () => import('../views/ChapterList.vue') },
  { path: '/chapter/:chapterId', component: () => import('../views/ChapterDetail.vue') },
  { path: '/login', component: () => import('../views/Login.vue') },
  {
    path: '/portal',
    component: () => import('../views/Portal.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/portal/chapter/:id/edit',
    component: () => import('../views/ChapterEdit.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/portal/upload',
    component: () => import('../views/Upload.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/portal/users',
    component: () => import('../views/UserManagement.vue'),
    meta: { requiresAuth: true, requiresAdmin: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return next('/login')
  }
  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return next('/portal')
  }
  next()
})

export default router
