<template>
  <main class="page">
    <div class="page-head">
      <div>
        <router-link to="/staff" class="back-link">← Staff List</router-link>
        <h2 class="page-title">{{ isEdit ? 'Edit Staff Member' : 'Add New Staff' }}</h2>
      </div>
    </div>

    <div v-if="loadError" class="error-msg">{{ loadError }}</div>

    <form @submit.prevent="submit" class="form-card" v-if="!loadError">
      <section class="form-section">
        <h3 class="section-title">Login Credentials</h3>
        <div class="form-grid">
          <div class="field">
            <label for="f-name">Full Name *</label>
            <input id="f-name" v-model="form.name" required />
          </div>
          <div class="field">
            <label for="f-email">Email / Username *</label>
            <input id="f-email" type="email" v-model="form.email" required />
          </div>
          <div class="field" v-if="!isEdit">
            <label for="f-pass">Initial Password *</label>
            <input id="f-pass" type="password" v-model="form.password" required />
          </div>
          <div class="field">
            <label for="f-role">Role *</label>
            <select id="f-role" v-model="form.role" required>
              <option value="teacher">Teacher</option>
              <option value="subject_head">Subject Head</option>
              <option value="mentor">Mentor</option>
              <option value="hm">HM</option>
              <option value="principal">Principal</option>
              <option value="admin">Admin</option>
              <option value="accounts">Accounts</option>
            </select>
          </div>
          <div class="field" v-if="isEdit">
            <label for="f-active">Account Status</label>
            <select id="f-active" v-model="form.is_active">
              <option :value="true">Active</option>
              <option :value="false">Inactive</option>
            </select>
          </div>
        </div>
      </section>

      <section class="form-section">
        <h3 class="section-title">Staff Profile</h3>
        <div class="form-grid">
          <div class="field">
            <label for="f-code">Staff Code</label>
            <input id="f-code" v-model="form.staff_code" placeholder="e.g. DVM-T-001" />
          </div>
          <div class="field">
            <label for="f-phone">Phone Number (for AI/Auth)</label>
            <input id="f-phone" v-model="form.phone" placeholder="10-digit number" />
          </div>
          <div class="field">
            <label for="f-dept">Department</label>
            <select id="f-dept" v-model="form.department_id">
              <option :value="null">Select Department</option>
              <option v-for="d in departments" :key="d.id" :value="d.id">{{ d.name }}</option>
            </select>
          </div>
          <div class="field">
            <label for="f-desig">Designation</label>
            <input id="f-desig" v-model="form.designation" placeholder="e.g. Senior Teacher" />
          </div>
          <div class="field">
            <label for="f-gender">Gender</label>
            <select id="f-gender" v-model="form.gender">
              <option value="">Select</option>
              <option>Male</option>
              <option>Female</option>
              <option>Other</option>
            </select>
          </div>
          <div class="field">
            <label for="f-dob">Date of Birth</label>
            <input id="f-dob" type="date" v-model="form.date_of_birth" />
          </div>
          <div class="field field--full">
            <label for="f-address">Address</label>
            <textarea id="f-address" v-model="form.address" rows="2" />
          </div>
        </div>
      </section>

      <div v-if="error" class="error-msg">{{ error }}</div>
      <div v-if="success" class="success-msg">{{ success }}</div>

      <div class="form-actions">
        <router-link to="/staff" class="btn btn--ghost">Cancel</router-link>
        <button type="submit" class="btn btn--primary" :disabled="submitting">
          {{ submitting ? 'Saving…' : (isEdit ? 'Update Staff' : 'Create Staff') }}
        </button>
      </div>
    </form>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '../api'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const loadError = ref('')
const error = ref('')
const success = ref('')
const submitting = ref(false)
const departments = ref([])

const form = ref({
  name: '', email: '', password: '', role: 'teacher', is_active: true,
  staff_code: '', phone: '', department_id: null, designation: '',
  gender: '', date_of_birth: '', address: '',
})

onMounted(async () => {
  try {
    const { data: depts } = await api.get('/api/portal/departments')
    departments.value = depts

    if (isEdit.value) {
      const { data } = await api.get(`/api/portal/staff/${route.params.id}`)
      form.value = {
        name: data.name,
        email: data.email,
        role: data.role,
        is_active: data.is_active,
        staff_code: data.profile?.staff_code || '',
        phone: data.profile?.phone || '',
        department_id: data.profile?.department_id || null,
        designation: data.profile?.designation || '',
        gender: data.profile?.gender || '',
        date_of_birth: data.profile?.date_of_birth || '',
        address: data.profile?.address || '',
      }
    }
  } catch (e) {
    loadError.value = e.response?.data?.detail || 'Failed to load data'
  }
})

const submit = async () => {
  submitting.value = true; error.value = ''; success.value = ''
  try {
    const payload = { ...form.value }
    
    // Clean up payload: remove empty strings for dates/integers to avoid validation errors
    if (!payload.date_of_birth) delete payload.date_of_birth
    if (!payload.department_id) payload.department_id = null
    
    // Explicitly delete legacy field if it exists
    delete payload.department
    
    if (isEdit.value) {
      delete payload.password
      await api.put(`/api/portal/staff/${route.params.id}`, payload)
      success.value = 'Staff updated successfully!'
      setTimeout(() => router.push('/staff'), 1000)
    } else {
      await api.post('/api/portal/staff', payload)
      success.value = 'Staff created successfully!'
      setTimeout(() => router.push('/staff'), 1000)
    }
  } catch (e) {
    error.value = e.response?.data?.detail || 'Save failed. Please check the form.'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.page { padding: 1.5rem 2rem; max-width: 800px; margin: 0 auto; }
.page-head { margin-bottom: 1.25rem; }
.back-link { color: #64748b; text-decoration: none; font-size: 0.82rem; font-weight: 600; display: block; margin-bottom: 0.3rem; }
.page-title { font-size: 1.5rem; font-weight: 800; color: #0f172a; margin: 0; }

.form-card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 2rem; }
.form-section { margin-bottom: 2rem; }
.form-section:last-of-type { margin-bottom: 1rem; }
.section-title { font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin: 0 0 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #f1f5f9; }

.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.9rem; }
.field { display: flex; flex-direction: column; gap: 0.3rem; }
.field--full { grid-column: 1 / -1; }
label { font-size: 0.82rem; font-weight: 600; color: #374151; }
input, select, textarea {
  padding: 0.45rem 0.7rem; border: 1px solid #d1d5db; border-radius: 6px;
  font-size: 0.88rem; color: #1f2937; background: #fff; width: 100%; box-sizing: border-box;
}
input:focus, select:focus, textarea:focus { outline: none; border-color: #0ea5e9; box-shadow: 0 0 0 2px #e0f2fe; }

.form-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid #f1f5f9; }
.btn { padding: 0.5rem 1.25rem; border-radius: 6px; border: none; font-size: 0.88rem; font-weight: 600; cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; }
.btn--primary { background: #0f172a; color: #fff; }
.btn--primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn--ghost { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }

.error-msg { background: #fef2f2; color: #dc2626; padding: 0.6rem 1rem; border-radius: 6px; margin-bottom: 1rem; font-size: 0.88rem; }
.success-msg { background: #f0fdf4; color: #16a34a; padding: 0.6rem 1rem; border-radius: 6px; margin-bottom: 1rem; font-size: 0.88rem; }
</style>
