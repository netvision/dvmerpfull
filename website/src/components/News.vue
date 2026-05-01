<template>
  <section class="py-16 bg-white">
    <div class="container mx-auto px-4">
      <div class="flex flex-col lg:flex-row gap-10">
        <!-- News Section -->
        <div class="lg:w-2/3">
          <h2 class="text-3xl font-bold text-blue-900 mb-2">Latest News</h2>
          <div class="w-20 h-1 bg-yellow-500 mb-6"></div>
          
          <div v-if="loading" class="text-center py-8">
            <p class="text-gray-600">Loading news...</p>
          </div>
          
          <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div 
              v-for="item in newsItems" 
              :key="item.id" 
              class="bg-white border border-gray-200 rounded-lg overflow-hidden shadow-sm hover:shadow-md transition-shadow"
            >
              <img 
                :src="item.image" 
                :alt="item.title" 
                class="w-full h-48 object-cover"
              />
              <div class="p-5">
                <div class="flex items-center gap-2 text-sm text-gray-600 mb-2">
                  <Calendar :size="14" />
                  <span>{{ item.date }}</span>
                </div>
                <h3 class="font-bold text-lg mb-2">{{ item.title }}</h3>
                <p class="text-gray-700 text-sm mb-3">{{ item.excerpt }}</p>
                <router-link 
                  :to="`/news/${item.slug}`"
                  class="inline-flex items-center text-blue-700 hover:text-blue-800 font-medium text-sm"
                >
                  Read More <ArrowRight :size="14" class="ml-1" />
                </router-link>
              </div>
            </div>
          </div>
          
          <div class="mt-6 text-center">
            <router-link 
              to="/news" 
              class="inline-flex items-center justify-center bg-blue-700 hover:bg-blue-800 text-white font-medium py-2 px-4 rounded transition-colors"
            >
              View All News
            </router-link>
          </div>
        </div>
        
        <!-- Events Section -->
        <div class="lg:w-1/3">
          <h2 class="text-3xl font-bold text-blue-900 mb-2">Upcoming Events</h2>
          <div class="w-20 h-1 bg-yellow-500 mb-6"></div>
          
          <div class="bg-gray-50 rounded-lg p-6">
            <div v-if="loading" class="text-center py-4">
              <p class="text-gray-600">Loading events...</p>
            </div>
            
            <div v-else>
              <div 
                v-for="event in events" 
                :key="event.id" 
                class="mb-4 pb-4 border-b border-gray-200 last:border-0 last:mb-0 last:pb-0"
              >
                <h3 class="font-bold text-lg mb-1">{{ event.title }}</h3>
                <div class="text-sm text-gray-700">
                  <div class="flex items-center gap-2">
                    <Calendar :size="14" />
                    <span>{{ event.date }}</span>
                  </div>
                  <div class="mt-1">{{ event.time }}</div>
                </div>
              </div>
            </div>
            
            <router-link 
              to="/events" 
              class="inline-flex items-center justify-center w-full bg-white border border-blue-700 text-blue-700 hover:bg-blue-50 font-medium py-2 px-4 rounded mt-4 transition-colors"
            >
              View All Events
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Calendar, ArrowRight } from 'lucide-vue-next'
import cmsService from '../services/cms.service'
import type { NewsArticle, Event } from '../services/cms.service'

interface NewsItem {
  id: number
  title: string
  date: string
  excerpt: string
  image: string
  slug: string
}

interface EventItem {
  id: number
  title: string
  date: string
  time: string
  slug: string
}

const newsItems = ref<NewsItem[]>([])
const events = ref<EventItem[]>([])
const loading = ref(true)

// Format date helper
const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

// Format event date/time helper
const formatEventDateTime = (startDate: string, endDate: string) => {
  const start = new Date(startDate)
  const end = new Date(endDate)
  
  const date = start.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
  
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
  
  return { date, time: `${startTime} - ${endTime}` }
}

onMounted(async () => {
  try {
    // Fetch real data from API
    const [newsRes, eventsRes] = await Promise.all([
      cmsService.getNews({ limit: 3, status: 'published' }),
      cmsService.getEvents({ limit: 4, upcoming: true })
    ])
    
    // Transform news data
    newsItems.value = newsRes.data.map((article: NewsArticle) => ({
      id: article.id,
      title: article.title,
      slug: article.slug,
      date: formatDate(article.published_at || article.created_at),
      excerpt: article.excerpt || article.content.substring(0, 150) + '...',
      image: article.featured_image_url || 'https://pub-cdn.sider.ai/u/U01AH8KELLX/web-coder/684e997d0484c40371d10541/resource/3287fc45-4809-4e3f-84b6-8aea6ee8e9ac.jpg'
    }))
    
    // Transform events data
    events.value = eventsRes.data.map((event: Event) => {
      const { date, time } = formatEventDateTime(event.start_date, event.end_date)
      return {
        id: event.id,
        title: event.title,
        slug: event.slug,
        date,
        time
      }
    })
  } catch (error) {
    console.error('Error fetching news or events:', error)
    // If API fails, keep empty arrays
    newsItems.value = []
    events.value = []
  } finally {
    loading.value = false
  }
})
</script>
