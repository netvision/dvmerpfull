<template>
  <PortalShell
    title="Utilities"
    subtitle="Backup and restore"
    @logout="logout"
    @change-password="router.push('/portal')"
  >
    <div class="utilities-grid">
      <section class="dvm-card utility-panel">
        <div class="panel-heading">
          <div>
            <p class="eyebrow">Export</p>
            <h2>Download backup</h2>
          </div>
          <span class="status-pill">ZIP</span>
        </div>
        <p class="panel-copy">
          Creates one archive containing the lesson-planning database data and every file in uploaded assets.
        </p>
        <button type="button" class="dvm-btn dvm-btn--primary" :disabled="downloading" @click="downloadBackup">
          {{ downloading ? 'Preparing...' : 'Download Backup' }}
        </button>
        <div v-if="downloadError" class="error-banner">{{ downloadError }}</div>
      </section>

      <section class="dvm-card utility-panel">
        <div class="panel-heading">
          <div>
            <p class="eyebrow">Import</p>
            <h2>Restore backup</h2>
          </div>
          <span class="status-pill danger">Destructive</span>
        </div>
        <p class="panel-copy">
          Restores database rows and uploaded assets from a previous backup archive. Current records and uploaded files are replaced.
        </p>

        <form class="restore-form" @submit.prevent="restoreBackup">
          <label class="field">
            <span>Backup archive</span>
            <input ref="fileInput" type="file" accept=".zip,application/zip" @change="onFileChange" />
          </label>

          <label class="field">
            <span>Confirmation</span>
            <input v-model="confirmText" type="text" autocomplete="off" placeholder="Type RESTORE" />
          </label>

          <button
            type="submit"
            class="dvm-btn dvm-btn--danger"
            :disabled="restoring || !restoreFile || confirmText !== 'RESTORE'"
          >
            {{ restoring ? 'Restoring...' : 'Restore Backup' }}
          </button>
        </form>

        <div v-if="restoreError" class="error-banner">{{ restoreError }}</div>
        <div v-if="restoreSuccess" class="success-banner">{{ restoreSuccess }}</div>
      </section>
    </div>
  </PortalShell>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import PortalShell from '../components/PortalShell.vue'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()

const downloading = ref(false)
const restoring = ref(false)
const downloadError = ref('')
const restoreError = ref('')
const restoreSuccess = ref('')
const restoreFile = ref(null)
const confirmText = ref('')
const fileInput = ref(null)

function logout() {
  auth.logout()
  router.push('/login')
}

function filenameFromDisposition(disposition) {
  const match = /filename="?([^"]+)"?/i.exec(disposition || '')
  return match?.[1] || 'dvm-lesson-portal-backup.zip'
}

async function downloadBackup() {
  downloading.value = true
  downloadError.value = ''

  try {
    const response = await api.get('/api/portal/utilities/backup', { responseType: 'blob' })
    const url = URL.createObjectURL(response.data)
    const link = document.createElement('a')
    link.href = url
    link.download = filenameFromDisposition(response.headers['content-disposition'])
    document.body.appendChild(link)
    link.click()
    link.remove()
    URL.revokeObjectURL(url)
  } catch (err) {
    downloadError.value = err.response?.data?.detail || 'Failed to download backup.'
  } finally {
    downloading.value = false
  }
}

function onFileChange(event) {
  restoreFile.value = event.target.files?.[0] || null
  restoreError.value = ''
  restoreSuccess.value = ''
}

async function restoreBackup() {
  if (!restoreFile.value || confirmText.value !== 'RESTORE') return

  restoring.value = true
  restoreError.value = ''
  restoreSuccess.value = ''

  const formData = new FormData()
  formData.append('file', restoreFile.value)
  formData.append('confirm_restore', confirmText.value)

  try {
    const { data } = await api.post('/api/portal/utilities/restore', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    restoreSuccess.value = `${data.message}. Restored ${data.restored_tables} tables and ${data.restored_upload_files} uploaded files.`
    restoreFile.value = null
    confirmText.value = ''
    if (fileInput.value) fileInput.value.value = ''
  } catch (err) {
    restoreError.value = err.response?.data?.detail || 'Failed to restore backup.'
  } finally {
    restoring.value = false
  }
}
</script>

<style scoped>
.utilities-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 1rem;
}

.utility-panel {
  display: grid;
  align-content: start;
  gap: 1rem;
}

.panel-heading {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 1rem;
}

.eyebrow {
  margin: 0 0 0.2rem;
  color: var(--dvm-muted);
  font-size: 0.72rem;
  font-weight: 850;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.panel-heading h2 {
  margin: 0;
  color: var(--dvm-text);
  font-size: 1.1rem;
}

.panel-copy {
  margin: 0;
  color: var(--dvm-muted);
  line-height: 1.55;
}

.status-pill {
  border-radius: 6px;
  background: #e0f2fe;
  color: #075985;
  font-size: 0.72rem;
  font-weight: 850;
  padding: 0.25rem 0.45rem;
  text-transform: uppercase;
}

.status-pill.danger {
  background: #fee2e2;
  color: #991b1b;
}

.restore-form {
  display: grid;
  gap: 0.85rem;
}

.field {
  display: grid;
  gap: 0.35rem;
  color: var(--dvm-text);
  font-size: 0.86rem;
  font-weight: 750;
}

.field input {
  width: 100%;
}

.error-banner,
.success-banner {
  border-radius: 7px;
  padding: 0.7rem 0.8rem;
  font-size: 0.86rem;
  font-weight: 700;
}

.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
}

.success-banner {
  background: #ecfdf5;
  border: 1px solid #bbf7d0;
  color: #047857;
}

@media (max-width: 820px) {
  .utilities-grid {
    grid-template-columns: 1fr;
  }
}
</style>
