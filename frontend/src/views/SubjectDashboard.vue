<template>
  <div class="page">
    <!-- Top Banner -->
    <div class="banner" :style="{ background: bannerGradient }">
      <div class="banner-inner">
        <nav class="breadcrumb">
          <span class="crumb crumb-link" @click="router.push('/')">Home</span>
          <span class="crumb-sep">›</span>
          <span class="crumb">{{ className || `Class ${classId}` }}</span>
        </nav>
        <h1 class="banner-title">{{ className || `Class ${classId}` }}</h1>
        <p class="banner-subtitle">Choose a subject to explore</p>
      </div>
    </div>

    <!-- Content -->
    <div class="content">
      <LoadingSpinner v-if="loading" message="Loading subjects…" />

      <div v-else-if="error" class="error-box">
        <ErrorBanner :message="error" />
        <button class="retry-btn" @click="fetchSubjects">Retry</button>
      </div>

      <div v-else class="grid">
        <div
          v-for="subject in subjects"
          :key="subject.id"
          class="subject-card"
          :style="{ '--top-border-color': subject.color || '#4f46e5' }"
          @click="router.push(`/class/${classId}/${subject.id}`)"
        >
          <div class="subject-icon-wrap">
            <span class="subject-icon">{{ subject.icon || '📖' }}</span>
          </div>
          <span class="subject-name">{{ subject.name }}</span>
          <span class="subject-badge">
            {{ subject.chapter_count }} chapter{{ subject.chapter_count !== 1 ? 's' : '' }}
          </span>
          <span class="subject-explore">Explore →</span>
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
const subjects = ref([])
const loading = ref(true)
const error = ref(null)
const className = ref('')

const bannerGradient = computed(() => {
  return 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)'
})

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
.page {
  min-height: 100vh;
  background: #f0f4ff;
  font-family: system-ui, -apple-system, sans-serif;
}

/* Banner */
.banner {
  padding: 3rem 2rem 2.5rem;
  color: white;
}

.banner-inner {
  max-width: 860px;
  margin: 0 auto;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.85rem;
  margin-bottom: 0.9rem;
  opacity: 0.85;
  font-weight: 500;
}

.crumb-link {
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 2px;
}

.crumb-link:hover {
  opacity: 1;
}

.crumb-sep {
  opacity: 0.6;
}

.banner-title {
  font-size: 2.4rem;
  font-weight: 900;
  margin: 0 0 0.5rem;
  letter-spacing: -0.02em;
  text-shadow: 0 2px 12px rgba(0,0,0,0.15);
}

.banner-subtitle {
  font-size: 1rem;
  margin: 0;
  opacity: 0.88;
}

/* Content */
.content {
  max-width: 860px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 4rem;
}

/* Grid */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.25rem;
}

.subject-card {
  background: white;
  border-radius: 16px;
  border-top: 4px solid var(--top-border-color, #4f46e5);
  padding: 1.75rem 1.25rem 1.25rem;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 0.4rem;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.subject-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.16);
}

.subject-icon-wrap {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: #f0f4ff;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 0.3rem;
}

.subject-icon {
  font-size: 2rem;
  line-height: 1;
}

.subject-name {
  font-size: 1.05rem;
  font-weight: 700;
  color: #1e1b4b;
  line-height: 1.3;
}

.subject-badge {
  font-size: 0.78rem;
  font-weight: 600;
  background: #eef2ff;
  color: #4f46e5;
  padding: 0.2rem 0.65rem;
  border-radius: 20px;
  margin-top: 0.15rem;
}

.subject-explore {
  font-size: 0.82rem;
  font-weight: 600;
  color: #6b7280;
  margin-top: 0.4rem;
  transition: color 0.2s ease;
}

.subject-card:hover .subject-explore {
  color: #4f46e5;
}

/* Error */
.error-box {
  text-align: center;
  padding: 2rem;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-family: inherit;
  transition: background 0.2s ease;
}

.retry-btn:hover {
  background: #4338ca;
}

@media (max-width: 640px) {
  .banner { padding: 2rem 1rem 2rem; }
  .banner-title { font-size: 1.8rem; }
  .content { padding: 2rem 1rem 3rem; }
  .grid { grid-template-columns: repeat(2, 1fr); gap: 1rem; }
}
</style>
