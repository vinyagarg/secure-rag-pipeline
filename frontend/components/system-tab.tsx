'use client'

import { useEffect, useState } from 'react'

interface Stats {
  total_requests: number
  total_blocked: number
  block_rate: number
  avg_grounding_score: number | null
}

interface LogRow {
  time: string
  query: string
  blocked: string
  grounding: string
  latency: string
}

export function SystemTab() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [logs, setLogs] = useState<LogRow[]>([])

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://raguard-api.onrender.com'
    fetch(`${apiUrl}/stats`).then(r => r.json()).then(setStats).catch(() => {})
    fetch(`${apiUrl}/logs`).then(r => r.json()).then(setLogs).catch(() => {})
  }, [])

  const metrics = [
    { label: 'Total Requests', value: stats?.total_requests ?? '—' },
    { label: 'Blocked',        value: stats?.total_blocked ?? '—' },
    { label: 'Block Rate',     value: stats ? `${(stats.block_rate * 100).toFixed(1)}%` : '—' },
    { label: 'Avg Grounding',  value: stats?.avg_grounding_score ? `${stats.avg_grounding_score}/5` : '—' },
  ]

  return (
    <div className="h-full overflow-y-auto p-6">
      <div className="max-w-6xl mx-auto">
        <p className="text-[#333] text-xs uppercase tracking-wider mb-6">System Observability</p>

        <div className="grid grid-cols-4 gap-4 mb-8">
          {metrics.map((m, i) => (
            <div key={i} className="bg-[#0d0d0d] border border-[#1a1a1a] rounded-lg p-4">
              <p className="text-[#555] text-xs uppercase tracking-wider mb-2">{m.label}</p>
              <p className="text-[#e0e0e0] text-2xl font-semibold">{String(m.value)}</p>
            </div>
          ))}
        </div>

        <p className="text-[#333] text-xs uppercase tracking-wider mb-4">Recent Requests</p>
        <div className="bg-[#0d0d0d] border border-[#1a1a1a] rounded-lg overflow-hidden">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-[#1a1a1a]">
                {['Time','Query','Status','Grounding','Latency'].map(h => (
                  <th key={h} className="px-4 py-3 text-left text-[#555] text-xs uppercase tracking-wider">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {logs.length === 0 ? (
                <tr><td colSpan={5} className="px-4 py-8 text-[#333] text-xs text-center">No requests logged yet</td></tr>
              ) : logs.map((log, i) => (
                <tr key={i} className="border-b border-[#1a1a1a] last:border-b-0 hover:bg-[#141414] transition-colors">
                  <td className="px-4 py-3 text-[#555] text-xs font-mono">{log.time}</td>
                  <td className="px-4 py-3 text-[#e0e0e0] text-xs max-w-xs truncate">{log.query}</td>
                  <td className="px-4 py-3 text-xs">
                    <span className={log.blocked === 'blocked' ? 'text-[#ef4444]' : 'text-[#22c55e]'}>
                      ● {log.blocked === 'blocked' ? 'Blocked' : 'Clean'}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-[#555] text-xs">{log.grounding}</td>
                  <td className="px-4 py-3 text-[#555] text-xs font-mono">{log.latency}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
