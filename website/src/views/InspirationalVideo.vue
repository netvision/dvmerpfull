<template>
  <div class="inspirational-video-page">
    <!-- Hero Section -->
    <div class="relative h-64 bg-gradient-to-r from-purple-900 to-indigo-700">
      <div class="absolute inset-0 bg-black opacity-30"></div>
      <div class="container mx-auto px-4 h-full flex items-center relative z-10">
        <div class="text-white">
          <h1 class="text-5xl font-bold mb-4">Inspirational Video</h1>
          <p class="text-xl">Empowering minds, inspiring futures</p>
        </div>
      </div>
    </div>

    <!-- Video Section -->
    <div class="container mx-auto px-4 py-16">
      <div class="max-w-5xl mx-auto">
        <!-- Video Container -->
        <div class="bg-white rounded-lg shadow-2xl overflow-hidden mb-8">
          <div class="aspect-video w-full">
            <video 
              controls 
              class="w-full h-full object-contain bg-black"
              controlsList="nodownload"
            >
              <source src="/inspirational video.mp4" type="video/mp4">
              Your browser does not support the video tag.
            </video>
          </div>
        </div>

        <!-- Video Description -->
        <div class="bg-gray-50 rounded-lg p-8 shadow-md">
          <h2 class="text-2xl font-bold text-gray-800 mb-4">About This Video</h2>
          <p class="text-gray-700 leading-relaxed mb-4">
            This inspirational video showcases the spirit and values of our institution. 
            It captures the essence of our educational philosophy and the journey of our students 
            as they grow into confident, capable individuals ready to make a positive impact on the world.
          </p>
          <p class="text-gray-700 leading-relaxed">
            Through dedication, hard work, and the right guidance, every student can achieve their dreams. 
            Watch this video to understand our commitment to excellence and holistic development.
          </p>
        </div>

        <!-- Call to Action -->
        <div class="mt-12 text-center">
          <h3 class="text-2xl font-bold text-gray-800 mb-6">Join Our Community</h3>
          <div class="flex flex-wrap justify-center gap-4">
            <router-link 
              to="/admissions" 
              class="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-semibold"
            >
              Apply for Admission
            </router-link>
            <router-link 
              to="/contact" 
              class="px-8 py-3 bg-gray-200 text-gray-800 rounded-lg hover:bg-gray-300 transition-colors font-semibold"
            >
              Contact Us
            </router-link>
          </div>
        </div>
      </div>
    </div>

    <!-- Related Links Section -->
    <div class="bg-gray-100 py-16">
      <div class="container mx-auto px-4">
        <h3 class="text-3xl font-bold text-center text-gray-800 mb-12">Explore More</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          <router-link 
            to="/about" 
            class="bg-white rounded-lg p-6 shadow-md hover:shadow-xl transition-shadow"
          >
            <div class="text-blue-600 mb-3">
              <i class="i-lucide-info text-4xl"></i>
            </div>
            <h4 class="text-xl font-bold text-gray-800 mb-2">About Us</h4>
            <p class="text-gray-600">Learn about our rich heritage and educational philosophy</p>
          </router-link>

          <router-link 
            to="/gallery" 
            class="bg-white rounded-lg p-6 shadow-md hover:shadow-xl transition-shadow"
          >
            <div class="text-green-600 mb-3">
              <i class="i-lucide-image text-4xl"></i>
            </div>
            <h4 class="text-xl font-bold text-gray-800 mb-2">Gallery</h4>
            <p class="text-gray-600">Explore photos and moments from our campus life</p>
          </router-link>

          <router-link 
            to="/events" 
            class="bg-white rounded-lg p-6 shadow-md hover:shadow-xl transition-shadow"
          >
            <div class="text-purple-600 mb-3">
              <i class="i-lucide-calendar text-4xl"></i>
            </div>
            <h4 class="text-xl font-bold text-gray-800 mb-2">Events</h4>
            <p class="text-gray-600">Stay updated with our latest activities and programs</p>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// No additional logic needed for now
</script>

<style scoped>
.aspect-video {
  aspect-ratio: 16 / 9;
}
</style>
