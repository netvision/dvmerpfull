<template>
  <main class="page">
    <div class="head"><h2>Fee Invoices</h2><button @click="load">Refresh</button></div>
    <div v-if="error" class="error">{{ error }}</div>
    <table class="table">
      <thead><tr><th>Invoice</th><th>Student</th><th>Total</th><th>Paid</th><th>Balance</th><th>Status</th></tr></thead>
      <tbody>
        <tr v-for="inv in invoices" :key="inv.id">
          <td>{{ inv.invoice_no }}</td>
          <td>{{ inv.student_name }}</td>
          <td>{{ inv.total_amount }}</td>
          <td>{{ inv.paid_amount }}</td>
          <td>{{ inv.balance_amount }}</td>
          <td>{{ inv.status }}</td>
        </tr>
      </tbody>
    </table>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import api from '../api'

const invoices = ref([])
const error = ref('')

const load = async () => {
  error.value = ''
  try {
    const { data } = await api.get('/api/portal/erp/fee-invoices')
    invoices.value = data
  } catch (e) {
    error.value = e.response?.data?.detail || 'Failed to load fee invoices'
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
