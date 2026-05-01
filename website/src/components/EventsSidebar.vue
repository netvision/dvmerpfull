<template>
  <div class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-gradient-to-r from-green-600 to-teal-600 px-4 py-3 border-b-2 border-green-700">
      <div class="flex items-center justify-between">
        <h3 class="text-base font-bold text-white flex items-center">
          <CalendarDays :size="16" class="mr-2" />
          Upcoming Events
        </h3>
        <router-link 
          to="/events"
          class="text-green-100 hover:text-white transition-colors text-xs font-medium no-underline flex items-center"
        >
          <span>View All</span>
          <ChevronRight :size="14" class="ml-1" />
        </router-link>
      </div>
    </div>

    <!-- Event Items -->
    <div class="divide-y divide-gray-100 max-h-80 overflow-y-auto">
      <article 
        v-for="(event, index) in upcomingEvents" 
        :key="index"
        class="p-3 hover:bg-green-50 transition-colors duration-200 cursor-pointer group border-l-3 border-transparent hover:border-green-500"
      >
        <div class="flex items-start space-x-2">
          <div class="flex-shrink-0">
            <div class="w-10 h-10 bg-gradient-to-r from-green-500 to-teal-500 rounded-lg flex flex-col items-center justify-center text-white shadow-sm">
              <span class="text-xs font-bold leading-none">{{ formatDay(event.date) }}</span>
              <span class="text-xs leading-none">{{ formatMonth(event.date) }}</span>
            </div>
          </div>
          
          <div class="flex-1 min-w-0">
            <h4 class="text-xs font-semibold text-gray-900 group-hover:text-green-700 transition-colors line-clamp-2 mb-1">
              {{ event.title }}
            </h4>
            <p class="text-xs text-gray-600 mb-1 line-clamp-1">
              {{ event.description }}
            </p>
            <div class="flex items-center justify-between">
              <div class="flex items-center text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">
                <Clock :size="12" class="mr-1" />
                {{ event.time }}
              </div>
              <span class="text-xs text-green-600 font-medium group-hover:text-green-700 flex items-center">
                Learn more
                <ArrowRight :size="12" class="ml-1 group-hover:translate-x-1 transition-transform" />
              </span>
            </div>
          </div>
        </div>
      </article>
    </div>

    <!-- View All Link -->
    <div class="px-6 py-4 bg-gray-50 border-t border-gray-200">
      <router-link 
        to="/events"
        class="w-full inline-flex items-center justify-center px-4 py-2 bg-gradient-to-r from-green-600 to-teal-600 text-white text-sm font-medium rounded-lg hover:shadow-lg transition-all duration-200 transform hover:scale-105 no-underline"
      >
        <span>View All Events</span>
        <ArrowRight :size="16" class="ml-2" />
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { CalendarDays, Clock, ArrowRight, ChevronRight } from 'lucide-vue-next'
import cmsService, { type Event } from '../services/cms.service'

const upcomingEvents = ref<Array<{
  title: string
  description: string
  date: string
  time: string
  slug: string
}>>([])

// Helper functions for date formatting
const formatDay = (dateString: string) => {
  const date = new Date(dateString)
  return date.getDate().toString().padStart(2, '0')
}

const formatMonth = (dateString: string) => {
  const date = new Date(dateString)
  const months = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
  return months[date.getMonth()]
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

onMounted(async () => {
  try {
    const response = await cmsService.getEvents({ limit: 5, upcoming: true })
    upcomingEvents.value = response.data.map((event: Event) => ({
      title: event.title,
      description: event.description || '',
      date: event.start_date,
      time: formatTime(event.start_date, event.end_date),
      slug: event.slug
    }))
  } catch (error) {
    console.error('Error fetching events:', error)
    // Keep empty array on error
    upcomingEvents.value = []
  }
})
</script>

<style scoped>
/* Line clamp utility for text truncation */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-clamp: 2;
}

/* Remove underline from router-links */
.no-underline {
  text-decoration: none !important;
}

.no-underline:hover {
  text-decoration: none !important;
}
</style>
