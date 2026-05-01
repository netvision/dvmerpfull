<template>
  <div class="transfer-certificate-page">
    <!-- Hero Section -->
    <div class="relative h-80 bg-gradient-to-r from-green-600 to-blue-600">
      <div class="absolute inset-0 bg-black opacity-30"></div>
      <div class="container mx-auto px-4 h-full flex items-center relative z-10">
        <div class="text-white">
          <h1 class="text-5xl font-bold mb-4">Transfer Certificate</h1>
          <p class="text-xl">TC Application Process & Guidelines</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-16">
      <!-- TC Application Process -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Transfer Certificate Application Process</h2>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <h3 class="text-2xl font-semibold text-blue-900 mb-6">Steps to Apply for TC</h3>
            <div class="space-y-6">
              <div class="flex items-start">
                <div class="bg-blue-100 text-blue-800 rounded-full w-8 h-8 flex items-center justify-center font-bold mr-4">1</div>
                <div>
                  <h4 class="font-semibold text-gray-800">Submit Application</h4>
                  <p class="text-gray-600 text-sm">Submit TC application form to the school office with required documents</p>
                </div>
              </div>
              <div class="flex items-start">
                <div class="bg-blue-100 text-blue-800 rounded-full w-8 h-8 flex items-center justify-center font-bold mr-4">2</div>
                <div>
                  <h4 class="font-semibold text-gray-800">Clear All Dues</h4>
                  <p class="text-gray-600 text-sm">Clear all pending fees and return library books/school property</p>
                </div>
              </div>
              <div class="flex items-start">
                <div class="bg-blue-100 text-blue-800 rounded-full w-8 h-8 flex items-center justify-center font-bold mr-4">3</div>
                <div>
                  <h4 class="font-semibold text-gray-800">Document Verification</h4>
                  <p class="text-gray-600 text-sm">School will verify student records and academic documents</p>
                </div>
              </div>
              <div class="flex items-start">
                <div class="bg-blue-100 text-blue-800 rounded-full w-8 h-8 flex items-center justify-center font-bold mr-4">4</div>
                <div>
                  <h4 class="font-semibold text-gray-800">TC Issuance</h4>
                  <p class="text-gray-600 text-sm">Transfer Certificate will be issued within 7 working days</p>
                </div>
              </div>
            </div>
          </div>
          <div>
            <img 
              src="https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=600&h=400&fit=crop" 
              alt="Document Processing" 
              class="w-full h-80 object-cover rounded-lg shadow-lg"
            />
          </div>
        </div>
      </div>

      <!-- Required Documents -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Required Documents</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div class="bg-blue-50 p-6 rounded-lg">
            <h4 class="text-xl font-semibold text-blue-900 mb-4">📄 Documents Required</h4>
            <ul class="space-y-3">
              <li class="flex items-center">
                <span class="text-green-600 mr-2">✓</span>
                <span>Duly filled TC application form</span>
              </li>
              <li class="flex items-center">
                <span class="text-green-600 mr-2">✓</span>
                <span>Original admission receipt</span>
              </li>
              <li class="flex items-center">
                <span class="text-green-600 mr-2">✓</span>
                <span>Fee clearance certificate</span>
              </li>
              <li class="flex items-center">
                <span class="text-green-600 mr-2">✓</span>
                <span>Library clearance certificate</span>
              </li>
              <li class="flex items-center">
                <span class="text-green-600 mr-2">✓</span>
                <span>Student ID card (if issued)</span>
              </li>
              <li class="flex items-center">
                <span class="text-green-600 mr-2">✓</span>
                <span>Reason for transfer (written)</span>
              </li>
            </ul>
          </div>
          <div class="bg-green-50 p-6 rounded-lg">
            <h4 class="text-xl font-semibold text-blue-900 mb-4">⏰ Processing Time</h4>
            <div class="space-y-4">
              <div class="flex justify-between border-b pb-2">
                <span class="font-semibold text-gray-700">Application Review:</span>
                <span class="text-gray-600">2-3 Days</span>
              </div>
              <div class="flex justify-between border-b pb-2">
                <span class="font-semibold text-gray-700">Document Verification:</span>
                <span class="text-gray-600">1-2 Days</span>
              </div>
              <div class="flex justify-between border-b pb-2">
                <span class="font-semibold text-gray-700">TC Preparation:</span>
                <span class="text-gray-600">1-2 Days</span>
              </div>
              <div class="flex justify-between border-b pb-2">
                <span class="font-semibold text-gray-700">Total Time:</span>
                <span class="text-gray-600 font-semibold">5-7 Working Days</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- TC Information -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Transfer Certificate Details</h2>
        <div class="bg-yellow-50 p-8 rounded-lg">
          <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
            <div>
              <h4 class="text-xl font-semibold text-blue-900 mb-4">Information Included in TC</h4>
              <ul class="space-y-2 text-gray-700">
                <li>• Student's full name and father's name</li>
                <li>• Date of birth (as per school records)</li>
                <li>• Class/Grade last attended</li>
                <li>• Date of admission and leaving</li>
                <li>• Academic performance summary</li>
                <li>• Character and conduct remarks</li>
                <li>• Reason for leaving</li>
                <li>• Fee dues status</li>
                <li>• School leaving date</li>
                <li>• Principal's signature and school seal</li>
              </ul>
            </div>
            <div>
              <h4 class="text-xl font-semibold text-blue-900 mb-4">Important Notes</h4>
              <div class="space-y-4">
                <div class="bg-white p-4 rounded-lg border-l-4 border-red-500">
                  <h5 class="font-semibold text-red-700 mb-2">⚠️ Validity</h5>
                  <p class="text-sm text-gray-600">TC is valid for admission in other schools as per CBSE guidelines</p>
                </div>
                <div class="bg-white p-4 rounded-lg border-l-4 border-blue-500">
                  <h5 class="font-semibold text-blue-700 mb-2">📋 Original Document</h5>
                  <p class="text-sm text-gray-600">TC is issued only once. Duplicate copies require special process</p>
                </div>
                <div class="bg-white p-4 rounded-lg border-l-4 border-green-500">
                  <h5 class="font-semibold text-green-700 mb-2">✅ Verification</h5>
                  <p class="text-sm text-gray-600">TC can be verified through school office for authenticity</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Download Section -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Download Forms</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-white p-6 rounded-lg shadow-md text-center">
            <div class="text-4xl mb-4">📄</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">TC Application Form</h4>
            <p class="text-gray-600 text-sm mb-4">Download the official Transfer Certificate application form</p>
            <a 
              href="#" 
              class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg text-sm transition-colors"
            >
              Download PDF
            </a>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-md text-center">
            <div class="text-4xl mb-4">📋</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">Document Checklist</h4>
            <p class="text-gray-600 text-sm mb-4">Complete checklist of required documents for TC</p>
            <a 
              href="#" 
              class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg text-sm transition-colors"
            >
              Download PDF
            </a>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-md text-center">
            <div class="text-4xl mb-4">ℹ️</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">TC Guidelines</h4>
            <p class="text-gray-600 text-sm mb-4">Detailed guidelines and procedures for TC application</p>
            <a 
              href="#" 
              class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg text-sm transition-colors"
            >
              Download PDF
            </a>
          </div>
        </div>
      </div>

      <!-- Contact for TC -->
      <div class="bg-gradient-to-r from-blue-900 to-purple-900 text-white p-8 rounded-lg">
        <h2 class="text-3xl font-bold mb-6 text-center">Contact for TC Related Queries</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="text-center">
            <div class="text-4xl mb-3">👨‍💼</div>
            <h4 class="text-lg font-semibold mb-2">Administrative Office</h4>
            <p class="text-sm text-blue-100">For TC application submission</p>
            <p class="text-sm text-blue-100">Office Hours: 9:00 AM - 4:00 PM</p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-3">📞</div>
            <h4 class="text-lg font-semibold mb-2">Phone</h4>
            <p class="text-sm text-blue-100">+91-11-2345-6789</p>
            <p class="text-sm text-blue-100">Ext: 101 (Admin)</p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-3">📧</div>
            <h4 class="text-lg font-semibold mb-2">Email</h4>
            <p class="text-sm text-blue-100">admin@dalmiavidyamandir.edu.in</p>
            <p class="text-sm text-blue-100">Response within 24 hours</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Transfer Certificate page component
</script>
