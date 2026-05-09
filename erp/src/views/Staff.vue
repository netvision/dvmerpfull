<template>
  <main class="page">
    <!-- Header -->
    <div class="page-head">
      <div>
        <h2 class="page-title">Staff Management</h2>
        <p class="page-sub">{{ total }} total staff members</p>
      </div>
      <router-link to="/staff/new" class="btn btn--primary">+ Add Staff</router-link>
    </div>

    <!-- Filters -->
    <div class="filters-bar">
      <input
        id="staff-search"
        v-model="q"
        placeholder="Search name, email, or code…"
        class="search-input"
        @keyup.enter="load"
      />
      <select v-model="roleFilter" class="sel">
        <option value="">All Roles</option>
        <option value="teacher">Teacher</option>
        <option value="subject_head">Subject Head</option>
        <option value="mentor">Mentor</option>
        <option value="hm">HM</option>
        <option value="principal">Principal</option>
      </select>
      <input
        v-model="deptFilter"
        placeholder="Department…"
        class="search-input"
        style="min-width: 150px;"
        @keyup.enter="load"
      />
      <button class="btn btn--search" @click="load">Search</button>
      <button class="btn btn--ghost" @click="reset">Reset</button>
    </div>

    <!-- Error -->
    <div v-if="error" class="error-msg">{{ error }}</div>

    <!-- Table -->
    <div class="table-wrap">
      <table class="table" v-if="staff.length > 0">
        <thead>
          <tr>
            <th>Code</th>
            <th>Name</th>
            <th>Role</th>
            <th>Department</th>
            <th>Designation</th>
            <th>Phone</th>
            <th>Status</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="s in staff" :key="s.id" class="table-row">
            <td class="mono">{{ s.profile?.staff_code || '—' }}</td>
            <td class="name-cell">
              <div class="avatar">{{ initials(s) }}</div>
              <div>
                <div class="name-text">{{ s.name }}</div>
                <div class="email-text">{{ s.email }}</div>
              </div>
            </td>
            <td class="role-cell">{{ formatRole(s.role) }}</td>
            <td>{{ s.profile?.department || '—' }}</td>
            <td>{{ s.profile?.designation || '—' }}</td>
            <td>{{ s.profile?.phone || '—' }}</td>
            <td>
              <span :class="['status-dot', s.is_active ? 'status-dot--active' : 'status-dot--inactive']"></span>
              {{ s.is_active ? 'Active' : 'Inactive' }}
            </td>
            <td>
              <router-link :to="`/staff/${s.id}/edit`" class="link-btn">Edit</router-link>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-else-if="!loading" class="empty">No staff members found.</div>
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

const staff = ref([])
const total = ref(0)
const loading = ref(false)
const error = ref('')
const q = ref('')
const roleFilter = ref('')
const deptFilter = ref('')
const pageSize = 50
const offset = ref(0)

const initials = (s) => s.name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
const formatRole = (r) => r.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())

const load = async () => {
  loading.value = true
  error.value = ''
  try {
    const params = new URLSearchParams({ limit: pageSize, offset: offset.value })
    if (q.value.trim()) params.append('q', q.value.trim())
    if (roleFilter.value) params.append('role', roleFilter.value)
    if (deptFilter.value.trim()) params.append('department', deptFilter.value.trim())
    
    const { data } = await api.get(`/api/portal/staff?${params}`)
    staff.value = data.items || []
    total.value = data.total || 0
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load staff'
  } finally {
    loading.value = false
  }
}

const reset = () => {
  q.value = ''; roleFilter.value = ''; deptFilter.value = ''; offset.value = 0
  load()
}
const prev = () => { offset.value = Math.max(0, offset.value - pageSize); load() }
const next = () => { offset.value += pageSize; load() }

watch([roleFilter], () => { offset.value = 0; load() })

onMounted(() => {
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

.name-cell { display: flex; align-items: center; gap: 0.75rem; }
.avatar { width: 34px; height: 34px; border-radius: 8px; background: #f1f5f9; color: #475569; font-size: 0.8rem; font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.name-text { font-weight: 600; color: #0f172a; line-height: 1.2; }
.email-text { font-size: 0.75rem; color: #64748b; }
.role-cell { font-weight: 500; color: #4f46e5; }

.status-dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%; margin-right: 6px; }
.status-dot--active { background: #22c55e; }
.status-dot--inactive { background: #94a3b8; }

.mono { font-family: monospace; font-size: 0.82rem; color: #475569; }
.link-btn { color: #0ea5e9; font-weight: 600; text-decoration: none; font-size: 0.85rem; }
.link-btn:hover { text-decoration: underline; }

.error-msg { background: #fef2f2; color: #dc2626; padding: 0.6rem 1rem; border-radius: 6px; margin-bottom: 1rem; font-size: 0.88rem; }
.empty, .loading { padding: 3rem; text-align: center; color: #94a3b8; font-size: 0.9rem; }

.pagination { display: flex; align-items: center; gap: 0.75rem; margin-top: 1rem; }
.page-info { font-size: 0.85rem; color: #64748b; }
</style>
