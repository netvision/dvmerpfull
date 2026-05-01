<template>
  <div class="academics-page">
    <!-- Hero Section -->
    <div class="relative h-80 bg-gradient-to-r from-purple-600 to-blue-600">
      <div class="absolute inset-0 bg-black opacity-30"></div>
      <div class="container mx-auto px-4 h-full flex items-center relative z-10">
        <div class="text-white">
          <h1 class="text-5xl font-bold mb-4">Academics</h1>
          <p class="text-xl">Comprehensive CBSE Curriculum with Holistic Development</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-16">
      <!-- CBSE Affiliation -->
      <div class="mb-16 text-center">
        <h2 class="text-3xl font-bold text-blue-900 mb-6">CBSE Affiliation</h2>
        <div class="bg-blue-50 p-8 rounded-lg max-w-4xl mx-auto">
          <p class="text-lg text-gray-700 leading-relaxed mb-4">
            Dalmia Vidya Mandir is affiliated with the Central Board of Secondary Education (CBSE), 
            New Delhi, ensuring our students receive education that meets national standards and 
            prepares them for competitive examinations and higher education.
          </p>
          <div class="flex justify-center items-center space-x-8">
            <div class="text-center">
              <div class="text-2xl font-bold text-blue-900">CBSE</div>
              <div class="text-sm text-gray-600">Affiliation No: 1730422</div>
            </div>
            
          </div>
        </div>
      </div>

      <!-- Curriculum Overview -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Curriculum Structure</h2>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h3 class="text-2xl font-semibold text-blue-900 mb-6">Primary Section (Classes I-V)</h3>
            <div class="space-y-4">
              <div class="bg-green-50 p-4 rounded-lg">
                <h4 class="font-semibold text-green-800 mb-2">Core Subjects</h4>
                <ul class="text-green-700 text-sm space-y-1">
                  <li>• English Language & Literature</li>
                  <li>• Hindi (First/Second Language)</li>
                  <li>• Mathematics</li>
                  <li>• Environmental Studies (EVS)</li>
                  <li>• General Knowledge</li>
                </ul>
              </div>
              <div class="bg-blue-50 p-4 rounded-lg">
                <h4 class="font-semibold text-blue-800 mb-2">Co-curricular Activities</h4>
                <ul class="text-blue-700 text-sm space-y-1">
                  <li>• Art & Craft</li>
                  <li>• Music & Dance</li>
                  <li>• Physical Education</li>
                  <li>• Computer Basics</li>
                  <li>• Moral Science</li>
                </ul>
              </div>
            </div>
          </div>
          <div>
            <img 
              src="/images/academics.jpg" 
              alt="Primary Students" 
              class="w-full h-64 object-cover rounded-lg shadow-lg mb-6"
            />
            <div class="bg-yellow-50 p-4 rounded-lg">
              <h4 class="font-semibold text-yellow-800 mb-2">Teaching Methodology</h4>
              <ul class="text-yellow-700 text-sm space-y-1">
                <li>• Activity-based learning</li>
                <li>• Interactive smart classrooms</li>
                <li>• Hands-on experiments</li>
                <li>• Project-based assessments</li>
                <li>• Individual attention</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Secondary & Senior Secondary -->
      <div class="mb-16">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h3 class="text-2xl font-semibold text-blue-900 mb-6">Secondary Section (Classes VI-X)</h3>
            <div class="space-y-4">
              <div class="bg-purple-50 p-4 rounded-lg">
                <h4 class="font-semibold text-purple-800 mb-2">Compulsory Subjects</h4>
                <ul class="text-purple-700 text-sm space-y-1">
                  <li>• English (Language & Literature)</li>
                  <li>• Hindi/Sanskrit</li>
                  <li>• Mathematics</li>
                  <li>• Science (Physics, Chemistry, Biology)</li>
                  <li>• Social Science (History, Geography, Civics, Economics)</li>
                </ul>
              </div>
              <div class="bg-red-50 p-4 rounded-lg">
                <h4 class="font-semibold text-red-800 mb-2">Optional Subjects</h4>
                <ul class="text-red-700 text-sm space-y-1">
                  <li>• French/German</li>
                  <li>• Computer Applications</li>
                  <li>• Physical Education</li>
                  <li>• Fine Arts</li>
                </ul>
              </div>
            </div>
          </div>
          <div>
            <h3 class="text-2xl font-semibold text-blue-900 mb-6">Senior Secondary (Classes XI-XII)</h3>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div class="bg-blue-50 p-4 rounded-lg text-center">
                <h4 class="font-semibold text-blue-800 mb-3">Science Stream</h4>
                <ul class="text-blue-700 text-sm space-y-1">
                  <li>Physics</li>
                  <li>Chemistry</li>
                  <li>Mathematics/Biology</li>
                  <li>English</li>
                  <li>Physical Education</li>
                </ul>
              </div>
              <div class="bg-green-50 p-4 rounded-lg text-center">
                <h4 class="font-semibold text-green-800 mb-3">Commerce Stream</h4>
                <ul class="text-green-700 text-sm space-y-1">
                  <li>Accountancy</li>
                  <li>Business Studies</li>
                  <li>Economics</li>
                  <li>Mathematics</li>
                  <li>English</li>
                </ul>
              </div>
              <div class="bg-yellow-50 p-4 rounded-lg text-center">
                <h4 class="font-semibold text-yellow-800 mb-3">Humanities</h4>
                <ul class="text-yellow-700 text-sm space-y-1">
                  <li>History</li>
                  <li>Political Science</li>
                  <li>Economics</li>
                  <li>English</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Special Programs -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Special Academic Programs</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div class="bg-gradient-to-br from-blue-500 to-purple-600 text-white p-6 rounded-lg">
            <h4 class="text-xl font-semibold mb-3">� Remedial Classes</h4>
            <p class="text-sm mb-4">Additional academic support for students who need extra help in core subjects.</p>
            <ul class="text-sm space-y-1">
              <li>• Mathematics Support</li>
              <li>• Science Concepts</li>
              <li>• Language Skills</li>
              <li>• Individual Attention</li>
            </ul>
          </div>
          <div class="bg-gradient-to-br from-green-500 to-blue-500 text-white p-6 rounded-lg">
            <h4 class="text-xl font-semibold mb-3">� Competitive Exams</h4>
            <p class="text-sm mb-4">Preparation for various competitive examinations and Olympiads.</p>
            <ul class="text-sm space-y-1">
              <li>• JEE/NEET Coaching</li>
              <li>• Science Olympiad</li>
              <li>• Mathematics Olympiad</li>
              <li>• English Olympiad</li>
            </ul>
          </div>
          <div class="bg-gradient-to-br from-yellow-500 to-red-500 text-white p-6 rounded-lg">
            <h4 class="text-xl font-semibold mb-3">🎨 Co-curricular Activities</h4>
            <p class="text-sm mb-4">Comprehensive programs fostering creativity and personality development.</p>
            <ul class="text-sm space-y-1">
              <li>• Debate & Elocution</li>
              <li>• Music & Dance</li>
              <li>• Art & Craft</li>
              <li>• Drama & Theatre</li>
            </ul>
          </div>
          <div class="bg-gradient-to-br from-teal-500 to-cyan-600 text-white p-6 rounded-lg">
            <h4 class="text-xl font-semibold mb-3">💻 Remote Expert Teaching</h4>
            <p class="text-sm mb-4">Interactive classes with expert guest faculty through our AV Room technology.</p>
            <ul class="text-sm space-y-1">
              <li>• Subject Matter Experts</li>
              <li>• Live Interactive Sessions</li>
              <li>• Specialized Guest Faculty</li>
              <li>• Advanced Topics Coverage</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Assessment & Evaluation -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Assessment & Evaluation</h2>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h3 class="text-2xl font-semibold text-blue-900 mb-6">Continuous Assessment</h3>
            <div class="space-y-4">
              <div class="flex items-start">
                <div class="bg-blue-100 p-2 rounded-full mr-4">
                  <span class="text-blue-600 font-bold">40%</span>
                </div>
                <div>
                  <h4 class="font-semibold text-gray-800">Formative Assessment</h4>
                  <p class="text-gray-600 text-sm">Projects, assignments, class participation, quizzes</p>
                </div>
              </div>
              <div class="flex items-start">
                <div class="bg-green-100 p-2 rounded-full mr-4">
                  <span class="text-green-600 font-bold">60%</span>
                </div>
                <div>
                  <h4 class="font-semibold text-gray-800">Summative Assessment</h4>
                  <p class="text-gray-600 text-sm">Term examinations and board examinations</p>
                </div>
              </div>
            </div>
            <div class="mt-6 bg-gray-50 p-4 rounded-lg">
              <h4 class="font-semibold text-gray-800 mb-2">Grade System</h4>
              <p class="text-gray-600 text-sm">We follow CBSE's 9-point grading system ensuring holistic evaluation without academic pressure.</p>
            </div>
          </div>
          <div>
            <img 
              src="https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=600&h=300&fit=crop" 
              alt="Examination Hall" 
              class="w-full h-64 object-cover rounded-lg shadow-lg mb-6"
            />
            <div class="bg-gray-50 p-4 rounded-lg">
              <h4 class="font-semibold text-gray-800 mb-2">Feedback Mechanism</h4>
              <p class="text-gray-600 text-sm">Regular feedback sessions with students and parents to discuss academic progress and areas of improvement.</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Academic Support -->
      <div class="bg-gradient-to-r from-blue-900 to-purple-900 text-white p-8 rounded-lg">
        <h2 class="text-3xl font-bold mb-6 text-center">Academic Support Services</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="text-center">
            <div class="text-4xl mb-3">📚</div>
            <h4 class="text-lg font-semibold mb-2">Library & Research</h4>
            <p class="text-sm text-blue-100">Well-stocked library with digital resources and research facilities</p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-3">👨‍🏫</div>
            <h4 class="text-lg font-semibold mb-2">Extra Classes</h4>
            <p class="text-sm text-blue-100">Additional support classes for slow learners and advanced students</p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-3">🎯</div>
            <h4 class="text-lg font-semibold mb-2">Career Guidance</h4>
            <p class="text-sm text-blue-100">Professional counseling for stream selection and career planning</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Academics page component
</script>
