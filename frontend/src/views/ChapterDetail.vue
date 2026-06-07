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
          <div v-if="chapter.aim" class="hero-aim ql-content" v-html="sanitize(chapter.aim)"></div>
          <div class="hero-stats">
            <span class="stat-badge">⏱ {{ totalSessions }} sessions</span>
            <span class="stat-badge">💡 {{ chapter.concepts?.length || 0 }} concepts</span>
          </div>
          <a
            v-if="chapter.pdf_url"
            :href="buildAssetUrl(chapter.pdf_url)"
            target="_blank"
            rel="noopener"
            class="pdf-download-btn"
            @click.stop
          >
            📄 Download Chapter PDF
          </a>
        </div>
      </div>

      <!-- B) Concepts Section -->
      <div class="concepts-section" v-if="chapter.concepts?.length">
        <div class="concepts-inner">
          <p class="section-eyebrow">In this chapter</p>
          <h2 class="section-heading">Concepts</h2>

          <div class="concept-list">
            <div
              v-for="(concept, idx) in chapter.concepts"
              :key="concept.id"
              class="concept-card"
              :style="{ '--accent': accentColor }"
            >
              <!-- Ghost watermark number -->
              <div class="card-watermark" aria-hidden="true">{{ concept.s_no }}</div>

              <!-- Card Header -->
              <div class="concept-header">
                <div class="concept-badge">{{ concept.s_no }}</div>
                <div class="concept-header-text">
                  <h3 class="concept-title">{{ concept.title }}</h3>
                </div>
                <div v-if="concept.sessions" class="sessions-pill">
                  <span class="sessions-dot"></span>
                  {{ concept.sessions }} sess.
                </div>
              </div>

              <!-- Card Body -->
              <div class="concept-body">
                <div v-if="concept.concept_description" class="extra-field concept-description-field">
                  <p class="field-label">📖 Concept Description</p>
                  <div class="ql-content field-content" v-html="sanitize(concept.concept_description)"></div>
                </div>

                <!-- Learning Outcomes callout -->
                <div v-if="concept.learning_outcomes" class="lo-callout">
                  <p class="lo-label">🎯 Learning Outcomes</p>
                  <div class="ql-content lo-content" v-html="sanitize(concept.learning_outcomes)"></div>
                </div>

                <!-- Extra Fields -->
                <div v-if="concept.integration_other_sub || concept.library || concept.activity || concept.life_lesson || concept.remarks" class="extra-fields">
                  <div v-if="concept.integration_other_sub" class="extra-field">
                    <p class="field-label">🔗 Integration with Other Subjects</p>
                    <div class="ql-content field-content" v-html="sanitize(concept.integration_other_sub)"></div>
                  </div>
                  <div v-if="concept.library" class="extra-field">
                    <p class="field-label">📚 Library</p>
                    <div class="ql-content field-content" v-html="sanitize(concept.library)"></div>
                  </div>
                  <div v-if="concept.activity" class="extra-field">
                    <p class="field-label">✏️ Activity</p>
                    <div class="ql-content field-content" v-html="sanitize(concept.activity)"></div>
                  </div>
                  <div v-if="concept.life_lesson" class="extra-field">
                    <p class="field-label">💡 Life Lesson</p>
                    <div class="ql-content field-content" v-html="sanitize(concept.life_lesson)"></div>
                  </div>
                  <div v-if="concept.remarks" class="extra-field">
                    <p class="field-label">📝 Remarks</p>
                    <div class="ql-content field-content" v-html="sanitize(concept.remarks)"></div>
                  </div>
                </div>

                <!-- Images -->
                <div v-if="concept.images?.length" class="images-row">
                  <a
                    v-for="img in concept.images"
                    :key="img.id"
                    :href="buildAssetUrl(img.url)"
                    target="_blank"
                    rel="noopener"
                    class="thumb-link"
                  >
                    <img
                      :src="buildAssetUrl(img.url)"
                      :alt="img.original_name"
                      class="concept-thumbnail"
                    />
                  </a>
                </div>

                <!-- Exhibit Button -->
                <div class="concept-card-footer">
                  <button class="exhibit-btn" @click="openModal(concept)">
                    <span>View Exhibit</span>
                    <span class="btn-arrow">→</span>
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
      <div v-if="showModal" class="modal-backdrop">
        <div class="modal-card" role="dialog" aria-modal="true" :style="{ '--accent': accentColor }">
          <!-- Modal Header -->
          <div class="modal-header">
            <div class="modal-header-icon" aria-hidden="true">📋</div>
            <div class="modal-header-text">
              <p class="modal-subtitle">Exhibit Details</p>
              <h3 class="modal-title">{{ modalConcept?.title }}</h3>
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
                <div class="exhibit-header">
                  <div class="exhibit-label-row">
                    <span class="exhibit-index">{{ idx + 1 }}</span>
                    <p class="exhibit-label">{{ formatFieldKey(exhibit.field_key) }}</p>
                  </div>
                </div>
                
                <div class="exhibit-value">
                  <!-- String type -->
                  <template v-if="exhibit.field_type === 'string'">
                    <div class="ql-content" v-html="sanitize(exhibit.field_value)"></div>
                  </template>

                  <!-- Link type -->
                  <template v-else-if="exhibit.field_type === 'link'">
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
                    <!-- Other URLs as links -->
                    <template v-else>
                      <a
                        :href="exhibit.field_value"
                        target="_blank"
                        rel="noopener"
                        class="exhibit-link"
                      >{{ exhibit.field_value }}</a>
                    </template>
                  </template>

                  <!-- Image type -->
                  <template v-else-if="exhibit.field_type === 'image'">
                    <div class="media-container image-container">
                      <img 
                        :src="buildAssetUrl(exhibit.file_url)"
                        :alt="exhibit.field_key"
                        class="exhibit-image"
                      />
                    </div>
                  </template>

                  <!-- Audio type -->
                  <template v-else-if="exhibit.field_type === 'audio'">
                    <div class="media-container audio-container">
                      <audio controls class="exhibit-audio">
                        <source :src="buildAssetUrl(exhibit.file_url)" />
                        Your browser does not support the audio element.
                      </audio>
                    </div>
                  </template>

                  <!-- Video type -->
                  <template v-else-if="exhibit.field_type === 'video'">
                    <div class="media-container video-container">
                      <video controls class="exhibit-video">
                        <source :src="buildAssetUrl(exhibit.file_url)" />
                        Your browser does not support the video element.
                      </video>
                    </div>
                  </template>

                  <!-- Fallback for old format (legacy field_value rendering) -->
                  <template v-else>
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
                    <!-- Plain URL -->
                    <template v-else-if="isUrl(stripHtml(exhibit.field_value))">
                      <a
                        :href="stripHtml(exhibit.field_value).trim()"
                        target="_blank"
                        rel="noopener"
                        class="exhibit-link"
                      >{{ stripHtml(exhibit.field_value).trim() }}</a>
                    </template>
                    <!-- Rich text -->
                    <template v-else>
                      <div class="ql-content" v-html="sanitize(exhibit.field_value)"></div>
                    </template>
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
import DOMPurify from 'dompurify'
import api from '../api.js'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import ErrorBanner from '../components/ErrorBanner.vue'

const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const sanitize = (html) => DOMPurify.sanitize(html || '')

function buildAssetUrl(path) {
  if (!path) return ''
  return encodeURI(`${apiBase}${path}`)
}

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
  if (!color) return 'linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%)'
  return `linear-gradient(135deg, ${color} 0%, ${shiftColor(color)} 100%)`
})

const accentColor = computed(() => chapter.value?.subject?.color || '#2563eb')

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
  background: var(--dvm-bg);
  font-family: var(--dvm-font);
  padding-bottom: 4rem;
}

.hero {
  background: #fff !important;
  border-bottom: 1px solid var(--dvm-line);
  color: var(--dvm-text);
  padding: 1.5rem 1rem;
}

.hero-inner {
  width: min(960px, 100%);
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
  color: var(--dvm-muted);
  margin-bottom: 1rem;
}

.crumb-link {
  cursor: pointer;
  color: var(--dvm-blue);
}

.crumb-link:hover {
  opacity: 1;
  text-decoration: underline;
  text-underline-offset: 2px;
}

.crumb-sep { color: var(--dvm-muted-2); }

.hero-title {
  color: var(--dvm-navy);
  font-size: clamp(1.65rem, 3vw, 2.3rem);
  font-weight: 900;
  margin: 0 0 0.8rem;
  line-height: 1.15;
  text-shadow: none;
  letter-spacing: 0;
}

.hero-aim {
  max-width: 820px;
  color: var(--dvm-muted);
  font-size: 0.98rem;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.hero-aim :deep(p) { margin: 0 0 4px; }
.hero-aim :deep(p:last-child) { margin: 0; }

.hero-stats {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}

.stat-badge {
  background: var(--dvm-blue-soft);
  color: var(--dvm-navy);
  padding: 0.28rem 0.65rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 800;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

.pdf-download-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  margin-top: 1rem;
  padding: 0.5rem 0.85rem;
  background: var(--dvm-gold);
  border: 1px solid var(--dvm-gold);
  border-radius: 7px;
  color: #201a08;
  font-size: 0.88rem;
  font-weight: 700;
  text-decoration: none;
  transition: background 0.2s ease;
}
.pdf-download-btn:hover {
  background: var(--dvm-gold-hover);
  color: #fff;
}

/* Concepts Section */
.concepts-section { padding: 0 1rem; }

.concepts-inner {
  max-width: 960px;
  margin: 0 auto;
  padding-top: 1.5rem;
}

.section-eyebrow {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--dvm-muted);
  margin: 0 0 0.3rem;
}

.section-heading {
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--dvm-text);
  margin: 0 0 1.5rem;
}

/* Concept List */
.concept-list { display: flex; flex-direction: column; gap: 1rem; position: relative; }

/* Vertical connector line behind cards */
.concept-list::before { display: none; }

.concept-card {
  background: #fff;
  border-radius: var(--dvm-radius-lg);
  border: 1px solid var(--dvm-line);
  border-left: 4px solid var(--accent, var(--dvm-blue));
  box-shadow: var(--dvm-shadow-soft);
  overflow: hidden;
  position: relative;
  transition: transform 0.25s cubic-bezier(.22,.68,0,1.2), box-shadow 0.25s ease;
  z-index: 1;
}

.concept-card:hover { transform: translateY(-2px); box-shadow: var(--dvm-shadow); }

/* Ghost watermark number */
.card-watermark {
  position: absolute;
  top: -0.5rem;
  right: 0.75rem;
  font-size: 8rem;
  font-weight: 900;
  line-height: 1;
  color: var(--accent, #2563eb);
  opacity: 0.04;
  pointer-events: none;
  user-select: none;
  letter-spacing: -0.04em;
  z-index: 0;
}

/* Card Header */
.concept-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.2rem 1.5rem 1.1rem;
  border-bottom: 1px solid #f0f0f8;
  background: linear-gradient(to right, #fafafe 0%, #fff 55%);
  position: relative;
  z-index: 1;
}

.concept-badge {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: var(--accent, #2563eb);
  color: white;
  font-size: 1rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  letter-spacing: -0.02em;
}

.concept-header-text {
  flex: 1;
  min-width: 0;
}

.concept-title {
  font-size: 1.08rem;
  font-weight: 700;
  color: #18181b;
  margin: 0;
  line-height: 1.35;
}

.sessions-pill {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--accent, #2563eb);
  background: color-mix(in srgb, var(--accent, #2563eb) 10%, white);
  padding: 0.3rem 0.8rem 0.3rem 0.6rem;
  border-radius: 20px;
  flex-shrink: 0;
  border: 1px solid color-mix(in srgb, var(--accent, #2563eb) 20%, transparent);
}

.sessions-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--accent, #2563eb);
  display: inline-block;
  flex-shrink: 0;
}

/* Card Body */
.concept-body {
  padding: 1.4rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  position: relative;
  z-index: 1;
}

/* Learning Outcomes callout block */
.lo-callout {
  background: color-mix(in srgb, var(--accent, #2563eb) 6%, white);
  border-left: 3px solid var(--accent, #2563eb);
  border-radius: 0 10px 10px 0;
  padding: 0.9rem 1.1rem;
}

.lo-label {
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent, #2563eb);
  margin: 0 0 0.5rem;
  opacity: 0.85;
}

.lo-content {
  font-size: 0.93rem;
  color: #2d2d3a;
  line-height: 1.7;
}

/* Extra Fields */
.extra-fields {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding-top: 0.1rem;
}

.extra-field {
  /* no border — icon+label does the job */
}

.field-label {
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: #8b8ba0;
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
  padding-bottom: 0.3rem;
  scrollbar-width: thin;
  scrollbar-color: color-mix(in srgb, var(--accent, #2563eb) 40%, transparent) transparent;
}

.images-row::-webkit-scrollbar {
  height: 4px;
}

.images-row::-webkit-scrollbar-thumb {
  background: color-mix(in srgb, var(--accent, #2563eb) 40%, transparent);
  border-radius: 4px;
}

.thumb-link {
  flex-shrink: 0;
  display: block;
  border-radius: 10px;
  overflow: hidden;
}

.concept-thumbnail {
  height: 100px;
  width: auto;
  border-radius: 10px;
  object-fit: cover;
  display: block;
  transition: transform 0.25s ease, filter 0.25s ease;
  filter: brightness(0.97);
}

.thumb-link:hover .concept-thumbnail {
  transform: scale(1.05);
  filter: brightness(1.03);
}

/* Exhibit Button */
.concept-card-footer {
  padding-top: 0.1rem;
}

.exhibit-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--accent, #2563eb);
  color: white;
  border: none;
  border-radius: 10px;
  padding: 0.55rem 1.3rem;
  font-size: 0.9rem;
  font-weight: 700;
  font-family: inherit;
  cursor: pointer;
  transition: background 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
  box-shadow: 0 3px 12px rgba(0,0,0,0.15);
}

.exhibit-btn:hover {
  filter: brightness(1.1);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0,0,0,0.2);
}

.btn-arrow {
  display: inline-block;
  transition: transform 0.2s ease;
}

.exhibit-btn:hover .btn-arrow {
  transform: translateX(4px);
}

/* Quill content styles */
.ql-content :deep(p) { margin: 0 0 6px; }
.ql-content :deep(ul), .ql-content :deep(ol) { padding-left: 20px; margin: 4px 0; }
.ql-content :deep(strong) { font-weight: 600; }
.ql-content :deep(em) { font-style: italic; }
.ql-content :deep(a) { color: #2563eb; }
.ql-content :deep(p:last-child) { margin-bottom: 0; }
.ql-content :deep(img) {
  max-width: 100%;
  width: auto;
  height: auto !important;
  display: block;
}
.ql-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  table-layout: fixed;
  margin: 0.6rem 0;
}
.ql-content :deep(th),
.ql-content :deep(td) {
  border: 1px solid rgba(0, 0, 0, 0.38) !important;
  padding: 0.45rem 0.6rem;
  vertical-align: top;
}
.ql-content :deep(th) {
  background: #f8fafc;
  font-weight: 700;
}

/* Modal */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(15, 15, 30, 0.65);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.modal-card {
  background: #fff;
  border-radius: 20px;
  width: min(96vw, 660px);
  max-width: 96vw;
  max-height: 90vh;
  min-width: 340px;
  min-height: 280px;
  overflow: auto;
  resize: both;
  display: flex;
  flex-direction: column;
  box-shadow: 0 32px 80px rgba(0,0,0,0.35);
  border-top: 4px solid var(--accent, #2563eb);
}

.modal-header {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  padding: 1.5rem 1.5rem 1.2rem;
  position: sticky;
  top: 0;
  background: #fff;
  border-radius: 20px 20px 0 0;
  z-index: 1;
  border-bottom: 1px solid #f0f0f8;
}

.modal-header-icon {
  font-size: 1.6rem;
  line-height: 1;
  flex-shrink: 0;
  margin-top: 0.1rem;
}

.modal-header-text {
  flex: 1;
  min-width: 0;
}

.modal-subtitle {
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent, #2563eb);
  margin: 0 0 0.25rem;
  opacity: 0.8;
}

.modal-title {
  font-size: 1.2rem;
  font-weight: 800;
  color: #18181b;
  margin: 0;
  line-height: 1.3;
}

.modal-close {
  background: #f4f4f8;
  border: none;
  width: 34px;
  height: 34px;
  border-radius: 50%;
  cursor: pointer;
  font-size: 0.85rem;
  color: #374151;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s ease, transform 0.15s ease;
  font-family: inherit;
  margin-top: 0.1rem;
}

.modal-close:hover {
  background: #e5e7eb;
  transform: scale(1.1);
}

.modal-body {
  padding: 1.25rem 1.5rem 1.75rem;
  display: flex;
  flex-direction: column;
  gap: 0;
}

.exhibit-entry {
  padding: 1.1rem 0;
}

.exhibit-entry:first-child {
  padding-top: 0.25rem;
}

/* Exhibit header row */
.exhibit-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 0.75rem;
}

.exhibit-label-row {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.exhibit-index {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--accent, #2563eb);
  color: white;
  font-size: 0.7rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.exhibit-label {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #3f3f50;
  margin: 0;
}

.exhibit-value {
  font-size: 0.93rem;
  color: #1f2937;
  line-height: 1.65;
  word-break: break-word;
  padding-left: 2rem;
}

.exhibit-divider {
  border: none;
  border-top: 1px solid #f0f0f8;
  margin: 0;
}

.exhibit-link {
  color: #2563eb;
  word-break: break-all;
}

.exhibit-link:hover {
  color: #1d4ed8;
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

@media (max-width: 640px) {
  .hero { padding: 2rem 1rem 2rem; }
  .hero-title { font-size: 1.6rem; }
  .concepts-section { padding: 0 1rem; }
  .concept-header { padding: 1rem 1.1rem; gap: 0.75rem; }
  .concept-badge { width: 36px; height: 36px; font-size: 0.9rem; }
  .concept-title { font-size: 1rem; }
  .concept-body { padding: 1.1rem; gap: 1rem; }
  .card-watermark { font-size: 5.5rem; }
  .concept-list::before { left: 29px; }
  .modal-card {
    max-height: 92vh;
    border-radius: 16px;
    min-width: 0;
    min-height: 0;
    width: 100%;
    resize: none;
  }
  .modal-header { padding: 1rem 1rem 0.9rem; }
  .modal-body { padding: 0.75rem 1rem 1.25rem; }
  .exhibit-value { padding-left: 1.75rem; }
}

/* ---- Media Containers ---- */
.media-container {
  border-radius: 12px;
  overflow: hidden;
  background: #f4f4f8;
  display: flex;
  align-items: center;
  justify-content: center;
}

.image-container {
  aspect-ratio: 4/3;
  max-width: 100%;
}

.exhibit-image {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}

.audio-container {
  padding: 1.5rem 1rem;
  width: 100%;
}

.exhibit-audio {
  width: 100%;
  height: 40px;
}

.video-container {
  aspect-ratio: 16/9;
  width: 100%;
}

.exhibit-video {
  width: 100%;
  height: 100%;
  object-fit: contain;
  display: block;
}
</style>
