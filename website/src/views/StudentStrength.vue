<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-16">
      <div class="container mx-auto px-4">
        <div class="text-center">
          <h1 class="text-4xl md:text-5xl font-bold mb-4">Student Strength</h1>
          <p class="text-xl md:text-2xl text-indigo-100">
            Academic Year 2025-26
          </p>
          <p class="text-lg text-indigo-200 mt-2">
            Section-wise Student Information | Published: 04 Aug 2025
          </p>
          <div class="mt-6">
            <div class="inline-flex items-center px-6 py-3 bg-white/10 backdrop-blur rounded-full font-semibold">
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              </svg>
              Total Students: {{ totalStudents }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-12">
      
      <!-- Overall Statistics -->
      <section class="mb-12">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div class="bg-white rounded-xl shadow-lg p-6 text-center border-l-4 border-blue-500">
            <div class="text-3xl font-bold text-blue-600">{{ totalBoys }}</div>
            <div class="text-gray-600 font-medium">Total Boys</div>
            <div class="text-sm text-gray-500 mt-1">{{ ((totalBoys / totalStudents) * 100).toFixed(1) }}%</div>
          </div>
          <div class="bg-white rounded-xl shadow-lg p-6 text-center border-l-4 border-pink-500">
            <div class="text-3xl font-bold text-pink-600">{{ totalGirls }}</div>
            <div class="text-gray-600 font-medium">Total Girls</div>
            <div class="text-sm text-gray-500 mt-1">{{ ((totalGirls / totalStudents) * 100).toFixed(1) }}%</div>
          </div>
          <div class="bg-white rounded-xl shadow-lg p-6 text-center border-l-4 border-green-500">
            <div class="text-3xl font-bold text-green-600">{{ totalStudents }}</div>
            <div class="text-gray-600 font-medium">Total Students</div>
            <div class="text-sm text-gray-500 mt-1">All Sections</div>
          </div>
          <div class="bg-white rounded-xl shadow-lg p-6 text-center border-l-4 border-purple-500">
            <div class="text-3xl font-bold text-purple-600">{{ totalSections }}</div>
            <div class="text-gray-600 font-medium">Total Sections</div>
            <div class="text-sm text-gray-500 mt-1">Active Classes</div>
          </div>
        </div>
      </section>

      <!-- Student Strength Sections -->
      <div class="space-y-12">
        
        <!-- Pre-Primary Section -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-pink-500 to-purple-500 text-white p-6">
            <h2 class="text-2xl font-bold">Pre-Primary Section</h2>
            <p class="text-pink-100 mt-2">Nursery - UKG Student Strength</p>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full border-collapse border border-gray-300">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Class & Section</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Boys</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Girls</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Total</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Gender Ratio</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="student in prePrimaryStudents" :key="student.section" class="hover:bg-gray-50">
                    <td class="border border-gray-300 px-4 py-3 font-semibold" :class="getSectionColor(student.section)">{{ student.section }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-blue-600 font-medium">{{ student.boys }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-pink-600 font-medium">{{ student.girls }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center font-bold text-green-600">{{ student.total }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-sm">{{ getGenderRatio(student.boys, student.girls) }}</td>
                  </tr>
                  <tr class="bg-purple-50 font-bold">
                    <td class="border border-gray-300 px-4 py-3">Pre-Primary Total</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-blue-700">{{ prePrimaryTotals.boys }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-pink-700">{{ prePrimaryTotals.girls }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-green-700">{{ prePrimaryTotals.total }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-sm">{{ getGenderRatio(prePrimaryTotals.boys, prePrimaryTotals.girls) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- Primary Section -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-blue-500 to-indigo-500 text-white p-6">
            <h2 class="text-2xl font-bold">Primary Section</h2>
            <p class="text-blue-100 mt-2">Classes I - V Student Strength</p>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full border-collapse border border-gray-300">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Class & Section</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Boys</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Girls</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Total</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Gender Ratio</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="student in primaryStudents" :key="student.section" class="hover:bg-gray-50">
                    <td class="border border-gray-300 px-4 py-3 font-semibold" :class="getSectionColor(student.section)">{{ student.section }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-blue-600 font-medium">{{ student.boys }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-pink-600 font-medium">{{ student.girls }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center font-bold text-green-600">{{ student.total }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-sm">{{ getGenderRatio(student.boys, student.girls) }}</td>
                  </tr>
                  <tr class="bg-blue-50 font-bold">
                    <td class="border border-gray-300 px-4 py-3">Primary Total</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-blue-700">{{ primaryTotals.boys }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-pink-700">{{ primaryTotals.girls }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-green-700">{{ primaryTotals.total }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-sm">{{ getGenderRatio(primaryTotals.boys, primaryTotals.girls) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- Secondary Section -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-orange-500 to-red-500 text-white p-6">
            <h2 class="text-2xl font-bold">Secondary Section</h2>
            <p class="text-orange-100 mt-2">Classes VI - X Student Strength</p>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full border-collapse border border-gray-300">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Class & Section</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Boys</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Girls</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Total</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Gender Ratio</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="student in secondaryStudents" :key="student.section" class="hover:bg-gray-50">
                    <td class="border border-gray-300 px-4 py-3 font-semibold" :class="getSectionColor(student.section)">{{ student.section }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-blue-600 font-medium">{{ student.boys }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-pink-600 font-medium">{{ student.girls }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center font-bold text-green-600">{{ student.total }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-sm">{{ getGenderRatio(student.boys, student.girls) }}</td>
                  </tr>
                  <tr class="bg-orange-50 font-bold">
                    <td class="border border-gray-300 px-4 py-3">Secondary Total</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-blue-700">{{ secondaryTotals.boys }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-pink-700">{{ secondaryTotals.girls }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-green-700">{{ secondaryTotals.total }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-sm">{{ getGenderRatio(secondaryTotals.boys, secondaryTotals.girls) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- Senior Secondary Section -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-purple-600 to-indigo-600 text-white p-6">
            <h2 class="text-2xl font-bold">Senior Secondary Section</h2>
            <p class="text-purple-100 mt-2">Classes XI - XII Student Strength</p>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full border-collapse border border-gray-300">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Class & Section</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Boys</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Girls</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Total</th>
                    <th class="border border-gray-300 px-4 py-3 text-center font-bold">Gender Ratio</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="student in seniorSecondaryStudents" :key="student.section" class="hover:bg-gray-50">
                    <td class="border border-gray-300 px-4 py-3 font-semibold" :class="getSectionColor(student.section)">{{ student.section }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-blue-600 font-medium">{{ student.boys }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-pink-600 font-medium">{{ student.girls }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center font-bold text-green-600">{{ student.total }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-sm">{{ getGenderRatio(student.boys, student.girls) }}</td>
                  </tr>
                  <tr class="bg-purple-50 font-bold">
                    <td class="border border-gray-300 px-4 py-3">Sr. Secondary Total</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-blue-700">{{ seniorSecondaryTotals.boys }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-pink-700">{{ seniorSecondaryTotals.girls }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-green-700">{{ seniorSecondaryTotals.total }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center text-sm">{{ getGenderRatio(seniorSecondaryTotals.boys, seniorSecondaryTotals.girls) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- Summary and Analysis -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-teal-500 to-cyan-500 text-white p-6">
            <h2 class="text-2xl font-bold">Student Strength Analysis</h2>
            <p class="text-teal-100 mt-2">Statistical Overview & CBSE Compliance</p>
          </div>
          <div class="p-6">
            <div class="grid md:grid-cols-2 gap-6">
              <div>
                <h3 class="text-lg font-bold text-gray-800 mb-4">Section-wise Distribution</h3>
                <div class="space-y-3">
                  <div class="flex justify-between items-center p-3 bg-pink-50 rounded-lg">
                    <span class="font-medium text-gray-700">Pre-Primary (4 sections)</span>
                    <span class="font-bold text-pink-600">{{ prePrimaryTotals.total }} students</span>
                  </div>
                  <div class="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                    <span class="font-medium text-gray-700">Primary (11 sections)</span>
                    <span class="font-bold text-blue-600">{{ primaryTotals.total }} students</span>
                  </div>
                  <div class="flex justify-between items-center p-3 bg-orange-50 rounded-lg">
                    <span class="font-medium text-gray-700">Secondary (14 sections)</span>
                    <span class="font-bold text-orange-600">{{ secondaryTotals.total }} students</span>
                  </div>
                  <div class="flex justify-between items-center p-3 bg-purple-50 rounded-lg">
                    <span class="font-medium text-gray-700">Sr. Secondary (6 sections)</span>
                    <span class="font-bold text-purple-600">{{ seniorSecondaryTotals.total }} students</span>
                  </div>
                </div>
              </div>
              
              <div>
                <h3 class="text-lg font-bold text-gray-800 mb-4">CBSE Compliance Information</h3>
                <div class="space-y-3 text-sm text-gray-700">
                  <div class="p-3 bg-gray-50 rounded-lg">
                    <p><strong>Data Source:</strong> School Management System</p>
                    <p class="mt-1">Published on: 04 Aug 2025, 12:07</p>
                  </div>
                  <div class="p-3 bg-green-50 rounded-lg">
                    <p><strong>Verification:</strong> All data verified by administration</p>
                    <p class="mt-1">Section-wise information as per CBSE mandate</p>
                  </div>
                  <div class="p-3 bg-blue-50 rounded-lg">
                    <p><strong>Total Enrollment:</strong> {{ totalStudents }} students</p>
                    <p class="mt-1">Across {{ totalSections }} active sections</p>
                  </div>
                  <div class="p-3 bg-yellow-50 rounded-lg">
                    <p><strong>Gender Balance:</strong> {{ ((totalBoys / totalStudents) * 100).toFixed(1) }}% Boys, {{ ((totalGirls / totalStudents) * 100).toFixed(1) }}% Girls</p>
                    <p class="mt-1">Promoting inclusive education</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface StudentData {
  section: string
  boys: number
  girls: number
  total: number
}

// Raw student data from the provided information
const studentStrengthData: StudentData[] = [
  { section: 'NURSERY-A', boys: 14, girls: 16, total: 30 },
  { section: 'LKG-A', boys: 14, girls: 14, total: 28 },
  { section: 'UKG-A', boys: 10, girls: 8, total: 18 },
  { section: 'UKG-B', boys: 9, girls: 10, total: 19 },
  { section: 'I-A', boys: 20, girls: 16, total: 36 },
  { section: 'I-B', boys: 20, girls: 18, total: 38 },
  { section: 'II-A', boys: 16, girls: 10, total: 26 },
  { section: 'II-B', boys: 15, girls: 13, total: 28 },
  { section: 'III-A', boys: 14, girls: 11, total: 25 },
  { section: 'III-B', boys: 14, girls: 12, total: 26 },
  { section: 'IV-A', boys: 19, girls: 14, total: 33 },
  { section: 'IV-B', boys: 17, girls: 16, total: 33 },
  { section: 'V-A', boys: 13, girls: 12, total: 25 },
  { section: 'V-B', boys: 13, girls: 11, total: 24 },
  { section: 'V-C', boys: 12, girls: 12, total: 24 },
  { section: 'VI-A', boys: 13, girls: 16, total: 29 },
  { section: 'VI-B', boys: 13, girls: 16, total: 29 },
  { section: 'VI-C', boys: 12, girls: 11, total: 23 },
  { section: 'VII-A', boys: 17, girls: 13, total: 30 },
  { section: 'VII-B', boys: 12, girls: 10, total: 22 },
  { section: 'VII-C', boys: 9, girls: 13, total: 22 },
  { section: 'VIII-A', boys: 15, girls: 16, total: 31 },
  { section: 'VIII-B', boys: 23, girls: 4, total: 27 },
  { section: 'VIII-C', boys: 17, girls: 14, total: 31 },
  { section: 'IX-A', boys: 18, girls: 11, total: 29 },
  { section: 'IX-B', boys: 17, girls: 19, total: 36 },
  { section: 'IX-C', boys: 21, girls: 11, total: 32 },
  { section: 'X-A', boys: 23, girls: 15, total: 38 },
  { section: 'X-B', boys: 20, girls: 16, total: 36 },
  { section: 'XI-A', boys: 6, girls: 8, total: 14 },
  { section: 'XI-B', boys: 14, girls: 15, total: 29 },
  { section: 'XI-C', boys: 5, girls: 8, total: 13 },
  { section: 'XII-A', boys: 15, girls: 9, total: 24 },
  { section: 'XII-B', boys: 18, girls: 10, total: 28 },
  { section: 'XII-C', boys: 6, girls: 7, total: 13 }
]

// Computed properties for different sections
const prePrimaryStudents = computed(() => 
  studentStrengthData.filter(student => 
    student.section.includes('NURSERY') || 
    student.section.includes('LKG') || 
    student.section.includes('UKG')
  )
)

const primaryStudents = computed(() => 
  studentStrengthData.filter(student => 
    student.section.startsWith('I-') || 
    student.section.startsWith('II-') || 
    student.section.startsWith('III-') || 
    student.section.startsWith('IV-') || 
    student.section.startsWith('V-')
  )
)

const secondaryStudents = computed(() => 
  studentStrengthData.filter(student => 
    student.section.startsWith('VI-') || 
    student.section.startsWith('VII-') || 
    student.section.startsWith('VIII-') || 
    student.section.startsWith('IX-') || 
    student.section.startsWith('X-')
  )
)

const seniorSecondaryStudents = computed(() => 
  studentStrengthData.filter(student => 
    student.section.startsWith('XI-') || 
    student.section.startsWith('XII-')
  )
)

// Computed totals for each section
const prePrimaryTotals = computed(() => ({
  boys: prePrimaryStudents.value.reduce((sum, student) => sum + student.boys, 0),
  girls: prePrimaryStudents.value.reduce((sum, student) => sum + student.girls, 0),
  total: prePrimaryStudents.value.reduce((sum, student) => sum + student.total, 0)
}))

const primaryTotals = computed(() => ({
  boys: primaryStudents.value.reduce((sum, student) => sum + student.boys, 0),
  girls: primaryStudents.value.reduce((sum, student) => sum + student.girls, 0),
  total: primaryStudents.value.reduce((sum, student) => sum + student.total, 0)
}))

const secondaryTotals = computed(() => ({
  boys: secondaryStudents.value.reduce((sum, student) => sum + student.boys, 0),
  girls: secondaryStudents.value.reduce((sum, student) => sum + student.girls, 0),
  total: secondaryStudents.value.reduce((sum, student) => sum + student.total, 0)
}))

const seniorSecondaryTotals = computed(() => ({
  boys: seniorSecondaryStudents.value.reduce((sum, student) => sum + student.boys, 0),
  girls: seniorSecondaryStudents.value.reduce((sum, student) => sum + student.girls, 0),
  total: seniorSecondaryStudents.value.reduce((sum, student) => sum + student.total, 0)
}))

// Overall totals
const totalBoys = computed(() => studentStrengthData.reduce((sum, student) => sum + student.boys, 0))
const totalGirls = computed(() => studentStrengthData.reduce((sum, student) => sum + student.girls, 0))
const totalStudents = computed(() => studentStrengthData.reduce((sum, student) => sum + student.total, 0))
const totalSections = computed(() => studentStrengthData.length)

// Utility functions
const getGenderRatio = (boys: number, girls: number): string => {
  const total = boys + girls
  if (total === 0) return 'N/A'
  const boysPercent = ((boys / total) * 100).toFixed(0)
  const girlsPercent = ((girls / total) * 100).toFixed(0)
  return `${boysPercent}% B : ${girlsPercent}% G`
}

const getSectionColor = (section: string): string => {
  if (section.includes('NURSERY')) return 'bg-pink-50 text-pink-800'
  if (section.includes('LKG')) return 'bg-purple-50 text-purple-800'
  if (section.includes('UKG')) return 'bg-indigo-50 text-indigo-800'
  if (section.includes('I-') || section.includes('II-')) return 'bg-blue-50 text-blue-800'
  if (section.includes('III-') || section.includes('IV-') || section.includes('V-')) return 'bg-cyan-50 text-cyan-800'
  if (section.includes('VI-') || section.includes('VII-') || section.includes('VIII-')) return 'bg-orange-50 text-orange-800'
  if (section.includes('IX-') || section.includes('X-')) return 'bg-red-50 text-red-800'
  if (section.includes('XI-') || section.includes('XII-')) return 'bg-purple-50 text-purple-800'
  return 'bg-gray-50 text-gray-800'
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
    background: #4f46e5 !important;
    color: white !important;
  }
}
</style>
