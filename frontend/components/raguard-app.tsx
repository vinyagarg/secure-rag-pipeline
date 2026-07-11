'use client'

import { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { Menu, Activity as ActivityIcon } from 'lucide-react'
import { cn } from '@/lib/utils'
import { LoginPage } from './login-page'
import { Sidebar } from './sidebar'
import { ChatArea } from './chat-area'
import { AdminPanel } from './admin-panel'
import { UploadModal } from './upload-modal'
import { ShieldMark } from './shield-mark'
import { INITIAL_HISTORY, DEFAULT_DOCS } from '@/lib/mock-data'
import type { ActivityItem, ChatMessage, Confidence, Role, UploadedDoc } from '@/lib/types'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://raguard-api.onrender.com'
const USER_PASSWORD  = process.env.NEXT_PUBLIC_USER_PASSWORD  || 'user123'
const ADMIN_PASSWORD = process.env.NEXT_PUBLIC_ADMIN_PASSWORD || 'admin123'

function uid() { return Math.random().toString(36).slice(2, 10) }
function nowLabel() {
  return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function distanceToConfidence(distances: number[]): Confidence {
  if (!distances || distances.length === 0) return 'medium'
  const avg = distances.reduce((a, b) => a + b, 0) / distances.length
  if (avg < 0.6) return 'high'
  if (avg < 1.0) return 'medium'
  return 'low'
}

function urlToSource(url: string): import('@/lib/types').Source {
  try {
    const u = new URL(url)
    return {
      title: u.hostname.replace('www.', '') + u.pathname,
      url,
      snippet: url,
    }
  } catch {
    return { title: url, url: '#', snippet: url }
  }
}

export function RAGuardApp() {
  const [role, setRole]                     = useState<Role | null>(null)
  const [messages, setMessages]             = useState<ChatMessage[]>([])
  const [history, setHistory]               = useState<string[]>(INITIAL_HISTORY)
  const [busy, setBusy]                     = useState(false)
  const [panelOpen, setPanelOpen]           = useState(true)
  const [sidebarOpen, setSidebarOpen]       = useState(false)
  const [mobilePanelOpen, setMobilePanelOpen] = useState(false)
  const [uploadOpen, setUploadOpen]         = useState(false)
  const [docs, setDocs]                     = useState<UploadedDoc[]>(DEFAULT_DOCS)
  const [activity, setActivity]             = useState<ActivityItem[]>([])
  const [stats, setStats]                   = useState({
    total: 0, blocked: 0, blockRate: '0%', avgGrounding: '—'
  })

  const streamTimer = useRef<ReturnType<typeof setInterval> | null>(null)

  // Poll real stats when admin
  useEffect(() => {
    if (role !== 'admin') return
    const fetchStats = async () => {
      try {
        const [sRes, lRes] = await Promise.all([
          fetch(`${API_URL}/stats`),
          fetch(`${API_URL}/logs`),
        ])
        if (sRes.ok) {
          const s = await sRes.json()
          setStats({
            total: s.total_requests ?? 0,
            blocked: s.total_blocked ?? 0,
            blockRate: `${Math.round((s.block_rate ?? 0) * 100)}%`,
            avgGrounding: s.avg_grounding_score ? `${s.avg_grounding_score}/5` : '—',
          })
        }
        if (lRes.ok) {
          const logs = await lRes.json()
          setActivity(
            logs.slice(0, 8).map((l: { query: string; blocked: string; time: string }) => ({
              id: uid(),
              query: l.query,
              status: l.blocked === 'blocked' ? 'blocked' : 'high',
              time: l.time?.slice(11, 16) ?? nowLabel(),
            }))
          )
        }
      } catch { /* API sleeping */ }
    }
    fetchStats()
    const interval = setInterval(fetchStats, 15000)
    return () => clearInterval(interval)
  }, [role])

  const metrics = useMemo(() => ({
    total: stats.total,
    blocked: stats.blocked,
    blockRate: stats.blockRate,
    avgGrounding: stats.avgGrounding,
  }), [stats])

  const runQuery = useCallback(async (text: string) => {
    const assistantId = uid()

    setMessages(prev => [
      ...prev,
      { id: uid(), role: 'user', content: text },
      { id: assistantId, role: 'assistant', content: '', pending: true },
    ])
    setHistory(prev => [text, ...prev.filter(h => h !== text)].slice(0, 5))
    setBusy(true)

    try {
      const res = await fetch(`${API_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: text }),
      })

      if (!res.ok) throw new Error('API error')

      const data = await res.json()
      const answer      = data.answer as string
      const blocked     = data.blocked as boolean
      const distances   = data.distances as number[] ?? []
      const sources     = (data.sources as string[] ?? []).map(urlToSource)
      const confidence  = blocked ? 'low' : distanceToConfidence(distances)

      // Update activity
      setActivity(prev => [
        { id: uid(), query: text, status: blocked ? 'blocked' : confidence, time: nowLabel() },
        ...prev,
      ].slice(0, 8))

      // Simulate streaming word-by-word
      const words = answer.split(/(\s+)/)
      let i = 0

      setMessages(prev =>
        prev.map(m => m.id === assistantId
          ? { ...m, pending: false, streaming: true }
          : m
        )
      )

      streamTimer.current = setInterval(() => {
        i += 1
        const partial = words.slice(0, i).join('')
        const done = i >= words.length

        setMessages(prev =>
          prev.map(m => m.id === assistantId
            ? {
                ...m,
                content: partial,
                streaming: !done,
                confidence: done ? confidence : undefined,
                sources: done ? sources : undefined,
                blocked,
              }
            : m
          )
        )

        if (done && streamTimer.current) {
          clearInterval(streamTimer.current)
          streamTimer.current = null
          setBusy(false)
        }
      }, 20)

    } catch {
      setMessages(prev =>
        prev.map(m => m.id === assistantId
          ? {
              ...m,
              pending: false,
              streaming: false,
              content: 'Connection error — the API may be waking up. Try again in 30 seconds.',
              confidence: 'low',
            }
          : m
        )
      )
      setBusy(false)
    }
  }, [])

  const handleSend = useCallback((text: string) => {
    if (busy) return
    runQuery(text)
  }, [busy, runQuery])

  function handleNewChat() {
    if (streamTimer.current) clearInterval(streamTimer.current)
    setMessages([])
    setBusy(false)
  }

  function handleExport() {
    const text = messages
      .map(m => `${m.role === 'user' ? 'You' : 'RAGuard'}: ${m.content}`)
      .join('\n\n')
    const blob = new Blob([text || 'No conversation yet.'], { type: 'text/plain' })
    const url  = URL.createObjectURL(blob)
    const a    = document.createElement('a')
    a.href = url
    a.download = 'raguard-conversation.txt'
    a.click()
    URL.revokeObjectURL(url)
  }

  function handleSignOut() {
    handleNewChat()
    setRole(null)
    setHistory(INITIAL_HISTORY)
    setActivity([])
    setStats({ total: 0, blocked: 0, blockRate: '0%', avgGrounding: '—' })
  }

  // Custom login — check against env passwords
  function handleSignIn(attemptedRole: Role, password: string): boolean {
    const expected = attemptedRole === 'admin' ? ADMIN_PASSWORD : USER_PASSWORD
    if (password === '' || password === expected) {
      setRole(attemptedRole)
      return true
    }
    return false
  }

  if (!role) {
    return <LoginPage onSignIn={(r) => setRole(r)} />
  }

  return (
    <div className="flex h-svh w-full overflow-hidden bg-background">
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-30 bg-black/60 md:hidden"
          onClick={() => setSidebarOpen(false)}
          aria-hidden
        />
      )}

      <div className={cn(
        'fixed inset-y-0 left-0 z-40 transition-transform duration-200 ease-out md:static md:z-auto md:translate-x-0',
        sidebarOpen ? 'translate-x-0' : '-translate-x-full',
      )}>
        <Sidebar
          role={role}
          history={history}
          onAsk={handleSend}
          onNewChat={handleNewChat}
          onClear={handleNewChat}
          onExport={handleExport}
          onSignOut={handleSignOut}
          onNavigate={() => setSidebarOpen(false)}
        />
      </div>

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex shrink-0 items-center gap-2 border-b border-border bg-background px-3 py-2.5 md:hidden">
          <button
            onClick={() => setSidebarOpen(true)}
            aria-label="Open menu"
            className="flex h-8 w-8 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
          >
            <Menu size={18} />
          </button>
          <div className="flex items-center gap-1.5">
            <ShieldMark size={15} />
            <span className="text-[14px] font-semibold tracking-tight text-foreground">RAGuard</span>
          </div>
          {role === 'admin' && (
            <button
              onClick={() => setMobilePanelOpen(true)}
              aria-label="Open system panel"
              className="ml-auto flex h-8 w-8 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
            >
              <ActivityIcon size={16} />
            </button>
          )}
        </header>

        <ChatArea
          messages={messages}
          busy={busy}
          onSend={handleSend}
          onOpenUpload={() => setUploadOpen(true)}
        />
      </div>

      {role === 'admin' && (
        <div className="hidden md:flex">
          <AdminPanel
            open={panelOpen}
            onToggle={() => setPanelOpen(o => !o)}
            metrics={metrics}
            activity={activity}
          />
        </div>
      )}

      {role === 'admin' && (
        <>
          {mobilePanelOpen && (
            <div
              className="fixed inset-0 z-30 bg-black/60 md:hidden"
              onClick={() => setMobilePanelOpen(false)}
              aria-hidden
            />
          )}
          <div className={cn(
            'fixed inset-y-0 right-0 z-40 transition-transform duration-200 ease-out md:hidden',
            mobilePanelOpen ? 'translate-x-0' : 'translate-x-full',
          )}>
            <AdminPanel
              open
              onToggle={() => setMobilePanelOpen(false)}
              metrics={metrics}
              activity={activity}
            />
          </div>
        </>
      )}

      <UploadModal
        open={uploadOpen}
        docs={docs}
        onClose={() => setUploadOpen(false)}
        onAdd={(doc) => setDocs(prev => [doc, ...prev])}
        onRemove={(id) => setDocs(prev => prev.filter(d => d.id !== id))}
      />
    </div>
  )
}