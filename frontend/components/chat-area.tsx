'use client'

import { useEffect, useRef, useState } from 'react'
import { Send, Paperclip, ShieldCheck, Search, ScrollText, Zap } from 'lucide-react'
import { ShieldMark } from './shield-mark'
import { ChatMessageItem } from './chat-message'
import type { ChatMessage } from '@/lib/types'

const FEATURE_PILLS = [
  { icon: Search, label: 'Semantic retrieval' },
  { icon: ShieldCheck, label: 'Grounded answers' },
  { icon: ScrollText, label: 'Cited sources' },
  { icon: Zap, label: 'Confidence scoring' },
]

function EmptyState() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center px-6 text-center">
      <div className="flex h-14 w-14 items-center justify-center rounded-xl border border-border bg-card">
        <ShieldMark size={26} />
      </div>
      <h1 className="mt-5 text-[20px] font-semibold tracking-tight text-foreground text-balance">
        Ask anything, grounded in your sources
      </h1>
      <p className="mt-2 max-w-[420px] text-[13.5px] leading-relaxed text-muted-foreground text-pretty">
        RAGuard retrieves from your indexed documents and answers only from
        what it can cite — with a confidence score on every response.
      </p>
      <div className="mt-6 flex flex-wrap items-center justify-center gap-2">
        {FEATURE_PILLS.map(({ icon: Icon, label }) => (
          <div
            key={label}
            className="flex items-center gap-1.5 rounded-full border border-border bg-card px-3 py-1.5 text-[12px] text-muted-foreground"
          >
            <Icon size={13} />
            {label}
          </div>
        ))}
      </div>
    </div>
  )
}

export function ChatArea({
  messages,
  busy,
  onSend,
  onOpenUpload,
}: {
  messages: ChatMessage[]
  busy: boolean
  onSend: (text: string) => void
  onOpenUpload: () => void
}) {
  const [input, setInput] = useState('')
  const scrollRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    const el = scrollRef.current
    if (el) el.scrollTop = el.scrollHeight
  }, [messages])

  // auto-grow textarea
  useEffect(() => {
    const ta = textareaRef.current
    if (!ta) return
    ta.style.height = 'auto'
    ta.style.height = `${Math.min(ta.scrollHeight, 160)}px`
  }, [input])

  function submit() {
    const text = input.trim()
    if (!text || busy) return
    onSend(text)
    setInput('')
  }

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (
      e.key === 'Enter' &&
      !e.shiftKey &&
      !e.nativeEvent.isComposing &&
      e.keyCode !== 229
    ) {
      e.preventDefault()
      submit()
    }
  }

  const hasMessages = messages.length > 0

  return (
    <section className="flex h-full min-w-0 flex-1 flex-col bg-background">
      {/* Messages / empty state */}
      <div ref={scrollRef} className="thin-scroll flex-1 overflow-y-auto">
        {hasMessages ? (
          <div className="mx-auto flex w-full max-w-[760px] flex-col gap-6 px-5 py-8">
            {messages.map((m) => (
              <ChatMessageItem key={m.id} message={m} />
            ))}
          </div>
        ) : (
          <div className="flex h-full flex-col">
            <EmptyState />
          </div>
        )}
      </div>

      {/* Fixed input bar */}
      <div className="shrink-0 border-t border-border bg-background">
        <div className="mx-auto w-full max-w-[760px] px-5 py-4">
          <div className="flex items-end gap-2 rounded-lg border border-border bg-card px-2 py-2 transition-colors focus-within:border-border-strong">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              rows={1}
              placeholder="Ask anything about RAG, LLMs, or AI engineering…"
              className="max-h-40 flex-1 resize-none bg-transparent py-1.5 text-[14px] leading-relaxed text-foreground outline-none placeholder:text-muted-foreground"
            />
            <button
              onClick={submit}
              disabled={!input.trim() || busy}
              aria-label="Send message"
              className="flex h-8 shrink-0 items-center gap-1.5 rounded-md bg-primary px-3 text-[13px] font-medium text-primary-foreground transition-opacity hover:opacity-90 disabled:opacity-30"
            >
              <Send size={13} />
              Send
            </button>
          </div>
          <p className="mt-2 px-1 text-[10.5px] tracking-wide text-muted-foreground">
            <kbd className="font-mono">Enter</kbd> to send ·{' '}
            <kbd className="font-mono">Shift+Enter</kbd> for newline · answers are
            grounded in indexed sources
          </p>
        </div>
      </div>
    </section>
  )
}
