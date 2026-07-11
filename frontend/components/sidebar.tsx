'use client'

import { Plus, Trash2, Download, LogOut, MessageSquare } from 'lucide-react'
import { ShieldMark } from './shield-mark'
import { SUGGESTED_QUESTIONS, TECH_STACK } from '@/lib/mock-data'
import type { Role } from '@/lib/types'

function SectionLabel({ children }: { children: React.ReactNode }) {
  return (
    <div className="px-3 pb-1.5 pt-4 text-[10px] font-medium uppercase tracking-[0.14em] text-muted-foreground">
      {children}
    </div>
  )
}

export function Sidebar({
  role,
  history,
  onAsk,
  onNewChat,
  onClear,
  onExport,
  onSignOut,
  onNavigate,
}: {
  role: Role
  history: string[]
  onAsk: (q: string) => void
  onNewChat: () => void
  onClear: () => void
  onExport: () => void
  onSignOut: () => void
  onNavigate?: () => void
}) {
  const ask = (q: string) => {
    onAsk(q)
    onNavigate?.()
  }
  const run = (fn: () => void) => () => {
    fn()
    onNavigate?.()
  }
  return (
    <aside className="flex h-full w-[86vw] max-w-[300px] shrink-0 flex-col border-r border-border bg-sidebar md:w-[220px]">
      {/* Brand */}
      <div className="flex items-center gap-2 border-b border-border px-4 py-3.5">
        <ShieldMark size={16} />
        <span className="text-[14px] font-semibold tracking-tight text-foreground">
          RAGuard
        </span>
        {role === 'admin' && (
          <span className="ml-auto rounded border border-border-strong px-1.5 py-0.5 text-[9px] font-medium uppercase tracking-[0.12em] text-muted-foreground">
            Admin
          </span>
        )}
      </div>

      {/* Scrollable content */}
      <div className="thin-scroll flex-1 overflow-y-auto pb-2">
        <SectionLabel>Suggested</SectionLabel>
        <nav className="flex flex-col px-2">
          {SUGGESTED_QUESTIONS.map((q) => (
            <button
              key={q}
              onClick={() => ask(q)}
              className="rounded-md px-2 py-1.5 text-left text-[12.5px] leading-snug text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
            >
              {q}
            </button>
          ))}
        </nav>

        <SectionLabel>History</SectionLabel>
        <nav className="flex flex-col px-2">
          {history.length === 0 ? (
            <span className="px-2 py-1.5 text-[12px] text-muted-foreground">
              No queries yet
            </span>
          ) : (
            history.slice(0, 5).map((q, i) => (
              <button
                key={`${q}-${i}`}
                onClick={() => ask(q)}
                className="flex items-center gap-2 rounded-md px-2 py-1.5 text-left text-[12.5px] text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
              >
                <MessageSquare size={12} className="shrink-0 opacity-60" />
                <span className="truncate">{q}</span>
              </button>
            ))
          )}
        </nav>
      </div>

      {/* Bottom actions */}
      <div className="flex flex-col gap-0.5 border-t border-border p-2">
        <SidebarAction icon={<Plus size={14} />} label="New chat" onClick={run(onNewChat)} />
        <SidebarAction icon={<Trash2 size={14} />} label="Clear" onClick={run(onClear)} />
        <SidebarAction
          icon={<Download size={14} />}
          label="Export"
          onClick={onExport}
        />
        <SidebarAction
          icon={<LogOut size={14} />}
          label="Sign out"
          onClick={onSignOut}
        />
      </div>

      {/* Footer */}
      <div className="border-t border-border px-3 py-2.5">
        <p className="text-[10px] leading-relaxed tracking-wide text-muted-foreground">
          {TECH_STACK}
        </p>
      </div>
    </aside>
  )
}

function SidebarAction({
  icon,
  label,
  onClick,
}: {
  icon: React.ReactNode
  label: string
  onClick: () => void
}) {
  return (
    <button
      onClick={onClick}
      className="flex items-center gap-2.5 rounded-md px-2.5 py-2 text-[12.5px] text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
    >
      <span className="shrink-0 opacity-80">{icon}</span>
      {label}
    </button>
  )
}
