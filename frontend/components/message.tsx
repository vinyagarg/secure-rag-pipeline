'use client'

import { useState } from 'react'
import { Message, ConfidenceLevel } from '@/lib/chat-context'

interface MessageComponentProps {
  message: Message
}

function getConfidenceColor(level: ConfidenceLevel) {
  switch (level) {
    case 'high':
      return 'bg-[#22c55e]'
    case 'medium':
      return 'bg-[#f59e0b]'
    case 'low':
      return 'bg-[#ef4444]'
  }
}

function getConfidenceLabel(level: ConfidenceLevel) {
  switch (level) {
    case 'high':
      return 'High confidence'
    case 'medium':
      return 'Medium confidence'
    case 'low':
      return 'Low confidence'
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

  // Assistant message
  return (
    <div className="flex gap-3 mb-4 max-w-2xl">
      <div className="text-lg mt-1">🛡️</div>
      <div className="flex-1">
        <div className="text-[#e0e0e0] text-sm leading-relaxed mb-2">
          {message.content}
        </div>

        {/* Confidence indicator */}
        {message.confidence && (
          <div className="flex items-center gap-2 mb-3">
            <div className={`w-2 h-2 rounded-full ${getConfidenceColor(message.confidence)}`} />
            <span className="text-[#555] text-xs">
              {getConfidenceLabel(message.confidence)}
            </span>
          </div>
        )}

        {/* Sources section */}
        {message.sources && message.sources.length > 0 && (
          <div className="mt-3 text-xs">
            <button
              onClick={() => setExpandedSources(!expandedSources)}
              className="text-[#555] hover:text-[#888] flex items-center gap-1 transition-colors"
            >
              <span>{expandedSources ? '▼' : '▶'}</span>
              Sources ({message.sources.length})
            </button>
            
            {expandedSources && (
              <div className="mt-2 space-y-1">
                {message.sources.map((source, idx) => (
                  <div
                    key={idx}
                    className="text-[#555] pl-4 text-xs leading-tight"
                  >
                    • {source}
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
