'use client'

import { useState } from 'react'
import { Message, ConfidenceLevel } from '@/lib/chat-context'

interface MessageComponentProps {
  message: Message
}

function getConfidenceColor(level: ConfidenceLevel) {
  switch (level) {
    case 'high':   return 'bg-[#22c55e]'
    case 'medium': return 'bg-[#f59e0b]'
    case 'low':    return 'bg-[#ef4444]'
  }
}

function getConfidenceLabel(level: ConfidenceLevel) {
  switch (level) {
    case 'high':   return 'High confidence'
    case 'medium': return 'Medium confidence'
    case 'low':    return 'Low confidence'
  }
}

function renderInline(line: string): React.ReactNode[] {
  const parts = line.split(/(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/)
  return parts.map((part, idx) => {
    if (part.startsWith('**') && part.endsWith('**')) {
      return <strong key={idx} className="text-white font-semibold">{part.slice(2, -2)}</strong>
    }
    if (part.startsWith('*') && part.endsWith('*') && part.length > 2 && !part.startsWith('**')) {
      return <em key={idx} className="italic text-[#c0c0c0]">{part.slice(1, -1)}</em>
    }
    if (part.startsWith('`') && part.endsWith('`')) {
      return <code key={idx} className="bg-[#1a1a1a] px-1.5 py-0.5 rounded text-[#a0a0a0] text-xs font-mono">{part.slice(1, -1)}</code>
    }
    return <span key={idx}>{part}</span>
  })
}

function renderMarkdown(text: string): React.ReactNode[] {
  const lines = text.split('\n')
  const elements: React.ReactNode[] = []
  let i = 0

  while (i < lines.length) {
    const line = lines[i]

    if (line.trim() === '') {
      i++
      continue
    }

    if (line.startsWith('### ')) {
      elements.push(<h3 key={i} className="text-[#e0e0e0] font-semibold text-sm mt-4 mb-1">{renderInline(line.slice(4))}</h3>)
      i++
      continue
    }

    if (line.startsWith('## ')) {
      elements.push(<h2 key={i} className="text-[#e0e0e0] font-semibold text-sm mt-4 mb-2">{renderInline(line.slice(3))}</h2>)
      i++
      continue
    }

    if (line.startsWith('# ')) {
      elements.push(<h1 key={i} className="text-[#e0e0e0] font-semibold text-base mt-4 mb-2">{renderInline(line.slice(2))}</h1>)
      i++
      continue
    }

    if (line.trim() === '---' || line.trim() === '***') {
      elements.push(<hr key={i} className="border-[#1a1a1a] my-3" />)
      i++
      continue
    }

    if (/^\d+\.\s/.test(line)) {
      const listItems: React.ReactNode[] = []
      while (i < lines.length && /^\d+\.\s/.test(lines[i])) {
        const content = lines[i].replace(/^\d+\.\s/, '')
        listItems.push(
          <li key={i} className="text-[#c0c0c0] mb-2 leading-relaxed">
            {renderInline(content)}
          </li>
        )
        i++
      }
      elements.push(
        <ol key={'ol' + i} className="list-decimal pl-5 my-3 space-y-1">
          {listItems}
        </ol>
      )
      continue
    }

    if (/^[\s]*[-*]\s/.test(line)) {
      const listItems: React.ReactNode[] = []
      while (i < lines.length && /^[\s]*[-*]\s/.test(lines[i])) {
        const content = lines[i].replace(/^[\s]*[-*]\s/, '')
        listItems.push(
          <li key={i} className="text-[#c0c0c0] mb-1.5 leading-relaxed">
            {renderInline(content)}
          </li>
        )
        i++
      }
      elements.push(
        <ul key={'ul' + i} className="list-disc pl-5 my-2 space-y-0.5">
          {listItems}
        </ul>
      )
      continue
    }

    elements.push(
      <p key={i} className="text-[#c0c0c0] leading-relaxed mb-2">
        {renderInline(line)}
      </p>
    )
    i++
  }

  return elements
}

export function MessageComponent({ message }: MessageComponentProps) {
  const [expandedSources, setExpandedSources] = useState(false)

  if (message.role === 'user') {
    return (
      <div className="flex justify-end mb-4">
        <div className="bg-[#141414] rounded-lg px-4 py-3 max-w-md border border-[#1a1a1a]">
          <p className="text-[#e0e0e0] text-sm leading-relaxed">{message.content}</p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex gap-3 mb-6 max-w-2xl">
      <div className="text-lg mt-1 flex-shrink-0">🛡️</div>
      <div className="flex-1 min-w-0">

        <div className="text-sm">
          {renderMarkdown(message.content)}
        </div>

        {message.confidence && (
          <div className="flex items-center gap-2 mt-3 mb-2">
            <div className={`w-2 h-2 rounded-full flex-shrink-0 ${getConfidenceColor(message.confidence)}`} />
            <span className="text-[#555] text-xs">{getConfidenceLabel(message.confidence)}</span>
          </div>
        )}

        {message.sources && message.sources.length > 0 && (
          <div className="mt-2 text-xs">
            <button
              onClick={() => setExpandedSources(!expandedSources)}
              className="text-[#444] hover:text-[#888] flex items-center gap-1.5 transition-colors"
            >
              <span className="text-[10px]">{expandedSources ? '▼' : '▶'}</span>
              <span>{'Sources (' + message.sources.length + ')'}</span>
            </button>
            {expandedSources && (
              <div className="mt-2 space-y-1.5 pl-3 border-l border-[#1a1a1a]">
                {message.sources.map((source, idx) => (
                  <div key={idx}>
                    {source.startsWith('http') ? (
                      <a href={source} target="_blank" rel="noopener noreferrer" className="text-[#4F8BF9] hover:text-[#8AB4F8] text-xs break-all transition-colors">
                        {'↗ ' + source}
                      </a>
                    ) : (
                      <span className="text-[#555] text-xs">{'• ' + source}</span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}