<template>
  <div class="mandatory-disclosure-page">
    <!-- Hero Section -->
    <div class="relative h-80 bg-gradient-to-r from-blue-800 to-indigo-800">
      <div class="absolute inset-0 bg-black opacity-30"></div>
      <div class="container mx-auto px-4 h-full flex items-center relative z-10">
        <div class="text-white">
          <h1 class="text-5xl font-bold mb-4">Mandatory Disclosure</h1>
          <p class="text-xl">As per CBSE Guidelines and Right to Education Act</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-16">
      <!-- School Information -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">School Information</h2>
        <div class="bg-blue-50 p-8 rounded-lg">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div class="space-y-4">
              <div class="flex justify-between border-b pb-2">
                <span class="font-semibold text-gray-700">Name of School:</span>
                <span class="text-gray-600">Dalmia Vidya Mandir</span>
              </div>
              <div class="flex justify-between border-b pb-2">
                <span class="font-semibold text-gray-700">CBSE Affiliation No:</span>
                <span class="text-gray-600">1730422</span>
              </div>
              <div class="flex justify-between border-b pb-2">
                <span class="font-semibold text-gray-700">School Code:</span>
                <span class="text-gray-600">10765</span>
              </div>
              <div class="flex justify-between border-b pb-2">
                <span class="font-semibold text-gray-700">Complete Address:</span>
                <span class="text-gray-600">STATION ROAD CHIRAWA, JHUNJHUNU, RAJASTHAN - 333026</span>
              </div>
              <div class="flex justify-between border-b pb-2">
                <span class="font-semibold text-gray-700">Principal Name:</span>
                <span class="text-gray-600">Mr. Shakti Singh</span>
              </div>
              <div class="flex justify-between border-b pb-2">
                <span class="font-semibold text-gray-700">Principal Qualification:</span>
                <span class="text-gray-600">M.A., B.Ed.</span>
              </div>
            </div>
            <div class="space-y-4">
              <div class="flex justify-between border-b pb-2">
                <span class="font-semibold text-gray-700">School Email ID:</span>
                <span class="text-gray-600">10765@cbsesiksha.in, info@dalmiavidyamandir.org.in</span>
              </div>
              <div class="flex justify-between border-b pb-2">
                <span class="font-semibold text-gray-700">Contact Details:</span>
                <span class="text-gray-600">+91-1596-220602</span>
              </div>
              <div class="flex justify-between border-b pb-2">
                <span class="font-semibold text-gray-700">Total Campus Area:</span>
                <span class="text-gray-600">14500 Sq. Mtrs.</span>
              </div>
              <div class="flex justify-between border-b pb-2">
                <span class="font-semibold text-gray-700">Total Number of Students:</span>
                <span class="text-gray-600">949</span>
              </div>
              <div class="flex justify-between border-b pb-2">
                <span class="font-semibold text-gray-700">Total Number of Teachers:</span>
                <span class="text-gray-600">52</span>
              </div>
            </div>
          </div>
        </div>
      </div>

    <!-- Documents -->
    <div id="documents" class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Mandatory Documents</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div id="cbse-affiliation" class="bg-white p-6 rounded-lg shadow-md">
            <h4 class="text-lg font-semibold text-blue-900 mb-3">📄 CBSE Affiliation Certificate</h4>
            <p class="text-gray-600 text-sm mb-4">Certificate of Affiliation issued by CBSE</p>
            <a href="/pdfs/cbse_affiliation.pdf" target="_blank" class="text-blue-600 hover:text-blue-800 text-sm">Open PDF</a>
            <div class="mt-4 border rounded overflow-hidden">
              <iframe src="/pdfs/cbse_affiliation.pdf" class="w-full h-40" />
            </div>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h4 class="text-lg font-semibold text-blue-900 mb-3">🏗️ Building Safety Certificate</h4>
            <p class="text-gray-600 text-sm mb-4">Fire Safety & Building Safety Certificates</p>
            <a href="/pdfs/building_safety.pdf" target="_blank" class="text-blue-600 hover:text-blue-800 text-sm">Open PDF</a>
            <div class="mt-4 border rounded overflow-hidden">
              <iframe src="/pdfs/building_safety.pdf" class="w-full h-40" />
            </div>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h4 class="text-lg font-semibold text-blue-900 mb-3">💧 Water & Health Certificates</h4>
            <p class="text-gray-600 text-sm mb-4">Water Quality & Health Sanitation Certificates</p>
            <a href="/pdfs/WATER_TESTING_CERTIFICATE_2025.pdf" target="_blank" class="text-blue-600 hover:text-blue-800 text-sm">Open PDF</a>
            <div class="mt-4 border rounded overflow-hidden">
              <iframe src="/pdfs/WATER_TESTING_CERTIFICATE_2025.pdf" class="w-full h-40" />
            </div>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h4 class="text-lg font-semibold text-blue-900 mb-3">📋 DEO/State NOC</h4>
            <p class="text-gray-600 text-sm mb-4">No Objection Certificate from State Authorities</p>
            <a href="/pdfs/noc.pdf" target="_blank" class="text-blue-600 hover:text-blue-800 text-sm">Open PDF</a>
            <div class="mt-4 border rounded overflow-hidden">
              <iframe src="/pdfs/noc.pdf" class="w-full h-40" />
            </div>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h4 class="text-lg font-semibold text-blue-900 mb-3">⚖️ Trust/Society Registration</h4>
            <p class="text-gray-600 text-sm mb-4">Trust/Society Registration Certificate</p>
            <a href="/pdfs/Society-Registration.pdf" target="_blank" class="text-blue-600 hover:text-blue-800 text-sm">Open PDF</a>
            <div class="mt-4 border rounded overflow-hidden">
              <iframe src="/pdfs/Society-Registration.pdf" class="w-full h-40" />
            </div>
          </div>
        </div>
      </div>

      <!-- Compliance & Supporting Documents -->
      <div id="compliance-documents" class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Compliance & Supporting Documents</h2>
        <div class="mb-8">
          <p class="text-gray-600 text-center mb-8">Complete documentation demonstrating school compliance with regulations and standards</p>
        </div>
        
        <!-- Documents Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <a href="/documents/1%20AFFADAVIT.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">📋 Affidavit</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Official affidavit document</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/academic%20calender.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">📅 Academic Calendar</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Current academic year calendar</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/balance%20sheet%20AR.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">💰 Balance Sheet</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Annual financial statement</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/biology%20and%20chemistry.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">🔬 Lab Infrastructure</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Biology & Chemistry laboratories</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/building%20safety%20pwd.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">🏢 Building Safety PWD</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">PWD safety certification</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/deo%20certificate.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">📜 DEO Certificate</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">State education authority certificate</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/executive%20committee.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">👥 Executive Committee</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Committee details and members</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/extention%20of%20affiliation.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">✅ Affiliation Extension</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">CBSE affiliation extension letter</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/fire%20safety.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">🚒 Fire Safety</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Fire safety compliance certificate</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/land%20certificate.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">🏗️ Land Certificate</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Land ownership documents</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/library%20and%20math%20lab%20photos.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">📚 Library & Lab</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Library and mathematics laboratory photos</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/noc%20cbse.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">✔️ CBSE NOC</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">No objection from CBSE board</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/physics%20and%20computer%20lab.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">💻 Science Labs</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Physics and computer laboratory details</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/playground%20and%20science%20lab.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">🎾 Sports & Science</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Playground and science laboratory</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/ramp.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">♿ Accessibility Ramp</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Disabled accessibility compliance</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/recognition%20under%20rte.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">📜 RTE Recognition</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Right to Education recognition</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/salary%20bank%20statement.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">💼 Salary Statements</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Staff salary account statements</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/school%20entrance.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">🚪 School Entrance</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">School entrance and building photos</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/society%20registration%20certificate.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">⚖️ Society Registration</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Trust/Society registration certificate</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/staff%20and%20salary.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">👨‍🏫 Staff Details</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Complete staff and salary information</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/staff%20details.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">📋 Staff Directory</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Detailed staff directory and qualifications</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/toilets.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">🚽 Sanitary Facilities</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Toilet and sanitation facilities</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>

          <a href="/documents/water%20and%20sanitary.pdf" target="_blank" class="group bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow">
            <div class="flex items-start justify-between mb-3">
              <h4 class="text-lg font-semibold text-blue-900 group-hover:text-blue-600 flex-1">💧 Water & Sanitation</h4>
              <span class="text-2xl text-gray-400 group-hover:text-blue-400 ml-2">→</span>
            </div>
            <p class="text-gray-600 text-sm mb-4">Water quality and sanitation compliance</p>
            <div class="text-blue-600 text-sm font-medium">View Document</div>
          </a>
        </div>
      </div>

      <!-- Faculty Information -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Faculty Information</h2>
        <div class="bg-green-50 p-8 rounded-lg">
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8 text-center">
            <div>
              <div class="text-3xl font-bold text-green-900 mb-2">52</div>
              <div class="text-gray-700">Total Teaching Staff</div>
            </div>
            <div>
              <div class="text-3xl font-bold text-green-900 mb-2">100%</div>
              <div class="text-gray-700">Trained Graduate Teachers</div>
            </div>
            <div>
              <div class="text-3xl font-bold text-green-900 mb-2">1:20</div>
              <div class="text-gray-700">Student-Teacher Ratio</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Infrastructure Details -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Infrastructure Details</h2>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h4 class="text-xl font-semibold text-blue-900 mb-4">Academic Infrastructure</h4>
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-700">Total Classrooms:</span>
                <span class="font-semibold">105</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-700">Science Laboratories:</span>
                <span class="font-semibold">6</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-700">Computer Labs:</span>
                <span class="font-semibold">3</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-700">Library Books:</span>
                <span class="font-semibold">25,000+</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-700">AV Room:</span>
                <span class="font-semibold">1 (Newly Added)</span>
              </div>
            </div>
          </div>
          <div class="bg-white p-6 rounded-lg shadow-md">
            <h4 class="text-xl font-semibold text-blue-900 mb-4">Support Infrastructure</h4>
            <div class="space-y-3">
              <div class="flex justify-between">
                <span class="text-gray-700">Playground Area:</span>
                <span class="font-semibold">8 Acres</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-700">Medical Room:</span>
                <span class="font-semibold">Available</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-700">Security System:</span>
                <span class="font-semibold">CCTV + Guards</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-700">Power Backup:</span>
                <span class="font-semibold">100% Generator</span>
              </div>
              <div class="flex justify-between">
                <span class="text-gray-700">Internet Connectivity:</span>
                <span class="font-semibold">High-Speed Broadband</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Fee Structure -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Academic Session Information</h2>
        <div class="bg-yellow-50 p-8 rounded-lg">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
            <div>
              <h4 class="text-xl font-semibold text-blue-900 mb-4">Session Details</h4>
              <div class="space-y-3">
                <div class="flex justify-between border-b pb-2">
                  <span class="font-semibold text-gray-700">Academic Session:</span>
                  <span class="text-gray-600">April to March</span>
                </div>
                <div class="flex justify-between border-b pb-2">
                  <span class="font-semibold text-gray-700">Vacation Period:</span>
                  <span class="text-gray-600">May-June (Summer)</span>
                </div>
                <div class="flex justify-between border-b pb-2">
                  <span class="font-semibold text-gray-700">Working Days:</span>
                  <span class="text-gray-600">220+ Days</span>
                </div>
                <div class="flex justify-between border-b pb-2">
                  <span class="font-semibold text-gray-700">School Hours:</span>
                  <span class="text-gray-600">7:30 AM - 2:00 PM</span>
                </div>
              </div>
            </div>
            <div>
              <h4 class="text-xl font-semibold text-blue-900 mb-4">Admission Process</h4>
              <div class="space-y-3">
                <div class="flex justify-between border-b pb-2">
                  <span class="font-semibold text-gray-700">Admission Notification:</span>
                  <span class="text-gray-600">January</span>
                </div>
                <div class="flex justify-between border-b pb-2">
                  <span class="font-semibold text-gray-700">Form Submission:</span>
                  <span class="text-gray-600">February-March</span>
                </div>
                <div class="flex justify-between border-b pb-2">
                  <span class="font-semibold text-gray-700">Age Criteria:</span>
                  <span class="text-gray-600">As per RTE Guidelines</span>
                </div>
                <div class="flex justify-between border-b pb-2">
                  <span class="font-semibold text-gray-700">EWS/DG Quota:</span>
                  <span class="text-gray-600">25% as per RTE</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Board Results -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Academic Performance</h2>
        <div class="bg-gradient-to-r from-green-500 to-blue-600 text-white p-8 rounded-lg">
          <div class="grid grid-cols-1 md:grid-cols-4 gap-6 text-center">
            <div>
              <div class="text-3xl font-bold mb-2">98.69%</div>
              <div class="text-sm">Class X Pass Rate (2025)</div>
            </div>
            <div>
              <div class="text-3xl font-bold mb-2">92.85%</div>
              <div class="text-sm">Class XII Pass Rate (2025)</div>
            </div>
            <div>
              <div class="text-3xl font-bold mb-2">85%</div>
              <div class="text-sm">Students Above 80% (Class X)</div>
            </div>
            <div>
              <div class="text-3xl font-bold mb-2">78%</div>
              <div class="text-sm">Students Above 80% (Class XII)</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Contact Information -->
      <div class="bg-blue-900 text-white p-8 rounded-lg">
        <h2 class="text-3xl font-bold mb-6 text-center">Contact Information</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="text-center">
            <div class="text-4xl mb-3">📧</div>
            <h4 class="text-lg font-semibold mb-2">Email</h4>
            <p class="text-sm text-blue-100">info@dalmiavidyamandir.edu.in</p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-3">📞</div>
            <h4 class="text-lg font-semibold mb-2">Phone</h4>
            <p class="text-sm text-blue-100">+91-1596-220602</p>
          </div>
          <div class="text-center">
            <div class="text-4xl mb-3">📍</div>
            <h4 class="text-lg font-semibold mb-2">Address</h4>
            <p class="text-sm text-blue-100">STATION ROAD CHIRAWA, JHUNJHUNU, RAJASTHAN - 333026</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Mandatory Disclosure page component
</script>
