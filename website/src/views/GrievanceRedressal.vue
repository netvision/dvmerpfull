<template>
  <div class="grievance-page">
    <!-- Hero Section -->
    <div class="relative h-80 bg-gradient-to-r from-red-600 to-orange-600">
      <div class="absolute inset-0 bg-black opacity-30"></div>
      <div class="container mx-auto px-4 h-full flex items-center relative z-10">
        <div class="text-white">
          <h1 class="text-5xl font-bold mb-4">Grievance Redressal</h1>
          <p class="text-xl">Student & Parent Complaint Resolution System</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-16">
      <!-- Introduction -->
      <div class="mb-16 text-center">
        <h2 class="text-3xl font-bold text-blue-900 mb-6">Our Commitment to Resolution</h2>
        <p class="text-lg text-gray-700 leading-relaxed max-w-4xl mx-auto">
          At Dalmia Vidya Mandir, we believe in maintaining open communication and addressing concerns promptly. 
          Our grievance redressal mechanism ensures that every student and parent concern is heard and resolved 
          in a fair and transparent manner.
        </p>
      </div>

      <!-- Grievance Process -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Grievance Resolution Process</h2>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <div class="space-y-6">
              <div class="flex items-start">
                <div class="bg-red-100 text-red-800 rounded-full w-10 h-10 flex items-center justify-center font-bold mr-4">1</div>
                <div>
                  <h4 class="font-semibold text-gray-800 mb-2">Submit Grievance</h4>
                  <p class="text-gray-600 text-sm">Submit your complaint through online form, email, or written application</p>
                </div>
              </div>
              <div class="flex items-start">
                <div class="bg-orange-100 text-orange-800 rounded-full w-10 h-10 flex items-center justify-center font-bold mr-4">2</div>
                <div>
                  <h4 class="font-semibold text-gray-800 mb-2">Acknowledgment</h4>
                  <p class="text-gray-600 text-sm">Receive acknowledgment with reference number within 24 hours</p>
                </div>
              </div>
              <div class="flex items-start">
                <div class="bg-yellow-100 text-yellow-800 rounded-full w-10 h-10 flex items-center justify-center font-bold mr-4">3</div>
                <div>
                  <h4 class="font-semibold text-gray-800 mb-2">Investigation</h4>
                  <p class="text-gray-600 text-sm">Concerned department investigates the matter thoroughly</p>
                </div>
              </div>
              <div class="flex items-start">
                <div class="bg-green-100 text-green-800 rounded-full w-10 h-10 flex items-center justify-center font-bold mr-4">4</div>
                <div>
                  <h4 class="font-semibold text-gray-800 mb-2">Resolution</h4>
                  <p class="text-gray-600 text-sm">Resolution provided within 7-15 working days</p>
                </div>
              </div>
              <div class="flex items-start">
                <div class="bg-blue-100 text-blue-800 rounded-full w-10 h-10 flex items-center justify-center font-bold mr-4">5</div>
                <div>
                  <h4 class="font-semibold text-gray-800 mb-2">Follow-up</h4>
                  <p class="text-gray-600 text-sm">Follow-up to ensure satisfactory resolution</p>
                </div>
              </div>
            </div>
          </div>
          <div>
            <img 
              src="https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=600&h=400&fit=crop" 
              alt="Resolution Process" 
              class="w-full h-80 object-cover rounded-lg shadow-lg"
            />
          </div>
        </div>
      </div>

      <!-- Types of Grievances -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Types of Grievances We Address</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div class="bg-blue-50 p-6 rounded-lg">
            <div class="text-4xl mb-4">📚</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">Academic Issues</h4>
            <ul class="text-gray-700 text-sm space-y-1">
              <li>• Assessment and evaluation concerns</li>
              <li>• Teaching methodology issues</li>
              <li>• Curriculum-related problems</li>
              <li>• Academic performance disputes</li>
            </ul>
          </div>
          <div class="bg-green-50 p-6 rounded-lg">
            <div class="text-4xl mb-4">👥</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">Behavioral Issues</h4>
            <ul class="text-gray-700 text-sm space-y-1">
              <li>• Bullying or harassment</li>
              <li>• Disciplinary action concerns</li>
              <li>• Student conduct issues</li>
              <li>• Peer relationship problems</li>
            </ul>
          </div>
          <div class="bg-purple-50 p-6 rounded-lg">
            <div class="text-4xl mb-4">🏢</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">Administrative Issues</h4>
            <ul class="text-gray-700 text-sm space-y-1">
              <li>• Fee-related concerns</li>
              <li>• Documentation problems</li>
              <li>• Transport issues</li>
              <li>• Facility-related complaints</li>
            </ul>
          </div>
          <div class="bg-yellow-50 p-6 rounded-lg">
            <div class="text-4xl mb-4">🛡️</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">Safety & Security</h4>
            <ul class="text-gray-700 text-sm space-y-1">
              <li>• Campus safety concerns</li>
              <li>• Health and hygiene issues</li>
              <li>• Emergency response problems</li>
              <li>• Infrastructure safety</li>
            </ul>
          </div>
          <div class="bg-red-50 p-6 rounded-lg">
            <div class="text-4xl mb-4">⚖️</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">Discrimination</h4>
            <ul class="text-gray-700 text-sm space-y-1">
              <li>• Gender-based discrimination</li>
              <li>• Caste or religion-based issues</li>
              <li>• Economic background bias</li>
              <li>• Unfair treatment concerns</li>
            </ul>
          </div>
          <div class="bg-orange-50 p-6 rounded-lg">
            <div class="text-4xl mb-4">💬</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">Communication</h4>
            <ul class="text-gray-700 text-sm space-y-1">
              <li>• Teacher-student communication</li>
              <li>• Parent-school interaction</li>
              <li>• Information dissemination</li>
              <li>• Feedback mechanism issues</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Online Grievance Form -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Submit Your Grievance Online</h2>
        <div class="max-w-4xl mx-auto bg-white p-8 rounded-lg shadow-lg">
          <form class="space-y-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Full Name *</label>
                <input type="text" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="Enter your full name">
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Contact Number *</label>
                <input type="tel" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="Enter your contact number">
              </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Email Address *</label>
                <input type="email" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="Enter your email address">
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Relationship to Student</label>
                <select class="w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500">
                  <option>Select relationship</option>
                  <option>Student</option>
                  <option>Parent</option>
                  <option>Guardian</option>
                  <option>Alumni</option>
                </select>
              </div>
            </div>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Student Name (if applicable)</label>
                <input type="text" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="Enter student name">
              </div>
              <div>
                <label class="block text-sm font-semibold text-gray-700 mb-2">Class/Section</label>
                <input type="text" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="e.g., X-A">
              </div>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Type of Grievance *</label>
              <select class="w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500">
                <option>Select grievance type</option>
                <option>Academic Issues</option>
                <option>Behavioral Issues</option>
                <option>Administrative Issues</option>
                <option>Safety & Security</option>
                <option>Discrimination</option>
                <option>Communication</option>
                <option>Other</option>
              </select>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Subject/Title *</label>
              <input type="text" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="Brief title of your grievance">
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Detailed Description *</label>
              <textarea rows="6" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" placeholder="Please provide detailed description of your grievance..."></textarea>
            </div>
            <div>
              <label class="block text-sm font-semibold text-gray-700 mb-2">Upload Supporting Documents (if any)</label>
              <input type="file" class="w-full p-3 border border-gray-300 rounded-lg focus:ring-blue-500 focus:border-blue-500" multiple>
              <p class="text-xs text-gray-500 mt-1">Maximum file size: 10MB. Accepted formats: PDF, JPG, PNG, DOC</p>
            </div>
            <div class="text-center">
              <button type="submit" class="bg-red-600 hover:bg-red-700 text-white px-8 py-3 rounded-lg font-semibold transition-colors">
                Submit Grievance
              </button>
            </div>
          </form>
        </div>
      </div>

      
      <!-- Contact Information -->
      <div class="bg-gradient-to-r from-red-900 to-orange-900 text-white p-8 rounded-lg">
        <h2 class="text-3xl font-bold mb-6 text-center">Contact Grievance Cell</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="text-center">
            <div class="text-4xl mb-3">📧</div>
            <h4 class="text-lg font-semibold mb-2">Email</h4>
            <p class="text-sm text-red-100">grievance@dalmiavidyamandir.edu.in</p>
            <p class="text-sm text-red-100">Response within 24 hours</p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-3">📞</div>
            <h4 class="text-lg font-semibold mb-2">Phone</h4>
            <p class="text-sm text-red-100">+91-1596-220602</p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-3">🕒</div>
            <h4 class="text-lg font-semibold mb-2">Office Hours</h4>
            <p class="text-sm text-red-100">Monday to Friday</p>
            <p class="text-sm text-red-100">9:00 AM - 5:00 PM</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Grievance Redressal page component
</script>
