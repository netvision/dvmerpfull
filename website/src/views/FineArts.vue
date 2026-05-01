<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-orange-900 via-red-800 to-pink-900 text-white py-20">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto text-center">
          <div class="inline-block px-6 py-2 bg-white/20 rounded-full text-sm font-semibold tracking-wide uppercase mb-6">
            STEAM Education
          </div>
          <h1 class="text-4xl md:text-6xl font-bold mb-6">
            STEAM Over STEM: 
            <span class="bg-gradient-to-r from-yellow-300 to-orange-300 bg-clip-text text-transparent">
              The Vital Role of Fine Arts
            </span>
          </h1>
          <p class="text-xl md:text-2xl text-orange-100 leading-relaxed">
            Where creativity meets science, and imagination fuels innovation
          </p>
        </div>
      </div>
    </section>

    <!-- Sanskrit Wisdom -->
    <section class="py-16 bg-gradient-to-r from-orange-100 to-yellow-100">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto text-center">
          <h2 class="text-3xl font-bold text-gray-800 mb-8">Timeless Wisdom</h2>
          
          <!-- Sanskrit Text -->
          <div class="bg-white/80 rounded-2xl p-8 mb-8 shadow-xl">
            <p class="text-2xl md:text-3xl font-bold text-orange-800 leading-relaxed mb-6" 
               style="font-family: 'Noto Sans Devanagari', serif;">
              साहित्यसङ्गीतकलाविहीनः साक्षात्पशुः पुच्छविषाणहीनः।<br>
              तृणं न खादन्नपि जीवमानः तद्भागधेयं परमं पशूनाम् ॥
            </p>
          </div>
          
          <!-- Translation -->
          <p class="text-xl italic text-gray-700 leading-relaxed bg-white/60 rounded-xl p-6 shadow-lg">
            "A life devoid of literature, music, and art is akin to that of a beast—alive, yet unfulfilled."
          </p>
          
          <p class="text-lg text-gray-600 mt-6">
            This ancient Sanskrit verse reminds us that <strong>Fine Arts are essential to human development</strong>, 
            not mere decorations to education.
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
              <div class="w-12 h-12 bg-gradient-to-r from-pink-500 to-purple-500 rounded-xl flex items-center justify-center mr-4">
                <Palette :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">The Soul of Education</h2>
            </div>
            <p class="text-lg text-gray-700 leading-relaxed mb-6">
              Fine Arts are not luxury additions to education—they are fundamental to developing complete human beings. 
              They cultivate emotional intelligence, spark creativity, and foster cultural awareness in ways that 
              traditional subjects alone cannot achieve.
            </p>
            <p class="text-lg text-gray-700 leading-relaxed">
              When we integrate arts into science, technology, engineering, and mathematics, we create STEAM—
              a holistic approach that nurtures both the analytical and creative aspects of the human mind.
            </p>
          </div>

          <!-- Core Philosophy -->
          <div class="bg-gradient-to-br from-pink-50 to-purple-50 rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center mr-4">
                <Heart :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">Why Arts Matter</h2>
            </div>
            
            <div class="grid md:grid-cols-3 gap-8">
              <div class="text-center bg-white/70 rounded-xl p-6 shadow-lg">
                <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Brain :size="28" class="text-white" />
                </div>
                <h3 class="text-lg font-bold text-gray-800 mb-3">Emotional Intelligence</h3>
                <p class="text-gray-600 text-sm leading-relaxed">
                  Arts help students understand and express emotions, develop empathy, and connect with others on a deeper level.
                </p>
              </div>

              <div class="text-center bg-white/70 rounded-xl p-6 shadow-lg">
                <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Lightbulb :size="28" class="text-white" />
                </div>
                <h3 class="text-lg font-bold text-gray-800 mb-3">Creative Thinking</h3>
                <p class="text-gray-600 text-sm leading-relaxed">
                  Artistic expression nurtures innovation, problem-solving skills, and the ability to think outside the box.
                </p>
              </div>

              <div class="text-center bg-white/70 rounded-xl p-6 shadow-lg">
                <div class="w-16 h-16 bg-gradient-to-r from-orange-500 to-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Globe :size="28" class="text-white" />
                </div>
                <h3 class="text-lg font-bold text-gray-800 mb-3">Cultural Awareness</h3>
                <p class="text-gray-600 text-sm leading-relaxed">
                  Exposure to diverse art forms builds appreciation for different cultures and perspectives.
                </p>
              </div>
            </div>
          </div>

          <!-- Our Arts Integration -->
          <div class="bg-white rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl flex items-center justify-center mr-4">
                <Sparkles :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">Our Arts Integration</h2>
            </div>
            
            <div class="grid md:grid-cols-2 gap-8">
              <div class="space-y-6">
                <div class="flex items-start">
                  <div class="w-10 h-10 bg-pink-100 rounded-lg flex items-center justify-center mr-4 mt-1">
                    <Brush :size="20" class="text-pink-600" />
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-gray-800 mb-2">Visual Arts</h3>
                    <p class="text-gray-600">Painting, drawing, sculpture, and digital art integrated into all subjects to enhance visual learning and creativity.</p>
                  </div>
                </div>

                <div class="flex items-start">
                  <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-4 mt-1">
                    <Music :size="20" class="text-blue-600" />
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-gray-800 mb-2">Music & Sound</h3>
                    <p class="text-gray-600">Classical and contemporary music, sound engineering, and audio production as part of comprehensive education.</p>
                  </div>
                </div>
              </div>

              <div class="space-y-6">
                <div class="flex items-start">
                  <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-4 mt-1">
                    <Theater :size="20" class="text-green-600" />
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-gray-800 mb-2">Drama & Performance</h3>
                    <p class="text-gray-600">Theater arts, public speaking, and performance skills to build confidence and communication abilities.</p>
                  </div>
                </div>

                <div class="flex items-start">
                  <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mr-4 mt-1">
                    <PenTool :size="20" class="text-purple-600" />
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-gray-800 mb-2">Creative Writing</h3>
                    <p class="text-gray-600">Poetry, storytelling, and creative writing to develop language skills and emotional expression.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- STEM to STEAM -->
          <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-xl flex items-center justify-center mr-4">
                <Zap :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">From STEM to STEAM</h2>
            </div>
            
            <div class="text-center mb-8">
              <p class="text-lg text-gray-700">
                We add the "A" for Arts to STEM, creating a holistic learning model that nurtures both logic and imagination.
              </p>
            </div>

            <div class="grid md:grid-cols-5 gap-4 text-center">
              <div class="bg-white/70 rounded-xl p-4 shadow-lg">
                <div class="w-12 h-12 bg-blue-500 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Beaker :size="20" class="text-white" />
                </div>
                <h3 class="font-bold text-blue-600">Science</h3>
                <p class="text-xs text-gray-600 mt-1">Discovery & Analysis</p>
              </div>

              <div class="bg-white/70 rounded-xl p-4 shadow-lg">
                <div class="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Cpu :size="20" class="text-white" />
                </div>
                <h3 class="font-bold text-green-600">Technology</h3>
                <p class="text-xs text-gray-600 mt-1">Innovation & Tools</p>
              </div>

              <div class="bg-white/70 rounded-xl p-4 shadow-lg">
                <div class="w-12 h-12 bg-purple-500 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Settings :size="20" class="text-white" />
                </div>
                <h3 class="font-bold text-purple-600">Engineering</h3>
                <p class="text-xs text-gray-600 mt-1">Design & Build</p>
              </div>

              <div class="bg-white/70 rounded-xl p-4 shadow-lg">
                <div class="w-12 h-12 bg-pink-500 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Palette :size="20" class="text-white" />
                </div>
                <h3 class="font-bold text-pink-600">Arts</h3>
                <p class="text-xs text-gray-600 mt-1">Create & Express</p>
              </div>

              <div class="bg-white/70 rounded-xl p-4 shadow-lg">
                <div class="w-12 h-12 bg-orange-500 rounded-full flex items-center justify-center mx-auto mb-3">
                  <Calculator :size="20" class="text-white" />
                </div>
                <h3 class="font-bold text-orange-600">Mathematics</h3>
                <p class="text-xs text-gray-600 mt-1">Logic & Patterns</p>
              </div>
            </div>
          </div>

          <!-- Call to Action -->
          <div class="bg-gradient-to-r from-pink-600 to-purple-600 rounded-2xl p-8 md:p-12 text-white text-center">
            <h2 class="text-2xl md:text-3xl font-bold mb-4">
              Nurture the Complete Human Being
            </h2>
            <p class="text-lg md:text-xl mb-8 text-pink-100">
              Join us in creating a balanced education where arts and sciences work together to 
              develop emotionally intelligent, creative, and culturally aware students.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <router-link 
                to="/academics" 
                class="bg-white text-pink-600 px-8 py-3 rounded-lg font-semibold hover:bg-pink-50 transition-colors"
              >
                Explore STEAM Curriculum
              </router-link>
              <router-link 
                to="/gallery" 
                class="bg-pink-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-pink-400 transition-colors border border-pink-400"
              >
                View Art Gallery
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
  Palette, 
  Heart, 
  Brain, 
  Lightbulb, 
  Globe, 
  Sparkles, 
  Brush, 
  Music, 
  Theater, 
  PenTool, 
  Zap, 
  Beaker, 
  Cpu, 
  Settings, 
  Calculator 
} from 'lucide-vue-next'
</script>

<style scoped>
/* Custom font for Sanskrit */
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Devanagari:wght@400;700&display=swap');
</style>
