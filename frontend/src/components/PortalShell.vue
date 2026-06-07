<template>
  <div class="portal-shell">
    <aside class="portal-sidebar">
      <RouterLink to="/portal" class="portal-brand">
        <img src="/dvm-logo.png" alt="DVM Logo" />
        <span>Lesson Portal</span>
      </RouterLink>

      <nav class="portal-menu" aria-label="Portal navigation">
        <RouterLink
          v-for="item in visibleItems"
          :key="item.to"
          :to="item.to"
          class="portal-menu-item"
          :class="{ active: isActive(item) }"
        >
          <span class="menu-icon">{{ item.icon }}</span>
          <span>{{ item.label }}</span>
        </RouterLink>
      </nav>
    </aside>

    <div class="portal-main">
      <header class="portal-topbar">
        <div>
          <p v-if="subtitle" class="portal-subtitle">{{ subtitle }}</p>
          <h1>{{ title }}</h1>
        </div>
        <div class="portal-actions">
          <span v-if="auth.user" class="portal-user">
            <span class="user-text">
              <strong>{{ auth.user.name }}</strong>
              <small>{{ auth.user.role }}</small>
            </span>
            <span class="avatar">{{ initials }}</span>
          </span>
          <button v-if="showPassword" type="button" class="dvm-btn" @click="$emit('change-password')">
            Password
          </button>
          <button type="button" class="dvm-btn dvm-btn--danger" @click="$emit('logout')">
            Logout
          </button>
        </div>
      </header>

      <main class="portal-content">
        <slot />
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

defineEmits(['logout', 'change-password'])

defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: '' },
  showPassword: { type: Boolean, default: true },
})

const route = useRoute()
const auth = useAuthStore()

const navItems = [
  { label: 'Chapters', to: '/portal', icon: 'CH', show: () => true },
  { label: 'Classes', to: '/portal/classes', icon: 'CL', show: () => auth.isAdmin },
  { label: 'Subjects', to: '/portal/subjects', icon: 'SB', show: () => auth.isAdmin },
  { label: 'Users', to: '/portal/users', icon: 'US', show: () => auth.isAdmin },
  { label: 'Audit Logs', to: '/portal/audit', icon: 'AU', show: () => auth.isAdmin },
  { label: 'Utilities', to: '/portal/utilities', icon: 'UT', show: () => auth.isSuperAdmin },
]

const visibleItems = computed(() => navItems.filter(item => item.show()))

const initials = computed(() => {
  const name = auth.user?.name || 'User'
  return name
    .split(/\s+/)
    .filter(Boolean)
    .slice(0, 2)
    .map(part => part[0]?.toUpperCase())
    .join('') || 'U'
})

function isActive(item) {
  if (item.to === '/portal') return route.path === '/portal' || route.path.startsWith('/portal/chapter')
  return route.path.startsWith(item.to)
}
</script>

<style scoped>
.portal-shell {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 232px minmax(0, 1fr);
  background: var(--dvm-bg);
}

.portal-sidebar {
  position: sticky;
  top: 0;
  height: 100vh;
  background: var(--dvm-navy-2);
  color: #fff;
  padding: 1.1rem 0.9rem;
}

.portal-brand {
  display: flex;
  align-items: center;
  gap: 0.7rem;
  color: #fff;
  text-decoration: none;
  font-weight: 850;
  margin-bottom: 1.6rem;
}

.portal-brand img {
  width: 42px;
  height: 42px;
  object-fit: contain;
  border-radius: 8px;
  background: #fff;
  padding: 4px;
}

.portal-menu {
  display: grid;
  gap: 0.25rem;
}

.portal-menu-item {
  display: flex;
  align-items: center;
  gap: 0.65rem;
  border-radius: 7px;
  color: rgba(255,255,255,0.72);
  text-decoration: none;
  padding: 0.65rem 0.7rem;
  font-size: 0.9rem;
  font-weight: 700;
}

.portal-menu-item:hover,
.portal-menu-item.active {
  color: #fff;
  background: rgba(255,255,255,0.13);
}

.menu-icon {
  width: 26px;
  height: 26px;
  border-radius: 6px;
  display: grid;
  place-items: center;
  background: rgba(255,255,255,0.1);
  font-size: 0.64rem;
  font-weight: 900;
}

.portal-main {
  min-width: 0;
}

.portal-topbar {
  min-height: 68px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  background: #fff;
  border-bottom: 1px solid var(--dvm-line);
  padding: 0.8rem 1.5rem;
}

.portal-subtitle {
  margin: 0 0 0.1rem;
  color: var(--dvm-muted);
  font-size: 0.76rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}

.portal-topbar h1 {
  margin: 0;
  color: var(--dvm-text);
  font-size: 1.28rem;
  line-height: 1.2;
}

.portal-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 0.55rem;
}

.portal-user {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  color: var(--dvm-muted);
  font-size: 0.8rem;
}

.user-text {
  display: grid;
  text-align: right;
}

.user-text strong {
  color: var(--dvm-text);
}

.user-text small {
  color: var(--dvm-muted);
  text-transform: capitalize;
}

.avatar {
  width: 34px;
  height: 34px;
  border-radius: 999px;
  display: grid;
  place-items: center;
  background: #dbeafe;
  color: var(--dvm-navy);
  font-size: 0.78rem;
  font-weight: 900;
}

.portal-content {
  padding: 1.4rem 1.5rem 2.5rem;
}

@media (max-width: 900px) {
  .portal-shell {
    grid-template-columns: 1fr;
  }

  .portal-sidebar {
    position: static;
    height: auto;
  }

  .portal-menu {
    display: flex;
    overflow-x: auto;
    padding-bottom: 0.15rem;
  }

  .portal-menu-item {
    white-space: nowrap;
  }

  .portal-topbar {
    align-items: flex-start;
    flex-direction: column;
  }

  .portal-actions {
    width: 100%;
    justify-content: flex-start;
    flex-wrap: wrap;
  }
}
</style>
