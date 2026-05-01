import apiClient from '../config/api'

export interface NewsArticle {
  id: number
  title: string
  slug: string
  excerpt: string | null
  content: string
  featured_image_url: string | null
  author_id: number
  status: 'draft' | 'published' | 'archived'
  views: number
  published_at: string | null
  created_at: string
  updated_at: string
  category_id?: number | null
  category_name?: string | null
  gallery?: Array<{
    id: number
    image_url: string
    caption?: string | null
    display_order: number
  }>
}

export interface Event {
  id: number
  title: string
  slug: string
  description: string | null
  location: string | null
  start_date: string
  end_date: string
  featured_image_url: string | null
  organizer_id: number
  capacity: number | null
  registered_count: number
  status: 'upcoming' | 'ongoing' | 'completed' | 'cancelled'
  created_at: string
  updated_at: string
  gallery?: Array<{
    id: number
    image_url: string
    caption?: string | null
    display_order: number
  }>
}

export interface NewsCategory {
  id: number
  name: string
  slug: string
  description?: string | null
  created_at: string
  updated_at: string
}

export interface PaginatedResponse<T> {
  success: boolean
  data: T[]
  pagination: {
    page: number
    limit: number
    total: number
    pages: number
  }
}

export interface SingleResponse<T> {
  success: boolean
  data: T
}

class CMSService {
  // News endpoints
  async getNews(params?: {
    page?: number
    limit?: number
    status?: string
    search?: string
    category_id?: string
  }): Promise<PaginatedResponse<NewsArticle>> {
    const response = await apiClient.get('/cms/news', { params })
    return response.data
  }

  async getNewsBySlug(slug: string): Promise<SingleResponse<NewsArticle>> {
    const response = await apiClient.get(`/cms/news/${slug}`)
    return response.data
  }

  async createNews(data: {
    title: string
    excerpt?: string
    content: string
    featured_image_url?: string
    category_id?: number
    status?: 'draft' | 'published' | 'archived'
  }): Promise<SingleResponse<NewsArticle>> {
    const response = await apiClient.post('/cms/news', data)
    return response.data
  }

  async updateNews(
    id: number,
    data: Partial<{
      title: string
      excerpt: string
      content: string
      featured_image_url: string
      category_id: number
      status: 'draft' | 'published' | 'archived'
    }>
  ): Promise<SingleResponse<NewsArticle>> {
    const response = await apiClient.put(`/cms/news/${id}`, data)
    return response.data
  }

  async deleteNews(id: number): Promise<{ success: boolean; message: string }> {
    const response = await apiClient.delete(`/cms/news/${id}`)
    return response.data
  }

  // Events endpoints
  async getEvents(params?: {
    page?: number
    limit?: number
    status?: string
    upcoming?: boolean
    search?: string
  }): Promise<PaginatedResponse<Event>> {
    const response = await apiClient.get('/cms/events', { params })
    return response.data
  }

  async getEventBySlug(slug: string): Promise<SingleResponse<Event>> {
    const response = await apiClient.get(`/cms/events/${slug}`)
    return response.data
  }

  async createEvent(data: {
    title: string
    description?: string
    location?: string
    start_date: string
    end_date: string
    featured_image_url?: string
    capacity?: number
    status?: 'upcoming' | 'ongoing' | 'completed' | 'cancelled'
  }): Promise<SingleResponse<Event>> {
    const response = await apiClient.post('/cms/events', data)
    return response.data
  }

  async updateEvent(
    id: number,
    data: Partial<{
      title: string
      description: string
      location: string
      start_date: string
      end_date: string
      featured_image_url: string
      capacity: number
      status: 'upcoming' | 'ongoing' | 'completed' | 'cancelled'
    }>
  ): Promise<SingleResponse<Event>> {
    const response = await apiClient.put(`/cms/events/${id}`, data)
    return response.data
  }

  async deleteEvent(id: number): Promise<{ success: boolean; message: string }> {
    const response = await apiClient.delete(`/cms/events/${id}`)
    return response.data
  }

  // Category endpoints
  async getNewsCategories(): Promise<SingleResponse<NewsCategory[]>> {
    const response = await apiClient.get('/cms/categories')
    return response.data
  }
}

export default new CMSService()
