<template>
  <main class="site">
    <section class="hero">
      <p class="eyebrow">Dalmia Vidya Mandir</p>
      <h1>Main Website App</h1>
      <p>This app is dedicated to the public website experience. It can consume the same backend API where needed.</p>
    </section>
  </main>
</template>

<style scoped>
.site { min-height: 100vh; display: grid; place-items: center; background: radial-gradient(circle at top, #e0f2fe, #f8fafc 55%); padding: 1rem; }
.hero { max-width: 760px; text-align: center; background: #fff; border: 1px solid #dbeafe; border-radius: 16px; padding: 2rem; }
.eyebrow { letter-spacing: 0.1em; text-transform: uppercase; color: #0369a1; font-weight: 700; font-size: 0.8rem; }
h1 { margin: 0.4rem 0 0.8rem; font-size: 2rem; color: #0f172a; }
p { color: #334155; }
</style>
