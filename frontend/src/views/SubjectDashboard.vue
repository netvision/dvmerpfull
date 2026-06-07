<template>
  <main class="subject-page dvm-page">
    <section class="subject-header">
      <div class="dvm-container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <button type="button" @click="router.push('/')">Home</button>
          <span>/</span>
          <span>{{ className || `Class ${classId}` }}</span>
        </nav>
        <div class="header-row">
          <div>
            <h1>{{ className || `Class ${classId}` }}</h1>
            <p>Choose a subject to view chapter plans, concepts, exhibits, and resources.</p>
          </div>
          <span v-if="!loading && !error" class="dvm-badge">{{ subjects.length }} subjects</span>
        </div>
      </div>
    </section>

    <section class="dvm-container content">
      <LoadingSpinner v-if="loading" message="Loading subjects..." />

      <div v-else-if="error" class="dvm-error">
        <ErrorBanner :message="error" />
        <button class="dvm-btn dvm-btn--navy retry-btn" @click="fetchSubjects">Retry</button>
      </div>

      <div v-else-if="subjects.length === 0" class="dvm-empty">
        No subjects found for this class.
      </div>

      <div v-else class="subject-grid">
        <button
          v-for="subject in subjects"
          :key="subject.id"
          class="subject-card"
          type="button"
          :style="{ '--subject-accent': subject.color || '#2563eb' }"
          @click="router.push(`/class/${classId}/${subject.id}`)"
        >
          <span class="accent-line"></span>
          <span class="subject-icon">{{ subject.icon || '📘' }}</span>
          <span class="subject-name">{{ subject.name }}</span>
          <span class="subject-count">
            {{ subject.chapter_count }} chapter{{ subject.chapter_count !== 1 ? 's' : '' }}
          </span>
          <span class="subject-action">Explore subject</span>
        </button>
      </div>
    </section>
  </main>
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

async function fetchSubjects() {
  loading.value = true
  error.value = null
  try {
    const res = await api.get(`/api/public/classes/${classId.value}/subjects`)
    subjects.value = res.data
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
.subject-header {
  background: #fff;
  border-bottom: 1px solid var(--dvm-line);
  padding: 1.6rem 0;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  margin-bottom: 0.8rem;
  color: var(--dvm-muted);
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.breadcrumb button {
  border: 0;
  background: transparent;
  color: var(--dvm-blue);
  padding: 0;
  font: inherit;
}

.header-row {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 1rem;
}

.header-row h1 {
  margin: 0;
  color: var(--dvm-navy);
  font-size: clamp(1.75rem, 3vw, 2.35rem);
  line-height: 1.1;
}

.header-row p {
  max-width: 640px;
  margin: 0.55rem 0 0;
  color: var(--dvm-muted);
}

.content {
  padding: 1.5rem 0 4rem;
}

.subject-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(190px, 1fr));
  gap: 0.9rem;
}

.subject-card {
  position: relative;
  min-height: 172px;
  overflow: hidden;
  text-align: left;
  background: #fff;
  border: 1px solid var(--dvm-line);
  border-radius: var(--dvm-radius-lg);
  padding: 1.1rem;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  box-shadow: var(--dvm-shadow-soft);
  transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
}

.subject-card:hover {
  transform: translateY(-2px);
  border-color: var(--subject-accent);
  box-shadow: var(--dvm-shadow);
}

.accent-line {
  position: absolute;
  inset: 0 0 auto;
  height: 4px;
  background: var(--subject-accent);
}

.subject-icon {
  width: 42px;
  height: 42px;
  margin-top: 0.35rem;
  border-radius: 9px;
  display: grid;
  place-items: center;
  background: var(--dvm-blue-soft);
  font-size: 1.35rem;
}

.subject-name {
  margin-top: 0.9rem;
  color: var(--dvm-text);
  font-size: 1.02rem;
  font-weight: 850;
}

.subject-count {
  margin-top: 0.3rem;
  color: var(--dvm-muted);
  font-size: 0.82rem;
  font-weight: 700;
}

.subject-action {
  margin-top: auto;
  color: var(--dvm-blue);
  font-size: 0.82rem;
  font-weight: 800;
}

.retry-btn {
  margin-top: 0.75rem;
}

@media (max-width: 700px) {
  .header-row {
    align-items: start;
    flex-direction: column;
  }

  .subject-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
