<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 via-yellow-50 to-amber-50">
    <!-- Hero Section -->
    <section class="py-20 relative overflow-hidden">
      <!-- Background decorative elements -->
      <div class="absolute inset-0 overflow-hidden">
        <div class="absolute -top-40 -right-40 w-80 h-80 rounded-full bg-gradient-to-br from-orange-200/30 to-red-200/30 blur-3xl"></div>
        <div class="absolute -bottom-40 -left-40 w-80 h-80 rounded-full bg-gradient-to-tr from-yellow-200/30 to-orange-200/30 blur-3xl"></div>
      </div>

      <div class="container mx-auto px-4 relative">
        <!-- Back Navigation -->
        <div class="mb-8">
          <router-link 
            to="/"
            class="inline-flex items-center text-orange-600 hover:text-orange-700 transition-colors duration-200 no-underline"
          >
            <ArrowLeft :size="20" class="mr-2" />
            <span class="font-medium">Back to Home</span>
          </router-link>
        </div>

        <!-- Page Header -->
        <div class="text-center mb-16">
          <div class="inline-block px-6 py-2 bg-orange-100 text-orange-800 rounded-full text-sm font-semibold tracking-wide uppercase mb-6">
            Our Mission
          </div>
          <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            Divine Qualities in
            <span class="bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
              Education
            </span>
          </h1>
          <p class="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            Inspired by the timeless wisdom of the Bhagavad Gita, our mission is to cultivate divine qualities 
            in every student, fostering character that transcends material success.
          </p>
        </div>
      </div>
    </section>

    <!-- Sanskrit Verses Section -->
    <section class="py-16 bg-white/70 backdrop-blur-sm">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto">
          <div class="text-center mb-12">
            <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              श्रीमद्भगवद्गीता
              <span class="text-orange-600">अध्याय १६</span>
            </h2>
            <p class="text-lg text-gray-600">Chapter 16: Divine and Demonic Qualities (Verses 1-3)</p>
          </div>

          <!-- Verse 1 -->
          <div class="mb-12 bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl p-8 shadow-lg border border-orange-200">
            <div class="text-center mb-6">
              <h3 class="text-2xl font-bold text-orange-800 mb-4">श्लोक १</h3>
              <div class="sanskrit-text text-xl md:text-2xl text-gray-800 leading-relaxed mb-6 font-devanagari">
                अभयं सत्त्वसंशुद्धिर्ज्ञानयोगव्यवस्थितिः।<br>
                दानं दमश्च यज्ञश्च स्वाध्यायस्तप आर्जवम्॥१॥
              </div>
              <div class="transliteration text-lg text-gray-600 italic mb-4">
                abhayaṁ sattva-saṁśuddhir jñāna-yoga-vyavasthitiḥ<br>
                dānaṁ damaś ca yajñaś ca svādhyāyas tapa ārjavam
              </div>
            </div>
            <div class="prose prose-lg max-w-none">
              <p class="text-gray-700 leading-relaxed">
                <strong class="text-orange-700">Translation:</strong> Fearlessness, purity of mind, steadfastness in the yoga of knowledge, 
                charity, self-control, sacrifice, study of scriptures, austerity, and straightforwardness.
              </p>
            </div>
          </div>

          <!-- Verse 2 -->
          <div class="mb-12 bg-gradient-to-br from-yellow-50 to-orange-50 rounded-2xl p-8 shadow-lg border border-yellow-200">
            <div class="text-center mb-6">
              <h3 class="text-2xl font-bold text-orange-800 mb-4">श्लोक २</h3>
              <div class="sanskrit-text text-xl md:text-2xl text-gray-800 leading-relaxed mb-6 font-devanagari">
                अहिंसा सत्यमक्रोधस्त्यागः शान्तिरपैशुनम्।<br>
                दया भूतेष्वलोलुप्त्वं मार्दवं ह्रीरचापलम्॥२॥
              </div>
              <div class="transliteration text-lg text-gray-600 italic mb-4">
                ahiṁsā satyam akrodhas tyāgaḥ śāntir apaiśunam<br>
                dayā bhūteṣv aloluptvaṁ mārdavaṁ hrīr acāpalam
              </div>
            </div>
            <div class="prose prose-lg max-w-none">
              <p class="text-gray-700 leading-relaxed">
                <strong class="text-orange-700">Translation:</strong> Non-violence, truthfulness, absence of anger, renunciation, 
                tranquility, absence of fault-finding, compassion toward all beings, freedom from greed, gentleness, modesty, and reliability.
              </p>
            </div>
          </div>

          <!-- Verse 3 -->
          <div class="mb-12 bg-gradient-to-br from-red-50 to-pink-50 rounded-2xl p-8 shadow-lg border border-red-200">
            <div class="text-center mb-6">
              <h3 class="text-2xl font-bold text-orange-800 mb-4">श्लोक ३</h3>
              <div class="sanskrit-text text-xl md:text-2xl text-gray-800 leading-relaxed mb-6 font-devanagari">
                तेजः क्षमा धृतिः शौचमद्रोहो नातिमानिता।<br>
                भवन्ति सम्पदं दैवीमभिजातस्य भारत॥३॥
              </div>
              <div class="transliteration text-lg text-gray-600 italic mb-4">
                tejaḥ kṣamā dhṛtiḥ śaucam adroho nāti-mānitā<br>
                bhavanti sampadaṁ daivīm abhijātasya bhārata
              </div>
            </div>
            <div class="prose prose-lg max-w-none">
              <p class="text-gray-700 leading-relaxed">
                <strong class="text-orange-700">Translation:</strong> Vigor, forgiveness, fortitude, cleanliness, freedom from envy, 
                and absence of pride—these qualities belong to those endowed with divine nature, O Bharata.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Our Mission Statement -->
    <section class="py-16">
      <div class="container mx-auto px-4">
        <div class="max-w-5xl mx-auto">
          <div class="bg-gradient-to-r from-orange-600 to-red-600 rounded-3xl p-8 md:p-12 text-white shadow-2xl">
            <div class="text-center mb-8">
              <h2 class="text-3xl md:text-4xl font-bold mb-6">Our Sacred Mission</h2>
              <div class="w-24 h-1 bg-white/50 mx-auto rounded-full"></div>
            </div>
            
            <div class="prose prose-lg prose-invert max-w-none space-y-6">
              <blockquote class="text-xl md:text-2xl font-medium text-center border-l-0 pl-0 italic text-orange-100 mb-8">
                "To cultivate the twenty-six divine qualities as outlined in the Bhagavad Gita, 
                transforming education from mere knowledge acquisition to character formation."
              </blockquote>
              
              <p class="text-lg leading-relaxed">
                At Dalmia Vidya Mandir, we draw inspiration from Lord Krishna's divine wisdom to shape not just scholars, 
                but complete human beings. Our mission transcends traditional education by embedding the <strong>daivi sampat</strong> 
                (divine qualities) into every aspect of learning.
              </p>
              
              <p class="text-lg leading-relaxed">
                We believe that true education must nurture <strong>abhaya</strong> (fearlessness) in the face of challenges, 
                <strong>satya</strong> (truthfulness) in character, <strong>ahimsa</strong> (non-violence) in thought and action, 
                and <strong>daya</strong> (compassion) toward all beings.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Divine Qualities Grid -->
    <section class="py-16 bg-gradient-to-br from-orange-50 to-yellow-50">
      <div class="container mx-auto px-4">
        <div class="max-w-6xl mx-auto">
          <div class="text-center mb-12">
            <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              The Twenty-Six
              <span class="bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
                Divine Qualities
              </span>
            </h2>
            <p class="text-lg text-gray-600">Integrated into our educational framework</p>
          </div>

          <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- Quality Cards -->
            <div class="bg-white rounded-xl p-6 shadow-lg border border-orange-100 hover:shadow-xl transition-shadow duration-300">
              <div class="flex items-center mb-4">
                <div class="w-12 h-12 bg-gradient-to-r from-orange-500 to-red-500 rounded-lg flex items-center justify-center mr-4">
                  <Shield :size="20" class="text-white" />
                </div>
                <div>
                  <h4 class="font-bold text-gray-900">Abhaya</h4>
                  <p class="text-sm text-gray-600">Fearlessness</p>
                </div>
              </div>
              <p class="text-gray-700 text-sm">Courage to pursue truth and stand for righteousness</p>
            </div>

            <div class="bg-white rounded-xl p-6 shadow-lg border border-orange-100 hover:shadow-xl transition-shadow duration-300">
              <div class="flex items-center mb-4">
                <div class="w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center mr-4">
                  <Droplets :size="20" class="text-white" />
                </div>
                <div>
                  <h4 class="font-bold text-gray-900">Sattva Samshuddhi</h4>
                  <p class="text-sm text-gray-600">Purity of Mind</p>
                </div>
              </div>
              <p class="text-gray-700 text-sm">Clarity of thought and intention in all endeavors</p>
            </div>

            <div class="bg-white rounded-xl p-6 shadow-lg border border-orange-100 hover:shadow-xl transition-shadow duration-300">
              <div class="flex items-center mb-4">
                <div class="w-12 h-12 bg-gradient-to-r from-green-500 to-teal-500 rounded-lg flex items-center justify-center mr-4">
                  <BookOpen :size="20" class="text-white" />
                </div>
                <div>
                  <h4 class="font-bold text-gray-900">Jnana Yoga</h4>
                  <p class="text-sm text-gray-600">Knowledge & Wisdom</p>
                </div>
              </div>
              <p class="text-gray-700 text-sm">Steadfast pursuit of learning and understanding</p>
            </div>

            <div class="bg-white rounded-xl p-6 shadow-lg border border-orange-100 hover:shadow-xl transition-shadow duration-300">
              <div class="flex items-center mb-4">
                <div class="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center mr-4">
                  <Heart :size="20" class="text-white" />
                </div>
                <div>
                  <h4 class="font-bold text-gray-900">Daya</h4>
                  <p class="text-sm text-gray-600">Compassion</p>
                </div>
              </div>
              <p class="text-gray-700 text-sm">Kindness and empathy toward all living beings</p>
            </div>

            <div class="bg-white rounded-xl p-6 shadow-lg border border-orange-100 hover:shadow-xl transition-shadow duration-300">
              <div class="flex items-center mb-4">
                <div class="w-12 h-12 bg-gradient-to-r from-yellow-500 to-orange-500 rounded-lg flex items-center justify-center mr-4">
                  <CheckCircle :size="20" class="text-white" />
                </div>
                <div>
                  <h4 class="font-bold text-gray-900">Satya</h4>
                  <p class="text-sm text-gray-600">Truthfulness</p>
                </div>
              </div>
              <p class="text-gray-700 text-sm">Honesty in word, thought, and action</p>
            </div>

            <div class="bg-white rounded-xl p-6 shadow-lg border border-orange-100 hover:shadow-xl transition-shadow duration-300">
              <div class="flex items-center mb-4">
                <div class="w-12 h-12 bg-gradient-to-r from-indigo-500 to-blue-500 rounded-lg flex items-center justify-center mr-4">
                  <Zap :size="20" class="text-white" />
                </div>
                <div>
                  <h4 class="font-bold text-gray-900">Tejas</h4>
                  <p class="text-sm text-gray-600">Vigor & Brilliance</p>
                </div>
              </div>
              <p class="text-gray-700 text-sm">Inner strength and radiant energy</p>
            </div>
          </div>

          <div class="text-center mt-12">
            <p class="text-gray-600 text-lg max-w-3xl mx-auto leading-relaxed">
              Through systematic cultivation of these divine qualities, we prepare students not just for academic success, 
              but for a life of purpose, integrity, and service to humanity.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- Call to Action -->
    <section class="py-16">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl mx-auto text-center">
          <div class="bg-white/70 backdrop-blur-sm rounded-2xl p-8 md:p-12 shadow-xl border border-white/50">
            <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
              Join Our Sacred Journey
            </h2>
            <p class="text-xl text-gray-600 mb-8 leading-relaxed">
              Experience education that transforms not just minds, but hearts and souls—guided by ancient wisdom for modern times.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 justify-center">
              <router-link 
                to="/admissions"
                class="inline-flex items-center px-8 py-4 bg-gradient-to-r from-orange-600 to-red-600 text-white rounded-full font-semibold hover:shadow-lg transition-all duration-300 transform hover:scale-105 no-underline"
              >
                <span>Begin the Journey</span>
                <ArrowRight :size="20" class="ml-3" />
              </router-link>
              <router-link 
                to="/vision"
                class="inline-flex items-center px-8 py-4 border-2 border-orange-600 text-orange-600 rounded-full font-semibold hover:bg-orange-50 transition-all duration-300 no-underline"
              >
                <span>Explore Our Vision</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { 
  ArrowLeft,
  ArrowRight,
  Shield,
  Droplets,
  BookOpen,
  Heart,
  CheckCircle,
  Zap
} from 'lucide-vue-next'
</script>

<style scoped>
/* Sanskrit/Devanagari font */
.font-devanagari {
  font-family: 'Noto Sans Devanagari', 'Devanagari MT', 'Kohinoor Devanagari', sans-serif;
  font-weight: 500;
}

.sanskrit-text {
  line-height: 1.8;
}

.transliteration {
  font-style: italic;
}

/* Remove underline from router-links */
.no-underline {
  text-decoration: none !important;
}

.no-underline:hover {
  text-decoration: none !important;
}
</style>
