<template>
  <section class="py-20 bg-white relative">
    <!-- Background Pattern -->
    <div class="absolute inset-0 opacity-5">
      <div class="absolute inset-0 bg-gray-100"></div>
    </div>

    <div class="container mx-auto px-4 relative">
      <!-- Section Header -->
      <div class="text-center mb-16">
        <div class="inline-block px-6 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-semibold tracking-wide uppercase mb-4">
          Educational Philosophy
        </div>
        <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
          Our Foundation 
          <span class="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Articles
          </span>
        </h2>
        <p class="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
          Discover the core principles that guide our educational approach and transform lives
        </p>
        <div class="w-24 h-1 bg-gradient-to-r from-blue-600 to-purple-600 mx-auto mt-6 rounded-full"></div>
      </div>

      <!-- Articles Grid -->
      <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-7xl mx-auto">
        <!-- Article 1: Standard of Life -->
        <router-link 
          to="/standard-of-life"
          class="group bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-blue-100 hover:border-blue-200"
        >
          <div class="flex flex-col h-full">
            <div class="flex items-center justify-center w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl mb-6 group-hover:scale-110 transition-transform duration-300">
              <TrendingUp :size="28" class="text-white" />
            </div>
            
            <h3 class="text-xl font-bold text-gray-900 mb-4 group-hover:text-blue-600 transition-colors">
              Standard of Life
            </h3>
            
            <p class="text-gray-600 text-sm leading-relaxed mb-6 flex-grow">
              Beyond material wealth lies a deeper pursuit—cultivating values, resilience, and purpose that define true success.
            </p>
            
            <div class="flex items-center text-blue-600 text-sm font-semibold group-hover:text-blue-700">
              <span>Read More</span>
              <ArrowRight :size="16" class="ml-2 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </router-link>

        <!-- Article 2: Conceptual Learning -->
        <router-link 
          to="/conceptual-learning"
          class="group bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-purple-100 hover:border-purple-200"
        >
          <div class="flex flex-col h-full">
            <div class="flex items-center justify-center w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl mb-6 group-hover:scale-110 transition-transform duration-300">
              <Lightbulb :size="28" class="text-white" />
            </div>
            
            <h3 class="text-xl font-bold text-gray-900 mb-4 group-hover:text-purple-600 transition-colors">
              Conceptual Learning
            </h3>
            
            <p class="text-gray-600 text-sm leading-relaxed mb-6 flex-grow">
              Transforming passive absorption into active understanding—where students become creators of meaning and knowledge.
            </p>
            
            <div class="flex items-center text-purple-600 text-sm font-semibold group-hover:text-purple-700">
              <span>Read More</span>
              <ArrowRight :size="16" class="ml-2 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </router-link>

        <!-- Article 3: Fine Arts -->
        <router-link 
          to="/fine-arts"
          class="group bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-orange-100 hover:border-orange-200"
        >
          <div class="flex flex-col h-full">
            <div class="flex items-center justify-center w-16 h-16 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl mb-6 group-hover:scale-110 transition-transform duration-300">
              <Palette :size="28" class="text-white" />
            </div>
            
            <h3 class="text-xl font-bold text-gray-900 mb-4 group-hover:text-orange-600 transition-colors">
              Fine Arts Integration
            </h3>
            
            <p class="text-gray-600 text-sm leading-relaxed mb-6 flex-grow">
              From STEM to STEAM—nurturing creativity, emotional intelligence, and cultural awareness through artistic expression.
            </p>
            
            <div class="flex items-center text-orange-600 text-sm font-semibold group-hover:text-orange-700">
              <span>Read More</span>
              <ArrowRight :size="16" class="ml-2 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </router-link>

        <!-- Article 4: Sports Excellence -->
        <router-link 
          to="/sports-excellence"
          class="group bg-gradient-to-br from-green-50 to-teal-50 rounded-2xl p-8 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-green-100 hover:border-green-200"
        >
          <div class="flex flex-col h-full">
            <div class="flex items-center justify-center w-16 h-16 bg-gradient-to-r from-green-500 to-teal-500 rounded-xl mb-6 group-hover:scale-110 transition-transform duration-300">
              <Trophy :size="28" class="text-white" />
            </div>
            
            <h3 class="text-xl font-bold text-gray-900 mb-4 group-hover:text-green-600 transition-colors">
              Sports Excellence
            </h3>
            
            <p class="text-gray-600 text-sm leading-relaxed mb-6 flex-grow">
              Beyond academics—where champions are forged through discipline, teamwork, and the pursuit of athletic greatness.
            </p>
            
            <div class="flex items-center text-green-600 text-sm font-semibold group-hover:text-green-700">
              <span>Read More</span>
              <ArrowRight :size="16" class="ml-2 group-hover:translate-x-1 transition-transform" />
            </div>
          </div>
        </router-link>
      </div>

      <!-- Bottom CTA -->
      <div class="text-center mt-16">
        <div class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105">
          <BookOpen :size="20" class="mr-3" />
          <span class="font-semibold">Explore Our Complete Philosophy</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { 
  TrendingUp, 
  Lightbulb, 
  Palette, 
  Trophy, 
  ArrowRight, 
  BookOpen 
} from 'lucide-vue-next'
</script>
