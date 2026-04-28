<template>
  <div class="erp-shell">
    <header class="topbar" v-if="auth.isLoggedIn">
      <div class="brand">DVM ERP</div>
      <nav class="tabs">
        <RouterLink to="/students">Students</RouterLink>
        <RouterLink to="/attendance">Attendance</RouterLink>
        <RouterLink to="/fees">Fees</RouterLink>
        <RouterLink to="/audit">Audit</RouterLink>
      </nav>
      <div class="actions">
        <span class="user" v-if="auth.user">{{ auth.user.name }} ({{ auth.user.role }})</span>
        <button @click="logout">Logout</button>
      </div>
    </header>
    <RouterView />
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'

const router = useRouter()
const auth = useAuthStore()

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.erp-shell { min-height: 100vh; background: #f8fafc; color: #1f2937; }
.topbar { height: 58px; background: #0f172a; color: #fff; display: flex; align-items: center; justify-content: space-between; padding: 0 1rem; }
.brand { font-weight: 800; letter-spacing: 0.03em; }
.tabs { display: flex; gap: 1rem; }
.tabs a { color: #cbd5e1; text-decoration: none; font-weight: 600; }
.tabs a.router-link-active { color: #22d3ee; }
.actions { display: flex; align-items: center; gap: 0.7rem; }
.actions button { background: #ef4444; color: #fff; border: 0; border-radius: 6px; padding: 0.35rem 0.7rem; cursor: pointer; }
.user { font-size: 0.85rem; color: #e2e8f0; }
</style>
