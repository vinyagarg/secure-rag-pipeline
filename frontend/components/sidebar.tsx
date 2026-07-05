'use client'

import { useAuth } from '@/lib/auth-context'
import { useChat } from '@/lib/chat-context'

interface SidebarProps {
  onSuggestedQuestion: (question: string) => void
}

const suggestedQuestions = [
  'What is RAG and how does it work?',
  'Fine-tuning vs RAG — which to use?',
  'How do guardrails protect AI systems?',
  'What are chunking strategies for RAG?',
  'How does LLM evaluation work?',
  'What is prompt injection?',
]

export function Sidebar({ onSuggestedQuestion }: SidebarProps) {
  const { role, logout } = useAuth()
  const { clearMessages } = useChat()

  return (
    <div className="w-60 bg-[#0d0d0d] border-r border-[#1a1a1a] flex flex-col h-screen flex-shrink-0">
      <div className="p-4 border-b border-[#1a1a1a]">
        <div className="flex items-center gap-2 mb-1">
          <span className="text-xl">🛡️</span>
          <h1 className="text-[#e0e0e0] font-semibold text-sm">RAGuard</h1>
          {role === 'admin' && (
            <span className="ml-auto bg-[#141414] border border-[#1a1a1a] text-[#888] text-xs px-2 py-0.5 rounded">
              Admin
            </span>
          )}
        </div>
        <p className="text-[#666] text-xs">AI assistant grounded in source documents</p>
      </div>

      <div className="flex-1 overflow-y-auto p-3">
        <p className="text-[#555] text-xs uppercase tracking-wider font-medium px-1 mb-3">
          Suggested
        </p>
        {suggestedQuestions.map((q, i) => (
          <button
            key={i}
            onClick={() => onSuggestedQuestion(q)}
            className="w-full text-left px-3 py-2 rounded bg-transparent hover:bg-[#141414] border border-transparent hover:border-[#1a1a1a] text-[#999] hover:text-[#e0e0e0] text-xs leading-tight transition-all mb-1"
          >
            {q}
          </button>
        ))}
      </div>

      <div className="p-3 border-t border-[#1a1a1a] space-y-2">
        <button
          onClick={() => clearMessages()}
          className="w-full px-3 py-2 rounded bg-transparent hover:bg-[#141414] border border-[#1a1a1a] text-[#999] hover:text-[#e0e0e0] text-xs font-medium transition-all"
        >
          Clear conversation
        </button>
        <button
          onClick={() => { clearMessages(); logout() }}
          className="w-full px-3 py-2 rounded bg-transparent hover:bg-[#141414] border border-[#1a1a1a] text-[#999] hover:text-[#e0e0e0] text-xs font-medium transition-all"
        >
          Sign out
        </button>
        <p className="text-[#444] text-xs text-center pt-1">
          FastAPI · ChromaDB · Llama 3.3
        </p>
      </div>
    </div>
  )
}