<template>
  <PortalShell
    title="Chapter workspace"
    subtitle="Lesson plan portal"
    @logout="handleLogout"
    @change-password="openChangePasswordModal"
  >
    <section class="metrics">
      <div class="metric-card">
        <span>Total chapters</span>
        <strong>{{ chapters.length }}</strong>
      </div>
      <div class="metric-card">
        <span>Pending approval</span>
        <strong>{{ pendingCount }}</strong>
      </div>
      <div class="metric-card">
        <span>Concepts</span>
        <strong>{{ conceptCount }}</strong>
      </div>
      <div class="metric-card">
        <span>Sessions</span>
        <strong>{{ sessionCount }}</strong>
      </div>
    </section>

    <section class="dvm-card dvm-toolbar">
      <div class="filter-group">
        <label>Class</label>
        <select v-model="selectedClassId" class="dvm-select" @change="onClassChange">
          <option value="">All Classes</option>
          <option v-for="c in classes" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Subject</label>
        <select v-model="selectedSubjectId" class="dvm-select" @change="fetchChapters">
          <option value="">All Subjects</option>
          <option v-for="s in subjects" :key="s.id" :value="s.id">{{ formatSubjectLabel(s) }}</option>
        </select>
      </div>
      <div class="filter-group filter-search">
        <label>Search</label>
        <input v-model="chapterSearch" class="dvm-input" type="search" placeholder="Chapter title, class, subject..." />
      </div>
      <button class="dvm-btn dvm-btn--primary toolbar-action" @click="openAddModal">Add Chapter</button>
    </section>

    <div v-if="loading" class="dvm-card dvm-state">
      <div class="dvm-spinner"></div>
      <p>Loading chapters...</p>
    </div>

    <div v-else-if="error" class="dvm-error">{{ error }}</div>

    <div v-else-if="filteredChapters.length === 0" class="dvm-empty">
      <p>No chapters found.</p>
      <p v-if="auth.isAdmin">Use Add Chapter to create one, or upload an xlsx file from the chapter editor.</p>
      <p v-else>Use Add Chapter to create one for your assigned subjects.</p>
    </div>

    <div v-else class="dvm-table-wrap">
      <table class="dvm-table">
        <thead>
          <tr>
            <th>Class</th>
            <th>Subject</th>
            <th>Chapter</th>
            <th>Concepts</th>
            <th>Sessions</th>
            <th>Status</th>
            <th class="actions-head">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="ch in filteredChapters" :key="ch.id">
            <td>{{ ch.class_name }}</td>
            <td>{{ ch.subject_name }}</td>
            <td class="title-cell">
              <strong>{{ ch.title }}</strong>
              <span v-if="!ch.is_approved && ch.pending_change_summary" class="pending-change-note">
                Changed: {{ ch.pending_change_summary }}
              </span>
            </td>
            <td>{{ ch.concept_count }}</td>
            <td>{{ ch.sessions_total }}</td>
            <td>
              <span class="dvm-badge" :class="ch.is_approved ? 'dvm-badge--approved' : 'dvm-badge--pending'">
                {{ ch.is_approved ? 'Approved' : 'Pending' }}
              </span>
            </td>
            <td class="actions-cell">
              <button class="dvm-icon-btn" title="Edit" @click="router.push(`/portal/chapter/${ch.id}/edit`)">E</button>
              <button
                v-if="canVerifyChanges && !ch.is_approved"
                class="dvm-icon-btn"
                title="Approve"
                :disabled="ch.approving"
                @click="approveChapter(ch)"
              >
                <span v-if="ch.approving" class="spinner-inline"></span>
                <span v-else>A</span>
              </button>
              <button
                v-if="auth.isAdmin"
                class="dvm-icon-btn danger"
                title="Delete"
                :disabled="ch.deleting"
                @click="deleteChapter(ch)"
              >
                <span v-if="ch.deleting" class="spinner-inline"></span>
                <span v-else>D</span>
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

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
            <select v-model="newChapter.class_id" required @change="newChapter.subject_id = ''">
              <option value="">{{ modalClassOptions.length ? 'Select class' : 'No classes available' }}</option>
              <option v-for="c in modalClassOptions" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>
          <div class="field">
            <label>Subject *</label>
            <select v-model="newChapter.subject_id" required :disabled="!newChapter.class_id">
              <option value="">{{ newChapter.class_id ? 'Select subject' : 'Select class first' }}</option>
              <option v-for="s in modalSubjects" :key="s.id" :value="s.id">{{ formatSubjectLabel(s) }}</option>
            </select>
          </div>
          <div class="field">
            <label>Order Index</label>
            <input v-model.number="newChapter.order_index" type="number" min="0" class="input-sm" />
          </div>
          <div v-if="createError" class="error-banner">{{ createError }}</div>
          <div class="modal-actions">
            <button type="button" class="dvm-btn" @click="showAddModal = false">Cancel</button>
            <button type="submit" class="dvm-btn dvm-btn--primary" :disabled="creating">
              {{ creating ? 'Creating...' : 'Create' }}
            </button>
          </div>
        </form>
      </div>
    </div>

    <div v-if="showPasswordModal" class="modal-overlay" @click.self="closeChangePasswordModal">
      <div class="modal">
        <h2 class="modal-title">Change Password</h2>
        <form @submit.prevent="changePassword">
          <div class="field">
            <label>Current Password *</label>
            <input v-model="passwordForm.current_password" type="password" required autocomplete="current-password" />
          </div>
          <div class="field">
            <label>New Password *</label>
            <input v-model="passwordForm.new_password" type="password" required minlength="6" autocomplete="new-password" />
          </div>
          <div class="field">
            <label>Confirm New Password *</label>
            <input v-model="passwordForm.confirm_password" type="password" required minlength="6" autocomplete="new-password" />
          </div>
          <div v-if="passwordError" class="error-banner">{{ passwordError }}</div>
          <div v-if="passwordSuccess" class="success-banner">{{ passwordSuccess }}</div>
          <div class="modal-actions">
            <button type="button" class="dvm-btn" @click="closeChangePasswordModal">Cancel</button>
            <button type="submit" class="dvm-btn dvm-btn--primary" :disabled="changingPassword">
              {{ changingPassword ? 'Updating...' : 'Update Password' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </PortalShell>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api.js'
import PortalShell from '../components/PortalShell.vue'

const router = useRouter()
const auth = useAuthStore()

const classes = ref([])
const subjects = ref([])
const chapters = ref([])
const selectedClassId = ref('')
const selectedSubjectId = ref('')
const chapterSearch = ref('')
const loading = ref(false)
const error = ref('')

const showAddModal = ref(false)
const allModalSubjects = ref([])
const newChapter = ref({ title: '', aim: '', class_id: '', subject_id: '', order_index: 0 })
const creating = ref(false)
const createError = ref('')
const showPasswordModal = ref(false)
const passwordForm = ref({ current_password: '', new_password: '', confirm_password: '' })
const changingPassword = ref(false)
const passwordError = ref('')
const passwordSuccess = ref('')

const canVerifyChanges = computed(() => ['hm', 'principal'].includes(auth.user?.role))
const pendingCount = computed(() => chapters.value.filter(ch => !ch.is_approved).length)
const conceptCount = computed(() => chapters.value.reduce((sum, ch) => sum + Number(ch.concept_count || 0), 0))
const sessionCount = computed(() => chapters.value.reduce((sum, ch) => sum + Number(ch.sessions_total || 0), 0))

const filteredChapters = computed(() => {
  const q = chapterSearch.value.trim().toLowerCase()
  if (!q) return chapters.value
  return chapters.value.filter(ch => {
    return [ch.title, ch.class_name, ch.subject_name].some(value => String(value || '').toLowerCase().includes(q))
  })
})

const modalClassOptions = computed(() => {
  if (auth.isAdmin) return classes.value

  const seen = new Set()
  const scoped = []
  for (const subject of allModalSubjects.value) {
    const classId = Number(subject.class_id)
    if (!classId || seen.has(classId)) continue
    seen.add(classId)
    const fallback = classes.value.find(c => Number(c.id) === classId)
    scoped.push({
      id: classId,
      name: subject.class_name || fallback?.name || `Class ${classId}`,
    })
  }
  return scoped
})

const modalSubjects = computed(() => {
  if (!newChapter.value.class_id) return []
  const classId = Number(newChapter.value.class_id)
  return allModalSubjects.value.filter(s => Number(s.class_id) === classId)
})

async function openAddModal() {
  newChapter.value = { title: '', aim: '', class_id: '', subject_id: '', order_index: 0 }
  createError.value = ''
  allModalSubjects.value = []
  try {
    const res = await api.get('/api/portal/my-subjects')
    allModalSubjects.value = res.data
    if (!auth.isAdmin && modalClassOptions.value.length === 1) {
      newChapter.value.class_id = String(modalClassOptions.value[0].id)
    }
  } catch (_) {}
  showAddModal.value = true
}

onMounted(async () => {
  await ensureUser()
  await loadClasses()
  await loadAllSubjects()
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
      const cls = classes.value.find(c => Number(c.id) === Number(selectedClassId.value))
      subjects.value = res.data.map(s => ({ ...s, class_id: cls?.id, class_name: cls?.name }))
    } catch (_) {}
  } else {
    await loadAllSubjects()
  }
  await fetchChapters()
}

async function loadAllSubjects() {
  if (!classes.value.length) {
    subjects.value = []
    return
  }

  try {
    const subjectResponses = await Promise.all(
      classes.value.map(c => api.get(`/api/public/classes/${c.id}/subjects`))
    )
    const merged = []
    for (let i = 0; i < subjectResponses.length; i += 1) {
      const res = subjectResponses[i]
      const cls = classes.value[i]
      for (const subject of res.data) {
        if (!merged.find(s => s.id === subject.id)) {
          merged.push({ ...subject, class_id: cls?.id, class_name: cls?.name })
        }
      }
    }
    subjects.value = merged
  } catch (_) {
    subjects.value = []
  }
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

async function approveChapter(ch) {
  ch.approving = true
  try {
    await api.post(`/api/portal/chapters/${ch.id}/approve`)
    await fetchChapters()
  } catch (e) {
    alert(e.response?.data?.detail || 'Failed to approve chapter changes.')
  } finally {
    ch.approving = false
  }
}

function handleLogout() {
  auth.logout()
  router.replace('/login')
}

function openChangePasswordModal() {
  passwordForm.value = { current_password: '', new_password: '', confirm_password: '' }
  passwordError.value = ''
  passwordSuccess.value = ''
  showPasswordModal.value = true
}

function closeChangePasswordModal() {
  showPasswordModal.value = false
}

async function changePassword() {
  passwordError.value = ''
  passwordSuccess.value = ''
  if (passwordForm.value.new_password !== passwordForm.value.confirm_password) {
    passwordError.value = 'New password and confirmation do not match.'
    return
  }

  changingPassword.value = true
  try {
    const res = await api.post('/api/portal/auth/change-password', {
      current_password: passwordForm.value.current_password,
      new_password: passwordForm.value.new_password,
    })
    passwordSuccess.value = res.data?.message || 'Password updated successfully.'
    passwordForm.value = { current_password: '', new_password: '', confirm_password: '' }
  } catch (e) {
    passwordError.value = e.response?.data?.detail || 'Failed to update password.'
  } finally {
    changingPassword.value = false
  }
}

function formatSubjectLabel(subject) {
  const className = subject.class_name || classes.value.find(c => Number(c.id) === Number(subject.class_id))?.name
  return className ? `${className} - ${subject.name}` : subject.name
}

async function createChapter() {
  createError.value = ''
  creating.value = true
  try {
    await api.post('/api/portal/chapters', {
      title: newChapter.value.title,
      aim: newChapter.value.aim,
      subject_id: newChapter.value.subject_id,
      order_index: newChapter.value.order_index,
    })
    showAddModal.value = false
    newChapter.value = { title: '', aim: '', class_id: '', subject_id: '', order_index: 0 }
    await fetchChapters()
  } catch (e) {
    createError.value = e.response?.data?.detail || 'Failed to create chapter.'
  } finally {
    creating.value = false
  }
}

async function deleteChapter(ch) {
  if (!confirm(`Delete chapter "${ch.title}"? This will permanently remove all its concepts, exhibits, and images.`)) return
  ch.deleting = true
  try {
    await api.delete(`/api/portal/chapters/${ch.id}`)
    chapters.value = chapters.value.filter(c => c.id !== ch.id)
  } catch (e) {
    alert(e.response?.data?.detail || 'Delete failed')
    ch.deleting = false
  }
}
</script>

<style scoped>
.metrics {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 0.8rem;
  margin-bottom: 1rem;
}

.metric-card {
  background: #fff;
  border: 1px solid var(--dvm-line);
  border-radius: var(--dvm-radius-lg);
  padding: 0.9rem;
  box-shadow: var(--dvm-shadow-soft);
}

.metric-card span {
  display: block;
  color: var(--dvm-muted);
  font-size: 0.75rem;
  font-weight: 850;
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.metric-card strong {
  display: block;
  margin-top: 0.4rem;
  color: var(--dvm-text);
  font-size: 1.7rem;
  line-height: 1;
}

.filter-group {
  min-width: 155px;
}

.filter-search {
  flex: 1;
  min-width: 240px;
}

.toolbar-action {
  margin-left: auto;
}

.title-cell strong,
.title-cell span {
  display: block;
}

.pending-change-note {
  margin-top: 0.2rem;
  color: var(--dvm-amber);
  font-size: 0.78rem;
}

.actions-head {
  text-align: right;
}

.actions-cell {
  display: flex;
  justify-content: flex-end;
  gap: 0.35rem;
}

.dvm-icon-btn.danger {
  color: var(--dvm-red);
}

.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: 100;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(15, 23, 42, 0.46);
  padding: 1rem;
}

.modal {
  width: min(500px, 100%);
  background: #fff;
  border-radius: var(--dvm-radius-lg);
  border: 1px solid var(--dvm-line);
  box-shadow: 0 28px 80px rgba(15, 23, 42, 0.28);
  padding: 1.4rem;
}

.modal-title {
  margin: 0 0 1rem;
  color: var(--dvm-text);
  font-size: 1.2rem;
}

.field {
  margin-bottom: 0.9rem;
}

.field label {
  display: block;
  margin-bottom: 0.35rem;
  color: #475569;
  font-size: 0.78rem;
  font-weight: 800;
}

.field input,
.field select,
.field textarea {
  width: 100%;
  border: 1px solid var(--dvm-line);
  border-radius: 7px;
  padding: 0.6rem 0.7rem;
  outline: none;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.6rem;
  margin-top: 1.1rem;
}

.error-banner,
.success-banner {
  border-radius: 7px;
  padding: 0.65rem 0.8rem;
  font-size: 0.86rem;
}

.error-banner {
  background: #fff5f5;
  border: 1px solid #fecaca;
  color: var(--dvm-red);
}

.success-banner {
  background: #ecfdf5;
  border: 1px solid #bbf7d0;
  color: var(--dvm-green);
}

@media (max-width: 900px) {
  .metrics {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 620px) {
  .metrics {
    grid-template-columns: 1fr;
  }
}
</style>
