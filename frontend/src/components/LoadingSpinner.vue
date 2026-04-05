<template>
  <div class="spinner-wrap">
    <div class="spinner"></div>
    <p v-if="message" class="spinner-msg">{{ message }}</p>
  </div>
</template>
<script setup>
defineProps({ message: String })
</script>
<style scoped>
.spinner-wrap { display:flex; flex-direction:column; align-items:center; padding:40px; gap:12px; }
.spinner { width:40px; height:40px; border:4px solid #e5e7eb; border-top-color:#4f46e5; border-radius:50%; animation:spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }
.spinner-msg { color:#6b7280; font-size:14px; }
</style>
