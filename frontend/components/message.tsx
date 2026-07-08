'use client'

import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
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

        {/* Markdown rendered answer */}
        <div className="text-[#e0e0e0] text-sm leading-relaxed prose prose-invert prose-sm max-w-none
          [&>p]:mb-3 [&>p]:leading-relaxed
          [&>ul]:mt-2 [&>ul]:mb-3 [&>ul]:pl-4 [&>ul>li]:mb-1 [&>ul>li]:text-[#c0c0c0]
          [&>ol]:mt-2 [&>ol]:mb-3 [&>ol]:pl-4 [&>ol>li]:mb-2 [&>ol>li]:text-[#c0c0c0]
          [&>h1]:text-[#e0e0e0] [&>h1]:font-semibold [&>h1]:text-base [&>h1]:mt-4 [&>h1]:mb-2
          [&>h2]:text-[#e0e0e0] [&>h2]:font-semibold [&>h2]:text-sm [&>h2]:mt-4 [&>h2]:mb-2
          [&>h3]:text-[#c0c0c0] [&>h3]:font-medium [&>h3]:text-sm [&>h3]:mt-3 [&>h3]:mb-1
          [&>strong]:text-[#ffffff] [&>strong]:font-semibold
          [&_strong]:text-[#ffffff] [&_strong]:font-semibold
          [&>code]:bg-[#1a1a1a] [&>code]:px-1.5 [&>code]:py-0.5 [&>code]:rounded [&>code]:text-[#a0a0a0] [&>code]:text-xs
          [&>pre]:bg-[#0d0d0d] [&>pre]:border [&>pre]:border-[#1a1a1a] [&>pre]:rounded-lg [&>pre]:p-4 [&>pre]:my-3 [&>pre]:overflow-x-auto
          [&>blockquote]:border-l-2 [&>blockquote]:border-[#2a2a2a] [&>blockquote]:pl-3 [&>blockquote]:text-[#888] [&>blockquote]:italic
          [&>hr]:border-[#1a1a1a] [&>hr]:my-4">
          <ReactMarkdown>{message.content}</ReactMarkdown>
        </div>

        {/* Confidence indicator */}
        {message.confidence && (
          <div className="flex items-center gap-2 mt-3 mb-2">
            <div className={`w-2 h-2 rounded-full flex-shrink-0 ${getConfidenceColor(message.confidence)}`} />
            <span className="text-[#555] text-xs">{getConfidenceLabel(message.confidence)}</span>
          </div>
        )}

        {/* Sources */}
        {message.sources && message.sources.length > 0 && (
          <div className="mt-2 text-xs">
            <button
              onClick={() => setExpandedSources(!expandedSources)}
              className="text-[#444] hover:text-[#888] flex items-center gap-1.5 transition-colors"
            >
              <span className="text-[10px]">{expandedSources ? '▼' : '▶'}</span>
              <span>Sources ({message.sources.length})</span>
            </button>

            {expandedSources && (
              <div className="mt-2 space-y-1.5 pl-3 border-l border-[#1a1a1a]">
                {message.sources.map((source, idx) => (
                  <div key={idx}>
                    {source.startsWith('http') ? (
                      
                        href={source}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-[#4F8BF9] hover:text-[#8AB4F8] text-xs leading-tight break-all transition-colors"
                      >
                        ↗ {source}
                      </a>
                    ) : (
                      <span className="text-[#555] text-xs">• {source}</span>
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
