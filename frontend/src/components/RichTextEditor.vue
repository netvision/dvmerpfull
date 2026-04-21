<template>
  <div class="rte-wrapper">
    <div ref="editorEl"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import Quill from 'quill'
import 'quill/dist/quill.snow.css'
import api from '../api.js'

const apiBase = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function buildAssetUrl(path) {
  if (!path) return ''
  return encodeURI(`${apiBase}${path}`)
}

const props = defineProps({
  modelValue: { type: String, default: '' },
  placeholder: { type: String, default: 'Enter text...' },
  minHeight: { type: String, default: '120px' },
})
const emit = defineEmits(['update:modelValue'])

const editorEl = ref(null)
let quill = null

onMounted(() => {
  const selectAndInsertImage = () => {
    const input = document.createElement('input')
    input.setAttribute('type', 'file')
    input.setAttribute('accept', 'image/*')
    input.click()

    input.onchange = async () => {
      const file = input.files?.[0]
      if (!file) return

      try {
        const formData = new FormData()
        formData.append('file', file)
        const res = await api.post('/api/portal/editor-images', formData, {
          headers: { 'Content-Type': 'multipart/form-data' },
        })

        const range = quill.getSelection(true)
        const index = range ? range.index : quill.getLength()
        quill.insertEmbed(index, 'image', buildAssetUrl(res.data?.url), 'user')
        quill.setSelection(index + 1, 0)
      } catch (error) {
        alert(error.response?.data?.detail || 'Image upload failed')
      }
    }
  }

  const insertTable = () => {
    const rowsInput = window.prompt('Number of rows', '3')
    if (rowsInput === null) return

    const colsInput = window.prompt('Number of columns', '3')
    if (colsInput === null) return

    const rows = Math.max(1, Math.min(10, Number.parseInt(rowsInput, 10) || 3))
    const cols = Math.max(1, Math.min(10, Number.parseInt(colsInput, 10) || 3))

    const tableRows = Array.from({ length: rows }, () => {
      const cells = Array.from({ length: cols }, () => '<td><br></td>').join('')
      return `<tr>${cells}</tr>`
    }).join('')

    const tableHtml = `<table><tbody>${tableRows}</tbody></table><p><br></p>`
    const range = quill.getSelection(true)
    const index = range ? range.index : quill.getLength()
    quill.clipboard.dangerouslyPasteHTML(index, tableHtml, 'user')
  }

  quill = new Quill(editorEl.value, {
    theme: 'snow',
    placeholder: props.placeholder,
    modules: {
      toolbar: {
        container: [
          ['bold', 'italic', 'underline'],
          [{ list: 'ordered' }, { list: 'bullet' }],
          ['link', 'image'],
          ['insertTable'],
          ['clean'],
        ],
        handlers: {
          image: selectAndInsertImage,
          insertTable,
        },
      },
    },
  })

  const tableBtn = editorEl.value.querySelector('.ql-insertTable')
  if (tableBtn) {
    tableBtn.innerHTML = 'Table'
    tableBtn.setAttribute('title', 'Insert table')
  }

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
.rte-wrapper :deep(.ql-insertTable) { width: auto; min-width: 56px; font-size: 12px; font-weight: 600; }
.rte-wrapper :deep(.ql-editor table) { width: 100%; border-collapse: collapse; margin: 0.75rem 0; }
.rte-wrapper :deep(.ql-editor td),
.rte-wrapper :deep(.ql-editor th) { border: 1px solid #cbd5e1; padding: 0.45rem 0.6rem; vertical-align: top; }
</style>
