<template>
  <div class="sf-wrap">
    <select id="sf-class" :value="modelClass" @change="onClassChange">
      <option value="">All Classes</option>
      <option v-for="c in classes" :key="c.id" :value="c.id">{{ c.name }}</option>
    </select>
    <select id="sf-section" :value="modelSection" @change="$emit('update:modelSection', +$event.target.value || null)" :disabled="!modelClass">
      <option value="">All Sections</option>
      <option v-for="s in filteredSections" :key="s.id" :value="s.id">{{ s.name }}</option>
    </select>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../api'

const props = defineProps({
  modelClass: { type: Number, default: null },
  modelSection: { type: Number, default: null },
})
const emit = defineEmits(['update:modelClass', 'update:modelSection'])

const classes = ref([])
const sections = ref([])

onMounted(async () => {
  const [cls, sec] = await Promise.all([
    api.get('/api/portal/erp/lookups/classes'),
    api.get('/api/portal/erp/lookups/sections'),
  ])
  classes.value = cls.data
  sections.value = sec.data
})

const filteredSections = computed(() =>
  props.modelClass ? sections.value.filter(s => s.class_id === props.modelClass) : sections.value
)

function onClassChange(e) {
  const val = +e.target.value || null
  emit('update:modelClass', val)
  emit('update:modelSection', null) // reset section when class changes
}
</script>

<style scoped>
.sf-wrap { display: flex; gap: 0.5rem; }
select {
  padding: 0.42rem 0.6rem;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.88rem;
  background: #fff;
  color: #1f2937;
  cursor: pointer;
}
select:disabled { background: #f1f5f9; color: #94a3b8; cursor: not-allowed; }
</style>
