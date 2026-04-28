<template>
  <main class="page">
    <div class="head">
      <h2>Audit Logs</h2>
      <button @click="load">Refresh</button>
    </div>

    <div class="filters">
      <input v-model="filters.entity_type" placeholder="Entity type (student, fee_invoice...)" />
      <input v-model="filters.action" placeholder="Action (create, update...)" />
      <input v-model="filters.actor_user_id" type="number" placeholder="Actor user id" />
      <input v-model="filters.date_from" type="date" />
      <input v-model="filters.date_to" type="date" />
      <button @click="load">Apply</button>
      <button class="muted-btn" @click="resetFilters">Clear</button>
    </div>

    <div v-if="error" class="error">{{ error }}</div>

    <table class="table">
      <thead>
        <tr>
          <th>Time</th>
          <th>Actor</th>
          <th>Entity</th>
          <th>ID</th>
          <th>Action</th>
          <th>Summary</th>
          <th>IP</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="row in rows" :key="row.id">
          <td>{{ fmt(row.created_at) }}</td>
          <td>{{ row.actor_user_id ?? '-' }}</td>
          <td>{{ row.entity_type }}</td>
          <td>{{ row.entity_id }}</td>
          <td><span class="badge">{{ row.action }}</span></td>
          <td class="summary">{{ row.change_summary || '-' }}</td>
          <td>{{ row.ip_address || '-' }}</td>
        </tr>
        <tr v-if="!rows.length">
          <td colspan="7" class="empty">No audit logs found</td>
        </tr>
      </tbody>
    </table>

    <div class="pager">
      <button :disabled="offset === 0" @click="prev">Previous</button>
      <span>Showing {{ offset + 1 }} - {{ Math.min(offset + limit, total) }} of {{ total }}</span>
      <button :disabled="offset + limit >= total" @click="next">Next</button>
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import api from '../api'

const rows = ref([])
const total = ref(0)
const offset = ref(0)
const limit = ref(50)
const error = ref('')

const filters = ref({
  entity_type: '',
  action: '',
  actor_user_id: '',
  date_from: '',
  date_to: '',
})

const buildQuery = () => {
  const params = new URLSearchParams()
  params.append('limit', String(limit.value))
  params.append('offset', String(offset.value))

  if (filters.value.entity_type.trim()) params.append('entity_type', filters.value.entity_type.trim())
  if (filters.value.action.trim()) params.append('action', filters.value.action.trim())
  if (filters.value.actor_user_id) params.append('actor_user_id', String(filters.value.actor_user_id))
  if (filters.value.date_from) params.append('date_from', filters.value.date_from)
  if (filters.value.date_to) params.append('date_to', filters.value.date_to)

  return params.toString()
}

const load = async () => {
  error.value = ''
  try {
    const { data } = await api.get(`/api/portal/erp/audit-logs?${buildQuery()}`)
    rows.value = data.items || []
    total.value = data.total || 0
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load audit logs'
  }
}

const resetFilters = () => {
  filters.value = {
    entity_type: '',
    action: '',
    actor_user_id: '',
    date_from: '',
    date_to: '',
  }
  offset.value = 0
  load()
}

const next = async () => {
  offset.value += limit.value
  await load()
}

const prev = async () => {
  offset.value = Math.max(0, offset.value - limit.value)
  await load()
}

const fmt = (dt) => {
  if (!dt) return '-'
  const d = new Date(dt)
  return Number.isNaN(d.getTime()) ? dt : d.toLocaleString()
}

load()
</script>

<style scoped>
.page { padding: 1rem; }
.head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }
.filters { display: grid; grid-template-columns: repeat(7, minmax(0, 1fr)); gap: 0.45rem; margin-bottom: 0.8rem; }
input, button { padding: 0.5rem 0.7rem; border: 1px solid #d1d5db; border-radius: 6px; }
button { background: #0ea5e9; color: #fff; border: 0; cursor: pointer; }
.muted-btn { background: #64748b; }
.table { width: 100%; border-collapse: collapse; background: #fff; }
.table th, .table td { border-bottom: 1px solid #e5e7eb; padding: 0.5rem; text-align: left; font-size: 0.9rem; vertical-align: top; }
.badge { background: #ecfeff; color: #155e75; border: 1px solid #a5f3fc; border-radius: 999px; padding: 0.08rem 0.45rem; font-size: 0.76rem; }
.summary { max-width: 360px; }
.empty { text-align: center; color: #6b7280; }
.error { color: #b91c1c; margin-bottom: 0.6rem; }
.pager { display: flex; justify-content: space-between; align-items: center; margin-top: 0.7rem; }
.pager button:disabled { background: #cbd5e1; cursor: not-allowed; }
@media (max-width: 1300px) {
  .filters { grid-template-columns: repeat(3, minmax(0, 1fr)); }
}
</style>
