<template>
  <div class="p-8 space-y-8">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">News Management</h1>
        <p class="text-gray-600">Create, update and delete website news articles.</p>
      </div>
      <div class="flex items-center gap-2">
        <button
          @click="startCreate"
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          New Article
        </button>
      </div>
    </div>

    <section class="grid grid-cols-1 xl:grid-cols-[1fr_0.85fr] gap-8">
      <div class="space-y-6">
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 class="text-xl font-semibold text-gray-900 mb-4">News articles</h2>
          <div class="space-y-4">
            <div v-if="loading" class="text-gray-500">Loading news articles…</div>
            <div v-else-if="articles.length === 0" class="text-gray-500">No news articles found.</div>
            <div v-else class="space-y-4">
              <div v-for="article in articles" :key="article.id" class="rounded-xl border border-gray-200 p-4 hover:shadow-sm transition">
                <div class="flex items-start justify-between gap-3">
                  <div>
                    <p class="text-sm text-gray-500">{{ article.status.toUpperCase() }} • {{ formatDate(article.created_at) }}</p>
                    <h3 class="text-lg font-semibold text-gray-900">{{ article.title }}</h3>
                    <p class="text-sm text-gray-600 mt-1">{{ article.excerpt || 'No excerpt available.' }}</p>
                  </div>
                  <div class="flex gap-2">
                    <button @click="editArticle(article)" class="px-3 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:bg-indigo-700">Edit</button>
                    <button @click="confirmDelete(article.id)" class="px-3 py-2 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700">Delete</button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">{{ isEditing ? 'Edit Article' : 'Create Article' }}</h2>

        <form @submit.prevent="submitForm" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Title</label>
            <input v-model="form.title" required class="w-full rounded-lg border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Excerpt</label>
            <textarea v-model="form.excerpt" rows="3" class="w-full rounded-lg border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Content</label>
            <textarea v-model="form.content" rows="6" required class="w-full rounded-lg border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500"></textarea>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Featured Image URL</label>
              <input v-model="form.featured_image_url" class="w-full rounded-lg border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Category</label>
              <select v-model="form.category_id" class="w-full rounded-lg border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500">
                <option value="">Uncategorized</option>
                <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
            <select v-model="form.status" class="w-full rounded-lg border-gray-300 shadow-sm focus:ring-blue-500 focus:border-blue-500">
              <option value="draft">Draft</option>
              <option value="published">Published</option>
              <option value="archived">Archived</option>
            </select>
          </div>

          <div class="flex gap-3">
            <button type="submit" class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">{{ isEditing ? 'Update' : 'Create' }}</button>
            <button type="button" @click="resetForm" class="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300">Reset</button>
          </div>
          <div v-if="error" class="text-sm text-red-700">{{ error }}</div>
          <div v-if="success" class="text-sm text-green-700">{{ success }}</div>
        </form>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import cmsService from '../../services/cms.service'

type NewsArticleForm = {
  id?: number
  title: string
  excerpt: string | null
  content: string
  featured_image_url: string | null
  category_id: number | ''
  status: 'draft' | 'published' | 'archived'
}

const articles = ref<Array<any>>([])
const categories = ref<Array<any>>([])
const loading = ref(false)
const isEditing = ref(false)
const error = ref('')
const success = ref('')
const form = ref<NewsArticleForm>({
  title: '',
  excerpt: '',
  content: '',
  featured_image_url: '',
  category_id: '',
  status: 'draft'
})

const loadArticles = async () => {
  loading.value = true
  try {
    const response = await cmsService.getNews({ page: 1, limit: 25 })
    articles.value = response.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const loadCategories = async () => {
  try {
    const response = await cmsService.getNewsCategories()
    categories.value = response.data
  } catch (err) {
    console.error(err)
  }
}

const startCreate = () => {
  isEditing.value = false
  form.value = {
    title: '',
    excerpt: '',
    content: '',
    featured_image_url: '',
    category_id: '',
    status: 'draft'
  }
  error.value = ''
  success.value = ''
}

const editArticle = (article: any) => {
  isEditing.value = true
  form.value = {
    id: article.id,
    title: article.title,
    excerpt: article.excerpt,
    content: article.content,
    featured_image_url: article.featured_image_url,
    category_id: article.category_id || '',
    status: article.status,
  }
  error.value = ''
  success.value = ''
}

const submitForm = async () => {
  error.value = ''
  success.value = ''

  try {
    if (isEditing.value && form.value.id) {
      await cmsService.updateNews(form.value.id, {
        title: form.value.title,
        excerpt: form.value.excerpt || undefined,
        content: form.value.content,
        featured_image_url: form.value.featured_image_url || undefined,
        category_id: form.value.category_id || undefined,
        status: form.value.status,
      })
      success.value = 'News article updated successfully.'
    } else {
      await cmsService.createNews({
        title: form.value.title,
        excerpt: form.value.excerpt || undefined,
        content: form.value.content,
        featured_image_url: form.value.featured_image_url || undefined,
        category_id: form.value.category_id || undefined,
        status: form.value.status,
      })
      success.value = 'News article created successfully.'
      startCreate()
    }
    await loadArticles()
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.response?.data?.message || 'Failed to save news article.'
  }
}

const confirmDelete = async (id: number) => {
  if (!window.confirm('Delete this article?')) {
    return
  }

  try {
    await cmsService.deleteNews(id)
    success.value = 'News article deleted successfully.'
    await loadArticles()
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.response?.data?.message || 'Failed to delete news article.'
  }
}

const resetForm = () => {
  startCreate()
}

const formatDate = (value: string) => {
  return new Date(value).toLocaleDateString()
}

onMounted(async () => {
  await Promise.all([loadArticles(), loadCategories()])
})
</script>
