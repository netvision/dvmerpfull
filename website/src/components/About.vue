<template>
  <section class="py-16 bg-white">
    <div class="container mx-auto px-4">
      <div class="flex flex-col md:flex-row items-center gap-10">
        <div class="md:w-1/2">
          <img 
            src="https://images.unsplash.com/photo-1523050854058-8df90110c9f1?auto=format&fit=crop&w=800&q=80"
            alt="Students in classroom at Dalmia Vidya Mandir" 
            class="rounded-lg shadow-lg w-full h-[400px] object-cover"
          />
        </div>
        
        <div class="md:w-1/2">
          <div class="flex flex-col">
            <h2 class="text-3xl font-bold text-blue-900 mb-2">About Our School</h2>
            <div class="w-20 h-1 bg-yellow-500 mb-6"></div>
            <p class="text-gray-700 text-lg leading-relaxed mb-6">
              Dalmia Vidya Mandir has been a beacon of educational excellence for over three decades. 
              We are committed to providing holistic education that nurtures not just academic brilliance 
              but also character, creativity, and critical thinking skills.
            </p>
            <p class="text-gray-700 text-lg leading-relaxed mb-6">
              Our state-of-the-art facilities, experienced faculty, and innovative teaching methodologies 
              create an environment where every student can thrive and reach their full potential.
            </p>
            <div class="flex flex-col sm:flex-row gap-4">
              <router-link 
                to="/about" 
                class="bg-blue-700 hover:bg-blue-800 text-white font-medium py-3 px-6 rounded-md transition-colors text-center"
              >
                Learn More
              </router-link>
              <router-link 
                to="/admissions" 
                class="bg-white border border-blue-700 hover:bg-blue-50 text-blue-700 font-medium py-3 px-6 rounded-md transition-colors text-center"
              >
                Apply Now
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
// Component logic can be added here if needed
</script>
