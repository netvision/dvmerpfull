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
          <button v-if="auth.isAdmin" class="btn-delete-chapter" :disabled="deletingChapter" @click="deleteChapter">
            <span v-if="deletingChapter" class="spinner-sm"></span>
            <span v-else>Delete Chapter</span>
          </button>
        </div>

        <!-- Documents Card -->
        <div class="docs-card">
          <h3 class="docs-title">Chapter Documents</h3>
          <div class="docs-row">
            <!-- PDF Section -->
            <div class="doc-section">
              <div class="doc-label">Chapter PDF</div>
              <div v-if="chapter.pdf_url" class="doc-current">
                <a :href="buildAssetUrl(chapter.pdf_url)" target="_blank" class="pdf-link">&#128196; View current PDF</a>
              </div>
              <div class="doc-upload-row">
                <label class="file-pick-btn">
                  <input type="file" accept=".pdf" style="display:none" @change="onPdfChange" />
                  {{ pdfFile ? pdfFile.name : 'Choose PDF…' }}
                </label>
                <button class="btn-doc-upload" :disabled="!pdfFile || pdfUploading" @click="uploadPdf">
                  <span v-if="pdfUploading" class="spinner-sm"></span>
                  <span v-else>Upload PDF</span>
                </button>
              </div>
              <div v-if="pdfMsg.text" :class="['inline-msg', pdfMsg.type]">{{ pdfMsg.text }}</div>
            </div>

            <!-- xlsx Re-upload Section (admin only) -->
            <div v-if="auth.isAdmin" class="doc-section doc-section--border">
              <div class="doc-label">Re-upload from xlsx</div>
              <div class="doc-note">Replaces all chapter content from an xlsx file.</div>
              <div class="doc-upload-row">
                <label class="file-pick-btn">
                  <input type="file" accept=".xlsx" style="display:none" @change="onXlsxChange" />
                  {{ xlsxFile ? xlsxFile.name : 'Choose xlsx…' }}
                </label>
                <button class="btn-doc-upload btn-doc-upload--warn" :disabled="!xlsxFile || xlsxUploading" @click="uploadXlsx">
                  <span v-if="xlsxUploading" class="spinner-sm"></span>
                  <span v-else>Upload xlsx</span>
                </button>
              </div>
              <div v-if="xlsxMsg.text" :class="['inline-msg', xlsxMsg.type]">{{ xlsxMsg.text }}</div>
            </div>
          </div>
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
            <label>Class</label>
            <select v-model="chapterForm.class_id" @change="onModalClassChange">
              <option value="">Select class</option>
              <option v-for="c in classes" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>
          <div class="field">
            <label>Subject</label>
            <select v-model="chapterForm.subject_id" :disabled="!modalSubjects.length">
              <option value="">{{ chapterForm.class_id ? 'Select subject' : 'Select a class first' }}</option>
              <option v-for="s in modalSubjects" :key="s.id" :value="s.id">{{ formatModalSubjectLabel(s) }}</option>
            </select>
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
                <label>Order</label>
                <input v-model.number="conceptForm.display_order" type="number" />
              </div>
            </div>
            <div class="field">
              <label>Concept Description</label>
              <RichTextEditor v-model="conceptForm.concept_description" placeholder="Concept description…" />
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
              <label>Teaching Materials/Methods</label>
              <RichTextEditor v-model="conceptForm.teaching_materials_methods" placeholder="Teaching materials/methods…" />
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
              <div v-if="!exhibitRows.length" class="tab-notice">No exhibit fields yet.</div>
              <table v-else class="exhibits-table">
                <thead>
                  <tr>
                    <th>Field Key</th>
                    <th>Type</th>
                    <th>Value/File</th>
                    <th style="width: 130px">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(ex, idx) in exhibitRows" :key="ex.id ?? 'new-' + idx">
                    <td class="cell-key">{{ ex.field_key }}</td>
                    <td class="cell-type">
                      <span class="type-badge" :class="ex.field_type">{{ ex.field_type }}</span>
                    </td>
                    <td class="cell-value">
                      <span v-if="ex.field_type === 'string'" class="value-preview">{{ truncate(ex.field_value, 40) }}</span>
                      <span v-else-if="ex.field_type === 'link'" class="value-preview link-preview">{{ truncate(ex.field_value, 40) }}</span>
                      <span v-else class="value-preview">{{ ex.file_key ? '✓ File' : '(no file)' }}</span>
                    </td>
                    <td class="cell-actions">
                      <button
                        class="btn-order-ex"
                        :disabled="idx === 0 || ex.saving || ex.deleting"
                        @click="moveExhibit(idx, -1)"
                        title="Move up"
                      >↑</button>
                      <button
                        class="btn-order-ex"
                        :disabled="idx === exhibitRows.length - 1 || ex.saving || ex.deleting"
                        @click="moveExhibit(idx, 1)"
                        title="Move down"
                      >↓</button>
                      <button class="btn-edit-ex" :disabled="ex.saving" @click="openExhibitModal(ex, idx)" title="Edit">✎</button>
                      <button class="btn-del-ex" :disabled="ex.deleting" @click="deleteExhibit(ex, idx)" title="Delete">
                        <span v-if="ex.deleting" class="spinner-sm"></span>
                        <span v-else>&times;</span>
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
              <button class="btn-add-field" @click="openExhibitModal(null)">+ Add Exhibit Field</button>
            </template>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="showConceptModal = false">Cancel</button>
          <button
            v-if="activeTab === 0 && !isNewConcept"
            class="btn-delete-concept"
            :disabled="deletingConcept"
            @click="deleteConcept"
          >
            <span v-if="deletingConcept" class="spinner-sm"></span>
            <span v-else>Delete</span>
          </button>
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

    <!-- Exhibit Modal -->
    <div v-if="showExhibitModal" class="modal-backdrop">
      <div class="modal-box exhibit-modal-box">
        <div class="modal-header">
          <h2>{{ isNewExhibit ? 'Add Exhibit Field' : 'Edit Exhibit Field' }}</h2>
          <button class="modal-close" @click="showExhibitModal = false">&times;</button>
        </div>

        <div class="modal-body">
          <div class="form-group">
            <label>Field Key *</label>
            <input v-model="exhibitForm.field_key" type="text" placeholder="e.g., video_link, reference" />
          </div>

          <div class="form-group">
            <label>Field Type *</label>
            <div class="field-type-options">
              <label class="type-option" v-for="type in ['string', 'audio', 'image', 'video', 'link']" :key="type">
                <input v-model="exhibitForm.field_type" type="radio" :value="type" />
                <span class="type-label">{{ type === 'string' ? 'Rich Text' : type.charAt(0).toUpperCase() + type.slice(1) }}</span>
              </label>
            </div>
          </div>

          <!-- String Type Input -->
          <div v-if="exhibitForm.field_type === 'string'" class="form-group">
            <label>Value</label>
            <RichTextEditor v-model="exhibitForm.field_value" minHeight="150px" />
          </div>

          <!-- Link Type Input -->
          <div v-if="exhibitForm.field_type === 'link'" class="form-group">
            <label>URL *</label>
            <input v-model="exhibitForm.field_value" type="url" placeholder="https://youtube.com/watch?v=... or other URL" />
            <div class="input-note">Supports YouTube, social media links, and general URLs</div>
          </div>

          <!-- File Upload for Media Types -->
          <div v-if="['audio', 'image', 'video'].includes(exhibitForm.field_type)" class="form-group">
            <label>{{ exhibitForm.field_type.charAt(0).toUpperCase() + exhibitForm.field_type.slice(1) }} File *</label>
            <div class="file-upload-zone" @dragover.prevent="isDraggingExhibit = true" @dragleave="isDraggingExhibit = false" @drop.prevent="onExhibitFileDrop">
              <div v-if="!exhibitForm.selectedFile" class="upload-placeholder">
                <div class="upload-icon">📁</div>
                <p>Drag & drop your {{ exhibitForm.field_type }} file here</p>
                <p class="upload-note">or</p>
                <label class="upload-file-btn">
                  Browse
                  <input type="file" style="display:none" @change="onExhibitFileChange" :accept="getAcceptType(exhibitForm.field_type)" />
                </label>
              </div>
              <div v-else class="upload-preview">
                <div class="preview-icon">✓</div>
                <div class="preview-name">{{ exhibitForm.selectedFile.name }}</div>
                <button type="button" class="preview-remove" @click="exhibitForm.selectedFile = null">Remove</button>
              </div>
            </div>
            <div v-if="exhibitMsg.text" :class="['inline-msg', exhibitMsg.type]">{{ exhibitMsg.text }}</div>
          </div>
        </div>

        <div class="modal-footer">
          <button class="btn-cancel" @click="showExhibitModal = false">Cancel</button>
          <button class="btn-save" :disabled="exhibitSaving" @click="saveExhibit">
            <span v-if="exhibitSaving" class="spinner-sm"></span>
            {{ exhibitSaving ? 'Saving…' : 'Save' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../api.js'
import { useAuthStore } from '../stores/auth.js'
import RichTextEditor from '../components/RichTextEditor.vue'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function buildAssetUrl(path) {
  if (!path) return ''
  return encodeURI(`${API_BASE}${path}`)
}

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const chapterId = computed(() => route.params.id)

// ---- Data ----
const chapter = ref(null)
const loading = ref(true)
const loadError = ref(null)

// ---- Classes / Subjects for chapter modal ----
const classes = ref([])
const modalSubjects = ref([])

async function loadClasses() {
  try {
    const res = await api.get('/api/public/classes')
    classes.value = res.data
  } catch (_) {}
}

async function onModalClassChange() {
  modalSubjects.value = []
  chapterForm.value.subject_id = ''
  if (chapterForm.value.class_id) {
    try {
      const res = await api.get(`/api/public/classes/${chapterForm.value.class_id}/subjects`)
      modalSubjects.value = res.data
    } catch (_) {}
  }
}

function formatModalSubjectLabel(subject) {
  const className = classes.value.find(c => Number(c.id) === Number(chapterForm.value.class_id))?.name
  return className ? `${className} - ${subject.name}` : subject.name
}

// ---- Chapter Modal ----
const showChapterModal = ref(false)
const chapterForm = ref({ title: '', aim: '', order_index: 0, class_id: '', subject_id: '' })
const chapterSaving = ref(false)
const chapterMsg = ref({ text: '', type: '' })

// ---- Concept Modal ----
const showConceptModal = ref(false)
const isNewConcept = ref(false)
const selectedConcept = ref(null)
const activeTab = ref(0)
const conceptTabs = ['Concept Info', 'Exhibit Fields']

const conceptForm = ref({
  s_no: '',
  title: '',
  display_order: 0,
  concept_description: '',
  sessions: '',
  learning_outcomes: '',
  integration_other_sub: '',
  teaching_materials_methods: '',
  library: '',
  activity: '',
  life_lesson: '',
  remarks: '',
})
const conceptSaving = ref(false)
const conceptMsg = ref({ text: '', type: '' })
const deletingConcept = ref(false)
const deletingChapter = ref(false)

// ---- PDF upload ----
const pdfFile = ref(null)
const pdfUploading = ref(false)
const pdfMsg = ref({ text: '', type: '' })

// ---- xlsx re-upload ----
const xlsxFile = ref(null)
const xlsxUploading = ref(false)
const xlsxMsg = ref({ text: '', type: '' })

// ---- Exhibit rows ----
const exhibitRows = ref([])

// ---- Exhibit Modal ----
const showExhibitModal = ref(false)
const isNewExhibit = ref(false)
const exhibitEditingIndex = ref(null)
const exhibitForm = ref({
  field_key: '',
  field_type: 'string',
  field_value: '',
  selectedFile: null,
})
const exhibitSaving = ref(false)
const exhibitMsg = ref({ text: '', type: '' })
const isDraggingExhibit = ref(false)

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
  const classId = chapter.value.class?.id || ''
  const subjectId = chapter.value.subject?.id || ''
  chapterForm.value = {
    title: chapter.value.title || '',
    aim: chapter.value.aim || '',
    order_index: chapter.value.order_index ?? 0,
    class_id: classId,
    subject_id: subjectId,
  }
  if (classId) {
    api.get(`/api/public/classes/${classId}/subjects`)
      .then(res => { modalSubjects.value = res.data })
      .catch(() => {})
  } else {
    modalSubjects.value = []
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
    display_order: concept.display_order ?? 0,
    concept_description: concept.concept_description || '',
    sessions: concept.sessions || '',
    learning_outcomes: concept.learning_outcomes || '',
    integration_other_sub: concept.integration_other_sub || '',
    teaching_materials_methods: concept.teaching_materials_methods || '',
    library: concept.library || '',
    activity: concept.activity || '',
    life_lesson: concept.life_lesson || '',
    remarks: concept.remarks || '',
  }
  conceptMsg.value = { text: '', type: '' }
  activeTab.value = 0
  exhibitRows.value = (concept.exhibits || []).map(ex => ({ ...ex, saving: false, deleting: false }))
  showConceptModal.value = true
  await nextTick()
}

async function openAddConceptModal() {
  isNewConcept.value = true
  selectedConcept.value = null
  conceptForm.value = {
    s_no: '',
    title: '',
    display_order: 0,
    concept_description: '',
    sessions: '',
    learning_outcomes: '',
    integration_other_sub: '',
    teaching_materials_methods: '',
    library: '',
    activity: '',
    life_lesson: '',
    remarks: '',
  }
  conceptMsg.value = { text: '', type: '' }
  activeTab.value = 0
  exhibitRows.value = []
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
function truncate(str, len) {
  if (!str) return ''
  return str.length > len ? str.substring(0, len) + '…' : str
}

function getAcceptType(fieldType) {
  const accepts = {
    audio: 'audio/*',
    image: 'image/*',
    video: 'video/*',
  }
  return accepts[fieldType] || ''
}

function openExhibitModal(exhibit = null, idx = null) {
  isNewExhibit.value = exhibit === null
  exhibitEditingIndex.value = idx
  
  if (isNewExhibit.value) {
    exhibitForm.value = {
      field_key: '',
      field_type: 'string',
      field_value: '',
      selectedFile: null,
    }
  } else {
    exhibitForm.value = {
      field_key: exhibit.field_key || '',
      field_type: exhibit.field_type || 'string',
      field_value: exhibit.field_value || '',
      selectedFile: null, // Can't edit existing files inline
    }
  }
  
  exhibitMsg.value = { text: '', type: '' }
  isDraggingExhibit.value = false
  showExhibitModal.value = true
}

function onExhibitFileChange(e) {
  exhibitForm.value.selectedFile = e.target.files[0] || null
}

function onExhibitFileDrop(e) {
  isDraggingExhibit.value = false
  const files = e.dataTransfer.files
  if (files.length > 0) {
    exhibitForm.value.selectedFile = files[0]
  }
}

async function saveExhibit() {
  if (!selectedConcept.value?.id) return
  
  // Validation
  if (!exhibitForm.value.field_key?.trim()) {
    exhibitMsg.value = { text: 'Field key is required', type: 'error' }
    return
  }
  
  if (exhibitForm.value.field_type === 'link' && !exhibitForm.value.field_value?.trim()) {
    exhibitMsg.value = { text: 'URL is required for link type', type: 'error' }
    return
  }
  
  if (['audio', 'image', 'video'].includes(exhibitForm.value.field_type)) {
    if (isNewExhibit.value && !exhibitForm.value.selectedFile) {
      exhibitMsg.value = { text: `File is required for ${exhibitForm.value.field_type} type`, type: 'error' }
      return
    }
  }
  
  exhibitSaving.value = true
  exhibitMsg.value = { text: '', type: '' }
  
  try {
    const formData = new FormData()
    formData.append('field_key', exhibitForm.value.field_key)
    formData.append('field_type', exhibitForm.value.field_type)
    
    if (exhibitForm.value.field_type === 'string' || exhibitForm.value.field_type === 'link') {
      formData.append('field_value', exhibitForm.value.field_value || '')
    }
    
    if (exhibitForm.value.selectedFile) {
      formData.append('file', exhibitForm.value.selectedFile)
    }
    
    let res
    if (isNewExhibit.value) {
      formData.append('sort_order', String(exhibitRows.value.length))
      res = await api.post(`/api/portal/concepts/${selectedConcept.value.id}/exhibits`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      exhibitRows.value.push({
        ...res.data,
        saving: false,
        deleting: false,
      })
    } else {
      const currentExhibit = exhibitRows.value[exhibitEditingIndex.value]
      res = await api.put(`/api/portal/exhibits/${currentExhibit.id}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      Object.assign(currentExhibit, {
        ...res.data,
        saving: false,
        deleting: false,
      })
    }
    
    exhibitMsg.value = { text: 'Saved!', type: 'success' }
    setTimeout(() => {
      showExhibitModal.value = false
      exhibitMsg.value = { text: '', type: '' }
    }, 800)
  } catch (e) {
    exhibitMsg.value = { text: e.response?.data?.detail || 'Save failed', type: 'error' }
  } finally {
    exhibitSaving.value = false
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
    await persistExhibitOrder()
  } catch (e) {
    alert(e.response?.data?.detail || 'Delete failed')
    ex.deleting = false
  }
}

async function persistExhibitOrder() {
  const updates = exhibitRows.value
    .map((ex, idx) => ({ ex, idx }))
    .filter(({ ex, idx }) => ex.id && ex.sort_order !== idx)

  if (!updates.length) return

  await Promise.all(updates.map(async ({ ex, idx }) => {
    ex.saving = true
    try {
      const formData = new FormData()
      formData.append('sort_order', String(idx))
      const res = await api.put(`/api/portal/exhibits/${ex.id}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      Object.assign(ex, {
        ...res.data,
        saving: false,
        deleting: false,
      })
    } catch (e) {
      ex.saving = false
      throw e
    }
  }))
}

async function moveExhibit(idx, direction) {
  const newIdx = idx + direction
  if (newIdx < 0 || newIdx >= exhibitRows.value.length) return

  const snapshot = exhibitRows.value.map(ex => ({ ...ex }))
  const [moved] = exhibitRows.value.splice(idx, 1)
  exhibitRows.value.splice(newIdx, 0, moved)

  try {
    await persistExhibitOrder()
  } catch (e) {
    exhibitRows.value = snapshot
    alert(e.response?.data?.detail || 'Failed to reorder exhibit fields')
  }
}

onMounted(async () => {
  await Promise.all([fetchChapter(), loadClasses()])
})

async function deleteChapter() {
  if (!confirm(`Delete chapter "${chapter.value.title}"? This will permanently remove all its concepts, exhibits, and images.`)) return
  deletingChapter.value = true
  try {
    await api.delete(`/api/portal/chapters/${chapterId.value}`)
    router.replace('/portal')
  } catch (e) {
    alert(e.response?.data?.detail || 'Delete failed')
    deletingChapter.value = false
  }
}

async function deleteConcept() {
  if (!selectedConcept.value?.id) return
  if (!confirm(`Delete concept "${selectedConcept.value.title}"? This cannot be undone.`)) return
  deletingConcept.value = true
  try {
    await api.delete(`/api/portal/concepts/${selectedConcept.value.id}`)
    chapter.value.concepts = chapter.value.concepts.filter(c => c.id !== selectedConcept.value.id)
    showConceptModal.value = false
  } catch (e) {
    alert(e.response?.data?.detail || 'Delete failed')
  } finally {
    deletingConcept.value = false
  }
}

// ---- PDF upload ----
function onPdfChange(e) {
  pdfFile.value = e.target.files[0] || null
  pdfMsg.value = { text: '', type: '' }
}

async function uploadPdf() {
  if (!pdfFile.value) return
  pdfUploading.value = true
  pdfMsg.value = { text: '', type: '' }
  try {
    const fd = new FormData()
    fd.append('file', pdfFile.value)
    const res = await api.post(`/api/portal/chapters/${chapterId.value}/pdf`, fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    chapter.value.pdf_url = res.data.pdf_url
    pdfFile.value = null
    pdfMsg.value = { text: 'PDF uploaded!', type: 'success' }
    setTimeout(() => { pdfMsg.value = { text: '', type: '' } }, 2000)
  } catch (e) {
    pdfMsg.value = { text: e.response?.data?.detail || 'Upload failed', type: 'error' }
  } finally {
    pdfUploading.value = false
  }
}

// ---- xlsx re-upload ----
function onXlsxChange(e) {
  xlsxFile.value = e.target.files[0] || null
  xlsxMsg.value = { text: '', type: '' }
}

async function uploadXlsx() {
  if (!xlsxFile.value || !chapter.value?.subject?.id) return
  if (!confirm('Re-uploading xlsx will replace ALL concepts and exhibits for this chapter. Continue?')) return
  xlsxUploading.value = true
  xlsxMsg.value = { text: '', type: '' }
  try {
    const fd = new FormData()
    fd.append('file', xlsxFile.value)
    fd.append('subject_id', chapter.value.subject.id)
    await api.post('/api/portal/upload', fd, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    xlsxFile.value = null
    xlsxMsg.value = { text: 'Upload successful — reloading chapter…', type: 'success' }
    await fetchChapter()
    xlsxMsg.value = { text: '', type: '' }
  } catch (e) {
    xlsxMsg.value = { text: e.response?.data?.detail || 'Upload failed', type: 'error' }
  } finally {
    xlsxUploading.value = false
  }
}
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
  background: #1e3a8a;
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
  margin-bottom: 1.25rem;
}

/* ---- Documents Card ---- */
.docs-card {
  background: white;
  border-radius: 12px;
  padding: 1.2rem 1.6rem 1.4rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.07);
  margin-bottom: 2rem;
}

.docs-title {
  font-size: 0.9rem;
  font-weight: 700;
  color: #1e3a8a;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  margin: 0 0 1rem;
}

.docs-row {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.doc-section {
  flex: 1;
  min-width: 220px;
}

.doc-section--border {
  padding-left: 2rem;
  border-left: 1px solid #e5e7eb;
}

.doc-label {
  font-size: 0.83rem;
  font-weight: 700;
  color: #374151;
  margin-bottom: 0.4rem;
}

.doc-note {
  font-size: 0.8rem;
  color: #9ca3af;
  margin-bottom: 0.6rem;
}

.doc-current {
  margin-bottom: 0.6rem;
}

.pdf-link {
  color: #2563eb;
  font-size: 0.85rem;
  font-weight: 600;
  text-decoration: none;
}
.pdf-link:hover { text-decoration: underline; }

.doc-upload-row {
  display: flex;
  gap: 0.5rem;
  align-items: center;
  flex-wrap: wrap;
}

.file-pick-btn {
  display: inline-block;
  padding: 0.4rem 0.9rem;
  background: #f1f5f9;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 500;
  color: #374151;
  max-width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  transition: background 0.15s;
}
.file-pick-btn:hover { background: #e2e8f0; }

.btn-doc-upload {
  padding: 0.4rem 0.9rem;
  background: #1e3a8a;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  transition: background 0.15s;
}
.btn-doc-upload:hover { background: #1d4ed8; }
.btn-doc-upload:disabled { opacity: 0.55; cursor: not-allowed; }

.btn-doc-upload--warn {
  background: #92400e;
}
.btn-doc-upload--warn:hover { background: #b45309; }

.summary-title {
  font-size: 1.3rem;
  font-weight: 800;
  color: #1e3a8a;
  margin-bottom: 0.4rem;
}

.summary-meta {
  display: flex;
  gap: 0.5rem;
  flex-wrap: wrap;
}

.meta-badge {
  background: #eff6ff;
  color: #2563eb;
  font-size: 0.8rem;
  font-weight: 600;
  padding: 0.2rem 0.7rem;
  border-radius: 20px;
}

.btn-edit-chapter {
  background: #2563eb;
  color: white;
  border: none;
  padding: 0.55rem 1.2rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: background 0.15s;
}
.btn-edit-chapter:hover { background: #1d4ed8; }

.btn-delete-chapter {
  background: #fee2e2;
  color: #dc2626;
  border: 1.5px solid #fca5a5;
  padding: 0.55rem 1.1rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.88rem;
  font-weight: 600;
  transition: all 0.15s;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
}
.btn-delete-chapter:hover { background: #fecaca; border-color: #f87171; }
.btn-delete-chapter:disabled { opacity: 0.6; cursor: not-allowed; }

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
  color: #1e3a8a;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0;
}

.count-badge {
  background: #dbeafe;
  color: #1d4ed8;
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

.td-sno { color: #2563eb; font-weight: 700; width: 80px; }
.td-sessions { width: 90px; color: #6b7280; }
.td-actions { width: 80px; text-align: right; }

.btn-edit-sm {
  background: #ede9fe;
  color: #2563eb;
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
  background: #2563eb;
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
  border-top-color: #2563eb;
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

.modal-card,
.modal-box {
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
  color: #1e3a8a;
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

.tab-btn:hover { color: #2563eb; }

.tab-btn--active {
  color: #2563eb;
  border-bottom-color: #2563eb;
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
  background: #2563eb;
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
.btn-save:hover:not(:disabled) { background: #1d4ed8; }
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

.btn-delete-concept {
  background: #fee2e2;
  color: #dc2626;
  border: 1.5px solid #fca5a5;
  padding: 0.55rem 1.1rem;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.92rem;
  font-weight: 600;
  transition: all 0.15s;
  display: inline-flex;
  align-items: center;
  gap: 0.4rem;
  margin-right: auto;
}
.btn-delete-concept:hover { background: #fecaca; border-color: #f87171; }
.btn-delete-concept:disabled { opacity: 0.6; cursor: not-allowed; }

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
.upload-zone--drag { border-color: #2563eb; background: #eff6ff; }

.selected-files-list {
  list-style: none;
  padding: 0;
  margin: 0;
  text-align: left;
  display: inline-block;
}
.selected-files-list li { font-size: 0.84rem; color: #374151; padding: 0.15rem 0; }

.btn-upload {
  background: #2563eb;
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
.btn-upload:hover:not(:disabled) { background: #1d4ed8; }
.btn-upload:disabled { opacity: 0.5; cursor: not-allowed; }

.tab-notice {
  color: #6b7280;
  font-size: 0.9rem;
  padding: 1rem 0;
  text-align: center;
}

/* ---- Exhibits Table ---- */
.exhibits-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
  margin-bottom: 1rem;
}

.exhibits-table thead {
  background: #f9fafb;
  border-bottom: 2px solid #e5e7eb;
}

.exhibits-table th {
  padding: 0.7rem 0.9rem;
  text-align: left;
  font-weight: 600;
  color: #374151;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.exhibits-table td {
  padding: 0.8rem 0.9rem;
  border-bottom: 1px solid #e5e7eb;
  vertical-align: top;
}

.exhibits-table tbody tr:hover {
  background: #f3f4f6;
}

.cell-key {
  font-weight: 600;
  color: #1e3a8a;
  max-width: 150px;
  word-break: break-word;
}

.cell-type {
  text-align: center;
}

.type-badge {
  display: inline-block;
  padding: 0.25rem 0.6rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
}

.type-badge.string {
  background: #dbeafe;
  color: #1e40af;
}

.type-badge.audio {
  background: #fce7f3;
  color: #be123c;
}

.type-badge.image {
  background: #dcfce7;
  color: #166534;
}

.type-badge.video {
  background: #fed7aa;
  color: #92400e;
}

.type-badge.link {
  background: #f3e8ff;
  color: #6b21a8;
}

.cell-value {
  max-width: 250px;
  word-break: break-word;
}

.value-preview {
  display: block;
  color: #6b7280;
  font-size: 0.85rem;
  line-height: 1.4;
}

.value-preview.link-preview {
  color: #2563eb;
  text-decoration: underline;
}

.cell-actions {
  text-align: right;
  white-space: nowrap;
}

.btn-order-ex {
  padding: 0.3rem 0.45rem;
  background: #f8fafc;
  color: #334155;
  border: 1px solid #cbd5e1;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 700;
  transition: all 0.15s;
  margin-right: 0.25rem;
}

.btn-order-ex:hover:not(:disabled) {
  background: #e2e8f0;
}

.btn-order-ex:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.btn-edit-ex {
  padding: 0.3rem 0.6rem;
  background: #dbeafe;
  color: #1e40af;
  border: 1px solid #93c5fd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.15s;
  margin-right: 0.3rem;
}

.btn-edit-ex:hover {
  background: #bfdbfe;
}

.btn-edit-ex:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-del-ex {
  padding: 0.3rem 0.5rem;
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #fecaca;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: 700;
  transition: all 0.15s;
}

.btn-del-ex:hover {
  background: #fecaca;
}

.btn-del-ex:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-add-field {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #dbeafe;
  color: #0c4a6e;
  border: 2px dashed #3b82f6;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  font-weight: 600;
  transition: all 0.15s;
  margin-top: 1rem;
}

.btn-add-field:hover {
  background: #bfdbfe;
  border-color: #2563eb;
}

/* ---- Exhibit Modal ---- */
.exhibit-modal-box {
  width: min(90vw, 760px);
  max-width: 95vw;
  max-height: 90vh;
  min-width: 420px;
  min-height: 360px;
  resize: both;
  overflow: auto;
}

.exhibit-modal-box .modal-body {
  overflow: auto;
}

@media (max-width: 640px) {
  .exhibit-modal-box {
    width: 100%;
    min-width: 0;
    min-height: 0;
    max-height: 92vh;
    resize: none;
  }
}

/* ---- Form Styling ---- */
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.2rem;
}

.form-group label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #374151;
  display: block;
}

.form-group input[type="text"],
.form-group input[type="url"],
.form-group input[type="number"],
.form-group textarea {
  padding: 0.6rem 0.8rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.9rem;
  font-family: inherit;
  background: white;
  color: #1f2937;
  transition: border-color 0.15s, box-shadow 0.15s;
}

.form-group input[type="text"]:focus,
.form-group input[type="url"]:focus,
.form-group input[type="number"]:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.field-type-options {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  margin: 0.5rem 0;
}

.type-option {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
}

.type-option input[type="radio"] {
  cursor: pointer;
}

.type-label {
  font-weight: 500;
  color: #374151;
  cursor: pointer;
}

.type-option input[type="radio"]:checked + .type-label {
  color: #1e3a8a;
  font-weight: 600;
}

.input-note {
  font-size: 0.8rem;
  color: #9ca3af;
  margin-top: 0.4rem;
}

.file-upload-zone {
  border: 2px dashed #cbd5e1;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  background: #f8fafc;
  cursor: pointer;
  transition: all 0.15s;
}

.file-upload-zone:hover,
.file-upload-zone.dragging {
  border-color: #3b82f6;
  background: #eff6ff;
}

.upload-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
}

.upload-icon {
  font-size: 2.5rem;
}

.upload-placeholder p {
  margin: 0;
  color: #6b7280;
  font-size: 0.9rem;
}

.upload-note {
  color: #d1d5db !important;
  font-size: 0.85rem !important;
}

.upload-file-btn {
  display: inline-block;
  padding: 0.5rem 1rem;
  background: #3b82f6;
  color: white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.9rem;
  transition: background 0.15s;
}

.upload-file-btn:hover {
  background: #2563eb;
}

.upload-preview {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.8rem;
}

.preview-icon {
  font-size: 2rem;
  color: #10b981;
}

.preview-name {
  font-weight: 600;
  color: #374151;
  word-break: break-word;
  max-width: 100%;
}

.preview-remove {
  padding: 0.3rem 0.8rem;
  background: #fee2e2;
  color: #dc2626;
  border: 1px solid #fecaca;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  font-weight: 600;
  transition: all 0.15s;
}

.preview-remove:hover {
  background: #fecaca;
}

/* DVM redesign overlay: aligns the existing editor with the approved portal direction. */
.page {
  background: var(--dvm-bg);
  font-family: var(--dvm-font);
}

.navbar {
  background: #fff;
  color: var(--dvm-text);
  border-bottom: 1px solid var(--dvm-line);
  box-shadow: none;
}

.nav-title {
  color: var(--dvm-navy);
  font-weight: 900;
}

.back-btn {
  background: #fff;
  color: var(--dvm-navy);
  border: 1px solid var(--dvm-line);
}

.content {
  max-width: 1120px;
}

.summary-card,
.docs-card,
.concepts-table-wrap {
  border: 1px solid var(--dvm-line);
  border-radius: var(--dvm-radius-lg);
  box-shadow: var(--dvm-shadow-soft);
}

.summary-title,
.section-title {
  color: var(--dvm-text);
}

.meta-badge,
.count-badge {
  background: var(--dvm-blue-soft);
  color: var(--dvm-navy);
}

.concepts-table th {
  background: #f8fafc;
  color: var(--dvm-muted);
}

.concepts-table td {
  border-bottom-color: var(--dvm-line);
}

.modal-card--wide {
  width: min(1180px, calc(100vw - 42px));
  max-height: min(780px, calc(100vh - 42px));
  display: grid;
  grid-template-columns: 230px minmax(0, 1fr);
  grid-template-rows: auto minmax(0, 1fr) auto;
  overflow: hidden;
  border: 1px solid var(--dvm-line);
  border-radius: 10px;
  box-shadow: 0 28px 80px rgba(15, 23, 42, 0.28);
}

.modal-card--wide .modal-header {
  grid-column: 1 / -1;
  background: #fbfcfe;
  border-bottom: 1px solid var(--dvm-line);
}

.modal-card--wide .tab-bar {
  grid-row: 2;
  grid-column: 1;
  display: block;
  padding: 0.9rem;
  background: #fff;
  border-right: 1px solid var(--dvm-line);
  border-bottom: 0;
  overflow-y: auto;
}

.modal-card--wide .tab-bar::before {
  content: "Editor sections";
  display: block;
  margin: 0.1rem 0.45rem 0.55rem;
  color: var(--dvm-muted);
  font-size: 0.68rem;
  font-weight: 900;
  letter-spacing: 0.07em;
  text-transform: uppercase;
}

.modal-card--wide .tab-btn {
  width: 100%;
  justify-content: flex-start;
  margin-bottom: 0.3rem;
  border-radius: 7px;
  border: 0;
  color: var(--dvm-text);
  text-align: left;
}

.modal-card--wide .tab-btn--active {
  background: var(--dvm-blue-soft);
  color: var(--dvm-navy);
  box-shadow: inset 3px 0 0 var(--dvm-blue);
}

.modal-card--wide .modal-body {
  grid-row: 2;
  grid-column: 2;
  min-height: 0;
  overflow-y: auto;
  background: var(--dvm-bg);
  padding: 1rem;
}

.modal-card--wide .modal-body > div {
  background: #fff;
  border: 1px solid var(--dvm-line);
  border-radius: var(--dvm-radius-lg);
  padding: 1rem;
}

.modal-card--wide .fields-row {
  display: grid;
  grid-template-columns: 100px minmax(220px, 1fr) 110px 100px;
  gap: 0.75rem;
}

.modal-card--wide .field label {
  color: #475569;
  font-size: 0.76rem;
  font-weight: 850;
}

.modal-card--wide .field input,
.modal-card--wide .field select,
.modal-card--wide .field textarea {
  border-color: var(--dvm-line);
  border-radius: 7px;
}

.modal-card--wide .modal-footer {
  grid-column: 1 / -1;
  border-top: 1px solid var(--dvm-line);
  background: #fff;
}

@media (max-width: 900px) {
  .modal-card--wide {
    grid-template-columns: 1fr;
  }

  .modal-card--wide .tab-bar {
    grid-column: 1;
    display: flex;
    border-right: 0;
    border-bottom: 1px solid var(--dvm-line);
  }

  .modal-card--wide .tab-bar::before {
    display: none;
  }

  .modal-card--wide .modal-body {
    grid-column: 1;
  }

  .modal-card--wide .fields-row {
    grid-template-columns: 1fr;
  }
}
</style>
