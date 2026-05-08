<template>
  <main class="page">
    <!-- Header -->
    <div class="page-head">
      <div>
        <h2 class="page-title">Students</h2>
        <p class="page-sub">{{ total }} total students</p>
      </div>
      <router-link to="/students/new" class="btn btn--primary">+ Add Student</router-link>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <input
        id="student-search"
        v-model="q"
        placeholder="Search name or admission no…"
        class="search-input"
        @keyup.enter="load"
      />
      <SectionFilter v-model:modelClass="classId" v-model:modelSection="sectionId" />
      <select id="student-status-filter" v-model="statusFilter" class="sel">
        <option value="">All Statuses</option>
        <option value="active">Active</option>
        <option value="promoted">Promoted</option>
        <option value="left">Left</option>
        <option value="detained">Detained</option>
      </select>
      <select id="student-year-filter" v-model="yearId" class="sel">
        <option value="">All Years</option>
        <option v-for="y in years" :key="y.id" :value="y.id">{{ y.name }}</option>
      </select>
      <button class="btn btn--search" @click="load">Search</button>
      <button class="btn btn--ghost" @click="reset">Reset</button>
    </div>

    <!-- Error -->
    <div v-if="error" class="error-msg">{{ error }}</div>

    <!-- Table -->
    <div class="table-wrap">
      <table class="table" v-if="students.length > 0">
        <thead>
          <tr>
            <th>Adm. No.</th>
            <th>Name</th>
            <th>Class</th>
            <th>Section</th>
            <th>Guardian Phone</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in students" :key="s.id" class="table-row">
            <td class="mono">{{ s.admission_no }}</td>
            <td class="name-cell">
              <div class="avatar">{{ initials(s) }}</div>
              <span>{{ s.first_name }} {{ s.last_name }}</span>
            </td>
            <td>{{ s.class_name }}</td>
            <td>{{ s.section_name || '—' }}</td>
            <td>{{ primaryPhone(s) }}</td>
            <td><StatusBadge :status="s.status" /></td>
            <td>
              <router-link :to="`/students/${s.id}`" class="link-btn">View →</router-link>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else-if="!loading" class="empty">No students found.</div>
      <div v-if="loading" class="loading">Loading…</div>
    </div>

    <!-- Pagination -->
    <div class="pagination" v-if="total > pageSize">
      <button :disabled="offset === 0" @click="prev" class="btn btn--ghost">← Prev</button>
      <span class="page-info">{{ offset + 1 }}–{{ Math.min(offset + pageSize, total) }} of {{ total }}</span>
      <button :disabled="offset + pageSize >= total" @click="next" class="btn btn--ghost">Next →</button>
    </div>
  </main>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import api from '../api'
import StatusBadge from '../components/StatusBadge.vue'
import SectionFilter from '../components/SectionFilter.vue'

const students = ref([])
const total = ref(0)
const loading = ref(false)
const error = ref('')
const q = ref('')
const classId = ref(null)
const sectionId = ref(null)
const statusFilter = ref('')
const yearId = ref('')
const years = ref([])
const pageSize = 50
const offset = ref(0)

const initials = (s) => `${s.first_name?.[0] || ''}${s.last_name?.[0] || ''}`.toUpperCase()
const primaryPhone = (s) => s.guardians?.find(g => g.is_primary)?.phone || s.phone || '—'

const load = async () => {
  loading.value = true
  error.value = ''
  try {
    const params = new URLSearchParams({ limit: pageSize, offset: offset.value })
    if (q.value.trim()) params.append('q', q.value.trim())
    if (classId.value) params.append('class_id', classId.value)
    if (sectionId.value) params.append('section_id', sectionId.value)
    if (statusFilter.value) params.append('status', statusFilter.value)
    if (yearId.value) params.append('academic_year_id', yearId.value)
    const { data } = await api.get(`/api/portal/erp/students?${params}`)
    students.value = data.items || []
    total.value = data.total || 0
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load students'
  } finally {
    loading.value = false
  }
}

const reset = () => {
  q.value = ''; classId.value = null; sectionId.value = null
  statusFilter.value = ''; yearId.value = ''; offset.value = 0
  load()
}
const prev = () => { offset.value = Math.max(0, offset.value - pageSize); load() }
const next = () => { offset.value += pageSize; load() }

watch([classId, sectionId, statusFilter, yearId], () => { offset.value = 0; load() })

onMounted(async () => {
  const { data } = await api.get('/api/portal/erp/lookups/academic-years')
  years.value = data
  load()
})
</script>

<style scoped>
.page { padding: 1.5rem 2rem; max-width: 1400px; margin: 0 auto; }
.page-head { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 1.25rem; }
.page-title { font-size: 1.5rem; font-weight: 800; color: #0f172a; margin: 0; }
.page-sub { color: #64748b; font-size: 0.85rem; margin: 0.2rem 0 0; }

.filters-bar { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-bottom: 1.25rem; align-items: center; }
.search-input { padding: 0.42rem 0.75rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.88rem; min-width: 220px; color: #1f2937; }
.sel { padding: 0.42rem 0.6rem; border: 1px solid #d1d5db; border-radius: 6px; font-size: 0.88rem; background: #fff; color: #1f2937; }

.btn { padding: 0.42rem 1rem; border-radius: 6px; border: none; font-size: 0.88rem; font-weight: 600; cursor: pointer; }
.btn--primary { background: #0f172a; color: #fff; text-decoration: none; display: inline-flex; align-items: center; }
.btn--search  { background: #0ea5e9; color: #fff; }
.btn--ghost   { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }
.btn:disabled { opacity: 0.4; cursor: not-allowed; }

.table-wrap { background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; overflow: hidden; }
.table { width: 100%; border-collapse: collapse; }
.table th { background: #f8fafc; padding: 0.7rem 0.9rem; text-align: left; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.04em; color: #64748b; font-weight: 700; border-bottom: 1px solid #e5e7eb; }
.table td { padding: 0.65rem 0.9rem; font-size: 0.88rem; color: #1e293b; border-bottom: 1px solid #f1f5f9; }
.table-row:hover td { background: #f8fafc; }
.table-row:last-child td { border-bottom: none; }

.name-cell { display: flex; align-items: center; gap: 0.6rem; }
.avatar { width: 30px; height: 30px; border-radius: 50%; background: #e0e7ff; color: #4f46e5; font-size: 0.72rem; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.mono { font-family: monospace; font-size: 0.82rem; color: #475569; }
.link-btn { color: #0ea5e9; font-weight: 600; text-decoration: none; font-size: 0.85rem; }
.link-btn:hover { text-decoration: underline; }

.error-msg { background: #fef2f2; color: #dc2626; padding: 0.6rem 1rem; border-radius: 6px; margin-bottom: 1rem; font-size: 0.88rem; }
.empty, .loading { padding: 3rem; text-align: center; color: #94a3b8; font-size: 0.9rem; }

.pagination { display: flex; align-items: center; gap: 0.75rem; margin-top: 1rem; }
.page-info { font-size: 0.85rem; color: #64748b; }
</style>
