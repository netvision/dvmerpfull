<template>
  <div class="rte-wrapper">
    <div ref="editorEl"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import Quill from 'quill'
import 'quill/dist/quill.snow.css'

const props = defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: 'Enter text...' },
  minHeight: { type: String, default: '120px' },
})
const emit = defineEmits(['update:modelValue'])

const editorEl = ref(null)
let quill = null

onMounted(() => {
  quill = new Quill(editorEl.value, {
    theme: 'snow',
    placeholder: props.placeholder,
    modules: {
      toolbar: [
        ['bold', 'italic', 'underline'],
        [{ list: 'ordered' }, { list: 'bullet' }],
        ['link'],
        ['clean'],
      ],
    },
  })
  // Set initial value (plain text or HTML)
  if (props.modelValue) {
    quill.root.innerHTML = props.modelValue
  }
  // Emit changes
  quill.on('text-change', () => {
    emit('update:modelValue', quill.root.innerHTML)
  })
  // Apply minHeight
  editorEl.value.querySelector('.ql-editor').style.minHeight = props.minHeight
})

// Sync external changes (e.g. when modal opens with new data)
watch(() => props.modelValue, (val) => {
  if (quill && quill.root.innerHTML !== val) {
    quill.root.innerHTML = val || ''
  }
})

onBeforeUnmount(() => {
  quill = null
})
</script>

<style scoped>
.rte-wrapper { border: 1px solid #d1d5db; border-radius: 8px; overflow: hidden; }
.rte-wrapper :deep(.ql-toolbar) { border: none; border-bottom: 1px solid #e5e7eb; background: #f9fafb; }
.rte-wrapper :deep(.ql-container) { border: none; font-size: 14px; }
.rte-wrapper :deep(.ql-editor) { padding: 10px 12px; }
</style>
