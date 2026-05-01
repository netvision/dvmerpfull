<template>
  <div class="facilities-page bg-gray-50">
    <!-- Hero Section -->
    <div class="relative h-96 bg-gradient-to-br from-blue-600 via-indigo-700 to-purple-800 overflow-hidden">
      <div class="absolute inset-0 bg-black opacity-40"></div>
      <div class="absolute inset-0" style="background-image: url('/images/building.jpg'); background-size: cover; background-position: center; opacity: 0.3;"></div>
      <div class="container mx-auto px-4 h-full flex items-center justify-center relative z-10">
        <div class="text-white text-center">
          <h1 class="text-6xl font-bold mb-4 animate-fade-in">Our Facilities</h1>
          <p class="text-2xl font-light mb-6">World-Class Infrastructure for Excellence in Education</p>
          <div class="h-1 w-32 bg-yellow-400 mx-auto rounded-full"></div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-16">
      <!-- Introduction -->
      <div class="max-w-4xl mx-auto text-center mb-20">
        <h2 class="text-4xl font-bold text-gray-900 mb-6">Empowering Learning Through Modern Infrastructure</h2>
        <p class="text-lg text-gray-700 leading-relaxed">
          At our institution, we believe that a conducive learning environment is essential for holistic development. 
          Our state-of-the-art facilities are designed to nurture creativity, enhance learning experiences, 
          and ensure the safety and well-being of every student.
        </p>
      </div>

      <!-- Facilities Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16">
        
        <!-- SmartBoards -->
        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
          <div class="relative h-64 overflow-hidden">
            <div class="w-full h-full bg-gradient-to-br from-blue-400 to-cyan-500 flex items-center justify-center group-hover:scale-110 transition-transform duration-500">
              <span class="text-7xl">📱</span>
            </div>
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div class="absolute bottom-4 left-4">
              <span class="inline-block bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-semibold">Technology</span>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-2xl font-bold text-gray-900 mb-3 flex items-center">
              <span class="text-3xl mr-3">📱</span>
              SmartBoards in Every Classroom
            </h3>
            <p class="text-gray-600 leading-relaxed">
              Interactive digital boards in all classrooms enable engaging, multimedia-rich lessons that bring subjects to life 
              and make learning more interactive and enjoyable for students.
            </p>
          </div>
        </div>

        <!-- Audio-Visual Hall -->
        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
          <div class="relative h-64 overflow-hidden">
            <img 
              src="/images/avroom.jpg" 
              alt="Audio-Visual Hall" 
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div class="absolute bottom-4 left-4">
              <span class="inline-block bg-purple-600 text-white px-3 py-1 rounded-full text-sm font-semibold">Learning</span>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-2xl font-bold text-gray-900 mb-3 flex items-center">
              <span class="text-3xl mr-3">🎥</span>
              Audio-Visual Hall
            </h3>
            <p class="text-gray-600 leading-relaxed">
              A dedicated AV hall equipped with advanced technology for online interactive learning sessions, 
              virtual guest lectures, and multimedia presentations that connect students with global knowledge.
            </p>
          </div>
        </div>

        <!-- Music, Art & Dance Studios -->
        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
          <div class="relative h-64 overflow-hidden">
            <div class="w-full h-full bg-gradient-to-br from-pink-400 to-rose-500 flex items-center justify-center group-hover:scale-110 transition-transform duration-500">
              <span class="text-7xl">🎨</span>
            </div>
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div class="absolute bottom-4 left-4">
              <span class="inline-block bg-pink-600 text-white px-3 py-1 rounded-full text-sm font-semibold">Arts</span>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-2xl font-bold text-gray-900 mb-3 flex items-center">
              <span class="text-3xl mr-3">🎨</span>
              Advanced Studios
            </h3>
            <p class="text-gray-600 leading-relaxed">
              Dedicated studios for Music, Art, and Dance equipped with professional-grade instruments, 
              art supplies, and sound systems to nurture and develop creative talents.
            </p>
          </div>
        </div>

        <!-- Laboratories -->
        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
          <div class="relative h-64 overflow-hidden">
            <img 
              src="/images/labs.jpg" 
              alt="Science Laboratory" 
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div class="absolute bottom-4 left-4">
              <span class="inline-block bg-green-600 text-white px-3 py-1 rounded-full text-sm font-semibold">Science</span>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-2xl font-bold text-gray-900 mb-3 flex items-center">
              <span class="text-3xl mr-3">🔬</span>
              Well Equipped Laboratories
            </h3>
            <p class="text-gray-600 leading-relaxed">
              Modern Physics, Chemistry, Biology, and Computer labs with latest equipment and safety measures, 
              enabling hands-on learning and scientific exploration.
            </p>
          </div>
        </div>

        <!-- CCTV Surveillance -->
        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
          <div class="relative h-64 overflow-hidden">
            <div class="w-full h-full bg-gradient-to-br from-gray-500 to-slate-600 flex items-center justify-center group-hover:scale-110 transition-transform duration-500">
              <span class="text-7xl">📹</span>
            </div>
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div class="absolute bottom-4 left-4">
              <span class="inline-block bg-red-600 text-white px-3 py-1 rounded-full text-sm font-semibold">Security</span>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-2xl font-bold text-gray-900 mb-3 flex items-center">
              <span class="text-3xl mr-3">📹</span>
              CCTV Surveillance
            </h3>
            <p class="text-gray-600 leading-relaxed">
              Comprehensive 24/7 CCTV monitoring across the entire campus ensures enhanced safety and security 
              for all students, staff, and visitors.
            </p>
          </div>
        </div>

        <!-- Fire Safety -->
        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
          <div class="relative h-64 overflow-hidden">
            <img 
              src="/images/firesafety.jpg" 
              alt="Fire Safety Equipment" 
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div class="absolute bottom-4 left-4">
              <span class="inline-block bg-orange-600 text-white px-3 py-1 rounded-full text-sm font-semibold">Safety</span>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-2xl font-bold text-gray-900 mb-3 flex items-center">
              <span class="text-3xl mr-3">🔥</span>
              Fire Safety Measures
            </h3>
            <p class="text-gray-600 leading-relaxed">
              State-of-the-art fire detection and suppression systems, fire extinguishers, emergency exits, 
              and regular fire safety drills ensure preparedness for any emergency.
            </p>
          </div>
        </div>

        <!-- Sports Camps -->
        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
          <div class="relative h-64 overflow-hidden">
            <img 
              src="/images/sports.jpg" 
              alt="Sports Training" 
              class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
            />
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div class="absolute bottom-4 left-4">
              <span class="inline-block bg-yellow-600 text-white px-3 py-1 rounded-full text-sm font-semibold">Sports</span>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-2xl font-bold text-gray-900 mb-3 flex items-center">
              <span class="text-3xl mr-3">⚽</span>
              Sports Camps by Expert Coaches
            </h3>
            <p class="text-gray-600 leading-relaxed">
              Regular sports camps and training sessions conducted by certified professional coaches 
              help students excel in various sports and develop athletic skills.
            </p>
          </div>
        </div>

        <!-- Amphitheater -->
        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
          <div class="relative h-64 overflow-hidden">
            <div class="w-full h-full bg-gradient-to-br from-indigo-400 to-purple-500 flex items-center justify-center group-hover:scale-110 transition-transform duration-500">
              <span class="text-7xl">🎭</span>
            </div>
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div class="absolute bottom-4 left-4">
              <span class="inline-block bg-indigo-600 text-white px-3 py-1 rounded-full text-sm font-semibold">Events</span>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-2xl font-bold text-gray-900 mb-3 flex items-center">
              <span class="text-3xl mr-3">🎭</span>
              Amphitheater
            </h3>
            <p class="text-gray-600 leading-relaxed">
              An outdoor amphitheater provides an inspiring venue for cultural programs, assemblies, 
              performances, and various school events in a natural setting.
            </p>
          </div>
        </div>

        <!-- Abacus & Debate Classes -->
        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
          <div class="relative h-64 overflow-hidden">
            <div class="w-full h-full bg-gradient-to-br from-teal-400 to-emerald-500 flex items-center justify-center group-hover:scale-110 transition-transform duration-500">
              <span class="text-7xl">🧮</span>
            </div>
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div class="absolute bottom-4 left-4">
              <span class="inline-block bg-teal-600 text-white px-3 py-1 rounded-full text-sm font-semibold">Skills</span>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-2xl font-bold text-gray-900 mb-3 flex items-center">
              <span class="text-3xl mr-3">🧮</span>
              Abacus and Debate Classes
            </h3>
            <p class="text-gray-600 leading-relaxed">
              Specialized classes in Abacus for mental math development and Debate to enhance critical thinking, 
              public speaking, and communication skills.
            </p>
          </div>
        </div>

        <!-- Transportation -->
        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
          <div class="relative h-64 overflow-hidden">
            <div class="w-full h-full bg-gradient-to-br from-blue-500 to-indigo-600 flex items-center justify-center group-hover:scale-110 transition-transform duration-500">
              <span class="text-7xl">🚌</span>
            </div>
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div class="absolute bottom-4 left-4">
              <span class="inline-block bg-blue-600 text-white px-3 py-1 rounded-full text-sm font-semibold">Transport</span>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-2xl font-bold text-gray-900 mb-3 flex items-center">
              <span class="text-3xl mr-3">🚌</span>
              Transportation Service
            </h3>
            <p class="text-gray-600 leading-relaxed">
              Safe and reliable transportation services with GPS-tracked buses covering extensive routes, 
              ensuring convenient and secure commute for students.
            </p>
          </div>
        </div>

        <!-- Wi-Fi Campus -->
        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
          <div class="relative h-64 overflow-hidden">
            <div class="w-full h-full bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center group-hover:scale-110 transition-transform duration-500">
              <span class="text-7xl">📡</span>
            </div>
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div class="absolute bottom-4 left-4">
              <span class="inline-block bg-cyan-600 text-white px-3 py-1 rounded-full text-sm font-semibold">Connectivity</span>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-2xl font-bold text-gray-900 mb-3 flex items-center">
              <span class="text-3xl mr-3">📡</span>
              Wi-Fi Enabled Campus
            </h3>
            <p class="text-gray-600 leading-relaxed">
              High-speed Wi-Fi connectivity throughout the campus enables seamless access to digital learning resources, 
              online research, and modern educational tools.
            </p>
          </div>
        </div>

        <!-- RO Water -->
        <div class="group bg-white rounded-xl shadow-lg overflow-hidden hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2">
          <div class="relative h-64 overflow-hidden">
            <div class="w-full h-full bg-gradient-to-br from-blue-300 to-cyan-400 flex items-center justify-center group-hover:scale-110 transition-transform duration-500">
              <span class="text-7xl">💧</span>
            </div>
            <div class="absolute inset-0 bg-gradient-to-t from-black/60 to-transparent"></div>
            <div class="absolute bottom-4 left-4">
              <span class="inline-block bg-blue-500 text-white px-3 py-1 rounded-full text-sm font-semibold">Health</span>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-2xl font-bold text-gray-900 mb-3 flex items-center">
              <span class="text-3xl mr-3">💧</span>
              RO Water Facility
            </h3>
            <p class="text-gray-600 leading-relaxed">
              Purified drinking water through RO systems installed at multiple locations across campus 
              ensures clean, safe, and healthy hydration for all students and staff.
            </p>
          </div>
        </div>

      </div>

      <!-- Stats Section -->
      <div class="bg-gradient-to-r from-blue-900 to-indigo-900 rounded-2xl shadow-2xl p-12 mb-16">
        <h2 class="text-3xl font-bold text-white text-center mb-12">Our Infrastructure at a Glance</h2>
        <div class="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div class="text-center">
            <div class="text-5xl font-bold text-yellow-400 mb-2">100%</div>
            <div class="text-white text-lg">SmartBoard Coverage</div>
          </div>
          <div class="text-center">
            <div class="text-5xl font-bold text-yellow-400 mb-2">24/7</div>
            <div class="text-white text-lg">CCTV Surveillance</div>
          </div>
          <div class="text-center">
            <div class="text-5xl font-bold text-yellow-400 mb-2">100%</div>
            <div class="text-white text-lg">Wi-Fi Coverage</div>
          </div>
          <div class="text-center">
            <div class="text-5xl font-bold text-yellow-400 mb-2">100%</div>
            <div class="text-white text-lg">Safe & Secure</div>
          </div>
        </div>
      </div>

      <!-- CTA Section -->
      <div class="text-center bg-white rounded-2xl shadow-xl p-12">
        <h2 class="text-4xl font-bold text-gray-900 mb-4">Experience Our Facilities</h2>
        <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
          We invite you to visit our campus and witness firsthand how our world-class facilities 
          create an exceptional learning environment for your child.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <a 
            href="/contact" 
            class="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-4 px-10 rounded-lg transition-all duration-300 transform hover:scale-105 shadow-lg"
          >
            Schedule a Visit
          </a>
          <a 
            href="/contact" 
            class="bg-white hover:bg-gray-50 text-blue-600 border-2 border-blue-600 font-semibold py-4 px-10 rounded-lg transition-all duration-300 transform hover:scale-105 shadow-lg"
          >
            Contact Us
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Facilities page component - Complete revamp with modern design
</script>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-fade-in {
  animation: fade-in 1s ease-out;
}
</style>
