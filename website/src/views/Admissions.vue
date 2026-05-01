<template>
  <div class="admissions-page">
    <!-- Hero Section -->
    <div class="relative h-80 bg-gradient-to-r from-green-600 to-blue-600">
      <div class="absolute inset-0 bg-black opacity-30"></div>
      <div class="container mx-auto px-4 h-full flex items-center relative z-10">
        <div class="text-white">
          <h1 class="text-5xl font-bold mb-4">Admissions 2026-27</h1>
          <p class="text-xl">Join the DVM Family - Applications Now Open!</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-16">
      <!-- Admission Process Overview -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Admission Process</h2>
        <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div class="text-center p-6 bg-blue-50 rounded-lg">
            <div class="text-4xl font-bold text-blue-600 mb-3">1</div>
            <h4 class="text-lg font-semibold mb-2">Application Form</h4>
            <p class="text-gray-600">Submit online application with required documents</p>
          </div>
          <div class="text-center p-6 bg-green-50 rounded-lg">
            <div class="text-4xl font-bold text-green-600 mb-3">2</div>
            <h4 class="text-lg font-semibold mb-2">Entrance Test</h4>
            <p class="text-gray-600">Age-appropriate assessment for academic readiness</p>
          </div>
          <div class="text-center p-6 bg-yellow-50 rounded-lg">
            <div class="text-4xl font-bold text-yellow-600 mb-3">3</div>
            <h4 class="text-lg font-semibold mb-2">Interview</h4>
            <p class="text-gray-600">Personal interaction with student and parents</p>
          </div>
          <div class="text-center p-6 bg-purple-50 rounded-lg">
            <div class="text-4xl font-bold text-purple-600 mb-3">4</div>
            <h4 class="text-lg font-semibold mb-2">Admission</h4>
            <p class="text-gray-600">Fee payment and completion of formalities</p>
          </div>
        </div>
      </div>

      <!-- Classes & Eligibility -->
      <div class="mb-16">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h2 class="text-3xl font-bold text-blue-900 mb-6">Classes Offered</h2>
            <div class="space-y-4">
              <div class="border-l-4 border-blue-500 pl-4 py-2">
                <h4 class="text-lg font-semibold text-blue-900">Pre-Primary (Nursery - UKG)</h4>
                <p class="text-gray-600">Age: 3-5 years | Play-based learning with structured activities</p>
              </div>
              <div class="border-l-4 border-green-500 pl-4 py-2">
                <h4 class="text-lg font-semibold text-blue-900">Primary (Class I - V)</h4>
                <p class="text-gray-600">Age: 6-10 years | Foundation building with hands-on learning</p>
              </div>
              <div class="border-l-4 border-yellow-500 pl-4 py-2">
                <h4 class="text-lg font-semibold text-blue-900">Middle School (Class VI - VIII)</h4>
                <p class="text-gray-600">Age: 11-13 years | Comprehensive curriculum with skill development</p>
              </div>
              <div class="border-l-4 border-red-500 pl-4 py-2">
                <h4 class="text-lg font-semibold text-blue-900">Secondary (Class IX - X)</h4>
                <p class="text-gray-600">Age: 14-15 years | CBSE board preparation with career guidance</p>
              </div>
              <div class="border-l-4 border-purple-500 pl-4 py-2">
                <h4 class="text-lg font-semibold text-blue-900">Senior Secondary (Class XI - XII)</h4>
                <p class="text-gray-600">Age: 16-17 years | Science, Commerce & Humanities streams</p>
              </div>
            </div>
          </div>
          <div>
            <img 
              src="https://images.unsplash.com/photo-1509062522246-3755977927d7?w=600&h=400&fit=crop" 
              alt="Students in Classroom" 
              class="w-full h-96 object-cover rounded-lg shadow-lg mb-6"
            />
          </div>
        </div>
      </div>

      <!-- Required Documents -->
      <div class="mb-16">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h2 class="text-3xl font-bold text-blue-900 mb-6">Required Documents</h2>
            <div class="bg-blue-50 p-6 rounded-lg">
              <ul class="space-y-3">
                <li class="flex items-start">
                  <span class="text-blue-600 mr-2">✓</span>
                  <span>Birth Certificate (Original + 2 copies)</span>
                </li>
                <li class="flex items-start">
                  <span class="text-blue-600 mr-2">✓</span>
                  <span>Previous School Transfer Certificate (if applicable)</span>
                </li>
                <li class="flex items-start">
                  <span class="text-blue-600 mr-2">✓</span>
                  <span>Mark sheets of previous class</span>
                </li>
                <li class="flex items-start">
                  <span class="text-blue-600 mr-2">✓</span>
                  <span>Character Certificate from previous school</span>
                </li>
                <li class="flex items-start">
                  <span class="text-blue-600 mr-2">✓</span>
                  <span>Aadhar Card copies (Student & Parents)</span>
                </li>
                <li class="flex items-start">
                  <span class="text-blue-600 mr-2">✓</span>
                  <span>Passport size photographs (6 copies)</span>
                </li>
                <li class="flex items-start">
                  <span class="text-blue-600 mr-2">✓</span>
                  <span>Income Certificate (for scholarship eligibility)</span>
                </li>
              </ul>
            </div>
          </div>
          <div>
            <h2 class="text-3xl font-bold text-blue-900 mb-6">Scholarship Programs</h2>
            <div class="space-y-4">
              <div class="bg-purple-50 p-4 rounded-lg border-l-4 border-purple-500">
                <h4 class="font-semibold text-purple-800 mb-2">Need-based Support</h4>
                <p class="text-purple-700 text-sm">Financial assistance for economically disadvantaged students</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Contact for Admissions -->
      <div class="bg-gradient-to-r from-blue-900 to-blue-700 text-white p-8 rounded-lg text-center">
        <h2 class="text-3xl font-bold mb-4">Ready to Apply?</h2>
        <p class="text-xl mb-6">Join our family of excellence and unlock your child's potential!</p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <a 
            href="#" 
            class="bg-yellow-500 hover:bg-yellow-600 text-white font-semibold py-3 px-8 rounded-lg transition-colors"
          >
            Apply Online
          </a>
          <a 
            href="#" 
            class="bg-white hover:bg-gray-100 text-blue-900 font-semibold py-3 px-8 rounded-lg transition-colors"
          >
            Download Prospectus
          </a>
        </div>
        <div class="mt-6 text-blue-100">
          <p><strong>Admission Office:</strong> +91 1596 220602 | admissions@dvmchirawa.ac.in</p>
          <p><strong>Office Hours:</strong> Monday to Saturday, 9:00 AM - 4:00 PM</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Admissions page component
</script>
