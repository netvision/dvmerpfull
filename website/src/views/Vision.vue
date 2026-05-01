<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
    <!-- Hero Section -->
    <section class="py-20 relative overflow-hidden">
      <!-- Background decorative elements -->
      <div class="absolute inset-0 overflow-hidden">
        <div class="absolute -top-40 -right-40 w-80 h-80 rounded-full bg-gradient-to-br from-blue-200/30 to-purple-200/30 blur-3xl"></div>
        <div class="absolute -bottom-40 -left-40 w-80 h-80 rounded-full bg-gradient-to-tr from-yellow-200/30 to-orange-200/30 blur-3xl"></div>
      </div>

      <div class="container mx-auto px-4 relative">
        <div class="max-w-6xl mx-auto">
          <!-- Page Header -->
          <div class="text-center mb-16">
            <div class="inline-block px-6 py-2 bg-blue-100 text-blue-800 rounded-full text-sm font-semibold tracking-wide uppercase mb-4">
              Our Educational Philosophy
            </div>
            <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
              From Higher Standard of Living to 
              <span class="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                Higher Standard of Life
              </span>
            </h1>
            <p class="text-xl md:text-2xl text-gray-600 max-w-4xl mx-auto leading-relaxed">
              At the heart of our educational philosophy lies a transformative journey that empowers students to rise above their circumstances with clarity, resilience, and purpose.
            </p>
          </div>

          <!-- Core Philosophy Detailed -->
          <div class="bg-white/70 backdrop-blur-sm rounded-2xl p-8 md:p-12 shadow-xl border border-white/50 mb-16">
            <div class="prose prose-xl max-w-none text-gray-700 leading-relaxed space-y-8">
              <p>
                We believe that true education empowers students not merely to adapt to their circumstances, 
                but to <strong class="text-blue-600">rise above them with clarity, resilience, and purpose</strong>. 
                We envision a school where learning transcends information, evolving into deep conceptual 
                understanding and articulate expression.
              </p>
              
              <p>
                Our students are not passive recipients of content but <strong class="text-purple-600">active creators of meaning</strong>—capable 
                of connecting ideas, expressing insights, and applying knowledge with confidence and creativity.
              </p>

              <blockquote class="border-l-4 border-blue-500 pl-6 italic text-xl text-gray-600 my-8">
                "Education is not preparation for life; education is life itself. At DVM, we don't just prepare students for the future—we help them create it."
              </blockquote>
            </div>
          </div>

          <!-- STEAM Integration -->
          <div class="grid md:grid-cols-2 gap-8 mb-16">
            <div class="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-xl border border-white/50">
              <div class="flex items-center mb-6">
                <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mr-4">
                  <Palette :size="24" class="text-white" />
                </div>
                <h3 class="text-2xl font-bold text-gray-800">STEM to STEAM</h3>
              </div>
              <p class="text-gray-700 leading-relaxed text-lg">
                We integrate <strong>Fine Arts</strong> into our core curriculum, transforming STEM into STEAM, 
                and nurturing the aesthetic, emotional, and cultural dimensions of every learner.
              </p>
            </div>

            <div class="bg-white/70 backdrop-blur-sm rounded-2xl p-8 shadow-xl border border-white/50">
              <div class="flex items-center mb-6">
                <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-blue-500 rounded-xl flex items-center justify-center mr-4">
                  <Trophy :size="24" class="text-white" />
                </div>
                <h3 class="text-2xl font-bold text-gray-800">Sports Excellence</h3>
              </div>
              <p class="text-gray-700 leading-relaxed text-lg">
                We champion <strong>sports and physical excellence</strong> as integral to holistic development. 
                Why should a child only aspire to be a gold medalist in academics? 
                Why not dream of standing on the podium as a national or international sports star?
              </p>
            </div>
          </div>

          <!-- Three Pillars -->
          <div class="mb-16">
            <h2 class="text-3xl md:text-4xl font-bold text-center text-gray-900 mb-12">
              Our Three Pillars of Excellence
            </h2>
            <div class="grid md:grid-cols-3 gap-8">
              <div class="text-center bg-white/70 backdrop-blur-sm rounded-xl p-8 shadow-lg border border-white/50">
                <div class="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-6">
                  <GraduationCap :size="32" class="text-white" />
                </div>
                <h4 class="text-xl font-bold text-gray-800 mb-4">Academic Excellence</h4>
                <p class="text-gray-600 leading-relaxed">Deep conceptual understanding and critical thinking that transforms information into wisdom</p>
              </div>

              <div class="text-center bg-white/70 backdrop-blur-sm rounded-xl p-8 shadow-lg border border-white/50">
                <div class="w-20 h-20 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Music :size="32" class="text-white" />
                </div>
                <h4 class="text-xl font-bold text-gray-800 mb-4">Artistic Expression</h4>
                <p class="text-gray-600 leading-relaxed">Literature, music, and arts for holistic development and emotional intelligence</p>
              </div>

              <div class="text-center bg-white/70 backdrop-blur-sm rounded-xl p-8 shadow-lg border border-white/50">
                <div class="w-20 h-20 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-6">
                  <Zap :size="32" class="text-white" />
                </div>
                <h4 class="text-xl font-bold text-gray-800 mb-4">Athletic Achievement</h4>
                <p class="text-gray-600 leading-relaxed">Physical excellence and competitive spirit that builds character and resilience</p>
              </div>
            </div>
          </div>

          <!-- Foundation Articles Section -->
          <div class="mb-16">
            <div class="text-center mb-12">
              <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                Explore Our 
                <span class="bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  Foundation Articles
                </span>
              </h2>
              <p class="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
                Dive deeper into the core principles that guide our educational approach and transform lives
              </p>
            </div>

            <!-- Articles Grid -->
            <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
              <!-- Article 1: Standard of Life -->
              <router-link 
                to="/standard-of-life"
                class="group bg-gradient-to-br from-blue-50 to-indigo-100 rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-blue-200 hover:border-blue-300 no-underline"
              >
                <div class="flex flex-col h-full">
                  <div class="flex items-center justify-center w-14 h-14 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl mb-4 group-hover:scale-110 transition-transform duration-300">
                    <TrendingUp :size="24" class="text-white" />
                  </div>
                  
                  <h4 class="text-lg font-bold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors">
                    Standard of Life
                  </h4>
                  
                  <p class="text-gray-600 text-sm leading-relaxed mb-4 flex-grow">
                    Beyond material wealth lies a deeper pursuit—cultivating values, resilience, and purpose.
                  </p>
                  
                  <div class="flex items-center text-blue-600 text-sm font-semibold group-hover:text-blue-700">
                    <span>Read More</span>
                    <ArrowRight :size="14" class="ml-2 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </router-link>

              <!-- Article 2: Conceptual Learning -->
              <router-link 
                to="/conceptual-learning"
                class="group bg-gradient-to-br from-purple-50 to-pink-100 rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-purple-200 hover:border-purple-300 no-underline"
              >
                <div class="flex flex-col h-full">
                  <div class="flex items-center justify-center w-14 h-14 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl mb-4 group-hover:scale-110 transition-transform duration-300">
                    <Lightbulb :size="24" class="text-white" />
                  </div>
                  
                  <h4 class="text-lg font-bold text-gray-900 mb-3 group-hover:text-purple-600 transition-colors">
                    Conceptual Learning
                  </h4>
                  
                  <p class="text-gray-600 text-sm leading-relaxed mb-4 flex-grow">
                    Transforming passive absorption into active understanding—where students become creators of meaning.
                  </p>
                  
                  <div class="flex items-center text-purple-600 text-sm font-semibold group-hover:text-purple-700">
                    <span>Read More</span>
                    <ArrowRight :size="14" class="ml-2 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </router-link>

              <!-- Article 3: Fine Arts -->
              <router-link 
                to="/fine-arts"
                class="group bg-gradient-to-br from-orange-50 to-red-100 rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-orange-200 hover:border-orange-300 no-underline"
              >
                <div class="flex flex-col h-full">
                  <div class="flex items-center justify-center w-14 h-14 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl mb-4 group-hover:scale-110 transition-transform duration-300">
                    <PaletteIcon :size="24" class="text-white" />
                  </div>
                  
                  <h4 class="text-lg font-bold text-gray-900 mb-3 group-hover:text-orange-600 transition-colors">
                    Fine Arts Integration
                  </h4>
                  
                  <p class="text-gray-600 text-sm leading-relaxed mb-4 flex-grow">
                    From STEM to STEAM—nurturing creativity, emotional intelligence, and cultural awareness.
                  </p>
                  
                  <div class="flex items-center text-orange-600 text-sm font-semibold group-hover:text-orange-700">
                    <span>Read More</span>
                    <ArrowRight :size="14" class="ml-2 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </router-link>

              <!-- Article 4: Sports Excellence -->
              <router-link 
                to="/sports-excellence"
                class="group bg-gradient-to-br from-green-50 to-emerald-100 rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border border-green-200 hover:border-green-300 no-underline"
              >
                <div class="flex flex-col h-full">
                  <div class="flex items-center justify-center w-14 h-14 bg-gradient-to-r from-green-500 to-teal-500 rounded-xl mb-4 group-hover:scale-110 transition-transform duration-300">
                    <TrophyIcon :size="24" class="text-white" />
                  </div>
                  
                  <h4 class="text-lg font-bold text-gray-900 mb-3 group-hover:text-green-600 transition-colors">
                    Sports Excellence
                  </h4>
                  
                  <p class="text-gray-600 text-sm leading-relaxed mb-4 flex-grow">
                    Beyond academics—where champions are forged through discipline, teamwork, and athletic greatness.
                  </p>
                  
                  <div class="flex items-center text-green-600 text-sm font-semibold group-hover:text-green-700">
                    <span>Read More</span>
                    <ArrowRight :size="14" class="ml-2 group-hover:translate-x-1 transition-transform" />
                  </div>
                </div>
              </router-link>
            </div>
          </div>

          <!-- Closing Statement -->
          <div class="text-center bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-8 md:p-12 text-white shadow-2xl">
            <h3 class="text-2xl md:text-3xl font-bold mb-6">A Sanctuary of Balance</h3>
            <p class="text-lg md:text-xl leading-relaxed mb-8">
              Our school is a sanctuary of balance, where <strong>intellect meets imagination</strong>, 
              and <strong>ambition meets compassion</strong>. We prepare students not just for exams, but for life.
            </p>
            <div class="flex justify-center space-x-8 text-blue-100 mb-8">
              <div class="text-center">
                <Heart :size="32" class="mx-auto mb-2" />
                <span class="text-sm font-medium">Compassion</span>
              </div>
              <div class="text-center">
                <Lightbulb :size="32" class="mx-auto mb-2" />
                <span class="text-sm font-medium">Innovation</span>
              </div>
              <div class="text-center">
                <Target :size="32" class="mx-auto mb-2" />
                <span class="text-sm font-medium">Purpose</span>
              </div>
            </div>
            <router-link 
              to="/"
              class="inline-flex items-center px-6 py-3 bg-white text-blue-600 rounded-full font-semibold hover:bg-blue-50 transition-colors no-underline"
            >
              <ArrowLeft :size="20" class="mr-2" />
              Back to Home
            </router-link>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { 
  GraduationCap, 
  Music, 
  Zap, 
  Heart, 
  Lightbulb, 
  Target,
  TrendingUp,
  ArrowRight,
  ArrowLeft,
  Palette,
  Trophy,
  Palette as PaletteIcon,
  Trophy as TrophyIcon
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

/* Custom font for Sanskrit */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;700&display=swap');
</style>
