<template>
  <main class="public-home dvm-page">
    <section class="home-hero dvm-container">
      <div class="home-copy">
        <h1>Browse lesson plans by class, subject, and chapter.</h1>
        <p>
          A focused academic workspace for Dalmia Vidya Mandir lesson material,
          prepared chapters, concepts, exhibits, and chapter PDFs.
        </p>
        <div class="home-search" role="search">
          <input v-model="classQuery" type="search" placeholder="Filter classes..." aria-label="Filter classes" />
          <button class="dvm-btn dvm-btn--navy" type="button" @click="classQuery = ''">Clear</button>
        </div>
      </div>
      <aside class="home-preview dvm-card" aria-label="Lesson browser preview">
        <div class="preview-item">
          <strong>Class 6 - Science</strong>
          <span>Concepts, outcomes, activities, exhibits</span>
          <div class="preview-bars"><i></i><i></i><i></i></div>
        </div>
        <div class="preview-item">
          <strong>Chapter PDFs</strong>
          <span>Open attached teaching documents quickly</span>
          <div class="preview-bars"><i></i><i></i><i></i></div>
        </div>
      </aside>
    </section>

    <section class="class-section dvm-container">
      <div class="section-head">
        <div>
          <p class="eyebrow">Lesson Library</p>
          <h2>Choose your class</h2>
        </div>
        <span v-if="!loading && !error" class="dvm-badge">{{ filteredClasses.length }} available</span>
      </div>

      <LoadingSpinner v-if="loading" message="Loading classes..." />

      <div v-else-if="error" class="dvm-error">
        <ErrorBanner :message="error" />
        <button class="dvm-btn dvm-btn--navy retry-btn" @click="fetchClasses">Retry</button>
      </div>

      <div v-else-if="filteredClasses.length === 0" class="dvm-empty">
        No classes match your filter.
      </div>

      <div v-else class="class-grid">
        <button
          v-for="cls in filteredClasses"
          :key="cls.id"
          class="class-tile"
          type="button"
          @click="router.push(`/class/${cls.id}`)"
        >
          <span class="class-number">{{ classNumber(cls.name) }}</span>
          <span class="class-name">{{ cls.name }}</span>
          <span class="class-action">Open class</span>
        </button>
      </div>
    </section>
  </main>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api.js'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import ErrorBanner from '../components/ErrorBanner.vue'

const router = useRouter()
const classes = ref([])
const loading = ref(true)
const error = ref(null)
const classQuery = ref('')

const filteredClasses = computed(() => {
  const q = classQuery.value.trim().toLowerCase()
  if (!q) return classes.value
  return classes.value.filter(cls => cls.name.toLowerCase().includes(q))
})

function classNumber(name) {
  const match = name.match(/\d+/)
  if (match) return match[0]
  return name.replace(/^Class\s+/i, '').slice(0, 3).toUpperCase()
}

async function fetchClasses() {
  loading.value = true
  error.value = null
  try {
    const res = await api.get('/api/public/classes')
    classes.value = res.data
  } catch (e) {
    error.value = e.response?.data?.detail || e.message || 'Failed to load classes'
  } finally {
    loading.value = false
  }
}

onMounted(fetchClasses)
</script>

<style scoped>
.public-home {
  padding-bottom: 4rem;
}

.home-hero {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(320px, 0.9fr);
  gap: 2rem;
  align-items: center;
  padding: 3rem 0 2rem;
}

.home-copy h1 {
  max-width: 720px;
  margin: 0;
  color: var(--dvm-navy);
  font-size: clamp(2rem, 4vw, 3.15rem);
  line-height: 1.06;
  letter-spacing: 0;
}

.home-copy p {
  max-width: 640px;
  margin: 1rem 0 0;
  color: var(--dvm-muted);
  font-size: 1rem;
}

.home-search {
  display: flex;
  gap: 0.65rem;
  max-width: 520px;
  margin-top: 1.5rem;
}

.home-search input {
  flex: 1;
  min-width: 0;
  border: 1px solid var(--dvm-line);
  border-radius: var(--dvm-radius);
  padding: 0.75rem 0.85rem;
  outline: none;
}

.home-search input:focus {
  border-color: var(--dvm-blue);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
}

.home-preview {
  padding: 1rem;
  background: #f8fafc;
}

.preview-item {
  background: #fff;
  border: 1px solid var(--dvm-line);
  border-radius: var(--dvm-radius);
  padding: 1rem;
}

.preview-item + .preview-item {
  margin-top: 0.75rem;
}

.preview-item strong,
.preview-item span {
  display: block;
}

.preview-item strong {
  color: var(--dvm-navy);
  font-size: 0.98rem;
}

.preview-item span {
  margin-top: 0.25rem;
  color: var(--dvm-muted);
  font-size: 0.84rem;
}

.preview-bars {
  display: grid;
  gap: 0.45rem;
  margin-top: 0.9rem;
}

.preview-bars i {
  height: 8px;
  border-radius: 999px;
  background: #dbeafe;
}

.preview-bars i:nth-child(2) {
  width: 78%;
  background: #fef3c7;
}

.preview-bars i:nth-child(3) {
  width: 58%;
  background: #dcfce7;
}

.class-section {
  padding-top: 1rem;
}

.section-head {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 1rem;
  margin-bottom: 1rem;
}

.eyebrow {
  margin: 0 0 0.25rem;
  color: var(--dvm-muted);
  font-size: 0.75rem;
  font-weight: 850;
  text-transform: uppercase;
  letter-spacing: 0.07em;
}

.section-head h2 {
  margin: 0;
  color: var(--dvm-text);
  font-size: 1.45rem;
}

.class-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 0.8rem;
}

.class-tile {
  min-height: 118px;
  text-align: left;
  background: #fff;
  border: 1px solid var(--dvm-line);
  border-radius: var(--dvm-radius-lg);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: var(--dvm-shadow-soft);
  transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
}

.class-tile:hover {
  transform: translateY(-2px);
  border-color: var(--dvm-blue);
  box-shadow: var(--dvm-shadow);
}

.class-number {
  color: var(--dvm-navy);
  font-size: 1.8rem;
  font-weight: 900;
}

.class-name {
  color: var(--dvm-text);
  font-weight: 800;
}

.class-action {
  color: var(--dvm-muted);
  font-size: 0.78rem;
  font-weight: 750;
}

.retry-btn {
  margin-top: 0.75rem;
}

@media (max-width: 800px) {
  .home-hero {
    grid-template-columns: 1fr;
    padding-top: 2rem;
  }

  .home-search,
  .section-head {
    align-items: stretch;
    flex-direction: column;
  }
}
</style>
