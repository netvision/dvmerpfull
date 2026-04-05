<template>
  <div class="page">
    <!-- Navbar -->
    <nav class="navbar">
      <span class="nav-title">Editing Chapter</span>
      <button class="back-btn" @click="router.push('/portal')">&#8592; Back to Portal</button>
    </nav>

    <div class="content">
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

        <!-- Chapter Fields Card (collapsible) -->
        <div class="card">
          <div class="card-heading collapsible" @click="chapterOpen = !chapterOpen">
            <span>Chapter Details</span>
            <span class="toggle-icon">{{ chapterOpen ? '▲' : '▼' }}</span>
          </div>

          <transition name="slide">
            <div v-if="chapterOpen">
              <div class="field">
                <label>Title</label>
                <input v-model="chapterForm.title" type="text" placeholder="Chapter title" />
              </div>
              <div class="field">
                <label>Aim</label>
                <textarea v-model="chapterForm.aim" rows="4" placeholder="Chapter aim / objective"></textarea>
              </div>
              <div class="field">
                <label>Order Index</label>
                <input v-model.number="chapterForm.order_index" type="number" min="0" />
              </div>

              <div v-if="chapterMsg.text" :class="['inline-msg', chapterMsg.type]">{{ chapterMsg.text }}</div>

              <div class="form-actions">
                <button class="btn-save" :disabled="chapterSaving" @click="saveChapter">
                  <span v-if="chapterSaving" class="spinner-sm"></span>
                  {{ chapterSaving ? 'Saving…' : 'Save Chapter' }}
                </button>
              </div>
            </div>
          </transition>
        </div>

        <!-- Concepts Section -->
        <div class="concepts-header">
          <h2 class="section-title">
            Concepts
            <span class="count-badge">{{ chapter.concepts?.length || 0 }} total</span>
          </h2>
          <button class="btn-add" @click="addConcept">+ Add Concept</button>
        </div>

        <!-- No concepts yet -->
        <div v-if="!chapter.concepts?.length && !newConceptOpen" class="card empty-card">
          <p class="no-concepts">No concepts yet. Click "+ Add Concept" to create one.</p>
        </div>

        <!-- New Concept Form -->
        <div v-if="newConceptOpen" class="card concept-card">
          <div class="concept-card-header">
            <span class="concept-header-info">
              <span class="badge-sno">New</span>
              <span class="concept-header-title">New Concept</span>
            </span>
            <div class="concept-header-actions">
              <button class="btn-save-sm" :disabled="newConceptSaving" @click="saveNewConcept">
                <span v-if="newConceptSaving" class="spinner-sm"></span>
                {{ newConceptSaving ? 'Saving…' : 'Save' }}
              </button>
              <button class="btn-cancel-sm" @click="newConceptOpen = false">Cancel</button>
            </div>
          </div>
          <div class="concept-fields-grid">
            <div class="field">
              <label>S.No</label>
              <input v-model="newConceptForm.s_no" type="text" placeholder="e.g. 1.1" />
            </div>
            <div class="field">
              <label>Title <span class="required">*</span></label>
              <input v-model="newConceptForm.title" type="text" placeholder="Concept title" required />
            </div>
            <div class="field">
              <label>Sessions</label>
              <input v-model="newConceptForm.sessions" type="text" placeholder="e.g. 2" />
            </div>
            <div class="field">
              <label>Exhibit Ref</label>
              <input v-model="newConceptForm.exhibit_ref" type="text" placeholder="e.g. exhibit_1" />
            </div>
            <div class="field full-width">
              <label>Learning Outcomes</label>
              <textarea v-model="newConceptForm.learning_outcomes" rows="3"></textarea>
            </div>
            <div class="field full-width">
              <label>Integration / Other Subjects</label>
              <textarea v-model="newConceptForm.integration_other_sub" rows="3"></textarea>
            </div>
            <div class="field full-width">
              <label>Library</label>
              <textarea v-model="newConceptForm.library" rows="3"></textarea>
            </div>
            <div class="field full-width">
              <label>Activity</label>
              <textarea v-model="newConceptForm.activity" rows="3"></textarea>
            </div>
            <div class="field full-width">
              <label>Life Lesson</label>
              <textarea v-model="newConceptForm.life_lesson" rows="3"></textarea>
            </div>
            <div class="field full-width">
              <label>Remarks</label>
              <textarea v-model="newConceptForm.remarks" rows="3"></textarea>
            </div>
          </div>
          <div v-if="newConceptMsg.text" :class="['inline-msg', newConceptMsg.type]">{{ newConceptMsg.text }}</div>
        </div>

        <!-- Existing Concept Cards -->
        <div
          v-for="(concept, ci) in chapter.concepts"
          :key="concept.id"
          class="card concept-card"
        >
          <!-- Card Header (always visible) -->
          <div class="concept-card-header" @click="toggleConcept(concept.id)">
            <span class="concept-header-info">
              <span class="badge-sno">{{ concept.s_no || '—' }}</span>
              <span class="concept-header-title">{{ concept.title }}</span>
              <span class="badge-sessions">{{ concept.sessions || '?' }} sess.</span>
            </span>
            <div class="concept-header-actions" @click.stop>
              <template v-if="editingConceptId === concept.id">
                <button class="btn-save-sm" :disabled="conceptSaving[concept.id]" @click="saveConceptEdit(concept)">
                  <span v-if="conceptSaving[concept.id]" class="spinner-sm"></span>
                  {{ conceptSaving[concept.id] ? 'Saving…' : 'Save' }}
                </button>
                <button class="btn-cancel-sm" @click="cancelConceptEdit(concept.id)">Cancel</button>
              </template>
              <template v-else>
                <button class="btn-edit-sm" @click="startConceptEdit(concept)">Edit</button>
                <button
                  v-if="auth.isAdmin"
                  class="btn-delete-sm"
                  @click="deleteConcept(concept, ci)"
                >Delete</button>
              </template>
              <span class="expand-icon">{{ expandedConcepts.has(concept.id) ? '▲' : '▼' }}</span>
            </div>
          </div>

          <!-- Expanded Body -->
          <transition name="slide">
            <div v-if="expandedConcepts.has(concept.id)" class="concept-body">

              <!-- Concept Edit Fields -->
              <div class="concept-fields-grid">
                <div class="field">
                  <label>S.No</label>
                  <input
                    :value="conceptForms[concept.id]?.s_no ?? concept.s_no"
                    :readonly="editingConceptId !== concept.id"
                    @input="setConceptField(concept.id, 's_no', $event.target.value)"
                    type="text"
                    :class="{ readonly: editingConceptId !== concept.id }"
                  />
                </div>
                <div class="field">
                  <label>Title <span class="required">*</span></label>
                  <input
                    :value="conceptForms[concept.id]?.title ?? concept.title"
                    :readonly="editingConceptId !== concept.id"
                    @input="setConceptField(concept.id, 'title', $event.target.value)"
                    type="text"
                    :class="{ readonly: editingConceptId !== concept.id }"
                  />
                </div>
                <div class="field">
                  <label>Sessions</label>
                  <input
                    :value="conceptForms[concept.id]?.sessions ?? concept.sessions"
                    :readonly="editingConceptId !== concept.id"
                    @input="setConceptField(concept.id, 'sessions', $event.target.value)"
                    type="text"
                    :class="{ readonly: editingConceptId !== concept.id }"
                  />
                </div>
                <div class="field">
                  <label>Exhibit Ref</label>
                  <input
                    :value="conceptForms[concept.id]?.exhibit_ref ?? concept.exhibit_ref"
                    :readonly="editingConceptId !== concept.id"
                    @input="setConceptField(concept.id, 'exhibit_ref', $event.target.value)"
                    type="text"
                    placeholder="e.g. exhibit_1"
                    :class="{ readonly: editingConceptId !== concept.id }"
                  />
                </div>
                <div class="field full-width">
                  <label>Learning Outcomes</label>
                  <textarea
                    :value="conceptForms[concept.id]?.learning_outcomes ?? concept.learning_outcomes"
                    :readonly="editingConceptId !== concept.id"
                    @input="setConceptField(concept.id, 'learning_outcomes', $event.target.value)"
                    rows="3"
                    :class="{ readonly: editingConceptId !== concept.id }"
                  ></textarea>
                </div>
                <div class="field full-width">
                  <label>Integration / Other Subjects</label>
                  <textarea
                    :value="conceptForms[concept.id]?.integration_other_sub ?? concept.integration_other_sub"
                    :readonly="editingConceptId !== concept.id"
                    @input="setConceptField(concept.id, 'integration_other_sub', $event.target.value)"
                    rows="3"
                    :class="{ readonly: editingConceptId !== concept.id }"
                  ></textarea>
                </div>
                <div class="field full-width">
                  <label>Library</label>
                  <textarea
                    :value="conceptForms[concept.id]?.library ?? concept.library"
                    :readonly="editingConceptId !== concept.id"
                    @input="setConceptField(concept.id, 'library', $event.target.value)"
                    rows="3"
                    :class="{ readonly: editingConceptId !== concept.id }"
                  ></textarea>
                </div>
                <div class="field full-width">
                  <label>Activity</label>
                  <textarea
                    :value="conceptForms[concept.id]?.activity ?? concept.activity"
                    :readonly="editingConceptId !== concept.id"
                    @input="setConceptField(concept.id, 'activity', $event.target.value)"
                    rows="3"
                    :class="{ readonly: editingConceptId !== concept.id }"
                  ></textarea>
                </div>
                <div class="field full-width">
                  <label>Life Lesson</label>
                  <textarea
                    :value="conceptForms[concept.id]?.life_lesson ?? concept.life_lesson"
                    :readonly="editingConceptId !== concept.id"
                    @input="setConceptField(concept.id, 'life_lesson', $event.target.value)"
                    rows="3"
                    :class="{ readonly: editingConceptId !== concept.id }"
                  ></textarea>
                </div>
                <div class="field full-width">
                  <label>Remarks</label>
                  <textarea
                    :value="conceptForms[concept.id]?.remarks ?? concept.remarks"
                    :readonly="editingConceptId !== concept.id"
                    @input="setConceptField(concept.id, 'remarks', $event.target.value)"
                    rows="3"
                    :class="{ readonly: editingConceptId !== concept.id }"
                  ></textarea>
                </div>
              </div>

              <div v-if="conceptMsgs[concept.id]?.text" :class="['inline-msg', conceptMsgs[concept.id].type]">
                {{ conceptMsgs[concept.id].text }}
              </div>

              <!-- Exhibit Fields -->
              <div class="exhibits-section">
                <h4 class="exhibits-heading">Exhibit Fields</h4>

                <div
                  v-for="(ex, ei) in concept.exhibits"
                  :key="ex.id"
                  class="exhibit-row"
                >
                  <div class="exhibit-row-inputs">
                    <input
                      v-model="ex.field_key"
                      class="exhibit-key-input"
                      placeholder="e.g. explanation"
                      @blur="saveExhibit(ex, concept.id)"
                    />
                    <textarea
                      v-model="ex.field_value"
                      class="exhibit-value-input"
                      rows="2"
                      placeholder="Field value…"
                      @blur="saveExhibit(ex, concept.id)"
                    ></textarea>
                  </div>
                  <div class="exhibit-row-actions">
                    <button
                      class="btn-icon btn-icon-save"
                      :disabled="exhibitSaving[ex.id]"
                      :title="'Save field'"
                      @click="saveExhibit(ex, concept.id)"
                    >
                      <span v-if="exhibitSaving[ex.id]" class="spinner-sm dark"></span>
                      <span v-else>&#10003;</span>
                    </button>
                    <button
                      class="btn-icon btn-icon-delete"
                      title="Delete field"
                      @click="deleteExhibit(ex, concept, ei)"
                    >&#10005;</button>
                  </div>
                  <div v-if="exhibitMsgs[ex.id]?.text" :class="['inline-msg exhibit-msg', exhibitMsgs[ex.id].type]">
                    {{ exhibitMsgs[ex.id].text }}
                  </div>
                </div>

                <button class="btn-add-field" @click="addExhibitRow(concept)">+ Add Field</button>
              </div>

            </div>
          </transition>
        </div>

        <!-- Bottom hint -->
        <p class="upload-hint">To replace all content at once, use xlsx upload instead.</p>

      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../api.js'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const chapterId = computed(() => route.params.id)

// ── State ──────────────────────────────────────────────────────────────
const chapter    = ref(null)
const loading    = ref(true)
const loadError  = ref('')

const chapterOpen   = ref(true)
const chapterForm   = reactive({ title: '', aim: '', order_index: 0 })
const chapterSaving = ref(false)
const chapterMsg    = reactive({ text: '', type: '' })

const expandedConcepts  = reactive(new Set())
const editingConceptId  = ref(null)
const conceptForms      = reactive({})   // { [id]: { ...fields } }
const conceptSaving     = reactive({})   // { [id]: bool }
const conceptMsgs       = reactive({})   // { [id]: { text, type } }

const newConceptOpen   = ref(false)
const newConceptSaving = ref(false)
const newConceptMsg    = reactive({ text: '', type: '' })
const newConceptForm   = reactive({
  s_no: '', title: '', sessions: '', exhibit_ref: '',
  learning_outcomes: '', integration_other_sub: '',
  library: '', activity: '', life_lesson: '', remarks: '',
})

const exhibitSaving = reactive({})   // { [exhibitId]: bool }
const exhibitMsgs   = reactive({})   // { [exhibitId]: { text, type } }

// ── Lifecycle ──────────────────────────────────────────────────────────
onMounted(fetchChapter)

// ── Chapter fetch ──────────────────────────────────────────────────────
async function fetchChapter() {
  loading.value  = true
  loadError.value = ''
  try {
    const res = await api.get(`/api/portal/chapters/${chapterId.value}`)
    chapter.value = res.data
    chapterForm.title       = res.data.title       || ''
    chapterForm.aim         = res.data.aim          || ''
    chapterForm.order_index = res.data.order_index  ?? 0
  } catch (e) {
    loadError.value = e.response?.data?.detail || 'Failed to load chapter.'
  } finally {
    loading.value = false
  }
}

// ── Chapter save ───────────────────────────────────────────────────────
async function saveChapter() {
  chapterSaving.value = true
  chapterMsg.text = ''
  try {
    await api.put(`/api/portal/chapters/${chapterId.value}`, {
      title:       chapterForm.title,
      aim:         chapterForm.aim,
      order_index: chapterForm.order_index,
    })
    chapterMsg.type = 'success'
    chapterMsg.text = 'Chapter saved!'
    if (chapter.value) {
      chapter.value.title       = chapterForm.title
      chapter.value.aim         = chapterForm.aim
      chapter.value.order_index = chapterForm.order_index
    }
    setTimeout(() => { chapterMsg.text = '' }, 3000)
  } catch (e) {
    chapterMsg.type = 'error'
    chapterMsg.text = e.response?.data?.detail || 'Failed to save.'
  } finally {
    chapterSaving.value = false
  }
}

// ── Concept expand/collapse ────────────────────────────────────────────
function toggleConcept(id) {
  if (expandedConcepts.has(id)) {
    expandedConcepts.delete(id)
  } else {
    expandedConcepts.add(id)
  }
}

// ── Concept edit ───────────────────────────────────────────────────────
function startConceptEdit(concept) {
  editingConceptId.value = concept.id
  conceptForms[concept.id] = {
    s_no:                  concept.s_no                  || '',
    title:                 concept.title                 || '',
    sessions:              concept.sessions              || '',
    exhibit_ref:           concept.exhibit_ref           || '',
    learning_outcomes:     concept.learning_outcomes     || '',
    integration_other_sub: concept.integration_other_sub || '',
    library:               concept.library               || '',
    activity:              concept.activity              || '',
    life_lesson:           concept.life_lesson           || '',
    remarks:               concept.remarks               || '',
  }
  expandedConcepts.add(concept.id)
}

function cancelConceptEdit(id) {
  editingConceptId.value = null
  delete conceptForms[id]
}

function setConceptField(id, key, value) {
  if (!conceptForms[id]) return
  conceptForms[id][key] = value
}

async function saveConceptEdit(concept) {
  const form = conceptForms[concept.id]
  if (!form) return
  if (!form.title?.trim()) {
    setConceptMsg(concept.id, 'error', 'Title is required.')
    return
  }
  conceptSaving[concept.id] = true
  clearConceptMsg(concept.id)
  try {
    await api.put(`/api/portal/concepts/${concept.id}`, {
      s_no:                  form.s_no,
      title:                 form.title,
      sessions:              form.sessions,
      exhibit_ref:           form.exhibit_ref,
      learning_outcomes:     form.learning_outcomes,
      integration_other_sub: form.integration_other_sub,
      library:               form.library,
      activity:              form.activity,
      life_lesson:           form.life_lesson,
      remarks:               form.remarks,
    })
    // Update in-place
    Object.assign(concept, form)
    editingConceptId.value = null
    delete conceptForms[concept.id]
    setConceptMsg(concept.id, 'success', 'Concept saved!')
    setTimeout(() => clearConceptMsg(concept.id), 3000)
  } catch (e) {
    setConceptMsg(concept.id, 'error', e.response?.data?.detail || 'Failed to save concept.')
  } finally {
    conceptSaving[concept.id] = false
  }
}

function setConceptMsg(id, type, text) {
  conceptMsgs[id] = { type, text }
}

function clearConceptMsg(id) {
  conceptMsgs[id] = { type: '', text: '' }
}

// ── Delete concept ─────────────────────────────────────────────────────
async function deleteConcept(concept, index) {
  if (!window.confirm(`Delete concept "${concept.title}"? This cannot be undone.`)) return
  try {
    await api.delete(`/api/portal/concepts/${concept.id}`)
    chapter.value.concepts.splice(index, 1)
  } catch (e) {
    alert(e.response?.data?.detail || 'Failed to delete concept.')
  }
}

// ── Add new concept ────────────────────────────────────────────────────
function addConcept() {
  Object.assign(newConceptForm, {
    s_no: '', title: '', sessions: '', exhibit_ref: '',
    learning_outcomes: '', integration_other_sub: '',
    library: '', activity: '', life_lesson: '', remarks: '',
  })
  newConceptMsg.text = ''
  newConceptOpen.value = true
}

async function saveNewConcept() {
  if (!newConceptForm.title?.trim()) {
    newConceptMsg.type = 'error'
    newConceptMsg.text = 'Title is required.'
    return
  }
  newConceptSaving.value = true
  newConceptMsg.text = ''
  try {
    const res = await api.post('/api/portal/concepts', {
      chapter_id:            parseInt(chapterId.value),
      s_no:                  newConceptForm.s_no,
      title:                 newConceptForm.title,
      sessions:              newConceptForm.sessions,
      exhibit_ref:           newConceptForm.exhibit_ref,
      learning_outcomes:     newConceptForm.learning_outcomes,
      integration_other_sub: newConceptForm.integration_other_sub,
      library:               newConceptForm.library,
      activity:              newConceptForm.activity,
      life_lesson:           newConceptForm.life_lesson,
      remarks:               newConceptForm.remarks,
    })
    const newConcept = res.data
    if (!newConcept.exhibits) newConcept.exhibits = []
    if (!chapter.value.concepts) chapter.value.concepts = []
    chapter.value.concepts.push(newConcept)
    newConceptOpen.value = false
  } catch (e) {
    newConceptMsg.type = 'error'
    newConceptMsg.text = e.response?.data?.detail || 'Failed to create concept.'
  } finally {
    newConceptSaving.value = false
  }
}

// ── Exhibit save ───────────────────────────────────────────────────────
async function saveExhibit(ex, conceptId) {
  if (!ex.field_key?.trim()) return
  exhibitSaving[ex.id] = true
  exhibitMsgs[ex.id] = { text: '', type: '' }

  try {
    if (ex._isNew) {
      // POST new exhibit
      const res = await api.post(`/api/portal/concepts/${conceptId}/exhibits`, {
        field_key:   ex.field_key,
        field_value: ex.field_value || '',
      })
      // Replace temp object with real one from server
      const concept = chapter.value.concepts.find(c => c.id === conceptId)
      if (concept) {
        const idx = concept.exhibits.findIndex(e => e.id === ex.id)
        if (idx !== -1) {
          concept.exhibits[idx] = { ...res.data }
        }
      }
    } else {
      await api.put(`/api/portal/exhibits/${ex.id}`, {
        field_key:   ex.field_key,
        field_value: ex.field_value || '',
      })
      exhibitMsgs[ex.id] = { type: 'success', text: 'Saved' }
      setTimeout(() => { if (exhibitMsgs[ex.id]) exhibitMsgs[ex.id].text = '' }, 2000)
    }
  } catch (e) {
    exhibitMsgs[ex.id] = { type: 'error', text: e.response?.data?.detail || 'Save failed' }
  } finally {
    exhibitSaving[ex.id] = false
  }
}

// ── Add exhibit row ────────────────────────────────────────────────────
function addExhibitRow(concept) {
  if (!concept.exhibits) concept.exhibits = []
  const tempId = `new_${Date.now()}`
  concept.exhibits.push({
    id:          tempId,
    field_key:   '',
    field_value: '',
    _isNew:      true,
  })
}

// ── Delete exhibit ─────────────────────────────────────────────────────
async function deleteExhibit(ex, concept, index) {
  if (ex._isNew) {
    concept.exhibits.splice(index, 1)
    return
  }
  if (!window.confirm(`Delete field "${ex.field_key}"?`)) return
  try {
    await api.delete(`/api/portal/exhibits/${ex.id}`)
    concept.exhibits.splice(index, 1)
  } catch (e) {
    alert(e.response?.data?.detail || 'Failed to delete field.')
  }
}
</script>

<style scoped>
/* ── Page & Navbar ─────────────────────────────────────────────────── */
.page {
  min-height: 100vh;
  background: #f1f5f9;
  font-family: system-ui, -apple-system, sans-serif;
  padding-bottom: 4rem;
}

.navbar {
  background: #1e293b;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  height: 56px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.nav-title {
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 0.02em;
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

/* ── Content ──────────────────────────────────────────────────────── */
.content {
  max-width: 860px;
  margin: 0 auto;
  padding: 1.5rem 1rem;
}

/* ── Card ─────────────────────────────────────────────────────────── */
.card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem 1.8rem;
  box-shadow: 0 1px 6px rgba(0,0,0,0.07);
  margin-bottom: 1rem;
}

.empty-card {
  text-align: center;
  padding: 2rem;
}

/* ── Card Heading (collapsible) ───────────────────────────────────── */
.card-heading {
  font-size: 1rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 1.2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.collapsible {
  cursor: pointer;
  user-select: none;
}

.toggle-icon {
  font-size: 0.78rem;
  color: #94a3b8;
}

/* ── Form Fields ──────────────────────────────────────────────────── */
.field {
  margin-bottom: 1rem;
}

.field label {
  display: block;
  font-size: 0.82rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.35rem;
}

.required {
  color: #ef4444;
}

.field input,
.field textarea {
  width: 100%;
  padding: 0.6rem 0.85rem;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.93rem;
  color: #111827;
  outline: none;
  transition: border-color 0.15s;
  box-sizing: border-box;
  font-family: inherit;
  background: white;
}

.field input:focus,
.field textarea:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79,70,229,0.09);
}

.field textarea {
  resize: vertical;
}

.field input.readonly,
.field textarea.readonly {
  background: #f9fafb;
  color: #6b7280;
  cursor: default;
}

/* ── Inline message ───────────────────────────────────────────────── */
.inline-msg {
  font-size: 0.83rem;
  border-radius: 6px;
  padding: 0.45rem 0.8rem;
  margin-top: 0.5rem;
}

.inline-msg.success {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #15803d;
}

.inline-msg.error {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
}

/* ── Form actions ─────────────────────────────────────────────────── */
.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.btn-save {
  padding: 0.58rem 1.5rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.45rem;
  transition: background 0.15s;
}

.btn-save:hover:not(:disabled) {
  background: #4338ca;
}

.btn-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* ── Concepts section heading ─────────────────────────────────────── */
.concepts-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin: 1.5rem 0 0.8rem;
}

.section-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.count-badge {
  background: #e0e7ff;
  color: #4f46e5;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 0.18rem 0.55rem;
  border-radius: 20px;
}

.btn-add {
  padding: 0.5rem 1.1rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-add:hover {
  background: #4338ca;
}

/* ── Concept Card ─────────────────────────────────────────────────── */
.concept-card {
  padding: 0;
  overflow: hidden;
}

.concept-card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.9rem 1.3rem;
  cursor: pointer;
  user-select: none;
  gap: 0.8rem;
  border-bottom: 1px solid #f1f5f9;
}

.concept-card-header:hover {
  background: #fafbff;
}

.concept-header-info {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  flex: 1;
  min-width: 0;
}

.badge-sno {
  font-size: 0.7rem;
  font-weight: 700;
  background: #eef2ff;
  color: #4f46e5;
  padding: 0.15rem 0.5rem;
  border-radius: 20px;
  flex-shrink: 0;
}

.concept-header-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: #1e293b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.badge-sessions {
  font-size: 0.74rem;
  color: #6b7280;
  background: #f3f4f6;
  padding: 0.12rem 0.5rem;
  border-radius: 20px;
  flex-shrink: 0;
}

.concept-header-actions {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  flex-shrink: 0;
}

.expand-icon {
  font-size: 0.75rem;
  color: #94a3b8;
  margin-left: 0.2rem;
}

/* Small action buttons in header */
.btn-edit-sm {
  padding: 0.3rem 0.75rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-edit-sm:hover {
  background: #4338ca;
}

.btn-save-sm {
  padding: 0.3rem 0.75rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  transition: background 0.15s;
}

.btn-save-sm:hover:not(:disabled) {
  background: #4338ca;
}

.btn-save-sm:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-cancel-sm {
  padding: 0.3rem 0.75rem;
  background: white;
  color: #374151;
  border: 1.5px solid #e5e7eb;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-cancel-sm:hover {
  background: #f3f4f6;
}

.btn-delete-sm {
  padding: 0.3rem 0.75rem;
  background: white;
  color: #dc2626;
  border: 1.5px solid #fecaca;
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-delete-sm:hover {
  background: #fef2f2;
  border-color: #dc2626;
}

/* ── Concept Body ─────────────────────────────────────────────────── */
.concept-body {
  padding: 1.2rem 1.3rem 1.3rem;
}

/* ── 2-col grid for concept fields ───────────────────────────────── */
.concept-fields-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0 1rem;
}

.concept-fields-grid .full-width {
  grid-column: 1 / -1;
}

@media (max-width: 600px) {
  .concept-fields-grid {
    grid-template-columns: 1fr;
  }
  .concept-fields-grid .full-width {
    grid-column: 1;
  }
}

/* ── Exhibit Fields Section ───────────────────────────────────────── */
.exhibits-section {
  margin-top: 1.2rem;
  border-top: 1px solid #e2e8f0;
  padding-top: 1rem;
}

.exhibits-heading {
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: #4f46e5;
  margin: 0 0 0.8rem;
}

.exhibit-row {
  border-bottom: 1px solid #f1f5f9;
  padding-bottom: 0.7rem;
  margin-bottom: 0.7rem;
}

.exhibit-row:last-of-type {
  border-bottom: none;
}

.exhibit-row-inputs {
  display: flex;
  gap: 0.6rem;
  align-items: flex-start;
}

.exhibit-key-input {
  width: 160px;
  flex-shrink: 0;
  padding: 0.45rem 0.7rem;
  border: 1.5px solid #e5e7eb;
  border-radius: 7px;
  font-size: 0.88rem;
  color: #111827;
  outline: none;
  font-family: inherit;
  transition: border-color 0.15s;
}

.exhibit-key-input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79,70,229,0.09);
}

.exhibit-value-input {
  flex: 1;
  padding: 0.45rem 0.7rem;
  border: 1.5px solid #e5e7eb;
  border-radius: 7px;
  font-size: 0.88rem;
  color: #111827;
  outline: none;
  font-family: inherit;
  resize: vertical;
  transition: border-color 0.15s;
}

.exhibit-value-input:focus {
  border-color: #4f46e5;
  box-shadow: 0 0 0 3px rgba(79,70,229,0.09);
}

.exhibit-row-actions {
  display: flex;
  gap: 0.35rem;
  margin-top: 0.4rem;
}

.btn-icon {
  width: 30px;
  height: 30px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 0.9rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}

.btn-icon-save {
  background: #4f46e5;
  color: white;
}

.btn-icon-save:hover:not(:disabled) {
  background: #4338ca;
}

.btn-icon-save:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-icon-delete {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
}

.btn-icon-delete:hover {
  background: #dc2626;
  color: white;
}

.exhibit-msg {
  margin-top: 0.3rem;
  font-size: 0.78rem;
}

.btn-add-field {
  margin-top: 0.4rem;
  padding: 0.38rem 0.9rem;
  background: white;
  color: #4f46e5;
  border: 1.5px dashed #a5b4fc;
  border-radius: 7px;
  font-size: 0.84rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-add-field:hover {
  background: #eef2ff;
  border-color: #4f46e5;
}

/* ── Loading / Error ─────────────────────────────────────────────── */
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
  width: 34px;
  height: 34px;
  border: 3px solid #e2e8f0;
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.spinner-sm {
  width: 13px;
  height: 13px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
  display: inline-block;
}

.spinner-sm.dark {
  border-color: rgba(79,70,229,0.3);
  border-top-color: #4f46e5;
}

@keyframes spin {
  to { transform: rotate(360deg); }
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

.upload-hint {
  text-align: center;
  font-size: 0.82rem;
  color: #94a3b8;
  font-style: italic;
  margin-top: 1.5rem;
}

/* ── Slide transition ────────────────────────────────────────────── */
.slide-enter-active,
.slide-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
  overflow: hidden;
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(-6px);
}
</style>
