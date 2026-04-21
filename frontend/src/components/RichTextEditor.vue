<template>
  <div class="rte-wrapper">
    <div ref="editorEl"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import Quill from 'quill'
import 'quill/dist/quill.snow.css'
import QuillBetterTable from 'quill-better-table'
import 'quill-better-table/dist/quill-better-table.css'

Quill.register({ 'modules/better-table': QuillBetterTable }, true)

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

    input.onchange = () => {
      const file = input.files?.[0]
      if (!file) return
      const reader = new FileReader()
      reader.onload = () => {
        const range = quill.getSelection(true)
        const index = range ? range.index : quill.getLength()
        quill.insertEmbed(index, 'image', reader.result, 'user')
        quill.setSelection(index + 1, 0)
      }
      reader.readAsDataURL(file)
    }
  }

  const insertTable = () => {
    const tableModule = quill.getModule('better-table')
    if (tableModule) {
      tableModule.insertTable(3, 3)
    }
  }

  quill = new Quill(editorEl.value, {
    theme: 'snow',
    placeholder: props.placeholder,
    modules: {
      table: false,
      'better-table': {
        operationMenu: {
          items: {
            unmergeCells: {
              text: 'Unmerge cells',
            },
          },
        },
      },
      keyboard: {
        bindings: QuillBetterTable.keyboardBindings,
      },
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
</style>
