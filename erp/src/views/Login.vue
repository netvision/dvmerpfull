<template>
  <div class="login-page">
    <form class="card" @submit.prevent="submit">
      <h1>ERP Login</h1>
      <input v-model="email" type="email" placeholder="Email" required />
      <input v-model="password" type="password" placeholder="Password" required />
      <button :disabled="loading">{{ loading ? 'Signing in...' : 'Sign in' }}</button>
      <p class="error" v-if="error">{{ error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

const submit = async () => {
  error.value = ''
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    router.push('/students')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page { min-height: 100vh; display: grid; place-items: center; background: linear-gradient(120deg, #0f172a, #1e293b); }
.card { width: 360px; background: #fff; border-radius: 12px; padding: 1.2rem; display: flex; flex-direction: column; gap: 0.7rem; }
input, button { padding: 0.7rem; border-radius: 8px; border: 1px solid #d1d5db; }
button { border: 0; background: #0ea5e9; color: #fff; font-weight: 700; cursor: pointer; }
.error { color: #b91c1c; font-size: 0.9rem; }
</style>
