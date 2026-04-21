<template>
  <div class="rte-wrapper">
    <!-- Toolbar built as real DOM so custom buttons are always visible -->
    <div ref="toolbarEl" class="rte-toolbar">
      <span class="ql-formats">
        <button class="ql-bold" title="Bold"></button>
        <button class="ql-italic" title="Italic"></button>
        <button class="ql-underline" title="Underline"></button>
      </span>
      <span class="ql-formats">
        <button class="ql-list" value="ordered" title="Ordered list"></button>
        <button class="ql-list" value="bullet" title="Bullet list"></button>
      </span>
      <span class="ql-formats">
        <button class="ql-link" title="Insert link"></button>
        <button class="ql-image" title="Insert image"></button>
      </span>
      <span class="ql-formats">
        <button ref="tableBtnEl" type="button" class="rte-custom-btn" title="Insert table">Table</button>
        <button ref="htmlBtnEl" type="button" class="rte-custom-btn" title="Insert raw HTML">&lt;/&gt;</button>
      </span>
      <span class="ql-formats">
        <button class="ql-clean" title="Remove formatting"></button>
      </span>
    </div>

    <div ref="editorEl"></div>

    <!-- Raw HTML insert modal -->
    <div v-if="showHtmlModal" class="rte-html-overlay" @click.self="cancelHtml">
      <div class="rte-html-modal">
        <div class="rte-html-modal-header">Insert Raw HTML</div>
        <textarea
          v-model="rawHtmlInput"
          class="rte-html-textarea"
          rows="8"
          placeholder="<table>...</table>"
          spellcheck="false"
        ></textarea>
        <div class="rte-html-actions">
          <button class="rte-btn rte-btn-primary" @click="confirmInsertHtml">Insert</button>
          <button class="rte-btn" @click="cancelHtml">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import Quill from 'quill'
import 'quill/dist/quill.snow.css'
import api from '../api.js'

// ── Custom BlockEmbed blot for arbitrary HTML (tables, etc.) ─────────────────
// Must be registered at module level before any Quill instance is created.
// BlockEmbed is treated as an atomic unit — Quill's Delta normaliser never
// traverses its children, so tables are never stripped.
const BlockEmbed = Quill.import('blots/block/embed')
class RawHtmlBlot extends BlockEmbed {
  static create(html) {
    const node = super.create()
    node.innerHTML = html
    return node
  }
  static value(node) {
    return node.innerHTML
  }
}
RawHtmlBlot.blotName = 'rawHtml'
RawHtmlBlot.tagName = 'div'
RawHtmlBlot.className = 'ql-raw-html'
Quill.register(RawHtmlBlot, true)
// ─────────────────────────────────────────────────────────────────────────────

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

const editorEl   = ref(null)
const toolbarEl  = ref(null)
const tableBtnEl = ref(null)
const htmlBtnEl  = ref(null)
const showHtmlModal = ref(false)
const rawHtmlInput  = ref('')
let savedRange = null
let quill = null

// Insert HTML as an atomic embed so Quill never strips it.
function insertRawHtmlEmbed(html) {
  const range = savedRange || quill.getSelection(true)
  const index = range ? range.index : quill.getLength()
  quill.insertEmbed(index, 'rawHtml', html, 'user')
  quill.insertText(index + 1, '\n', 'user')
  quill.setSelection(index + 2, 0)
}

function cancelHtml() {
  showHtmlModal.value = false
  rawHtmlInput.value = ''
}

function confirmInsertHtml() {
  const html = rawHtmlInput.value.trim()
  if (html) insertRawHtmlEmbed(html)
  cancelHtml()
}

onMounted(() => {
  // ── Image upload ────────────────────────────────────────────────────────
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

  // ── Insert table ────────────────────────────────────────────────────────
  const insertTable = () => {
    savedRange = quill.getSelection(true)
    const rowsInput = window.prompt('Number of rows', '3')
    if (rowsInput === null) return
    const colsInput = window.prompt('Number of columns', '3')
    if (colsInput === null) return
    const rows = Math.max(1, Math.min(20, parseInt(rowsInput, 10) || 3))
    const cols = Math.max(1, Math.min(20, parseInt(colsInput, 10) || 3))
    const headerCells = Array.from({ length: cols }, () => '<th>&nbsp;</th>').join('')
    const dataRow = Array.from({ length: cols }, () => '<td>&nbsp;</td>').join('')
    const bodyRows = Array.from({ length: Math.max(0, rows - 1) }, () => `<tr>${dataRow}</tr>`).join('')
    const html = `<table><thead><tr>${headerCells}</tr></thead><tbody>${bodyRows}</tbody></table>`
    insertRawHtmlEmbed(html)
  }

  // ── Open raw-HTML modal ─────────────────────────────────────────────────
  const openHtmlModal = () => {
    savedRange = quill.getSelection(true)
    rawHtmlInput.value = ''
    showHtmlModal.value = true
  }

  // ── Create Quill ────────────────────────────────────────────────────────
  quill = new Quill(editorEl.value, {
    theme: 'snow',
    placeholder: props.placeholder,
    modules: {
      toolbar: {
        container: toolbarEl.value,
        handlers: { image: selectAndInsertImage },
      },
    },
  })

  // Wire custom buttons directly (bypasses Quill handler system)
  tableBtnEl.value?.addEventListener('click', insertTable)
  htmlBtnEl.value?.addEventListener('click', openHtmlModal)

  if (props.modelValue) {
    quill.root.innerHTML = props.modelValue
  }
  quill.on('text-change', () => {
    emit('update:modelValue', quill.root.innerHTML)
  })
  editorEl.value.querySelector('.ql-editor').style.minHeight = props.minHeight
})

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
.rte-wrapper { position: relative; border: 1px solid #d1d5db; border-radius: 8px; overflow: hidden; }
.rte-wrapper :deep(.ql-toolbar) { border: none; border-bottom: 1px solid #e5e7eb; background: #f9fafb; }
.rte-wrapper :deep(.ql-container) { border: none; font-size: 14px; }
.rte-wrapper :deep(.ql-editor) { padding: 10px 12px; }

/* Custom toolbar buttons (outside Quill's button size rules) */
.rte-custom-btn {
  float: left;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: auto;
  min-width: 28px;
  height: 24px;
  padding: 3px 5px;
  font-size: 13px;
  font-weight: 600;
  font-family: inherit;
  background: none;
  color: #444;
  border: none;
  border-radius: 0;
  cursor: pointer;
  line-height: 1;
  transition: color 0.15s;
  vertical-align: middle;
}
.rte-custom-btn:hover { color: #06c; }

/* Slight breathing room between custom controls */
.rte-custom-btn + .rte-custom-btn { margin-left: 6px; }

/* Keep </> weight close to icon buttons */
.rte-custom-btn[title="Insert raw HTML"] {
  font-size: 12px;
  font-weight: 500;
}

/* Raw-HTML embed block */
.rte-wrapper :deep(.ql-raw-html) { display: block; margin: 0.5rem 0; }

/* Table styles — inside both the embed wrapper and plain editor content */
.rte-wrapper :deep(.ql-raw-html table),
.rte-wrapper :deep(.ql-editor table) { width: 100%; border-collapse: collapse; margin: 0.25rem 0; }
.rte-wrapper :deep(.ql-raw-html td),
.rte-wrapper :deep(.ql-raw-html th),
.rte-wrapper :deep(.ql-editor td),
.rte-wrapper :deep(.ql-editor th) { border: 1px solid #94a3b8; padding: 0.4rem 0.6rem; vertical-align: top; min-width: 60px; }
.rte-wrapper :deep(.ql-raw-html th),
.rte-wrapper :deep(.ql-editor th) { background: #f1f5f9; font-weight: 700; }

/* Raw HTML modal */
.rte-html-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}
.rte-html-modal {
  background: #fff;
  border-radius: 10px;
  padding: 1.25rem 1.5rem;
  width: 520px;
  max-width: 94vw;
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
}
.rte-html-modal-header {
  font-weight: 700;
  font-size: 15px;
  margin-bottom: 0.75rem;
  color: #1e293b;
}
.rte-html-textarea {
  width: 100%;
  box-sizing: border-box;
  font-family: 'Consolas', 'Fira Code', monospace;
  font-size: 13px;
  border: 1px solid #cbd5e1;
  border-radius: 6px;
  padding: 0.6rem 0.75rem;
  resize: vertical;
  outline: none;
  background: #f8fafc;
  color: #0f172a;
}
.rte-html-textarea:focus { border-color: #6366f1; background: #fff; }
.rte-html-actions {
  display: flex;
  gap: 0.5rem;
  justify-content: flex-end;
  margin-top: 0.75rem;
}
.rte-btn {
  padding: 0.4rem 1rem;
  border-radius: 6px;
  border: 1px solid #cbd5e1;
  background: #f1f5f9;
  font-size: 13px;
  cursor: pointer;
  font-weight: 500;
}
.rte-btn:hover { background: #e2e8f0; }
.rte-btn-primary {
  background: #6366f1;
  color: #fff;
  border-color: #6366f1;
}
.rte-btn-primary:hover { background: #4f46e5; border-color: #4f46e5; }
</style>
