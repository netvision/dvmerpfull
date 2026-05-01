<template>
  <div class="events-page bg-gray-50 min-h-screen">
    <div class="container mx-auto px-4 py-16">
      <!-- Page Header -->
      <div class="mb-12">
        <h1 class="text-4xl font-bold text-blue-900 mb-4">Upcoming Events</h1>
        <p class="text-lg text-gray-600">Join us in our upcoming events and celebrations</p>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <p class="text-gray-600">Loading events...</p>
      </div>

      <!-- Events Grid -->
      <div v-else-if="events.length > 0" class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <article 
          v-for="event in events" 
          :key="event.id"
          class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300 cursor-pointer"
          @click="goToDetail(event.slug)"
        >
          <!-- Featured Image -->
          <img
            v-if="event.featured_image_url"
            :src="event.featured_image_url"
            :alt="event.title"
            class="w-full h-48 object-cover"
          />
          
          <div class="flex">
            <!-- Date Box -->
            <div class="w-32 bg-gradient-to-br from-green-500 to-teal-500 text-white flex flex-col items-center justify-center p-4">
              <span class="text-3xl font-bold">{{ formatDay(event.start_date) }}</span>
              <span class="text-sm uppercase">{{ formatMonth(event.start_date) }}</span>
              <span class="text-xs mt-1">{{ formatYear(event.start_date) }}</span>
            </div>

            <!-- Event Details -->
            <div class="flex-1 p-6">
              <h2 class="text-xl font-bold text-gray-900 mb-2 line-clamp-2">{{ event.title }}</h2>
              <p class="text-gray-600 mb-3 line-clamp-2">{{ event.description }}</p>
              
              <div class="space-y-2 text-sm text-gray-500">
                <div class="flex items-center">
                  <Clock :size="16" class="mr-2" />
                  <span>{{ formatTime(event.start_date, event.end_date) }}</span>
                </div>
                <div v-if="event.location" class="flex items-center">
                  <MapPin :size="16" class="mr-2" />
                  <span>{{ event.location }}</span>
                </div>
                <div v-if="event.capacity" class="flex items-center">
                  <Users :size="16" class="mr-2" />
                  <span>Capacity: {{ event.capacity }}</span>
                </div>
              </div>

              <div class="mt-4">
                <span class="text-sm text-green-600 font-medium flex items-center">
                  View Details
                  <ArrowRight :size="16" class="ml-1" />
                </span>
              </div>
            </div>
          </div>
        </article>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-12 bg-white rounded-lg shadow">
        <p class="text-gray-500 text-lg">No upcoming events at the moment.</p>
      </div>

      <!-- Pagination -->
      <div v-if="pagination.total > pagination.limit" class="mt-12 flex justify-center items-center gap-4">
        <button
          @click="changePage(pagination.page - 1)"
          :disabled="pagination.page === 1"
          class="px-4 py-2 bg-white border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        <span class="text-gray-700">
          Page {{ pagination.page }} of {{ pagination.pages }}
        </span>
        <button
          @click="changePage(pagination.page + 1)"
          :disabled="pagination.page >= pagination.pages"
          class="px-4 py-2 bg-white border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Clock, MapPin, Users, ArrowRight } from 'lucide-vue-next'
import cmsService, { type Event } from '../services/cms.service'

const router = useRouter()
const loading = ref(true)
const events = ref<Event[]>([])
const pagination = ref({
  page: 1,
  limit: 10,
  total: 0,
  pages: 1
})

const formatDay = (dateString: string) => {
  const date = new Date(dateString)
  return date.getDate().toString().padStart(2, '0')
}

const formatMonth = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', { month: 'short' }).toUpperCase()
}

const formatYear = (dateString: string) => {
  const date = new Date(dateString)
  return date.getFullYear()
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

const goToDetail = (slug: string) => {
  router.push(`/events/${slug}`)
}

const loadEvents = async () => {
  loading.value = true
  try {
    const response = await cmsService.getEvents({
      page: pagination.value.page,
      limit: pagination.value.limit,
      upcoming: true
    })
    events.value = response.data
    pagination.value = response.pagination
  } catch (error) {
    console.error('Error loading events:', error)
  } finally {
    loading.value = false
  }
}

const changePage = (page: number) => {
  pagination.value.page = page
  loadEvents()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  loadEvents()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
