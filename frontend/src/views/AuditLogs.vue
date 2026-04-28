<template>
  <div class="audit-page">
    <div class="page-header">
      <h1>Audit Logs</h1>
      <div class="header-actions">
        <button class="btn-secondary" @click="router.push('/portal')">Back to Portal</button>
        <button class="btn-primary" @click="load">Refresh</button>
      </div>
    </div>

    <div class="filters-card">
      <div class="filters-grid">
        <div class="field">
          <label>Entity Type</label>
          <input v-model="filters.entity_type" placeholder="student, fee_invoice, class..." />
        </div>
        <div class="field">
          <label>Action</label>
          <input v-model="filters.action" placeholder="create, update, delete..." />
        </div>
        <div class="field">
          <label>Actor User ID</label>
          <input v-model="filters.actor_user_id" type="number" min="1" placeholder="e.g. 1" />
        </div>
        <div class="field">
          <label>Date From</label>
          <input v-model="filters.date_from" type="date" />
        </div>
        <div class="field">
          <label>Date To</label>
          <input v-model="filters.date_to" type="date" />
        </div>
      </div>
      <div class="filter-actions">
        <button class="btn-primary" @click="applyFilters">Apply</button>
        <button class="btn-secondary" @click="clearFilters">Clear</button>
      </div>
    </div>

    <div v-if="loading" class="loading-state">Loading audit logs...</div>
    <div v-else-if="error" class="error-box">{{ error }}</div>

    <div v-else class="table-wrap">
      <table class="audit-table">
        <thead>
          <tr>
            <th>Timestamp</th>
            <th>Actor</th>
            <th>Entity</th>
            <th>Entity ID</th>
            <th>Action</th>
            <th>Summary</th>
            <th>IP</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in rows" :key="row.id">
            <td>{{ formatDate(row.created_at) }}</td>
            <td>{{ row.actor_user_id ?? '-' }}</td>
            <td>{{ row.entity_type }}</td>
            <td>{{ row.entity_id }}</td>
            <td>
              <span class="action-chip">{{ row.action }}</span>
            </td>
            <td class="summary">{{ row.change_summary || '-' }}</td>
            <td>{{ row.ip_address || '-' }}</td>
          </tr>
          <tr v-if="rows.length === 0">
            <td colspan="7" class="empty-cell">No audit logs found for current filter.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="pagination" v-if="total > 0">
      <button class="btn-secondary" :disabled="offset === 0" @click="previousPage">Previous</button>
      <span>
        Showing {{ offset + 1 }} - {{ Math.min(offset + limit, total) }} of {{ total }}
      </span>
      <button class="btn-secondary" :disabled="offset + limit >= total" @click="nextPage">Next</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'

const router = useRouter()

const loading = ref(false)
const error = ref('')
const rows = ref([])
const total = ref(0)
const limit = ref(50)
const offset = ref(0)

const filters = reactive({
  entity_type: '',
  action: '',
  actor_user_id: '',
  date_from: '',
  date_to: '',
})

const buildParams = () => {
  const params = new URLSearchParams()
  params.append('limit', String(limit.value))
  params.append('offset', String(offset.value))

  if (filters.entity_type.trim()) params.append('entity_type', filters.entity_type.trim())
  if (filters.action.trim()) params.append('action', filters.action.trim())
  if (filters.actor_user_id) params.append('actor_user_id', String(filters.actor_user_id))
  if (filters.date_from) params.append('date_from', filters.date_from)
  if (filters.date_to) params.append('date_to', filters.date_to)

  return params
}

const load = async () => {
  loading.value = true
  error.value = ''

  try {
    const params = buildParams()
    const { data } = await api.get(`/api/portal/erp/audit-logs?${params.toString()}`)
    rows.value = data.items || []
    total.value = data.total || 0
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to load audit logs'
  } finally {
    loading.value = false
  }
}

const applyFilters = async () => {
  offset.value = 0
  await load()
}

const clearFilters = async () => {
  filters.entity_type = ''
  filters.action = ''
  filters.actor_user_id = ''
  filters.date_from = ''
  filters.date_to = ''
  offset.value = 0
  await load()
}

const nextPage = async () => {
  offset.value += limit.value
  await load()
}

const previousPage = async () => {
  offset.value = Math.max(0, offset.value - limit.value)
  await load()
}

const formatDate = (raw) => {
  if (!raw) return '-'
  const d = new Date(raw)
  if (Number.isNaN(d.getTime())) return raw
  return d.toLocaleString()
}

onMounted(load)
</script>

<style scoped>
.audit-page {
  padding: 1.5rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.page-header h1 {
  margin: 0;
  font-size: 1.6rem;
}

.header-actions {
  display: flex;
  gap: 0.6rem;
}

.filters-card {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 0.75rem;
}

.field label {
  display: block;
  font-size: 0.82rem;
  font-weight: 600;
  margin-bottom: 0.3rem;
  color: #475569;
}

.field input {
  width: 100%;
  padding: 0.5rem 0.6rem;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  font-size: 0.9rem;
}

.filter-actions {
  display: flex;
  gap: 0.6rem;
  margin-top: 0.8rem;
}

.loading-state,
.error-box {
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  padding: 0.8rem;
  margin-bottom: 1rem;
}

.error-box {
  color: #b91c1c;
  border-color: #fecaca;
  background: #fef2f2;
}

.table-wrap {
  overflow-x: auto;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 8px;
}

.audit-table {
  width: 100%;
  border-collapse: collapse;
}

.audit-table th,
.audit-table td {
  border-bottom: 1px solid #e2e8f0;
  padding: 0.55rem 0.6rem;
  font-size: 0.86rem;
  text-align: left;
  vertical-align: top;
}

.audit-table th {
  background: #f8fafc;
  font-weight: 700;
}

.summary {
  max-width: 340px;
}

.action-chip {
  display: inline-block;
  padding: 0.1rem 0.45rem;
  border-radius: 999px;
  border: 1px solid #bae6fd;
  background: #ecfeff;
  color: #0e7490;
  font-size: 0.78rem;
  font-weight: 600;
}

.empty-cell {
  text-align: center;
  color: #64748b;
}

.pagination {
  margin-top: 0.9rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn-primary,
.btn-secondary {
  border: none;
  border-radius: 6px;
  padding: 0.5rem 0.8rem;
  cursor: pointer;
  font-size: 0.88rem;
  font-weight: 600;
}

.btn-primary {
  background: #0ea5e9;
  color: white;
}

.btn-secondary {
  background: #e2e8f0;
  color: #0f172a;
}

.btn-secondary:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

@media (max-width: 1200px) {
  .filters-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
