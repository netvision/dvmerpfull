<template>
  <section class="relative h-[600px] flex items-center overflow-hidden">
    <!-- Swiper Carousel as Background -->
    <div class="absolute inset-0 z-0 h-full w-full">
      <Swiper
        :modules="[EffectFade, Autoplay]"
        effect="fade"
        :autoplay="{ delay: 4000, disableOnInteraction: false }"
        :loop="true"
        :speed="1200"
        class="h-full w-full"
      >
        <SwiperSlide>
          <img
            src="/images/slide1.jpg"
            alt="Dalmia Vidya Mandir Campus 1"
            class="w-full h-full object-cover brightness-[0.85]"
            style="height: 600px; width: 100%"
          />
        </SwiperSlide>
        <SwiperSlide>
          <img
            src="/images/slide2.jpg"
            alt="Dalmia Vidya Mandir Campus 2"
            class="w-full h-full object-cover brightness-[0.85]"
            style="height: 600px; width: 100%"
          />
        </SwiperSlide>
        <SwiperSlide>
          <img
            src="/images/slide3.jpg"
            alt="Dalmia Vidya Mandir Campus 3"
            class="w-full h-full object-cover brightness-[0.85]"
            style="height: 600px; width: 100%"
          />
        </SwiperSlide>
      </Swiper>
    </div>

    <!-- Content -->
    <div class="container mx-auto px-4 relative z-10">
      <div class="max-w-2xl text-white">
        <h1 class="text-4xl md:text-5xl font-bold mb-4">
          Dalmia Vidya Mandir
        </h1>
        <p class="text-xl md:text-2xl mb-8">
          Nurturing minds, building character, and shaping futures through excellence in education
        </p>
        <div class="flex flex-col sm:flex-row gap-4">
          <router-link
            to="/admissions"
            class="bg-blue-700 hover:bg-blue-800 text-white font-medium py-3 px-6 rounded-md transition-colors text-center"
          >
            Admissions Open 2026-27
          </router-link>
          <router-link
            to="/about"
            class="bg-white hover:bg-gray-100 text-blue-900 font-medium py-3 px-6 rounded-md transition-colors text-center"
          >
            Explore Our School
          </router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { Swiper, SwiperSlide } from 'swiper/vue'
import { EffectFade, Autoplay } from 'swiper/modules'
</script>
