<template>
  <div class="page">
    <!-- Hero Banner -->
    <div class="hero">
      <div class="hero-inner">
        <h1 class="hero-school">DVM School</h1>
        <p class="hero-tagline">Explore lesson plans crafted for curious minds</p>
      </div>
      <!-- Wave SVG -->
      <svg class="hero-wave" viewBox="0 0 1440 60" preserveAspectRatio="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M0,30 C360,60 1080,0 1440,30 L1440,60 L0,60 Z" fill="#f0f4ff"/>
      </svg>
    </div>

    <!-- Content Area -->
    <div class="content">
      <p class="section-eyebrow">Browse</p>
      <h2 class="section-heading">Choose Your Class</h2>

      <LoadingSpinner v-if="loading" message="Loading classes…" />

      <div v-else-if="error" class="error-box">
        <ErrorBanner :message="error" />
        <button class="retry-btn" @click="fetchClasses">Retry</button>
      </div>

      <div v-else class="grid">
        <div
          v-for="cls in classes"
          :key="cls.id"
          class="class-card"
          :style="{ background: classGradient(cls.id) }"
          @click="router.push(`/class/${cls.id}`)"
        >
          <span class="class-number">{{ classNumber(cls.name) }}</span>
          <span class="class-label">{{ cls.name }}</span>
          <span class="class-arrow">→</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api.js'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import ErrorBanner from '../components/ErrorBanner.vue'

const router = useRouter()
const classes = ref([])
const loading = ref(true)
const error = ref(null)

const gradients = [
  'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
  'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
  'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
  'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
  'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
  'linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)',
  'linear-gradient(135deg, #f7971e 0%, #ffd200 100%)',
  'linear-gradient(135deg, #56ab2f 0%, #a8e063 100%)',
]

function classGradient(id) {
  return gradients[(id - 1) % gradients.length]
}

function classNumber(name) {
  const match = name.match(/\d+/)
  return match ? match[0] : name.charAt(0)
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
.page {
  min-height: 100vh;
  background: #f0f4ff;
  font-family: system-ui, -apple-system, sans-serif;
}

/* Hero */
.hero {
  position: relative;
  background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
  padding: 4rem 2rem 3.5rem;
  text-align: center;
  overflow: hidden;
}

.hero-inner {
  position: relative;
  z-index: 1;
}

.hero-school {
  font-size: 3rem;
  font-weight: 900;
  color: #fff;
  margin: 0 0 0.75rem;
  letter-spacing: -0.02em;
  text-shadow: 0 2px 16px rgba(0, 0, 0, 0.18);
}

.hero-tagline {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.88);
  margin: 0;
  font-weight: 400;
  letter-spacing: 0.01em;
}

.hero-wave {
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 60px;
  display: block;
}

/* Content */
.content {
  max-width: 860px;
  margin: 0 auto;
  padding: 2.5rem 1.5rem 4rem;
  text-align: center;
}

.section-eyebrow {
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #6b7280;
  margin: 0 0 0.4rem;
}

.section-heading {
  font-size: 1.8rem;
  font-weight: 800;
  color: #1e1b4b;
  margin: 0 0 2rem;
}

/* Grid */
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 1.25rem;
}

.class-card {
  position: relative;
  border-radius: 16px;
  padding: 2.2rem 1.25rem 1.5rem;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #fff;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.class-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 32px rgba(0, 0, 0, 0.22);
}

.class-number {
  font-size: 3.8rem;
  font-weight: 900;
  line-height: 1;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
}

.class-label {
  font-size: 1rem;
  font-weight: 600;
  margin-top: 0.45rem;
  opacity: 0.92;
  letter-spacing: 0.04em;
}

.class-arrow {
  position: absolute;
  bottom: 0.85rem;
  right: 1rem;
  font-size: 1.1rem;
  opacity: 0.7;
  font-weight: 700;
}

/* Error */
.error-box {
  text-align: center;
  padding: 2rem;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background: #4f46e5;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1rem;
  font-family: inherit;
  transition: background 0.2s ease;
}

.retry-btn:hover {
  background: #4338ca;
}

@media (max-width: 640px) {
  .hero-school { font-size: 2.2rem; }
  .hero-tagline { font-size: 1rem; }
  .content { padding: 2rem 1rem 3rem; }
  .section-heading { font-size: 1.4rem; }
  .grid { grid-template-columns: repeat(2, 1fr); gap: 1rem; }
  .class-number { font-size: 3rem; }
}
</style>
