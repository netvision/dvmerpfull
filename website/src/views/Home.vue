<template>
  <div class="home">
    <Hero />
    
    <!-- Main Content with Sidebar Layout -->
    <div class="bg-gray-50 min-h-screen">
      <div class="container mx-auto px-4 py-6">
        <div class="grid lg:grid-cols-4 gap-6 overflow-hidden">
          <!-- Main Content Area -->
          <div class="lg:col-span-3 overflow-hidden">
            <div class="space-y-6">
              <Vision />
              <Features />
            </div>
          </div>
          
          <!-- Sidebar -->
          <div class="lg:col-span-1">
            <div class="sticky top-6 space-y-4">
              <!-- Sidebar Header -->
              <div class="bg-white rounded-xl shadow-md border border-gray-200 p-4">
                <h2 class="text-lg font-bold text-gray-900 mb-1 flex items-center">
                  <div class="w-2.5 h-2.5 bg-blue-500 rounded-full mr-2"></div>
                  Latest Updates
                </h2>
                <p class="text-gray-600 text-xs">Stay informed with our latest news and upcoming events</p>
              </div>
              
              <AchieversSlider />
              <NewsSidebar />
              <EventsSidebar />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Hero from '../components/Hero.vue'
import Vision from '../components/Vision.vue'
import Features from '../components/Features.vue'
import AchieversSlider from '../components/AchieversSlider.vue'
import NewsSidebar from '../components/NewsSidebar.vue'
import EventsSidebar from '../components/EventsSidebar.vue'
</script>
