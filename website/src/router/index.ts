import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import { authStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/about',
    name: 'About',
    component: () => import('../views/About.vue')
  },
  {
    path: '/academics',
    name: 'Academics',
    component: () => import('../views/Academics.vue')
  },
  {
    path: '/admissions',
    name: 'Admissions',
    component: () => import('../views/Admissions.vue')
  },
  {
    path: '/facilities',
    name: 'Facilities',
    component: () => import('../views/Facilities.vue')
  },
  {
    path: '/news',
    name: 'News',
    component: () => import('../views/News.vue')
  },
  {
    path: '/news/:slug',
    name: 'NewsDetail',
    component: () => import('../views/NewsDetail.vue')
  },
  {
    path: '/events',
    name: 'Events',
    component: () => import('../views/Events.vue')
  },
  {
    path: '/events/:slug',
    name: 'EventDetail',
    component: () => import('../views/EventDetail.vue')
  },
  {
    path: '/gallery',
    name: 'Gallery',
    component: () => import('../views/Gallery.vue')
  },
  {
    path: '/inspirational-video',
    name: 'InspirationalVideo',
    component: () => import('../views/InspirationalVideo.vue')
  },
  {
    path: '/standard-of-life',
    name: 'StandardOfLife',
    component: () => import('../views/StandardOfLife.vue')
  },
  {
    path: '/conceptual-learning',
    name: 'ConceptualLearning',
    component: () => import('../views/ConceptualLearning.vue')
  },
  {
    path: '/fine-arts',
    name: 'FineArts',
    component: () => import('../views/FineArts.vue')
  },
  {
    path: '/sports-excellence',
    name: 'SportsExcellence',
    component: () => import('../views/SportsExcellence.vue')
  },
  {
    path: '/ncc',
    name: 'NCC',
    component: () => import('../views/NCC.vue')
  },
  {
    path: '/contact',
    name: 'Contact',
    component: () => import('../views/Contact.vue')
  },
  {
    path: '/mandatory-disclosure',
    name: 'MandatoryDisclosure',
    component: () => import('../views/MandatoryDisclosure.vue')
  },
  {
    path: '/transfer-certificate',
    name: 'TransferCertificate',
    component: () => import('../views/TransferCertificate.vue')
  },
  {
    path: '/grievance-redressal',
    name: 'GrievanceRedressal',
    component: () => import('../views/GrievanceRedressal.vue')
  },
  {
    path: '/annual-report',
    name: 'AnnualReport',
    component: () => import('../views/AnnualReport.vue')
  },
  {
    path: '/vision',
    name: 'Vision',
    component: () => import('../views/Vision.vue')
  },
  {
    path: '/mission',
    name: 'Mission',
    component: () => import('../views/Mission.vue')
  },
  {
    path: '/syllabus-breakup',
    name: 'SyllabusBreakup',
    component: () => import('../views/SyllabusBreakup.vue')
  },
  {
    path: '/book-list',
    name: 'BookList',
    component: () => import('../views/BookList.vue')
  },
  {
    path: '/staff',
    name: 'Staff',
    component: () => import('../views/Staff.vue')
  },
  {
    path: '/fee-structure',
    name: 'FeeStructure',
    component: () => import('../views/FeeStructure.vue')
  },
  {
    path: '/student-strength',
    name: 'StudentStrength',
    component: () => import('../views/StudentStrength.vue')
  },
  {
    path: '/smc',
    name: 'SMC',
    component: () => import('../views/SMC.vue')
  },
  // Admin Routes
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/admin/Login.vue')
  },
  {
    path: '/admin',
    component: () => import('../layouts/AdminLayout.vue'),
    meta: { requiresAuth: true, requiresAdmin: true },
    children: [
      {
        path: 'dashboard',
        name: 'AdminDashboard',
        component: () => import('../views/admin/Dashboard.vue')
      },
      {
        path: 'news',
        name: 'AdminNews',
        component: () => import('../views/admin/AdminNews.vue')
      },
      {
        path: 'events',
        name: 'AdminEvents',
        component: () => import('../views/admin/AdminEvents.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(_to, _from, savedPosition) {
    // If the user navigated with browser back/forward buttons, restore the position
    if (savedPosition) {
      return savedPosition
    }
    // For all other navigation, scroll to top
    return { top: 0, behavior: 'smooth' }
  }
})

// Navigation guard
router.beforeEach((to, _from, next) => {
  authStore.initializeFromStorage()

  if (to.meta.requiresAuth && !authStore.isAuthenticated.value) {
    next('/admin/login')
  } else if (to.meta.requiresAdmin && !authStore.isAdmin.value) {
    next('/admin/login')
  } else if (to.path === '/admin/login' && authStore.isAuthenticated.value) {
    next('/admin/dashboard')
  } else {
    next()
  }
})

export default router
