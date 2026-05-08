<template>
  <main class="page">
    <div class="page-head">
      <div>
        <router-link to="/students" class="back-link">← Students</router-link>
        <h2 class="page-title">{{ isEdit ? 'Edit Student' : 'Add New Student' }}</h2>
      </div>
    </div>

    <div v-if="loadError" class="error-msg">{{ loadError }}</div>

    <form @submit.prevent="submit" class="form-card" v-if="!loadError">
      <section class="form-section">
        <h3 class="section-title">Personal Information</h3>
        <div class="form-grid">
          <div class="field">
            <label for="f-fname">First Name *</label>
            <input id="f-fname" v-model="form.first_name" required />
          </div>
          <div class="field">
            <label for="f-lname">Last Name</label>
            <input id="f-lname" v-model="form.last_name" />
          </div>
          <div class="field">
            <label for="f-dob">Date of Birth</label>
            <input id="f-dob" type="date" v-model="form.date_of_birth" />
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
            <label for="f-phone">Phone</label>
            <input id="f-phone" v-model="form.phone" />
          </div>
          <div class="field">
            <label for="f-email">Email</label>
            <input id="f-email" type="email" v-model="form.email" />
          </div>
          <div class="field field--full">
            <label for="f-address">Address</label>
            <textarea id="f-address" v-model="form.address" rows="2" />
          </div>
        </div>
      </section>

      <section class="form-section">
        <h3 class="section-title">Academic Information</h3>
        <div class="form-grid">
          <div class="field">
            <label for="f-admno">Admission Number *</label>
            <input id="f-admno" v-model="form.admission_no" required />
          </div>
          <div class="field">
            <label for="f-rollno">Roll Number</label>
            <input id="f-rollno" v-model="form.roll_no" />
          </div>
          <div class="field">
            <label for="f-class">Class *</label>
            <select id="f-class" v-model="form.class_id" @change="form.section_id = null" required>
              <option :value="null">Select Class</option>
              <option v-for="c in classes" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>
          <div class="field">
            <label for="f-section">Section</label>
            <select id="f-section" v-model="form.section_id" :disabled="!form.class_id">
              <option :value="null">No Section</option>
              <option v-for="s in filteredSections" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
          <div class="field">
            <label for="f-year">Academic Year *</label>
            <select id="f-year" v-model="form.academic_year_id" required>
              <option :value="null">Select Year</option>
              <option v-for="y in years" :key="y.id" :value="y.id">{{ y.name }}</option>
            </select>
          </div>
          <div class="field">
            <label for="f-status">Status</label>
            <select id="f-status" v-model="form.status">
              <option value="active">Active</option>
              <option value="promoted">Promoted</option>
              <option value="left">Left</option>
              <option value="detained">Detained</option>
            </select>
          </div>
        </div>
      </section>

      <div v-if="error" class="error-msg">{{ error }}</div>
      <div v-if="success" class="success-msg">{{ success }}</div>

      <div class="form-actions">
        <router-link to="/students" class="btn btn--ghost">Cancel</router-link>
        <button type="submit" class="btn btn--primary" :disabled="submitting">
          {{ submitting ? 'Saving…' : (isEdit ? 'Update Student' : 'Create Student') }}
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
const classes = ref([])
const sections = ref([])
const years = ref([])
const loadError = ref('')
const error = ref('')
const success = ref('')
const submitting = ref(false)

const form = ref({
  first_name: '', last_name: '', date_of_birth: '', gender: '',
  phone: '', email: '', address: '',
  admission_no: '', roll_no: '', class_id: null, section_id: null,
  academic_year_id: null, status: 'active',
})

const filteredSections = computed(() =>
  form.value.class_id ? sections.value.filter(s => s.class_id === form.value.class_id) : []
)

onMounted(async () => {
  try {
    const [cls, sec, yrs] = await Promise.all([
      api.get('/api/portal/erp/lookups/classes'),
      api.get('/api/portal/erp/lookups/sections'),
      api.get('/api/portal/erp/lookups/academic-years'),
    ])
    classes.value = cls.data
    sections.value = sec.data
    years.value = yrs.data

    if (isEdit.value) {
      const { data } = await api.get(`/api/portal/erp/students/${route.params.id}`)
      form.value = {
        first_name: data.first_name, last_name: data.last_name || '',
        date_of_birth: data.date_of_birth || '', gender: data.gender || '',
        phone: data.phone || '', email: data.email || '', address: data.address || '',
        admission_no: data.admission_no, roll_no: data.roll_no || '',
        class_id: data.class_id, section_id: data.section_id || null,
        academic_year_id: data.academic_year_id, status: data.status,
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
    if (!payload.date_of_birth) delete payload.date_of_birth
    if (isEdit.value) {
      await api.put(`/api/portal/erp/students/${route.params.id}`, payload)
      success.value = 'Student updated successfully!'
      setTimeout(() => router.push(`/students/${route.params.id}`), 1000)
    } else {
      const { data } = await api.post('/api/portal/erp/students', payload)
      success.value = 'Student created successfully!'
      setTimeout(() => router.push(`/students/${data.id}`), 1000)
    }
  } catch (e) {
    error.value = e.response?.data?.detail || 'Save failed. Please check the form.'
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.page { padding: 1.5rem 2rem; max-width: 960px; margin: 0 auto; }
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
input:disabled, select:disabled { background: #f8fafc; color: #94a3b8; }

.form-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.5rem; padding-top: 1.25rem; border-top: 1px solid #f1f5f9; }
.btn { padding: 0.5rem 1.25rem; border-radius: 6px; border: none; font-size: 0.88rem; font-weight: 600; cursor: pointer; text-decoration: none; display: inline-flex; align-items: center; }
.btn--primary { background: #0f172a; color: #fff; }
.btn--primary:disabled { opacity: 0.5; cursor: not-allowed; }
.btn--ghost { background: #f1f5f9; color: #475569; border: 1px solid #e2e8f0; }
.error-msg { background: #fef2f2; color: #dc2626; padding: 0.6rem 1rem; border-radius: 6px; margin-bottom: 1rem; font-size: 0.88rem; }
.success-msg { background: #f0fdf4; color: #16a34a; padding: 0.6rem 1rem; border-radius: 6px; margin-bottom: 1rem; font-size: 0.88rem; }
</style>
