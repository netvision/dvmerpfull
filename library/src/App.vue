<template>
  <main class="library">
    <section class="panel">
      <p class="eyebrow">DVM Digital Library</p>
      <h1>Library App</h1>
      <p>This app is isolated for library workflows while sharing the same backend and database.</p>
    </section>
  </main>
</template>

<style scoped>
.library { min-height: 100vh; display: grid; place-items: center; background: radial-gradient(circle at top right, #dbeafe, #f8fafc 52%); padding: 1rem; }
.panel { max-width: 760px; text-align: center; background: #fff; border: 1px solid #dbeafe; border-radius: 16px; padding: 2rem; }
.eyebrow { letter-spacing: 0.1em; text-transform: uppercase; color: #1d4ed8; font-weight: 700; font-size: 0.8rem; }
h1 { margin: 0.4rem 0 0.8rem; font-size: 2rem; color: #0f172a; }
p { color: #334155; }
</style>
