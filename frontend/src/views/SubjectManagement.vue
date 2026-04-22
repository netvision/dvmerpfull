<template>
  <div class="sm-page">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-left">
        <span class="nav-title">Subject Management</span>
        <router-link to="/portal" class="back-link">← Back to Portal</router-link>
      </div>
      <div class="nav-right">
        <span v-if="auth.user" class="user-info">
          <span class="user-name">{{ auth.user.name }}</span>
          <span class="role-badge" :class="auth.user.role">{{ auth.user.role }}</span>
        </span>
      </div>
    </nav>

    <div class="content">
      <!-- Header row -->
      <div class="page-header">
        <div class="header-left">
          <h1 class="page-title">Subjects</h1>
          <select v-model="filterClassId" @change="fetchSubjects" class="class-filter">
            <option value="">All Classes</option>
            <option v-for="c in classes" :key="c.id" :value="c.id">{{ c.name }}</option>
          </select>
        </div>
        <button class="add-btn" @click="openAddModal">+ Add Subject</button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading subjects…</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="error-box">{{ error }}</div>

      <!-- Empty -->
      <div v-else-if="subjects.length === 0" class="empty-state">
        <p>No subjects found.</p>
      </div>

      <!-- Table -->
      <div v-else class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Icon</th>
              <th>Name</th>
              <th>Class</th>
              <th>Color</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in subjects" :key="s.id">
              <td class="td-icon">{{ s.icon || '—' }}</td>
              <td class="td-name">{{ s.name }}</td>
              <td>{{ s.class_name }}</td>
              <td class="td-color">
                <span v-if="s.color" class="color-swatch" :style="{ background: s.color }"></span>
                <span class="color-hex">{{ s.color || '—' }}</span>
              </td>
              <td class="actions-cell">
                <button class="btn-edit" @click="openEditModal(s)">Edit</button>
                <button class="btn-delete" @click="confirmDelete(s)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add / Edit Modal -->
    <div v-if="showFormModal" class="modal-overlay" @click.self="showFormModal = false">
      <div class="modal">
        <h2 class="modal-title">{{ isEdit ? 'Edit Subject' : 'Add Subject' }}</h2>
        <form @submit.prevent="saveSubject">
          <div class="field">
            <label>Class *</label>
            <select v-model="form.class_id" required>
              <option value="">Select class</option>
              <option v-for="c in classes" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>
          <div class="field">
            <label>Name *</label>
            <input v-model="form.name" type="text" required placeholder="e.g. Mathematics" />
          </div>
          <div class="field">
            <label>Icon <span class="hint-text">(emoji)</span></label>
            <input v-model="form.icon" type="text" placeholder="e.g. 📐" class="input-sm" />
          </div>
          <div class="field">
            <label>Color <span class="hint-text">(hex)</span></label>
            <div class="color-field">
              <input v-model="form.color" type="color" class="color-picker" />
              <input v-model="form.color" type="text" placeholder="#2563eb" class="color-text" />
            </div>
          </div>
          <div v-if="formError" class="error-banner">{{ formError }}</div>
          <div class="modal-actions">
            <button type="button" class="btn-cancel" @click="showFormModal = false">Cancel</button>
            <button type="submit" class="btn-save" :disabled="saving">
              {{ saving ? 'Saving…' : (isEdit ? 'Save Changes' : 'Create') }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirm Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click.self="showDeleteModal = false">
      <div class="modal modal-sm">
        <h2 class="modal-title">Delete Subject</h2>
        <p class="confirm-text">
          Delete <strong>{{ deleteTarget?.name }}</strong>? This cannot be undone.
          All teacher assignments for this subject will also be removed.
        </p>
        <div v-if="deleteError" class="error-banner">{{ deleteError }}</div>
        <div class="modal-actions">
          <button type="button" class="btn-cancel" @click="showDeleteModal = false">Cancel</button>
          <button class="btn-delete-confirm" :disabled="deleting" @click="doDelete">
            {{ deleting ? 'Deleting…' : 'Delete' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api.js'

const auth = useAuthStore()

const classes = ref([])
const subjects = ref([])
const filterClassId = ref('')
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  if (!auth.user) {
    try { await auth.fetchMe() } catch (_) {}
  }
  await loadClasses()
  await fetchSubjects()
})

async function loadClasses() {
  try {
    const res = await api.get('/api/public/classes')
    classes.value = res.data
  } catch (_) {}
}

async function fetchSubjects() {
  loading.value = true
  error.value = ''
  try {
    const params = filterClassId.value ? { class_id: filterClassId.value } : {}
    const res = await api.get('/api/portal/subjects', { params })
    subjects.value = res.data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load subjects.'
  } finally {
    loading.value = false
  }
}

// ── Add / Edit Modal ─────────────────────────────────────────────────────────
const showFormModal = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const form = ref({ class_id: '', name: '', icon: '', color: '#2563eb' })
const saving = ref(false)
const formError = ref('')

function openAddModal() {
  isEdit.value = false
  editId.value = null
  form.value = { class_id: filterClassId.value || '', name: '', icon: '', color: '#2563eb' }
  formError.value = ''
  showFormModal.value = true
}

function openEditModal(s) {
  isEdit.value = true
  editId.value = s.id
  form.value = { class_id: s.class_id, name: s.name, icon: s.icon || '', color: s.color || '#2563eb' }
  formError.value = ''
  showFormModal.value = true
}

async function saveSubject() {
  formError.value = ''
  saving.value = true
  try {
    const payload = {
      name: form.value.name,
      class_id: Number(form.value.class_id),
      icon: form.value.icon || null,
      color: form.value.color || null,
    }
    if (isEdit.value) {
      await api.put(`/api/portal/subjects/${editId.value}`, payload)
    } else {
      await api.post('/api/portal/subjects', payload)
    }
    showFormModal.value = false
    await fetchSubjects()
  } catch (e) {
    formError.value = e.response?.data?.detail || 'Failed to save subject.'
  } finally {
    saving.value = false
  }
}

// ── Delete Modal ─────────────────────────────────────────────────────────────
const showDeleteModal = ref(false)
const deleteTarget = ref(null)
const deleting = ref(false)
const deleteError = ref('')

function confirmDelete(s) {
  deleteTarget.value = s
  deleteError.value = ''
  showDeleteModal.value = true
}

async function doDelete() {
  deleting.value = true
  deleteError.value = ''
  try {
    await api.delete(`/api/portal/subjects/${deleteTarget.value.id}`)
    showDeleteModal.value = false
    await fetchSubjects()
  } catch (e) {
    deleteError.value = e.response?.data?.detail || 'Failed to delete subject.'
  } finally {
    deleting.value = false
  }
}
</script>

<style scoped>
.sm-page {
  min-height: 100vh;
  background: #f1f5f9;
  font-family: system-ui, -apple-system, sans-serif;
}

/* Navbar */
.navbar {
  background: #1e3a8a;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  height: 56px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
.nav-left { display: flex; align-items: center; gap: 1.2rem; }
.nav-title { font-size: 1.15rem; font-weight: 700; }
.back-link { font-size: 0.85rem; color: rgba(255,255,255,0.65); text-decoration: none; }
.back-link:hover { color: white; }
.nav-right { display: flex; align-items: center; gap: 1rem; }
.user-info { display: flex; align-items: center; gap: 0.5rem; font-size: 0.9rem; }
.user-name { color: rgba(255,255,255,0.85); }
.role-badge { font-size: 0.7rem; font-weight: 600; padding: 2px 8px; border-radius: 99px; text-transform: uppercase; letter-spacing: 0.05em; }
.role-badge.admin { background: #1d4ed8; color: white; }
.role-badge.teacher { background: #0891b2; color: white; }
.role-badge.super_admin { background: #1d4ed8; color: white; }
.role-badge.principal { background: #0f766e; color: white; }
.role-badge.hm { background: #0369a1; color: white; }
.role-badge.subject_head { background: #4f46e5; color: white; }
.role-badge.mentor { background: #7c3aed; color: white; }

/* Content */
.content { max-width: 900px; margin: 0 auto; padding: 2rem 1.5rem; }
.page-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.5rem; }
.header-left { display: flex; align-items: center; gap: 1rem; }
.page-title { font-size: 1.5rem; font-weight: 700; color: #1e293b; margin: 0; }
.class-filter { padding: 0.4rem 0.75rem; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.9rem; background: white; }
.add-btn { background: #2563eb; color: white; border: none; padding: 0.5rem 1.1rem; border-radius: 6px; font-size: 0.9rem; font-weight: 600; cursor: pointer; }
.add-btn:hover { background: #1d4ed8; }

/* States */
.loading-state { text-align: center; padding: 3rem; color: #64748b; }
.spinner { width: 32px; height: 32px; border: 3px solid #e2e8f0; border-top-color: #2563eb; border-radius: 50%; animation: spin 0.7s linear infinite; margin: 0 auto 1rem; }
@keyframes spin { to { transform: rotate(360deg); } }
.error-box { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; border-radius: 8px; padding: 1rem 1.25rem; }
.empty-state { text-align: center; padding: 3rem; color: #64748b; }

/* Table */
.table-wrapper { background: white; border-radius: 10px; box-shadow: 0 1px 4px rgba(0,0,0,0.07); overflow: hidden; }
.data-table { width: 100%; border-collapse: collapse; font-size: 0.9rem; }
.data-table thead { background: #f8fafc; }
.data-table th { padding: 0.75rem 1rem; text-align: left; font-size: 0.75rem; font-weight: 600; color: #64748b; text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid #e2e8f0; }
.data-table td { padding: 0.75rem 1rem; border-bottom: 1px solid #f1f5f9; color: #1e293b; }
.data-table tbody tr:last-child td { border-bottom: none; }
.data-table tbody tr:hover { background: #f8fafc; }
.td-icon { font-size: 1.3rem; }
.td-name { font-weight: 600; }
.td-color { display: flex; align-items: center; gap: 0.5rem; }
.color-swatch { display: inline-block; width: 18px; height: 18px; border-radius: 4px; border: 1px solid rgba(0,0,0,0.1); flex-shrink: 0; }
.color-hex { font-size: 0.8rem; color: #64748b; font-family: monospace; }
.actions-cell { display: flex; gap: 0.5rem; }
.btn-edit { background: #dbeafe; color: #1d4ed8; border: none; padding: 0.3rem 0.75rem; border-radius: 5px; font-size: 0.8rem; font-weight: 600; cursor: pointer; }
.btn-edit:hover { background: #c7d2fe; }
.btn-delete { background: #fee2e2; color: #b91c1c; border: none; padding: 0.3rem 0.75rem; border-radius: 5px; font-size: 0.8rem; font-weight: 600; cursor: pointer; }
.btn-delete:hover { background: #fecaca; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: center; z-index: 200; padding: 1rem; }
.modal { background: white; border-radius: 12px; padding: 1.75rem; width: 100%; max-width: 440px; box-shadow: 0 8px 32px rgba(0,0,0,0.18); }
.modal-sm { max-width: 360px; }
.modal-title { font-size: 1.15rem; font-weight: 700; color: #1e293b; margin: 0 0 1.25rem; }
.field { margin-bottom: 1rem; }
.field label { display: block; font-size: 0.8rem; font-weight: 600; color: #475569; margin-bottom: 0.35rem; }
.hint-text { font-weight: 400; color: #94a3b8; }
.field input, .field select { width: 100%; padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.9rem; box-sizing: border-box; }
.field input:focus, .field select:focus { outline: none; border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.12); }
.input-sm { max-width: 120px; }
.color-field { display: flex; align-items: center; gap: 0.5rem; }
.color-picker { width: 44px; height: 36px; padding: 2px; border: 1px solid #cbd5e1; border-radius: 6px; cursor: pointer; flex-shrink: 0; }
.color-text { flex: 1; }
.error-banner { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; border-radius: 6px; padding: 0.6rem 0.75rem; font-size: 0.85rem; margin-bottom: 0.75rem; }
.modal-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.25rem; }
.btn-cancel { background: #f1f5f9; color: #475569; border: none; padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.9rem; cursor: pointer; }
.btn-cancel:hover { background: #e2e8f0; }
.btn-save { background: #2563eb; color: white; border: none; padding: 0.5rem 1.2rem; border-radius: 6px; font-size: 0.9rem; font-weight: 600; cursor: pointer; }
.btn-save:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-save:hover:not(:disabled) { background: #1d4ed8; }
.btn-delete-confirm { background: #dc2626; color: white; border: none; padding: 0.5rem 1.2rem; border-radius: 6px; font-size: 0.9rem; font-weight: 600; cursor: pointer; }
.btn-delete-confirm:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-delete-confirm:hover:not(:disabled) { background: #b91c1c; }
.confirm-text { color: #475569; font-size: 0.9rem; line-height: 1.5; margin-bottom: 1rem; }
</style>
