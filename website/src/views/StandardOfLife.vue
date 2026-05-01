<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-blue-900 via-blue-800 to-purple-900 text-white py-20">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto text-center">
          <div class="inline-block px-6 py-2 bg-white/20 rounded-full text-sm font-semibold tracking-wide uppercase mb-6">
            Philosophy
          </div>
          <h1 class="text-4xl md:text-6xl font-bold mb-6">
            Beyond Circumstance: Cultivating the 
            <span class="bg-gradient-to-r from-yellow-300 to-orange-300 bg-clip-text text-transparent">
              Standard of Life
            </span>
          </h1>
          <p class="text-xl md:text-2xl text-blue-100 leading-relaxed">
            Redefining success by shifting focus from external achievements to internal growth
          </p>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <section class="py-16">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto">
          <!-- Introduction -->
          <div class="bg-white rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-blue-500 rounded-xl flex items-center justify-center mr-4">
                <Sprout :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">Introduction</h2>
            </div>
            <p class="text-lg text-gray-700 leading-relaxed mb-6">
              In today's fast-paced world, the pursuit of a higher standard of living—marked by material wealth, 
              comfort, and convenience—often overshadows the deeper quest for a meaningful life. At our school, 
              we redefine success by shifting the focus from external achievements to internal growth.
            </p>
            <p class="text-lg text-gray-700 leading-relaxed">
              We believe that true education empowers students to transcend their circumstances, fostering 
              emotional maturity, ethical decision-making, and a profound sense of purpose that extends far 
              beyond material gain.
            </p>
          </div>

          <!-- Core Philosophy -->
          <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center mr-4">
                <Compass :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">Core Philosophy</h2>
            </div>
            
            <div class="grid md:grid-cols-2 gap-8 mb-8">
              <div class="bg-white/70 rounded-xl p-6 shadow-lg">
                <h3 class="text-xl font-bold text-red-600 mb-4 flex items-center">
                  <TrendingDown :size="20" class="mr-2" />
                  Standard of Living
                </h3>
                <ul class="space-y-2 text-gray-700">
                  <li class="flex items-start">
                    <span class="w-2 h-2 bg-red-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                    Governed by circumstances and possessions
                  </li>
                  <li class="flex items-start">
                    <span class="w-2 h-2 bg-red-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                    Defined by social status and material wealth
                  </li>
                  <li class="flex items-start">
                    <span class="w-2 h-2 bg-red-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                    External validation and comparison
                  </li>
                </ul>
              </div>

              <div class="bg-white/70 rounded-xl p-6 shadow-lg">
                <h3 class="text-xl font-bold text-green-600 mb-4 flex items-center">
                  <TrendingUp :size="20" class="mr-2" />
                  Standard of Life
                </h3>
                <ul class="space-y-2 text-gray-700">
                  <li class="flex items-start">
                    <span class="w-2 h-2 bg-green-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                    Defined by values and resilience
                  </li>
                  <li class="flex items-start">
                    <span class="w-2 h-2 bg-green-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                    Purpose-driven and emotionally balanced
                  </li>
                  <li class="flex items-start">
                    <span class="w-2 h-2 bg-green-400 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                    Internal growth and self-awareness
                  </li>
                </ul>
              </div>
            </div>

            <div class="bg-white/70 rounded-xl p-6 shadow-lg">
              <h3 class="text-xl font-bold text-blue-600 mb-4">This Transformation Fosters:</h3>
              <div class="grid md:grid-cols-3 gap-4">
                <div class="text-center">
                  <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Heart :size="24" class="text-white" />
                  </div>
                  <h4 class="font-semibold text-gray-800">Emotional Maturity</h4>
                  <p class="text-sm text-gray-600">Self-awareness and empathy</p>
                </div>
                <div class="text-center">
                  <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Scale :size="24" class="text-white" />
                  </div>
                  <h4 class="font-semibold text-gray-800">Ethical Decision-Making</h4>
                  <p class="text-sm text-gray-600">Values-based choices</p>
                </div>
                <div class="text-center">
                  <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Target :size="24" class="text-white" />
                  </div>
                  <h4 class="font-semibold text-gray-800">Sense of Purpose</h4>
                  <p class="text-sm text-gray-600">Beyond material gain</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Practices We Embrace -->
          <div class="bg-white rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl flex items-center justify-center mr-4">
                <Users :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">Practices We Embrace</h2>
            </div>
            
            <div class="grid md:grid-cols-3 gap-8">
              <div class="text-center bg-gray-50 rounded-xl p-6">
                <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Brain :size="28" class="text-white" />
                </div>
                <h3 class="text-lg font-bold text-gray-800 mb-3">Mindfulness & Reflection</h3>
                <p class="text-gray-600 text-sm leading-relaxed">
                  Regular meditation sessions, reflective journaling, and mindfulness practices 
                  to develop self-awareness and emotional regulation.
                </p>
              </div>

              <div class="text-center bg-gray-50 rounded-xl p-6">
                <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <BookOpen :size="28" class="text-white" />
                </div>
                <h3 class="text-lg font-bold text-gray-800 mb-3">Value-Based Education</h3>
                <p class="text-gray-600 text-sm leading-relaxed">
                  Integrated life skills curriculum focusing on character development, 
                  ethical reasoning, and moral decision-making frameworks.
                </p>
              </div>

              <div class="text-center bg-gray-50 rounded-xl p-6">
                <div class="w-16 h-16 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <HandHeart :size="28" class="text-white" />
                </div>
                <h3 class="text-lg font-bold text-gray-800 mb-3">Community Service</h3>
                <p class="text-gray-600 text-sm leading-relaxed">
                  Active participation in community projects, gratitude initiatives, 
                  and social responsibility programs to foster empathy and purpose.
                </p>
              </div>
            </div>
          </div>

          <!-- Call to Action -->
          <div class="bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 md:p-12 text-white text-center">
            <h2 class="text-2xl md:text-3xl font-bold mb-4">
              Ready to Transform Lives?
            </h2>
            <p class="text-lg md:text-xl mb-8 text-blue-100">
              Join us in cultivating a higher standard of life, where students rise above circumstances 
              to become purposeful, resilient, and compassionate individuals.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <router-link 
                to="/admissions" 
                class="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-blue-50 transition-colors"
              >
                Learn About Admissions
              </router-link>
              <router-link 
                to="/contact" 
                class="bg-blue-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-400 transition-colors border border-blue-400"
              >
                Contact Us
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { 
  Sprout, 
  Compass, 
  TrendingDown, 
  TrendingUp, 
  Heart, 
  Scale, 
  Target, 
  Users, 
  Brain, 
  BookOpen, 
  HandHeart 
} from 'lucide-vue-next'
</script>
