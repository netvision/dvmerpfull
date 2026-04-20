<template>
  <div class="page">
    <!-- Page Header -->
    <div class="page-header" :style="{ '--accent': subjectColor }">
      <div class="header-inner">
        <nav class="breadcrumb">
          <span class="crumb crumb-link" @click="router.push('/')">Home</span>
          <span class="crumb-sep">›</span>
          <span class="crumb crumb-link" @click="router.push(`/class/${classId}`)">
            {{ className || `Class ${classId}` }}
          </span>
          <span class="crumb-sep">›</span>
          <span class="crumb">{{ subjectName || 'Chapters' }}</span>
        </nav>
        <div class="header-title-row">
          <span v-if="subjectIcon" class="header-icon">{{ subjectIcon }}</span>
          <h1 class="header-title">{{ subjectName || 'Chapters' }}</h1>
        </div>
      </div>
    </div>

    <!-- Chapter List -->
    <div class="content">
      <LoadingSpinner v-if="loading" message="Loading chapters…" />

      <div v-else-if="error" class="error-box">
        <ErrorBanner :message="error" />
        <button class="retry-btn" @click="fetchChapters">Retry</button>
      </div>

      <div v-else-if="chapters.length === 0" class="empty">
        <p>No chapters found for this subject.</p>
      </div>

      <div v-else class="chapter-list">
        <div
          v-for="chapter in chapters"
          :key="chapter.id"
          class="chapter-card"
          :style="{ '--accent': subjectColor }"
          @click="router.push(`/chapter/${chapter.id}`)"
        >
          <div class="accent-bar"></div>
          <div class="card-body">
            <h2 class="chapter-title">{{ chapter.title }}</h2>
            <div v-if="chapter.aim" class="chapter-aim ql-content" v-html="sanitize(chapter.aim)"></div>
            <div class="card-footer">
              <div class="badges">
                <span class="badge badge-sessions">⏱ {{ chapter.sessions_total }} sessions</span>
                <span class="badge badge-concepts">💡 {{ chapter.concept_count }} concept{{ chapter.concept_count !== 1 ? 's' : '' }}</span>
                <a
                  v-if="chapter.pdf_url"
                  :href="`${apiBase}${chapter.pdf_url}`"
                  target="_blank"
                  rel="noopener"
                  class="badge badge-pdf"
                  @click.stop
                >📄 PDF</a>
              </div>
              <span class="view-link">View →</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import DOMPurify from 'dompurify'
import api from '../api.js'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import ErrorBanner from '../components/ErrorBanner.vue'

const sanitize = (html) => DOMPurify.sanitize(html || '')

const router = useRouter()
const route = useRoute()

const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const classId = computed(() => route.params.classId)
const subjectId = computed(() => route.params.subjectId)

const chapters = ref([])
const loading = ref(true)
const error = ref(null)
const subjectName = ref('')
const subjectIcon = ref('')
const subjectColor = ref('#2563eb')
const className = ref('')

async function fetchChapters() {
  loading.value = true
  error.value = null
  try {
    const res = await api.get(`/api/public/subjects/${subjectId.value}/chapters`)
    chapters.value = res.data
    await fetchSubjectInfo()
  } catch (e) {
    error.value = e.response?.data?.detail || e.message || 'Failed to load chapters'
  } finally {
    loading.value = false
  }
}

async function fetchSubjectInfo() {
  try {
    const res = await api.get(`/api/public/classes/${classId.value}/subjects`)
    const subject = res.data.find(s => String(s.id) === String(subjectId.value))
    if (subject) {
      subjectName.value = subject.name
      subjectIcon.value = subject.icon || ''
      subjectColor.value = subject.color || '#2563eb'
    }
    // Also get class name
    const classRes = await api.get('/api/public/classes')
    const cls = classRes.data.find(c => String(c.id) === String(classId.value))
    if (cls) className.value = cls.name
  } catch {
    // non-critical
  }
}

onMounted(fetchChapters)
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f0f4ff;
  font-family: system-ui, -apple-system, sans-serif;
  padding-bottom: 4rem;
}

/* Page Header */
.page-header {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 1.75rem 1.5rem 1.5rem;
}

.header-inner {
  max-width: 860px;
  margin: 0 auto;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.78rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #6b7280;
  margin-bottom: 0.9rem;
}

.crumb-link {
  cursor: pointer;
  color: #2563eb;
}

.crumb-link:hover {
  text-decoration: underline;
  text-underline-offset: 2px;
}

.crumb-sep {
  color: #d1d5db;
}

.header-title-row {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.header-icon {
  font-size: 2.2rem;
  line-height: 1;
}

.header-title {
  font-size: 1.8rem;
  font-weight: 900;
  color: #1e1b4b;
  margin: 0;
  letter-spacing: -0.01em;
  border-left: 4px solid var(--accent, #2563eb);
  padding-left: 0.75rem;
}

/* Content */
.content {
  max-width: 860px;
  margin: 0 auto;
  padding: 2rem 1.5rem 0;
}

/* Chapter List */
.chapter-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.chapter-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  display: flex;
  flex-direction: row;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.07);
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.chapter-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.14);
}

.accent-bar {
  width: 4px;
  flex-shrink: 0;
  background: var(--accent, #2563eb);
  transition: background 0.2s ease;
}

.chapter-card:hover .accent-bar {
  background: color-mix(in srgb, var(--accent, #2563eb) 70%, black);
}

.card-body {
  flex: 1;
  padding: 1.4rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.chapter-title {
  font-size: 1.1rem;
  font-weight: 800;
  color: #1e1b4b;
  margin: 0;
  line-height: 1.3;
}

.chapter-aim {
  font-size: 0.9rem;
  color: #6b7280;
  margin: 0;
  line-height: 1.55;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.chapter-aim :deep(p) { margin: 0; display: inline; }
.chapter-aim :deep(ul), .chapter-aim :deep(ol) { margin: 0; padding: 0; list-style: none; display: inline; }
.chapter-aim :deep(li) { display: inline; }
.chapter-aim :deep(li::before) { content: '· '; }
.chapter-aim :deep(strong) { font-weight: 600; }
.chapter-aim :deep(em) { font-style: italic; }

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 0.3rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.badges {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  padding: 0.22rem 0.7rem;
  border-radius: 20px;
  font-size: 0.78rem;
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

.badge-pdf {
  background: #fff7ed;
  color: #9a3412;
  text-decoration: none;
  cursor: pointer;
}
.badge-pdf:hover {
  background: #fed7aa;
}

.view-link {
  font-size: 0.85rem;
  font-weight: 700;
  color: #2563eb;
  transition: color 0.2s ease;
}

.chapter-card:hover .view-link {
  color: #1d4ed8;
}

/* Error / Empty */
.error-box {
  text-align: center;
  padding: 2rem;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background: #2563eb;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-family: inherit;
  transition: background 0.2s ease;
}

.retry-btn:hover {
  background: #1d4ed8;
}

.empty {
  text-align: center;
  color: #9ca3af;
  padding: 3rem;
  font-size: 1.1rem;
}

@media (max-width: 640px) {
  .page-header { padding: 1.25rem 1rem 1.25rem; }
  .header-title { font-size: 1.4rem; }
  .content { padding: 1.5rem 1rem 0; }
  .card-body { padding: 1.1rem 1.1rem; }
  .chapter-title { font-size: 1rem; }
}
</style>
