<template>
  <main class="chapter-list-page dvm-page">
    <section class="list-header">
      <div class="dvm-container">
        <nav class="breadcrumb" aria-label="Breadcrumb">
          <button type="button" @click="router.push('/')">Home</button>
          <span>/</span>
          <button type="button" @click="router.push(`/class/${classId}`)">{{ className || `Class ${classId}` }}</button>
          <span>/</span>
          <span>{{ subjectName || 'Chapters' }}</span>
        </nav>
        <div class="header-title-row">
          <span v-if="subjectIcon" class="subject-icon">{{ subjectIcon }}</span>
          <div>
            <h1>{{ subjectName || 'Chapters' }}</h1>
            <p>Scan chapters, session counts, concepts, and attached PDFs.</p>
          </div>
        </div>
      </div>
    </section>

    <section class="dvm-container content">
      <LoadingSpinner v-if="loading" message="Loading chapters..." />

      <div v-else-if="error" class="dvm-error">
        <ErrorBanner :message="error" />
        <button class="dvm-btn dvm-btn--navy retry-btn" @click="fetchChapters">Retry</button>
      </div>

      <template v-else>
        <div class="dvm-card chapter-toolbar">
          <input v-model="chapterQuery" type="search" placeholder="Filter chapters..." aria-label="Filter chapters" />
          <span class="dvm-badge">{{ filteredChapters.length }} chapter{{ filteredChapters.length !== 1 ? 's' : '' }}</span>
        </div>

        <div v-if="filteredChapters.length === 0" class="dvm-empty">
          No chapters found for this subject.
        </div>

        <div v-else class="chapter-list">
          <article
            v-for="chapter in filteredChapters"
            :key="chapter.id"
            class="chapter-card"
            :style="{ '--accent': subjectColor }"
            @click="router.push(`/chapter/${chapter.id}`)"
          >
            <span class="accent-bar"></span>
            <div class="chapter-card-top">
              <h2>{{ chapter.title }}</h2>
              <span class="dvm-badge">{{ chapter.concept_count }} concept{{ chapter.concept_count !== 1 ? 's' : '' }}</span>
            </div>
            <div class="chapter-main">
              <div v-if="chapter.aim" class="chapter-aim ql-content" v-html="sanitize(chapter.aim)"></div>
              <div class="badges">
                <span class="dvm-badge">{{ chapter.sessions_total }} sessions</span>
                <a
                  v-if="chapter.pdf_url"
                  :href="`${apiBase}${chapter.pdf_url}`"
                  target="_blank"
                  rel="noopener"
                  class="dvm-badge pdf-badge"
                  @click.stop
                >PDF</a>
              </div>
            </div>
          </article>
        </div>
      </template>
    </section>
  </main>
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
const chapterQuery = ref('')

const filteredChapters = computed(() => {
  const q = chapterQuery.value.trim().toLowerCase()
  if (!q) return chapters.value
  return chapters.value.filter(chapter => {
    return [chapter.title, chapter.aim].some(value => String(value || '').toLowerCase().includes(q))
  })
})

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
.list-header {
  background: #fff;
  border-bottom: 1px solid var(--dvm-line);
  padding: 1.4rem 0;
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

.header-title-row {
  display: flex;
  align-items: center;
  gap: 0.8rem;
}

.subject-icon {
  width: 48px;
  height: 48px;
  border-radius: 10px;
  display: grid;
  place-items: center;
  background: var(--dvm-blue-soft);
  font-size: 1.5rem;
}

.header-title-row h1 {
  margin: 0;
  color: var(--dvm-navy);
  font-size: clamp(1.6rem, 3vw, 2.2rem);
  line-height: 1.1;
}

.header-title-row p {
  margin: 0.4rem 0 0;
  color: var(--dvm-muted);
}

.content {
  padding: 1.25rem 0 4rem;
}

.chapter-toolbar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
  padding: 0.75rem;
}

.chapter-toolbar input {
  flex: 1;
  min-width: 0;
  border: 1px solid var(--dvm-line);
  border-radius: var(--dvm-radius);
  padding: 0.65rem 0.75rem;
  outline: none;
}

.chapter-toolbar input:focus {
  border-color: var(--dvm-blue);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.chapter-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1rem;
}

.chapter-card {
  position: relative;
  overflow: hidden;
  display: grid;
  gap: 0.75rem;
  background: #fff;
  border: 1px solid var(--dvm-line);
  border-radius: var(--dvm-radius-lg);
  box-shadow: var(--dvm-shadow-soft);
  padding: 1.05rem 1.15rem 1.05rem 1.35rem;
  cursor: pointer;
  transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
}

.chapter-card:hover {
  transform: translateY(-2px);
  border-color: var(--accent);
  box-shadow: var(--dvm-shadow);
}

.accent-bar {
  position: absolute;
  inset: 0 auto 0 0;
  width: 4px;
  background: var(--accent);
}

.chapter-card-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 0.8rem;
}

.chapter-card-top h2 {
  margin: 0;
  color: var(--dvm-text);
  font-size: 1.12rem;
  line-height: 1.3;
}

.chapter-aim {
  display: -webkit-box;
  color: var(--dvm-muted);
  font-size: 0.86rem;
  line-height: 1.45;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.chapter-aim :deep(p) {
  display: inline;
  margin: 0;
}

.badges {
  display: flex;
  flex-wrap: wrap;
  gap: 0.45rem;
  margin-top: 0.65rem;
}

.pdf-badge {
  text-decoration: none;
  background: #fff7ed;
  color: #9a3412;
}

.retry-btn {
  margin-top: 0.75rem;
}

@media (max-width: 700px) {
  .header-title-row {
    align-items: flex-start;
  }

  .chapter-toolbar,
  .chapter-card {
    align-items: stretch;
  }

  .chapter-list {
    grid-template-columns: 1fr;
  }

  .chapter-card-top {
    flex-direction: column;
  }
}
</style>
