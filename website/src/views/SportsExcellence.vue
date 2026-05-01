<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-green-900 via-blue-800 to-teal-900 text-white py-20">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto text-center">
          <div class="inline-block px-6 py-2 bg-white/20 rounded-full text-sm font-semibold tracking-wide uppercase mb-6">
            Sports Excellence
          </div>
          <h1 class="text-4xl md:text-6xl font-bold mb-6">
            Beyond Books: 
            <span class="bg-gradient-to-r from-yellow-300 to-orange-300 bg-clip-text text-transparent">
              The Power of Sports
            </span>
          </h1>
          <p class="text-xl md:text-2xl text-green-100 leading-relaxed">
            Where champions are made and character is forged
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
                <Trophy :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">Redefining Excellence</h2>
            </div>
            <div class="bg-green-50 border-l-4 border-green-400 p-6 mb-6 rounded-r-lg">
              <p class="text-lg text-green-800 font-medium italic">
                "Why should a child only aspire to be a gold medalist in academics? 
                Why not dream of standing on the podium as a national or international sports star?"
              </p>
            </div>
            <p class="text-lg text-gray-700 leading-relaxed mb-6">
              We believe that <strong>sports are as vital as academics</strong> in shaping well-rounded individuals. 
              Physical excellence is not secondary to intellectual achievement—it's a parallel path to greatness 
              that deserves equal recognition and support.
            </p>
            <p class="text-lg text-gray-700 leading-relaxed">
              Our commitment extends beyond the classroom to the playing field, where students learn life lessons 
              that textbooks cannot teach: resilience in defeat, humility in victory, and the power of teamwork.
            </p>
          </div>

          <!-- Core Philosophy -->
          <div class="bg-gradient-to-br from-green-50 to-blue-50 rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-green-500 rounded-xl flex items-center justify-center mr-4">
                <Target :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">Why Sports Matter</h2>
            </div>
            
            <div class="grid md:grid-cols-3 gap-8">
              <div class="text-center bg-white/70 rounded-xl p-6 shadow-lg">
                <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Users :size="28" class="text-white" />
                </div>
                <h3 class="text-lg font-bold text-gray-800 mb-3">Character Building</h3>
                <p class="text-gray-600 text-sm leading-relaxed">
                  Sports build discipline, teamwork, leadership skills, and teach valuable life lessons about perseverance and sportsmanship.
                </p>
              </div>

              <div class="text-center bg-white/70 rounded-xl p-6 shadow-lg">
                <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-teal-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Heart :size="28" class="text-white" />
                </div>
                <h3 class="text-lg font-bold text-gray-800 mb-3">Physical & Mental Health</h3>
                <p class="text-gray-600 text-sm leading-relaxed">
                  Regular physical activity enhances physical fitness, mental well-being, stress management, and overall quality of life.
                </p>
              </div>

              <div class="text-center bg-white/70 rounded-xl p-6 shadow-lg">
                <div class="w-16 h-16 bg-gradient-to-r from-orange-500 to-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Zap :size="28" class="text-white" />
                </div>
                <h3 class="text-lg font-bold text-gray-800 mb-3">Peak Performance</h3>
                <p class="text-gray-600 text-sm leading-relaxed">
                  Athletic training develops focus, goal-setting abilities, time management, and the mindset needed for excellence in any field.
                </p>
              </div>
            </div>
          </div>

          <!-- Our Sports Program -->
          <div class="bg-white rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl flex items-center justify-center mr-4">
                <Medal :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">Our Commitment to Sports Excellence</h2>
            </div>
            
            <div class="grid md:grid-cols-2 gap-8">
              <div class="space-y-6">
                <div class="flex items-start">
                  <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-4 mt-1">
                    <Building :size="20" class="text-blue-600" />
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-gray-800 mb-2">World-Class Infrastructure</h3>
                    <p class="text-gray-600">State-of-the-art sports facilities, modern equipment, and safe playing environments for all athletic activities.</p>
                  </div>
                </div>

                <div class="flex items-start">
                  <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-4 mt-1">
                    <UserCheck :size="20" class="text-green-600" />
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-gray-800 mb-2">Professional Coaching</h3>
                    <p class="text-gray-600">Experienced coaches and trainers who specialize in developing athletic potential and competitive excellence.</p>
                  </div>
                </div>
              </div>

              <div class="space-y-6">
                <div class="flex items-start">
                  <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mr-4 mt-1">
                    <Search :size="20" class="text-purple-600" />
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-gray-800 mb-2">Talent Identification</h3>
                    <p class="text-gray-600">Early identification and development programs to nurture natural athletic abilities and potential champions.</p>
                  </div>
                </div>

                <div class="flex items-start">
                  <div class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center mr-4 mt-1">
                    <Globe :size="20" class="text-orange-600" />
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-gray-800 mb-2">Competitive Opportunities</h3>
                    <p class="text-gray-600">Regular participation in local, state, national, and international competitions to test and showcase skills.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Sports Offerings -->
          <div class="bg-gradient-to-br from-blue-50 to-green-50 rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-blue-500 rounded-xl flex items-center justify-center mr-4">
                <Activity :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">Our Sports Portfolio</h2>
            </div>
            
            <div class="grid md:grid-cols-4 gap-6">
              <div class="text-center bg-white/70 rounded-xl p-4 shadow-lg">
                <div class="w-12 h-12 bg-orange-500 rounded-full flex items-center justify-center mx-auto mb-3">
                  <span class="text-white font-bold">⚽</span>
                </div>
                <h3 class="font-bold text-gray-800">Football</h3>
                <p class="text-xs text-gray-600 mt-1">Team sports & strategy</p>
              </div>

              <div class="text-center bg-white/70 rounded-xl p-4 shadow-lg">
                <div class="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-3">
                  <span class="text-white font-bold">🏀</span>
                </div>
                <h3 class="font-bold text-gray-800">Basketball</h3>
                <p class="text-xs text-gray-600 mt-1">Agility & coordination</p>
              </div>

              <div class="text-center bg-white/70 rounded-xl p-4 shadow-lg">
                <div class="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-3">
                  <span class="text-white font-bold">🏸</span>
                </div>
                <h3 class="font-bold text-gray-800">Badminton</h3>
                <p class="text-xs text-gray-600 mt-1">Speed & precision</p>
              </div>

              <div class="text-center bg-white/70 rounded-xl p-4 shadow-lg">
                <div class="w-12 h-12 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-3">
                  <span class="text-white font-bold">🏃</span>
                </div>
                <h3 class="font-bold text-gray-800">Athletics</h3>
                <p class="text-xs text-gray-600 mt-1">Endurance & strength</p>
              </div>

              <div class="text-center bg-white/70 rounded-xl p-4 shadow-lg">
                <div class="w-12 h-12 bg-red-500 rounded-full flex items-center justify-center mx-auto mb-3">
                  <span class="text-white font-bold">🏏</span>
                </div>
                <h3 class="font-bold text-gray-800">Cricket</h3>
                <p class="text-xs text-gray-600 mt-1">National passion</p>
              </div>

              <div class="text-center bg-white/70 rounded-xl p-4 shadow-lg">
                <div class="w-12 h-12 bg-indigo-500 rounded-full flex items-center justify-center mx-auto mb-3">
                  <span class="text-white font-bold">🏐</span>
                </div>
                <h3 class="font-bold text-gray-800">Volleyball</h3>
                <p class="text-xs text-gray-600 mt-1">Teamwork & communication</p>
              </div>

              

              <div class="text-center bg-white/70 rounded-xl p-4 shadow-lg">
                <div class="w-12 h-12 bg-pink-500 rounded-full flex items-center justify-center mx-auto mb-3">
                  <span class="text-white font-bold">🤸</span>
                </div>
                <h3 class="font-bold text-gray-800">Gymnastics</h3>
                <p class="text-xs text-gray-600 mt-1">Flexibility & grace</p>
              </div>
            </div>
          </div>

          <!-- Balanced Excellence -->
          <div class="bg-white rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mr-4">
                <Scale :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">Balanced Excellence</h2>
            </div>
            
            <div class="bg-gradient-to-r from-blue-50 to-green-50 rounded-xl p-8">
              <p class="text-lg text-gray-700 leading-relaxed mb-6">
                We encourage parents and students to embrace <strong>diverse pathways to excellence</strong>—
                whether academic, artistic, or athletic. Every child deserves the chance to shine in their own way.
              </p>
              
              <div class="grid md:grid-cols-3 gap-6 text-center">
                <div>
                  <div class="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-3">
                    <GraduationCap :size="24" class="text-white" />
                  </div>
                  <h3 class="font-bold text-blue-600">Academic Champions</h3>
                  <p class="text-sm text-gray-600 mt-2">Excellence in studies and research</p>
                </div>

                <div>
                  <div class="w-16 h-16 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Palette :size="24" class="text-white" />
                  </div>
                  <h3 class="font-bold text-purple-600">Creative Artists</h3>
                  <p class="text-sm text-gray-600 mt-2">Masters of expression and imagination</p>
                </div>

                <div>
                  <div class="w-16 h-16 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-3">
                    <Trophy :size="24" class="text-white" />
                  </div>
                  <h3 class="font-bold text-green-600">Athletic Stars</h3>
                  <p class="text-sm text-gray-600 mt-2">Champions on the field and track</p>
                </div>
              </div>
            </div>
          </div>

          <!-- Call to Action -->
          <div class="bg-gradient-to-r from-green-600 to-blue-600 rounded-2xl p-8 md:p-12 text-white text-center">
            <h2 class="text-2xl md:text-3xl font-bold mb-4">
              Unleash Your Athletic Potential
            </h2>
            <p class="text-lg md:text-xl mb-8 text-green-100">
              Join us in creating champions who excel not just in sports, but in life. 
              Where every student has the opportunity to discover their athletic greatness.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <router-link 
                to="/facilities" 
                class="bg-white text-green-600 px-8 py-3 rounded-lg font-semibold hover:bg-green-50 transition-colors"
              >
                Explore Sports Facilities
              </router-link>
              <router-link 
                to="/admissions" 
                class="bg-green-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-green-400 transition-colors border border-green-400"
              >
                Join Our Champions
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
  Trophy, 
  Target, 
  Users, 
  Heart, 
  Zap, 
  Medal, 
  Building, 
  UserCheck, 
  Search, 
  Globe, 
  Activity, 
  Scale, 
  GraduationCap, 
  Palette 
} from 'lucide-vue-next'
</script>
