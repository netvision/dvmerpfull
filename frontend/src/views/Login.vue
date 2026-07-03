<template>
  <div>
    <header class="login-header">
      <a v-if="auth.isLoggedIn" href="/" class="login-home-link">Go to Lesson Home</a>
    </header>
    <div class="login-wrap">

      <!-- ── Left branding panel ── -->
      <div class="brand-panel">
        <div class="brand-deco brand-deco--tl"></div>
        <div class="brand-deco brand-deco--br"></div>
      <div class="brand-content">
        <div class="brand-logo">
          <img src="/dvm-logo.png" alt="Dalmia Vidya Mandir Logo" class="brand-logo-img" />
        </div>
        <h1 class="brand-name">Dalmia Vidya Mandir</h1>
        <p class="brand-tagline">✨ From Living Standards to Life Standards ✨</p>
        <div class="brand-divider"></div>
        <p class="brand-desc">Lesson Plan Management Platform for teachers and administrators.</p>
      </div>
    </div>

    <!-- ── Right form panel ── -->
    <div class="form-panel">
      <div class="form-card">
        <h2 class="form-title">Teacher Portal</h2>
        <p class="form-subtitle">Sign in to your account</p>

        <form class="login-form" @submit.prevent="handleLogin">
          <div class="field">
            <label for="email">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="teacher@dvmchirawa.ac.in"
              autocomplete="username"
              required
            />
          </div>
          <div class="field">
            <label for="password">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              placeholder="••••••••"
              autocomplete="current-password"
              required
            />
          </div>

          <div v-if="errorMsg" class="error-banner">
            {{ errorMsg }}
          </div>

          <button type="submit" class="login-btn" :disabled="loading">
            <span v-if="loading" class="spinner-sm"></span>
            {{ loading ? 'Signing in…' : 'Sign In' }}
          </button>
        </form>

        <p class="form-footer">
          Dalmia Vidya Mandir &mdash; Chirawa, Rajasthan
        </p>
      </div>
    </div>

  </div>
</div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref('')

onMounted(() => {
  if (auth.isLoggedIn) {
    router.replace(safeRedirectTarget())
  }
})

function safeRedirectTarget() {
  const target = typeof route.query.redirect === 'string' ? route.query.redirect : '/'
  return target.startsWith('/') && !target.startsWith('//') ? target : '/'
}

async function handleLogin() {
  errorMsg.value = ''
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    router.replace(safeRedirectTarget())
  } catch (e) {
    errorMsg.value =
      e.response?.data?.detail || 'Invalid credentials. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap {
  min-height: 100vh;
  display: flex;
  font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}

.login-header {
  background: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  padding: 0.75rem 1.5rem;
  text-align: right;
}

.login-home-link {
  color: #2563eb;
  font-weight: 700;
  text-decoration: none;
}

.login-home-link:hover {
  color: #1d4ed8;
}

/* ── Left panel ── */
.brand-panel {
  display: none;
  position: relative;
  overflow: hidden;
  background: #1e3a8a;
  color: white;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem 2.5rem;
}

@media (min-width: 768px) {
  .brand-panel { display: flex; flex: 0 0 42%; }
}

.brand-deco {
  position: absolute;
  border-radius: 50%;
  background: rgba(255,255,255,0.05);
}
.brand-deco--tl { width: 320px; height: 320px; top: -100px; left: -100px; }
.brand-deco--br { width: 260px; height: 260px; bottom: -80px; right: -80px; }

.brand-content {
  position: relative;
  z-index: 1;
  text-align: center;
}

.brand-logo {
  margin-bottom: 1.25rem;
  display: flex;
  justify-content: center;
}

.brand-logo-img {
  width: 80px;
  height: 80px;
  object-fit: contain;
}

.brand-name {
  font-size: 1.75rem;
  font-weight: 800;
  line-height: 1.2;
  margin: 0 0 0.5rem;
}

.brand-tagline {
  font-size: 0.88rem;
  color: #93c5fd;
  font-style: italic;
  margin: 0 0 1.5rem;
}

.brand-divider {
  width: 48px;
  height: 3px;
  background: #eab308;
  border-radius: 2px;
  margin: 0 auto 1.25rem;
}

.brand-desc {
  font-size: 0.9rem;
  color: rgba(255,255,255,0.7);
  line-height: 1.6;
  max-width: 280px;
  margin: 0 auto;
}

/* ── Right panel ── */
.form-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8fafc;
  padding: 2rem 1.5rem;
}

.form-card {
  background: white;
  border-radius: 16px;
  padding: 2.5rem 2rem;
  width: 100%;
  max-width: 400px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
}

.form-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: #1e3a8a;
  margin: 0 0 0.25rem;
}

.form-subtitle {
  font-size: 0.9rem;
  color: #64748b;
  margin: 0 0 2rem;
}

.login-form { text-align: left; }

.field { margin-bottom: 1.2rem; }

.field label {
  display: block;
  font-size: 0.82rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.4rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.field input {
  width: 100%;
  padding: 0.65rem 0.9rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #111827;
  outline: none;
  transition: border-color 0.15s, box-shadow 0.15s;
  box-sizing: border-box;
  font-family: inherit;
}

.field input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  border-radius: 8px;
  padding: 0.65rem 1rem;
  font-size: 0.88rem;
  margin-bottom: 1rem;
}

.login-btn {
  width: 100%;
  padding: 0.75rem;
  background: #1e3a8a;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: background 0.15s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-family: inherit;
  letter-spacing: 0.01em;
}

.login-btn:hover:not(:disabled) { background: #1d4ed8; }
.login-btn:disabled { opacity: 0.65; cursor: not-allowed; }

.spinner-sm {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.35);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}

@keyframes spin { to { transform: rotate(360deg); } }

.form-footer {
  margin-top: 1.75rem;
  text-align: center;
  font-size: 0.78rem;
  color: #94a3b8;
}
</style>
