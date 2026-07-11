'use client'

import { useRef, useState } from 'react'
import { X, UploadCloud, FileText, Trash2, AlertCircle } from 'lucide-react'
import type { UploadedDoc } from '@/lib/types'
import { extractText } from '@/lib/extract-text'

const ACCEPTED = '.pdf,.txt,.md'

function formatSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export function UploadModal({
  open,
  docs,
  onClose,
  onAdd,
  onRemove,
}: {
  open: boolean
  docs: UploadedDoc[]
  onClose: () => void
  onAdd: (doc: UploadedDoc) => void
  onRemove: (id: string) => void
}) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [dragging, setDragging] = useState(false)
  const [progress, setProgress] = useState<number | null>(null)

  if (!open) return null

  function ingest(files: FileList | null) {
    if (!files || files.length === 0) return
    const file = files[0]
    const ext = file.name.split('.').pop()?.toLowerCase() ?? ''
    if (!['pdf', 'txt', 'md'].includes(ext)) return

    // simulate upload progress
    setProgress(0)
    let p = 0
    const timer = setInterval(() => {
      p += Math.random() * 22 + 8
      if (p >= 100) {
        clearInterval(timer)
        setProgress(100)
        onAdd({
          id: `${Date.now()}`,
          name: file.name,
          size: file.size || Math.floor(Math.random() * 200_000) + 8_000,
          type: ext,
        })
        setTimeout(() => setProgress(null), 500)
      } else {
        setProgress(Math.floor(p))
      }
    }, 120)
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4"
      onClick={onClose}
    >
      <div
        className="thin-scroll max-h-[88svh] w-full max-w-[480px] overflow-y-auto rounded-lg border border-border bg-popover p-5"
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-label="Upload documents"
      >
        <div className="flex items-center justify-between">
          <h2 className="text-[14px] font-medium text-foreground">
            Upload documents
          </h2>
          <button
            onClick={onClose}
            aria-label="Close"
            className="flex h-7 w-7 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
          >
            <X size={15} />
          </button>
        </div>

        {/* Hidden file input (kept OUTSIDE the drop zone so the picker opens reliably) */}
        <input
          ref={inputRef}
          type="file"
          accept={ACCEPTED}
          className="sr-only"
          onChange={(e) => {
            ingest(e.target.files)
            // reset so selecting the same file again re-triggers change
            e.target.value = ''
          }}
        />

        {/* Drop zone */}
        <div
          role="button"
          tabIndex={0}
          onClick={() => inputRef.current?.click()}
          onKeyDown={(e) => {
            if (e.key === 'Enter' || e.key === ' ') {
              e.preventDefault()
              inputRef.current?.click()
            }
          }}
          onDragOver={(e) => {
            e.preventDefault()
            setDragging(true)
          }}
          onDragLeave={() => setDragging(false)}
          onDrop={(e) => {
            e.preventDefault()
            setDragging(false)
            ingest(e.dataTransfer.files)
          }}
          className={`mt-4 flex w-full cursor-pointer flex-col items-center justify-center gap-2 rounded-lg border border-dashed px-4 py-8 text-center outline-none transition-colors focus-visible:border-[color:var(--link)] ${
            dragging
              ? 'border-[color:var(--link)] bg-accent'
              : 'border-border-strong hover:bg-accent/50'
          }`}
        >
          <UploadCloud size={22} className="text-muted-foreground" />
          <span className="text-[13px] text-foreground">
            Drag &amp; drop or tap to browse
          </span>
          <span className="text-[11px] uppercase tracking-[0.12em] text-muted-foreground">
            PDF · TXT · MD
          </span>
        </div>

        {/* Progress */}
        {progress !== null && (
          <div className="mt-3">
            <div className="mb-1 flex justify-between text-[11px] text-muted-foreground">
              <span>Uploading…</span>
              <span className="font-mono">{progress}%</span>
            </div>
            <div className="h-1 w-full overflow-hidden rounded-full bg-border">
              <div
                className="h-full rounded-full bg-[color:var(--link)] transition-all duration-150"
                style={{ width: `${progress}%` }}
              />
            </div>
          </div>
        )}

        {/* Doc list */}
        <div className="mt-4">
          <div className="mb-2 text-[10px] font-medium uppercase tracking-[0.13em] text-muted-foreground">
            Indexed ({docs.length})
          </div>
          <ul className="thin-scroll flex max-h-[180px] flex-col gap-1.5 overflow-y-auto">
            {docs.length === 0 ? (
              <li className="py-2 text-[12px] text-muted-foreground">
                No documents yet.
              </li>
            ) : (
              docs.map((d) => (
                <li
                  key={d.id}
                  className="flex items-center gap-2.5 rounded-md border border-border bg-card px-3 py-2"
                >
                  <FileText size={14} className="shrink-0 text-muted-foreground" />
                  <div className="flex min-w-0 flex-1 flex-col">
                    <span className="truncate text-[12.5px] text-foreground">
                      {d.name}
                    </span>
                    <span className="font-mono text-[10px] text-muted-foreground">
                      {formatSize(d.size)} · {d.type.toUpperCase()}
                    </span>
                  </div>
                  <button
                    onClick={() => onRemove(d.id)}
                    aria-label={`Remove ${d.name}`}
                    className="flex h-6 w-6 shrink-0 items-center justify-center rounded text-muted-foreground transition-colors hover:bg-accent hover:text-[color:var(--confidence-low)]"
                  >
                    <Trash2 size={13} />
                  </button>
                </li>
              ))
            )}
          </ul>
        </div>
      </div>
    </div>
  )
}
