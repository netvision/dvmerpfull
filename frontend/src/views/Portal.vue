<template>
  <div class="portal-page">
    <!-- Nav Bar -->
    <nav class="navbar">
      <span class="nav-title">Teacher Portal</span>
      <div class="nav-right">
        <span v-if="auth.user" class="user-info">
          <span class="user-name">{{ auth.user.name }}</span>
          <span class="role-badge" :class="auth.user.role">{{ auth.user.role }}</span>
        </span>
        <button class="logout-btn" @click="handleLogout">Logout</button>
      </div>
    </nav>

    <div class="content">
      <!-- Filter Row -->
      <div class="filter-row">
        <div class="filter-group">
          <label>Class</label>
          <select v-model="selectedClassId" @change="onClassChange">
            <option value="">All Classes</option>
            <option v-for="c in classes" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
        <div class="filter-group">
          <label>Subject</label>
          <select v-model="selectedSubjectId" @change="fetchChapters">
            <option value="">All Subjects</option>
            <option v-for="s in subjects" :key="s.id" :value="s.id">{{ s.name }}</option>
          </select>
        </div>
        <button v-if="auth.isAdmin" class="add-btn" @click="showAddModal = true">
          + Add Chapter
        </button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading chapters…</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="error-box">{{ error }}</div>

      <!-- Empty State -->
      <div v-else-if="chapters.length === 0" class="empty-state">
        <p>No chapters found.</p>
        <p v-if="auth.isAdmin" class="hint">Click "Add Chapter" to create one, or upload an xlsx file.</p>
      </div>

      <!-- Data Table -->
      <div v-else class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Chapter Title</th>
              <th>Class</th>
              <th>Subject</th>
              <th>Sessions</th>
              <th>Concepts</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="ch in chapters" :key="ch.id">
              <td class="title-cell">{{ ch.title }}</td>
              <td>{{ ch.class_name }}</td>
              <td>{{ ch.subject_name }}</td>
              <td class="center">{{ ch.sessions_total }}</td>
              <td class="center">{{ ch.concept_count }}</td>
              <td class="actions-cell">
                <button class="btn-edit" @click="router.push(`/portal/chapter/${ch.id}/edit`)">
                  Edit
                </button>
                <button class="btn-upload" @click="goToUpload(ch)">
                  Upload xlsx
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add Chapter Modal (admin only) -->
    <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
      <div class="modal">
        <h2 class="modal-title">Add Chapter</h2>
        <form @submit.prevent="createChapter">
          <div class="field">
            <label>Title *</label>
            <input v-model="newChapter.title" type="text" required placeholder="Chapter title" />
          </div>
          <div class="field">
            <label>Aim</label>
            <textarea v-model="newChapter.aim" rows="3" placeholder="Chapter aim / objective"></textarea>
          </div>
          <div class="field">
            <label>Class *</label>
            <select v-model="newChapter.class_id" required @change="loadModalSubjects">
              <option value="">Select class</option>
              <option v-for="c in classes" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>
          <div class="field">
            <label>Subject *</label>
            <select v-model="newChapter.subject_id" required>
              <option value="">Select subject</option>
              <option v-for="s in modalSubjects" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
          <div v-if="createError" class="error-banner">{{ createError }}</div>
          <div class="modal-actions">
            <button type="button" class="btn-cancel" @click="showAddModal = false">Cancel</button>
            <button type="submit" class="btn-save" :disabled="creating">
              {{ creating ? 'Creating…' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api.js'

const router = useRouter()
const auth = useAuthStore()

const classes = ref([])
const subjects = ref([])
const chapters = ref([])
const selectedClassId = ref('')
const selectedSubjectId = ref('')
const loading = ref(false)
const error = ref('')

const showAddModal = ref(false)
const modalSubjects = ref([])
const newChapter = ref({ title: '', aim: '', class_id: '', subject_id: '' })
const creating = ref(false)
const createError = ref('')

onMounted(async () => {
  await ensureUser()
  await loadClasses()
  await fetchChapters()
})

async function ensureUser() {
  if (!auth.user) {
    try { await auth.fetchMe() } catch (_) {}
  }
}

async function loadClasses() {
  try {
    const res = await api.get('/api/public/classes')
    classes.value = res.data
  } catch (_) {}
}

async function onClassChange() {
  selectedSubjectId.value = ''
  subjects.value = []
  if (selectedClassId.value) {
    try {
      const res = await api.get(`/api/public/classes/${selectedClassId.value}/subjects`)
      subjects.value = res.data
    } catch (_) {}
  }
  await fetchChapters()
}

async function fetchChapters() {
  loading.value = true
  error.value = ''
  try {
    const params = {}
    if (selectedClassId.value) params.class_id = selectedClassId.value
    if (selectedSubjectId.value) params.subject_id = selectedSubjectId.value
    const res = await api.get('/api/portal/chapters', { params })
    chapters.value = res.data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load chapters.'
  } finally {
    loading.value = false
  }
}

function goToUpload(ch) {
  router.push({ path: '/portal/upload', query: { subject_id: ch.subject_id || '' } })
}

function handleLogout() {
  auth.logout()
  router.replace('/login')
}

async function loadModalSubjects() {
  modalSubjects.value = []
  newChapter.value.subject_id = ''
  if (newChapter.value.class_id) {
    try {
      const res = await api.get(`/api/public/classes/${newChapter.value.class_id}/subjects`)
      modalSubjects.value = res.data
    } catch (_) {}
  }
}

async function createChapter() {
  createError.value = ''
  creating.value = true
  try {
    await api.post('/api/portal/chapters', {
      title: newChapter.value.title,
      aim: newChapter.value.aim,
      subject_id: newChapter.value.subject_id,
    })
    showAddModal.value = false
    newChapter.value = { title: '', aim: '', class_id: '', subject_id: '' }
    await fetchChapters()
  } catch (e) {
    createError.value = e.response?.data?.detail || 'Failed to create chapter.'
  } finally {
    creating.value = false
  }
}
</script>

<style scoped>
.portal-page {
  min-height: 100vh;
  background: #f1f5f9;
  font-family: system-ui, -apple-system, sans-serif;
}

/* Navbar */
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
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 500;
}

.role-badge {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  padding: 0.2rem 0.55rem;
  border-radius: 20px;
}

.role-badge.admin {
  background: #dc2626;
  color: white;
}

.role-badge.teacher {
  background: #0ea5e9;
  color: white;
}

.logout-btn {
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.25);
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.88rem;
  transition: background 0.15s;
}

.logout-btn:hover {
  background: rgba(255,255,255,0.22);
}

/* Content */
.content {
  max-width: 1100px;
  margin: 0 auto;
  padding: 1.5rem 1rem;
}

/* Filter Row */
.filter-row {
  display: flex;
  align-items: flex-end;
  gap: 1rem;
  flex-wrap: wrap;
  background: white;
  border-radius: 10px;
  padding: 1rem 1.2rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.07);
  margin-bottom: 1.2rem;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 0.3rem;
}

.filter-group label {
  font-size: 0.78rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.07em;
}

.filter-group select {
  padding: 0.5rem 0.8rem;
  border: 1.5px solid #e2e8f0;
  border-radius: 7px;
  font-size: 0.93rem;
  color: #1e293b;
  background: white;
  outline: none;
  cursor: pointer;
  min-width: 160px;
}

.filter-group select:focus {
  border-color: #4f46e5;
}

.add-btn {
  margin-left: auto;
  padding: 0.55rem 1.2rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 7px;
  font-size: 0.93rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.add-btn:hover {
  background: #4338ca;
}

/* Table */
.table-wrapper {
  background: white;
  border-radius: 10px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.07);
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.93rem;
}

.data-table thead tr {
  background: #f8fafc;
  border-bottom: 2px solid #e2e8f0;
}

.data-table th {
  padding: 0.75rem 1rem;
  text-align: left;
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #64748b;
  white-space: nowrap;
}

.data-table td {
  padding: 0.8rem 1rem;
  border-bottom: 1px solid #f1f5f9;
  color: #1e293b;
  vertical-align: middle;
}

.data-table tbody tr:hover {
  background: #f8fafc;
}

.data-table tbody tr:last-child td {
  border-bottom: none;
}

.title-cell {
  font-weight: 600;
  max-width: 280px;
}

.center {
  text-align: center;
}

.actions-cell {
  white-space: nowrap;
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.btn-edit {
  padding: 0.35rem 0.85rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 0.83rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-edit:hover {
  background: #4338ca;
}

.btn-upload {
  padding: 0.35rem 0.85rem;
  background: white;
  color: #0ea5e9;
  border: 1.5px solid #0ea5e9;
  border-radius: 6px;
  font-size: 0.83rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-upload:hover {
  background: #f0f9ff;
}

/* Empty / Loading / Error */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  color: #64748b;
  gap: 1rem;
  background: white;
  border-radius: 10px;
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #e2e8f0;
  border-top-color: #4f46e5;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.error-box {
  background: #fef2f2;
  color: #dc2626;
  padding: 1rem 1.2rem;
  border-radius: 8px;
  border: 1px solid #fecaca;
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  color: #64748b;
  background: white;
  border-radius: 10px;
}

.empty-state p {
  margin: 0.25rem 0;
}

.empty-state .hint {
  font-size: 0.88rem;
  color: #94a3b8;
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 100;
  padding: 1rem;
}

.modal {
  background: white;
  border-radius: 14px;
  padding: 2rem;
  width: 100%;
  max-width: 480px;
  box-shadow: 0 20px 50px rgba(0,0,0,0.2);
}

.modal-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 1.4rem;
}

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

.field input,
.field textarea,
.field select {
  width: 100%;
  padding: 0.6rem 0.85rem;
  border: 1.5px solid #e5e7eb;
  border-radius: 7px;
  font-size: 0.93rem;
  color: #111827;
  outline: none;
  transition: border-color 0.15s;
  box-sizing: border-box;
  font-family: inherit;
  background: white;
}

.field input:focus,
.field textarea:focus,
.field select:focus {
  border-color: #4f46e5;
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

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.btn-cancel {
  padding: 0.55rem 1.2rem;
  background: white;
  color: #374151;
  border: 1.5px solid #e5e7eb;
  border-radius: 7px;
  font-size: 0.93rem;
  cursor: pointer;
}

.btn-cancel:hover {
  background: #f9fafb;
}

.btn-save {
  padding: 0.55rem 1.4rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 7px;
  font-size: 0.93rem;
  font-weight: 600;
  cursor: pointer;
}

.btn-save:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.btn-save:hover:not(:disabled) {
  background: #4338ca;
}

@media (max-width: 640px) {
  .navbar { padding: 0 1rem; }
  .user-name { display: none; }
  .data-table th, .data-table td { padding: 0.6rem 0.7rem; }
}
</style>
