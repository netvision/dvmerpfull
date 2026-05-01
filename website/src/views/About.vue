<template>
  <div class="about-page">
    <!-- Hero Section -->
    <div class="relative h-96 bg-gradient-to-r from-blue-900 to-blue-700">
      <div class="absolute inset-0 bg-black opacity-30"></div>
      <div class="container mx-auto px-4 h-full flex items-center relative z-10">
        <div class="text-white">
          <h1 class="text-5xl font-bold mb-4">About Dalmia Vidya Mandir</h1>
          <p class="text-xl">Celebrating 100 Years of Educational Excellence</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-16">
      <!-- Introduction -->
      <div class="mb-16">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div>
            <h2 class="text-3xl font-bold text-blue-900 mb-6">Our Legacy</h2>
            <p class="text-lg text-gray-700 leading-relaxed mb-6">
              Dalmia Vidya Mandir inherits a proud legacy of over 100 years of the Dalmia family's unwavering 
              commitment to advancing education in the region. Building upon this rich heritage of educational 
              initiatives, our institution has grown into a premier CBSE-affiliated school that has nurtured 
              thousands of students who have gone on to excel in various fields across the globe.
            </p>
            <p class="text-lg text-gray-700 leading-relaxed mb-6">
              Our institution stands as a testament to quality education, combining traditional values with modern 
              pedagogical approaches. We believe in holistic development, ensuring our students are academically 
              sound, morally upright, and socially responsible citizens.
            </p>
            <div class="flex items-center space-x-8 text-center">
              <div>
                <div class="text-3xl font-bold text-blue-900">100+</div>
                <div class="text-sm text-gray-600">Years of Legacy</div>
              </div>
              <div>
                <div class="text-3xl font-bold text-blue-900">4000+</div>
                <div class="text-sm text-gray-600">Alumni</div>
              </div>
              <div>
                <div class="text-3xl font-bold text-blue-900">100%</div>
                <div class="text-sm text-gray-600">Board Results</div>
              </div>
            </div>
          </div>
          <div>
            <img 
              src="/images/slide1.jpg" 
              alt="Dalmia Vidya Mandir School Building" 
              class="w-full h-96 object-cover rounded-lg shadow-lg"
            />
          </div>
        </div>
      </div>

      <!-- Vision & Mission -->
      <div class="mb-16">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="bg-gradient-to-br from-blue-50 to-indigo-100 p-8 rounded-xl shadow-lg border-l-4 border-blue-600">
            <div class="flex items-center mb-4">
              <div class="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center mr-4">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-blue-900">Our Vision</h3>
            </div>
            <h4 class="text-xl font-semibold text-purple-700 mb-3 italic">
              From Higher Standard of Living to Higher Standard of Life
            </h4>
            <p class="text-gray-700 leading-relaxed text-lg">
              We believe true education empowers students to rise above their circumstances with clarity, resilience, 
              and purpose—transforming them into active creators of meaning. We envision Dalmia Vidya Mandir as a beacon 
              of transformative education that nurtures enlightened minds and compassionate hearts, creating global citizens 
              who excel academically while embodying moral integrity and cultural pride.
            </p>
          </div>
          <div class="bg-gradient-to-br from-orange-50 to-red-100 p-8 rounded-xl shadow-lg border-l-4 border-orange-600">
            <div class="flex items-center mb-4">
              <div class="w-12 h-12 bg-orange-600 rounded-full flex items-center justify-center mr-4">
                <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </div>
              <h3 class="text-2xl font-bold text-blue-900">Our Mission</h3>
            </div>
            <blockquote class="text-lg font-medium italic text-orange-800 mb-3">
              "अभयं सत्त्वसंशुद्धिर्ज्ञानयोगव्यवस्थितिः"
            </blockquote>
            <p class="text-gray-700 leading-relaxed text-lg">
              Inspired by the divine qualities of the Bhagavad Gita, we cultivate fearlessness, truthfulness, compassion, 
              and wisdom in every student—transforming education into character formation. We are committed to providing 
              holistic education that integrates academic excellence with moral development, fostering critical thinking, 
              creativity, and cultural values while preparing students to serve humanity with distinction.
            </p>
          </div>
        </div>
      </div>

      <!-- Core Values -->
      <div class="mb-16">
        <div class="text-center mb-12">
          <h2 class="text-4xl font-bold text-blue-900 mb-4">Our Core Values</h2>
          <div class="w-24 h-1 bg-blue-600 mx-auto"></div>
          <p class="text-lg text-gray-600 mt-4 max-w-3xl mx-auto">
            The pillars that guide our century-old institution in shaping young minds and building character
          </p>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          <div class="text-center p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border-t-4 border-blue-600 group">
            <div class="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-blue-600 transition-colors duration-300">
              <svg class="w-8 h-8 text-blue-600 group-hover:text-white transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <h4 class="text-xl font-semibold text-blue-900 mb-3">Vidya (Knowledge)</h4>
            <p class="text-gray-600 leading-relaxed">Pursuing lifelong learning with curiosity, critical thinking, and academic excellence that illuminates minds and transforms lives.</p>
          </div>
          
          <div class="text-center p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border-t-4 border-green-600 group">
            <div class="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-green-600 transition-colors duration-300">
              <svg class="w-8 h-8 text-green-600 group-hover:text-white transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
              </svg>
            </div>
            <h4 class="text-xl font-semibold text-blue-900 mb-3">Karuna (Compassion)</h4>
            <p class="text-gray-600 leading-relaxed">Cultivating empathy, kindness, and service to others, fostering a spirit of humanity and social responsibility.</p>
          </div>
          
          <div class="text-center p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border-t-4 border-purple-600 group">
            <div class="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-purple-600 transition-colors duration-300">
              <svg class="w-8 h-8 text-purple-600 group-hover:text-white transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            </div>
            <h4 class="text-xl font-semibold text-blue-900 mb-3">Satya (Integrity)</h4>
            <p class="text-gray-600 leading-relaxed">Upholding truth, honesty, and moral courage in all endeavors, building character that stands the test of time.</p>
          </div>
          
          <div class="text-center p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border-t-4 border-orange-600 group">
            <div class="w-16 h-16 bg-orange-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-orange-600 transition-colors duration-300">
              <svg class="w-8 h-8 text-orange-600 group-hover:text-white transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <h4 class="text-xl font-semibold text-blue-900 mb-3">Pragati (Progress)</h4>
            <p class="text-gray-600 leading-relaxed">Embracing innovation and positive change while honoring our rich heritage, preparing students for future leadership.</p>
          </div>
        </div>
        
        <!-- Additional Values Row -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-8">
          <div class="text-center p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border-t-4 border-red-600 group">
            <div class="w-16 h-16 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-red-600 transition-colors duration-300">
              <svg class="w-8 h-8 text-red-600 group-hover:text-white transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
            </div>
            <h4 class="text-xl font-semibold text-blue-900 mb-3">Sanskara (Cultural Values)</h4>
            <p class="text-gray-600 leading-relaxed">Preserving and celebrating our rich Indian heritage while developing global perspectives and cultural appreciation.</p>
          </div>
          
          <div class="text-center p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border-t-4 border-teal-600 group">
            <div class="w-16 h-16 bg-teal-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-teal-600 transition-colors duration-300">
              <svg class="w-8 h-8 text-teal-600 group-hover:text-white transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 7.172V5L8 4z" />
              </svg>
            </div>
            <h4 class="text-xl font-semibold text-blue-900 mb-3">Anushashan (Discipline)</h4>
            <p class="text-gray-600 leading-relaxed">Building self-discipline, responsibility, and respect for others, creating a foundation for personal and professional success.</p>
          </div>
          
          <div class="text-center p-6 bg-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border-t-4 border-indigo-600 group">
            <div class="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mx-auto mb-4 group-hover:bg-indigo-600 transition-colors duration-300">
              <svg class="w-8 h-8 text-indigo-600 group-hover:text-white transition-colors duration-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z" />
              </svg>
            </div>
            <h4 class="text-xl font-semibold text-blue-900 mb-3">Uttkarsh (Excellence)</h4>
            <p class="text-gray-600 leading-relaxed">Striving for excellence in all endeavors, setting high standards and inspiring continuous improvement and achievement.</p>
          </div>
        </div>
      </div>

      <!-- Leadership Team -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Leadership Team</h2>
        <div class="w-24 h-1 bg-blue-600 mx-auto mb-8"></div>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="text-center">
            <img 
              src="/images/paragji.jpg" 
              alt="Shri Parag Dalmia" 
              class="w-48 h-48 mx-auto rounded-xl object-cover mb-4 shadow-lg"
            />
            <h4 class="text-xl font-semibold text-blue-900">Shri Parag Dalmia</h4>
            <p class="text-gray-600 mb-2">Chairman</p>
            <p class="text-sm text-gray-500">Educational Visionary<br/>Leading the Institution's Growth & Development</p>
          </div>
          <div class="text-center">
            <img 
              src="/images/shaktisingh.jpg" 
              alt="Mr. Shakti Singh" 
              class="w-48 h-48 mx-auto rounded-xl object-cover mb-4 shadow-lg"
            />
            <h4 class="text-xl font-semibold text-blue-900">Mr. Shakti Singh</h4>
            <p class="text-gray-600 mb-2">Principal</p>
            <p class="text-sm text-gray-500">Academic Leadership<br/>Ensuring Educational Excellence & Innovation</p>
          </div>
          <div class="text-center">
            <img 
              src="/images/namita.jpg" 
              alt="Ms. Namita Choudhary" 
              class="w-48 h-48 mx-auto rounded-xl object-cover mb-4 shadow-lg"
            />
            <h4 class="text-xl font-semibold text-blue-900">Ms. Namita Choudhary</h4>
            <p class="text-gray-600 mb-2">Head Mistress</p>
            <p class="text-sm text-gray-500">Student Affairs & Development<br/>Nurturing Young Minds & Character Building</p>
          </div>
        </div>
      </div>

      <!-- Awards & Recognition 
      <div class="bg-gray-50 p-8 rounded-lg">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Awards & Recognition</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          
          <div class="text-center">
            <div class="text-4xl mb-3">🏆</div>
            <h5 class="font-semibold text-blue-900 mb-2">Best CBSE School</h5>
            <p class="text-sm text-gray-600">Education Excellence Awards 2024</p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-3">🌟</div>
            <h5 class="font-semibold text-blue-900 mb-2">Green School Certification</h5>
            <p class="text-sm text-gray-600">Eco-friendly Campus Initiative</p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-3">📚</div>
            <h5 class="font-semibold text-blue-900 mb-2">Innovation in Education</h5>
            <p class="text-sm text-gray-600">Remote Interactive Teaching with Expert Faculty</p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-3">🎯</div>
            <h5 class="font-semibold text-blue-900 mb-2">Sports Excellence</h5>
            <p class="text-sm text-gray-600">Inter-School Championship</p>
          </div>
          
        </div>
      </div>
      -->
    </div>
  </div>
</template>

<script setup lang="ts">
// About page component
</script>
