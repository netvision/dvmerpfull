<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-16">
      <div class="container mx-auto px-4">
        <div class="text-center">
          <h1 class="text-4xl md:text-5xl font-bold mb-4">Our Staff</h1>
          <p class="text-xl md:text-2xl text-blue-100">
            Qualified & Experienced Educators
          </p>
          <p class="text-lg text-blue-200 mt-2">
            Academic Session 2025-26 | CBSE Mandated Staff Details
          </p>
          <div class="mt-6">
            <a 
              href="/staff.csv" 
              download
              class="inline-flex items-center px-6 py-3 bg-white text-blue-600 rounded-full font-semibold hover:bg-blue-50 transition-all duration-300 transform hover:scale-105"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2 2H5a2 2 0 01-2-2z" />
              </svg>
              Download Staff Details (CSV)
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-12">
      <!-- Staff Statistics -->
      <section class="mb-12">
        <div class="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div class="bg-white rounded-xl shadow-lg p-6 text-center border-l-4 border-blue-500">
            <div class="text-3xl font-bold text-blue-600">{{ principalCount }}</div>
            <div class="text-gray-600 font-medium">Principal</div>
          </div>
          <div class="bg-white rounded-xl shadow-lg p-6 text-center border-l-4 border-green-500">
            <div class="text-3xl font-bold text-green-600">{{ pgtCount }}</div>
            <div class="text-gray-600 font-medium">PGT Teachers</div>
          </div>
          <div class="bg-white rounded-xl shadow-lg p-6 text-center border-l-4 border-orange-500">
            <div class="text-3xl font-bold text-orange-600">{{ tgtCount }}</div>
            <div class="text-gray-600 font-medium">TGT Teachers</div>
          </div>
          <div class="bg-white rounded-xl shadow-lg p-6 text-center border-l-4 border-purple-500">
            <div class="text-3xl font-bold text-purple-600">{{ prtCount }}</div>
            <div class="text-gray-600 font-medium">PRT Teachers</div>
          </div>
        </div>
      </section>

      <!-- Teaching Staff Sections -->
      <div class="space-y-12">
        
        <!-- Principal -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white p-6">
            <h2 class="text-2xl font-bold">Principal</h2>
            <p class="text-blue-100 mt-2">School Leadership</p>
          </div>
          <div class="p-6">
            <div v-for="staff in principalStaff" :key="staff.sno" class="bg-blue-50 rounded-lg p-4 mb-4">
              <div class="flex flex-col md:flex-row md:items-center justify-between">
                <div class="flex-1">
                  <h3 class="text-xl font-bold text-blue-800">{{ staff.name }}</h3>
                  <p class="text-blue-600 font-medium">{{ staff.designation }}</p>
                  <p class="text-gray-700 mt-1"><strong>Qualification:</strong> {{ staff.qualification }}</p>
                  <p class="text-gray-600"><strong>Experience:</strong> {{ staff.experience }} years</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- PGT Teachers -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-green-500 to-emerald-500 text-white p-6">
            <h2 class="text-2xl font-bold">Post Graduate Teachers (PGT)</h2>
            <p class="text-green-100 mt-2">Senior Secondary Level (Classes XI-XII)</p>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full border-collapse border border-gray-300">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">S.No.</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Name</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Designation & Subject</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Qualification</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Experience (Years)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="staff in pgtStaff" :key="staff.sno" class="hover:bg-gray-50">
                    <td class="border border-gray-300 px-4 py-3 text-center">{{ staff.sno }}</td>
                    <td class="border border-gray-300 px-4 py-3 font-semibold">{{ staff.name }}</td>
                    <td class="border border-gray-300 px-4 py-3">{{ staff.designation }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">{{ staff.qualification }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">{{ staff.experience }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- TGT Teachers -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-orange-500 to-red-500 text-white p-6">
            <h2 class="text-2xl font-bold">Trained Graduate Teachers (TGT)</h2>
            <p class="text-orange-100 mt-2">Secondary Level (Classes VI-X)</p>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full border-collapse border border-gray-300">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">S.No.</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Name</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Designation & Subject</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Qualification</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Experience (Years)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="staff in tgtStaff" :key="staff.sno" class="hover:bg-gray-50">
                    <td class="border border-gray-300 px-4 py-3 text-center">{{ staff.sno }}</td>
                    <td class="border border-gray-300 px-4 py-3 font-semibold">{{ staff.name }}</td>
                    <td class="border border-gray-300 px-4 py-3">{{ staff.designation }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">{{ staff.qualification }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">{{ staff.experience }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- PRT Teachers -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-purple-500 to-pink-500 text-white p-6">
            <h2 class="text-2xl font-bold">Primary Teachers (PRT)</h2>
            <p class="text-purple-100 mt-2">Primary Level (Classes I-V)</p>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full border-collapse border border-gray-300">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">S.No.</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Name</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Designation</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Qualification</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Experience (Years)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="staff in prtStaff" :key="staff.sno" class="hover:bg-gray-50">
                    <td class="border border-gray-300 px-4 py-3 text-center">{{ staff.sno }}</td>
                    <td class="border border-gray-300 px-4 py-3 font-semibold">{{ staff.name }}</td>
                    <td class="border border-gray-300 px-4 py-3">{{ staff.designation }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">{{ staff.qualification }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">{{ staff.experience }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- Non-Teaching Staff -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-gray-600 to-gray-700 text-white p-6">
            <h2 class="text-2xl font-bold">Non-Teaching Staff</h2>
            <p class="text-gray-200 mt-2">Administrative & Support Staff</p>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full border-collapse border border-gray-300">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">S.No.</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Name</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Designation</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Qualification</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Experience (Years)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="staff in nonTeachingStaff" :key="staff.sno" class="hover:bg-gray-50">
                    <td class="border border-gray-300 px-4 py-3 text-center">{{ staff.sno }}</td>
                    <td class="border border-gray-300 px-4 py-3 font-semibold">{{ staff.name }}</td>
                    <td class="border border-gray-300 px-4 py-3">{{ staff.designation }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">{{ staff.qualification }}</td>
                    <td class="border border-gray-300 px-4 py-3 text-center">{{ staff.experience }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <!-- CBSE Compliance Notice -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-indigo-500 to-blue-600 text-white p-6">
            <h2 class="text-2xl font-bold">CBSE Compliance</h2>
            <p class="text-indigo-100 mt-2">Mandatory Staff Information Disclosure</p>
          </div>
          <div class="p-6">
            <div class="bg-blue-50 rounded-lg p-4">
              <p class="text-gray-700 mb-4">
                As mandated by the Central Board of Secondary Education (CBSE), this page provides complete details 
                of all teaching and non-teaching staff members including their qualifications and experience.
              </p>
              <div class="grid md:grid-cols-2 gap-4 text-sm">
                <div>
                  <h4 class="font-semibold text-gray-800 mb-2">Staff Categories</h4>
                  <ul class="space-y-1 text-gray-600">
                    <li>• Principal: School Leadership</li>
                    <li>• PGT: Post Graduate Teachers (XI-XII)</li>
                    <li>• TGT: Trained Graduate Teachers (VI-X)</li>
                    <li>• PRT: Primary Teachers (I-V)</li>
                    <li>• Non-Teaching: Administrative Staff</li>
                  </ul>
                </div>
                <div>
                  <h4 class="font-semibold text-gray-800 mb-2">Qualification Standards</h4>
                  <ul class="space-y-1 text-gray-600">
                    <li>• All teachers are professionally qualified</li>
                    <li>• B.Ed. certification for teaching positions</li>
                    <li>• Subject-specific specialization</li>
                    <li>• Continuous professional development</li>
                    <li>• CBSE training and certification</li>
                  </ul>
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

interface StaffMember {
  sno: number
  name: string
  designation: string
  qualification: string
  experience: string
}

const staffData = ref<StaffMember[]>([])

// Computed properties for different staff categories
const principalStaff = computed(() => 
  staffData.value.filter(staff => staff.designation.toUpperCase().includes('PRINCIPAL'))
)

const pgtStaff = computed(() => 
  staffData.value.filter(staff => staff.designation.toUpperCase().includes('PGT'))
)

const tgtStaff = computed(() => 
  staffData.value.filter(staff => staff.designation.toUpperCase().includes('TGT'))
)

const prtStaff = computed(() => 
  staffData.value.filter(staff => 
    staff.designation.toUpperCase().includes('PRT') || 
    staff.designation.toUpperCase().includes('PTI')
  )
)

const nonTeachingStaff = computed(() => 
  staffData.value.filter(staff => 
    !staff.designation.toUpperCase().includes('PRINCIPAL') &&
    !staff.designation.toUpperCase().includes('PGT') &&
    !staff.designation.toUpperCase().includes('TGT') &&
    !staff.designation.toUpperCase().includes('PRT') &&
    !staff.designation.toUpperCase().includes('PTI')
  )
)

// Staff count statistics
const principalCount = computed(() => principalStaff.value.length)
const pgtCount = computed(() => pgtStaff.value.length)
const tgtCount = computed(() => tgtStaff.value.length)
const prtCount = computed(() => prtStaff.value.length)

// Load staff data from CSV
onMounted(async () => {
  try {
    const response = await fetch('/staff.csv')
    const csvText = await response.text()
    
    const lines = csvText.split('\n').filter(line => line.trim())
    // Skip header line
    
    staffData.value = lines.slice(1).map((line, index) => {
      // Split by comma but handle quoted fields properly
      const values = []
      let current = ''
      let inQuotes = false
      
      for (let i = 0; i < line.length; i++) {
        const char = line[i]
        if (char === '"') {
          inQuotes = !inQuotes
        } else if (char === ',' && !inQuotes) {
          values.push(current.trim())
          current = ''
        } else {
          current += char
        }
      }
      values.push(current.trim()) // Add the last value
      
      return {
        sno: parseInt(values[0]) || index + 1,
        name: values[1]?.replace(/"/g, '').trim() || '',
        designation: values[2]?.replace(/"/g, '').trim() || '',
        qualification: values[3]?.replace(/"/g, '').trim() || '',
        experience: values[4]?.replace(/"/g, '').trim() || ''
      }
    }).filter(staff => staff.name && staff.designation)
    
  } catch (error) {
    console.error('Error loading staff data:', error)
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
    background: #1e40af !important;
    color: white !important;
  }
}
</style>
