<template>
  <div class="page">
    <header class="page-header">
      <h1 class="page-title">Lesson Plans</h1>
      <p class="page-subtitle">Select a class to explore subjects and chapters</p>
    </header>

    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Loading classes…</p>
    </div>

    <div v-else-if="error" class="error-box">
      <p>{{ error }}</p>
      <button @click="fetchClasses">Retry</button>
    </div>

    <div v-else class="grid">
      <div
        v-for="cls in classes"
        :key="cls.id"
        class="card class-card"
        :style="{ background: classGradient(cls.id) }"
        @click="router.push(`/class/${cls.id}`)"
      >
        <span class="class-number">{{ classNumber(cls.name) }}</span>
        <span class="class-label">{{ cls.name }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api.js'

const router = useRouter()
const classes = ref([])
const loading = ref(true)
const error = ref(null)

const gradients = [
  'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
  'linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)',
]

function classGradient(id) {
  return gradients[(id - 1) % gradients.length]
}

function classNumber(name) {
  const match = name.match(/\d+/)
  return match ? match[0] : name.charAt(0)
}

async function fetchClasses() {
  loading.value = true
  error.value = null
  try {
    const res = await api.get('/api/public/classes')
    classes.value = res.data
  } catch (e) {
    error.value = e.response?.data?.detail || e.message || 'Failed to load classes'
  } finally {
    loading.value = false
  }
}

onMounted(fetchClasses)
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f8f9fc;
  padding: 2rem 1.5rem;
  font-family: system-ui, -apple-system, sans-serif;
}

.page-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.page-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #1e1b4b;
  margin: 0 0 0.5rem;
}

.page-subtitle {
  color: #6b7280;
  font-size: 1.1rem;
  margin: 0;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 1.5rem;
  max-width: 900px;
  margin: 0 auto;
}

.card {
  border-radius: 16px;
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
}

.card:hover {
  transform: translateY(-4px) scale(1.02);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
}

.class-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2.5rem 1.5rem;
  color: white;
  text-align: center;
}

.class-number {
  font-size: 4rem;
  font-weight: 900;
  line-height: 1;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

.class-label {
  font-size: 1.1rem;
  font-weight: 600;
  margin-top: 0.5rem;
  opacity: 0.92;
  letter-spacing: 0.04em;
}

.loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  color: #6b7280;
  gap: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e5e7eb;
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-box {
  text-align: center;
  padding: 2rem;
  color: #dc2626;
}

.error-box button {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
}

@media (max-width: 600px) {
  .page-title { font-size: 1.8rem; }
  .grid { grid-template-columns: repeat(2, 1fr); gap: 1rem; }
  .class-number { font-size: 3rem; }
}
</style>
