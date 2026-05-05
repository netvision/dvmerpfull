<template>
  <div class="sm-page">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-left">
        <span class="nav-title">Class Management</span>
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
          <h1 class="page-title">Classes</h1>
        </div>
        <button class="add-btn" @click="openAddModal">+ Add Class</button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading classes…</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="error-box">{{ error }}</div>

      <!-- Empty -->
      <div v-else-if="classes.length === 0" class="empty-state">
        <p>No classes found.</p>
      </div>

      <!-- Table -->
      <div v-else class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Class Name</th>
              <th>Order</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="c in classes" :key="c.id">
              <td>{{ c.id }}</td>
              <td class="td-name">{{ c.name }}</td>
              <td>{{ c.display_order }}</td>
              <td class="actions-cell">
                <button class="btn-edit" @click="openEditModal(c)">Edit</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add / Edit Modal -->
    <div v-if="showFormModal" class="modal-overlay" @click.self="showFormModal = false">
      <div class="modal">
        <h2 class="modal-title">{{ isEdit ? 'Edit Class' : 'Add Class' }}</h2>
        <form @submit.prevent="saveClass">
          <div class="field">
            <label>Class Name *</label>
            <input v-model="form.name" type="text" required placeholder="e.g. Class 1" />
          </div>
          <div class="field">
            <label>Order *</label>
            <input v-model.number="form.display_order" type="number" required />
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api.js'

const auth = useAuthStore()

const classes = ref([])
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  if (!auth.user) {
    try { await auth.fetchMe() } catch (_) {}
  }
  await fetchClasses()
})

async function fetchClasses() {
  loading.value = true
  error.value = ''
  try {
    const res = await api.get('/api/public/classes')
    classes.value = res.data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load classes.'
  } finally {
    loading.value = false
  }
}

// ── Add / Edit Modal ─────────────────────────────────────────────────────────
const showFormModal = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const form = ref({ name: '', display_order: 0 })
const saving = ref(false)
const formError = ref('')

function openAddModal() {
  isEdit.value = false
  editId.value = null
  form.value = { name: '', display_order: 0 }
  formError.value = ''
  showFormModal.value = true
}

function openEditModal(c) {
  isEdit.value = true
  editId.value = c.id
  form.value = { name: c.name, display_order: c.display_order ?? 0 }
  formError.value = ''
  showFormModal.value = true
}

async function saveClass() {
  formError.value = ''
  saving.value = true
  try {
    const payload = {
      name: form.value.name,
      display_order: form.value.display_order,
    }
    if (isEdit.value) {
      await api.put(`/api/portal/erp/lookups/classes/${editId.value}`, payload)
    } else {
      await api.post('/api/portal/erp/lookups/classes', payload)
    }
    showFormModal.value = false
    await fetchClasses()
  } catch (e) {
    formError.value = e.response?.data?.detail || 'Failed to save class.'
  } finally {
    saving.value = false
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
.td-name { font-weight: 600; }
.actions-cell { display: flex; gap: 0.5rem; }
.btn-edit { background: #dbeafe; color: #1d4ed8; border: none; padding: 0.3rem 0.75rem; border-radius: 5px; font-size: 0.8rem; font-weight: 600; cursor: pointer; }
.btn-edit:hover { background: #c7d2fe; }

/* Modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,0.45); display: flex; align-items: center; justify-content: center; z-index: 200; padding: 1rem; }
.modal { background: white; border-radius: 12px; padding: 1.75rem; width: 100%; max-width: 440px; box-shadow: 0 8px 32px rgba(0,0,0,0.18); }
.modal-title { font-size: 1.15rem; font-weight: 700; color: #1e293b; margin: 0 0 1.25rem; }
.field { margin-bottom: 1rem; }
.field label { display: block; font-size: 0.8rem; font-weight: 600; color: #475569; margin-bottom: 0.35rem; }
.field input { width: 100%; padding: 0.5rem 0.75rem; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 0.9rem; box-sizing: border-box; }
.field input:focus { outline: none; border-color: #2563eb; box-shadow: 0 0 0 3px rgba(37,99,235,0.12); }
.error-banner { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; border-radius: 6px; padding: 0.6rem 0.75rem; font-size: 0.85rem; margin-bottom: 0.75rem; }
.modal-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.25rem; }
.btn-cancel { background: #f1f5f9; color: #475569; border: none; padding: 0.5rem 1rem; border-radius: 6px; font-size: 0.9rem; cursor: pointer; }
.btn-cancel:hover { background: #e2e8f0; }
.btn-save { background: #2563eb; color: white; border: none; padding: 0.5rem 1.2rem; border-radius: 6px; font-size: 0.9rem; font-weight: 600; cursor: pointer; }
.btn-save:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-save:hover:not(:disabled) { background: #1d4ed8; }
</style>
