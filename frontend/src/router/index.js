import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', component: () => import('../views/Home.vue') },
  { path: '/class/:classId', component: () => import('../views/SubjectDashboard.vue') },
  { path: '/class/:classId/:subjectId', component: () => import('../views/ChapterList.vue') },
  { path: '/chapter/:chapterId', component: () => import('../views/ChapterDetail.vue') },
  { path: '/login', component: () => import('../views/Login.vue'), meta: { hideNav: true } },
  {
    path: '/portal',
    component: () => import('../views/Portal.vue'),
    meta: { requiresAuth: true, hideNav: true }
  },
  {
    path: '/portal/chapter/:id/edit',
    component: () => import('../views/ChapterEdit.vue'),
    meta: { requiresAuth: true, hideNav: true }
  },
  {
    path: '/portal/users',
    component: () => import('../views/UserManagement.vue'),
    meta: { requiresAuth: true, requiresAdmin: true, hideNav: true }
  },
  {
    path: '/portal/subjects',
    component: () => import('../views/SubjectManagement.vue'),
    meta: { requiresAuth: true, requiresAdmin: true, hideNav: true }
  },
  {
    path: '/portal/classes',
    component: () => import('../views/ClassManagement.vue'),
    meta: { requiresAuth: true, requiresAdmin: true, hideNav: true }
  },
  {
    path: '/portal/audit',
    component: () => import('../views/AuditLogs.vue'),
    meta: { requiresAuth: true, requiresAdmin: true, hideNav: true }
  },
  {
    path: '/portal/utilities',
    component: () => import('../views/Utilities.vue'),
    meta: { requiresAuth: true, requiresSuperAdmin: true, hideNav: true }
  },
  {
    path: '/:pathMatch(.*)*',
    component: () => import('../views/NotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore()
  // If a token exists but user hasn't been fetched yet (e.g. hard refresh),
  // resolve the user before evaluating role-based guards.
  if ((to.meta.requiresAuth || to.meta.requiresAdmin || to.meta.requiresSuperAdmin) && auth.isLoggedIn && !auth.user) {
    try { await auth.fetchMe() } catch (_) {}
  }
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return next('/login')
  }
  if (to.meta.requiresAdmin && !auth.isAdmin) {
    return next('/portal')
  }
  if (to.meta.requiresSuperAdmin && !auth.isSuperAdmin) {
    return next('/portal')
  }
  next()
})

export default router
