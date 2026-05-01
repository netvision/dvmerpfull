<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-green-600 to-blue-600 text-white py-16">
      <div class="container mx-auto px-4">
        <div class="text-center">
          <h1 class="text-4xl md:text-5xl font-bold mb-4">Fee Structure</h1>
          <p class="text-xl md:text-2xl text-green-100">
            Academic Session 2025-26
          </p>
          <p class="text-lg text-green-200 mt-2">
            Transparent Fee Structure for All Classes
          </p>
          <div class="mt-6">
            <a 
              href="/fee-structure.csv" 
              download
              class="inline-flex items-center px-6 py-3 bg-white text-green-600 rounded-full font-semibold hover:bg-green-50 transition-all duration-300 transform hover:scale-105"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
              </svg>
              Download Fee Structure (CSV)
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-12">
      
      <!-- Fee Overview Statistics -->
      <section class="mb-12">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div class="bg-white rounded-xl shadow-lg p-6 text-center border-l-4 border-pink-500">
            <div class="text-2xl font-bold text-pink-600">₹{{ formatCurrency(nurseryFee) }}</div>
            <div class="text-gray-600 font-medium">Nursery Fee</div>
          </div>
          <div class="bg-white rounded-xl shadow-lg p-6 text-center border-l-4 border-blue-500">
            <div class="text-2xl font-bold text-blue-600">₹{{ formatCurrency(primaryFee) }}</div>
            <div class="text-gray-600 font-medium">Primary Classes</div>
          </div>
          <div class="bg-white rounded-xl shadow-lg p-6 text-center border-l-4 border-green-500">
            <div class="text-2xl font-bold text-green-600">₹{{ formatCurrency(secondaryFee) }}</div>
            <div class="text-gray-600 font-medium">Secondary Classes</div>
          </div>
          <div class="bg-white rounded-xl shadow-lg p-6 text-center border-l-4 border-purple-500">
            <div class="text-2xl font-bold text-purple-600">₹{{ formatCurrency(seniorSecondaryFee) }}</div>
            <div class="text-gray-600 font-medium">Sr. Secondary</div>
          </div>
        </div>
      </section>

      <!-- Fee Structure Sections -->
      <div class="space-y-12">
        
        <!-- Pre-Primary Section -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-pink-500 to-purple-500 text-white p-6">
            <h2 class="text-2xl font-bold">Pre-Primary Section</h2>
            <p class="text-pink-100 mt-2">Nursery - UKG Fee Structure</p>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full border-collapse border border-gray-300">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Class</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Annual Tuition Fee</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">1st Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">2nd Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">3rd Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">4th Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Total Fee</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="fee in prePrimaryFees" :key="fee.class" class="hover:bg-gray-50">
                    <td class="border border-gray-300 px-4 py-3 font-semibold" :class="getClassColor(fee.class)">{{ fee.class }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center font-medium">₹{{ formatCurrency(fee.tuitionFee) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.firstInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.secondInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.thirdInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.fourthInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center font-bold text-green-600">₹{{ formatCurrency(fee.totalFee) }}</td>
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
            <p class="text-blue-100 mt-2">Classes I - V Fee Structure</p>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full border-collapse border border-gray-300">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Class</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Annual Tuition Fee</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">1st Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">2nd Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">3rd Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">4th Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Total Fee</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="fee in primaryFees" :key="fee.class" class="hover:bg-gray-50">
                    <td class="border border-gray-300 px-4 py-3 font-semibold" :class="getClassColor(fee.class)">Class {{ fee.class }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center font-medium">₹{{ formatCurrency(fee.tuitionFee) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.firstInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.secondInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.thirdInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.fourthInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center font-bold text-green-600">₹{{ formatCurrency(fee.totalFee) }}</td>
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
            <p class="text-orange-100 mt-2">Classes VI - X Fee Structure</p>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full border-collapse border border-gray-300">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Class</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Annual Tuition Fee</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">1st Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">2nd Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">3rd Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">4th Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Total Fee</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="fee in secondaryFees" :key="fee.class" class="hover:bg-gray-50">
                    <td class="border border-gray-300 px-4 py-3 font-semibold" :class="getClassColor(fee.class)">Class {{ fee.class }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center font-medium">₹{{ formatCurrency(fee.tuitionFee) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.firstInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.secondInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.thirdInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.fourthInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center font-bold text-green-600">₹{{ formatCurrency(fee.totalFee) }}</td>
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
            <p class="text-purple-100 mt-2">Classes XI - XII Fee Structure</p>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full border-collapse border border-gray-300">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Class</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Annual Tuition Fee</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">1st Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">2nd Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">3rd Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">4th Instalment</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Total Fee</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="fee in seniorSecondaryFees" :key="fee.class" class="hover:bg-gray-50">
                    <td class="border border-gray-300 px-4 py-3 font-semibold" :class="getClassColor(fee.class)">Class {{ fee.class }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center font-medium">₹{{ formatCurrency(fee.tuitionFee) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.firstInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.secondInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.thirdInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">₹{{ formatCurrency(fee.fourthInstalment) }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center font-bold text-green-600">₹{{ formatCurrency(fee.totalFee) }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- Additional Fees Information -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-teal-500 to-cyan-500 text-white p-6">
            <h2 class="text-2xl font-bold">Additional Fees & Information</h2>
            <p class="text-teal-100 mt-2">One-time charges and important notes</p>
          </div>
          <div class="p-6">
            <div class="grid md:grid-cols-2 gap-6">
              <div>
                <h3 class="text-lg font-bold text-gray-800 mb-4">One-time Charges (New Admissions Only)</h3>
                <div class="space-y-3">
                  <div class="flex justify-between items-center p-3 bg-blue-50 rounded-lg">
                    <span class="font-medium text-gray-700">Admission Fee</span>
                    <span class="font-bold text-blue-600">₹5,000</span>
                  </div>
                  <div class="flex justify-between items-center p-3 bg-green-50 rounded-lg">
                    <span class="font-medium text-gray-700">Registration Fee</span>
                    <span class="font-bold text-green-600">₹200</span>
                  </div>
                  <div class="flex justify-between items-center p-3 bg-orange-50 rounded-lg">
                    <span class="font-medium text-gray-700">Transfer Certificate (TC)</span>
                    <span class="font-bold text-orange-600">₹100</span>
                  </div>
                </div>
              </div>
              
              <div>
                <h3 class="text-lg font-bold text-gray-800 mb-4">Payment Information</h3>
                <div class="space-y-3 text-sm text-gray-700">
                  <div class="p-3 bg-gray-50 rounded-lg">
                    <p><strong>Fee Payment:</strong> Quarterly instalments available</p>
                    <p class="mt-1">Annual fee can be paid in 4 equal instalments</p>
                  </div>
                  <div class="p-3 bg-yellow-50 rounded-lg">
                    <p><strong>New Admissions:</strong> Additional one-time charges apply</p>
                    <p class="mt-1">Admission and registration fees for new students only</p>
                  </div>
                  <div class="p-3 bg-red-50 rounded-lg">
                    <p><strong>Transfer Certificate:</strong> ₹100 charged when leaving school</p>
                    <p class="mt-1">Applicable for students leaving the institution</p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Fee Comparison Chart -->
            <div class="mt-8">
              <h3 class="text-lg font-bold text-gray-800 mb-4">Fee Structure Overview</h3>
              <div class="bg-gray-50 rounded-lg p-4">
                <div class="grid grid-cols-2 md:grid-cols-5 gap-4 text-center">
                  <div class="p-3 bg-pink-100 rounded">
                    <div class="text-2xl font-bold text-pink-600">₹30,000</div>
                    <div class="text-sm text-gray-600">Nursery</div>
                  </div>
                  <div class="p-3 bg-blue-100 rounded">
                    <div class="text-2xl font-bold text-blue-600">₹44,000</div>
                    <div class="text-sm text-gray-600">LKG - II</div>
                  </div>
                  <div class="p-3 bg-green-100 rounded">
                    <div class="text-2xl font-bold text-green-600">₹46,500</div>
                    <div class="text-sm text-gray-600">III - V</div>
                  </div>
                  <div class="p-3 bg-orange-100 rounded">
                    <div class="text-2xl font-bold text-orange-600">₹50,500</div>
                    <div class="text-sm text-gray-600">VI - VIII</div>
                  </div>
                  <div class="p-3 bg-purple-100 rounded">
                    <div class="text-2xl font-bold text-purple-600">₹77,000</div>
                    <div class="text-sm text-gray-600">XII (Max)</div>
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
import { ref, computed, onMounted } from 'vue'

interface FeeStructure {
  class: string
  tuitionFee: number
  firstInstalment: number
  secondInstalment: number
  thirdInstalment: number
  fourthInstalment: number
  totalFee: number
}

const feeData = ref<FeeStructure[]>([])

// Computed properties for different sections
const prePrimaryFees = computed(() => 
  feeData.value.filter(fee => ['Nursery', 'LKG', 'UKG'].includes(fee.class))
)

const primaryFees = computed(() => 
  feeData.value.filter(fee => ['I', 'II', 'III', 'IV', 'V'].includes(fee.class))
)

const secondaryFees = computed(() => 
  feeData.value.filter(fee => ['VI', 'VII', 'VIII', 'IX', 'X'].includes(fee.class))
)

const seniorSecondaryFees = computed(() => 
  feeData.value.filter(fee => ['XI', 'XII'].includes(fee.class))
)

// Fee statistics for overview
const nurseryFee = computed(() => 
  feeData.value.find(fee => fee.class === 'Nursery')?.totalFee || 0
)

const primaryFee = computed(() => 
  feeData.value.find(fee => fee.class === 'I')?.totalFee || 0
)

const secondaryFee = computed(() => 
  feeData.value.find(fee => fee.class === 'VI')?.totalFee || 0
)

const seniorSecondaryFee = computed(() => 
  feeData.value.find(fee => fee.class === 'XII')?.totalFee || 0
)

// Utility functions
const formatCurrency = (amount: number): string => {
  return amount.toLocaleString('en-IN')
}

const getClassColor = (className: string): string => {
  const colors: { [key: string]: string } = {
    'Nursery': 'bg-pink-50 text-pink-800',
    'LKG': 'bg-purple-50 text-purple-800',
    'UKG': 'bg-indigo-50 text-indigo-800',
    'I': 'bg-blue-50 text-blue-800',
    'II': 'bg-blue-50 text-blue-800',
    'III': 'bg-green-50 text-green-800',
    'IV': 'bg-green-50 text-green-800',
    'V': 'bg-green-50 text-green-800',
    'VI': 'bg-orange-50 text-orange-800',
    'VII': 'bg-orange-50 text-orange-800',
    'VIII': 'bg-orange-50 text-orange-800',
    'IX': 'bg-red-50 text-red-800',
    'X': 'bg-red-50 text-red-800',
    'XI': 'bg-purple-50 text-purple-800',
    'XII': 'bg-purple-50 text-purple-800'
  }
  return colors[className] || 'bg-gray-50 text-gray-800'
}

// Load fee data from CSV
onMounted(async () => {
  try {
    const response = await fetch('/fee-structure.csv')
    const csvText = await response.text()
    
    const lines = csvText.split('\n').filter(line => line.trim())
    
    // Find the data starting line (after header)
    let dataStartIndex = -1
    for (let i = 0; i < lines.length; i++) {
      if (lines[i].includes('Class,Tuition Fees')) {
        dataStartIndex = i + 1
        break
      }
    }
    
    if (dataStartIndex > -1) {
      feeData.value = lines.slice(dataStartIndex)
        .filter(line => line.trim() && !line.includes('Note:') && !line.includes('Admission Fee') && !line.includes('Registration') && !line.includes('TC Rs'))
        .map(line => {
          const values = line.split(',').map(v => v.trim())
          if (values.length >= 6 && values[0]) {
            return {
              class: values[0],
              tuitionFee: parseInt(values[1]) || 0,
              firstInstalment: parseInt(values[2]) || 0,
              secondInstalment: parseInt(values[3]) || 0,
              thirdInstalment: parseInt(values[4]) || 0,
              fourthInstalment: parseInt(values[5]) || 0,
              totalFee: parseInt(values[6]) || parseInt(values[1]) || 0
            }
          }
          return null
        })
        .filter((fee): fee is FeeStructure => fee !== null)
    }
    
  } catch (error) {
    console.error('Error loading fee data:', error)
  }
})
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
    background: #059669 !important;
    color: white !important;
  }
}
</style>
