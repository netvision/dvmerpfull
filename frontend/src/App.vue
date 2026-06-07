<template>
  <div>
    <header v-if="!route.meta.hideNav" class="site-header">
      <div class="header-strip">
        <span>Station Road, Chirawa, Rajasthan</span>
        <span>+91 1596 220602</span>
      </div>
      <nav class="main-nav">
        <RouterLink to="/" class="nav-brand">
          <img src="/dvm-logo.png" alt="DVM Logo" class="nav-logo" />
          <div>
            <span class="brand-name">Dalmia Vidya Mandir</span>
            <span class="brand-sub">Lesson Plans</span>
          </div>
        </RouterLink>
        <div class="nav-links">
          <RouterLink v-if="!auth.isLoggedIn" to="/login" class="nav-link">Teacher Login</RouterLink>
          <RouterLink v-if="auth.isLoggedIn" to="/portal" class="nav-link nav-link--portal">Portal</RouterLink>
          <a v-if="auth.isLoggedIn" href="https://lessons.dvmchirawa.ac.in" target="_blank" class="nav-link">Public Site</a>
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
.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid var(--dvm-line);
  box-shadow: 0 8px 22px rgba(23, 32, 51, 0.06);
}

.header-strip {
  background: var(--dvm-navy);
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.75rem;
  padding: 0.35rem 1.75rem;
  display: flex;
  gap: 1.5rem;
  justify-content: flex-end;
}

.main-nav {
  background: #fff;
  padding: 0 1.75rem;
  min-height: 68px;
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
  width: 42px;
  height: 42px;
  object-fit: contain;
  background: var(--dvm-navy);
  border-radius: 8px;
  padding: 4px;
}

.brand-name,
.brand-sub {
  display: block;
}

.brand-name {
  font-size: 1.08rem;
  font-weight: 850;
  color: var(--dvm-navy);
}

.brand-sub {
  margin-top: 0.12rem;
  font-size: 0.7rem;
  font-weight: 750;
  color: var(--dvm-blue);
  text-transform: uppercase;
  letter-spacing: 0.07em;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.nav-link {
  font-size: 0.88rem;
  font-weight: 750;
  color: var(--dvm-text);
  text-decoration: none;
  padding: 0.48rem 0.8rem;
  border-radius: 7px;
  transition: color 0.15s, background 0.15s;
}

.nav-link:hover {
  color: var(--dvm-navy);
  background: var(--dvm-blue-soft);
}

.nav-link--portal {
  background: var(--dvm-gold);
  color: #1f2937;
}

.nav-link--portal:hover {
  background: var(--dvm-gold-hover);
  color: #fff;
}

@media (max-width: 700px) {
  .header-strip {
    display: none;
  }

  .main-nav {
    padding: 0.75rem 1rem;
    gap: 1rem;
  }

  .brand-sub {
    display: none;
  }

  .nav-link {
    padding: 0.45rem 0.55rem;
    font-size: 0.82rem;
  }
}
</style>
