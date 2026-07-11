'use client'

import { PanelRightClose, PanelRightOpen } from 'lucide-react'
import type { ActivityItem } from '@/lib/types'

const STATUS_COLOR: Record<ActivityItem['status'], string> = {
  high: 'var(--confidence-high)',
  medium: 'var(--confidence-medium)',
  low: 'var(--confidence-low)',
  blocked: 'var(--confidence-low)',
}

interface Metrics {
  total: number
  blocked: number
  blockRate: string
  avgGrounding: string
}

function MetricCard({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col gap-1 rounded-md border border-border bg-card p-3">
      <span className="text-[9px] font-medium uppercase tracking-[0.13em] text-muted-foreground">
        {label}
      </span>
      <span className="font-mono text-[18px] leading-none text-foreground">
        {value}
      </span>
    </div>
  )
}

export function AdminPanel({
  open,
  onToggle,
  metrics,
  activity,
}: {
  open: boolean
  onToggle: () => void
  metrics: Metrics
  activity: ActivityItem[]
}) {
  if (!open) {
    return (
      <div className="flex h-full w-10 shrink-0 flex-col items-center border-l border-border bg-sidebar py-3">
        <button
          onClick={onToggle}
          aria-label="Expand system panel"
          className="flex h-7 w-7 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
        >
          <PanelRightOpen size={16} />
        </button>
      </div>
    )
  }

  return (
    <aside className="flex h-full w-[260px] shrink-0 flex-col border-l border-border bg-sidebar">
      <div className="flex items-center justify-between border-b border-border px-4 py-3.5">
        <span className="text-[11px] font-medium uppercase tracking-[0.14em] text-muted-foreground">
          System
        </span>
        <button
          onClick={onToggle}
          aria-label="Collapse system panel"
          className="flex h-6 w-6 items-center justify-center rounded-md text-muted-foreground transition-colors hover:bg-accent hover:text-foreground"
        >
          <PanelRightClose size={15} />
        </button>
      </div>

      <div className="thin-scroll flex-1 overflow-y-auto p-3">
        <div className="grid grid-cols-2 gap-2">
          <MetricCard label="Total Requests" value={String(metrics.total)} />
          <MetricCard label="Blocked" value={String(metrics.blocked)} />
          <MetricCard label="Block Rate" value={metrics.blockRate} />
          <MetricCard label="Avg Grounding" value={metrics.avgGrounding} />
        </div>

        <div className="mt-5 mb-2 text-[10px] font-medium uppercase tracking-[0.13em] text-muted-foreground">
          Live Activity
        </div>
        <ul className="flex flex-col">
          {activity.length === 0 ? (
            <li className="px-1 py-2 text-[12px] text-muted-foreground">
              No requests yet
            </li>
          ) : (
            activity.slice(0, 5).map((a) => (
              <li
                key={a.id}
                className="flex items-center gap-2 border-b border-border/60 py-2 last:border-b-0"
              >
                <span
                  className="h-1.5 w-1.5 shrink-0 rounded-full"
                  style={{ backgroundColor: STATUS_COLOR[a.status] }}
                />
                <span className="min-w-0 flex-1 truncate text-[12px] text-foreground">
                  {a.query}
                </span>
                <span className="shrink-0 font-mono text-[10px] text-muted-foreground">
                  {a.time}
                </span>
              </li>
            ))
          )}
        </ul>
      </div>
    </aside>
  )
}
