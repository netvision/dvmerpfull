<template>
  <div class="page">
    <!-- Nav Bar -->
    <nav class="navbar">
      <button class="back-btn" @click="router.push('/portal')">&#8592; Back to Portal</button>
      <span class="nav-title">Teacher Portal</span>
    </nav>

    <div class="content">
      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading chapter…</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="error-box">
        {{ error }}
        <button class="retry-btn" @click="fetchChapter">Retry</button>
      </div>

      <template v-else-if="chapter">
        <!-- Heading -->
        <h1 class="page-heading">Editing: <span class="chapter-title-span">{{ chapter.title }}</span></h1>

        <!-- Edit Form Card -->
        <div class="card">
          <h2 class="card-heading">Chapter Details</h2>
          <form @submit.prevent="saveChapter">
            <div class="field">
              <label for="title">Title</label>
              <input id="title" v-model="form.title" type="text" required />
            </div>
            <div class="field">
              <label for="aim">Aim</label>
              <textarea id="aim" v-model="form.aim" rows="4" placeholder="Chapter aim / objective"></textarea>
            </div>
            <div class="field">
              <label for="order">Order Index</label>
              <input id="order" v-model.number="form.order_index" type="number" min="0" />
            </div>

            <div v-if="saveError" class="error-banner">{{ saveError }}</div>
            <div v-if="saveSuccess" class="success-banner">Saved! Redirecting…</div>

            <div class="form-actions">
              <button type="submit" class="btn-save" :disabled="saving">
                <span v-if="saving" class="spinner-sm"></span>
                {{ saving ? 'Saving…' : 'Save Changes' }}
              </button>
            </div>
          </form>
        </div>

        <!-- Read-only Concepts & Exhibits -->
        <div v-if="chapter.concepts?.length" class="card concepts-card">
          <h2 class="card-heading">Concepts <span class="count-badge">{{ chapter.concepts.length }}</span></h2>
          <p class="upload-hint">To edit concepts, use "Upload xlsx" from the portal.</p>

          <!-- Concept Selector -->
          <div class="concept-chips">
            <div
              v-for="concept in chapter.concepts"
              :key="concept.id"
              class="concept-chip"
              :class="{ active: selectedConcept?.id === concept.id }"
              @click="selectedConcept = concept"
            >
              <span class="chip-sno">{{ concept.s_no }}</span>
              <span class="chip-title">{{ concept.title }}</span>
              <span class="chip-sessions">{{ concept.sessions }} sess.</span>
            </div>
          </div>

          <!-- Selected Concept Detail -->
          <transition name="fade">
            <div v-if="selectedConcept" class="concept-detail">
              <h3 class="concept-name">
                <span class="detail-sno">{{ selectedConcept.s_no }}</span>
                {{ selectedConcept.title }}
              </h3>

              <div v-if="selectedConcept.learning_outcomes" class="detail-section">
                <h4 class="section-label">Learning Outcomes</h4>
                <p class="detail-text preformatted">{{ selectedConcept.learning_outcomes }}</p>
              </div>

              <div v-if="selectedConcept.exhibits?.length" class="detail-section">
                <h4 class="section-label">Exhibits</h4>
                <div class="exhibits-grid">
                  <div v-for="ex in selectedConcept.exhibits" :key="ex.field_key" class="exhibit-item">
                    <span class="exhibit-label">{{ formatKey(ex.field_key) }}</span>
                    <p class="exhibit-value preformatted">{{ ex.field_value }}</p>
                  </div>
                </div>
              </div>

              <div class="detail-extras">
                <div v-if="selectedConcept.integration_other_sub" class="extra-section">
                  <h4 class="section-label">Integration with Other Subjects</h4>
                  <p class="detail-text preformatted">{{ selectedConcept.integration_other_sub }}</p>
                </div>
                <div v-if="selectedConcept.library" class="extra-section">
                  <h4 class="section-label">Library</h4>
                  <p class="detail-text preformatted">{{ selectedConcept.library }}</p>
                </div>
                <div v-if="selectedConcept.activity" class="extra-section">
                  <h4 class="section-label">Activity</h4>
                  <p class="detail-text preformatted">{{ selectedConcept.activity }}</p>
                </div>
                <div v-if="selectedConcept.life_lesson" class="extra-section">
                  <h4 class="section-label">Life Lesson</h4>
                  <p class="detail-text preformatted">{{ selectedConcept.life_lesson }}</p>
                </div>
                <div v-if="selectedConcept.remarks" class="extra-section">
                  <h4 class="section-label">Remarks</h4>
                  <p class="detail-text preformatted">{{ selectedConcept.remarks }}</p>
                </div>
              </div>
            </div>
          </transition>
        </div>

        <div v-else class="card">
          <p class="no-concepts">No concepts yet. Upload an xlsx file to add concepts.</p>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../api.js'

const router = useRouter()
const route = useRoute()

const chapterId = computed(() => route.params.id)
const chapter = ref(null)
const loading = ref(true)
const error = ref('')

const form = ref({ title: '', aim: '', order_index: 0 })
const saving = ref(false)
const saveError = ref('')
const saveSuccess = ref(false)

const selectedConcept = ref(null)

onMounted(fetchChapter)

async function fetchChapter() {
  loading.value = true
  error.value = ''
  try {
    const res = await api.get(`/api/portal/chapters/${chapterId.value}`)
    chapter.value = res.data
    form.value = {
      title: res.data.title || '',
      aim: res.data.aim || '',
      order_index: res.data.order_index ?? 0,
    }
    if (res.data.concepts?.length) {
      selectedConcept.value = res.data.concepts[0]
    }
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load chapter.'
  } finally {
    loading.value = false
  }
}

async function saveChapter() {
  saveError.value = ''
  saveSuccess.value = false
  saving.value = true
  try {
    await api.put(`/api/portal/chapters/${chapterId.value}`, {
      title: form.value.title,
      aim: form.value.aim,
      order_index: form.value.order_index,
    })
    saveSuccess.value = true
    setTimeout(() => router.push('/portal'), 1000)
  } catch (e) {
    saveError.value = e.response?.data?.detail || 'Failed to save chapter.'
  } finally {
    saving.value = false
  }
}

function formatKey(key) {
  return key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f1f5f9;
  font-family: system-ui, -apple-system, sans-serif;
  padding-bottom: 3rem;
}

/* Navbar */
.navbar {
  background: #1e293b;
  color: white;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0 1.5rem;
  height: 56px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.back-btn {
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.25);
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.88rem;
  transition: background 0.15s;
}

.back-btn:hover {
  background: rgba(255,255,255,0.22);
}

.nav-title {
  font-size: 1rem;
  font-weight: 600;
  opacity: 0.8;
}

/* Content */
.content {
  max-width: 800px;
  margin: 0 auto;
  padding: 1.5rem 1rem;
}

.page-heading {
  font-size: 1.4rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 1.2rem;
}

.chapter-title-span {
  color: #4f46e5;
}

/* Card */
.card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem 1.8rem;
  box-shadow: 0 1px 6px rgba(0,0,0,0.07);
  margin-bottom: 1.2rem;
}

.card-heading {
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 1.2rem;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.count-badge {
  background: #e0e7ff;
  color: #4f46e5;
  font-size: 0.78rem;
  font-weight: 700;
  padding: 0.15rem 0.55rem;
  border-radius: 20px;
}

/* Form Fields */
.field {
  margin-bottom: 1.1rem;
}

.field label {
  display: block;
  font-size: 0.83rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.4rem;
}

.field input,
.field textarea {
  width: 100%;
  padding: 0.62rem 0.9rem;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
  color: #111827;
  outline: none;
  transition: border-color 0.15s;
  box-sizing: border-box;
  font-family: inherit;
}

.field input:focus,
.field textarea:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79,70,229,0.1);
}

.field textarea {
  resize: vertical;
}

.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  border-radius: 7px;
  padding: 0.6rem 0.9rem;
  font-size: 0.88rem;
  margin-bottom: 1rem;
}

.success-banner {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #15803d;
  border-radius: 7px;
  padding: 0.6rem 0.9rem;
  font-size: 0.88rem;
  margin-bottom: 1rem;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.btn-save {
  padding: 0.6rem 1.6rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.97rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background 0.15s;
}

.btn-save:hover:not(:disabled) {
  background: #4338ca;
}

.btn-save:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.spinner-sm {
  width: 15px;
  height: 15px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Concepts */
.concepts-card {}

.upload-hint {
  font-size: 0.83rem;
  color: #94a3b8;
  margin: -0.8rem 0 1rem;
  font-style: italic;
}

.concept-chips {
  display: flex;
  gap: 0.65rem;
  flex-wrap: wrap;
  margin-bottom: 1.2rem;
}

.concept-chip {
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 9px;
  padding: 0.6rem 0.85rem;
  cursor: pointer;
  transition: all 0.15s;
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
  min-width: 110px;
  max-width: 160px;
}

.concept-chip:hover {
  border-color: #a5b4fc;
  box-shadow: 0 2px 8px rgba(79,70,229,0.12);
}

.concept-chip.active {
  border-color: #4f46e5;
  background: #eef2ff;
}

.chip-sno {
  font-size: 0.7rem;
  font-weight: 700;
  color: #4f46e5;
  text-transform: uppercase;
  letter-spacing: 0.07em;
}

.chip-title {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1e1b4b;
  line-height: 1.3;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.chip-sessions {
  font-size: 0.74rem;
  color: #6b7280;
}

/* Concept Detail */
.concept-detail {
  border-top: 1px solid #e2e8f0;
  padding-top: 1.2rem;
  margin-top: 0.2rem;
}

.concept-name {
  font-size: 1.15rem;
  font-weight: 700;
  color: #1e1b4b;
  margin: 0 0 1.1rem;
  display: flex;
  align-items: baseline;
  gap: 0.6rem;
}

.detail-sno {
  font-size: 0.72rem;
  font-weight: 700;
  color: white;
  background: #4f46e5;
  padding: 0.18rem 0.55rem;
  border-radius: 20px;
  flex-shrink: 0;
}

.detail-section {
  margin-bottom: 1.2rem;
}

.section-label {
  font-size: 0.73rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #4f46e5;
  margin: 0 0 0.4rem;
}

.detail-text {
  font-size: 0.93rem;
  color: #374151;
  line-height: 1.65;
  margin: 0;
}

.preformatted {
  white-space: pre-wrap;
  word-break: break-word;
}

.exhibits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 0.85rem;
}

.exhibit-item {
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 7px;
  padding: 0.8rem 0.95rem;
}

.exhibit-label {
  display: block;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #6b7280;
  margin-bottom: 0.3rem;
}

.exhibit-value {
  font-size: 0.91rem;
  color: #1f2937;
  margin: 0;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.55;
}

.detail-extras {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.extra-section {}

/* Loading / Error */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  color: #64748b;
  gap: 1rem;
  background: white;
  border-radius: 12px;
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #e2e8f0;
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.error-box {
  background: #fef2f2;
  color: #dc2626;
  padding: 1.2rem 1.4rem;
  border-radius: 10px;
  border: 1px solid #fecaca;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.retry-btn {
  padding: 0.4rem 1rem;
  background: #dc2626;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.88rem;
}

.no-concepts {
  color: #94a3b8;
  font-style: italic;
  margin: 0;
  font-size: 0.93rem;
}

/* Fade */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(6px);
}

.fade-leave-to {
  opacity: 0;
}
</style>
