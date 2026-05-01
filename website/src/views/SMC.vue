<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-16">
      <div class="container mx-auto px-4">
        <div class="text-center">
          <h1 class="text-4xl md:text-5xl font-bold mb-4">School Management Committee</h1>
          <p class="text-xl md:text-2xl text-blue-100">
            Dalmia Vidya Mandir, Chirawa
          </p>
          <p class="text-lg text-blue-200 mt-2">
            Governance & Administration | Academic Year 2025-26
          </p>
          <div class="mt-6">
            <div class="inline-flex items-center px-6 py-3 bg-white/10 backdrop-blur rounded-full font-semibold">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              {{ smcMembers.length }} Committee Members
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-12">
      
      <!-- Introduction Section -->
      <section class="mb-12">
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
          <div class="text-center mb-8">
            <h2 class="text-3xl font-bold text-gray-800 mb-4">About School Management Committee</h2>
            <div class="w-24 h-1 bg-blue-600 mx-auto mb-6"></div>
          </div>
          
          <div class="grid md:grid-cols-2 gap-8">
            <div>
              <h3 class="text-xl font-bold text-gray-800 mb-4">Governance Structure</h3>
              <div class="space-y-4 text-gray-700">
                <p class="leading-relaxed">
                  The School Management Committee (SMC) is constituted as per the provisions of the Right to Education Act, 2009, and CBSE guidelines to ensure effective governance and quality education delivery.
                </p>
                <p class="leading-relaxed">
                  The committee comprises representatives from various stakeholder groups including management, parents, teachers, and local community members to ensure holistic development of the institution.
                </p>
              </div>
            </div>
            
            <div>
              <h3 class="text-xl font-bold text-gray-800 mb-4">Key Responsibilities</h3>
              <ul class="space-y-2 text-gray-700">
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-blue-600 mt-0.5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  Monitor school functioning and academic performance
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-blue-600 mt-0.5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  Ensure quality infrastructure and facilities
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-blue-600 mt-0.5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  Oversee financial management and transparency
                </li>
                <li class="flex items-start">
                  <svg class="w-5 h-5 text-blue-600 mt-0.5 mr-2 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
                  </svg>
                  Promote community participation in education
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- SMC Members List -->
      <section class="mb-12">
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-indigo-600 to-blue-600 text-white p-6">
            <h2 class="text-2xl font-bold">List of Members of School Management Committee</h2>
            <p class="text-indigo-100 mt-2">Academic Year 2025-26 | As per CBSE Guidelines</p>
          </div>
          
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full border-collapse border border-gray-300">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold w-16">S.No.</th>
                    <th class="border border-gray-300 px-6 py-3 text-left font-bold">Name</th>
                    <th class="border border-gray-300 px-6 py-3 text-left font-bold">Designation</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold w-32">Signature</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(member, index) in smcMembers" :key="index" class="hover:bg-gray-50 transition-colors">
                    <td class="border border-gray-300 px-4 py-4 text-center font-medium" :class="getMemberRowColor(member.designation)">
                      {{ member.serialNo }}
                    </td>
                    <td class="border border-gray-300 px-6 py-4 font-semibold text-gray-800" :class="getMemberRowColor(member.designation)">
                      {{ member.name }}
                    </td>
                    <td class="border border-gray-300 px-6 py-4" :class="getMemberRowColor(member.designation)">
                      <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium" :class="getDesignationBadge(member.designation)">
                        <svg v-if="member.designation === 'Chairperson'" class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M9.664 1.319a.75.75 0 01.672 0 41.059 41.059 0 018.198 5.424.75.75 0 01-.254 1.285 31.372 31.372 0 00-7.86 3.83.75.75 0 01-.84 0 31.508 31.508 0 00-2.08-1.287V9.394c0-.244.116-.463.302-.592a35.504 35.504 0 013.305-2.033.75.75 0 00-.714-1.319 37 37 0 00-3.446 2.12A2.216 2.216 0 006 9.393v.38a31.293 31.293 0 00-4.28-1.746.75.75 0 01-.254-1.285 41.059 41.059 0 018.198-5.424zM6 11.459a29.848 29.848 0 00-2.455-1.158 41.029 41.029 0 00-.39 3.114.75.75 0 00.419.74c.528.256 1.046.53 1.554.82-.21-.899-.455-1.85-.755-2.932a.75.75 0 00-.373-.584zm7.5 2.932a29.874 29.874 0 00-.755-2.932.75.75 0 00-.373-.584 29.848 29.848 0 00-2.455-1.158 41.029 41.029 0 00-.39 3.114.75.75 0 00.419.74c.528.256 1.046.53 1.554.82z" clip-rule="evenodd" />
                        </svg>
                        <svg v-else-if="member.designation === 'Member Secretary'" class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M15.621 4.379a3 3 0 00-4.242 0l-7 7a3 3 0 004.241 4.243h.001l.497-.5a.75.75 0 011.064 1.057l-.498.501-.002.002a4.5 4.5 0 01-6.364-6.364l7-7a4.5 4.5 0 016.368 6.36l-3.455 3.553A2.625 2.625 0 119.52 9.52l3.45-3.451a.75.75 0 111.061 1.06l-3.45 3.451a1.125 1.125 0 001.587 1.595l3.454-3.553a3 3 0 000-4.242z" clip-rule="evenodd" />
                        </svg>
                        <svg v-else class="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                          <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z" clip-rule="evenodd" />
                        </svg>
                        {{ member.designation }}
                      </span>
                    </td>
                    <td class="border border-gray-300 px-4 py-4 text-center" :class="getMemberRowColor(member.designation)">
                      <div class="w-20 h-8 bg-gray-100 border border-gray-300 rounded mx-auto flex items-center justify-center text-xs text-gray-500">
                        Signature
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </section>

      <!-- Committee Statistics -->
      <section class="mb-12">
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
          <h2 class="text-2xl font-bold text-gray-800 mb-6 text-center">Committee Composition</h2>
          
          <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
            <div class="text-center p-4 bg-blue-50 rounded-lg border-l-4 border-blue-500">
              <div class="text-2xl font-bold text-blue-600">1</div>
              <div class="text-sm text-gray-600 font-medium">Chairperson</div>
            </div>
            <div class="text-center p-4 bg-green-50 rounded-lg border-l-4 border-green-500">
              <div class="text-2xl font-bold text-green-600">1</div>
              <div class="text-sm text-gray-600 font-medium">Secretary</div>
            </div>
            <div class="text-center p-4 bg-purple-50 rounded-lg border-l-4 border-purple-500">
              <div class="text-2xl font-bold text-purple-600">4</div>
              <div class="text-sm text-gray-600 font-medium">Parent Reps</div>
            </div>
            <div class="text-center p-4 bg-orange-50 rounded-lg border-l-4 border-orange-500">
              <div class="text-2xl font-bold text-orange-600">9</div>
              <div class="text-sm text-gray-600 font-medium">Other Members</div>
            </div>
          </div>
        </div>
      </section>

      <!-- CBSE Compliance -->
      <section class="mb-12">
        <div class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-teal-500 to-cyan-500 text-white p-6">
            <h2 class="text-2xl font-bold">CBSE Compliance & Governance</h2>
            <p class="text-teal-100 mt-2">Constitutional Framework & Legal Requirements</p>
          </div>
          
          <div class="p-6">
            <div class="grid md:grid-cols-2 gap-8">
              <div>
                <h3 class="text-lg font-bold text-gray-800 mb-4">Regulatory Framework</h3>
                <div class="space-y-3 text-sm text-gray-700">
                  <div class="p-3 bg-gray-50 rounded-lg">
                    <p><strong>Constitution:</strong> As per Right to Education Act, 2009</p>
                    <p class="mt-1">Section 21 & 22 provisions compliance</p>
                  </div>
                  <div class="p-3 bg-blue-50 rounded-lg">
                    <p><strong>CBSE Guidelines:</strong> Affiliation Bye-laws 2018</p>
                    <p class="mt-1">Chapter VIII - School Management Committee</p>
                  </div>
                  <div class="p-3 bg-green-50 rounded-lg">
                    <p><strong>Composition:</strong> Multi-stakeholder representation</p>
                    <p class="mt-1">Balanced governance structure maintained</p>
                  </div>
                </div>
              </div>
              
              <div>
                <h3 class="text-lg font-bold text-gray-800 mb-4">Meeting Schedule & Documentation</h3>
                <div class="space-y-3 text-sm text-gray-700">
                  <div class="p-3 bg-yellow-50 rounded-lg">
                    <p><strong>Regular Meetings:</strong> Quarterly basis</p>
                    <p class="mt-1">Minutes maintained as per guidelines</p>
                  </div>
                  <div class="p-3 bg-purple-50 rounded-lg">
                    <p><strong>Special Meetings:</strong> As required</p>
                    <p class="mt-1">Emergency decisions and policy matters</p>
                  </div>
                  <div class="p-3 bg-pink-50 rounded-lg">
                    <p><strong>Documentation:</strong> Complete records maintained</p>
                    <p class="mt-1">Available for inspection and audit</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

    </div>
  </div>
</template>

<script setup lang="ts">
interface SMCMember {
  serialNo: number
  name: string
  designation: string
}

// SMC Members data as provided
const smcMembers: SMCMember[] = [
  { serialNo: 1, name: 'Shri Parag Dalmia', designation: 'Chairperson' },
  { serialNo: 2, name: 'Shri Shakti Singh', designation: 'Member Secretary' },
  { serialNo: 3, name: 'Mr. Vijay Mashi', designation: 'CBSE Principal Representative' },
  { serialNo: 4, name: 'Mr. S. C. Karnatka', designation: 'CBSE Principal Representative' },
  { serialNo: 5, name: 'Mr. Rajesh Dalmia', designation: 'Parent Representative' },
  { serialNo: 6, name: 'Mr. Kuldeep Kulhar', designation: 'Parent Representative' },
  { serialNo: 7, name: 'Ms. Namita Choudhary', designation: 'Teacher Representative' },
  { serialNo: 8, name: 'Ms. Vinod Kumari', designation: 'Teacher Representative' },
  { serialNo: 9, name: 'Mr. Bhupendra Paliwal', designation: 'Member Representative' },
  { serialNo: 10, name: 'Ms. Poonam Harlalka', designation: 'Member Representative' },
  { serialNo: 11, name: 'Mr. Sarvesh Saxena', designation: 'Member Representative' },
  { serialNo: 12, name: 'Ms. Suman Sultania', designation: 'Member Representative' },
  { serialNo: 13, name: 'Ms. Manju Mahla', designation: 'Member Representative' },
  { serialNo: 14, name: 'Mr. Nitin Agarwal', designation: 'Member Representative' },
  { serialNo: 15, name: 'DEO', designation: 'Ex Officio Member' }
]

// Utility functions for styling
const getDesignationBadge = (designation: string): string => {
  if (designation === 'Chairperson') return 'bg-blue-100 text-blue-800'
  if (designation === 'Member Secretary') return 'bg-green-100 text-green-800'
  if (designation.includes('Principal Representative')) return 'bg-purple-100 text-purple-800'
  if (designation.includes('Parent Representative')) return 'bg-orange-100 text-orange-800'
  if (designation.includes('Teacher Representative')) return 'bg-indigo-100 text-indigo-800'
  if (designation === 'Ex Officio Member') return 'bg-red-100 text-red-800'
  return 'bg-gray-100 text-gray-800'
}

const getMemberRowColor = (designation: string): string => {
  if (designation === 'Chairperson') return 'bg-blue-50'
  if (designation === 'Member Secretary') return 'bg-green-50'
  return ''
}
</script>

<style scoped>
/* Custom table styling */
table {
  font-size: 0.875rem;
}

/* Responsive table scroll */
@media (max-width: 768px) {
  .overflow-x-auto {
    -webkit-overflow-scrolling: touch;
  }
}

/* Enhanced hover effects */
tr:hover {
  background-color: #f9fafb;
  transition: background-color 0.2s ease;
}

/* Print styles for better printing */
@media print {
  .bg-gradient-to-r {
    background: #2563eb !important;
    color: white !important;
  }
  
  .signature-box {
    border: 1px solid #000 !important;
    height: 30px !important;
  }
}

/* Signature box styling */
.signature-box {
  min-height: 32px;
  border: 1px solid #d1d5db;
  background-color: #f9fafb;
}
</style>
