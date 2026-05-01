<template>
  <!-- Vision Section -->
  <section class="py-8 bg-white rounded-xl shadow-md border border-gray-200 mb-6 relative overflow-hidden">
    <!-- Background decorative elements -->
    <div class="absolute inset-0 overflow-hidden">
      <div class="absolute -top-40 -right-40 w-80 h-80 rounded-full bg-gradient-to-br from-blue-200/20 to-purple-200/20 blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 rounded-full bg-gradient-to-tr from-yellow-200/20 to-orange-200/20 blur-3xl"></div>
    </div>

    <div class="container mx-auto px-4 relative overflow-hidden">
      <!-- Section Header -->
      <div class="text-center mb-8">
        <div class="inline-block px-4 py-1.5 bg-blue-100 text-blue-800 rounded-full text-xs font-semibold tracking-wide uppercase mb-3">
          Our Vision
        </div>
        <div class="w-20 h-0.5 bg-gradient-to-r from-blue-600 to-purple-600 mx-auto rounded-full"></div>
      </div>

      <!-- Main Vision Content -->
      <div class="max-w-full mx-auto overflow-hidden">
        <!-- Integrated Core Section -->
        <div class="bg-white/70 backdrop-blur-sm rounded-xl p-5 shadow-lg border border-white/50 mb-6 text-center">
          <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
            From Higher Standard of Living to 
            <span class="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              Higher Standard of Life
            </span>
          </h2>
          
          <p class="text-lg text-gray-600 mb-6 leading-relaxed">
            We believe true education empowers students to <strong class="text-blue-600">rise above their circumstances</strong> 
            with clarity, resilience, and purpose—transforming them into <strong class="text-purple-600">active creators of meaning</strong>.
          </p>

          <!-- Three Core Values in One Row -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
            <div class="flex flex-col items-center p-1">
              <div class="w-14 h-14 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mb-2 transform transition-transform hover:scale-105">
                <GraduationCap :size="20" class="text-white" />
              </div>
              <h4 class="font-bold text-gray-800 text-xs">Academic Excellence</h4>
            </div>
            <div class="flex flex-col items-center p-1">
              <div class="w-14 h-14 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mb-2 transform transition-transform hover:scale-105">
                <Music :size="20" class="text-white" />
              </div>
              <h4 class="font-bold text-gray-800 text-xs">Artistic Expression</h4>
            </div>
            <div class="flex flex-col items-center p-1">
              <div class="w-14 h-14 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-center mb-2 transform transition-transform hover:scale-105">
                <Zap :size="20" class="text-white" />
              </div>
              <h4 class="font-bold text-gray-800 text-xs">Athletic Achievement</h4>
            </div>
          </div>

          <router-link 
            to="/vision"
            class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full font-semibold hover:shadow-lg transition-all duration-300 transform hover:scale-105 no-underline"
          >
            <span>Explore Our Complete Vision</span>
            <ArrowRight :size="20" class="ml-3" />
          </router-link>
        </div>

        <!-- Sacred Mission Section -->
        <div class="bg-gradient-to-r from-orange-600 to-red-600 rounded-xl p-8 text-white text-center shadow-xl">
          <div class="flex items-center justify-center mb-4">
            <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center backdrop-blur-sm">
              <BookOpen :size="24" class="text-white" />
            </div>
            <h2 class="text-2xl md:text-3xl font-bold ml-3">Our Sacred Mission</h2>
          </div>
          
          <blockquote class="text-xl md:text-2xl font-medium italic text-orange-100 mb-6">
            "सत्त्वसंशुद्धिर्ज्ञानयोगव्यवस्थितिः"
          </blockquote>
          
          <p class="text-lg mb-8 leading-relaxed">
            Inspired by the divine qualities of Bhagavad Gita, we cultivate 
            <strong class="text-yellow-200">fearlessness, truthfulness, compassion, and wisdom</strong> 
            in every student—transforming education into character formation.
          </p>

          <router-link 
            to="/mission"
            class="inline-flex items-center px-8 py-4 bg-white text-orange-600 rounded-full font-semibold hover:shadow-lg transition-all duration-300 transform hover:scale-105 no-underline"
          >
            <span>Discover Our Sacred Mission</span>
            <ArrowRight :size="20" class="ml-3" />
          </router-link>
        </div>
      </div>
    </div>
  </section>

  <!-- Foundational Articles Section -->
  <section class="py-8 bg-gradient-to-br from-gray-50 to-blue-50 rounded-xl shadow-md border border-gray-200 overflow-hidden">
    <div class="container mx-auto px-4 relative">
      <!-- Section Header -->
      <div class="text-center mb-8">
        <div class="inline-block px-4 py-1.5 bg-purple-100 text-purple-800 rounded-full text-xs font-semibold tracking-wide uppercase mb-3">
          Educational Foundation
        </div>
        <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
          Foundational 
          <span class="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
            Articles
          </span>
        </h2>
        <p class="text-lg text-gray-600 max-w-3xl mx-auto leading-relaxed">
          Discover the core principles that guide our educational approach and philosophy
        </p>
        <div class="w-20 h-0.5 bg-gradient-to-r from-purple-600 to-blue-600 mx-auto mt-4 rounded-full"></div>
      </div>

      <!-- Articles Grid -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 overflow-hidden px-1">
        <!-- Article 1: Standard of Life -->
        <router-link 
          to="/standard-of-life"
          class="group bg-gradient-to-br from-blue-50 to-indigo-100 rounded-xl p-4 shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-blue-200 hover:border-blue-300 no-underline max-w-full"
        >
          <div class="flex flex-col h-full">
            <div class="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg mb-3 transform transition-transform duration-300 group-hover:scale-105">
              <TrendingUp :size="18" class="text-white" />
            </div>
            
            <h4 class="text-base font-bold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">
              Standard of Life
            </h4>
            
            <p class="text-gray-600 text-xs leading-relaxed mb-3 flex-grow">
              Beyond material wealth lies a deeper pursuit—cultivating values, resilience, and purpose.
            </p>
            
            <div class="flex items-center text-blue-600 text-xs font-semibold group-hover:text-blue-700">
              <span>Read More</span>
              <ArrowRight :size="12" class="ml-2 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </router-link>

        <!-- Article 2: Conceptual Learning -->
        <router-link 
          to="/conceptual-learning"
          class="group bg-gradient-to-br from-purple-50 to-pink-100 rounded-xl p-4 shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-purple-200 hover:border-purple-300 no-underline max-w-full"
        >
          <div class="flex flex-col h-full">
            <div class="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg mb-3 transform transition-transform duration-300 group-hover:scale-105">
              <Lightbulb :size="18" class="text-white" />
            </div>
            
            <h4 class="text-base font-bold text-gray-900 mb-2 group-hover:text-purple-600 transition-colors">
              Conceptual Learning
            </h4>
            
            <p class="text-gray-600 text-xs leading-relaxed mb-3 flex-grow">
              Transforming passive absorption into active understanding—where students become creators of meaning.
            </p>
            
            <div class="flex items-center text-purple-600 text-xs font-semibold group-hover:text-purple-700">
              <span>Read More</span>
              <ArrowRight :size="12" class="ml-2 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </router-link>

        <!-- Article 3: Fine Arts -->
        <router-link 
          to="/fine-arts"
          class="group bg-gradient-to-br from-orange-50 to-red-100 rounded-xl p-4 shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-orange-200 hover:border-orange-300 no-underline max-w-full"
        >
          <div class="flex flex-col h-full">
            <div class="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-orange-500 to-red-500 rounded-lg mb-3 transform transition-transform duration-300 group-hover:scale-105">
              <Palette :size="18" class="text-white" />
            </div>
            
            <h4 class="text-base font-bold text-gray-900 mb-2 group-hover:text-orange-600 transition-colors">
              Fine Arts Integration
            </h4>
            
            <p class="text-gray-600 text-xs leading-relaxed mb-3 flex-grow">
              From STEM to STEAM—nurturing creativity, emotional intelligence, and cultural awareness.
            </p>
            
            <div class="flex items-center text-orange-600 text-xs font-semibold group-hover:text-orange-700">
              <span>Read More</span>
              <ArrowRight :size="12" class="ml-2 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </router-link>

        <!-- Article 4: Sports Excellence -->
        <router-link 
          to="/sports-excellence"
          class="group bg-gradient-to-br from-green-50 to-emerald-100 rounded-xl p-4 shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-green-200 hover:border-green-300 no-underline max-w-full"
        >
          <div class="flex flex-col h-full">
            <div class="flex items-center justify-center w-12 h-12 bg-gradient-to-r from-green-500 to-teal-500 rounded-lg mb-3 transform transition-transform duration-300 group-hover:scale-105">
              <Trophy :size="18" class="text-white" />
            </div>
            
            <h4 class="text-base font-bold text-gray-900 mb-2 group-hover:text-green-600 transition-colors">
              Sports Excellence
            </h4>
            
            <p class="text-gray-600 text-xs leading-relaxed mb-3 flex-grow">
              Beyond academics—where champions are forged through discipline, teamwork, and athletic greatness.
            </p>
            
            <div class="flex items-center text-green-600 text-xs font-semibold group-hover:text-green-700">
              <span>Read More</span>
              <ArrowRight :size="12" class="ml-2 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { 
  GraduationCap, 
  Music, 
  Zap,
  TrendingUp,
  ArrowRight,
  Lightbulb,
  Palette,
  Trophy,
  BookOpen
} from 'lucide-vue-next'
</script>

<style scoped>
.prose p strong {
  font-weight: 600;
}

/* Remove underline from router-links */
.no-underline {
  text-decoration: none !important;
}

.no-underline:hover {
  text-decoration: none !important;
}

/* Line clamp utility */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-1 {
  display: -webkit-box;
  -webkit-line-clamp: 1;
  line-clamp: 1;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
