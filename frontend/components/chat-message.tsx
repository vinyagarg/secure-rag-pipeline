'use client'

import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import {
  Copy,
  Check,
  ThumbsUp,
  ThumbsDown,
  Share2,
  ChevronRight,
  Link as LinkIcon,
} from 'lucide-react'
import { ShieldMark } from './shield-mark'
import { CONFIDENCE_META } from '@/lib/mock-data'
import type { ChatMessage } from '@/lib/types'

function TypingIndicator() {
  return (
    <div className="flex items-center gap-1 py-1" aria-label="Assistant is thinking">
      {[0, 1, 2].map((i) => (
        <span
          key={i}
          className="typing-dot h-1.5 w-1.5 rounded-full bg-muted-foreground"
          style={{ animationDelay: `${i * 0.16}s` }}
        />
      ))}
    </div>
  )
}

function ConfidenceBadge({ level }: { level: NonNullable<ChatMessage['confidence']> }) {
  const meta = CONFIDENCE_META[level]
  return (
    <div className="flex items-center gap-1.5">
      <span
        className="h-2 w-2 rounded-full"
        style={{ backgroundColor: meta.varName }}
      />
      <span className="text-[10px] font-medium uppercase tracking-[0.12em] text-muted-foreground">
        {meta.label}
      </span>
    </div>
  )
}

function Sources({ sources }: { sources: NonNullable<ChatMessage['sources']> }) {
  const [open, setOpen] = useState(false)
  if (sources.length === 0) return null

  return (
    <div className="mt-3 overflow-hidden rounded-md border border-border">
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex w-full items-center gap-2 px-3 py-2 text-left text-[11px] font-medium uppercase tracking-[0.1em] text-muted-foreground transition-colors hover:text-foreground"
      >
        <ChevronRight
          size={13}
          className={`transition-transform ${open ? 'rotate-90' : ''}`}
        />
        {sources.length} {sources.length === 1 ? 'Source' : 'Sources'}
      </button>
      {open && (
        <ul className="flex flex-col gap-2 border-t border-border px-3 py-2.5">
          {sources.map((s, i) => (
            <li key={i} className="flex flex-col gap-0.5">
              <a
                href={s.url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1.5 text-[12.5px] text-[color:var(--link)] hover:underline"
              >
                <LinkIcon size={11} className="shrink-0" />
                {s.title}
              </a>
              <span className="pl-[18px] text-[11.5px] leading-relaxed text-muted-foreground">
                {s.snippet}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

function ResponseActions() {
  const [copied, setCopied] = useState(false)
  const [vote, setVote] = useState<'up' | 'down' | null>(null)

  const iconClass =
    'flex h-6 w-6 items-center justify-center rounded text-muted-foreground transition-colors hover:bg-accent hover:text-foreground'

  return (
    <div className="mt-2 flex items-center gap-0.5 opacity-0 transition-opacity group-hover:opacity-100">
      <button
        className={iconClass}
        aria-label="Copy response"
        onClick={() => {
          setCopied(true)
          setTimeout(() => setCopied(false), 1200)
        }}
      >
        {copied ? <Check size={13} className="text-[color:var(--confidence-high)]" /> : <Copy size={13} />}
      </button>
      <button
        className={iconClass}
        aria-label="Good response"
        data-active={vote === 'up'}
        onClick={() => setVote(vote === 'up' ? null : 'up')}
      >
        <ThumbsUp
          size={13}
          className={vote === 'up' ? 'text-[color:var(--confidence-high)]' : ''}
        />
      </button>
      <button
        className={iconClass}
        aria-label="Bad response"
        onClick={() => setVote(vote === 'down' ? null : 'down')}
      >
        <ThumbsDown
          size={13}
          className={vote === 'down' ? 'text-[color:var(--confidence-low)]' : ''}
        />
      </button>
      <button className={iconClass} aria-label="Share response">
        <Share2 size={13} />
      </button>
    </div>
  )
}

export function ChatMessageItem({ message }: { message: ChatMessage }) {
  if (message.role === 'user') {
    return (
      <div className="flex justify-end">
        <div className="max-w-[80%] rounded-lg rounded-br-sm border border-border bg-card px-3.5 py-2.5 text-[14px] leading-relaxed text-foreground">
          {message.content}
        </div>
      </div>
    )
  }

  return (
    <div className="group flex gap-3">
      <div className="mt-0.5 flex h-7 w-7 shrink-0 items-center justify-center rounded-md border border-border bg-card">
        <ShieldMark size={14} />
      </div>

      <div className="min-w-0 flex-1">
        {message.pending ? (
          <TypingIndicator />
        ) : (
          <>
            <div className="md-content">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {message.content}
              </ReactMarkdown>
              {message.streaming && <span className="streaming-cursor" />}
            </div>

            {!message.streaming && (
              <>
                {message.confidence && (
                  <div className="mt-3">
                    <ConfidenceBadge level={message.confidence} />
                  </div>
                )}
                {message.sources && <Sources sources={message.sources} />}
                <ResponseActions />
              </>
            )}
          </>
        )}
      </div>
    </div>
  )
}
