<template>
  <div class="page">
    <LoadingSpinner v-if="loading" message="Loading chapter…" />

    <div v-else-if="error" class="error-box">
      <ErrorBanner :message="error" />
      <button class="retry-btn" @click="fetchChapter">Retry</button>
    </div>

    <template v-else-if="chapter">
      <!-- A) Hero Section -->
      <div class="hero" :style="{ background: heroGradient }">
        <div class="hero-inner">
          <nav class="breadcrumb">
            <span class="crumb crumb-link" @click="router.push('/')">Home</span>
            <span class="crumb-sep">›</span>
            <span class="crumb crumb-link" @click="router.push(`/class/${chapter.class?.id}`)">
              {{ chapter.class?.name }}
            </span>
            <span class="crumb-sep">›</span>
            <span class="crumb crumb-link"
              @click="router.push(`/class/${chapter.class?.id}/${chapter.subject?.id}`)">
              {{ chapter.subject?.name }}
            </span>
          </nav>
          <h1 class="hero-title">{{ chapter.title }}</h1>
          <div v-if="chapter.aim" class="hero-aim ql-content" v-html="chapter.aim"></div>
          <div class="hero-stats">
            <span class="stat-badge">⏱ {{ totalSessions }} sessions</span>
            <span class="stat-badge">💡 {{ chapter.concepts?.length || 0 }} concepts</span>
          </div>
        </div>
      </div>

      <!-- B) Concepts Section -->
      <div class="concepts-section" v-if="chapter.concepts?.length">
        <div class="concepts-inner">
          <p class="section-eyebrow">In this chapter</p>
          <h2 class="section-heading">Concepts</h2>

          <div class="concept-list">
            <div
              v-for="concept in chapter.concepts"
              :key="concept.id"
              class="concept-card"
            >
              <!-- Card Header -->
              <div class="concept-header">
                <span class="concept-badge">{{ concept.s_no }}</span>
                <span class="concept-title">{{ concept.title }}</span>
                <span class="sessions-pill">{{ concept.sessions }} sess.</span>
              </div>

              <!-- Card Body -->
              <div class="concept-body">
                <!-- Learning Outcomes -->
                <div v-if="concept.learning_outcomes" class="concept-section">
                  <p class="field-label">Learning Outcomes</p>
                  <div class="ql-content field-content" v-html="concept.learning_outcomes"></div>
                </div>

                <!-- Extra Fields -->
                <div class="extra-fields">
                  <div v-if="concept.integration_other_sub" class="extra-field">
                    <p class="field-label">Integration with Other Subjects</p>
                    <div class="ql-content field-content" v-html="concept.integration_other_sub"></div>
                  </div>
                  <div v-if="concept.library" class="extra-field">
                    <p class="field-label">Library</p>
                    <div class="ql-content field-content" v-html="concept.library"></div>
                  </div>
                  <div v-if="concept.activity" class="extra-field">
                    <p class="field-label">Activity</p>
                    <div class="ql-content field-content" v-html="concept.activity"></div>
                  </div>
                  <div v-if="concept.life_lesson" class="extra-field">
                    <p class="field-label">Life Lesson</p>
                    <div class="ql-content field-content" v-html="concept.life_lesson"></div>
                  </div>
                  <div v-if="concept.remarks" class="extra-field">
                    <p class="field-label">Remarks</p>
                    <div class="ql-content field-content" v-html="concept.remarks"></div>
                  </div>
                </div>

                <!-- Images -->
                <div v-if="concept.images?.length" class="images-row">
                  <a
                    v-for="img in concept.images"
                    :key="img.id"
                    :href="`http://localhost:8000${img.url}`"
                    target="_blank"
                    rel="noopener"
                  >
                    <img
                      :src="`http://localhost:8000${img.url}`"
                      :alt="img.original_name"
                      class="concept-thumbnail"
                    />
                  </a>
                </div>

                <!-- View Exhibit Button -->
                <div class="concept-card-footer">
                  <button
                    class="exhibit-btn"
                    @click="openModal(concept)"
                  >
                    View Exhibit →
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- C) Exhibit Modal -->
    <transition name="modal-fade">
      <div v-if="showModal" class="modal-backdrop" @click.self="closeModal">
        <div class="modal-card" role="dialog" aria-modal="true">
          <!-- Modal Header -->
          <div class="modal-header">
            <div class="modal-header-text">
              <h3 class="modal-title">{{ modalConcept?.title }}</h3>
              <p class="modal-subtitle">Exhibit Details</p>
            </div>
            <button class="modal-close" @click="closeModal" aria-label="Close">✕</button>
          </div>

          <!-- Modal Body -->
          <div class="modal-body">
            <template v-if="modalConcept?.exhibits?.length">
              <div
                v-for="(exhibit, idx) in modalConcept.exhibits"
                :key="exhibit.id || exhibit.field_key"
                class="exhibit-entry"
              >
                <p class="exhibit-label">{{ formatFieldKey(exhibit.field_key) }}</p>
                <div class="exhibit-value">
                  <!-- YouTube embed -->
                  <template v-if="getYoutubeId(exhibit.field_value)">
                    <div class="video-wrap">
                      <iframe
                        :src="`https://www.youtube.com/embed/${getYoutubeId(exhibit.field_value)}`"
                        allowfullscreen
                        class="yt-iframe"
                      ></iframe>
                    </div>
                  </template>
                  <!-- Plain URL (not youtube) -->
                  <template v-else-if="isUrl(stripHtml(exhibit.field_value))">
                    <a
                      :href="stripHtml(exhibit.field_value).trim()"
                      target="_blank"
                      rel="noopener"
                      class="exhibit-link"
                    >{{ stripHtml(exhibit.field_value).trim() }}</a>
                  </template>
                  <!-- Rich text / HTML -->
                  <template v-else>
                    <div class="ql-content" v-html="exhibit.field_value"></div>
                  </template>
                </div>
                <hr v-if="idx < modalConcept.exhibits.length - 1" class="exhibit-divider" />
              </div>
            </template>
            <p v-else class="no-exhibit">No exhibit data available.</p>
          </div>
        </div>
      </div>
    </transition>
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

const chapterId = computed(() => route.params.chapterId)
const chapter = ref(null)
const loading = ref(true)
const error = ref(null)

// Modal state
const showModal = ref(false)
const modalConcept = ref(null)

const heroGradient = computed(() => {
  const color = chapter.value?.subject?.color
  if (!color) return 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)'
  return `linear-gradient(135deg, ${color} 0%, ${shiftColor(color)} 100%)`
})

const totalSessions = computed(() => {
  if (!chapter.value?.concepts) return 0
  return chapter.value.concepts.reduce((sum, c) => sum + (parseInt(c.sessions) || 0), 0)
})

function shiftColor(hex) {
  const num = parseInt(hex.replace('#', ''), 16)
  const r = Math.max(0, (num >> 16) - 50)
  const g = Math.max(0, ((num >> 8) & 0xff) - 50)
  const b = Math.max(0, (num & 0xff) - 50)
  return `#${((r << 16) | (g << 8) | b).toString(16).padStart(6, '0')}`
}

function formatFieldKey(key) {
  if (!key) return ''
  return key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}

function getYoutubeId(text) {
  if (!text) return null
  const m = text.trim().match(/(?:youtu\.be\/|watch\?v=|embed\/)([A-Za-z0-9_-]{11})/)
  return m ? m[1] : null
}

function isUrl(text) {
  if (!text) return false
  return /^https?:\/\//.test(text.trim())
}

function stripHtml(value) {
  if (!value) return ''
  return value.replace(/<[^>]*>/g, '').trim()
}

function openModal(concept) {
  modalConcept.value = concept
  showModal.value = true
  document.body.style.overflow = 'hidden'
}

function closeModal() {
  showModal.value = false
  modalConcept.value = null
  document.body.style.overflow = ''
}

async function fetchChapter() {
  loading.value = true
  error.value = null
  try {
    const res = await api.get(`/api/public/chapters/${chapterId.value}`)
    chapter.value = res.data
  } catch (e) {
    error.value = e.response?.data?.detail || e.message || 'Failed to load chapter'
  } finally {
    loading.value = false
  }
}

onMounted(fetchChapter)
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f0f4ff;
  font-family: system-ui, -apple-system, sans-serif;
  padding-bottom: 4rem;
}

/* Hero */
.hero {
  padding: 3rem 1.5rem 2.5rem;
  color: white;
}

.hero-inner {
  max-width: 860px;
  margin: 0 auto;
}

.breadcrumb {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  opacity: 0.82;
  margin-bottom: 1rem;
}

.crumb-link {
  cursor: pointer;
}

.crumb-link:hover {
  opacity: 1;
  text-decoration: underline;
  text-underline-offset: 2px;
}

.crumb-sep {
  opacity: 0.5;
}

.hero-title {
  font-size: 2.2rem;
  font-weight: 900;
  margin: 0 0 1rem;
  line-height: 1.2;
  text-shadow: 0 2px 12px rgba(0,0,0,0.15);
  letter-spacing: -0.02em;
}

.hero-aim {
  font-size: 1rem;
  line-height: 1.65;
  opacity: 0.92;
  margin-bottom: 1.25rem;
}

.hero-aim :deep(p) { margin: 0 0 4px; }
.hero-aim :deep(p:last-child) { margin: 0; }

.hero-stats {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.stat-badge {
  background: rgba(255, 255, 255, 0.22);
  backdrop-filter: blur(4px);
  padding: 0.3rem 0.9rem;
  border-radius: 20px;
  font-size: 0.88rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

/* Concepts Section */
.concepts-section {
  padding: 0 1.5rem;
}

.concepts-inner {
  max-width: 860px;
  margin: 0 auto;
  padding-top: 2.5rem;
}

.section-eyebrow {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #6b7280;
  margin: 0 0 0.3rem;
}

.section-heading {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1e1b4b;
  margin: 0 0 1.5rem;
}

/* Concept List */
.concept-list {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.concept-card {
  background: white;
  border-radius: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.07);
  overflow: hidden;
}

/* Concept Card Header */
.concept-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.1rem 1.5rem;
  border-bottom: 1px solid #f3f4f6;
  background: #fafafa;
}

.concept-badge {
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: white;
  background: #4f46e5;
  padding: 0.22rem 0.65rem;
  border-radius: 20px;
  flex-shrink: 0;
}

.concept-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #1e1b4b;
  flex: 1;
  line-height: 1.3;
}

.sessions-pill {
  font-size: 0.78rem;
  font-weight: 600;
  color: #5b21b6;
  background: #ede9fe;
  padding: 0.2rem 0.65rem;
  border-radius: 20px;
  flex-shrink: 0;
}

/* Concept Card Body */
.concept-body {
  padding: 1.4rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

.concept-section {
  /* wrapper for learning outcomes */
}

.extra-fields {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.extra-field {
  /* wrapper for each extra field */
}

.field-label {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #6b7280;
  margin: 0 0 0.35rem;
}

.field-content {
  font-size: 0.93rem;
  color: #374151;
  line-height: 1.65;
}

/* Images Row */
.images-row {
  display: flex;
  gap: 0.75rem;
  overflow-x: auto;
  padding-bottom: 0.25rem;
  scrollbar-width: thin;
  scrollbar-color: #c4b5fd transparent;
}

.images-row::-webkit-scrollbar {
  height: 4px;
}

.images-row::-webkit-scrollbar-thumb {
  background: #c4b5fd;
  border-radius: 4px;
}

.concept-thumbnail {
  height: 90px;
  width: auto;
  border-radius: 8px;
  object-fit: cover;
  cursor: pointer;
  flex-shrink: 0;
  transition: transform 0.2s ease;
}

.concept-thumbnail:hover {
  transform: scale(1.03);
}

/* Exhibit Button */
.concept-card-footer {
  padding-top: 0.25rem;
}

.exhibit-btn {
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 0.55rem 1.25rem;
  font-size: 0.9rem;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease;
}

.exhibit-btn:hover {
  background: #4338ca;
  transform: translateY(-1px);
}

/* Quill content styles */
.ql-content :deep(p) { margin: 0 0 6px; }
.ql-content :deep(ul), .ql-content :deep(ol) { padding-left: 20px; margin: 4px 0; }
.ql-content :deep(strong) { font-weight: 600; }
.ql-content :deep(em) { font-style: italic; }
.ql-content :deep(a) { color: #4f46e5; }
.ql-content :deep(p:last-child) { margin-bottom: 0; }

/* Modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.modal-card {
  background: white;
  border-radius: 16px;
  width: 100%;
  max-width: 640px;
  max-height: 85vh;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.modal-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.4rem 1.5rem 1.2rem;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  background: white;
  border-radius: 16px 16px 0 0;
  z-index: 1;
}

.modal-header-text {
  flex: 1;
}

.modal-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: #1e1b4b;
  margin: 0 0 0.2rem;
  line-height: 1.3;
}

.modal-subtitle {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #6b7280;
  margin: 0;
}

.modal-close {
  background: #f3f4f6;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 0.85rem;
  color: #374151;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease;
  font-family: inherit;
}

.modal-close:hover {
  background: #e5e7eb;
}

.modal-body {
  padding: 1.25rem 1.5rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.exhibit-entry {
  padding: 1rem 0;
}

.exhibit-entry:first-child {
  padding-top: 0;
}

.exhibit-label {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #6b7280;
  margin: 0 0 0.4rem;
}

.exhibit-value {
  font-size: 0.93rem;
  color: #1f2937;
  line-height: 1.6;
  word-break: break-word;
}

.exhibit-divider {
  border: none;
  border-top: 1px solid #f3f4f6;
  margin: 0;
}

.exhibit-link {
  color: #4f46e5;
  word-break: break-all;
}

.exhibit-link:hover {
  color: #4338ca;
}

/* YouTube embed */
.video-wrap {
  position: relative;
  width: 100%;
  aspect-ratio: 16/9;
  border-radius: 8px;
  overflow: hidden;
}

.yt-iframe {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  border: none;
  border-radius: 8px;
}

.no-exhibit {
  text-align: center;
  color: #9ca3af;
  font-size: 0.95rem;
  padding: 2rem 0;
  margin: 0;
}

/* Modal transition */
.modal-fade-enter-active,
.modal-fade-leave-active {
  transition: opacity 0.2s ease;
}

.modal-fade-enter-active .modal-card,
.modal-fade-leave-active .modal-card {
  transition: transform 0.2s ease;
}

.modal-fade-enter-from {
  opacity: 0;
}

.modal-fade-enter-from .modal-card {
  transform: translateY(16px) scale(0.97);
}

.modal-fade-leave-to {
  opacity: 0;
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
  .hero { padding: 2rem 1rem 2rem; }
  .hero-title { font-size: 1.6rem; }
  .concepts-section { padding: 0 1rem; }
  .concept-header { padding: 1rem 1.1rem; }
  .concept-body { padding: 1.1rem; }
  .modal-card { max-height: 90vh; }
  .modal-header { padding: 1.1rem 1.1rem 1rem; }
  .modal-body { padding: 1rem 1.1rem 1.25rem; }
}
</style>
