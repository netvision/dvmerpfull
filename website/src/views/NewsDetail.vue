<template>
  <div class="news-detail-page bg-gray-50 min-h-screen">
    <!-- Loading State -->
    <div v-if="loading" class="container mx-auto px-4 py-16 text-center">
      <p class="text-gray-600">Loading article...</p>
    </div>

    <!-- Article Content -->
    <article v-else-if="article" class="container mx-auto px-4 py-16">
      <div class="max-w-4xl mx-auto bg-white rounded-lg shadow-lg overflow-hidden">
        <!-- Featured Image -->
        <img 
          v-if="article.featured_image_url"
          :src="article.featured_image_url" 
          :alt="article.title"
          class="w-full h-96 object-cover"
        />

        <!-- Article Header -->
        <div class="p-8">
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center text-sm text-gray-500">
              <Calendar :size="16" class="mr-2" />
              <span>{{ formatDate(article.published_at || article.created_at) }}</span>
              <span class="mx-3">•</span>
              <Eye :size="16" class="mr-2" />
              <span>{{ article.views || 0 }} views</span>
            </div>
            <span v-if="article.category_name" class="px-3 py-1 text-sm font-medium bg-blue-100 text-blue-800 rounded-lg">
              {{ article.category_name }}
            </span>
          </div>

          <h1 class="text-4xl font-bold text-gray-900 mb-6">{{ article.title }}</h1>

          <!-- Excerpt -->
          <p v-if="article.excerpt" class="text-xl text-gray-600 mb-8 italic border-l-4 border-blue-500 pl-4">
            {{ article.excerpt }}
          </p>

          <!-- Content -->
          <div class="prose prose-lg max-w-none" v-html="formatContent(article.content)"></div>

          <!-- Image Gallery -->
          <div v-if="article.gallery && article.gallery.length > 0" class="mt-12">
            <h2 class="text-2xl font-bold text-gray-900 mb-6">Photo Gallery</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div
                v-for="image in article.gallery"
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

          <!-- Back Button -->
          <div class="mt-12 pt-8 border-t border-gray-200">
            <button 
              @click="$router.push('/news')"
              class="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium"
            >
              <ArrowLeft :size="20" class="mr-2" />
              Back to All News
            </button>
          </div>
        </div>
      </div>
    </article>

    <!-- Error State -->
    <div v-else class="container mx-auto px-4 py-16 text-center">
      <p class="text-gray-500 text-lg mb-4">Article not found</p>
      <button 
        @click="$router.push('/news')"
        class="inline-flex items-center text-blue-600 hover:text-blue-800 font-medium"
      >
        <ArrowLeft :size="20" class="mr-2" />
        Back to All News
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { Calendar, Eye, ArrowLeft } from 'lucide-vue-next'
import cmsService, { type NewsArticle } from '../services/cms.service'

const route = useRoute()
const loading = ref(true)
const article = ref<NewsArticle | null>(null)

const formatDate = (dateString: string) => {
  const date = new Date(dateString)
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const formatContent = (content: string) => {
  // Convert line breaks to paragraphs
  return content.split('\n\n').map(para => `<p>${para.replace(/\n/g, '<br>')}</p>`).join('')
}

onMounted(async () => {
  try {
    const slug = route.params.slug as string
    const response = await cmsService.getNewsBySlug(slug)
    article.value = response.data
  } catch (error) {
    console.error('Error loading article:', error)
    article.value = null
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.prose {
  color: #374151;
  line-height: 1.75;
}

.prose p {
  margin-bottom: 1.25rem;
}

.prose h2 {
  font-size: 1.875rem;
  font-weight: 700;
  margin-top: 2rem;
  margin-bottom: 1rem;
  color: #1f2937;
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
