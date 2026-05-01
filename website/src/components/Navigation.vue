<template>
  <header class="bg-white shadow-lg relative z-50 overflow-visible">
    <!-- Top Header with Contact Info -->
    <div class="bg-blue-900 text-white py-2">
      <div class="container mx-auto px-4">
        <div class="flex flex-col sm:flex-row justify-between items-center text-sm">
          <div class="flex items-center space-x-4 mb-1 sm:mb-0">
            <div class="flex items-center">
              <Phone :size="14" class="mr-1" />
              <span>+91 1596 220602</span>
            </div>
            <div class="flex items-center">
              <Mail :size="14" class="mr-1" />
              <span>info@dvmchirawa.ac.in</span>
            </div>
          </div>
          <div class="flex items-center space-x-4">
            <div class="flex items-center">
              <MapPin :size="14" class="mr-1" />
              <span>Station Road, Chirawa - 333026, Rajasthan</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Header -->
    <div class="bg-white border-b border-gray-100 overflow-visible">
      <div class="container mx-auto px-4 overflow-visible">
        <div class="flex items-center justify-between h-20 overflow-visible">
          <!-- Logo Section -->
          <router-link to="/" class="flex items-center space-x-4 hover:opacity-80 transition-opacity duration-200">
            <div class="w-20 h-20 flex items-center justify-center">
              <img 
                src="/images/dvm-logo-white.png" 
                alt="Dalmia Vidya Mandir Logo" 
                class="w-full h-full object-contain"
              />
            </div>
            <div class="flex flex-col justify-center">
              <h1 class="text-3xl font-black text-blue-900 leading-none mb-0">Dalmia Vidya Mandir</h1>
              <p class="text-base text-blue-600 font-bold italic tracking-wider -mt-0.3">
                ✨ From Living Standards to Life Standards ✨
              </p>
            </div>
          </router-link>

          <!-- Desktop Navigation -->
          <nav class="hidden lg:flex items-center space-x-6 overflow-visible">
            <router-link 
              to="/" 
              class="nav-link"
              active-class="nav-link-active"
            >
              <Home :size="18" class="mr-1" />
              Home
            </router-link>
            <router-link 
              to="/about" 
              class="nav-link"
              active-class="nav-link-active"
            >
              <Info :size="18" class="mr-1" />
              About
            </router-link>
            
            <!-- Academics Dropdown -->
            <div class="relative dropdown-container" @mouseenter="showAcademicsDropdown = true" @mouseleave="showAcademicsDropdown = false">
              <button class="nav-link flex items-center dropdown-trigger">
                <BookOpen :size="18" class="mr-1" />
                Academics
                <ChevronDown :size="16" class="ml-1 transition-transform duration-200" :class="{ 'rotate-180': showAcademicsDropdown }" />
              </button>
              <transition name="dropdown">
                <div v-show="showAcademicsDropdown" class="dropdown-menu">
                  <router-link to="/academics" class="dropdown-link" @click="showAcademicsDropdown = false">
                    <BookOpen :size="16" class="mr-2" />
                    Curriculum
                  </router-link>
                  <!-- <router-link to="/syllabus-breakup" class="dropdown-link" @click="showAcademicsDropdown = false">
                    <FileText :size="16" class="mr-2" />
                    Syllabus Breakup
                  </router-link> -->
                  <!-- <router-link to="/book-list" class="dropdown-link" @click="showAcademicsDropdown = false">
                    <BookOpen :size="16" class="mr-2" />
                    Book List 2025-26
                  </router-link> -->
                  <!-- <router-link to="/admissions" class="dropdown-link" @click="showAcademicsDropdown = false">
                    <Users :size="16" class="mr-2" />
                    Admissions
                  </router-link> -->
                  <router-link to="/facilities" class="dropdown-link" @click="showAcademicsDropdown = false">
                    <Building :size="16" class="mr-2" />
                    Facilities
                  </router-link>
                </div>
              </transition>
            </div>

            <!-- Student Life Dropdown -->
            <div class="relative dropdown-container" @mouseenter="showStudentLifeDropdown = true" @mouseleave="showStudentLifeDropdown = false">
              <button class="nav-link flex items-center dropdown-trigger">
                <Users :size="18" class="mr-1" />
                Student Life
                <ChevronDown :size="16" class="ml-1 transition-transform duration-200" :class="{ 'rotate-180': showStudentLifeDropdown }" />
              </button>
              <transition name="dropdown">
                <div v-show="showStudentLifeDropdown" class="dropdown-menu">
                  <router-link to="/news" class="dropdown-link" @click="showStudentLifeDropdown = false">
                    <Newspaper :size="16" class="mr-2" />
                    News
                  </router-link>
                  <router-link to="/events" class="dropdown-link" @click="showStudentLifeDropdown = false">
                    <Calendar :size="16" class="mr-2" />
                    Events
                  </router-link>
                  <router-link to="/gallery" class="dropdown-link" @click="showStudentLifeDropdown = false">
                    <Image :size="16" class="mr-2" />
                    Photo Gallery
                  </router-link>
                  <router-link to="/ncc" class="dropdown-link" @click="showStudentLifeDropdown = false">
                    <Shield :size="16" class="mr-2" />
                    NCC
                  </router-link>
                  <router-link to="/transfer-certificate" class="dropdown-link" @click="showStudentLifeDropdown = false">
                    <FileText :size="16" class="mr-2" />
                    Transfer Certificate
                  </router-link>
                </div>
              </transition>
            </div>

            <!-- Mandatory Disclosure Dropdown -->
            <div class="relative dropdown-container" @mouseenter="showMandatoryDropdown = true" @mouseleave="showMandatoryDropdown = false">
              <button class="nav-link flex items-center dropdown-trigger">
                <FileText :size="18" class="mr-1" />
                Disclosures
                <ChevronDown :size="16" class="ml-1 transition-transform duration-200" :class="{ 'rotate-180': showMandatoryDropdown }" />
              </button>
              <transition name="dropdown">
                <div v-show="showMandatoryDropdown" class="dropdown-menu w-56">
                  <router-link to="/mandatory-disclosure" class="dropdown-link" @click="showMandatoryDropdown = false">
                    <Info :size="16" class="mr-2" />
                    School Information
                  </router-link>
                  <router-link to="/staff" class="dropdown-link" @click="showMandatoryDropdown = false">
                    <Users :size="16" class="mr-2" />
                    Staff Details
                  </router-link>
                  <!-- <router-link to="/fee-structure" class="dropdown-link" @click="showMandatoryDropdown = false">
                    <DollarSign :size="16" class="mr-2" />
                    Fee Structure
                  </router-link> -->
                  <router-link to="/student-strength" class="dropdown-link" @click="showMandatoryDropdown = false">
                    <TrendingUp :size="16" class="mr-2" />
                    Student Strength
                  </router-link>
                  <router-link to="/smc" class="dropdown-link" @click="showMandatoryDropdown = false">
                    <UserCheck :size="16" class="mr-2" />
                    School Management Committee
                  </router-link>
                  <!-- <router-link to="/annual-report" class="dropdown-link" @click="showMandatoryDropdown = false">
                    <BarChart3 :size="16" class="mr-2" />
                    Annual Report
                  </router-link> -->
                  <router-link to="/grievance-redressal" class="dropdown-link" @click="showMandatoryDropdown = false">
                    <MessageSquare :size="16" class="mr-2" />
                    Grievance Redressal
                  </router-link>
                  <router-link to="/mandatory-disclosure#documents" class="dropdown-link" @click="showMandatoryDropdown = false">
                    <Shield :size="16" class="mr-2" />
                    Safety Certificates
                  </router-link>
                  <router-link to="/mandatory-disclosure#cbse-affiliation" class="dropdown-link" @click="showMandatoryDropdown = false">
                    <Award :size="16" class="mr-2" />
                    CBSE Affiliation
                  </router-link>
                </div>
              </transition>
            </div>

            <router-link 
              to="/contact" 
              class="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-2 rounded-lg font-medium transition-colors shadow-md"
            >
              Contact Us
            </router-link>
          </nav>

          <!-- Mobile Menu Button -->
          <button 
            @click="toggleMobileMenu"
            class="lg:hidden p-2 rounded-md text-gray-600 hover:text-blue-600 hover:bg-gray-100 transition-colors"
          >
            <Menu v-if="!isMobileMenuOpen" :size="24" />
            <X v-else :size="24" />
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Navigation -->
    <div 
      v-show="isMobileMenuOpen" 
      class="lg:hidden bg-white border-t border-gray-200 shadow-lg"
    >
      <nav class="container mx-auto px-4 py-4">
        <div class="flex flex-col space-y-3">
          <router-link 
            to="/" 
            class="mobile-nav-link"
            active-class="mobile-nav-link-active"
            @click="closeMobileMenu"
          >
            <Home :size="18" class="mr-2" />
            Home
          </router-link>
          <router-link 
            to="/about" 
            class="mobile-nav-link"
            active-class="mobile-nav-link-active"
            @click="closeMobileMenu"
          >
            <Info :size="18" class="mr-2" />
            About
          </router-link>
          <router-link 
            to="/academics" 
            class="mobile-nav-link"
            active-class="mobile-nav-link-active"
            @click="closeMobileMenu"
          >
            <BookOpen :size="18" class="mr-2" />
            Academics
          </router-link>
          <!-- <router-link 
            to="/admissions" 
            class="mobile-nav-link"
            active-class="mobile-nav-link-active"
            @click="closeMobileMenu"
          >
            <Users :size="18" class="mr-2" />
            Admissions
          </router-link> -->
          <router-link 
            to="/facilities" 
            class="mobile-nav-link"
            active-class="mobile-nav-link-active"
            @click="closeMobileMenu"
          >
            <Building :size="18" class="mr-2" />
            Facilities
          </router-link>
          <router-link 
            to="/news" 
            class="mobile-nav-link"
            active-class="mobile-nav-link-active"
            @click="closeMobileMenu"
          >
            <Newspaper :size="18" class="mr-2" />
            News
          </router-link>
          <router-link 
            to="/events" 
            class="mobile-nav-link"
            active-class="mobile-nav-link-active"
            @click="closeMobileMenu"
          >
            <Calendar :size="18" class="mr-2" />
            Events
          </router-link>
          <router-link 
            to="/gallery" 
            class="mobile-nav-link"
            active-class="mobile-nav-link-active"
            @click="closeMobileMenu"
          >
            <Image :size="18" class="mr-2" />
            Photo Gallery
          </router-link>
          <router-link 
            to="/ncc" 
            class="mobile-nav-link"
            active-class="mobile-nav-link-active"
            @click="closeMobileMenu"
          >
            <Shield :size="18" class="mr-2" />
            NCC
          </router-link>
          <router-link 
            to="/mandatory-disclosure" 
            class="mobile-nav-link"
            active-class="mobile-nav-link-active"
            @click="closeMobileMenu"
          >
            <Info :size="18" class="mr-2" />
            Mandatory Disclosure
          </router-link>
          <router-link 
            to="/grievance-redressal" 
            class="mobile-nav-link"
            active-class="mobile-nav-link-active"
            @click="closeMobileMenu"
          >
            <MessageSquare :size="18" class="mr-2" />
            Grievance Redressal
          </router-link>
          <router-link 
            to="/student-strength" 
            class="mobile-nav-link"
            active-class="mobile-nav-link-active"
            @click="closeMobileMenu"
          >
            <TrendingUp :size="18" class="mr-2" />
            Student Strength
          </router-link>
          <router-link 
            to="/smc" 
            class="mobile-nav-link"
            active-class="mobile-nav-link-active"
            @click="closeMobileMenu"
          >
            <UserCheck :size="18" class="mr-2" />
            School Management Committee
          </router-link>
          <router-link 
            to="/contact" 
            class="bg-yellow-500 hover:bg-yellow-600 text-white px-4 py-3 rounded-lg font-medium transition-colors text-center"
            @click="closeMobileMenu"
          >
            Contact Us
          </router-link>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { 
  Home, 
  Info, 
  Users, 
  Newspaper, 
  Calendar, 
  Phone, 
  Mail, 
  MapPin, 
  Menu, 
  X,
  BookOpen,
  Building,
  ChevronDown,
  FileText,
  MessageSquare,
  // BarChart3,
  Shield,
  Award,
  Image,
  // DollarSign,
  TrendingUp,
  UserCheck
} from 'lucide-vue-next'

const isMobileMenuOpen = ref(false)
const showAcademicsDropdown = ref(false)
const showStudentLifeDropdown = ref(false)
const showMandatoryDropdown = ref(false)

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const closeMobileMenu = () => {
  isMobileMenuOpen.value = false
}
</script>

<style scoped>
/* Remove underlines from all links */
a {
  text-decoration: none !important;
}

a:hover {
  text-decoration: none !important;
}

.nav-link {
  display: flex;
  align-items: center;
  color: #374151;
  font-weight: 500;
  padding: 0.5rem 0.75rem;
  border-radius: 0.5rem;
  transition: color 0.2s, background-color 0.2s;
  text-decoration: none !important;
}

.nav-link:hover {
  color: #2563eb;
  text-decoration: none !important;
}

.nav-link-active {
  color: #2563eb !important;
  background-color: #eff6ff;
  text-decoration: none !important;
}

/* Dropdown Container */
.dropdown-container {
  position: relative;
}

.dropdown-trigger {
  cursor: pointer;
  border: none;
  background: none;
  outline: none;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  margin-top: 0.5rem;
  width: 12rem; /* w-48 equivalent */
  background: white;
  border-radius: 0.75rem;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  border: 1px solid #e5e7eb;
  padding: 0.5rem 0;
  z-index: 100;
  overflow: hidden;
}

.dropdown-menu.w-56 {
  width: 14rem; /* w-56 equivalent */
}

/* Right-align dropdown for items near the right edge */
.dropdown-container:nth-last-child(-n+2) .dropdown-menu {
  left: auto;
  right: 0;
  transform: none;
}

/* Ensure dropdowns don't cause horizontal scroll */
.dropdown-container {
  position: static;
}

@media (min-width: 1024px) {
  .dropdown-container {
    position: relative;
  }
}

.dropdown-link {
  display: flex;
  align-items: center;
  color: #374151;
  font-weight: 500;
  padding: 0.75rem 1rem;
  transition: all 0.15s ease-in-out;
  text-decoration: none !important;
  border-radius: 0;
}

.dropdown-link:hover {
  color: #2563eb;
  background-color: #f8fafc;
  transform: translateX(4px);
  text-decoration: none !important;
}

.dropdown-link:active {
  background-color: #e2e8f0;
  text-decoration: none !important;
}

/* Dropdown Animations */
.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.2s ease-out;
}

.dropdown-enter-from {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-10px) scale(0.95);
}

.dropdown-enter-to,
.dropdown-leave-from {
  opacity: 1;
  transform: translateY(0) scale(1);
}

/* Mobile Navigation */
.mobile-nav-link {
  display: flex;
  align-items: center;
  color: #374151;
  font-weight: 500;
  padding: 0.75rem;
  border-radius: 0.5rem;
  transition: color 0.2s, background-color 0.2s;
  text-decoration: none !important;
}

.mobile-nav-link:hover {
  color: #2563eb;
  background-color: #f9fafb;
  text-decoration: none !important;
}

.mobile-nav-link-active {
  color: #2563eb !important;
  background-color: #eff6ff;
  text-decoration: none !important;
}

/* Chevron rotation animation */
.rotate-180 {
  transform: rotate(180deg);
}
</style>
