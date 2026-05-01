<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-blue-900 to-blue-700 text-white py-16">
      <div class="container mx-auto px-4">
        <div class="text-center">
          <h1 class="text-4xl md:text-5xl font-bold mb-4">Photo Gallery</h1>
          <p class="text-xl text-blue-100 max-w-3xl mx-auto">
            Capturing precious moments and celebrating the vibrant life at Dalmia Vidya Mandir
          </p>
        </div>
      </div>
    </section>

    <!-- Filter Tabs -->
    <section class="py-8 bg-white sticky top-0 z-10 shadow-sm">
      <div class="container mx-auto px-4">
        <div class="flex flex-wrap justify-center gap-2 md:gap-4">
          <button
            v-for="category in categories"
            :key="category.id"
            @click="activeCategory = category.id"
            :class="[
              'px-4 py-2 rounded-full font-medium transition-all duration-200',
              activeCategory === category.id
                ? 'bg-blue-600 text-white shadow-md'
                : 'bg-gray-100 text-gray-700 hover:bg-blue-50 hover:text-blue-600'
            ]"
          >
            {{ category.name }}
          </button>
        </div>
      </div>
    </section>

    <!-- Gallery Albums -->
    <section class="py-12">
      <div class="container mx-auto px-4">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div
            v-for="album in filteredAlbums"
            :key="album.id"
            class="bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-xl transition-all duration-300 cursor-pointer group"
            @click="openAlbum(album)"
          >
            <!-- Album Cover -->
            <div class="relative h-64 overflow-hidden">
              <img
                :src="album.coverImage"
                :alt="album.title"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
              />
              <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent"></div>
              <div class="absolute bottom-4 left-4 right-4">
                <div class="flex items-center text-white text-sm mb-2">
                  <Calendar :size="16" class="mr-2" />
                  {{ album.date }}
                </div>
                <div class="flex items-center text-white text-sm">
                  <Image :size="16" class="mr-2" />
                  {{ album.photoCount }} Photos
                </div>
              </div>
            </div>

            <!-- Album Info -->
            <div class="p-6">
              <h3 class="text-xl font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
                {{ album.title }}
              </h3>
              <p class="text-gray-600 text-sm leading-relaxed">
                {{ album.description }}
              </p>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="filteredAlbums.length === 0" class="text-center py-16">
          <Image :size="64" class="mx-auto text-gray-300 mb-4" />
          <h3 class="text-xl font-semibold text-gray-500 mb-2">No albums found</h3>
          <p class="text-gray-400">Check back soon for more photos!</p>
        </div>
      </div>
    </section>

    <!-- Album Modal -->
    <div
      v-if="selectedAlbum"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/90"
      @click="closeAlbum"
    >
      <div class="relative w-full h-full max-w-6xl mx-4 flex flex-col">
        <!-- Modal Header -->
        <div class="flex items-center justify-between p-6 text-white">
          <div>
            <h2 class="text-2xl font-bold">{{ selectedAlbum.title }}</h2>
            <p class="text-gray-300">{{ selectedAlbum.date }}</p>
          </div>
          <button
            @click="closeAlbum"
            class="p-2 hover:bg-white/10 rounded-full transition-colors"
          >
            <X :size="24" />
          </button>
        </div>

        <!-- Photo Grid -->
        <div class="flex-1 overflow-y-auto p-6">
          <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            <div
              v-for="(photo, index) in selectedAlbum.photos"
              :key="index"
              class="aspect-square bg-gray-800 rounded-lg overflow-hidden cursor-pointer hover:opacity-80 transition-opacity"
              @click="openLightbox(index)"
            >
              <img
                :src="photo.thumbnail || photo.url"
                :alt="photo.caption"
                class="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Lightbox -->
    <div
      v-if="lightboxIndex !== null && selectedAlbum"
      class="fixed inset-0 z-60 flex items-center justify-center bg-black"
      @click="closeLightbox"
    >
      <button
        @click="previousPhoto"
        class="absolute left-4 top-1/2 transform -translate-y-1/2 text-white p-3 hover:bg-white/10 rounded-full transition-colors"
        :disabled="lightboxIndex === 0"
      >
        <ChevronLeft :size="24" />
      </button>

      <div class="relative max-w-5xl max-h-full mx-4 flex flex-col">
        <img
          :src="selectedAlbum.photos[lightboxIndex].url"
          :alt="selectedAlbum.photos[lightboxIndex].caption"
          class="max-w-full max-h-[80vh] object-contain"
        />
        <div v-if="selectedAlbum.photos[lightboxIndex].caption" class="text-center text-white mt-4">
          <p class="text-lg">{{ selectedAlbum.photos[lightboxIndex].caption }}</p>
        </div>
      </div>

      <button
        @click="nextPhoto"
        class="absolute right-4 top-1/2 transform -translate-y-1/2 text-white p-3 hover:bg-white/10 rounded-full transition-colors"
        :disabled="lightboxIndex === selectedAlbum.photos.length - 1"
      >
        <ChevronRight :size="24" />
      </button>

      <button
        @click="closeLightbox"
        class="absolute top-4 right-4 text-white p-3 hover:bg-white/10 rounded-full transition-colors"
      >
        <X :size="24" />
      </button>

      <div class="absolute bottom-4 left-1/2 transform -translate-x-1/2 text-white">
        <span class="text-sm">{{ lightboxIndex + 1 }} of {{ selectedAlbum.photos.length }}</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { Calendar, Image, X, ChevronLeft, ChevronRight } from 'lucide-vue-next'

interface Photo {
  url: string
  thumbnail?: string
  caption?: string
}

interface Album {
  id: number
  title: string
  description: string
  coverImage: string
  date: string
  photoCount: number
  category: string
  photos: Photo[]
}

interface Category {
  id: string
  name: string
}

const activeCategory = ref('all')
const selectedAlbum = ref<Album | null>(null)
const lightboxIndex = ref<number | null>(null)

const categories: Category[] = [
  { id: 'all', name: 'All Albums' },
  { id: 'events', name: 'School Events' },
  { id: 'academics', name: 'Academic Activities' },
  { id: 'sports', name: 'Sports & Games' },
  { id: 'cultural', name: 'Cultural Programs' },
  { id: 'achievements', name: 'Achievements' },
  { id: 'infrastructure', name: 'Infrastructure' }
]

// Sample album data (replace with actual API data)
const albums = ref<Album[]>([
  {
    id: 1,
    title: 'Annual Day Celebration 2024',
    description: 'A grand celebration showcasing student talents through dance, drama, and cultural performances.',
    coverImage: '/images/slide1.jpg',
    date: 'December 15, 2024',
    photoCount: 45,
    category: 'cultural',
    photos: [
      { url: '/images/slide1.jpg', caption: 'Opening ceremony with traditional dance' },
      { url: '/images/slide2.jpg', caption: 'Students performing classical music' },
      { url: '/images/slide3.jpg', caption: 'Drama presentation by Class 8 students' },
      { url: '/images/slide4.jpg', caption: 'Award ceremony for outstanding performers' }
    ]
  },
  {
    id: 2,
    title: 'Science Exhibition 2024',
    description: 'Students showcasing innovative science projects and experiments across various disciplines.',
    coverImage: '/images/slide2.jpg',
    date: 'November 20, 2024',
    photoCount: 32,
    category: 'academics',
    photos: [
      { url: '/images/slide2.jpg', caption: 'Physics experiments demonstration' },
      { url: '/images/slide3.jpg', caption: 'Chemistry lab projects display' },
      { url: '/images/slide4.jpg', caption: 'Biology models and charts' },
      { url: '/images/slide1.jpg', caption: 'Award winners with their projects' }
    ]
  },
  {
    id: 3,
    title: 'Inter-House Sports Meet',
    description: 'Exciting sports competitions bringing together all four houses in friendly rivalry.',
    coverImage: '/images/slide3.jpg',
    date: 'October 8-10, 2024',
    photoCount: 68,
    category: 'sports',
    photos: [
      { url: '/images/slide3.jpg', caption: 'Track and field events' },
      { url: '/images/slide4.jpg', caption: 'Basketball championship finals' },
      { url: '/images/slide1.jpg', caption: 'Victory ceremony with house captains' },
      { url: '/images/slide2.jpg', caption: 'Football match highlights' }
    ]
  },
  {
    id: 4,
    title: 'Republic Day Parade 2024',
    description: 'Patriotic celebration with march past, cultural programs, and flag hoisting ceremony.',
    coverImage: '/images/slide4.jpg',
    date: 'January 26, 2024',
    photoCount: 28,
    category: 'events',
    photos: [
      { url: '/images/slide4.jpg', caption: 'Flag hoisting ceremony' },
      { url: '/images/slide1.jpg', caption: 'Students in parade formation' },
      { url: '/images/slide2.jpg', caption: 'Cultural performance highlights' },
      { url: '/images/slide3.jpg', caption: 'Chief guest addressing students' }
    ]
  },
  {
    id: 5,
    title: 'New AV Room Installation',
    description: 'State-of-the-art Audio-Visual room setup for enhanced remote interactive learning.',
    coverImage: '/images/slide1.jpg',
    date: 'September 2024',
    photoCount: 15,
    category: 'infrastructure',
    photos: [
      { url: '/images/slide1.jpg', caption: 'Modern AV equipment installation' },
      { url: '/images/slide2.jpg', caption: 'Interactive whiteboard setup' },
      { url: '/images/slide3.jpg', caption: 'Students experiencing virtual learning' },
      { url: '/images/slide4.jpg', caption: 'Teacher conducting remote session' }
    ]
  },
  {
    id: 6,
    title: 'CBSE Topper Awards 2024',
    description: 'Celebrating our outstanding students who excelled in CBSE Board examinations.',
    coverImage: '/images/slide2.jpg',
    date: 'June 2024',
    photoCount: 22,
    category: 'achievements',
    photos: [
      { url: '/images/slide2.jpg', caption: 'CBSE toppers with their certificates' },
      { url: '/images/slide3.jpg', caption: 'Principal felicitating achievers' },
      { url: '/images/slide4.jpg', caption: 'Class 10 distinction holders' },
      { url: '/images/slide1.jpg', caption: 'Class 12 excellence awards' }
    ]
  }
])

const filteredAlbums = computed(() => {
  if (activeCategory.value === 'all') {
    return albums.value
  }
  return albums.value.filter(album => album.category === activeCategory.value)
})

const openAlbum = (album: Album) => {
  selectedAlbum.value = album
  document.body.style.overflow = 'hidden'
}

const closeAlbum = () => {
  selectedAlbum.value = null
  lightboxIndex.value = null
  document.body.style.overflow = 'auto'
}

const openLightbox = (index: number) => {
  lightboxIndex.value = index
}

const closeLightbox = () => {
  lightboxIndex.value = null
}

const previousPhoto = () => {
  if (lightboxIndex.value !== null && lightboxIndex.value > 0) {
    lightboxIndex.value--
  }
}

const nextPhoto = () => {
  if (lightboxIndex.value !== null && selectedAlbum.value && lightboxIndex.value < selectedAlbum.value.photos.length - 1) {
    lightboxIndex.value++
  }
}

// Keyboard navigation
const handleKeydown = (event: KeyboardEvent) => {
  if (lightboxIndex.value !== null) {
    switch (event.key) {
      case 'ArrowLeft':
        previousPhoto()
        break
      case 'ArrowRight':
        nextPhoto()
        break
      case 'Escape':
        closeLightbox()
        break
    }
  } else if (selectedAlbum.value && event.key === 'Escape') {
    closeAlbum()
  }
}

onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
  document.body.style.overflow = 'auto'
})
</script>
