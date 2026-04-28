<template>
  <main class="page">
    <div class="head">
      <h2>Students</h2>
      <button @click="load">Refresh</button>
    </div>

    <div class="filters">
      <input v-model="q" placeholder="Search admission no / name" @keyup.enter="load" />
      <button @click="load">Search</button>
    </div>

    <div v-if="error" class="error">{{ error }}</div>
    <table class="table">
      <thead>
        <tr>
          <th>Admission</th>
          <th>Name</th>
          <th>Class</th>
          <th>Section</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="s in students" :key="s.id">
          <td>{{ s.admission_no }}</td>
          <td>{{ s.first_name }} {{ s.last_name }}</td>
          <td>{{ s.class_name }}</td>
          <td>{{ s.section_name }}</td>
          <td>{{ s.status }}</td>
        </tr>
      </tbody>
    </table>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import api from '../api'

const students = ref([])
const q = ref('')
const error = ref('')

const load = async () => {
  error.value = ''
  try {
    const params = new URLSearchParams({ limit: '100', offset: '0' })
    if (q.value.trim()) params.append('q', q.value.trim())
    const { data } = await api.get(`/api/portal/erp/students?${params.toString()}`)
    students.value = data.items || []
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load students'
  }
}

onMounted(load)
</script>

<style scoped>
.page { padding: 1rem; }
.head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem; }
.filters { display: flex; gap: 0.5rem; margin-bottom: 0.8rem; }
input, button { padding: 0.5rem 0.7rem; border: 1px solid #d1d5db; border-radius: 6px; }
button { background: #0ea5e9; color: white; border: 0; cursor: pointer; }
.table { width: 100%; border-collapse: collapse; background: #fff; }
.table th, .table td { border-bottom: 1px solid #e5e7eb; padding: 0.5rem; text-align: left; font-size: 0.92rem; }
.error { color: #b91c1c; margin-bottom: 0.6rem; }
</style>
