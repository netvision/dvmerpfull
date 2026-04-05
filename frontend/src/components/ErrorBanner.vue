<template>
  <div v-if="message" class="error-banner">⚠️ {{ message }}</div>
</template>
<script setup>
defineProps({ message: String })
</script>
<style scoped>
.error-banner { background:#fef2f2; border:1px solid #fecaca; color:#dc2626; padding:12px 16px; border-radius:8px; margin-bottom:16px; }
</style>
