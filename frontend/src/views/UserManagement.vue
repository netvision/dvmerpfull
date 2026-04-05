<template>
  <div class="um-page">
    <!-- Navbar -->
    <nav class="navbar">
      <div class="nav-left">
        <span class="nav-title">User Management</span>
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
        <h1 class="page-title">Users</h1>
        <button class="add-btn" @click="openAddModal">+ Add User</button>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading users…</p>
      </div>

      <!-- Error -->
      <div v-else-if="error" class="error-box">{{ error }}</div>

      <!-- Empty -->
      <div v-else-if="users.length === 0" class="empty-state">
        <p>No users found.</p>
      </div>

      <!-- Users Table -->
      <div v-else class="table-wrapper">
        <table class="data-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td class="name-cell">{{ u.name }}</td>
              <td>{{ u.email }}</td>
              <td>
                <span class="role-badge" :class="u.role">{{ u.role }}</span>
              </td>
              <td>
                <span class="status-badge" :class="u.is_active ? 'active' : 'inactive'">
                  {{ u.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td class="actions-cell">
                <button class="btn-edit" @click="openEditModal(u)">Edit</button>
                <button
                  v-if="u.role === 'teacher'"
                  class="btn-subjects"
                  @click="openSubjectsModal(u)"
                >
                  Assign Subjects
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Add User Modal -->
    <div v-if="showAddModal" class="modal-overlay" @click.self="showAddModal = false">
      <div class="modal">
        <h2 class="modal-title">Add User</h2>
        <form @submit.prevent="createUser">
          <div class="field">
            <label>Name *</label>
            <input v-model="newUser.name" type="text" required placeholder="Full name" />
          </div>
          <div class="field">
            <label>Email *</label>
            <input v-model="newUser.email" type="email" required placeholder="email@school.com" />
          </div>
          <div class="field">
            <label>Password *</label>
            <input v-model="newUser.password" type="password" required placeholder="Password" />
          </div>
          <div class="field">
            <label>Role *</label>
            <select v-model="newUser.role" required>
              <option value="teacher">Teacher</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div v-if="addError" class="error-banner">{{ addError }}</div>
          <div class="modal-actions">
            <button type="button" class="btn-cancel" @click="showAddModal = false">Cancel</button>
            <button type="submit" class="btn-save" :disabled="adding">
              {{ adding ? 'Creating…' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit User Modal -->
    <div v-if="showEditModal" class="modal-overlay" @click.self="closeEditModal">
      <div class="modal">
        <h2 class="modal-title">Edit User</h2>
        <form @submit.prevent="saveEdit">
          <div class="field">
            <label>Name *</label>
            <input v-model="editUser.name" type="text" required placeholder="Full name" />
          </div>
          <div class="field">
            <label>Email *</label>
            <input v-model="editUser.email" type="email" required placeholder="email@school.com" />
          </div>
          <div class="field">
            <label>Role *</label>
            <select v-model="editUser.role" required>
              <option value="teacher">Teacher</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div class="field">
            <label class="toggle-label">
              <span>Active</span>
              <div class="toggle-wrapper">
                <input
                  id="active-toggle"
                  v-model="editUser.is_active"
                  type="checkbox"
                  class="toggle-input"
                />
                <label for="active-toggle" class="toggle-track">
                  <span class="toggle-thumb"></span>
                </label>
              </div>
            </label>
          </div>
          <div v-if="editError" class="error-banner">{{ editError }}</div>
          <div class="modal-actions">
            <button type="button" class="btn-cancel" @click="closeEditModal">Cancel</button>
            <button type="submit" class="btn-save" :disabled="saving">
              {{ saving ? 'Saving…' : 'Save' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Assign Subjects Modal -->
    <div v-if="showSubjectsModal" class="modal-overlay" @click.self="closeSubjectsModal">
      <div class="modal modal-wide">
        <h2 class="modal-title">Assign Subjects — {{ subjectTarget?.name }}</h2>
        <p class="modal-subtitle">Class 6 subjects</p>

        <div v-if="subjectsLoading" class="subjects-loading">
          <div class="spinner"></div>
        </div>
        <div v-else class="subjects-grid">
          <label
            v-for="s in allSubjects"
            :key="s.id"
            class="subject-item"
            :class="{ selected: selectedSubjectIds.includes(s.id) }"
          >
            <input
              type="checkbox"
              :value="s.id"
              v-model="selectedSubjectIds"
              class="subject-checkbox"
            />
            <span v-if="s.icon" class="subject-icon">{{ s.icon }}</span>
            <span class="subject-name">{{ s.name }}</span>
          </label>
        </div>

        <div v-if="subjectsError" class="error-banner">{{ subjectsError }}</div>
        <div class="modal-actions">
          <button type="button" class="btn-cancel" @click="closeSubjectsModal">Cancel</button>
          <button class="btn-save" :disabled="assigningSubs" @click="saveSubjects">
            {{ assigningSubs ? 'Saving…' : 'Save' }}
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

// ── Users list ──────────────────────────────────────────────────────────────
const users = ref([])
const loading = ref(false)
const error = ref('')

onMounted(async () => {
  if (!auth.user) {
    try { await auth.fetchMe() } catch (_) {}
  }
  await fetchUsers()
  await loadAllSubjects()
})

async function fetchUsers() {
  loading.value = true
  error.value = ''
  try {
    const res = await api.get('/api/users/')
    users.value = res.data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load users.'
  } finally {
    loading.value = false
  }
}

// ── Add User Modal ───────────────────────────────────────────────────────────
const showAddModal = ref(false)
const newUser = ref({ name: '', email: '', password: '', role: 'teacher' })
const adding = ref(false)
const addError = ref('')

function openAddModal() {
  newUser.value = { name: '', email: '', password: '', role: 'teacher' }
  addError.value = ''
  showAddModal.value = true
}

async function createUser() {
  addError.value = ''
  adding.value = true
  try {
    await api.post('/api/users/', {
      name: newUser.value.name,
      email: newUser.value.email,
      password: newUser.value.password,
      role: newUser.value.role,
    })
    showAddModal.value = false
    await fetchUsers()
  } catch (e) {
    addError.value = e.response?.data?.detail || 'Failed to create user.'
  } finally {
    adding.value = false
  }
}

// ── Edit User Modal ──────────────────────────────────────────────────────────
const showEditModal = ref(false)
const editUser = ref({ id: null, name: '', email: '', role: 'teacher', is_active: true })
const saving = ref(false)
const editError = ref('')

function openEditModal(u) {
  editUser.value = { id: u.id, name: u.name, email: u.email, role: u.role, is_active: u.is_active }
  editError.value = ''
  showEditModal.value = true
}

function closeEditModal() {
  showEditModal.value = false
}

async function saveEdit() {
  editError.value = ''
  saving.value = true
  try {
    await api.put(`/api/users/${editUser.value.id}`, {
      name: editUser.value.name,
      email: editUser.value.email,
      role: editUser.value.role,
      is_active: editUser.value.is_active,
    })
    showEditModal.value = false
    await fetchUsers()
  } catch (e) {
    editError.value = e.response?.data?.detail || 'Failed to save changes.'
  } finally {
    saving.value = false
  }
}

// ── Assign Subjects Modal ───────────────────────────────────────────────────
const showSubjectsModal = ref(false)
const subjectTarget = ref(null)
const allSubjects = ref([])
const selectedSubjectIds = ref([])
const subjectsLoading = ref(false)
const subjectsError = ref('')
const assigningSubs = ref(false)

async function loadAllSubjects() {
  try {
    const res = await api.get('/api/public/classes/1/subjects')
    allSubjects.value = res.data
  } catch (_) {}
}

async function openSubjectsModal(u) {
  subjectTarget.value = u
  subjectsError.value = ''
  selectedSubjectIds.value = []
  showSubjectsModal.value = true
  subjectsLoading.value = true
  try {
    const res = await api.get(`/api/users/${u.id}/subjects`)
    selectedSubjectIds.value = res.data.map(s => s.id)
  } catch (_) {
    subjectsError.value = 'Could not load current subjects.'
  } finally {
    subjectsLoading.value = false
  }
}

function closeSubjectsModal() {
  showSubjectsModal.value = false
  subjectTarget.value = null
}

async function saveSubjects() {
  subjectsError.value = ''
  assigningSubs.value = true
  try {
    await api.post(`/api/users/${subjectTarget.value.id}/subjects`, {
      subject_ids: selectedSubjectIds.value,
    })
    showSubjectsModal.value = false
  } catch (e) {
    subjectsError.value = e.response?.data?.detail || 'Failed to assign subjects.'
  } finally {
    assigningSubs.value = false
  }
}
</script>

<style scoped>
/* ── Base ─────────────────────────────────────────────────────────────────── */
.um-page {
  min-height: 100vh;
  background: #f1f5f9;
  font-family: system-ui, -apple-system, sans-serif;
}

/* ── Navbar ───────────────────────────────────────────────────────────────── */
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

.nav-left {
  display: flex;
  align-items: center;
  gap: 1.2rem;
}

.nav-title {
  font-size: 1.15rem;
  font-weight: 700;
  letter-spacing: 0.02em;
}

.back-link {
  font-size: 0.85rem;
  color: rgba(255,255,255,0.65);
  text-decoration: none;
  transition: color 0.15s;
}

.back-link:hover {
  color: white;
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
  color: white;
}

/* ── Role / Status Badges ─────────────────────────────────────────────────── */
.role-badge {
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  padding: 0.2rem 0.55rem;
  border-radius: 20px;
}

.role-badge.admin {
  background: #7c3aed;
  color: white;
}

.role-badge.teacher {
  background: #0ea5e9;
  color: white;
}

.status-badge {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  padding: 0.22rem 0.6rem;
  border-radius: 20px;
}

.status-badge.active {
  background: #dcfce7;
  color: #16a34a;
}

.status-badge.inactive {
  background: #f1f5f9;
  color: #94a3b8;
}

/* ── Content ──────────────────────────────────────────────────────────────── */
.content {
  max-width: 1100px;
  margin: 0 auto;
  padding: 1.5rem 1rem;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1.2rem;
}

.page-title {
  font-size: 1.3rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.add-btn {
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

/* ── Table ────────────────────────────────────────────────────────────────── */
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

.name-cell {
  font-weight: 600;
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

.btn-subjects {
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

.btn-subjects:hover {
  background: #f0f9ff;
}

/* ── States ───────────────────────────────────────────────────────────────── */
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

/* ── Modal ────────────────────────────────────────────────────────────────── */
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

.modal-wide {
  max-width: 560px;
}

.modal-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.25rem;
}

.modal-subtitle {
  font-size: 0.85rem;
  color: #64748b;
  margin: 0 0 1.2rem;
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
.field select:focus {
  border-color: #4f46e5;
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
  transition: background 0.15s;
}

.btn-save:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.btn-save:hover:not(:disabled) {
  background: #4338ca;
}

/* ── Toggle Switch ───────────────────────────────────────────────────────── */
.toggle-label {
  display: flex !important;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
}

.toggle-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.toggle-input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-track {
  display: inline-block;
  width: 42px;
  height: 24px;
  background: #cbd5e1;
  border-radius: 12px;
  position: relative;
  cursor: pointer;
  transition: background 0.2s;
}

.toggle-input:checked + .toggle-track {
  background: #4f46e5;
}

.toggle-thumb {
  position: absolute;
  top: 3px;
  left: 3px;
  width: 18px;
  height: 18px;
  background: white;
  border-radius: 50%;
  transition: transform 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.2);
}

.toggle-input:checked + .toggle-track .toggle-thumb {
  transform: translateX(18px);
}

/* ── Subjects Grid ───────────────────────────────────────────────────────── */
.subjects-loading {
  display: flex;
  justify-content: center;
  padding: 1.5rem 0;
}

.subjects-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.6rem;
  margin-bottom: 0.5rem;
  max-height: 300px;
  overflow-y: auto;
  padding: 0.25rem 0.1rem;
}

.subject-item {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  padding: 0.55rem 0.75rem;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  font-size: 0.88rem;
  color: #374151;
  transition: border-color 0.15s, background 0.15s;
  user-select: none;
}

.subject-item:hover {
  border-color: #a5b4fc;
  background: #f5f3ff;
}

.subject-item.selected {
  border-color: #4f46e5;
  background: #eef2ff;
  color: #4f46e5;
  font-weight: 600;
}

.subject-checkbox {
  display: none;
}

.subject-icon {
  font-size: 1.1rem;
  line-height: 1;
}

.subject-name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ── Responsive ──────────────────────────────────────────────────────────── */
@media (max-width: 640px) {
  .navbar { padding: 0 1rem; }
  .user-name { display: none; }
  .data-table th, .data-table td { padding: 0.6rem 0.7rem; }
  .actions-cell { flex-wrap: wrap; }
}
</style>
