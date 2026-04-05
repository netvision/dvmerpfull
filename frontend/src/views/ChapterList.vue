<template>
  <div class="page">
    <div class="top-bar">
      <button class="back-btn" @click="router.push(`/class/${classId}`)">&#8592; Back</button>
    </div>

    <header class="page-header">
      <h1 class="page-title">{{ subjectName || 'Chapters' }}</h1>
    </header>

    <LoadingSpinner v-if="loading" message="Loading chapters…" />

    <div v-else-if="error" class="error-box">
      <ErrorBanner :message="error" />
      <button @click="fetchChapters">Retry</button>
    </div>

    <div v-else-if="chapters.length === 0" class="empty">
      <p>No chapters found for this subject.</p>
    </div>

    <div v-else class="chapter-list">
      <div
        v-for="chapter in chapters"
        :key="chapter.id"
        class="chapter-card"
        @click="router.push(`/chapter/${chapter.id}`)"
      >
        <div class="chapter-body">
          <h2 class="chapter-title">{{ chapter.title }}</h2>
          <p class="chapter-aim">{{ chapter.aim }}</p>
        </div>
        <div class="chapter-badges">
          <span class="badge badge-sessions">
            <span class="badge-icon">⏱</span> {{ chapter.sessions_total }} sessions
          </span>
          <span class="badge badge-concepts">
            <span class="badge-icon">💡</span> {{ chapter.concept_count }} concept{{ chapter.concept_count !== 1 ? 's' : '' }}
          </span>
        </div>
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
const subjectId = computed(() => route.params.subjectId)

const chapters = ref([])
const loading = ref(true)
const error = ref(null)
const subjectName = ref('')

async function fetchChapters() {
  loading.value = true
  error.value = null
  try {
    const res = await api.get(`/api/public/subjects/${subjectId.value}/chapters`)
    chapters.value = res.data
    await fetchSubjectName()
  } catch (e) {
    error.value = e.response?.data?.detail || e.message || 'Failed to load chapters'
  } finally {
    loading.value = false
  }
}

async function fetchSubjectName() {
  try {
    const res = await api.get(`/api/public/classes/${classId.value}/subjects`)
    const subject = res.data.find(s => String(s.id) === String(subjectId.value))
    if (subject) subjectName.value = subject.name
  } catch {
    // non-critical
  }
}

onMounted(fetchChapters)
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
  margin-bottom: 2rem;
}

.page-title {
  font-size: 2rem;
  font-weight: 800;
  color: #1e1b4b;
  margin: 0;
}

.chapter-list {
  max-width: 800px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chapter-card {
  background: white;
  border-radius: 12px;
  padding: 1.4rem 1.6rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  cursor: pointer;
  transition: transform 0.18s ease, box-shadow 0.18s ease;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chapter-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.14);
}

.chapter-title {
  font-size: 1.15rem;
  font-weight: 700;
  color: #1e1b4b;
  margin: 0 0 0.4rem;
}

.chapter-aim {
  font-size: 0.93rem;
  color: #6b7280;
  margin: 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.5;
}

.chapter-badges {
  display: flex;
  gap: 0.6rem;
  flex-wrap: wrap;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.25rem 0.8rem;
  border-radius: 20px;
  font-size: 0.82rem;
  font-weight: 600;
}

.badge-sessions {
  background: #ede9fe;
  color: #5b21b6;
}

.badge-concepts {
  background: #d1fae5;
  color: #065f46;
}

.badge-icon {
  font-size: 0.8rem;
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

.empty {
  text-align: center;
  color: #9ca3af;
  padding: 3rem;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .page { padding: 1.5rem 16px; }
  .page-title { font-size: 1.5rem; }
}
</style>
