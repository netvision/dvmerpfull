<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="bg-gradient-to-br from-purple-900 via-blue-800 to-indigo-900 text-white py-20">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto text-center">
          <div class="inline-block px-6 py-2 bg-white/20 rounded-full text-sm font-semibold tracking-wide uppercase mb-6">
            Learning Philosophy
          </div>
          <h1 class="text-4xl md:text-6xl font-bold mb-6">
            From Content to Concept: 
            <span class="bg-gradient-to-r from-yellow-300 to-orange-300 bg-clip-text text-transparent">
              Empowering Expression
            </span>
          </h1>
          <p class="text-xl md:text-2xl text-blue-100 leading-relaxed">
            Transforming information into insight, and learning into articulation
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
              <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center mr-4">
                <BookOpen :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">Introduction</h2>
            </div>
            <p class="text-lg text-gray-700 leading-relaxed mb-6">
              In traditional education, students often memorize content without truly understanding it. 
              We aim to transform <strong>information into insight</strong>, and <strong>learning into articulation</strong>.
            </p>
            <p class="text-lg text-gray-700 leading-relaxed">
              Our approach goes beyond rote learning to develop deep conceptual understanding, 
              critical thinking skills, and the ability to express complex ideas with clarity and confidence.
            </p>
          </div>

          <!-- Learning Evolution -->
          <div class="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-xl flex items-center justify-center mr-4">
                <TrendingUp :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">The Learning Evolution</h2>
            </div>
            
            <div class="grid md:grid-cols-3 gap-8">
              <!-- Information Learning -->
              <div class="bg-white/70 rounded-xl p-6 shadow-lg text-center">
                <div class="w-16 h-16 bg-gradient-to-r from-red-400 to-red-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <FileText :size="28" class="text-white" />
                </div>
                <h3 class="text-xl font-bold text-red-600 mb-4">Information Learning</h3>
                <ul class="text-sm text-gray-600 space-y-2 text-left">
                  <li>• Passive absorption of facts</li>
                  <li>• Memorization-based approach</li>
                  <li>• Surface-level understanding</li>
                  <li>• Limited retention</li>
                </ul>
              </div>

              <!-- Conceptual Learning -->
              <div class="bg-white/70 rounded-xl p-6 shadow-lg text-center">
                <div class="w-16 h-16 bg-gradient-to-r from-blue-500 to-blue-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Lightbulb :size="28" class="text-white" />
                </div>
                <h3 class="text-xl font-bold text-blue-600 mb-4">Conceptual Learning</h3>
                <ul class="text-sm text-gray-600 space-y-2 text-left">
                  <li>• Active engagement with ideas</li>
                  <li>• Pattern recognition</li>
                  <li>• Deep understanding</li>
                  <li>• Principle-based thinking</li>
                </ul>
              </div>

              <!-- Articulation -->
              <div class="bg-white/70 rounded-xl p-6 shadow-lg text-center">
                <div class="w-16 h-16 bg-gradient-to-r from-green-500 to-green-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <MessageCircle :size="28" class="text-white" />
                </div>
                <h3 class="text-xl font-bold text-green-600 mb-4">Articulation</h3>
                <ul class="text-sm text-gray-600 space-y-2 text-left">
                  <li>• Express complex ideas clearly</li>
                  <li>• Connect different concepts</li>
                  <li>• Apply knowledge creatively</li>
                  <li>• Communicate with confidence</li>
                </ul>
              </div>
            </div>
          </div>

          <!-- Our Approach -->
          <div class="bg-white rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-blue-500 rounded-xl flex items-center justify-center mr-4">
                <Target :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">Our Approach</h2>
            </div>
            
            <div class="grid md:grid-cols-2 gap-8">
              <div class="space-y-6">
                <div class="flex items-start">
                  <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-4 mt-1">
                    <Search :size="20" class="text-blue-600" />
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-gray-800 mb-2">Inquiry-Based Learning</h3>
                    <p class="text-gray-600">Students explore questions, investigate problems, and discover solutions through guided inquiry and research.</p>
                  </div>
                </div>

                <div class="flex items-start">
                  <div class="w-10 h-10 bg-purple-100 rounded-lg flex items-center justify-center mr-4 mt-1">
                    <Puzzle :size="20" class="text-purple-600" />
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-gray-800 mb-2">Project-Based Assessment</h3>
                    <p class="text-gray-600">Real-world projects that require application of knowledge, critical thinking, and creative problem-solving.</p>
                  </div>
                </div>
              </div>

              <div class="space-y-6">
                <div class="flex items-start">
                  <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-4 mt-1">
                    <Mic :size="20" class="text-green-600" />
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-gray-800 mb-2">Expression & Communication</h3>
                    <p class="text-gray-600">Emphasis on writing, speaking, and creative expression across all subjects and disciplines.</p>
                  </div>
                </div>

                <div class="flex items-start">
                  <div class="w-10 h-10 bg-orange-100 rounded-lg flex items-center justify-center mr-4 mt-1">
                    <Network :size="20" class="text-orange-600" />
                  </div>
                  <div>
                    <h3 class="text-lg font-bold text-gray-800 mb-2">Interdisciplinary Thinking</h3>
                    <p class="text-gray-600">Connecting concepts across subjects to develop holistic understanding and systems thinking.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Outcomes -->
          <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-2xl shadow-xl p-8 md:p-12 mb-12">
            <div class="flex items-center mb-8">
              <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-xl flex items-center justify-center mr-4">
                <Award :size="24" class="text-white" />
              </div>
              <h2 class="text-3xl font-bold text-gray-900">Student Outcomes</h2>
            </div>
            
            <div class="text-center mb-8">
              <p class="text-lg text-gray-700">Our students become:</p>
            </div>

            <div class="grid md:grid-cols-3 gap-8">
              <div class="text-center bg-white/70 rounded-xl p-6 shadow-lg">
                <div class="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Users :size="32" class="text-white" />
                </div>
                <h3 class="text-xl font-bold text-gray-800 mb-3">Confident Communicators</h3>
                <p class="text-gray-600 text-sm leading-relaxed">
                  Able to express ideas clearly, engage in meaningful discussions, and present with confidence
                </p>
              </div>

              <div class="text-center bg-white/70 rounded-xl p-6 shadow-lg">
                <div class="w-20 h-20 bg-gradient-to-r from-green-500 to-blue-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Brain :size="32" class="text-white" />
                </div>
                <h3 class="text-xl font-bold text-gray-800 mb-3">Critical Thinkers</h3>
                <p class="text-gray-600 text-sm leading-relaxed">
                  Skilled at analyzing information, evaluating evidence, and making reasoned decisions
                </p>
              </div>

              <div class="text-center bg-white/70 rounded-xl p-6 shadow-lg">
                <div class="w-20 h-20 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Infinity :size="32" class="text-white" />
                </div>
                <h3 class="text-xl font-bold text-gray-800 mb-3">Lifelong Learners</h3>
                <p class="text-gray-600 text-sm leading-relaxed">
                  Curious, self-directed, and equipped with skills to continue learning throughout life
                </p>
              </div>
            </div>
          </div>

          <!-- Call to Action -->
          <div class="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-2xl p-8 md:p-12 text-white text-center">
            <h2 class="text-2xl md:text-3xl font-bold mb-4">
              Experience Transformative Learning
            </h2>
            <p class="text-lg md:text-xl mb-8 text-purple-100">
              Join us in creating confident communicators, critical thinkers, and lifelong learners 
              who can articulate their ideas and impact the world.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <router-link 
                to="/academics" 
                class="bg-white text-purple-600 px-8 py-3 rounded-lg font-semibold hover:bg-purple-50 transition-colors"
              >
                Explore Our Curriculum
              </router-link>
              <router-link 
                to="/admissions" 
                class="bg-purple-500 text-white px-8 py-3 rounded-lg font-semibold hover:bg-purple-400 transition-colors border border-purple-400"
              >
                Apply Now
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
  BookOpen, 
  TrendingUp, 
  FileText, 
  Lightbulb, 
  MessageCircle, 
  Target, 
  Search, 
  Puzzle, 
  Mic, 
  Network, 
  Award, 
  Users, 
  Brain, 
  Infinity 
} from 'lucide-vue-next'
</script>
