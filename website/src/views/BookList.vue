<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Hero Section -->
    <section class="bg-gradient-to-r from-green-600 to-blue-600 text-white py-16">
      <div class="container mx-auto px-4">
        <div class="text-center">
          <h1 class="text-4xl md:text-5xl font-bold mb-4">Book List</h1>
          <p class="text-xl md:text-2xl text-green-100">
            Academic Session 2025-26
          </p>
          <div class="mt-6">
            <a 
              href="/Book list For Session 2025-26.xlsx" 
              download
              class="inline-flex items-center px-6 py-3 bg-white text-green-600 rounded-full font-semibold hover:bg-green-50 transition-all duration-300 transform hover:scale-105"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
              </svg>
              Download Complete Book List (Excel)
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-12">
      <!-- Important Notice -->
      <div class="bg-yellow-50 border-l-4 border-yellow-400 p-6 mb-8 rounded-r-lg">
        <div class="flex">
          <div class="flex-shrink-0">
            <svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
          </div>
          <div class="ml-3">
            <h3 class="text-sm font-medium text-yellow-800">Important Instructions</h3>
            <div class="mt-2 text-sm text-yellow-700">
              <ul class="list-disc pl-5 space-y-1">
                <li>Ensure you buy the correct edition as specified in the list</li>
                <li>Second-hand books should be in good condition with all pages intact</li>
                <li>For any queries regarding books, contact the school office</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Class-wise Book Lists -->
      <div class="space-y-8">
        
        <!-- Pre-Primary Section -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-pink-500 to-purple-500 text-white p-6">
            <h2 class="text-2xl font-bold">Pre-Primary Section</h2>
            <p class="text-pink-100 mt-2">Nursery, LKG & UKG</p>
          </div>
          <div class="p-6">
            <div class="grid md:grid-cols-3 gap-6">
              
              <!-- Nursery -->
              <div class="bg-pink-50 rounded-lg p-4">
                <h3 class="text-lg font-bold text-pink-800 mb-4">Nursery</h3>
                
                <!-- Books Section -->
                <div class="mb-4">
                  <h4 class="text-sm font-semibold text-pink-700 mb-2">📚 Required Books</h4>
                  <div class="bg-white p-3 rounded border">
                    <h4 class="font-semibold text-sm text-gray-800">All Subjects (English, Math, EVS, Hindi, Art)</h4>
                    <p class="text-xs text-gray-600">LEARN WELL STEP-1</p>
                    <p class="text-xs text-gray-500">Publisher: Learn well India Pvt Ltd</p>
                  </div>
                </div>

                <!-- Notebooks & Stationery Section -->
                <div>
                  <h4 class="text-sm font-semibold text-pink-700 mb-2">📝 Notebooks & Stationery</h4>
                  <div class="space-y-2">
                    <div class="bg-white p-2 rounded border border-pink-200">
                      <div class="flex justify-between items-center">
                        <span class="text-xs font-medium text-gray-800">English - 4 lines notebook (120 pages)</span>
                        <span class="text-xs bg-pink-100 text-pink-800 px-2 py-1 rounded">Qty: 1</span>
                      </div>
                    </div>
                    <div class="bg-white p-2 rounded border border-pink-200">
                      <div class="flex justify-between items-center">
                        <span class="text-xs font-medium text-gray-800">Hindi - Single line notebook (120 pages)</span>
                        <span class="text-xs bg-pink-100 text-pink-800 px-2 py-1 rounded">Qty: 1</span>
                      </div>
                    </div>
                    <div class="bg-white p-2 rounded border border-pink-200">
                      <div class="flex justify-between items-center">
                        <span class="text-xs font-medium text-gray-800">Math - Square (24 boxes) 120 pages</span>
                        <span class="text-xs bg-pink-100 text-pink-800 px-2 py-1 rounded">Qty: 1</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Download CSV Link -->
                <div class="mt-3 pt-2 border-t border-pink-200">
                  <a 
                    href="/nursery-books.csv" 
                    download
                    class="text-xs text-pink-600 hover:text-pink-800 underline flex items-center"
                  >
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                    </svg>
                    Download Nursery List (CSV)
                  </a>
                </div>
              </div>

              <!-- LKG -->
              <div class="bg-purple-50 rounded-lg p-4">
                <h3 class="text-lg font-bold text-purple-800 mb-4">LKG</h3>
                
                <!-- Books Section -->
                <div class="mb-4">
                  <h4 class="text-sm font-semibold text-purple-700 mb-2">📚 Required Books</h4>
                  <div class="bg-white p-3 rounded border">
                    <h4 class="font-semibold text-sm text-gray-800">All Subjects (English, Math, EVS, Hindi, Art)</h4>
                    <p class="text-xs text-gray-600">LEARN WELL STEP-2</p>
                    <p class="text-xs text-gray-500">Publisher: Learn well India Pvt Ltd</p>
                  </div>
                </div>

                <!-- Notebooks & Stationery Section -->
                <div>
                  <h4 class="text-sm font-semibold text-purple-700 mb-2">📝 Notebooks & Stationery</h4>
                  <div class="space-y-2">
                    <div class="bg-white p-2 rounded border border-purple-200">
                      <div class="flex justify-between items-center">
                        <span class="text-xs font-medium text-gray-800">English - 4 lines notebook (120 pages)</span>
                        <span class="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">Qty: 1</span>
                      </div>
                    </div>
                    <div class="bg-white p-2 rounded border border-purple-200">
                      <div class="flex justify-between items-center">
                        <span class="text-xs font-medium text-gray-800">Hindi - Single line notebook (120 pages)</span>
                        <span class="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">Qty: 1</span>
                      </div>
                    </div>
                    <div class="bg-white p-2 rounded border border-purple-200">
                      <div class="flex justify-between items-center">
                        <span class="text-xs font-medium text-gray-800">Math - Square (24 boxes) 120 pages</span>
                        <span class="text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded">Qty: 1</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Download CSV Link -->
                <div class="mt-3 pt-2 border-t border-purple-200">
                  <a 
                    href="/lkg-books.csv" 
                    download
                    class="text-xs text-purple-600 hover:text-purple-800 underline flex items-center"
                  >
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                    </svg>
                    Download LKG List (CSV)
                  </a>
                </div>
              </div>

              <!-- UKG -->
              <div class="bg-indigo-50 rounded-lg p-4">
                <h3 class="text-lg font-bold text-indigo-800 mb-4">UKG</h3>
                
                <!-- Books Section -->
                <div class="mb-4">
                  <h4 class="text-sm font-semibold text-indigo-700 mb-2">📚 Required Books</h4>
                  <div class="bg-white p-3 rounded border">
                    <h4 class="font-semibold text-sm text-gray-800">All Subjects (English, Math, EVS, Hindi, Art)</h4>
                    <p class="text-xs text-gray-600">LEARN WELL STEP-3</p>
                    <p class="text-xs text-gray-500">Publisher: Learn well India Pvt Ltd</p>
                  </div>
                </div>

                <!-- Notebooks & Stationery Section -->
                <div>
                  <h4 class="text-sm font-semibold text-indigo-700 mb-2">📝 Notebooks & Stationery</h4>
                  <div class="space-y-2">
                    <div class="bg-white p-2 rounded border border-indigo-200">
                      <div class="flex justify-between items-center">
                        <span class="text-xs font-medium text-gray-800">English - 4 lines notebook (120 pages)</span>
                        <span class="text-xs bg-indigo-100 text-indigo-800 px-2 py-1 rounded">Qty: 2</span>
                      </div>
                    </div>
                    <div class="bg-white p-2 rounded border border-indigo-200">
                      <div class="flex justify-between items-center">
                        <span class="text-xs font-medium text-gray-800">Hindi - Single line notebook (120 pages)</span>
                        <span class="text-xs bg-indigo-100 text-indigo-800 px-2 py-1 rounded">Qty: 1</span>
                      </div>
                    </div>
                    <div class="bg-white p-2 rounded border border-indigo-200">
                      <div class="flex justify-between items-center">
                        <span class="text-xs font-medium text-gray-800">Math - Square (24 boxes) 120 pages</span>
                        <span class="text-xs bg-indigo-100 text-indigo-800 px-2 py-1 rounded">Qty: 1</span>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Download CSV Link -->
                <div class="mt-3 pt-2 border-t border-indigo-200">
                  <a 
                    href="/ukg-books.csv" 
                    download
                    class="text-xs text-indigo-600 hover:text-indigo-800 underline flex items-center"
                  >
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                    </svg>
                    Download UKG List (CSV)
                  </a>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Primary Section -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-green-500 to-blue-500 text-white p-6">
            <h2 class="text-2xl font-bold">Primary Section (Class I - V)</h2>
            <p class="text-green-100 mt-2">Core Subject Books</p>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full border-collapse border border-gray-300">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Class</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Subject</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Book Title</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Publisher</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">ISBN</th>
                  </tr>
                </thead>
                <tbody>
                  <!-- Class I -->
                  <tr>
                    <td class="border border-gray-300 px-4 py-3 font-semibold bg-blue-50" rowspan="9">Class I</td>
                    <td class="border border-gray-300 px-4 py-3">English</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Mridang-1</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">English Grammar</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Learner's English Grammar & Composition 1</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">S. Chand</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">English Writing</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Cursive Writing 1</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Wings</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">EVS</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Environmental studies 1</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Viva Education</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Mathematics</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Joyful Mathematics 1</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Sarangi 1</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi Grammar</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Vishesh Hindi Vyakaran thatha Rachna 1</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">AMANDA</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi Writing</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Sulekh Tara 1</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Wings</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Art & Craft</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Exploring spread colours 1</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Learn Well</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  
                  <!-- Class II -->
                  <tr>
                    <td class="border border-gray-300 px-4 py-3 font-semibold bg-green-50" rowspan="9">Class II</td>
                    <td class="border border-gray-300 px-4 py-3">English</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Mridang-2</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">English Grammar</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Learner's English Grammar & Composition 2</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">S. Chand</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">English Writing</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Cursive Writing 2</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Wings</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">EVS</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Environmental studies 2</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Viva Education</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Mathematics</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Joyful Mathematics 2</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Sarangi 2</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi Grammar</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Vishesh Hindi Vyakaran thatha Rachna 2</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">AMANDA</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi Writing</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Sulekh Tara 2</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Wings</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Art & Craft</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Exploring spread colours 2</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Learn Well</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>

                  <!-- Class III -->
                  <tr>
                    <td class="border border-gray-300 px-4 py-3 font-semibold bg-yellow-50" rowspan="11">Class III</td>
                    <td class="border border-gray-300 px-4 py-3">English</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">SANTOOR</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">English Grammar</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Learner's English Grammar & Composition 3</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">S. Chand</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">English Writing</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Cursive Writing 3</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Wings</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">EVS</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">OUR WONDEROUS WORLD</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Mathematics</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Math MELA</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">VEENA</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi Writing</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Sulekh Tara</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Wings</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi Grammar</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Vishesh Hindi Vyakaran thatha Rachna 3</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">AMANDA</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Computer</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Step to Success Computer Book</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Purple leaf Pub.</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Art & Craft</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Exploring Spread Colour</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Learn Well</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Oral Sanskrit</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Snskrit Dipiti Praveshika</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Megha Mind Pvt. Ltd.</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>

                  <!-- Class IV -->
                  <tr>
                    <td class="border border-gray-300 px-4 py-3 font-semibold bg-orange-50" rowspan="11">Class IV</td>
                    <td class="border border-gray-300 px-4 py-3">English</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Marigold -4</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">English Grammar</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Learner's English Grammar & Composition 4</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">S. Chand</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">English Writing</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Cursive Writing 4</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Wings</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">EVS</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Looking Around - 4</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Mathematics</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Math Magic -4</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Rimjhim -4</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi Writing</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Sulekh Tara</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Wings</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi Grammar</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Vishesh Hindi Vyakaran thatha Rachna 4</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">AMANDA</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Computer</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Step to Success Computer Book</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Purple leaf Pub.</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Art & Craft</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Exploring Spread Colour</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Learn Well</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Oral Sanskrit</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Sanskrit Dipiti Part 1</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Megha Mind Pvt. Ltd.</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>

                  <!-- Class V -->
                  <tr>
                    <td class="border border-gray-300 px-4 py-3 font-semibold bg-purple-50" rowspan="11">Class V</td>
                    <td class="border border-gray-300 px-4 py-3">English</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Marigold -5</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">English Grammar</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Learner's English Grammar & Composition 5</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">S. Chand</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">English Writing</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Cursive Writing 5</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Wings</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">EVS</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Looking Around - 5</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Mathematics</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Math Magic -5</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Rimjhim -5</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi Writing</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Sulekh Tara</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Wings</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi Grammar</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Vishesh Hindi Vyakaran thatha Rachna 5</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">AMANDA</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Computer</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Step to Success Computer Book</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Purple leaf Pub.</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Art & Craft</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Exploring Spread Colour</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Learn Well</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Oral Sanskrit</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Sanskrut Dipiti Part 2</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Megha Mind Pvt. Ltd.</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="mt-4 text-sm text-gray-600">
              <p><strong>Note:</strong> This table shows detailed book information for all primary classes. Individual CSV downloads are available below.</p>
            </div>

            <!-- Primary Classes Download Links -->
            <div class="mt-6 grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-3">
              <a href="/class_i.csv" download class="flex items-center justify-center px-3 py-2 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors text-sm font-medium">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                </svg>
                Class I
              </a>
              <a href="/class_ii.csv" download class="flex items-center justify-center px-3 py-2 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors text-sm font-medium">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                </svg>
                Class II
              </a>
              <a href="/class_iii.csv" download class="flex items-center justify-center px-3 py-2 bg-yellow-100 text-yellow-700 rounded-lg hover:bg-yellow-200 transition-colors text-sm font-medium">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                </svg>
                Class III
              </a>
              <a href="/class_iv.csv" download class="flex items-center justify-center px-3 py-2 bg-orange-100 text-orange-700 rounded-lg hover:bg-orange-200 transition-colors text-sm font-medium">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                </svg>
                Class IV
              </a>
              <a href="/class_v.csv" download class="flex items-center justify-center px-3 py-2 bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 transition-colors text-sm font-medium">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                </svg>
                Class V
              </a>
            </div>

            <!-- Class I Notebooks Section -->
            <div class="mt-6 bg-blue-50 rounded-lg p-4">
              <h3 class="text-lg font-bold text-blue-800 mb-3">📝 Class I - Notebooks & Stationery</h3>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
                <div class="bg-white p-3 rounded border border-blue-200">
                  <div class="flex justify-between items-center">
                    <span class="text-sm font-medium text-gray-800">4 line notebook (120 pages)</span>
                    <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">Qty: 2</span>
                  </div>
                </div>
                <div class="bg-white p-3 rounded border border-blue-200">
                  <div class="flex justify-between items-center">
                    <span class="text-sm font-medium text-gray-800">Single ruled (120 pages)</span>
                    <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">Qty: 1</span>
                  </div>
                </div>
                <div class="bg-white p-3 rounded border border-blue-200">
                  <div class="flex justify-between items-center">
                    <span class="text-sm font-medium text-gray-800">Square Box Notebook (120 pages)</span>
                    <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">Qty: 1</span>
                  </div>
                </div>
                <div class="bg-white p-3 rounded border border-blue-200">
                  <div class="flex justify-between items-center">
                    <span class="text-sm font-medium text-gray-800">Drawing Note book</span>
                    <span class="text-xs bg-blue-100 text-blue-800 px-2 py-1 rounded">Qty: 1</span>
                  </div>
                </div>
              </div>
              <div class="mt-3 pt-2 border-t border-blue-200">
                <a 
                  href="/i-books.csv" 
                  download
                  class="text-xs text-blue-600 hover:text-blue-800 underline flex items-center"
                >
                  <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                  </svg>
                  Download Class I List (CSV)
                </a>
              </div>
            </div>
          </div>
        </section>

        <!-- Secondary Section -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-orange-500 to-red-500 text-white p-6">
            <h2 class="text-2xl font-bold">Secondary Section (Class VI - X)</h2>
            <p class="text-orange-100 mt-2">CBSE Curriculum Books</p>
          </div>
          <div class="p-6">
            <div class="overflow-x-auto">
              <table class="w-full border-collapse border border-gray-300">
                <thead>
                  <tr class="bg-gray-50">
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Class</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Subject</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Book Title</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">Publisher</th>
                    <th class="border border-gray-300 px-4 py-3 text-left font-bold">ISBN</th>
                  </tr>
                </thead>
                <tbody>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3 font-semibold bg-orange-50" rowspan="10">Class VI</td>
                    <td class="border border-gray-300 px-4 py-3">English</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">POORVI</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">English Grammar</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Learner's English Grammar & Composition 6</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">S. Chand</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Mathematics</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">GANIT PRAKASH</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">MALHAR</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Hindi Grammar</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Nav Tarang 6</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Rohan Books</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Science</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">CURIOSITY</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Social Science</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">EXPLORING SOCIETY & INDIA BEYOND</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Sanskrit</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">DEEPAKAM</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">NCERT</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Computer</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Step to Success Computer Book</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Purple leaf Pub.</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                  <tr>
                    <td class="border border-gray-300 px-4 py-3">Art & Craft</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Exploring Spread Colours</td>
                    <td class="border border-gray-300 px-4 py-3 text-sm">Learnwell Publication</td>
                    <td class="border border-gray-300 px-4 py-3 text-xs">-</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <div class="mt-4 text-sm text-gray-600">
              <p><strong>Note:</strong> Complete book lists for Classes VII-X are available in individual CSV downloads below.</p>
            </div>

            <!-- Download Links for Secondary Classes -->
            <div class="mt-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <a href="/class_vi.csv" download class="flex items-center justify-center px-4 py-3 bg-orange-100 text-orange-700 rounded-lg hover:bg-orange-200 transition-colors text-sm font-medium">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                </svg>
                Class VI List
              </a>
              <a href="/class_vii.csv" download class="flex items-center justify-center px-4 py-3 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 transition-colors text-sm font-medium">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                </svg>
                Class VII List
              </a>
              <a href="/class_viii.csv" download class="flex items-center justify-center px-4 py-3 bg-yellow-100 text-yellow-700 rounded-lg hover:bg-yellow-200 transition-colors text-sm font-medium">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                </svg>
                Class VIII List
              </a>
              <a href="/class_ix.csv" download class="flex items-center justify-center px-4 py-3 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors text-sm font-medium">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                </svg>
                Class IX List
              </a>
              <a href="/class_x.csv" download class="flex items-center justify-center px-4 py-3 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors text-sm font-medium">
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                </svg>
                Class X List
              </a>
            </div>
          </div>
        </section>

        <!-- Senior Secondary Section -->
        <section class="bg-white rounded-xl shadow-lg border border-gray-200 overflow-hidden">
          <div class="bg-gradient-to-r from-purple-600 to-indigo-600 text-white p-6">
            <h2 class="text-2xl font-bold">Senior Secondary (Class XI - XII)</h2>
            <p class="text-purple-100 mt-2">Stream-wise Book Lists</p>
          </div>
          <div class="p-6">
            <div class="grid md:grid-cols-3 gap-6">
              
              <!-- Science Stream -->
              <div class="bg-blue-50 rounded-lg p-4">
                <h3 class="text-lg font-bold text-blue-800 mb-4">Science Stream</h3>
                <div class="space-y-3">
                  <div class="bg-white p-3 rounded border border-blue-200">
                    <h4 class="font-semibold text-sm text-gray-800">English</h4>
                    <p class="text-xs text-gray-600">Hornbill & Snapshot</p>
                    <p class="text-xs text-gray-500">NCERT Publications</p>
                  </div>
                  <div class="bg-white p-3 rounded border border-blue-200">
                    <h4 class="font-semibold text-sm text-gray-800">Physics</h4>
                    <p class="text-xs text-gray-600">Physics Part I & II</p>
                    <p class="text-xs text-gray-600">Comprehensive Lab Manual</p>
                    <p class="text-xs text-gray-500">NCERT & Rachana Sagar</p>
                  </div>
                  <div class="bg-white p-3 rounded border border-blue-200">
                    <h4 class="font-semibold text-sm text-gray-800">Chemistry</h4>
                    <p class="text-xs text-gray-600">Chemistry Part I & II</p>
                    <p class="text-xs text-gray-600">Lab Manual Chemistry</p>
                    <p class="text-xs text-gray-500">NCERT & Rachana Sagar</p>
                  </div>
                  <div class="bg-white p-3 rounded border border-blue-200">
                    <h4 class="font-semibold text-sm text-gray-800">Mathematics</h4>
                    <p class="text-xs text-gray-600">Mathematics</p>
                    <p class="text-xs text-gray-500">NCERT Publications</p>
                  </div>
                  <div class="bg-white p-3 rounded border border-blue-200">
                    <h4 class="font-semibold text-sm text-gray-800">Biology</h4>
                    <p class="text-xs text-gray-600">Biology</p>
                    <p class="text-xs text-gray-600">Comprehensive Biology Lab Manual</p>
                    <p class="text-xs text-gray-500">NCERT & Laxmi Publication</p>
                  </div>
                </div>
                <div class="mt-4">
                  <a href="/class_xi_science.csv" download class="text-xs text-blue-600 hover:text-blue-800 underline flex items-center">
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                    </svg>
                    Download Science List (CSV)
                  </a>
                </div>
              </div>

              <!-- Commerce Stream -->
              <div class="bg-green-50 rounded-lg p-4">
                <h3 class="text-lg font-bold text-green-800 mb-4">Commerce Stream</h3>
                <div class="space-y-3">
                  <div class="bg-white p-3 rounded border border-green-200">
                    <h4 class="font-semibold text-sm text-gray-800">English</h4>
                    <p class="text-xs text-gray-600">Hornbill & Snapshot</p>
                    <p class="text-xs text-gray-500">NCERT Publications</p>
                  </div>
                  <div class="bg-white p-3 rounded border border-green-200">
                    <h4 class="font-semibold text-sm text-gray-800">Accountancy</h4>
                    <p class="text-xs text-gray-600">Accountancy Part I & II</p>
                    <p class="text-xs text-gray-600">APC Books</p>
                    <p class="text-xs text-gray-500">NCERT & D K Goel</p>
                  </div>
                  <div class="bg-white p-3 rounded border border-green-200">
                    <h4 class="font-semibold text-sm text-gray-800">Business Studies</h4>
                    <p class="text-xs text-gray-600">Business Studies</p>
                    <p class="text-xs text-gray-500">NCERT/VK</p>
                  </div>
                  <div class="bg-white p-3 rounded border border-green-200">
                    <h4 class="font-semibold text-sm text-gray-800">Economics</h4>
                    <p class="text-xs text-gray-600">Intro Micro Economics</p>
                    <p class="text-xs text-gray-600">Statistics</p>
                    <p class="text-xs text-gray-500">Genius Publication</p>
                  </div>
                  <div class="bg-white p-3 rounded border border-green-200">
                    <h4 class="font-semibold text-sm text-gray-800">Mathematics</h4>
                    <p class="text-xs text-gray-600">Mathematics</p>
                    <p class="text-xs text-gray-500">NCERT Publications</p>
                  </div>
                </div>
                <div class="mt-4">
                  <a href="/class_xi_commerce.csv" download class="text-xs text-green-600 hover:text-green-800 underline flex items-center">
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                    </svg>
                    Download Commerce List (CSV)
                  </a>
                </div>
              </div>

              <!-- Humanities Stream -->
              <div class="bg-purple-50 rounded-lg p-4">
                <h3 class="text-lg font-bold text-purple-800 mb-4">Humanities Stream</h3>
                <div class="space-y-3">
                  <div class="bg-white p-3 rounded border border-purple-200">
                    <h4 class="font-semibold text-sm text-gray-800">English</h4>
                    <p class="text-xs text-gray-600">Hornbill & Snapshot</p>
                    <p class="text-xs text-gray-500">NCERT Publications</p>
                  </div>
                  <div class="bg-white p-3 rounded border border-purple-200">
                    <h4 class="font-semibold text-sm text-gray-800">History</h4>
                    <p class="text-xs text-gray-600">Themes in World History XI</p>
                    <p class="text-xs text-gray-500">NCERT Publications</p>
                  </div>
                  <div class="bg-white p-3 rounded border border-purple-200">
                    <h4 class="font-semibold text-sm text-gray-800">Political Science</h4>
                    <p class="text-xs text-gray-600">Indian Constitution at work XI</p>
                    <p class="text-xs text-gray-600">Political Theory XI</p>
                    <p class="text-xs text-gray-500">NCERT Publications</p>
                  </div>
                  <div class="bg-white p-3 rounded border border-purple-200">
                    <h4 class="font-semibold text-sm text-gray-800">Economics</h4>
                    <p class="text-xs text-gray-600">Intro Micro Economics</p>
                    <p class="text-xs text-gray-600">Statistics</p>
                    <p class="text-xs text-gray-500">Genius Publication</p>
                  </div>
                </div>
                <div class="mt-4">
                  <a href="/class_xi_humanities.csv" download class="text-xs text-purple-600 hover:text-purple-800 underline flex items-center">
                    <svg class="w-3 h-3 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                    </svg>
                    Download Humanities List (CSV)
                  </a>
                </div>
              </div>
            </div>

            <!-- Class XII Downloads -->
            <div class="mt-8 bg-gray-50 rounded-lg p-6">
              <h3 class="text-lg font-bold text-gray-800 mb-4">📚 Class XII Book Lists</h3>
              <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <a href="/class_xii_science.csv" download class="flex items-center justify-center px-4 py-3 bg-blue-100 text-blue-700 rounded-lg hover:bg-blue-200 transition-colors text-sm font-medium">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                  </svg>
                  Class XII Science
                </a>
                <a href="/class_xii_commerce.csv" download class="flex items-center justify-center px-4 py-3 bg-green-100 text-green-700 rounded-lg hover:bg-green-200 transition-colors text-sm font-medium">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                  </svg>
                  Class XII Commerce
                </a>
                <a href="/class_xii_humanities.csv" download class="flex items-center justify-center px-4 py-3 bg-purple-100 text-purple-700 rounded-lg hover:bg-purple-200 transition-colors text-sm font-medium">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3M3 17V7a2 2 0 012-2h6l2 2h6a2 2 0 012 2v10a2 2 0 01-2-2H5a2 2 0 01-2-2z" />
                  </svg>
                  Class XII Humanities
                </a>
              </div>
            </div>
          </div>
        </section>

        

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Book List page for Dalmia Vidya Mandir
// Academic Session 2025-26
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
</style>
