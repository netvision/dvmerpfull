<template>
  <div class="contact-page">
    <!-- Hero Section -->
    <div class="relative h-80 bg-gradient-to-r from-teal-600 to-blue-600">
      <div class="absolute inset-0 bg-black opacity-30"></div>
      <div class="container mx-auto px-4 h-full flex items-center relative z-10">
        <div class="text-white">
          <h1 class="text-5xl font-bold mb-4">Contact Us</h1>
          <p class="text-xl">Get in Touch - We're Here to Help</p>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <div class="container mx-auto px-4 py-16">
      <!-- Contact Information -->
      <div class="mb-16">
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <!-- Contact Details -->
          <div class="lg:col-span-1">
            <h2 class="text-3xl font-bold text-blue-900 mb-6">Get in Touch</h2>
            
            <div class="space-y-6">
              <div class="flex items-start">
                <div class="bg-blue-100 p-3 rounded-full mr-4">
                  <svg class="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path>
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-blue-900 mb-2">School Address</h3>
                  <p class="text-gray-700">
                    Dalmia Vidya Mandir<br>
                    Station Road, Chirawa<br>
                    Jhunjhunu, Rajasthan - 333026
                  </p>
                </div>
              </div>

              <div class="flex items-start">
                <div class="bg-green-100 p-3 rounded-full mr-4">
                  <svg class="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-blue-900 mb-2">Phone Numbers</h3>
                  <div class="text-gray-700 space-y-1">
                    <p><strong>Main Office:</strong> 01596220602</p>
                    <p><strong>Reception:</strong> +91 9672609111</p>
                    <p><strong>Principal:</strong> +91 9928073151</p>
                  </div>
                </div>
              </div>

              <div class="flex items-start">
                <div class="bg-purple-100 p-3 rounded-full mr-4">
                  <svg class="w-6 h-6 text-purple-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-blue-900 mb-2">Email Addresses</h3>
                  <div class="text-gray-700 space-y-1">
                    <p><strong>General Inquiries:</strong> info@dvmchirawa.ac.in</p>
                    <p><strong>Admissions:</strong> admissions@dvmchirawa.ac.in</p>
                    <p><strong>Principal:</strong> principal@dvmchirawa.ac.in</p>
                  </div>
                </div>
              </div>

              <div class="flex items-start">
                <div class="bg-yellow-100 p-3 rounded-full mr-4">
                  <svg class="w-6 h-6 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                </div>
                <div>
                  <h3 class="text-lg font-semibold text-blue-900 mb-2">Office Hours</h3>
                  <div class="text-gray-700 space-y-1">
                    <p><strong>Monday - Friday:</strong> 8:00 AM - 4:00 PM</p>
                    <p><strong>Saturday:</strong> 8:00 AM - 2:00 PM</p>
                    <p><strong>Sunday:</strong> Closed</p>
                    <p><strong>Holidays:</strong> As per school calendar</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Contact Form -->
          <div class="lg:col-span-2">
            <div class="bg-white shadow-lg rounded-lg p-8">
              <h2 class="text-3xl font-bold text-blue-900 mb-6">Send us a Message</h2>
              
              <!-- Success Message -->
              <div v-if="submitSuccess" class="mb-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded-lg">
                <div class="flex items-center">
                  <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="font-semibold">Thank you! Your message has been sent successfully. We'll get back to you soon.</span>
                </div>
              </div>
              
              <!-- Error Message -->
              <div v-if="submitError" class="mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
                <div class="flex items-center">
                  <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                  </svg>
                  <span class="font-semibold">{{ submitError }}</span>
                </div>
              </div>
              
              <form @submit.prevent="handleSubmit" class="space-y-6">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">First Name *</label>
                    <input 
                      v-model="formData.firstName"
                      type="text" 
                      required
                      class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Enter your first name"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Last Name *</label>
                    <input 
                      v-model="formData.lastName"
                      type="text" 
                      required
                      class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Enter your last name"
                    />
                  </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Email Address *</label>
                    <input 
                      v-model="formData.email"
                      type="email" 
                      required
                      class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Enter your email"
                    />
                  </div>
                  <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Phone Number</label>
                    <input 
                      v-model="formData.phone"
                      type="tel" 
                      class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder="Enter your phone number"
                    />
                  </div>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Subject *</label>
                  <select 
                    v-model="formData.subject"
                    required
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  >
                    <option value="">Select a subject</option>
                    <option value="admissions">Admissions Inquiry</option>
                    <option value="academic">Academic Information</option>
                    <option value="facilities">Facilities & Infrastructure</option>
                    <option value="transport">Transportation</option>
                    <option value="fees">Fee Structure</option>
                    <option value="careers">Career Opportunities</option>
                    <option value="complaint">Complaint/Suggestion</option>
                    <option value="other">Other</option>
                  </select>
                </div>

                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">Message *</label>
                  <textarea 
                    v-model="formData.message"
                    rows="5" 
                    required
                    class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Enter your message here..."
                  ></textarea>
                </div>

                <div class="flex items-start">
                  <input 
                    v-model="formData.agreeToPolicy"
                    type="checkbox" 
                    required
                    class="mt-1 mr-3 h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <label class="text-sm text-gray-700">
                    I agree to the <a href="#" class="text-blue-600 hover:underline">Privacy Policy</a> 
                    and consent to being contacted regarding my inquiry.
                  </label>
                </div>

                <button 
                  type="submit" 
                  :disabled="isSubmitting"
                  class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-6 rounded-lg transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                  <span v-if="isSubmitting">Sending...</span>
                  <span v-else>Send Message</span>
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>

      <!-- Quick Contact Cards -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Quick Contact</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div class="bg-gradient-to-br from-blue-500 to-purple-600 text-white p-6 rounded-lg text-center">
            <div class="text-4xl mb-4">🎓</div>
            <h3 class="text-xl font-semibold mb-3">Main Office</h3>
            <p class="text-sm mb-4">For general inquiries and information</p>
            <div class="space-y-2 text-sm">
              <p>📞 01596220602</p>
              <p>✉️ info@dvmchirawa.ac.in</p>
            </div>
          </div>
          <div class="bg-gradient-to-br from-green-500 to-teal-600 text-white p-6 rounded-lg text-center">
            <div class="text-4xl mb-4">👨‍💼</div>
            <h3 class="text-xl font-semibold mb-3">Principal's Office</h3>
            <p class="text-sm mb-4">For academic matters and school policies</p>
            <div class="space-y-2 text-sm">
              <p>📞 +91 9928073151</p>
              <p>✉️ principal@dvmchirawa.ac.in</p>
            </div>
          </div>
          <div class="bg-gradient-to-br from-orange-500 to-red-600 text-white p-6 rounded-lg text-center">
            <div class="text-4xl mb-4">📱</div>
            <h3 class="text-xl font-semibold mb-3">Reception</h3>
            <p class="text-sm mb-4">For immediate assistance and queries</p>
            <div class="space-y-2 text-sm">
              <p>📞 +91 9672609111</p>
              <p>✉️ admissions@dvmchirawa.ac.in</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Location Map -->
      <div class="mb-16">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Find Us</h2>
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12">
          <div>
            <div class="h-96 rounded-lg overflow-hidden shadow-lg">
              <iframe 
                src="https://www.openstreetmap.org/export/embed.html?bbox=75.64977836608888%2C28.237778091430664%2C75.65377807617189%2C28.24177780151367&layer=mapnik&marker=28.239778%2C75.651778" 
                width="100%" 
                height="100%" 
                style="border:0;" 
                allowfullscreen
                loading="lazy" 
                referrerpolicy="no-referrer-when-downgrade"
              ></iframe>
            </div>
            <div class="mt-4 text-center">
              <a 
                href="https://www.google.com/maps/dir/?api=1&destination=28.239778,75.651778" 
                target="_blank" 
                rel="noopener noreferrer"
                class="inline-block bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors"
              >
                Get Directions
              </a>
            </div>
          </div>
          <div>
            <h3 class="text-2xl font-semibold text-blue-900 mb-6">How to Reach Us</h3>
            <div class="space-y-6">
              <div class="flex items-start">
                <div class="bg-blue-100 p-2 rounded-full mr-4">
                  <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.367 2.684 3 3 0 00-5.367-2.684z"></path>
                  </svg>
                </div>
                <div>
                  <h4 class="font-semibold text-gray-800 mb-2">By Train</h4>
                  <p class="text-gray-600 text-sm">Chirawa Railway Station is just 2 km from school. Regular trains from Delhi, Jaipur, and other major cities.</p>
                </div>
              </div>
              <div class="flex items-start">
                <div class="bg-green-100 p-2 rounded-full mr-4">
                  <svg class="w-5 h-5 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                  </svg>
                </div>
                <div>
                  <h4 class="font-semibold text-gray-800 mb-2">By Road</h4>
                  <p class="text-gray-600 text-sm">NH-11 highway connection. Regular bus services from Jaipur (165 km), Delhi (250 km), and Sikar (45 km).</p>
                </div>
              </div>
              <div class="flex items-start">
                <div class="bg-yellow-100 p-2 rounded-full mr-4">
                  <svg class="w-5 h-5 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
                  </svg>
                </div>
                <div>
                  <h4 class="font-semibold text-gray-800 mb-2">By Air</h4>
                  <p class="text-gray-600 text-sm">Nearest airport is Jaipur International Airport (165 km). Taxi and bus services available.</p>
                </div>
              </div>
            </div>
            
            <div class="mt-8 p-4 bg-blue-50 rounded-lg">
              <h4 class="font-semibold text-blue-900 mb-2">School Transport</h4>
              <p class="text-blue-700 text-sm">
                We provide safe and reliable transportation services covering 50+ routes across Jhunjhunu, 
                Sikar, and surrounding areas. GPS-enabled buses with trained drivers and conductors.
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- FAQ Section -->
      <div class="bg-gray-50 p-8 rounded-lg">
        <h2 class="text-3xl font-bold text-blue-900 mb-8 text-center">Frequently Asked Questions</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="space-y-4">
            <div class="bg-white p-4 rounded-lg">
              <h4 class="font-semibold text-blue-900 mb-2">What are the admission requirements?</h4>
              <p class="text-gray-600 text-sm">Age-appropriate entrance test, previous academic records, and document verification.</p>
            </div>
            <div class="bg-white p-4 rounded-lg">
              <h4 class="font-semibold text-blue-900 mb-2">Do you provide transportation?</h4>
              <p class="text-gray-600 text-sm">Yes, we have GPS-enabled buses covering 50+ routes with trained staff.</p>
            </div>
            <div class="bg-white p-4 rounded-lg">
              <h4 class="font-semibold text-blue-900 mb-2">What is the teacher-student ratio?</h4>
              <p class="text-gray-600 text-sm">We maintain a ratio of 1:25 to ensure personalized attention to each student.</p>
            </div>
          </div>
          <div class="space-y-4">
            <div class="bg-white p-4 rounded-lg">
              <h4 class="font-semibold text-blue-900 mb-2">Are scholarships available?</h4>
              <p class="text-gray-600 text-sm">Yes, we offer merit-based, sports, and need-based scholarships up to 50% fee waiver.</p>
            </div>
            <div class="bg-white p-4 rounded-lg">
              <h4 class="font-semibold text-blue-900 mb-2">What extracurricular activities do you offer?</h4>
              <p class="text-gray-600 text-sm">Sports, arts, music, dance, drama, robotics, and various clubs and societies.</p>
            </div>
            <div class="bg-white p-4 rounded-lg">
              <h4 class="font-semibold text-blue-900 mb-2">How can parents track student progress?</h4>
              <p class="text-gray-600 text-sm">Through our parent portal, regular PTMs, progress reports, and mobile app.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

const formData = ref({
  firstName: '',
  lastName: '',
  email: '',
  phone: '',
  subject: '',
  message: '',
  agreeToPolicy: false
})

const isSubmitting = ref(false)
const submitSuccess = ref(false)
const submitError = ref('')

const handleSubmit = async () => {
  isSubmitting.value = true
  submitSuccess.value = false
  submitError.value = ''

  try {
    const response = await axios.post(`${API_URL}/cms/contact`, {
      firstName: formData.value.firstName,
      lastName: formData.value.lastName,
      email: formData.value.email,
      phone: formData.value.phone,
      subject: formData.value.subject,
      message: formData.value.message
    })

    if (response.data.success) {
      submitSuccess.value = true
      
      // Reset form
      formData.value = {
        firstName: '',
        lastName: '',
        email: '',
        phone: '',
        subject: '',
        message: '',
        agreeToPolicy: false
      }

      // Scroll to success message
      window.scrollTo({ top: 0, behavior: 'smooth' })

      // Hide success message after 10 seconds
      setTimeout(() => {
        submitSuccess.value = false
      }, 10000)
    }
  } catch (error: any) {
    console.error('Failed to submit contact form:', error)
    submitError.value = error.response?.data?.message || 'Failed to send message. Please try again later.'
    
    // Scroll to error message
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } finally {
    isSubmitting.value = false
  }
}
</script>
