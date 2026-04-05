<template>
  <div class="page">
    <!-- Navbar -->
    <nav class="navbar">
      <span class="nav-title">Chapter Editor</span>
      <button class="back-btn" @click="router.push('/portal')">&#8592; Back to Portal</button>
    </nav>

    <!-- Loading -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading chapter…</p>
    </div>

    <!-- Error -->
    <div v-else-if="loadError" class="error-box">
      {{ loadError }}
      <button class="retry-btn" @click="fetchChapter">Retry</button>
    </div>

    <template v-else-if="chapter">
      <!-- Chapter Summary Card -->
      <div class="content">
        <div class="summary-card">
          <div class="summary-info">
            <div class="summary-title">{{ chapter.title }}</div>
            <div class="summary-meta">
              <span v-if="chapter.subject?.name" class="meta-badge">{{ chapter.subject.name }}</span>
              <span v-if="chapter.class?.name" class="meta-badge">{{ chapter.class.name }}</span>
            </div>
          </div>
          <button class="btn-edit-chapter" @click="openChapterModal">Edit Chapter Details</button>
        </div>

        <!-- Concepts Section -->
        <div class="concepts-header">
          <h2 class="section-title">
            Concepts
            <span class="count-badge">{{ chapter.concepts?.length || 0 }}</span>
          </h2>
          <button class="btn-add" @click="openAddConceptModal">+ Add Concept</button>
        </div>

        <!-- Concepts Table -->
        <div class="concepts-table-wrap">
          <div v-if="!chapter.concepts?.length" class="empty-card">
            <p>No concepts yet. Click "+ Add Concept" to create one.</p>
          </div>
          <table v-else class="concepts-table">
            <thead>
              <tr>
                <th>S.No</th>
                <th>Title</th>
                <th>Sessions</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="concept in chapter.concepts" :key="concept.id">
                <td class="td-sno">{{ concept.s_no }}</td>
                <td class="td-title">{{ concept.title }}</td>
                <td class="td-sessions">{{ concept.sessions }}</td>
                <td class="td-actions">
                  <button class="btn-edit-sm" @click="openConceptModal(concept)">Edit</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </template>

    <!-- ===== Chapter Modal ===== -->
    <div v-if="showChapterModal" class="modal-backdrop" @click.self="showChapterModal = false">
      <div class="modal-card">
        <div class="modal-header">
          <h2 class="modal-title">Edit Chapter</h2>
          <button class="modal-close" @click="showChapterModal = false">&times;</button>
        </div>
        <div class="modal-body">
          <div class="field">
            <label>Title</label>
            <input v-model="chapterForm.title" type="text" placeholder="Chapter title" />
          </div>
          <div class="field">
            <label>Aim</label>
            <RichTextEditor v-model="chapterForm.aim" placeholder="Chapter aim / objective" minHeight="140px" />
          </div>
          <div class="field">
            <label>Order Index</label>
            <input v-model.number="chapterForm.order_index" type="number" min="0" class="input-sm" />
          </div>
          <div v-if="chapterMsg.text" :class="['inline-msg', chapterMsg.type]">{{ chapterMsg.text }}</div>
        </div>
        <div class="modal-footer">
          <button class="btn-cancel" @click="showChapterModal = false">Cancel</button>
          <button class="btn-save" :disabled="chapterSaving" @click="saveChapter">
            <span v-if="chapterSaving" class="spinner-sm"></span>
            {{ chapterSaving ? 'Saving…' : 'Save' }}
          </button>
        </div>
      </div>
    </div>

    <!-- ===== Concept Modal ===== -->
    <div v-if="showConceptModal" class="modal-backdrop" @click.self="showConceptModal = false">
      <div class="modal-card modal-card--wide">
        <div class="modal-header">
          <h2 class="modal-title">{{ isNewConcept ? 'Add Concept' : 'Edit Concept' }}</h2>
          <button class="modal-close" @click="showConceptModal = false">&times;</button>
        </div>

        <!-- Tab Bar -->
        <div class="tab-bar">
          <button
            v-for="(tab, i) in conceptTabs"
            :key="i"
            :class="['tab-btn', { 'tab-btn--active': activeTab === i }]"
            @click="activeTab = i"
          >{{ tab }}</button>
        </div>

        <div class="modal-body">
          <!-- Tab 1: Concept Info -->
          <div v-if="activeTab === 0">
            <div class="fields-row">
              <div class="field field--sm">
                <label>S.No</label>
                <input v-model="conceptForm.s_no" type="text" placeholder="e.g. 1.1" />
              </div>
              <div class="field field--grow">
                <label>Title <span class="required">*</span></label>
                <input v-model="conceptForm.title" type="text" placeholder="Concept title" />
              </div>
              <div class="field field--sm">
                <label>Sessions</label>
                <input v-model="conceptForm.sessions" type="text" placeholder="e.g. 2" />
              </div>
              <div class="field field--sm">
                <label>Exhibit Ref</label>
                <input v-model="conceptForm.exhibit_ref" type="text" placeholder="exhibit_1" />
              </div>
            </div>
            <div class="field">
              <label>Learning Outcomes</label>
              <RichTextEditor v-model="conceptForm.learning_outcomes" placeholder="Learning outcomes…" />
            </div>
            <div class="field">
              <label>Integration / Other Subjects</label>
              <RichTextEditor v-model="conceptForm.integration_other_sub" placeholder="Integration with other subjects…" />
            </div>
            <div class="field">
              <label>Library</label>
              <RichTextEditor v-model="conceptForm.library" placeholder="Library resources…" />
            </div>
            <div class="field">
              <label>Activity</label>
              <RichTextEditor v-model="conceptForm.activity" placeholder="Activity details…" />
            </div>
            <div class="field">
              <label>Life Lesson</label>
              <RichTextEditor v-model="conceptForm.life_lesson" placeholder="Life lesson…" />
            </div>
            <div class="field">
              <label>Remarks</label>
              <RichTextEditor v-model="conceptForm.remarks" placeholder="Remarks…" />
            </div>
            <div v-if="conceptMsg.text" :class="['inline-msg', conceptMsg.type]">{{ conceptMsg.text }}</div>
          </div>

          <!-- Tab 2: Exhibit Fields -->
          <div v-if="activeTab === 1">
            <div v-if="!selectedConcept?.id" class="tab-notice">
              Save concept first to manage exhibit fields.
            </div>
            <template v-else>
              <div
                v-for="(ex, idx) in exhibitRows"
                :key="ex.id ?? 'new-' + idx"
                class="exhibit-row"
              >
                <input
                  v-model="ex.field_key"
                  type="text"
                  class="exhibit-key-input"
                  placeholder="field_key"
                />
                <div class="exhibit-value-wrap">
                  <RichTextEditor v-model="ex.field_value" minHeight="80px" />
                </div>
                <div class="exhibit-row-actions">
                  <button class="btn-save-ex" :disabled="ex.saving" @click="saveExhibit(ex, idx)" title="Save">
                    <span v-if="ex.saving" class="spinner-sm"></span>
                    <span v-else>&#10003;</span>
                  </button>
                  <button class="btn-del-ex" :disabled="ex.deleting" @click="deleteExhibit(ex, idx)" title="Delete">
                    <span v-if="ex.deleting" class="spinner-sm"></span>
                    <span v-else>&times;</span>
                  </button>
                </div>
              </div>
              <div v-if="!exhibitRows.length" class="tab-notice">No exhibit fields yet.</div>
              <button class="btn-add-field" @click="addExhibitRow">+ Add Field</button>
            </template>
          </div>

          <!-- Tab 3: Images -->
          <div v-if="activeTab === 2">
            <div v-if="!selectedConcept?.id" class="tab-notice">
              Save concept first to manage images.
            </div>
            <template v-else>
              <!-- Existing images grid -->
              <div v-if="imageList.length" class="images-grid">
                <div v-for="img in imageList" :key="img.id" class="image-item">
                  <img
                    :src="`${API_BASE}${img.url}`"
                    :alt="img.original_name"
                    class="image-thumb"
                  />
                  <div class="image-name">{{ img.original_name }}</div>
                  <button class="btn-del-img" :disabled="img.deleting" @click="deleteImage(img)">
                    <span v-if="img.deleting" class="spinner-sm"></span>
                    <span v-else>Delete</span>
                  </button>
                </div>
              </div>
              <div v-else class="tab-notice">No images yet.</div>

              <!-- Upload zone -->
              <div
                class="upload-zone"
                :class="{ 'upload-zone--drag': isDragging }"
                @dragover.prevent="isDragging = true"
                @dragleave.prevent="isDragging = false"
                @drop.prevent="onDrop"
                @click="fileInputRef.click()"
              >
                <input
                  ref="fileInputRef"
                  type="file"
                  accept="image/*"
                  multiple
                  style="display:none"
                  @change="onFileChange"
                />
                <p v-if="!selectedFiles.length">Drag &amp; drop images here, or click to select</p>
                <ul v-else class="selected-files-list">
                  <li v-for="f in selectedFiles" :key="f.name">{{ f.name }}</li>
                </ul>
              </div>

              <div v-if="uploadMsg.text" :class="['inline-msg', uploadMsg.type]">{{ uploadMsg.text }}</div>

              <button
                class="btn-upload"
                :disabled="!selectedFiles.length || uploading"
                @click="uploadImages"
              >
                <span v-if="uploading" class="spinner-sm"></span>
                {{ uploading ? 'Uploading…' : 'Upload Images' }}
              </button>
            </template>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="showConceptModal = false">Cancel</button>
          <button
            v-if="activeTab === 0"
            class="btn-save"
            :disabled="conceptSaving"
            @click="saveConcept"
          >
            <span v-if="conceptSaving" class="spinner-sm"></span>
            {{ conceptSaving ? 'Saving…' : 'Save Concept' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../api.js'
import { useAuthStore } from '../stores/auth.js'
import RichTextEditor from '../components/RichTextEditor.vue'

const API_BASE = 'http://localhost:8000'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const chapterId = computed(() => route.params.id)

// ---- Data ----
const chapter = ref(null)
const loading = ref(true)
const loadError = ref(null)

// ---- Chapter Modal ----
const showChapterModal = ref(false)
const chapterForm = ref({ title: '', aim: '', order_index: 0 })
const chapterSaving = ref(false)
const chapterMsg = ref({ text: '', type: '' })

// ---- Concept Modal ----
const showConceptModal = ref(false)
const isNewConcept = ref(false)
const selectedConcept = ref(null)
const activeTab = ref(0)
const conceptTabs = ['Concept Info', 'Exhibit Fields', 'Images']

const conceptForm = ref({
  s_no: '',
  title: '',
  sessions: '',
  exhibit_ref: '',
  learning_outcomes: '',
  integration_other_sub: '',
  library: '',
  activity: '',
  life_lesson: '',
  remarks: '',
})
const conceptSaving = ref(false)
const conceptMsg = ref({ text: '', type: '' })

// ---- Exhibit rows ----
const exhibitRows = ref([])

// ---- Images ----
const imageList = ref([])
const selectedFiles = ref([])
const isDragging = ref(false)
const uploading = ref(false)
const uploadMsg = ref({ text: '', type: '' })
const fileInputRef = ref(null)

// ---- Fetch ----
async function fetchChapter() {
  loading.value = true
  loadError.value = null
  try {
    const res = await api.get(`/api/portal/chapters/${chapterId.value}`)
    chapter.value = res.data
  } catch (e) {
    loadError.value = e.response?.data?.detail || e.message || 'Failed to load chapter'
  } finally {
    loading.value = false
  }
}

// ---- Chapter Modal ----
function openChapterModal() {
  chapterForm.value = {
    title: chapter.value.title || '',
    aim: chapter.value.aim || '',
    order_index: chapter.value.order_index ?? 0,
  }
  chapterMsg.value = { text: '', type: '' }
  showChapterModal.value = true
}

async function saveChapter() {
  chapterSaving.value = true
  chapterMsg.value = { text: '', type: '' }
  try {
    const res = await api.put(`/api/portal/chapters/${chapterId.value}`, chapterForm.value)
    Object.assign(chapter.value, res.data)
    chapterMsg.value = { text: 'Saved!', type: 'success' }
    setTimeout(() => {
      showChapterModal.value = false
      chapterMsg.value = { text: '', type: '' }
    }, 800)
  } catch (e) {
    chapterMsg.value = { text: e.response?.data?.detail || 'Save failed', type: 'error' }
  } finally {
    chapterSaving.value = false
  }
}

// ---- Concept Modal ----
async function openConceptModal(concept) {
  isNewConcept.value = false
  selectedConcept.value = { ...concept }
  conceptForm.value = {
    s_no: concept.s_no || '',
    title: concept.title || '',
    sessions: concept.sessions || '',
    exhibit_ref: concept.exhibit_ref || '',
    learning_outcomes: concept.learning_outcomes || '',
    integration_other_sub: concept.integration_other_sub || '',
    library: concept.library || '',
    activity: concept.activity || '',
    life_lesson: concept.life_lesson || '',
    remarks: concept.remarks || '',
  }
  conceptMsg.value = { text: '', type: '' }
  activeTab.value = 0
  // Populate exhibit rows
  exhibitRows.value = (concept.exhibits || []).map(ex => ({ ...ex, saving: false, deleting: false }))
  // Populate image list
  imageList.value = (concept.images || []).map(img => ({ ...img, deleting: false }))
  selectedFiles.value = []
  uploadMsg.value = { text: '', type: '' }
  showConceptModal.value = true
  await nextTick()
}

async function openAddConceptModal() {
  isNewConcept.value = true
  selectedConcept.value = null
  conceptForm.value = {
    s_no: '',
    title: '',
    sessions: '',
    exhibit_ref: '',
    learning_outcomes: '',
    integration_other_sub: '',
    library: '',
    activity: '',
    life_lesson: '',
    remarks: '',
  }
  conceptMsg.value = { text: '', type: '' }
  activeTab.value = 0
  exhibitRows.value = []
  imageList.value = []
  selectedFiles.value = []
  uploadMsg.value = { text: '', type: '' }
  showConceptModal.value = true
  await nextTick()
}

async function saveConcept() {
  if (!conceptForm.value.title?.trim()) {
    conceptMsg.value = { text: 'Title is required', type: 'error' }
    return
  }
  conceptSaving.value = true
  conceptMsg.value = { text: '', type: '' }
  try {
    let res
    if (isNewConcept.value) {
      res = await api.post(`/api/portal/concepts`, {
        ...conceptForm.value,
        chapter_id: chapterId.value,
      })
      if (!chapter.value.concepts) chapter.value.concepts = []
      chapter.value.concepts.push(res.data)
      selectedConcept.value = { ...res.data }
      isNewConcept.value = false
    } else {
      res = await api.put(`/api/portal/concepts/${selectedConcept.value.id}`, conceptForm.value)
      // Update in chapter list
      const idx = chapter.value.concepts.findIndex(c => c.id === selectedConcept.value.id)
      if (idx >= 0) chapter.value.concepts[idx] = { ...chapter.value.concepts[idx], ...res.data }
      selectedConcept.value = { ...res.data }
    }
    conceptMsg.value = { text: 'Saved!', type: 'success' }
    setTimeout(() => { conceptMsg.value = { text: '', type: '' } }, 1500)
  } catch (e) {
    conceptMsg.value = { text: e.response?.data?.detail || 'Save failed', type: 'error' }
  } finally {
    conceptSaving.value = false
  }
}

// ---- Exhibit Fields ----
function addExhibitRow() {
  exhibitRows.value.push({ id: null, field_key: '', field_value: '', saving: false, deleting: false })
}

async function saveExhibit(ex, idx) {
  if (!selectedConcept.value?.id) return
  ex.saving = true
  try {
    if (ex.id) {
      const res = await api.put(`/api/portal/exhibits/${ex.id}`, {
        field_key: ex.field_key,
        field_value: ex.field_value,
      })
      ex.id = res.data.id
    } else {
      const res = await api.post(`/api/portal/concepts/${selectedConcept.value.id}/exhibits`, {
        field_key: ex.field_key,
        field_value: ex.field_value,
      })
      ex.id = res.data.id
    }
  } catch (e) {
    alert(e.response?.data?.detail || 'Save failed')
  } finally {
    ex.saving = false
  }
}

async function deleteExhibit(ex, idx) {
  if (!ex.id) {
    exhibitRows.value.splice(idx, 1)
    return
  }
  if (!confirm('Delete this exhibit field?')) return
  ex.deleting = true
  try {
    await api.delete(`/api/portal/exhibits/${ex.id}`)
    exhibitRows.value.splice(idx, 1)
  } catch (e) {
    alert(e.response?.data?.detail || 'Delete failed')
    ex.deleting = false
  }
}

// ---- Images ----
function onFileChange(e) {
  selectedFiles.value = Array.from(e.target.files)
}

function onDrop(e) {
  isDragging.value = false
  selectedFiles.value = Array.from(e.dataTransfer.files).filter(f => f.type.startsWith('image/'))
}

async function uploadImages() {
  if (!selectedConcept.value?.id || !selectedFiles.value.length) return
  uploading.value = true
  uploadMsg.value = { text: '', type: '' }
  try {
    const formData = new FormData()
    for (const f of selectedFiles.value) {
      formData.append('files', f)
    }
    const res = await api.post(
      `/api/portal/concepts/${selectedConcept.value.id}/images`,
      formData,
      { headers: { 'Content-Type': 'multipart/form-data' } }
    )
    const newImgs = Array.isArray(res.data) ? res.data : [res.data]
    imageList.value.push(...newImgs.map(img => ({ ...img, deleting: false })))
    selectedFiles.value = []
    if (fileInputRef.value) fileInputRef.value.value = ''
    uploadMsg.value = { text: 'Upload successful!', type: 'success' }
    setTimeout(() => { uploadMsg.value = { text: '', type: '' } }, 1500)
  } catch (e) {
    uploadMsg.value = { text: e.response?.data?.detail || 'Upload failed', type: 'error' }
  } finally {
    uploading.value = false
  }
}

async function deleteImage(img) {
  if (!confirm('Delete this image?')) return
  img.deleting = true
  try {
    await api.delete(`/api/portal/images/${img.id}`)
    imageList.value = imageList.value.filter(i => i.id !== img.id)
  } catch (e) {
    alert(e.response?.data?.detail || 'Delete failed')
    img.deleting = false
  }
}

onMounted(fetchChapter)
</script>

<style scoped>
/* ---- Page ---- */
.page {
  min-height: 100vh;
  background: #f3f4f6;
  font-family: system-ui, -apple-system, sans-serif;
}

/* ---- Navbar ---- */
.navbar {
  background: #1e1b4b;
  color: white;
  padding: 0 1.5rem;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-title {
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.back-btn {
  background: rgba(255,255,255,0.12);
  color: white;
  border: 1px solid rgba(255,255,255,0.25);
  padding: 0.4rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background 0.15s;
}
.back-btn:hover { background: rgba(255,255,255,0.22); }

/* ---- Content ---- */
.content {
  max-width: 860px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

/* ---- Summary Card ---- */
.summary-card {
  background: white;
  border-radius: 12px;
  padding: 1.4rem 1.6rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.08);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 2rem;
}

.summary-title {
  font-size: 1.3rem;
  font-weight: 800;
  color: #1e1b4b;
  margin-bottom: 0.4rem;
}

.summary-meta {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.meta-badge {
  background: #eef2ff;
  color: #4f46e5;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.2rem 0.7rem;
  border-radius: 20px;
}

.btn-edit-chapter {
  background: #4f46e5;
  color: white;
  border: none;
  padding: 0.55rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: background 0.15s;
}
.btn-edit-chapter:hover { background: #4338ca; }

/* ---- Concepts Header ---- */
.concepts-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e1b4b;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
}

.count-badge {
  background: #e0e7ff;
  color: #4338ca;
  font-size: 0.78rem;
  font-weight: 700;
  padding: 0.15rem 0.6rem;
  border-radius: 20px;
}

.btn-add {
  background: #10b981;
  color: white;
  border: none;
  padding: 0.5rem 1.1rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: background 0.15s;
}
.btn-add:hover { background: #059669; }

/* ---- Concepts Table ---- */
.concepts-table-wrap {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.07);
  overflow: hidden;
}

.empty-card {
  padding: 2rem;
  text-align: center;
  color: #6b7280;
  font-size: 0.95rem;
}

.concepts-table {
  width: 100%;
  border-collapse: collapse;
}

.concepts-table th {
  background: #f9fafb;
  text-align: left;
  padding: 0.7rem 1rem;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #6b7280;
  border-bottom: 1px solid #e5e7eb;
}

.concepts-table td {
  padding: 0.85rem 1rem;
  border-bottom: 1px solid #f3f4f6;
  font-size: 0.92rem;
  color: #374151;
}

.concepts-table tbody tr:last-child td { border-bottom: none; }
.concepts-table tbody tr:hover td { background: #fafafa; }

.td-sno { color: #4f46e5; font-weight: 700; width: 80px; }
.td-sessions { width: 90px; color: #6b7280; }
.td-actions { width: 80px; text-align: right; }

.btn-edit-sm {
  background: #ede9fe;
  color: #4f46e5;
  border: none;
  padding: 0.35rem 0.85rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 600;
  transition: background 0.15s;
}
.btn-edit-sm:hover { background: #ddd6fe; }

/* ---- Loading / Error ---- */
.loading-state {
  text-align: center;
  padding: 4rem 1rem;
  color: #6b7280;
}

.error-box {
  max-width: 500px;
  margin: 2rem auto;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  padding: 1.5rem;
  text-align: center;
  color: #dc2626;
}

.retry-btn {
  margin-top: 1rem;
  background: #4f46e5;
  color: white;
  border: none;
  padding: 0.5rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
}

/* ---- Spinner ---- */
.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #e5e7eb;
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  margin: 0 auto 1rem;
}

.spinner-sm {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255,255,255,0.5);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.6s linear infinite;
  vertical-align: middle;
  margin-right: 4px;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ---- Modal ---- */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.5);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
}

.modal-card {
  background: white;
  border-radius: 12px;
  max-width: 560px;
  width: 90%;
  max-height: 85vh;
  overflow-y: auto;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
  display: flex;
  flex-direction: column;
}

.modal-card--wide {
  max-width: 720px;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.2rem 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  position: sticky;
  top: 0;
  background: white;
  z-index: 1;
}

.modal-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1e1b4b;
  margin: 0;
}

.modal-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #6b7280;
  cursor: pointer;
  line-height: 1;
  padding: 0 0.2rem;
  transition: color 0.15s;
}
.modal-close:hover { color: #1f2937; }

.modal-body {
  padding: 1.5rem;
  flex: 1;
}

.modal-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #e5e7eb;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  position: sticky;
  bottom: 0;
  background: white;
}

/* ---- Tab Bar ---- */
.tab-bar {
  display: flex;
  border-bottom: 1px solid #e5e7eb;
  padding: 0 1.5rem;
  gap: 0;
  background: white;
}

.tab-btn {
  background: none;
  border: none;
  padding: 0.75rem 1.1rem;
  font-size: 0.88rem;
  font-weight: 600;
  color: #6b7280;
  cursor: pointer;
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
  transition: color 0.15s, border-color 0.15s;
}

.tab-btn:hover { color: #4f46e5; }

.tab-btn--active {
  color: #4f46e5;
  border-bottom-color: #4f46e5;
}

/* ---- Form fields ---- */
.field {
  margin-bottom: 1.1rem;
}

.field label {
  display: block;
  font-size: 0.83rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.35rem;
}

.field input[type="text"],
.field input[type="number"],
.field textarea {
  width: 100%;
  padding: 0.5rem 0.75rem;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  font-size: 0.92rem;
  color: #1f2937;
  background: white;
  outline: none;
  transition: border-color 0.15s;
  box-sizing: border-box;
}

.field input:focus,
.field textarea:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.1);
}

.input-sm { max-width: 160px; }

.fields-row {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  align-items: flex-start;
}

.field--sm { min-width: 100px; flex: 0 0 auto; }
.field--sm input { width: 100px; }
.field--grow { flex: 1 1 180px; }

.required { color: #ef4444; }

/* ---- Buttons ---- */
.btn-save {
  background: #4f46e5;
  color: white;
  border: none;
  padding: 0.55rem 1.4rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.92rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  transition: background 0.15s;
}
.btn-save:hover:not(:disabled) { background: #4338ca; }
.btn-save:disabled { opacity: 0.6; cursor: not-allowed; }

.btn-cancel {
  background: #f3f4f6;
  color: #374151;
  border: 1px solid #d1d5db;
  padding: 0.55rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.92rem;
  font-weight: 600;
  transition: background 0.15s;
}
.btn-cancel:hover { background: #e5e7eb; }

/* ---- Inline messages ---- */
.inline-msg {
  font-size: 0.85rem;
  padding: 0.4rem 0.75rem;
  border-radius: 6px;
  margin-top: 0.5rem;
}

.inline-msg.success { background: #d1fae5; color: #065f46; }
.inline-msg.error { background: #fee2e2; color: #991b1b; }

/* ---- Exhibit rows ---- */
.exhibit-row {
  display: flex;
  gap: 0.75rem;
  align-items: flex-start;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #f3f4f6;
}

.exhibit-key-input {
  width: 140px;
  flex-shrink: 0;
  padding: 0.5rem 0.6rem;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  font-size: 0.88rem;
  color: #1f2937;
  outline: none;
  box-sizing: border-box;
}
.exhibit-key-input:focus {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99,102,241,0.1);
}

.exhibit-value-wrap { flex: 1; }

.exhibit-row-actions {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.btn-save-ex {
  background: #d1fae5;
  color: #065f46;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
}
.btn-save-ex:hover:not(:disabled) { background: #a7f3d0; }
.btn-save-ex:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-del-ex {
  background: #fee2e2;
  color: #991b1b;
  border: none;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.15s;
}
.btn-del-ex:hover:not(:disabled) { background: #fecaca; }
.btn-del-ex:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-add-field {
  margin-top: 0.5rem;
  background: #f3f4f6;
  color: #374151;
  border: 1px dashed #d1d5db;
  padding: 0.5rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.88rem;
  font-weight: 600;
  width: 100%;
  transition: background 0.15s;
}
.btn-add-field:hover { background: #e5e7eb; }

/* ---- Images ---- */
.images-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.image-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  padding: 0.6rem;
}

.image-thumb {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 6px;
}

.image-name {
  font-size: 0.72rem;
  color: #6b7280;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.btn-del-img {
  background: #fee2e2;
  color: #991b1b;
  border: none;
  padding: 0.2rem 0.6rem;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.78rem;
  font-weight: 600;
  transition: background 0.15s;
}
.btn-del-img:hover:not(:disabled) { background: #fecaca; }
.btn-del-img:disabled { opacity: 0.5; cursor: not-allowed; }

.upload-zone {
  border: 2px dashed #d1d5db;
  border-radius: 10px;
  padding: 1.5rem;
  text-align: center;
  color: #6b7280;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}
.upload-zone:hover { border-color: #a5b4fc; background: #f5f3ff; }
.upload-zone--drag { border-color: #4f46e5; background: #eef2ff; }

.selected-files-list {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: left;
  display: inline-block;
}
.selected-files-list li { font-size: 0.84rem; color: #374151; padding: 0.15rem 0; }

.btn-upload {
  background: #4f46e5;
  color: white;
  border: none;
  padding: 0.55rem 1.4rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.92rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  transition: background 0.15s;
}
.btn-upload:hover:not(:disabled) { background: #4338ca; }
.btn-upload:disabled { opacity: 0.5; cursor: not-allowed; }

.tab-notice {
  color: #6b7280;
  font-size: 0.9rem;
  padding: 1rem 0;
  text-align: center;
}
</style>
