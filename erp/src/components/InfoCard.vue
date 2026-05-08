<template>
  <div class="info-card">
    <h3 v-if="title" class="info-card__title">{{ title }}</h3>
    <dl class="info-card__grid">
      <template v-for="(row, i) in rows" :key="i">
        <dt class="info-card__label">{{ row.label }}</dt>
        <dd class="info-card__value">{{ row.value ?? '—' }}</dd>
      </template>
    </dl>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  rows: Array, // [{ label, value }]
})
</script>

<style scoped>
.info-card {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  padding: 1.25rem 1.5rem;
  margin-bottom: 1rem;
}
.info-card__title {
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: #64748b;
  margin: 0 0 1rem;
  padding-bottom: 0.6rem;
  border-bottom: 1px solid #f1f5f9;
}
.info-card__grid {
  display: grid;
  grid-template-columns: 160px 1fr;
  gap: 0.45rem 1rem;
  margin: 0;
}
.info-card__label {
  color: #64748b;
  font-size: 0.84rem;
  font-weight: 500;
  display: flex;
  align-items: center;
}
.info-card__value {
  color: #1e293b;
  font-size: 0.88rem;
  font-weight: 500;
  margin: 0;
}
</style>
