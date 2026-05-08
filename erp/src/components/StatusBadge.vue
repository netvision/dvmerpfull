<template>
  <span :class="['badge', `badge--${color}`]">{{ label }}</span>
</template>

<script setup>
const props = defineProps({ status: String })

const MAP = {
  active: { label: 'Active', color: 'green' },
  promoted: { label: 'Promoted', color: 'blue' },
  left: { label: 'Left', color: 'red' },
  detained: { label: 'Detained', color: 'orange' },
}
const resolved = MAP[props.status?.toLowerCase()] || { label: props.status || '—', color: 'gray' }
const label = resolved.label
const color = resolved.color
</script>

<style scoped>
.badge {
  display: inline-block;
  padding: 2px 10px;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.02em;
}
.badge--green  { background: #dcfce7; color: #16a34a; }
.badge--blue   { background: #dbeafe; color: #1d4ed8; }
.badge--red    { background: #fee2e2; color: #dc2626; }
.badge--orange { background: #ffedd5; color: #ea580c; }
.badge--gray   { background: #f1f5f9; color: #64748b; }
</style>
