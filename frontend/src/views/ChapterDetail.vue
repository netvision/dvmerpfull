<template>
  <div class="page">
    <div class="top-bar">
      <button class="back-btn" @click="goBack">&#8592; Back</button>
    </div>

    <LoadingSpinner v-if="loading" message="Loading chapter…" />

    <div v-else-if="error" class="error-box">
      <ErrorBanner :message="error" />
      <button @click="fetchChapter">Retry</button>
    </div>

    <template v-else-if="chapter">
      <!-- Hero Section -->
      <div class="hero" :style="{ background: heroGradient }">
        <div class="hero-inner">
          <div class="breadcrumb">
            {{ chapter.class?.name }} &rsaquo; {{ chapter.subject?.name }}
          </div>
          <h1 class="hero-title">{{ chapter.title }}</h1>
          <div class="hero-meta">
            <span class="hero-badge">
              <span>⏱</span> {{ totalSessions }} sessions
            </span>
            <span class="hero-badge">
              <span>💡</span> {{ chapter.concepts?.length || 0 }} concepts
            </span>
          </div>
        </div>
      </div>

      <!-- Aim -->
      <div v-if="chapter.aim" class="aim-section">
        <h2 class="section-label">Aim</h2>
        <p class="aim-text">{{ chapter.aim }}</p>
      </div>

      <!-- Concept Cards Row -->
      <div class="concepts-scroll-area" v-if="chapter.concepts?.length">
        <h2 class="section-label padded">Concepts</h2>
        <div class="concept-cards-row">
          <div
            v-for="concept in chapter.concepts"
            :key="concept.id"
            class="concept-chip"
            :class="{ 'concept-chip--active': selectedConcept?.id === concept.id }"
            @click="selectedConcept = concept"
          >
            <span class="chip-sno">{{ concept.s_no }}</span>
            <span class="chip-title">{{ concept.title }}</span>
            <span class="chip-sessions">{{ concept.sessions }} sess.</span>
          </div>
        </div>
      </div>

      <!-- Selected Concept Detail -->
      <transition name="fade">
        <div v-if="selectedConcept" class="concept-detail">
          <div class="detail-card">
            <h2 class="detail-title">
              <span class="detail-sno">{{ selectedConcept.s_no }}</span>
              {{ selectedConcept.title }}
            </h2>

            <!-- Learning Outcomes -->
            <div v-if="selectedConcept.learning_outcomes" class="detail-section">
              <h3 class="detail-section-label">Learning Outcomes</h3>
              <p class="detail-text preformatted">{{ selectedConcept.learning_outcomes }}</p>
            </div>

            <!-- Exhibit Fields -->
            <div v-if="selectedConcept.exhibits?.length" class="detail-section">
              <h3 class="detail-section-label">Exhibits</h3>
              <div class="exhibits-grid">
                <div
                  v-for="exhibit in selectedConcept.exhibits"
                  :key="exhibit.field_key"
                  class="exhibit-item"
                >
                  <span class="exhibit-label">{{ formatFieldKey(exhibit.field_key) }}</span>
                  <div class="exhibit-value">
                    <template v-for="(part, pi) in splitLines(exhibit.field_value)" :key="pi">
                      <!-- YouTube embed -->
                      <template v-if="getYoutubeId(part)">
                        <iframe
                          :src="`https://www.youtube.com/embed/${getYoutubeId(part)}`"
                          width="100%"
                          style="max-width:480px;aspect-ratio:16/9;border:none;border-radius:8px;display:block;margin:4px 0"
                          allowfullscreen
                        ></iframe>
                      </template>
                      <!-- Other URL -->
                      <template v-else-if="isUrl(part)">
                        <a :href="part.trim()" target="_blank" rel="noopener" style="display:block;word-break:break-all">{{ part.trim() }}</a>
                      </template>
                      <!-- Plain text (preserve newlines within part) -->
                      <template v-else>
                        <span style="white-space:pre-wrap;display:block">{{ part }}</span>
                      </template>
                    </template>
                  </div>
                </div>
              </div>
            </div>

            <!-- Images -->
            <div v-if="selectedConcept.images?.length" class="concept-images detail-section">
              <h3 class="detail-section-label">Images</h3>
              <div class="images-row">
                <a v-for="img in selectedConcept.images" :key="img.id"
                   :href="`http://localhost:8000${img.url}`" target="_blank">
                  <img :src="`http://localhost:8000${img.url}`" :alt="img.original_name"
                       style="height:100px;width:auto;border-radius:6px;object-fit:cover;cursor:pointer" />
                </a>
              </div>
            </div>

            <!-- Extra fields -->
            <div class="detail-extras">
              <div v-if="selectedConcept.integration_other_sub" class="extra-section">
                <h3 class="detail-section-label">Integration with Other Subjects</h3>
                <p class="detail-text preformatted">{{ selectedConcept.integration_other_sub }}</p>
              </div>
              <div v-if="selectedConcept.library" class="extra-section">
                <h3 class="detail-section-label">Library</h3>
                <p class="detail-text preformatted">{{ selectedConcept.library }}</p>
              </div>
              <div v-if="selectedConcept.activity" class="extra-section">
                <h3 class="detail-section-label">Activity</h3>
                <p class="detail-text preformatted">{{ selectedConcept.activity }}</p>
              </div>
              <div v-if="selectedConcept.life_lesson" class="extra-section">
                <h3 class="detail-section-label">Life Lesson</h3>
                <p class="detail-text preformatted">{{ selectedConcept.life_lesson }}</p>
              </div>
              <div v-if="selectedConcept.remarks" class="extra-section">
                <h3 class="detail-section-label">Remarks</h3>
                <p class="detail-text preformatted">{{ selectedConcept.remarks }}</p>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </template>
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
const selectedConcept = ref(null)

const heroGradient = computed(() => {
  const color = chapter.value?.subject?.color
  if (!color) return 'linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%)'
  return `linear-gradient(135deg, ${color} 0%, ${shiftColor(color)} 100%)`
})

const totalSessions = computed(() => {
  if (!chapter.value?.concepts) return 0
  return chapter.value.concepts.reduce((sum, c) => sum + (c.sessions || 0), 0)
})

function shiftColor(hex) {
  const num = parseInt(hex.replace('#', ''), 16)
  const r = Math.max(0, (num >> 16) - 50)
  const g = Math.max(0, ((num >> 8) & 0xff) - 50)
  const b = Math.max(0, (num & 0xff) - 50)
  return `#${((r << 16) | (g << 8) | b).toString(16).padStart(6, '0')}`
}

function formatFieldKey(key) {
  return key
    .replace(/_/g, ' ')
    .replace(/\b\w/g, c => c.toUpperCase())
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

/**
 * Split a field_value by newlines so each line can be rendered
 * individually (URL detection per line).
 */
function splitLines(value) {
  if (!value) return ['']
  return value.split('\n')
}

function goBack() {
  if (window.history.length > 2) {
    router.back()
  } else if (chapter.value?.subject?.id && chapter.value?.class?.id) {
    router.push(`/class/${chapter.value.class.id}/${chapter.value.subject.id}`)
  } else {
    router.push('/')
  }
}

async function fetchChapter() {
  loading.value = true
  error.value = null
  try {
    const res = await api.get(`/api/public/chapters/${chapterId.value}`)
    chapter.value = res.data
    // Auto-select first concept
    if (res.data.concepts?.length) {
      selectedConcept.value = res.data.concepts[0]
    }
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
  background: #f8f9fc;
  font-family: system-ui, -apple-system, sans-serif;
  padding-bottom: 3rem;
}

.top-bar {
  padding: 1rem 1.5rem 0;
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

/* Hero */
.hero {
  margin-top: 1rem;
  padding: 2.5rem 1.5rem 2rem;
  color: white;
}

.hero-inner {
  max-width: 800px;
  margin: 0 auto;
}

.breadcrumb {
  font-size: 0.88rem;
  opacity: 0.82;
  margin-bottom: 0.8rem;
  font-weight: 500;
  letter-spacing: 0.03em;
}

.hero-title {
  font-size: 2rem;
  font-weight: 800;
  margin: 0 0 1rem;
  line-height: 1.25;
  text-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.hero-meta {
  display: flex;
  gap: 0.8rem;
  flex-wrap: wrap;
}

.hero-badge {
  background: rgba(255,255,255,0.22);
  backdrop-filter: blur(4px);
  padding: 0.3rem 0.9rem;
  border-radius: 20px;
  font-size: 0.88rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
}

/* Aim */
.aim-section {
  max-width: 800px;
  margin: 1.8rem auto 0;
  padding: 0 1.5rem;
}

.section-label {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #4f46e5;
  margin: 0 0 0.5rem;
}

.aim-text {
  font-size: 1rem;
  color: #374151;
  line-height: 1.65;
  margin: 0;
}

/* Concept chips row */
.concepts-scroll-area {
  max-width: 800px;
  margin: 2rem auto 0;
  padding: 0 1.5rem;
}

.padded {
  margin-bottom: 0.8rem;
}

.concept-cards-row {
  display: flex;
  gap: 0.75rem;
  overflow-x: auto;
  padding-bottom: 0.5rem;
  scrollbar-width: thin;
  scrollbar-color: #c4b5fd transparent;
}

.concept-cards-row::-webkit-scrollbar {
  height: 4px;
}

.concept-cards-row::-webkit-scrollbar-track {
  background: transparent;
}

.concept-cards-row::-webkit-scrollbar-thumb {
  background: #c4b5fd;
  border-radius: 4px;
}

.concept-chip {
  flex-shrink: 0;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  cursor: pointer;
  transition: all 0.18s ease;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  min-width: 130px;
  max-width: 180px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.06);
}

.concept-chip:hover {
  border-color: #a5b4fc;
  box-shadow: 0 3px 12px rgba(79,70,229,0.15);
  transform: translateY(-1px);
}

.concept-chip--active {
  border-color: #4f46e5;
  background: #eef2ff;
  box-shadow: 0 3px 14px rgba(79,70,229,0.2);
}

.chip-sno {
  font-size: 0.72rem;
  font-weight: 700;
  color: #4f46e5;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}

.chip-title {
  font-size: 0.88rem;
  font-weight: 600;
  color: #1e1b4b;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.chip-sessions {
  font-size: 0.76rem;
  color: #6b7280;
  margin-top: 0.1rem;
}

/* Concept Detail */
.concept-detail {
  max-width: 800px;
  margin: 1.5rem auto 0;
  padding: 0 1.5rem;
}

.detail-card {
  background: white;
  border-radius: 14px;
  padding: 1.8rem;
  box-shadow: 0 3px 16px rgba(0,0,0,0.09);
}

.detail-title {
  font-size: 1.4rem;
  font-weight: 800;
  color: #1e1b4b;
  margin: 0 0 1.4rem;
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
  line-height: 1.3;
}

.detail-sno {
  font-size: 0.78rem;
  font-weight: 700;
  color: white;
  background: #4f46e5;
  padding: 0.2rem 0.6rem;
  border-radius: 20px;
  flex-shrink: 0;
}

.detail-section {
  margin-bottom: 1.4rem;
}

.detail-section-label {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #4f46e5;
  margin: 0 0 0.5rem;
}

.detail-text {
  font-size: 0.95rem;
  color: #374151;
  line-height: 1.65;
  margin: 0;
}

.preformatted {
  white-space: pre-wrap;
  word-break: break-word;
}

/* Exhibits */
.exhibits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.exhibit-item {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.9rem 1rem;
}

.exhibit-label {
  display: block;
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #6b7280;
  margin-bottom: 0.35rem;
}

.exhibit-value {
  font-size: 0.93rem;
  color: #1f2937;
  margin: 0;
  word-break: break-word;
  line-height: 1.55;
}

.images-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  overflow-x: auto;
  padding-bottom: 0.25rem;
}

.detail-extras {
  display: flex;
  flex-direction: column;
  gap: 1.1rem;
}

.extra-section {}

/* Fade transition */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.fade-leave-to {
  opacity: 0;
}

/* Loading / Error */
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
  .page { padding-left: 0; padding-right: 0; }
  .top-bar { padding: 1rem 16px 0; }
  .hero { padding: 2rem 16px 1.5rem; }
  .aim-section { padding: 0 16px; }
  .concepts-scroll-area { padding: 0 16px; }
  .concept-detail { padding: 0 16px; }
  .hero-title { font-size: 1.5rem; }
  .concept-chip { min-width: 110px; }
  .detail-card { padding: 1.2rem; }
  .exhibits-grid { grid-template-columns: 1fr; }
}
</style>
