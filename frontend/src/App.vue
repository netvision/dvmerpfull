<template>
  <div>
    <header v-if="!route.meta.hideNav" class="site-header">
      <!-- Top strip -->
      <div class="header-strip">
        <span>📍 Station Road, Chirawa, Rajasthan</span>
        <span>📞 +91 1596 220602</span>
      </div>
      <!-- Main nav -->
      <nav class="main-nav">
        <RouterLink to="/" class="nav-brand">
          <img src="/dvm-logo.png" alt="DVM Logo" class="nav-logo" />
          <div>
            <span class="brand-name">Dalmia Vidya Mandir</span>
            <span class="brand-sub">Lesson Plans</span>
          </div>
        </RouterLink>
        <div class="nav-links">
          <RouterLink to="/login" class="nav-link" v-if="!auth.isLoggedIn">Teacher Login</RouterLink>
          <RouterLink to="/portal" class="nav-link nav-link--portal" v-if="auth.isLoggedIn">Portal</RouterLink>
          <a href="https://lessons.dvmchirawa.ac.in" target="_blank" class="nav-link" v-if="auth.isLoggedIn">Public Site</a>
        </div>
      </nav>
    </header>
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
body { font-family: 'Inter', 'Segoe UI', system-ui, sans-serif; background: #f8fafc; color: #374151; }

.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}

/* Top info strip — navy */
.header-strip {
  background: #1e3a8a;
  color: rgba(255,255,255,0.85);
  font-size: 0.75rem;
  padding: 0.25rem 1.5rem;
  display: flex;
  gap: 1.5rem;
  justify-content: flex-end;
}

/* Main nav bar — white */
.main-nav {
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  padding: 0 1.5rem;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  line-height: 1.15;
}

.nav-logo {
  width: 44px;
  height: 44px;
  object-fit: contain;
  /* logo is white — render on navy pill */
  background: #1e3a8a;
  border-radius: 8px;
  padding: 4px;
}

.brand-name {
  font-size: 1.1rem;
  font-weight: 800;
  color: #1e3a8a;
  letter-spacing: -0.01em;
}

.brand-sub {
  font-size: 0.72rem;
  font-weight: 600;
  color: #2563eb;
  text-transform: uppercase;
  letter-spacing: 0.07em;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.nav-link {
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
  text-decoration: none;
  padding: 0.4rem 1rem;
  border-radius: 6px;
  transition: color 0.15s, background 0.15s;
}

.nav-link:hover {
  color: #1e3a8a;
  background: #eff6ff;
}

.nav-link--portal {
  background: #eab308;
  color: #1e293b;
}

.nav-link--portal:hover {
  background: #ca8a04;
  color: #fff;
}
</style>
