<template>
  <div class="achievers-slider bg-white rounded-lg shadow-lg p-6">
    <h3 class="text-2xl font-bold text-center text-primary-600 mb-4">
      🏆 Achievers of the Year
    </h3>
    
    <div v-if="loading" class="text-center py-8">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
    </div>

    <div v-else-if="achievers.length > 0" class="relative">
      <!-- Main Slider -->
      <div class="overflow-hidden relative" style="min-height: 400px;">
        <transition-group name="slide" tag="div">
          <div
            v-for="(achiever, index) in achievers"
            v-show="index === currentIndex"
            :key="achiever.id"
            class="achiever-slide"
          >
            <div class="text-center">
              <!-- Photo -->
              <div class="mb-4 flex justify-center">
                <img
                  v-if="achiever.photo_url"
                  :src="getImageUrl(achiever.photo_url)"
                  :alt="achiever.name"
                  class="w-48 h-48 object-cover rounded-full border-4 border-primary-500 shadow-lg"
                  @error="handleImageError"
                />
                <div v-else class="w-48 h-48 rounded-full bg-gray-200 flex items-center justify-center">
                  <svg class="w-24 h-24 text-gray-400" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd" />
                  </svg>
                </div>
              </div>

              <!-- Name -->
              <h4 class="text-xl font-bold text-gray-800 mb-2">
                {{ achiever.name }}
              </h4>

              <!-- Achievement -->
              <p class="text-gray-600 mb-3 px-4">
                {{ achiever.achievement }}
              </p>

              <!-- Category Badge -->
              <span
                class="inline-block px-4 py-1 rounded-full text-sm font-semibold"
                :class="{
                  'bg-blue-100 text-blue-800': achiever.category === 'Academic',
                  'bg-green-100 text-green-800': achiever.category === 'Sports',
                  'bg-purple-100 text-purple-800': achiever.category === 'Cultural',
                  'bg-orange-100 text-orange-800': achiever.category === 'Other'
                }"
              >
                {{ achiever.category }} • {{ achiever.year }}
              </span>
            </div>
          </div>
        </transition-group>
      </div>

      <!-- Navigation Arrows -->
      <button
        @click="prevSlide"
        class="absolute left-0 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white rounded-full p-2 shadow-lg transition-all"
        aria-label="Previous achiever"
      >
        <svg class="w-6 h-6 text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
      </button>
      <button
        @click="nextSlide"
        class="absolute right-0 top-1/2 transform -translate-y-1/2 bg-white/80 hover:bg-white rounded-full p-2 shadow-lg transition-all"
        aria-label="Next achiever"
      >
        <svg class="w-6 h-6 text-gray-800" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
        </svg>
      </button>

      <!-- Dots Indicator -->
      <div class="flex justify-center mt-6 gap-2">
        <button
          v-for="(achiever, index) in achievers"
          :key="`dot-${achiever.id}`"
          @click="goToSlide(index)"
          class="w-2 h-2 rounded-full transition-all"
          :class="index === currentIndex ? 'bg-primary-600 w-8' : 'bg-gray-300 hover:bg-gray-400'"
          :aria-label="`Go to achiever ${index + 1}`"
        />
      </div>
    </div>

    <div v-else class="text-center py-8 text-gray-500">
      No achievers to display
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { apiClient } from '../config/api'

interface Achiever {
  id: string
  name: string
  photo_url: string | null
  achievement: string
  category: string
  year: number
  display_order: number
}

const achievers = ref<Achiever[]>([])
const currentIndex = ref(0)
const loading = ref(true)
let autoPlayInterval: number | null = null

const getImageUrl = (url: string) => {
  if (!url) return ''
  if (url.startsWith('http')) return url
  return `${import.meta.env.VITE_API_BASE_URL?.replace('/api/v1', '') || 'http://localhost:8000'}${url}`
}

const handleImageError = (e: Event) => {
  const target = e.target as HTMLImageElement
  target.style.display = 'none'
}

const fetchAchievers = async () => {
  try {
    loading.value = true
    const response = await apiClient.get('/cms/achievers', {
      params: {
        is_active: true,
        limit: 100,
        sort_by: 'display_order',
        sort_order: 'ASC'
      }
    })
    achievers.value = response.data.data
  } catch (error) {
    console.error('Failed to fetch achievers:', error)
  } finally {
    loading.value = false
  }
}

const nextSlide = () => {
  currentIndex.value = (currentIndex.value + 1) % achievers.value.length
}

const prevSlide = () => {
  currentIndex.value = currentIndex.value === 0 ? achievers.value.length - 1 : currentIndex.value - 1
}

const goToSlide = (index: number) => {
  currentIndex.value = index
}

const startAutoPlay = () => {
  autoPlayInterval = window.setInterval(() => {
    nextSlide()
  }, 5000) // Change slide every 5 seconds
}

const stopAutoPlay = () => {
  if (autoPlayInterval) {
    clearInterval(autoPlayInterval)
    autoPlayInterval = null
  }
}

onMounted(() => {
  fetchAchievers()
  startAutoPlay()
})

onUnmounted(() => {
  stopAutoPlay()
})
</script>

<style scoped>
.achiever-slide {
  position: absolute;
  width: 100%;
  top: 0;
  left: 0;
}

.slide-enter-active,
.slide-leave-active {
  transition: all 0.5s ease;
}

.slide-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.slide-leave-to {
  opacity: 0;
  transform: translateX(-100%);
}
</style>
