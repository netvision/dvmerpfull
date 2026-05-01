<template>
  <div class="news-page bg-gray-50 min-h-screen">
    <div class="container mx-auto px-4 py-16">
      <!-- Page Header -->
      <div class="mb-12">
        <h1 class="text-4xl font-bold text-blue-900 mb-4">Latest News</h1>
        <p class="text-lg text-gray-600">Stay updated with the latest happenings at our institute</p>
      </div>

      <!-- Category Filter -->
      <div class="mb-8 flex flex-wrap gap-3">
        <button
          @click="selectedCategory = null; loadNews()"
          :class="[selectedCategory === null ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-50']"
          class="px-4 py-2 rounded-lg border border-gray-200 transition-colors"
        >
          All News
        </button>
        <button
          v-for="category in categories"
          :key="category.id"
          @click="selectedCategory = category.id; loadNews()"
          :class="[selectedCategory === category.id ? 'bg-blue-600 text-white' : 'bg-white text-gray-700 hover:bg-gray-50']"
          class="px-4 py-2 rounded-lg border border-gray-200 transition-colors"
        >
          {{ category.name }}
        </button>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="text-center py-12">
        <p class="text-gray-600">Loading news...</p>
      </div>

      <!-- News Grid -->
      <div v-else-if="newsItems.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <article 
          v-for="article in newsItems" 
          :key="article.id"
          class="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300 cursor-pointer"
          @click="goToDetail(article.slug)"
        >
          <img 
            :src="article.featured_image_url || 'https://via.placeholder.com/400x250?text=News'" 
            :alt="article.title"
            class="w-full h-48 object-cover"
          />
          <div class="p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center text-sm text-gray-500">
                <Calendar :size="16" class="mr-2" />
                <span>{{ formatDate(article.published_at || article.created_at) }}</span>
              </div>
              <span v-if="article.category_name" class="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 rounded">
                {{ article.category_name }}
              </span>
            </div>
            <h2 class="text-xl font-bold text-gray-900 mb-3 line-clamp-2">{{ article.title }}</h2>
            <p class="text-gray-600 mb-4 line-clamp-3">{{ article.excerpt || getExcerpt(article.content) }}</p>
            <div class="flex items-center justify-between">
              <span class="text-sm text-blue-600 font-medium flex items-center">
                Read More
                <ArrowRight :size="16" class="ml-1" />
              </span>
              <span class="text-xs text-gray-500">{{ article.views || 0 }} views</span>
            </div>
          </div>
        </article>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-12 bg-white rounded-lg shadow">
        <p class="text-gray-500 text-lg">No news articles available at the moment.</p>
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
import { Calendar, ArrowRight } from 'lucide-vue-next'
import cmsService, { type NewsArticle, type NewsCategory } from '../services/cms.service'

const router = useRouter()
const loading = ref(true)
const newsItems = ref<NewsArticle[]>([])
const categories = ref<NewsCategory[]>([])
const selectedCategory = ref<string | null>(null)
const pagination = ref({
  page: 1,
  limit: 9,
  total: 0,
  pages: 1
})

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const getExcerpt = (content: string) => {
  return content.substring(0, 150) + '...'
}

const goToDetail = (slug: string) => {
  router.push(`/news/${slug}`)
}

const loadCategories = async () => {
  try {
    const response = await cmsService.getNewsCategories()
    categories.value = response.data
  } catch (error) {
    console.error('Error loading categories:', error)
  }
}

const loadNews = async () => {
  loading.value = true
  try {
    const response = await cmsService.getNews({
      page: pagination.value.page,
      limit: pagination.value.limit,
      status: 'published',
      category_id: selectedCategory.value || undefined
    })
    newsItems.value = response.data
    pagination.value = response.pagination
  } catch (error) {
    console.error('Error loading news:', error)
  } finally {
    loading.value = false
  }
}

const changePage = (page: number) => {
  pagination.value.page = page
  loadNews()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  loadCategories()
  loadNews()
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
