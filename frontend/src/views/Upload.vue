<template>
  <div class="page">
    <!-- Nav Bar -->
    <nav class="navbar">
      <button class="back-btn" @click="router.push('/portal')">&#8592; Back to Portal</button>
      <span class="nav-title">Teacher Portal</span>
    </nav>

    <div class="content">
      <h1 class="page-heading">Upload Lesson Plan <span class="accent">(xlsx)</span></h1>

      <div class="card">
        <!-- Class + Subject -->
        <div class="field-row">
          <div class="field">
            <label>Class</label>
            <select v-model="selectedClassId" @change="onClassChange">
              <option value="">Select class</option>
              <option v-for="c in classes" :key="c.id" :value="c.id">{{ c.name }}</option>
            </select>
          </div>
          <div class="field">
            <label>Subject *</label>
            <select v-model="selectedSubjectId" :disabled="!selectedClassId">
              <option value="">Select subject</option>
              <option v-for="s in subjects" :key="s.id" :value="s.id">{{ s.name }}</option>
            </select>
          </div>
        </div>

        <!-- File Input -->
        <div class="field">
          <label>xlsx File *</label>
          <div
            class="drop-zone"
            :class="{ 'drop-zone--active': dragOver, 'drop-zone--has-file': selectedFile }"
            @dragover.prevent="dragOver = true"
            @dragleave.prevent="dragOver = false"
            @drop.prevent="onDrop"
            @click="fileInput.click()"
          >
            <input
              ref="fileInput"
              type="file"
              accept=".xlsx"
              style="display:none"
              @change="onFileChange"
            />
            <template v-if="selectedFile">
              <span class="file-icon">&#128196;</span>
              <span class="file-name">{{ selectedFile.name }}</span>
              <span class="file-size">{{ formatSize(selectedFile.size) }}</span>
            </template>
            <template v-else>
              <span class="drop-icon">&#8682;</span>
              <span class="drop-text">Click to browse or drag &amp; drop an .xlsx file</span>
            </template>
          </div>
        </div>

        <!-- Error -->
        <div v-if="uploadError" class="error-banner">{{ uploadError }}</div>

        <!-- Upload Button -->
        <div class="form-actions">
          <button
            class="upload-btn"
            :disabled="!selectedFile || !selectedSubjectId || uploading"
            @click="doUpload"
          >
            <span v-if="uploading" class="spinner-sm"></span>
            {{ uploading ? `Uploading… ${uploadProgress}%` : 'Upload' }}
          </button>
        </div>

        <!-- Progress Bar -->
        <div v-if="uploading" class="progress-bar-wrap">
          <div class="progress-bar" :style="{ width: uploadProgress + '%' }"></div>
        </div>
      </div>

      <!-- Success Result -->
      <div v-if="result" class="result-card">
        <div class="result-icon">&#10003;</div>
        <h2 class="result-heading">Upload Successful</h2>
        <div class="result-details">
          <div class="result-row">
            <span class="result-label">Chapter</span>
            <span class="result-value">{{ result.title }}</span>
          </div>
          <div class="result-row">
            <span class="result-label">Concepts</span>
            <span class="result-value result-badge">{{ result.concepts_count ?? result.concept_count ?? '—' }}</span>
          </div>
          <div class="result-row">
            <span class="result-label">Exhibits</span>
            <span class="result-value result-badge">{{ result.exhibits_count ?? result.exhibit_count ?? '—' }}</span>
          </div>
        </div>
        <div class="result-actions">
          <button class="btn-portal" @click="router.push('/portal')">Go to Portal</button>
          <button class="btn-another" @click="resetForm">Upload Another</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api.js'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const classes = ref([])
const subjects = ref([])
const selectedClassId = ref('')
const selectedSubjectId = ref('')

const fileInput = ref(null)
const selectedFile = ref(null)
const dragOver = ref(false)

const uploading = ref(false)
const uploadProgress = ref(0)
const uploadError = ref('')
const result = ref(null)

onMounted(async () => {
  await loadClasses()
  // Pre-select subject from query param if present
  const qSubject = route.query.subject_id
  if (qSubject) {
    await preselectSubject(parseInt(qSubject))
  }
})

async function loadClasses() {
  try {
    const res = await api.get('/api/public/classes')
    classes.value = res.data
  } catch (_) {}
}

async function preselectSubject(subjectId) {
  // Load each class's subjects to find which class owns this subject
  for (const cls of classes.value) {
    try {
      const res = await api.get(`/api/public/classes/${cls.id}/subjects`)
      const found = res.data.find(s => s.id === subjectId)
      if (found) {
        selectedClassId.value = cls.id
        subjects.value = res.data
        selectedSubjectId.value = subjectId
        break
      }
    } catch (_) {}
  }
}

async function onClassChange() {
  selectedSubjectId.value = ''
  subjects.value = []
  if (selectedClassId.value) {
    try {
      const res = await api.get(`/api/public/classes/${selectedClassId.value}/subjects`)
      subjects.value = res.data
    } catch (_) {}
  }
}

function onFileChange(e) {
  const f = e.target.files[0]
  if (f) selectedFile.value = f
}

function onDrop(e) {
  dragOver.value = false
  const f = e.dataTransfer.files[0]
  if (f && f.name.endsWith('.xlsx')) {
    selectedFile.value = f
  } else {
    uploadError.value = 'Please drop a valid .xlsx file.'
  }
}

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

async function doUpload() {
  if (!selectedFile.value || !selectedSubjectId.value) return
  uploadError.value = ''
  uploading.value = true
  uploadProgress.value = 0
  result.value = null

  const formData = new FormData()
  formData.append('file', selectedFile.value)
  formData.append('subject_id', selectedSubjectId.value)

  try {
    const res = await api.post('/api/portal/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress(e) {
        if (e.total) {
          uploadProgress.value = Math.round((e.loaded / e.total) * 100)
        }
      },
    })
    result.value = res.data
  } catch (e) {
    uploadError.value = e.response?.data?.detail || 'Upload failed. Please try again.'
  } finally {
    uploading.value = false
  }
}

function resetForm() {
  selectedFile.value = null
  uploadError.value = ''
  uploadProgress.value = 0
  result.value = null
  if (fileInput.value) fileInput.value.value = ''
}
</script>

<style scoped>
.page {
  min-height: 100vh;
  background: #f1f5f9;
  font-family: system-ui, -apple-system, sans-serif;
  padding-bottom: 3rem;
}

/* Navbar */
.navbar {
  background: #1e293b;
  color: white;
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0 1.5rem;
  height: 56px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.back-btn {
  background: rgba(255,255,255,0.12);
  border: 1px solid rgba(255,255,255,0.25);
  color: white;
  padding: 0.4rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.88rem;
  transition: background 0.15s;
}

.back-btn:hover {
  background: rgba(255,255,255,0.22);
}

.nav-title {
  font-size: 1rem;
  font-weight: 600;
  opacity: 0.8;
}

/* Content */
.content {
  max-width: 680px;
  margin: 0 auto;
  padding: 1.5rem 1rem;
}

.page-heading {
  font-size: 1.5rem;
  font-weight: 800;
  color: #1e293b;
  margin: 0 0 1.2rem;
}

.accent {
  color: #0ea5e9;
  font-weight: 600;
}

/* Card */
.card {
  background: white;
  border-radius: 12px;
  padding: 1.6rem 1.8rem;
  box-shadow: 0 1px 6px rgba(0,0,0,0.07);
}

/* Fields */
.field-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.field {
  margin-bottom: 1.1rem;
}

.field label {
  display: block;
  font-size: 0.83rem;
  font-weight: 600;
  color: #374151;
  margin-bottom: 0.4rem;
}

.field select {
  width: 100%;
  padding: 0.62rem 0.9rem;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.93rem;
  color: #111827;
  background: white;
  outline: none;
  transition: border-color 0.15s;
  box-sizing: border-box;
  cursor: pointer;
}

.field select:focus {
  border-color: #4f46e5;
}

.field select:disabled {
  background: #f9fafb;
  color: #9ca3af;
  cursor: not-allowed;
}

/* Drop Zone */
.drop-zone {
  border: 2px dashed #cbd5e1;
  border-radius: 10px;
  padding: 2rem 1.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.18s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  background: #f8fafc;
}

.drop-zone:hover,
.drop-zone--active {
  border-color: #4f46e5;
  background: #eef2ff;
}

.drop-zone--has-file {
  border-color: #0ea5e9;
  background: #f0f9ff;
}

.drop-icon {
  font-size: 2rem;
  color: #94a3b8;
}

.drop-text {
  font-size: 0.9rem;
  color: #64748b;
}

.file-icon {
  font-size: 2rem;
}

.file-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: #0369a1;
}

.file-size {
  font-size: 0.8rem;
  color: #64748b;
}

/* Error */
.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #dc2626;
  border-radius: 7px;
  padding: 0.6rem 0.9rem;
  font-size: 0.88rem;
  margin-bottom: 1rem;
}

/* Actions */
.form-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 0.5rem;
}

.upload-btn {
  padding: 0.65rem 1.8rem;
  background: #0ea5e9;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.97rem;
  font-weight: 600;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  transition: background 0.15s;
}

.upload-btn:hover:not(:disabled) {
  background: #0284c7;
}

.upload-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.spinner-sm {
  width: 15px;
  height: 15px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Progress Bar */
.progress-bar-wrap {
  height: 4px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  margin-top: 0.75rem;
}

.progress-bar {
  height: 100%;
  background: linear-gradient(90deg, #0ea5e9, #4f46e5);
  border-radius: 4px;
  transition: width 0.2s ease;
}

/* Result Card */
.result-card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 1px 6px rgba(0,0,0,0.07);
  margin-top: 1.2rem;
  text-align: center;
}

.result-icon {
  width: 52px;
  height: 52px;
  background: #dcfce7;
  color: #16a34a;
  border-radius: 50%;
  font-size: 1.5rem;
  font-weight: 800;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.result-heading {
  font-size: 1.2rem;
  font-weight: 700;
  color: #15803d;
  margin: 0 0 1.2rem;
}

.result-details {
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 1rem 1.2rem;
  margin-bottom: 1.4rem;
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}

.result-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.result-label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.07em;
}

.result-value {
  font-size: 0.95rem;
  font-weight: 600;
  color: #1e293b;
}

.result-badge {
  background: #e0e7ff;
  color: #4f46e5;
  padding: 0.2rem 0.65rem;
  border-radius: 20px;
  font-size: 0.88rem;
}

.result-actions {
  display: flex;
  gap: 0.75rem;
  justify-content: center;
}

.btn-portal {
  padding: 0.55rem 1.3rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 0.93rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s;
}

.btn-portal:hover {
  background: #4338ca;
}

.btn-another {
  padding: 0.55rem 1.3rem;
  background: white;
  color: #374151;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.93rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.15s;
}

.btn-another:hover {
  background: #f9fafb;
}

@media (max-width: 500px) {
  .field-row { grid-template-columns: 1fr; }
}
</style>
