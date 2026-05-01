<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-green-900 via-green-700 to-olive-800 text-white py-20" style="background: linear-gradient(135deg, #14532d 0%, #166534 40%, #365314 100%);">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto text-center">
          <div class="inline-block px-6 py-2 bg-white/20 rounded-full text-sm font-semibold tracking-wide uppercase mb-6">
            Co-Curricular Activities
          </div>
          <h1 class="text-4xl md:text-6xl font-bold mb-6">
            National Cadet Corps
            <span class="block text-2xl md:text-3xl font-medium mt-2 text-green-200">
              Unity &amp; Discipline
            </span>
          </h1>
          <p class="text-xl md:text-2xl text-green-100 leading-relaxed">
            Shaping responsible, disciplined, and patriotic citizens of the nation
          </p>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <section class="py-16">
      <div class="container mx-auto px-4">
        <div class="max-w-5xl mx-auto">

          <!-- Introduction Card -->
          <div class="bg-white rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-green-600 to-green-800 rounded-xl flex items-center justify-center mr-4">
                <Shield :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">About NCC in Our School</h2>
            </div>
            <div class="bg-green-50 border-l-4 border-green-500 p-6 mb-6 rounded-r-lg">
              <p class="text-lg text-green-900 font-medium italic">
                "The NCC motto — Unity and Discipline — reflects the spirit we instil in every cadet."
              </p>
            </div>
            <p class="text-lg text-gray-700 leading-relaxed mb-6">
              The <strong>National Cadet Corps (NCC)</strong> is an important part of the co-curricular activities in our school. 
              It provides students with an excellent platform to develop <strong>discipline, leadership, and a strong sense of responsibility</strong>. 
              Our NCC cadets actively participate in various activities such as drills, parades, social service programmes, and adventure activities.
            </p>
            <p class="text-lg text-gray-700 leading-relaxed">
              Through NCC activities, students develop <strong>confidence, physical fitness</strong>, and a strong spirit of 
              <strong>patriotism and national pride</strong>. NCC in our school plays a significant role in shaping responsible 
              and disciplined citizens of the nation.
            </p>
          </div>

          <!-- Photo Gallery -->
          <div class="bg-white rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-teal-600 rounded-xl flex items-center justify-center mr-4">
                <Image :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">NCC in Action</h2>
            </div>
            <div class="grid md:grid-cols-2 gap-6">
              <div class="overflow-hidden rounded-xl shadow-lg">
                <img 
                  src="/images/ncc1.jpeg" 
                  alt="NCC cadets at school" 
                  class="w-full h-72 object-cover hover:scale-105 transition-transform duration-300"
                />
              </div>
              <div class="overflow-hidden rounded-xl shadow-lg">
                <img 
                  src="/images/ncc2.png" 
                  alt="NCC parade and activities" 
                  class="w-full h-72 object-cover hover:scale-105 transition-transform duration-300"
                />
              </div>
            </div>
          </div>

          <!-- NCC Camps Section -->
          <div class="bg-gradient-to-br from-green-50 to-teal-50 rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-teal-500 to-green-600 rounded-xl flex items-center justify-center mr-4">
                <Tent :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">NCC Camps</h2>
            </div>
            <p class="text-lg text-gray-700 leading-relaxed mb-8">
              Our cadets attend a variety of prestigious NCC camps that help them learn teamwork, 
              leadership, and self-reliance. These camps form the backbone of NCC training and create experiences that last a lifetime.
            </p>
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div 
                v-for="camp in camps" 
                :key="camp.name"
                class="bg-white rounded-xl p-6 shadow-md hover:shadow-lg transition-shadow duration-200"
              >
                <div class="w-10 h-10 rounded-full flex items-center justify-center mb-4" :class="camp.color">
                  <component :is="camp.icon" :size="20" class="text-white" />
                </div>
                <h3 class="text-lg font-bold text-gray-800 mb-2">{{ camp.name }}</h3>
                <p class="text-sm font-semibold text-green-700 mb-2">{{ camp.abbr }}</p>
                <p class="text-gray-600 text-sm leading-relaxed">{{ camp.description }}</p>
              </div>
            </div>
          </div>

          <!-- Key Benefits -->
          <div class="bg-white rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-xl flex items-center justify-center mr-4">
                <Star :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">What NCC Teaches</h2>
            </div>
            <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <div 
                v-for="benefit in benefits" 
                :key="benefit.title"
                class="text-center p-6 rounded-xl border border-gray-100 hover:border-green-200 hover:bg-green-50 transition-all duration-200"
              >
                <div class="w-14 h-14 rounded-full flex items-center justify-center mx-auto mb-4" :class="benefit.color">
                  <component :is="benefit.icon" :size="26" class="text-white" />
                </div>
                <h3 class="text-base font-bold text-gray-800 mb-2">{{ benefit.title }}</h3>
                <p class="text-gray-600 text-sm leading-relaxed">{{ benefit.description }}</p>
              </div>
            </div>
          </div>

        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { 
  Shield, 
  Image, 
  Star,
  Flag,
  Users,
  Heart,
  Zap,
  Mountain,
  Award,
  Globe,
  Tent
} from 'lucide-vue-next'

const camps = [
  {
    name: 'Combined Annual Training Camp',
    abbr: 'CATC',
    icon: Users,
    color: 'bg-gradient-to-r from-blue-500 to-blue-700',
    description: 'Annual camp combining training exercises, drills, and team-building activities for all cadets.'
  },
  {
    name: 'Republic Day Camp',
    abbr: 'RDC',
    icon: Flag,
    color: 'bg-gradient-to-r from-orange-500 to-red-600',
    description: 'Prestigious national-level camp held in New Delhi for the Republic Day parade and celebrations.'
  },
  {
    name: 'Annual Training Camp',
    abbr: 'ATC',
    icon: Award,
    color: 'bg-gradient-to-r from-green-500 to-green-700',
    description: 'Core NCC training camp focusing on military drills, physical fitness, and cadet development.'
  },
  {
    name: 'Thal Sainik Camp',
    abbr: 'TSC',
    icon: Shield,
    color: 'bg-gradient-to-r from-slate-500 to-slate-700',
    description: 'Army wing camp focused on military subjects, weapons training, and tactical exercises.'
  },
  {
    name: 'National Integration Camp',
    abbr: 'NIC',
    icon: Globe,
    color: 'bg-gradient-to-r from-purple-500 to-purple-700',
    description: 'Brings cadets from across India together to promote national unity and cultural exchange.'
  },
  {
    name: 'Adventure Camps',
    abbr: '',
    icon: Mountain,
    color: 'bg-gradient-to-r from-teal-500 to-cyan-600',
    description: 'Outdoor adventure activities like trekking, rock climbing, and river crossing to build self-reliance.'
  }
]

const benefits = [
  {
    title: 'Discipline',
    icon: Zap,
    color: 'bg-gradient-to-r from-yellow-500 to-orange-500',
    description: 'Cadets learn punctuality, orderliness, and self-discipline through structured routines.'
  },
  {
    title: 'Leadership',
    icon: Star,
    color: 'bg-gradient-to-r from-blue-500 to-blue-700',
    description: 'Develops the ability to lead teams and make decisions under pressure.'
  },
  {
    title: 'Physical Fitness',
    icon: Heart,
    color: 'bg-gradient-to-r from-red-500 to-pink-600',
    description: 'Regular drills and physical training build strength, stamina, and overall fitness.'
  },
  {
    title: 'Patriotism',
    icon: Flag,
    color: 'bg-gradient-to-r from-green-600 to-green-800',
    description: 'Instils a deep sense of national pride and a spirit of service to the country.'
  }
]
</script>
