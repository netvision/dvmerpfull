<template>
  <div class="annual-report-page">
    <!-- Hero Section -->
    <div class="relative h-80 bg-gradient-to-r from-blue-800 to-indigo-900">
      <div class="absolute inset-0 bg-black opacity-30"></div>
      <div class="container mx-auto px-4 h-full flex items-center relative z-10">
        <div class="text-white">
          <h1 class="text-5xl font-bold mb-4">Annual Report</h1>
          <p class="text-xl">Academic Year 2023-24 - Comprehensive School Performance</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-16">
      <!-- Executive Summary -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Executive Summary</h2>
        <div class="bg-blue-50 p-8 rounded-lg">
          <p class="text-lg text-gray-700 leading-relaxed mb-6">
            The Academic Year 2023-24 has been a year of remarkable achievements and continued excellence at Dalmia Vidya Mandir. 
            Despite global challenges, our institution has maintained its commitment to providing quality education while adapting 
            to modern teaching methodologies and technology integration.
          </p>
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6 text-center">
            <div class="bg-white p-4 rounded-lg">
              <div class="text-3xl font-bold text-blue-900">2,450</div>
              <div class="text-sm text-gray-600">Total Students</div>
            </div>
            <div class="bg-white p-4 rounded-lg">
              <div class="text-3xl font-bold text-green-900">98.5%</div>
              <div class="text-sm text-gray-600">Overall Pass Rate</div>
            </div>
            <div class="bg-white p-4 rounded-lg">
              <div class="text-3xl font-bold text-purple-900">120</div>
              <div class="text-sm text-gray-600">Teaching Staff</div>
            </div>
            <div class="bg-white p-4 rounded-lg">
              <div class="text-3xl font-bold text-orange-900">95%</div>
              <div class="text-sm text-gray-600">Parent Satisfaction</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Academic Performance -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Academic Performance 2023-24</h2>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <!-- Board Results -->
          <div class="bg-green-50 p-6 rounded-lg">
            <h4 class="text-xl font-semibold text-blue-900 mb-4">📊 CBSE Board Results</h4>
            <div class="space-y-4">
              <div class="border-b pb-3">
                <h5 class="font-semibold text-gray-800 mb-2">Class X (2024)</h5>
                <div class="grid grid-cols-2 gap-4 text-sm">
                  <div>Students Appeared: <span class="font-semibold">245</span></div>
                  <div>Pass Percentage: <span class="font-semibold text-green-600">98.5%</span></div>
                  <div>Distinction (90%+): <span class="font-semibold">45 students</span></div>
                  <div>First Class (75%+): <span class="font-semibold">165 students</span></div>
                </div>
              </div>
              <div>
                <h5 class="font-semibold text-gray-800 mb-2">Class XII (2024)</h5>
                <div class="grid grid-cols-2 gap-4 text-sm">
                  <div>Students Appeared: <span class="font-semibold">220</span></div>
                  <div>Pass Percentage: <span class="font-semibold text-green-600">96.2%</span></div>
                  <div>Distinction (90%+): <span class="font-semibold">38 students</span></div>
                  <div>First Class (75%+): <span class="font-semibold">142 students</span></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Subject-wise Performance -->
          <div class="bg-blue-50 p-6 rounded-lg">
            <h4 class="text-xl font-semibold text-blue-900 mb-4">📚 Subject-wise Excellence</h4>
            <div class="space-y-3">
              <div class="flex justify-between items-center border-b pb-2">
                <span class="text-gray-700">Mathematics</span>
                <span class="font-semibold text-blue-600">95.8% Pass Rate</span>
              </div>
              <div class="flex justify-between items-center border-b pb-2">
                <span class="text-gray-700">Science</span>
                <span class="font-semibold text-blue-600">97.2% Pass Rate</span>
              </div>
              <div class="flex justify-between items-center border-b pb-2">
                <span class="text-gray-700">English</span>
                <span class="font-semibold text-blue-600">98.9% Pass Rate</span>
              </div>
              <div class="flex justify-between items-center border-b pb-2">
                <span class="text-gray-700">Social Science</span>
                <span class="font-semibold text-blue-600">96.5% Pass Rate</span>
              </div>
              <div class="flex justify-between items-center">
                <span class="text-gray-700">Hindi</span>
                <span class="font-semibold text-blue-600">99.1% Pass Rate</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Infrastructure Development -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Infrastructure Development</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-white p-6 rounded-lg shadow-md">
            <div class="text-4xl mb-4">🏗️</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">New Facilities Added</h4>
            <ul class="text-gray-700 text-sm space-y-2">
              <li>• AV Room for Remote Interactive Teaching</li>
              <li>• Upgraded Science Laboratory Equipment</li>
              <li>• Enhanced CCTV Security System</li>
              <li>• Solar Power Installation (Phase 1)</li>
              <li>• Library Digital Resources Expansion</li>
            </ul>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-md">
            <div class="text-4xl mb-4">💰</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">Infrastructure Investment</h4>
            <div class="space-y-2 text-sm">
              <div class="flex justify-between">
                <span class="text-gray-700">Technology Upgrades:</span>
                <span class="font-semibold">₹15,00,000</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-700">Security Systems:</span>
                <span class="font-semibold">₹8,50,000</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-700">Laboratory Equipment:</span>
                <span class="font-semibold">₹12,00,000</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-700">Green Energy:</span>
                <span class="font-semibold">₹20,00,000</span>
              </div>
              <div class="flex justify-between border-t pt-2 font-semibold">
                <span class="text-gray-800">Total Investment:</span>
                <span class="text-blue-900">₹55,50,000</span>
              </div>
            </div>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-md">
            <div class="text-4xl mb-4">🔮</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">Upcoming Projects</h4>
            <ul class="text-gray-700 text-sm space-y-2">
              <li>• Innovation Lab Setup</li>
              <li>• Sports Complex Renovation</li>
              <li>• Digital Classroom Expansion</li>
              <li>• Rainwater Harvesting System</li>
              <li>• Campus Wi-Fi Enhancement</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Student Activities & Achievements -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Student Activities & Achievements</h2>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div class="bg-yellow-50 p-6 rounded-lg">
            <h4 class="text-xl font-semibold text-blue-900 mb-4">🏆 Awards & Recognition</h4>
            <div class="space-y-3">
              <div class="border-l-4 border-yellow-500 pl-4">
                <h5 class="font-semibold text-gray-800">National Science Olympiad</h5>
                <p class="text-sm text-gray-600">15 students qualified for national level, 3 gold medals</p>
              </div>
              <div class="border-l-4 border-blue-500 pl-4">
                <h5 class="font-semibold text-gray-800">Inter-School Debate Competition</h5>
                <p class="text-sm text-gray-600">First Prize in Regional Level Championship</p>
              </div>
              <div class="border-l-4 border-green-500 pl-4">
                <h5 class="font-semibold text-gray-800">Sports Excellence</h5>
                <p class="text-sm text-gray-600">State Level Champions in Basketball & Athletics</p>
              </div>
              <div class="border-l-4 border-purple-500 pl-4">
                <h5 class="font-semibold text-gray-800">Cultural Programs</h5>
                <p class="text-sm text-gray-600">Best Performance Award in District Cultural Festival</p>
              </div>
            </div>
          </div>
          <div class="bg-green-50 p-6 rounded-lg">
            <h4 class="text-xl font-semibold text-blue-900 mb-4">📈 Participation Statistics</h4>
            <div class="space-y-4">
              <div class="grid grid-cols-2 gap-4">
                <div class="text-center bg-white p-3 rounded">
                  <div class="text-2xl font-bold text-green-900">450</div>
                  <div class="text-xs text-gray-600">Sports Participants</div>
                </div>
                <div class="text-center bg-white p-3 rounded">
                  <div class="text-2xl font-bold text-blue-900">320</div>
                  <div class="text-xs text-gray-600">Cultural Activities</div>
                </div>
              </div>
              <div class="grid grid-cols-2 gap-4">
                <div class="text-center bg-white p-3 rounded">
                  <div class="text-2xl font-bold text-purple-900">180</div>
                  <div class="text-xs text-gray-600">Science Projects</div>
                </div>
                <div class="text-center bg-white p-3 rounded">
                  <div class="text-2xl font-bold text-orange-900">250</div>
                  <div class="text-xs text-gray-600">Community Service</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Faculty Development -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Faculty Development & Training</h2>
        <div class="bg-purple-50 p-8 rounded-lg">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h4 class="text-xl font-semibold text-blue-900 mb-4">👨‍🏫 Training Programs Conducted</h4>
              <ul class="space-y-3">
                <li class="flex items-start">
                  <span class="text-green-600 mr-2">✓</span>
                  <div>
                    <span class="font-semibold">CBSE Curriculum Training</span>
                    <p class="text-sm text-gray-600">85 teachers participated in latest curriculum updates</p>
                  </div>
                </li>
                <li class="flex items-start">
                  <span class="text-green-600 mr-2">✓</span>
                  <div>
                    <span class="font-semibold">Digital Teaching Methods</span>
                    <p class="text-sm text-gray-600">Technology integration workshop for 60 faculty members</p>
                  </div>
                </li>
                <li class="flex items-start">
                  <span class="text-green-600 mr-2">✓</span>
                  <div>
                    <span class="font-semibold">Student Psychology & Counseling</span>
                    <p class="text-sm text-gray-600">Specialized training for student guidance counselors</p>
                  </div>
                </li>
                <li class="flex items-start">
                  <span class="text-green-600 mr-2">✓</span>
                  <div>
                    <span class="font-semibold">Remote Teaching Certification</span>
                    <p class="text-sm text-gray-600">AV Room operation and remote guest faculty coordination</p>
                  </div>
                </li>
              </ul>
            </div>
            <div>
              <h4 class="text-xl font-semibold text-blue-900 mb-4">📊 Faculty Statistics</h4>
              <div class="space-y-4">
                <div class="bg-white p-4 rounded-lg">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-700">Post Graduate Teachers:</span>
                    <span class="font-semibold text-blue-600">95 (79%)</span>
                  </div>
                </div>
                <div class="bg-white p-4 rounded-lg">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-700">B.Ed Qualified:</span>
                    <span class="font-semibold text-blue-600">118 (98%)</span>
                  </div>
                </div>
                <div class="bg-white p-4 rounded-lg">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-700">Technology Certified:</span>
                    <span class="font-semibold text-blue-600">105 (88%)</span>
                  </div>
                </div>
                <div class="bg-white p-4 rounded-lg">
                  <div class="flex justify-between items-center">
                    <span class="text-gray-700">Years of Experience (Avg):</span>
                    <span class="font-semibold text-blue-600">12.5 years</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Financial Summary -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Financial Summary 2023-24</h2>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div class="bg-blue-50 p-6 rounded-lg">
            <h4 class="text-xl font-semibold text-blue-900 mb-4">💰 Revenue Sources</h4>
            <div class="space-y-3">
              <div class="flex justify-between items-center border-b pb-2">
                <span class="text-gray-700">Tuition Fees</span>
                <span class="font-semibold text-green-600">₹8.5 Crores</span>
              </div>
              <div class="flex justify-between items-center border-b pb-2">
                <span class="text-gray-700">Development Fees</span>
                <span class="font-semibold text-green-600">₹1.2 Crores</span>
              </div>
              <div class="flex justify-between items-center border-b pb-2">
                <span class="text-gray-700">Transport Fees</span>
                <span class="font-semibold text-green-600">₹85 Lakhs</span>
              </div>
              <div class="flex justify-between items-center border-b pb-2">
                <span class="text-gray-700">Other Income</span>
                <span class="font-semibold text-green-600">₹35 Lakhs</span>
              </div>
              <div class="flex justify-between items-center font-semibold text-lg border-t pt-2">
                <span class="text-gray-800">Total Revenue</span>
                <span class="text-blue-900">₹10.7 Crores</span>
              </div>
            </div>
          </div>
          <div class="bg-red-50 p-6 rounded-lg">
            <h4 class="text-xl font-semibold text-blue-900 mb-4">💸 Expenditure Breakdown</h4>
            <div class="space-y-3">
              <div class="flex justify-between items-center border-b pb-2">
                <span class="text-gray-700">Staff Salaries & Benefits</span>
                <span class="font-semibold text-red-600">₹6.2 Crores</span>
              </div>
              <div class="flex justify-between items-center border-b pb-2">
                <span class="text-gray-700">Infrastructure & Maintenance</span>
                <span class="font-semibold text-red-600">₹1.8 Crores</span>
              </div>
              <div class="flex justify-between items-center border-b pb-2">
                <span class="text-gray-700">Educational Materials</span>
                <span class="font-semibold text-red-600">₹95 Lakhs</span>
              </div>
              <div class="flex justify-between items-center border-b pb-2">
                <span class="text-gray-700">Administrative Expenses</span>
                <span class="font-semibold text-red-600">₹75 Lakhs</span>
              </div>
              <div class="flex justify-between items-center font-semibold text-lg border-t pt-2">
                <span class="text-gray-800">Total Expenditure</span>
                <span class="text-red-900">₹9.7 Crores</span>
              </div>
            </div>
          </div>
        </div>
        <div class="mt-6 bg-green-100 p-4 rounded-lg text-center">
          <span class="text-lg font-semibold text-green-800">Net Surplus: ₹1.0 Crore (Allocated to Development Fund)</span>
        </div>
      </div>

      <!-- Future Plans -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Strategic Plan 2024-25</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div class="bg-blue-100 p-6 rounded-lg">
            <div class="text-4xl mb-4">🎯</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">Academic Excellence</h4>
            <ul class="text-gray-700 text-sm space-y-1">
              <li>• Target 99% pass rate in board exams</li>
              <li>• Expand remote expert teaching program</li>
              <li>• Introduce AI-based learning modules</li>
              <li>• Enhance competitive exam preparation</li>
            </ul>
          </div>
          <div class="bg-green-100 p-6 rounded-lg">
            <div class="text-4xl mb-4">🏗️</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">Infrastructure Development</h4>
            <ul class="text-gray-700 text-sm space-y-1">
              <li>• Complete Innovation Lab setup</li>
              <li>• Upgrade playground facilities</li>
              <li>• Install complete solar power system</li>
              <li>• Enhance digital library resources</li>
            </ul>
          </div>
          <div class="bg-yellow-100 p-6 rounded-lg">
            <div class="text-4xl mb-4">👥</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">Community Engagement</h4>
            <ul class="text-gray-700 text-sm space-y-1">
              <li>• Strengthen parent-teacher collaboration</li>
              <li>• Expand alumni network programs</li>
              <li>• Increase community service initiatives</li>
              <li>• Develop industry partnerships</li>
            </ul>
          </div>
        </div>
      </div>

      <!-- Download Reports -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Download Detailed Reports</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-white p-6 rounded-lg shadow-md text-center">
            <div class="text-4xl mb-4">📊</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">Complete Annual Report</h4>
            <p class="text-gray-600 text-sm mb-4">Comprehensive report with all details and statistics</p>
            <a 
              href="#" 
              class="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg text-sm transition-colors"
            >
              Download PDF (2.5 MB)
            </a>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-md text-center">
            <div class="text-4xl mb-4">📈</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">Academic Performance Report</h4>
            <p class="text-gray-600 text-sm mb-4">Subject-wise analysis and board results breakdown</p>
            <a 
              href="#" 
              class="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg text-sm transition-colors"
            >
              Download PDF (1.8 MB)
            </a>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-md text-center">
            <div class="text-4xl mb-4">💰</div>
            <h4 class="text-lg font-semibold text-blue-900 mb-3">Financial Statement</h4>
            <p class="text-gray-600 text-sm mb-4">Audited financial reports and budget allocation</p>
            <a 
              href="#" 
              class="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg text-sm transition-colors"
            >
              Download PDF (1.2 MB)
            </a>
          </div>
        </div>
      </div>

      <!-- Contact for Queries -->
      <div class="bg-gradient-to-r from-blue-900 to-indigo-900 text-white p-8 rounded-lg">
        <h2 class="text-3xl font-bold mb-6 text-center">For Report Queries</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="text-center">
            <div class="text-4xl mb-3">👨‍💼</div>
            <h4 class="text-lg font-semibold mb-2">Administrative Office</h4>
            <p class="text-sm text-blue-100">For detailed report information</p>
            <p class="text-sm text-blue-100">Office Hours: 9:00 AM - 5:00 PM</p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-3">📧</div>
            <h4 class="text-lg font-semibold mb-2">Email</h4>
            <p class="text-sm text-blue-100">reports@dalmiavidyamandir.edu.in</p>
            <p class="text-sm text-blue-100">Response within 48 hours</p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-3">📞</div>
            <h4 class="text-lg font-semibold mb-2">Phone</h4>
            <p class="text-sm text-blue-100">+91-11-2345-6789</p>
            <p class="text-sm text-blue-100">Ext: 105 (Reports)</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Annual Report page component
</script>
