<template>
  <div class="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
    <!-- Header -->
    <div class="bg-gradient-to-r from-blue-600 to-purple-600 px-4 py-3 border-b-2 border-blue-700">
      <div class="flex items-center justify-between">
        <h3 class="text-base font-bold text-white flex items-center">
          <Newspaper :size="16" class="mr-2" />
          Latest News
        </h3>
        <router-link 
          to="/news"
          class="text-blue-100 hover:text-white transition-colors text-xs font-medium no-underline flex items-center"
        >
          <span>View All</span>
          <ChevronRight :size="14" class="ml-1" />
        </router-link>
      </div>
    </div>

    <!-- News Items -->
    <div class="divide-y divide-gray-100 max-h-80 overflow-y-auto">
      <router-link 
        v-for="(article, index) in latestNews" 
        :key="index"
        :to="`/news/${article.slug}`"
        class="block p-3 hover:bg-blue-50 transition-colors duration-200 cursor-pointer group border-l-3 border-transparent hover:border-blue-500 no-underline"
      >
        <div class="flex items-start space-x-2">
          <div class="flex-shrink-0">
            <div class="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center shadow-sm">
              <Calendar :size="12" class="text-white" />
            </div>
          </div>
          
          <div class="flex-1 min-w-0">
            <div class="flex items-center justify-between mb-1">
              <h4 class="text-xs font-semibold text-gray-900 group-hover:text-blue-700 transition-colors line-clamp-2 flex-1">
                {{ article.title }}
              </h4>
              <span v-if="article.category_name" class="ml-2 px-1.5 py-0.5 text-xs bg-blue-100 text-blue-700 rounded flex-shrink-0">
                {{ article.category_name }}
              </span>
            </div>
            <p class="text-xs text-gray-600 mb-1 line-clamp-1">
              {{ article.excerpt }}
            </p>
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded-full">{{ article.date }}</span>
              <span class="text-xs text-blue-600 font-medium group-hover:text-blue-700 flex items-center">
                Read more
                <ArrowRight :size="12" class="ml-1 group-hover:translate-x-1 transition-transform" />
              </span>
            </div>
          </div>
        </div>
      </router-link>
    </div>

    <!-- View All Link -->
    <div class="px-6 py-4 bg-gray-50 border-t border-gray-200">
      <router-link 
        to="/news"
        class="w-full inline-flex items-center justify-center px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white text-sm font-medium rounded-lg hover:shadow-lg transition-all duration-200 transform hover:scale-105 no-underline"
      >
        <span>View All News</span>
        <ArrowRight :size="16" class="ml-2" />
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Newspaper, Calendar, ArrowRight, ChevronRight } from 'lucide-vue-next'
import cmsService, { type NewsArticle } from '../services/cms.service'

const latestNews = ref<Array<{
  title: string
  excerpt: string
  date: string
  slug: string
  category_name?: string | null
}>>([])

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(async () => {
  try {
    const response = await cmsService.getNews({ limit: 5, status: 'published' })
    latestNews.value = response.data.map((article: NewsArticle) => ({
      title: article.title,
      excerpt: article.excerpt || article.content.substring(0, 100) + '...',
      date: formatDate(article.published_at || article.created_at),
      slug: article.slug,
      category_name: article.category_name
    }))
  } catch (error) {
    console.error('Error fetching news:', error)
    // Keep empty array on error
    latestNews.value = []
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
