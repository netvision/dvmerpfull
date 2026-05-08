<template>
  <div v-if="loading" class="center-msg">Loading…</div>
  <div v-else-if="!student" class="center-msg error">Student not found.</div>

  <main v-else class="detail-page">
    <!-- Sticky Header -->
    <div class="sticky-header">
      <router-link to="/students" class="back-link">← Students</router-link>
      <div class="sticky-identity">
        <div class="avatar-lg">{{ initials }}</div>
        <div>
          <div class="sticky-name">{{ student.first_name }} {{ student.last_name }}</div>
          <div class="sticky-meta">{{ student.admission_no }} · {{ student.class_name }} {{ student.section_name }}</div>
        </div>
      </div>
      <div class="sticky-actions">
        <StatusBadge :status="student.status" />
        <router-link :to="`/students/${student.id}/edit`" class="btn btn--edit">Edit</router-link>
      </div>
    </div>

    <!-- Tab Bar -->
    <div class="tab-bar">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        :id="`tab-${tab.id}`"
        :class="['tab-btn', { 'tab-btn--active': activeTab === tab.id }]"
        @click="activeTab = tab.id"
      >{{ tab.label }}</button>
    </div>

    <div class="tab-content">
      <!-- Personal -->
      <div v-if="activeTab === 'personal'">
        <InfoCard title="Personal Details" :rows="personalRows" />
        <InfoCard title="Contact & Address" :rows="contactRows" />
      </div>

      <!-- Academic -->
      <div v-if="activeTab === 'academic'">
        <InfoCard title="Academic Information" :rows="academicRows" />
      </div>

      <!-- Guardians -->
      <div v-if="activeTab === 'guardians'">
        <div v-if="student.guardians && student.guardians.length" class="guardians-grid">
          <div v-for="g in student.guardians" :key="g.id" class="guardian-card">
            <div class="guardian-card__head">
              <span class="guardian-relation">{{ g.relation || 'Guardian' }}</span>
              <span v-if="g.is_primary" class="primary-badge">Primary</span>
            </div>
            <p class="guardian-name">{{ g.name }}</p>
            <div class="guardian-details">
              <span v-if="g.phone">📞 {{ g.phone }}</span>
              <span v-if="g.email">✉ {{ g.email }}</span>
            </div>
          </div>
        </div>
        <div v-else class="empty-tab">No guardian information available.</div>
      </div>

      <!-- Extended Profile -->
      <div v-if="activeTab === 'profile'">
        <div v-if="student.profile">
          <InfoCard title="Health & Physical" :rows="healthRows" />
          <InfoCard title="Transport" :rows="transportRows" />
          <InfoCard title="Bank & Identity" :rows="bankRows" />
        </div>
        <div v-else class="empty-tab">No extended profile data available.</div>
      </div>

      <!-- Attendance Summary -->
      <div v-if="activeTab === 'attendance'">
        <div v-if="attendance" class="stats-grid">
          <div class="stat-card">
            <div class="stat-value">{{ attendance.present }}</div>
            <div class="stat-label">Present</div>
          </div>
          <div class="stat-card">
            <div class="stat-value text-red">{{ attendance.absent }}</div>
            <div class="stat-label">Absent</div>
          </div>
          <div class="stat-card">
            <div class="stat-value text-orange">{{ attendance.late }}</div>
            <div class="stat-label">Late</div>
          </div>
          <div class="stat-card">
            <div class="stat-value">{{ attendance.total_entries }}</div>
            <div class="stat-label">Total Days</div>
          </div>
          <div class="stat-card">
            <div class="stat-value text-green">{{ attendancePct }}%</div>
            <div class="stat-label">Attendance %</div>
          </div>
        </div>
        <div v-else class="empty-tab">No attendance data found.</div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'
import StatusBadge from '../components/StatusBadge.vue'
import InfoCard from '../components/InfoCard.vue'

const route = useRoute()
const student = ref(null)
const attendance = ref(null)
const loading = ref(true)
const activeTab = ref('personal')

const tabs = [
  { id: 'personal', label: 'Personal' },
  { id: 'academic', label: 'Academic' },
  { id: 'guardians', label: 'Guardians' },
  { id: 'profile', label: 'Extended Profile' },
  { id: 'attendance', label: 'Attendance' },
]

const fmt = (v) => v || '—'
const fmtDate = (d) => d ? new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' }) : '—'
const fmtBool = (b) => b == null ? '—' : (b ? 'Yes' : 'No')

const initials = computed(() => {
  const s = student.value
  return `${s?.first_name?.[0] || ''}${s?.last_name?.[0] || ''}`.toUpperCase()
})

const personalRows = computed(() => {
  const s = student.value
  return [
    { label: 'Full Name', value: `${s.first_name} ${s.last_name || ''}`.trim() },
    { label: 'Date of Birth', value: fmtDate(s.date_of_birth) },
    { label: 'Gender', value: fmt(s.gender) },
    { label: 'Blood Group', value: fmt(s.profile?.blood_group) },
    { label: 'Category', value: fmt(s.profile?.category) },
    { label: 'Religion', value: fmt(s.profile?.religion) },
    { label: 'Nationality', value: fmt(s.profile?.nationality) },
    { label: 'Mother Tongue', value: fmt(s.profile?.mother_tongue) },
  ]
})

const contactRows = computed(() => {
  const s = student.value
  return [
    { label: 'Phone', value: fmt(s.phone) },
    { label: 'Email', value: fmt(s.email) },
    { label: 'Address', value: fmt(s.address) },
  ]
})

const academicRows = computed(() => {
  const s = student.value
  return [
    { label: 'Admission No.', value: fmt(s.admission_no) },
    { label: 'Roll No.', value: fmt(s.roll_no) },
    { label: 'Class', value: fmt(s.class_name) },
    { label: 'Section', value: fmt(s.section_name) },
    { label: 'Academic Year', value: fmt(s.academic_year_name) },
    { label: 'Previous School', value: fmt(s.profile?.previous_school) },
    { label: 'Status', value: fmt(s.status) },
  ]
})

const healthRows = computed(() => {
  const p = student.value?.profile
  return [
    { label: 'Height (cm)', value: fmt(p?.height) },
    { label: 'Weight (kg)', value: fmt(p?.weight) },
    { label: 'Vision', value: fmt(p?.vision) },
  ]
})

const transportRows = computed(() => {
  const p = student.value?.profile
  return [
    { label: 'Uses Transport', value: fmtBool(p?.is_transport) },
    { label: 'Pickup Route', value: fmt(p?.pickup_route) },
    { label: 'Drop Route', value: fmt(p?.drop_route) },
  ]
})

const bankRows = computed(() => {
  const p = student.value?.profile
  return [
    { label: 'Aadhaar No.', value: fmt(p?.aadhaar_no) },
    { label: 'PEN No.', value: fmt(p?.pen_no) },
    { label: 'APAAR ID', value: fmt(p?.apaar_id) },
    { label: 'Bank Name', value: fmt(p?.bank_name) },
    { label: 'Account No.', value: fmt(p?.account_no) },
    { label: 'IFSC Code', value: fmt(p?.ifsc_code) },
  ]
})

const attendancePct = computed(() => {
  const a = attendance.value
  if (!a || !a.total_entries) return 0
  return Math.round((a.present / a.total_entries) * 100)
})

onMounted(async () => {
  const id = route.params.id
  try {
    const { data } = await api.get(`/api/portal/erp/students/${id}`)
    student.value = data
    // Try load attendance summary for this student
    try {
      const res = await api.get(`/api/portal/erp/attendance-report?student_id=${id}`)
      attendance.value = res.data
    } catch (_) {}
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.detail-page { background: #f8fafc; min-height: calc(100vh - 58px); }

/* Sticky Header */
.sticky-header {
  position: sticky; top: 58px; z-index: 10;
  background: #fff; border-bottom: 1px solid #e5e7eb;
  display: flex; align-items: center; gap: 1.5rem;
  padding: 0.75rem 2rem;
}
.back-link { color: #64748b; text-decoration: none; font-size: 0.85rem; font-weight: 600; white-space: nowrap; }
.back-link:hover { color: #0f172a; }
.sticky-identity { display: flex; align-items: center; gap: 0.75rem; flex: 1; }
.avatar-lg {
  width: 42px; height: 42px; border-radius: 50%; flex-shrink: 0;
  background: #e0e7ff; color: #4f46e5; font-size: 1rem; font-weight: 800;
  display: flex; align-items: center; justify-content: center;
}
.sticky-name { font-size: 1rem; font-weight: 700; color: #0f172a; }
.sticky-meta { font-size: 0.8rem; color: #64748b; }
.sticky-actions { display: flex; align-items: center; gap: 0.75rem; }

.btn--edit { padding: 0.35rem 0.9rem; background: #0f172a; color: #fff; border-radius: 6px; text-decoration: none; font-size: 0.82rem; font-weight: 600; }
.btn--edit:hover { background: #1e293b; }

/* Tabs */
.tab-bar {
  display: flex; gap: 0; padding: 0 2rem;
  background: #fff; border-bottom: 1px solid #e5e7eb;
  overflow-x: auto;
}
.tab-btn {
  padding: 0.75rem 1.25rem; border: none; background: transparent;
  font-size: 0.88rem; font-weight: 600; color: #64748b;
  cursor: pointer; border-bottom: 2px solid transparent;
  white-space: nowrap;
}
.tab-btn--active { color: #0ea5e9; border-bottom-color: #0ea5e9; }
.tab-btn:hover:not(.tab-btn--active) { color: #1e293b; }

.tab-content { padding: 1.5rem 2rem; max-width: 960px; }

/* Guardians */
.guardians-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1rem; }
.guardian-card {
  background: #fff; border: 1px solid #e5e7eb; border-radius: 10px;
  padding: 1.25rem 1.5rem;
}
.guardian-card__head { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.5rem; }
.guardian-relation { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; }
.primary-badge { background: #dcfce7; color: #16a34a; font-size: 0.7rem; padding: 2px 8px; border-radius: 999px; font-weight: 700; }
.guardian-name { font-size: 1rem; font-weight: 700; color: #0f172a; margin: 0 0 0.6rem; }
.guardian-details { display: flex; flex-direction: column; gap: 0.25rem; font-size: 0.84rem; color: #475569; }

/* Attendance Stats */
.stats-grid { display: flex; flex-wrap: wrap; gap: 1rem; }
.stat-card {
  background: #fff; border: 1px solid #e5e7eb; border-radius: 10px;
  padding: 1.25rem 2rem; text-align: center; min-width: 120px;
}
.stat-value { font-size: 2rem; font-weight: 800; color: #0f172a; }
.stat-label { font-size: 0.78rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; margin-top: 0.2rem; }
.text-red { color: #dc2626; }
.text-orange { color: #ea580c; }
.text-green { color: #16a34a; }

.empty-tab { padding: 3rem; text-align: center; color: #94a3b8; font-size: 0.9rem; }
.center-msg { display: flex; justify-content: center; align-items: center; height: calc(100vh - 120px); font-size: 1rem; color: #64748b; }
.center-msg.error { color: #dc2626; }
</style>
