<template>
  <main class="page">
    <div class="page-head">
      <h2 class="page-title">Department Management</h2>
      <button @click="showForm = true" class="btn btn--primary">+ Add Department</button>
    </div>

    <!-- Dept List -->
    <div class="table-container">
      <table class="data-table">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="dept in departments" :key="dept.id">
            <td><strong>{{ dept.name }}</strong></td>
            <td>{{ dept.description || '—' }}</td>
            <td>
              <div class="actions">
                <button @click="edit(dept)" class="action-btn action-btn--edit">Edit</button>
                <button @click="remove(dept)" class="action-btn action-btn--delete">Delete</button>
              </div>
            </td>
          </tr>
          <tr v-if="departments.length === 0">
            <td colspan="3" class="empty-state">No departments found.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal Form -->
    <div v-if="showForm" class="modal-overlay">
      <div class="modal">
        <div class="modal-head">
          <h3>{{ editingId ? 'Edit Department' : 'New Department' }}</h3>
          <button @click="closeForm" class="close-btn">&times;</button>
        </div>
        <form @submit.prevent="submit" class="modal-body">
          <div class="field">
            <label>Department Name *</label>
            <input v-model="form.name" required placeholder="e.g. Science" />
          </div>
          <div class="field">
            <label>Description</label>
            <textarea v-model="form.description" rows="3" placeholder="Optional notes..." />
          </div>
          <div v-if="error" class="error-msg">{{ error }}</div>
          <div class="modal-actions">
            <button type="button" @click="closeForm" class="btn btn--ghost">Cancel</button>
            <button type="submit" class="btn btn--primary" :disabled="submitting">
              {{ submitting ? 'Saving...' : 'Save Department' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../api'

const departments = ref([])
const showForm = ref(false)
const submitting = ref(false)
const error = ref('')
const editingId = ref(null)

const form = ref({ name: '', description: '' })

onMounted(fetchDepartments)

async function fetchDepartments() {
  try {
    const { data } = await api.get('/api/portal/departments')
    departments.value = data
  } catch (e) {
    console.error('Failed to fetch departments', e)
  }
}

function edit(dept) {
  editingId.value = dept.id
  form.value = { name: dept.name, description: dept.description || '' }
  showForm.value = true
}

async function remove(dept) {
  if (!confirm(`Are you sure you want to delete "${dept.name}"?`)) return
  try {
    await api.delete(`/api/portal/departments/${dept.id}`)
    await fetchDepartments()
  } catch (e) {
    alert(e.response?.data?.detail || 'Delete failed')
  }
}

function closeForm() {
  showForm.value = false
  editingId.value = null
  form.value = { name: '', description: '' }
  error.value = ''
}

async function submit() {
  submitting.value = true
  error.value = ''
  try {
    if (editingId.value) {
      await api.put(`/api/portal/departments/${editingId.value}`, form.value)
    } else {
      await api.post('/api/portal/departments', form.value)
    }
    await fetchDepartments()
    closeForm()
  } catch (e) {
    error.value = e.response?.data?.detail || 'Operation failed'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.page { padding: 1.5rem 2rem; max-width: 1200px; margin: 0 auto; }
.page-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.page-title { font-size: 1.5rem; font-weight: 800; color: #0f172a; margin: 0; }

.table-container { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; overflow: hidden; }
.data-table { width: 100%; border-collapse: collapse; text-align: left; }
.data-table th { background: #f8fafc; padding: 0.75rem 1rem; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; color: #64748b; border-bottom: 1px solid #e5e7eb; }
.data-table td { padding: 1rem; border-bottom: 1px solid #f1f5f9; font-size: 0.88rem; color: #334155; }
.empty-state { text-align: center; padding: 3rem; color: #94a3b8; }

.actions { display: flex; gap: 0.5rem; }
.action-btn { padding: 0.35rem 0.7rem; border-radius: 4px; border: 1px solid #e2e8f0; font-size: 0.75rem; font-weight: 600; cursor: pointer; background: #fff; }
.action-btn--edit { color: #0ea5e9; }
.action-btn--delete { color: #ef4444; }

.modal-overlay { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.4); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.modal { background: #fff; width: 450px; border-radius: 12px; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.1); }
.modal-head { display: flex; justify-content: space-between; align-items: center; padding: 1rem 1.5rem; border-bottom: 1px solid #f1f5f9; }
.modal-head h3 { margin: 0; font-size: 1.1rem; color: #0f172a; }
.close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: #94a3b8; }
.modal-body { padding: 1.5rem; }

.field { margin-bottom: 1rem; }
label { display: block; font-size: 0.82rem; font-weight: 600; color: #475569; margin-bottom: 0.35rem; }
input, textarea { width: 100%; padding: 0.5rem 0.75rem; border: 1px solid #d1d5db; border-radius: 6px; box-sizing: border-box; }

.modal-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.5rem; }
.btn { padding: 0.5rem 1.25rem; border-radius: 6px; border: none; font-size: 0.88rem; font-weight: 600; cursor: pointer; }
.btn--primary { background: #0f172a; color: #fff; }
.btn--ghost { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }

.error-msg { color: #ef4444; font-size: 0.82rem; margin-bottom: 0.5rem; }
</style>
