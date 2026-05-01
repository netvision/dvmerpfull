<template>
  <div class="event-detail-page bg-gray-50 min-h-screen">
    <!-- Loading State -->
    <div v-if="loading" class="container mx-auto px-4 py-16 text-center">
      <p class="text-gray-600">Loading event...</p>
    </div>

    <!-- Event Content -->
    <article v-else-if="event" class="container mx-auto px-4 py-16">
      <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
        <!-- Featured Image -->
        <img 
          v-if="event.featured_image_url"
          :src="event.featured_image_url" 
          :alt="event.title"
          class="w-full h-96 object-cover"
        />

        <!-- Event Header -->
        <div class="p-8">
          <h1 class="text-4xl font-bold text-gray-900 mb-6">{{ event.title }}</h1>

          <!-- Event Details Grid -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8 p-6 bg-gray-50 rounded-lg">
            <div class="flex items-start">
              <Calendar :size="24" class="mr-3 text-green-600 flex-shrink-0 mt-1" />
              <div>
                <p class="text-sm text-gray-500 mb-1">Date</p>
                <p class="text-lg font-semibold text-gray-900">{{ formatFullDate(event.start_date) }}</p>
              </div>
            </div>

            <div class="flex items-start">
              <Clock :size="24" class="mr-3 text-green-600 flex-shrink-0 mt-1" />
              <div>
                <p class="text-sm text-gray-500 mb-1">Time</p>
                <p class="text-lg font-semibold text-gray-900">{{ formatTime(event.start_date, event.end_date) }}</p>
              </div>
            </div>

            <div v-if="event.location" class="flex items-start">
              <MapPin :size="24" class="mr-3 text-green-600 flex-shrink-0 mt-1" />
              <div>
                <p class="text-sm text-gray-500 mb-1">Location</p>
                <p class="text-lg font-semibold text-gray-900">{{ event.location }}</p>
              </div>
            </div>

            <div v-if="event.capacity" class="flex items-start">
              <Users :size="24" class="mr-3 text-green-600 flex-shrink-0 mt-1" />
              <div>
                <p class="text-sm text-gray-500 mb-1">Capacity</p>
                <p class="text-lg font-semibold text-gray-900">{{ event.capacity }} attendees</p>
              </div>
            </div>
          </div>

          <!-- Description -->
          <div class="prose prose-lg max-w-none mb-8">
            <h2 class="text-2xl font-bold text-gray-900 mb-4">About This Event</h2>
            <div v-html="formatDescription(event.description)"></div>
          </div>

          <!-- Image Gallery -->
          <div v-if="event.gallery && event.gallery.length > 0" class="mb-8">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Photo Gallery</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div
                v-for="image in event.gallery"
                :key="image.id"
                class="group relative overflow-hidden rounded-lg shadow-md hover:shadow-xl transition-shadow"
              >
                <img
                  :src="image.image_url"
                  :alt="image.caption || 'Gallery image'"
                  class="w-full h-64 object-cover group-hover:scale-110 transition-transform duration-300"
                />
                <div v-if="image.caption" class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/70 to-transparent p-4">
                  <p class="text-white text-sm">{{ image.caption }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Status Badge -->
          <div class="mb-8">
            <span 
              :class="getStatusClass(event.status)"
              class="inline-block px-4 py-2 rounded-full text-sm font-semibold"
            >
              {{ formatStatus(event.status) }}
            </span>
          </div>

          <!-- Back Button -->
          <div class="pt-8 border-t border-gray-200">
            <button 
              @click="$router.push('/events')"
              class="inline-flex items-center text-green-600 hover:text-green-800 font-medium"
            >
              <ArrowLeft :size="20" class="mr-2" />
              Back to All Events
            </button>
          </div>
        </div>
      </div>
    </article>

    <!-- Error State -->
    <div v-else class="container mx-auto px-4 py-16 text-center">
      <p class="text-gray-500 text-lg mb-4">Event not found</p>
      <button 
        @click="$router.push('/events')"
        class="inline-flex items-center text-green-600 hover:text-green-800 font-medium"
      >
        <ArrowLeft :size="20" class="mr-2" />
        Back to All Events
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Calendar, Clock, MapPin, Users, ArrowLeft } from 'lucide-vue-next'
import cmsService, { type Event } from '../services/cms.service'

const route = useRoute()
const loading = ref(true)
const event = ref<Event | null>(null)

const formatFullDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatTime = (startDate: string, endDate: string) => {
  const start = new Date(startDate)
  const end = new Date(endDate)
  
  const startTime = start.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
  
  const endTime = end.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true
  })
  
  return `${startTime} - ${endTime}`
}

const formatDescription = (description: string | null) => {
  if (!description) return '<p>No description available.</p>'
  return description.split('\n\n').map(para => `<p>${para.replace(/\n/g, '<br>')}</p>`).join('')
}

const formatStatus = (status: string) => {
  return status.charAt(0).toUpperCase() + status.slice(1)
}

const getStatusClass = (status: string) => {
  switch (status) {
    case 'upcoming':
      return 'bg-green-100 text-green-800'
    case 'ongoing':
      return 'bg-blue-100 text-blue-800'
    case 'completed':
      return 'bg-gray-100 text-gray-800'
    case 'cancelled':
      return 'bg-red-100 text-red-800'
    default:
      return 'bg-gray-100 text-gray-800'
  }
}

onMounted(async () => {
  try {
    const slug = route.params.slug as string
    const response = await cmsService.getEventBySlug(slug)
    event.value = response.data
  } catch (error) {
    console.error('Error loading event:', error)
    event.value = null
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.prose p {
  margin-bottom: 1.25rem;
  line-height: 1.75;
  color: #374151;
}

.prose h3 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-top: 1.5rem;
  margin-bottom: 0.75rem;
  color: #1f2937;
}

.prose ul, .prose ol {
  margin-bottom: 1.25rem;
  padding-left: 1.5rem;
}

.prose li {
  margin-bottom: 0.5rem;
}
</style>
