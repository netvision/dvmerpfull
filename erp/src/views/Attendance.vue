<template>
  <main class="page">
    <div class="head"><h2>Attendance Sessions</h2><button @click="load">Refresh</button></div>
    <div v-if="error" class="error">{{ error }}</div>
    <table class="table">
      <thead><tr><th>Date</th><th>Class</th><th>Section</th><th>Entries</th></tr></thead>
      <tbody>
        <tr v-for="s in sessions" :key="s.id">
          <td>{{ s.attendance_date }}</td>
          <td>{{ s.class_name }}</td>
          <td>{{ s.section_name }}</td>
          <td>{{ s.entries_count }}</td>
        </tr>
      </tbody>
    </table>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import api from '../api'

const sessions = ref([])
const error = ref('')

const load = async () => {
  error.value = ''
  try {
    const { data } = await api.get('/api/portal/erp/attendance-sessions?limit=200&offset=0')
    sessions.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load attendance sessions'
  }
}

onMounted(load)
</script>

<style scoped>
.page { padding: 1rem; }
.head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }
button { padding: 0.5rem 0.7rem; background: #0ea5e9; color: #fff; border: 0; border-radius: 6px; cursor: pointer; }
.table { width: 100%; border-collapse: collapse; background: #fff; }
.table th, .table td { border-bottom: 1px solid #e5e7eb; padding: 0.5rem; text-align: left; font-size: 0.92rem; }
.error { color: #b91c1c; margin-bottom: 0.6rem; }
</style>
