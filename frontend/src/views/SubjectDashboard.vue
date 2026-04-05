<template>
  <div class="page">
    <div class="top-bar">
      <button class="back-btn" @click="router.push('/')">&#8592; Back</button>
    </div>

    <header class="page-header">
      <h1 class="page-title">{{ pageTitle }}</h1>
    </header>

    <LoadingSpinner v-if="loading" message="Loading subjects…" />

    <div v-else-if="error" class="error-box">
      <ErrorBanner :message="error" />
      <button @click="fetchSubjects">Retry</button>
    </div>

    <div v-else class="grid">
      <div
        v-for="subject in subjects"
        :key="subject.id"
        class="card subject-card"
        :style="{ background: subjectGradient(subject.color) }"
        @click="router.push(`/class/${classId}/${subject.id}`)"
      >
        <span class="subject-icon">{{ subject.icon || '📖' }}</span>
        <span class="subject-name">{{ subject.name }}</span>
        <span class="subject-meta">{{ subject.chapter_count }} chapter{{ subject.chapter_count !== 1 ? 's' : '' }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../api.js'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import ErrorBanner from '../components/ErrorBanner.vue'

const router = useRouter()
const route = useRoute()

const classId = computed(() => route.params.classId)
const subjects = ref([])
const loading = ref(true)
const error = ref(null)
const className = ref('')

const pageTitle = computed(() =>
  className.value ? `${className.value} — Subjects` : 'Subjects'
)

function subjectGradient(color) {
  if (!color) return 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)'
  // color is a hex like #e74c3c — build a shifted gradient
  return `linear-gradient(135deg, ${color} 0%, ${shiftColor(color)} 100%)`
}

function shiftColor(hex) {
  // Darken the hex color slightly for the gradient end
  const num = parseInt(hex.replace('#', ''), 16)
  const r = Math.max(0, (num >> 16) - 40)
  const g = Math.max(0, ((num >> 8) & 0xff) - 40)
  const b = Math.max(0, (num & 0xff) - 40)
  return `#${((r << 16) | (g << 8) | b).toString(16).padStart(6, '0')}`
}

async function fetchSubjects() {
  loading.value = true
  error.value = null
  try {
    const res = await api.get(`/api/public/classes/${classId.value}/subjects`)
    subjects.value = res.data
    // Try to infer className from the URL or fetch it
    await fetchClassName()
  } catch (e) {
    error.value = e.response?.data?.detail || e.message || 'Failed to load subjects'
  } finally {
    loading.value = false
  }
}

async function fetchClassName() {
  try {
    const res = await api.get('/api/public/classes')
    const cls = res.data.find(c => String(c.id) === String(classId.value))
    if (cls) className.value = cls.name
  } catch {
    // non-critical
  }
}

onMounted(fetchSubjects)
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f8f9fc;
  padding: 1.5rem 32px;
  font-family: system-ui, -apple-system, sans-serif;
}

.top-bar {
  margin-bottom: 1rem;
}

.back-btn {
  background: white;
  border: 1px solid #e5e7eb;
  padding: 0.5rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.95rem;
  color: #374151;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
  transition: background 0.15s;
}

.back-btn:hover {
  background: #f3f4f6;
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: #1e1b4b;
  margin: 0;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1.5rem;
  max-width: 1000px;
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

.subject-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 2rem 1rem;
  color: white;
  text-align: center;
  gap: 0.4rem;
}

.subject-icon {
  font-size: 2.8rem;
  line-height: 1;
}

.subject-name {
  font-size: 1.15rem;
  font-weight: 700;
  margin-top: 0.4rem;
  text-shadow: 0 1px 4px rgba(0,0,0,0.15);
}

.subject-meta {
  font-size: 0.85rem;
  opacity: 0.88;
  background: rgba(255,255,255,0.2);
  padding: 0.15rem 0.7rem;
  border-radius: 20px;
  margin-top: 0.3rem;
}

.error-box {
  text-align: center;
  padding: 2rem;
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

@media (max-width: 768px) {
  .page { padding: 1.5rem 16px; }
  .page-title { font-size: 1.5rem; }
  .grid { grid-template-columns: repeat(2, 1fr); gap: 1rem; }
}
</style>
