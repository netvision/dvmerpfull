<template>
  <div>
    <nav class="top-nav" v-if="!route.meta.hideNav">
      <RouterLink to="/" class="nav-brand">📚 Lesson Plans</RouterLink>
      <RouterLink to="/login" class="nav-login" v-if="!auth.isLoggedIn">Teacher Login</RouterLink>
      <RouterLink to="/portal" class="nav-portal" v-if="auth.isLoggedIn">Portal</RouterLink>
    </nav>
    <RouterView />
  </div>
</template>
<script setup>
import { useRoute } from 'vue-router'
import { useAuthStore } from './stores/auth'
const route = useRoute()
const auth = useAuthStore()
</script>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f9fafb; color: #1f2937; }
.top-nav { background: white; border-bottom: 1px solid #e5e7eb; padding: 12px 24px; display: flex; align-items: center; gap: 16px; position: sticky; top: 0; z-index: 100; }
.nav-brand { font-weight: 700; font-size: 18px; color: #4f46e5; text-decoration: none; }
.nav-login, .nav-portal { margin-left: auto; color: #4f46e5; text-decoration: none; font-size: 14px; font-weight: 500; }
</style>
