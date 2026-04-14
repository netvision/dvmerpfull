<template>
  <div class="not-found">
    <div class="nf-card">
      <div class="nf-code">404</div>
      <h1 class="nf-title">Page Not Found</h1>
      <p class="nf-desc">The page you're looking for doesn't exist or has been moved.</p>
      <RouterLink to="/" class="nf-btn">Go to Home</RouterLink>
    </div>
  </div>
</template>

<script setup>
// No logic needed
</script>

<style scoped>
.not-found {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f1f5f9;
  padding: 2rem;
}

.nf-card {
  text-align: center;
  background: white;
  border-radius: 16px;
  padding: 3rem 2.5rem;
  box-shadow: 0 4px 24px rgba(30, 58, 138, 0.1);
  max-width: 420px;
  width: 100%;
}

.nf-code {
  font-size: 6rem;
  font-weight: 900;
  line-height: 1;
  color: #1e3a8a;
  margin-bottom: 0.5rem;
}

.nf-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 0.75rem;
}

.nf-desc {
  color: #64748b;
  font-size: 0.95rem;
  margin: 0 0 2rem;
}

.nf-btn {
  display: inline-block;
  background: #1e3a8a;
  color: white;
  padding: 0.65rem 1.75rem;
  border-radius: 8px;
  text-decoration: none;
  font-weight: 600;
  font-size: 0.95rem;
  transition: background 0.2s;
}

.nf-btn:hover {
  background: #1d4ed8;
}
</style>
