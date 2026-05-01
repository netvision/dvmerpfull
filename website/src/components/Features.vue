<template>
  <section class="py-8 bg-white rounded-xl shadow-md border border-gray-200 relative overflow-hidden">
    <!-- Subtle background pattern -->
    <div class="absolute inset-0 opacity-5">
      <div class="h-full w-full" style="background-image: radial-gradient(circle at 2px 2px, #3B82F6 1px, transparent 0); background-size: 40px 40px;"></div>
    </div>

    <div class="container mx-auto px-4 relative overflow-hidden">
      <div class="text-center mb-8">
        <div class="inline-flex items-center px-6 py-2 bg-gradient-to-r from-green-50 to-blue-50 rounded-full border border-green-200/50 shadow-sm mb-4">
          <div class="w-2 h-2 bg-gradient-to-r from-green-500 to-blue-500 rounded-full mr-3"></div>
          <span class="text-sm font-bold bg-gradient-to-r from-green-700 to-blue-700 bg-clip-text text-transparent tracking-wide uppercase">
            Other Salient Features
          </span>
          <div class="w-2 h-2 bg-gradient-to-r from-blue-500 to-green-500 rounded-full ml-3"></div>
        </div>
        <h2 class="text-2xl md:text-3xl font-bold text-gray-900 mb-4">
          Proven Excellence in 
          <span class="bg-gradient-to-r from-green-600 to-blue-600 bg-clip-text text-transparent">
            Action
          </span>
        </h2>
        <p class="text-lg text-gray-600 max-w-3xl mx-auto leading-relaxed">
          Beyond our philosophy lies concrete advantages that make DVM the right choice for your child's future
        </p>
        <div class="w-20 h-0.5 bg-gradient-to-r from-green-600 to-blue-600 mx-auto mt-4 rounded-full"></div>
      </div>

      <!-- Facilities Slider -->
      <div class="relative px-12">
        <swiper
          :modules="modules"
          :slides-per-view="1"
          :space-between="20"
          :navigation="{
            prevEl: '.swiper-button-prev-custom',
            nextEl: '.swiper-button-next-custom',
          }"
          :breakpoints="{
            640: { slidesPerView: 2, spaceBetween: 20 },
            1024: { slidesPerView: 3, spaceBetween: 20 },
            1280: { slidesPerView: 4, spaceBetween: 20 }
          }"
          class="facilities-swiper"
        >
          <!-- Slide 1: 100 Years Legacy -->
          <swiper-slide>
            <div class="group bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-amber-100 h-full">
              <div class="w-full h-32 overflow-hidden rounded-t-xl transform transition-transform duration-300 group-hover:scale-105">
                <img 
                  src="/images/student1.jpg" 
                  alt="100 Years Legacy" 
                  class="w-full h-full object-cover"
                />
              </div>
              <div class="p-4 text-center">
                <h3 class="text-lg font-bold text-gray-900 mb-2">100+ Years Legacy</h3>
                <p class="text-gray-600 text-xs leading-relaxed mb-3">
                  A century of educational excellence and proven track record
                </p>
                <div class="text-amber-600 font-semibold text-xs">
                  Established Heritage
                </div>
              </div>
            </div>
          </swiper-slide>

          <!-- Slide 2: Audio Visual Excellence -->
          <swiper-slide>
            <div class="group bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-blue-100 h-full">
              <div class="w-full h-32 overflow-hidden rounded-t-xl transform transition-transform duration-300 group-hover:scale-105">
                <img 
                  src="/images/avroom.jpg" 
                  alt="AV Room Excellence" 
                  class="w-full h-full object-cover"
                />
              </div>
              <div class="p-4 text-center">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Audio Visual Excellence</h3>
                <p class="text-gray-600 text-xs leading-relaxed mb-3">
                  Interactive learning with global expert faculty via advanced AV facility
                </p>
                <div class="text-blue-600 font-semibold text-xs">
                  Global Expertise Access
                </div>
              </div>
            </div>
          </swiper-slide>

          <!-- Slide 3: Small Class Advantage -->
          <swiper-slide>
            <div class="group bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-purple-100 h-full">
              <div class="w-full h-32 overflow-hidden rounded-t-xl transform transition-transform duration-300 group-hover:scale-105">
                <img 
                  src="/images/student2.jpg" 
                  alt="Small Class Advantage" 
                  class="w-full h-full object-cover"
                />
              </div>
              <div class="p-4 text-center">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Small Class Advantage</h3>
                <p class="text-gray-600 text-xs leading-relaxed mb-3">
                  Maximum 25 students per class ensuring personalized attention
                </p>
                <div class="text-purple-600 font-semibold text-xs">
                  Personal Mentorship
                </div>
              </div>
            </div>
          </swiper-slide>

          <!-- Slide 4: Holistic Development -->
          <swiper-slide>
            <div class="group bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-green-100 h-full">
              <div class="w-full h-32 overflow-hidden rounded-t-xl transform transition-transform duration-300 group-hover:scale-105">
                <img 
                  src="/images/sports.jpg" 
                  alt="Complete Development" 
                  class="w-full h-full object-cover"
                />
              </div>
              <div class="p-4 text-center">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Complete Development</h3>
                <p class="text-gray-600 text-xs leading-relaxed mb-3">
                  Academic excellence + Sports + Arts = Well-rounded individuals
                </p>
                <div class="text-green-600 font-semibold text-xs">
                  Future-Ready Citizens
                </div>
              </div>
            </div>
          </swiper-slide>

          <!-- Slide 5: SmartBoards -->
          <swiper-slide>
            <div class="group bg-gradient-to-br from-cyan-50 to-blue-50 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-cyan-100 h-full">
              <div class="w-full h-32 overflow-hidden rounded-t-xl transform transition-transform duration-300 group-hover:scale-105">
                <img 
                  src="/images/academics.jpg" 
                  alt="SmartBoards" 
                  class="w-full h-full object-cover"
                />
              </div>
              <div class="p-4 text-center">
                <h3 class="text-lg font-bold text-gray-900 mb-2">SmartBoards</h3>
                <p class="text-gray-600 text-xs leading-relaxed mb-3">
                  Interactive digital boards in all classrooms for engaging lessons
                </p>
                <div class="text-cyan-600 font-semibold text-xs">
                  Modern Technology
                </div>
              </div>
            </div>
          </swiper-slide>

          <!-- Slide 6: Advanced Studios -->
          <swiper-slide>
            <div class="group bg-gradient-to-br from-pink-50 to-rose-50 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-pink-100 h-full">
              <div class="w-full h-32 overflow-hidden rounded-t-xl transform transition-transform duration-300 group-hover:scale-105">
                <img 
                  src="/images/building.jpg" 
                  alt="Music, Art & Dance Studios" 
                  class="w-full h-full object-cover"
                />
              </div>
              <div class="p-4 text-center">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Music, Art & Dance Studios</h3>
                <p class="text-gray-600 text-xs leading-relaxed mb-3">
                  Professional-grade facilities to nurture creative talents
                </p>
                <div class="text-pink-600 font-semibold text-xs">
                  Creative Excellence
                </div>
              </div>
            </div>
          </swiper-slide>

          <!-- Slide 7: Laboratories -->
          <swiper-slide>
            <div class="group bg-gradient-to-br from-teal-50 to-green-50 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-teal-100 h-full">
              <div class="w-full h-32 overflow-hidden rounded-t-xl transform transition-transform duration-300 group-hover:scale-105">
                <img 
                  src="/images/labs.jpg" 
                  alt="Modern Laboratories" 
                  class="w-full h-full object-cover"
                />
              </div>
              <div class="p-4 text-center">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Modern Laboratories</h3>
                <p class="text-gray-600 text-xs leading-relaxed mb-3">
                  Physics, Chemistry, Biology & Computer labs with latest equipment
                </p>
                <div class="text-teal-600 font-semibold text-xs">
                  Scientific Exploration
                </div>
              </div>
            </div>
          </swiper-slide>

          <!-- Slide 8: Fire Safety -->
          <swiper-slide>
            <div class="group bg-gradient-to-br from-red-50 to-orange-50 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-red-100 h-full">
              <div class="w-full h-32 overflow-hidden rounded-t-xl transform transition-transform duration-300 group-hover:scale-105">
                <img 
                  src="/images/firesafety.jpg" 
                  alt="Fire Safety" 
                  class="w-full h-full object-cover"
                />
              </div>
              <div class="p-4 text-center">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Fire Safety Measures</h3>
                <p class="text-gray-600 text-xs leading-relaxed mb-3">
                  Advanced fire detection systems and emergency preparedness
                </p>
                <div class="text-red-600 font-semibold text-xs">
                  Complete Safety
                </div>
              </div>
            </div>
          </swiper-slide>

          <!-- Slide 9: Computer Lab -->
          <swiper-slide>
            <div class="group bg-gradient-to-br from-yellow-50 to-amber-50 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-yellow-100 h-full">
              <div class="w-full h-32 overflow-hidden rounded-t-xl transform transition-transform duration-300 group-hover:scale-105">
                <img 
                  src="/images/computerlab.jpeg" 
                  alt="Computer Lab" 
                  class="w-full h-full object-cover"
                />
              </div>
              <div class="p-4 text-center">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Advanced Computer Lab</h3>
                <p class="text-gray-600 text-xs leading-relaxed mb-3">
                  Modern computers with latest software for digital learning
                </p>
                <div class="text-yellow-600 font-semibold text-xs">
                  Tech Excellence
                </div>
              </div>
            </div>
          </swiper-slide>

          <!-- Slide 10: Campus -->
          <swiper-slide>
            <div class="group bg-gradient-to-br from-indigo-50 to-violet-50 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-indigo-100 h-full">
              <div class="w-full h-32 overflow-hidden rounded-t-xl transform transition-transform duration-300 group-hover:scale-105">
                <img 
                  src="/images/slide1.jpg" 
                  alt="Beautiful Campus" 
                  class="w-full h-full object-cover"
                />
              </div>
              <div class="p-4 text-center">
                <h3 class="text-lg font-bold text-gray-900 mb-2">Beautiful Campus</h3>
                <p class="text-gray-600 text-xs leading-relaxed mb-3">
                  Spacious and well-maintained campus with green spaces
                </p>
                <div class="text-indigo-600 font-semibold text-xs">
                  Inspiring Environment
                </div>
              </div>
            </div>
          </swiper-slide>

          <!-- Slide 11: NCC -->
          <swiper-slide>
            <router-link to="/ncc" class="block h-full no-underline">
              <div class="group bg-gradient-to-br from-green-50 to-lime-50 rounded-xl shadow-md hover:shadow-lg transition-all duration-300 transform hover:-translate-y-1 border border-green-100 h-full">
                <div class="w-full h-32 overflow-hidden rounded-t-xl transform transition-transform duration-300 group-hover:scale-105">
                  <img 
                    src="/images/ncc1.jpeg" 
                    alt="National Cadet Corps" 
                    class="w-full h-full object-cover"
                  />
                </div>
                <div class="p-4 text-center">
                  <h3 class="text-lg font-bold text-gray-900 mb-2">National Cadet Corps</h3>
                  <p class="text-gray-600 text-xs leading-relaxed mb-3">
                    Building discipline, leadership, and patriotism through NCC camps and activities
                  </p>
                  <div class="text-green-700 font-semibold text-xs">
                    Unity &amp; Discipline
                  </div>
                </div>
              </div>
            </router-link>
          </swiper-slide>
        </swiper>

        <!-- Custom Navigation Buttons -->
        <button class="swiper-button-prev-custom absolute left-0 top-1/2 -translate-y-1/2 z-10 w-10 h-10 bg-white rounded-full shadow-lg flex items-center justify-center text-gray-700 hover:bg-blue-600 hover:text-white transition-all duration-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        <button class="swiper-button-next-custom absolute right-0 top-1/2 -translate-y-1/2 z-10 w-10 h-10 bg-white rounded-full shadow-lg flex items-center justify-center text-gray-700 hover:bg-blue-600 hover:text-white transition-all duration-300">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>

      <!-- Bottom Stats -->
      <div class="mt-8 bg-gradient-to-r from-gray-900 to-blue-900 rounded-xl p-6 text-white">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
          <div>
            <div class="text-2xl md:text-3xl font-bold text-blue-300 mb-1">100+</div>
            <div class="text-xs text-gray-300 uppercase tracking-wide">Years of Excellence</div>
          </div>
          <div>
            <div class="text-2xl md:text-3xl font-bold text-green-300 mb-1">1:25</div>
            <div class="text-xs text-gray-300 uppercase tracking-wide">Teacher-Student Ratio</div>
          </div>
          <div>
            <div class="text-2xl md:text-3xl font-bold text-purple-300 mb-1">360°</div>
            <div class="text-xs text-gray-300 uppercase tracking-wide">Holistic Development</div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Swiper, SwiperSlide } from 'swiper/vue'
import { Navigation } from 'swiper/modules'

const modules = [Navigation]
</script>

<style scoped>
@import 'swiper/css';
@import 'swiper/css/navigation';

.facilities-swiper {
  padding: 10px 0;
}
</style>
