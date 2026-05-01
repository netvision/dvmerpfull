<template>
  <div class="p-8 space-y-8">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div>
        <h1 class="text-3xl font-bold text-gray-900">Event Management</h1>
        <p class="text-gray-600">Manage website event listings and scheduling details.</p>
      </div>
      <button @click="startCreate" class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition">New Event</button>
    </div>

    <section class="grid grid-cols-1 xl:grid-cols-[1fr_0.9fr] gap-8">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">Events</h2>
        <div v-if="loading" class="text-gray-500">Loading events…</div>
        <div v-else-if="events.length === 0" class="text-gray-500">No events available.</div>
        <div v-else class="space-y-4">
          <div v-for="event in events" :key="event.id" class="rounded-xl border border-gray-200 p-4 hover:shadow-sm transition">
            <div class="flex items-start justify-between gap-3">
              <div>
                <p class="text-sm text-gray-500">{{ event.status.toUpperCase() }} • {{ formatDate(event.start_date) }} - {{ formatDate(event.end_date) }}</p>
                <h3 class="text-lg font-semibold text-gray-900">{{ event.title }}</h3>
                <p class="text-sm text-gray-600 mt-1">{{ event.location || 'Location not specified' }}</p>
              </div>
              <div class="flex gap-2">
                <button @click="editEvent(event)" class="px-3 py-2 bg-indigo-600 text-white rounded-lg text-sm hover:bg-indigo-700">Edit</button>
                <button @click="confirmDelete(event.id)" class="px-3 py-2 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700">Delete</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 class="text-xl font-semibold text-gray-900 mb-4">{{ isEditing ? 'Edit Event' : 'Create Event' }}</h2>
        <form @submit.prevent="submitForm" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Title</label>
            <input v-model="form.title" required class="w-full rounded-lg border-gray-300 shadow-sm focus:ring-green-500 focus:border-green-500" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Description</label>
            <textarea v-model="form.description" rows="3" class="w-full rounded-lg border-gray-300 shadow-sm focus:ring-green-500 focus:border-green-500"></textarea>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Location</label>
            <input v-model="form.location" class="w-full rounded-lg border-gray-300 shadow-sm focus:ring-green-500 focus:border-green-500" />
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">Start Date</label>
              <input type="date" v-model="form.start_date" required class="w-full rounded-lg border-gray-300 shadow-sm focus:ring-green-500 focus:border-green-500" />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-2">End Date</label>
              <input type="date" v-model="form.end_date" required class="w-full rounded-lg border-gray-300 shadow-sm focus:ring-green-500 focus:border-green-500" />
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Featured Image URL</label>
            <input v-model="form.featured_image_url" class="w-full rounded-lg border-gray-300 shadow-sm focus:ring-green-500 focus:border-green-500" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Capacity</label>
            <input type="number" min="0" v-model.number="form.capacity" class="w-full rounded-lg border-gray-300 shadow-sm focus:ring-green-500 focus:border-green-500" />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Status</label>
            <select v-model="form.status" class="w-full rounded-lg border-gray-300 shadow-sm focus:ring-green-500 focus:border-green-500">
              <option value="upcoming">Upcoming</option>
              <option value="ongoing">Ongoing</option>
              <option value="completed">Completed</option>
              <option value="cancelled">Cancelled</option>
            </select>
          </div>

          <div class="flex gap-3">
            <button type="submit" class="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">{{ isEditing ? 'Update' : 'Create' }}</button>
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

type EventForm = {
  id?: number
  title: string
  description: string | null
  location: string | null
  start_date: string
  end_date: string
  featured_image_url: string | null
  capacity: number | null
  status: 'upcoming' | 'ongoing' | 'completed' | 'cancelled'
}

const events = ref<Array<any>>([])
const loading = ref(false)
const isEditing = ref(false)
const error = ref('')
const success = ref('')
const form = ref<EventForm>({
  title: '',
  description: '',
  location: '',
  start_date: new Date().toISOString().slice(0, 10),
  end_date: new Date().toISOString().slice(0, 10),
  featured_image_url: '',
  capacity: null,
  status: 'upcoming'
})

const loadEvents = async () => {
  loading.value = true
  try {
    const response = await cmsService.getEvents({ page: 1, limit: 25 })
    events.value = response.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

const startCreate = () => {
  isEditing.value = false
  form.value = {
    title: '',
    description: '',
    location: '',
    start_date: new Date().toISOString().slice(0, 10),
    end_date: new Date().toISOString().slice(0, 10),
    featured_image_url: '',
    capacity: null,
    status: 'upcoming'
  }
  error.value = ''
  success.value = ''
}

const editEvent = (event: any) => {
  isEditing.value = true
  form.value = {
    id: event.id,
    title: event.title,
    description: event.description,
    location: event.location,
    start_date: event.start_date,
    end_date: event.end_date,
    featured_image_url: event.featured_image_url,
    capacity: event.capacity,
    status: event.status,
  }
  error.value = ''
  success.value = ''
}

const submitForm = async () => {
  error.value = ''
  success.value = ''

  try {
    if (isEditing.value && form.value.id) {
      await cmsService.updateEvent(form.value.id, {
        title: form.value.title,
        description: form.value.description || undefined,
        location: form.value.location || undefined,
        start_date: form.value.start_date,
        end_date: form.value.end_date,
        featured_image_url: form.value.featured_image_url || undefined,
        capacity: form.value.capacity ?? undefined,
        status: form.value.status,
      })
      success.value = 'Event updated successfully.'
    } else {
      await cmsService.createEvent({
        title: form.value.title,
        description: form.value.description || undefined,
        location: form.value.location || undefined,
        start_date: form.value.start_date,
        end_date: form.value.end_date,
        featured_image_url: form.value.featured_image_url || undefined,
        capacity: form.value.capacity ?? undefined,
        status: form.value.status,
      })
      success.value = 'Event created successfully.'
      startCreate()
    }
    await loadEvents()
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.response?.data?.message || 'Failed to save event.'
  }
}

const confirmDelete = async (id: number) => {
  if (!window.confirm('Delete this event?')) {
    return
  }

  try {
    await cmsService.deleteEvent(id)
    success.value = 'Event deleted successfully.'
    await loadEvents()
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.response?.data?.message || 'Failed to delete event.'
  }
}

const resetForm = () => {
  startCreate()
}

const formatDate = (value: string) => {
  return new Date(value).toLocaleDateString()
}

onMounted(loadEvents)
</script>
