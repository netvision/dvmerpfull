<template>
  <footer class="bg-blue-900 text-white py-12">
    <div class="container mx-auto px-4">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- Logo & School Info -->
        <div>
          <div class="flex items-center mb-4">
            <img 
              src="/images/dvm-logo-white.png" 
              alt="Dalmia Vidya Mandir Logo" 
              class="w-16 h-16 object-contain mr-3"
            />
            <div class="flex flex-col justify-center">
              <h3 class="text-lg font-bold text-white leading-none mb-0">Dalmia Vidya Mandir</h3>
              <p class="text-sm text-yellow-300 font-semibold italic -mt-0.5">
                ✨ Excellence in Education ✨
              </p>
            </div>
          </div>
          <p class="text-blue-100 text-sm leading-relaxed">
            Nurturing minds, building character, and shaping futures through 100 years of educational excellence.
          </p>
        </div>

        <!-- Contact Info -->
        <div>
          <h4 class="text-lg font-semibold mb-4">Contact Info</h4>
          <div class="text-blue-100 space-y-2 text-sm">
            <div class="flex items-start">
              <span class="mr-2">📍</span>
              <span>Station Road, Chirawa - 333026, Rajasthan</span>
            </div>
            <div class="flex items-center">
              <span class="mr-2">📞</span>
              <span>+91 1596 220602</span>
            </div>
            <div class="flex items-center">
              <span class="mr-2">✉️</span>
              <span>info@dvmchirawa.ac.in</span>
            </div>
          </div>
        </div>

        <!-- Quick Links -->
        <div>
          <h4 class="text-lg font-semibold mb-4">Quick Links</h4>
          <div class="space-y-3">
            <router-link 
              to="/about" 
              class="block text-blue-100 hover:text-yellow-300 transition-colors text-sm py-1 border-l-2 border-transparent hover:border-yellow-300 pl-3 hover:pl-4 transition-all"
            >
              About Us
            </router-link>
            <router-link 
              to="/academics" 
              class="block text-blue-100 hover:text-yellow-300 transition-colors text-sm py-1 border-l-2 border-transparent hover:border-yellow-300 pl-3 hover:pl-4 transition-all"
            >
              Academics
            </router-link>
            <router-link 
              to="/admissions" 
              class="block text-blue-100 hover:text-yellow-300 transition-colors text-sm py-1 border-l-2 border-transparent hover:border-yellow-300 pl-3 hover:pl-4 transition-all"
            >
              Admissions
            </router-link>
            <router-link 
              to="/facilities" 
              class="block text-blue-100 hover:text-yellow-300 transition-colors text-sm py-1 border-l-2 border-transparent hover:border-yellow-300 pl-3 hover:pl-4 transition-all"
            >
              Facilities
            </router-link>
            <router-link 
              to="/gallery" 
              class="block text-blue-100 hover:text-yellow-300 transition-colors text-sm py-1 border-l-2 border-transparent hover:border-yellow-300 pl-3 hover:pl-4 transition-all"
            >
              Photo Gallery
            </router-link>
            <router-link 
              to="/contact" 
              class="block text-blue-100 hover:text-yellow-300 transition-colors text-sm py-1 border-l-2 border-transparent hover:border-yellow-300 pl-3 hover:pl-4 transition-all"
            >
              Contact Us
            </router-link>
          </div>
        </div>

        <!-- Mandatory Disclosures -->
        <div>
          <h4 class="text-lg font-semibold mb-4">Mandatory Disclosures</h4>
          <div class="space-y-3">
            <router-link 
              to="/mandatory-disclosure" 
              class="block text-blue-100 hover:text-yellow-300 transition-colors text-sm py-1 border-l-2 border-transparent hover:border-yellow-300 pl-3 hover:pl-4 transition-all"
            >
              School Information
            </router-link>
            <router-link 
              to="/transfer-certificate" 
              class="block text-blue-100 hover:text-yellow-300 transition-colors text-sm py-1 border-l-2 border-transparent hover:border-yellow-300 pl-3 hover:pl-4 transition-all"
            >
              Transfer Certificate
            </router-link>
            <router-link 
              to="/grievance-redressal" 
              class="block text-blue-100 hover:text-yellow-300 transition-colors text-sm py-1 border-l-2 border-transparent hover:border-yellow-300 pl-3 hover:pl-4 transition-all"
            >
              Grievance Redressal
            </router-link>
            <router-link 
              to="/annual-report" 
              class="block text-blue-100 hover:text-yellow-300 transition-colors text-sm py-1 border-l-2 border-transparent hover:border-yellow-300 pl-3 hover:pl-4 transition-all"
            >
              Annual Report
            </router-link>
          </div>
        </div>
      </div>

      <div class="border-t border-blue-800 mt-8 pt-6 text-center text-blue-100">
        <p>&copy; {{ currentYear }} Dalmia Vidya Mandir. All rights reserved.</p>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
</script>
