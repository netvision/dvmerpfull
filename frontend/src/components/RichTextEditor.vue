<template>
  <div class="rte-wrapper" :style="{ '--rte-min-height': minHeight }">
    <div v-if="editor" class="rte-toolbar">
      <div class="rte-toolbar-row">
        <button type="button" class="rte-tool-btn rte-tool-btn--icon" title="Bold" aria-label="Bold" :class="{ 'rte-tool-btn--active': editor.isActive('bold') }" @click="editor.chain().focus().toggleBold().run()"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M4 2.5h4.6c2 0 3.2 1.1 3.2 2.7 0 1.2-.7 2-1.8 2.4 1.5.3 2.4 1.4 2.4 2.9 0 1.9-1.4 3-3.8 3H4v-11zm2 1.7v2.7h2.2c1.1 0 1.7-.5 1.7-1.4s-.6-1.3-1.7-1.3H6zm0 4.3v3.1h2.5c1.2 0 1.9-.6 1.9-1.5 0-1-.7-1.6-2-1.6H6z" fill="currentColor"/></svg></button>
        <button type="button" class="rte-tool-btn rte-tool-btn--icon" title="Italic" aria-label="Italic" :class="{ 'rte-tool-btn--active': editor.isActive('italic') }" @click="editor.chain().focus().toggleItalic().run()"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6.8 2.5h5.2v1.7H9.9l-2.7 7.6h2.1v1.7H4v-1.7h2.1l2.7-7.6H6.8V2.5z" fill="currentColor"/></svg></button>
        <button type="button" class="rte-tool-btn rte-tool-btn--icon" title="Underline" aria-label="Underline" :class="{ 'rte-tool-btn--active': editor.isActive('underline') }" @click="editor.chain().focus().toggleUnderline().run()"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M5 2.5v4.3c0 1.8 1.2 3 3 3s3-1.2 3-3V2.5h1.8v4.4c0 2.7-1.9 4.6-4.8 4.6S3.2 9.6 3.2 6.9V2.5H5zm-1.8 10.9h9.6V15H3.2v-1.6z" fill="currentColor"/></svg></button>
        <button type="button" class="rte-tool-btn rte-tool-btn--icon" title="Bullet list" aria-label="Bullet list" :class="{ 'rte-tool-btn--active': editor.isActive('bulletList') }" @click="editor.chain().focus().toggleBulletList().run()"><svg viewBox="0 0 16 16" aria-hidden="true"><circle cx="3" cy="4" r="1.2" fill="currentColor"/><circle cx="3" cy="8" r="1.2" fill="currentColor"/><circle cx="3" cy="12" r="1.2" fill="currentColor"/><path d="M6 3.2h7v1.6H6zm0 4h7v1.6H6zm0 4h7v1.6H6z" fill="currentColor"/></svg></button>
        <button type="button" class="rte-tool-btn rte-tool-btn--icon" title="Numbered list" aria-label="Numbered list" :class="{ 'rte-tool-btn--active': editor.isActive('orderedList') }" @click="editor.chain().focus().toggleOrderedList().run()"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2.2 3h1.2v3H2.2v-.8h.5V3.8h-.5V3zm-.1 5.4c0-.9.6-1.5 1.7-1.5 1 0 1.7.5 1.7 1.4 0 .6-.3 1-.9 1.5l-.9.7H5.5V12H2v-1.2l1.5-1.2c.4-.3.6-.5.6-.8 0-.3-.2-.5-.6-.5s-.7.2-.7.7H2.1zm4.9-1h7v1.6H7zm0 4h7V13H7z" fill="currentColor"/></svg></button>
        <button type="button" class="rte-tool-btn rte-tool-btn--icon" title="Insert link" aria-label="Insert link" @click="openLinkPrompt"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M6.5 10.7H4.8A2.8 2.8 0 0 1 4.8 5h2.1v1.7H4.8a1.1 1.1 0 1 0 0 2.3h1.7v1.7zm4.7 0H9.1V9h2.1a1.1 1.1 0 1 0 0-2.3H9.5V5h1.7a2.8 2.8 0 1 1 0 5.7zM5.9 8.8V7.2h4.2v1.6H5.9z" fill="currentColor"/></svg></button>
        <button type="button" class="rte-tool-btn rte-tool-btn--icon" title="Insert image" aria-label="Insert image" @click="selectAndInsertImage"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 3.2h10a1 1 0 0 1 1 1v7.6a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V4.2a1 1 0 0 1 1-1zm0 1.6v6.4h10V4.8H3zm2 4.8 1.7-1.9 1.6 1.7 2.2-2.5 2 2.7H5zm1-3.5a1.1 1.1 0 1 1 0 2.2 1.1 1.1 0 0 1 0-2.2z" fill="currentColor"/></svg></button>
        <button type="button" class="rte-tool-btn rte-tool-btn--icon" title="Insert table" aria-label="Insert table" @click="insertTable"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2.5 3h11v10h-11V3zm1.5 1.5v2h3v-2h-3zm4.5 0v2h3v-2h-3zm-4.5 3.5v2h3V8h-3zm4.5 0v2h3V8h-3zm4 0v2H12V8h.5zm0-3.5v2H12v-2h.5zM4 11.5h3v0H4zm4.5 0h3v0h-3z" fill="currentColor"/></svg></button>
        <button type="button" class="rte-tool-btn rte-tool-btn--icon" title="Insert raw HTML" aria-label="Insert raw HTML" @click="openHtmlModal"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M5.6 4.1 2.8 8l2.8 3.9H3.7L1 8l2.7-3.9h1.9zm4.1-1.4h1.7l-2.1 10.6H7.6L9.7 2.7zm2.6 1.4h1.9L17 8l-2.8 3.9h-1.9L15.1 8l-2.8-3.9z" fill="currentColor" transform="translate(-1 0)"/></svg></button>
        <button type="button" class="rte-tool-btn rte-tool-btn--icon" title="Clear formatting" aria-label="Clear formatting" @click="clearFormatting"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="m3.6 12.4 6.9-6.9 1.1 1.1-6.9 6.9H3.6v-1.1zm.6-5.9L6 4.7l3.8 3.8L8.7 9.6 7.6 8.5 5.4 10.7H3.8l2.7-2.7-2.3-2.3zm7.8 5.7H7.8v1.6H12v-1.6z" fill="currentColor"/></svg></button>
      </div>

      <div v-if="editor.isActive('table')" class="rte-toolbar-row rte-toolbar-row--table">
        <button type="button" class="rte-tool-btn rte-tool-btn--icon rte-tool-btn--table" title="Add row" aria-label="Add row" @click="editor.chain().focus().addRowAfter().run()"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2.5 3h8v10h-8V3zm1.5 1.5v2h5v-2H4zm0 3.5v2h5V8H4zm0 3.5h5v0H4zm8.5-2.3V7.8H14v1.4h1.4v1.4H14V12h-1.4v-1.4h-1.4V9.2h1.4z" fill="currentColor"/></svg></button>
        <button type="button" class="rte-tool-btn rte-tool-btn--icon rte-tool-btn--table" title="Add column" aria-label="Add column" @click="editor.chain().focus().addColumnAfter().run()"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 2.5h10v8H3v-8zm1.5 1.5v5h2V4h-2zm3.5 0v5h2V4H8zm3.5 0v5V4h-.5zM9.2 12.6H7.8V14H6.4v-1.4H5v-1.4h1.4V9.8h1.4v1.4h1.4v1.4z" fill="currentColor" transform="translate(1 0)"/></svg></button>
        <button type="button" class="rte-tool-btn rte-tool-btn--icon rte-tool-btn--table" title="Delete row" aria-label="Delete row" @click="editor.chain().focus().deleteRow().run()"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2.5 3h8v10h-8V3zm1.5 1.5v2h5v-2H4zm0 3.5v2h5V8H4zm0 3.5h5v0H4zm7.2-2h4.3v1.4h-4.3z" fill="currentColor"/></svg></button>
        <button type="button" class="rte-tool-btn rte-tool-btn--icon rte-tool-btn--table" title="Delete column" aria-label="Delete column" @click="editor.chain().focus().deleteColumn().run()"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 2.5h10v8H3v-8zm1.5 1.5v5h2V4h-2zm3.5 0v5h2V4H8zm3.5 0v5V4h-.5zm-1.1 8.1h4.3v1.4h-4.3z" fill="currentColor" transform="translate(0 -1)"/></svg></button>
        <button type="button" class="rte-tool-btn rte-tool-btn--icon rte-tool-btn--table" title="Toggle header row" aria-label="Toggle header row" @click="editor.chain().focus().toggleHeaderRow().run()"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M2.5 3h11v10h-11V3zm1.5 1.5v2H12v-2H4zm0 3.5v3.5h2.5V8H4zm4 0v3.5H12V8H8z" fill="currentColor"/></svg></button>
        <button type="button" class="rte-tool-btn rte-tool-btn--icon rte-tool-btn--danger" title="Delete table" aria-label="Delete table" @click="editor.chain().focus().deleteTable().run()"><svg viewBox="0 0 16 16" aria-hidden="true"><path d="M3 3h10v10H3V3zm2.1 2.1L8 8l2.9-2.9L12 6.2 9.1 9.1 12 12l-1.1 1.1L8 10.2l-2.9 2.9L4 12l2.9-2.9L4 6.2l1.1-1.1z" fill="currentColor"/></svg></button>
      </div>
    </div>

    <EditorContent :editor="editor" class="rte-editor" />

    <div v-if="showHtmlModal" class="rte-html-overlay" @click.self="cancelHtml">
      <div class="rte-html-modal">
        <div class="rte-html-modal-header">Insert Raw HTML</div>
        <textarea
          v-model="rawHtmlInput"
          class="rte-html-textarea"
          rows="8"
          placeholder="<table><tr><td>...</td></tr></table>"
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
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { Editor, EditorContent } from '@tiptap/vue-3'
import { StarterKit } from '@tiptap/starter-kit'
import { Underline } from '@tiptap/extension-underline'
import { Link } from '@tiptap/extension-link'
import { Image } from '@tiptap/extension-image'
import { Table } from '@tiptap/extension-table'
import { TableRow } from '@tiptap/extension-table-row'
import { TableHeader } from '@tiptap/extension-table-header'
import { TableCell } from '@tiptap/extension-table-cell'
import { Placeholder } from '@tiptap/extension-placeholder'
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

const editor = ref(null)
const showHtmlModal = ref(false)
const rawHtmlInput = ref('')

function getEditorHtml() {
  if (!editor.value) return ''
  return editor.value.isEmpty ? '' : editor.value.getHTML()
}

function cancelHtml() {
  showHtmlModal.value = false
  rawHtmlInput.value = ''
}

function confirmInsertHtml() {
  const html = rawHtmlInput.value.trim()
  if (html && editor.value) {
    editor.value.chain().focus().insertContent(html).run()
  }
  cancelHtml()
}

function openHtmlModal() {
  rawHtmlInput.value = ''
  showHtmlModal.value = true
}

function clearFormatting() {
  if (!editor.value) return
  editor.value.chain().focus().clearNodes().unsetAllMarks().run()
}

function openLinkPrompt() {
  if (!editor.value) return
  const previousUrl = editor.value.getAttributes('link').href || 'https://'
  const url = window.prompt('Enter URL', previousUrl)
  if (url === null) return
  if (!url.trim()) {
    editor.value.chain().focus().extendMarkRange('link').unsetLink().run()
    return
  }
  editor.value.chain().focus().extendMarkRange('link').setLink({ href: url.trim() }).run()
}

async function selectAndInsertImage() {
  if (!editor.value) return
  const input = document.createElement('input')
  input.type = 'file'
  input.accept = 'image/*'
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

      editor.value.chain().focus().setImage({ src: buildAssetUrl(res.data?.url) }).run()
    } catch (error) {
      alert(error.response?.data?.detail || 'Image upload failed')
    }
  }
}

function insertTable() {
  if (!editor.value) return
  const rowsInput = window.prompt('Number of rows', '3')
  if (rowsInput === null) return
  const colsInput = window.prompt('Number of columns', '3')
  if (colsInput === null) return

  const rows = Math.max(1, Math.min(20, Number.parseInt(rowsInput, 10) || 3))
  const cols = Math.max(1, Math.min(20, Number.parseInt(colsInput, 10) || 3))

  editor.value.chain().focus().insertTable({ rows, cols, withHeaderRow: true }).run()
}

onMounted(() => {
  editor.value = new Editor({
    content: props.modelValue || '',
    extensions: [
      StarterKit,
      Underline,
      Link.configure({
        openOnClick: false,
        autolink: true,
        defaultProtocol: 'https',
      }),
      Image,
      Table.configure({ resizable: true }),
      TableRow,
      TableHeader,
      TableCell,
      Placeholder.configure({ placeholder: props.placeholder }),
    ],
    editorProps: {
      attributes: {
        class: 'rte-prosemirror',
      },
    },
    onUpdate: () => {
      emit('update:modelValue', getEditorHtml())
    },
  })
})

watch(
  () => props.modelValue,
  (value) => {
    if (!editor.value) return
    const currentHtml = getEditorHtml()
    const nextHtml = value || ''
    if (currentHtml !== nextHtml) {
      editor.value.commands.setContent(nextHtml, { emitUpdate: false })
    }
  }
)

onBeforeUnmount(() => {
  if (editor.value) {
    editor.value.destroy()
    editor.value = null
  }
})
</script>

<style scoped>
.rte-wrapper {
  --rte-min-height: 120px;
  position: relative;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  overflow: hidden;
  background: #fff;
}

.rte-toolbar {
  border-bottom: 1px solid #e5e7eb;
  background: #f9fafb;
  padding: 0.45rem 0.55rem;
}

.rte-toolbar-row {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
}

.rte-toolbar-row + .rte-toolbar-row {
  margin-top: 0.45rem;
  padding-top: 0.45rem;
  border-top: 1px solid #e5e7eb;
}

.rte-tool-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  height: 30px;
  padding: 0 0.7rem;
  border: 1px solid transparent;
  border-radius: 6px;
  background: transparent;
  color: #374151;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s, color 0.15s, border-color 0.15s;
}

.rte-tool-btn--icon {
  width: 30px;
  min-width: 30px;
  padding: 0;
  font-size: 13px;
}

.rte-tool-btn--icon svg {
  width: 15px;
  height: 15px;
  display: block;
}

.rte-tool-btn:hover {
  background: #eef2ff;
  color: #1d4ed8;
}

.rte-tool-btn--active {
  background: #dbeafe;
  border-color: #bfdbfe;
  color: #1d4ed8;
}

.rte-tool-btn--table {
  width: 34px;
  min-width: 34px;
  font-size: 11px;
  letter-spacing: -0.02em;
}

.rte-tool-btn--danger {
  color: #b91c1c;
}

.rte-tool-btn--danger:hover {
  background: #fee2e2;
  color: #991b1b;
}

.rte-editor :deep(.tiptap) {
  min-height: var(--rte-min-height);
  padding: 10px 12px;
  font-size: 14px;
  line-height: 1.55;
  color: #111827;
  outline: none;
}

.rte-editor :deep(.tiptap p.is-editor-empty:first-child::before) {
  content: attr(data-placeholder);
  color: #9ca3af;
  pointer-events: none;
  float: left;
  height: 0;
}

.rte-editor :deep(.tiptap p) {
  margin: 0 0 0.65rem;
}

.rte-editor :deep(.tiptap ul),
.rte-editor :deep(.tiptap ol) {
  margin: 0 0 0.75rem 1.2rem;
  padding: 0;
}

.rte-editor :deep(.tiptap a) {
  color: #2563eb;
  text-decoration: underline;
}

.rte-editor :deep(.tiptap img) {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0.6rem 0;
  border-radius: 6px;
}

.rte-editor :deep(.tiptap table) {
  border-collapse: collapse;
  table-layout: fixed;
  width: 100%;
  margin: 0.75rem 0;
  overflow: hidden;
}

.rte-editor :deep(.tiptap th),
.rte-editor :deep(.tiptap td) {
  position: relative;
  border: 1px solid rgba(0, 0, 0, 0.32);
  min-width: 1em;
  padding: 0.5rem 0.65rem;
  vertical-align: top;
  box-sizing: border-box;
}

.rte-editor :deep(.tiptap th) {
  background: #f8fafc;
  font-weight: 700;
}

.rte-editor :deep(.tiptap .selectedCell::after) {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(59, 130, 246, 0.12);
  pointer-events: none;
}

.rte-editor :deep(.tiptap .column-resize-handle) {
  position: absolute;
  top: 0;
  right: -2px;
  bottom: -2px;
  width: 4px;
  background: #60a5fa;
  pointer-events: none;
}

.rte-editor :deep(.tiptap .tableWrapper) {
  overflow-x: auto;
}

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
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.18);
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

.rte-html-textarea:focus {
  border-color: #6366f1;
  background: #fff;
}

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

.rte-btn:hover {
  background: #e2e8f0;
}

.rte-btn-primary {
  background: #6366f1;
  color: #fff;
  border-color: #6366f1;
}

.rte-btn-primary:hover {
  background: #4f46e5;
  border-color: #4f46e5;
}
</style>