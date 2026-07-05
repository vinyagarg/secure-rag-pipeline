'use client'

import { useEffect, useRef, useState } from 'react'
import { useAuth } from '@/lib/auth-context'
import { useChat } from '@/lib/chat-context'
import { Sidebar } from './sidebar'
import { MessageComponent } from './message'
import { SystemTab } from './system-tab'

export function ChatInterface() {
  const { role } = useAuth()
  const { messages, addMessage } = useChat()
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [activeTab, setActiveTab] = useState<'chat' | 'system'>('chat')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSuggestedQuestion = (question: string) => {
    setInput(question)
  }

  const handleSendMessage = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return

    const question = input.trim()
    setInput('')
    setLoading(true)

    addMessage({
      id: Date.now().toString(),
      role: 'user',
      content: question,
    })

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://raguard-api.onrender.com'
      const res = await fetch(`${apiUrl}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question })
      })
      const data = await res.json()

      let confidence: 'high' | 'medium' | 'low' = 'medium'
      if (data.distances && data.distances.length > 0) {
        const avg = data.distances.reduce((a: number, b: number) => a + b, 0) / data.distances.length
        if (avg < 0.6) confidence = 'high'
        else if (avg < 1.0) confidence = 'medium'
        else confidence = 'low'
      }
      if (data.blocked) confidence = 'low'

      addMessage({
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.answer,
        confidence,
        sources: data.sources || [],
      })
    } catch {
      addMessage({
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Connection error — the API may be sleeping. Try again in 30 seconds.',
        confidence: 'low',
        sources: [],
      })
    } finally {
      setLoading(false)
    }
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInput(e.currentTarget.value)
    e.currentTarget.style.height = 'auto'
    e.currentTarget.style.height = Math.min(e.currentTarget.scrollHeight, 120) + 'px'
  }

  const isComposing = useRef(false)

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.nativeEvent.isComposing) { isComposing.current = true; return }
    if (e.key === 'Enter' && !e.shiftKey && !isComposing.current) {
      e.preventDefault()
      handleSendMessage(e as any)
    }
  }

  const handleCompositionEnd = () => { isComposing.current = false }

  return (
    <div className="flex h-screen bg-[#080808]">
      <Sidebar onSuggestedQuestion={handleSuggestedQuestion} />

      <div className="flex-1 flex flex-col min-w-0">
        {/* Tab navigation */}
        <div className="border-b border-[#1a1a1a] flex items-center flex-shrink-0">
          <button
            onClick={() => setActiveTab('chat')}
            className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
              activeTab === 'chat'
                ? 'border-[#e0e0e0] text-[#e0e0e0]'
                : 'border-transparent text-[#555] hover:text-[#888]'
            }`}
          >
            Chat
          </button>
          {role === 'admin' && (
            <button
              onClick={() => setActiveTab('system')}
              className={`px-4 py-3 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'system'
                  ? 'border-[#e0e0e0] text-[#e0e0e0]'
                  : 'border-transparent text-[#555] hover:text-[#888]'
              }`}
            >
              System
            </button>
          )}
        </div>

        {/* Content */}
        <div className="flex-1 overflow-hidden">
          {activeTab === 'chat' ? (
            <div className="h-full flex flex-col">
              {/* Messages */}
              <div className="flex-1 overflow-y-auto p-6">
                <div className="max-w-3xl mx-auto">
                  {messages.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-64">
                      <div className="text-4xl mb-3">🛡️</div>
                      <p className="text-[#555] text-sm text-center">
                        Smart enough to answer.<br />Smart enough to know when not to.
                      </p>
                    </div>
                  ) : (
                    <>
                      {messages.map((msg) => (
                        <MessageComponent key={msg.id} message={msg} />
                      ))}
                      {loading && (
                        <div className="flex gap-3 mb-4">
                          <div className="text-lg mt-1">🛡️</div>
                          <div className="flex items-center gap-1 pt-2">
                            <span className="w-1.5 h-1.5 bg-[#333] rounded-full animate-bounce" style={{animationDelay:'0ms'}}/>
                            <span className="w-1.5 h-1.5 bg-[#333] rounded-full animate-bounce" style={{animationDelay:'150ms'}}/>
                            <span className="w-1.5 h-1.5 bg-[#333] rounded-full animate-bounce" style={{animationDelay:'300ms'}}/>
                          </div>
                        </div>
                      )}
                      <div ref={messagesEndRef} />
                    </>
                  )}
                </div>
              </div>

              {/* Fixed input */}
              <div className="border-t border-[#1a1a1a] p-4 bg-[#080808] flex-shrink-0">
                <form onSubmit={handleSendMessage} className="max-w-3xl mx-auto">
                  <div className="flex gap-3">
                    <textarea
                      value={input}
                      onChange={handleInputChange}
                      onKeyDown={handleKeyDown}
                      onCompositionEnd={handleCompositionEnd}
                      placeholder="Ask anything about RAG, LLMs, or AI engineering..."
                      rows={1}
                      disabled={loading}
                      className="flex-1 bg-[#141414] border border-[#1a1a1a] rounded px-4 py-3 text-[#e0e0e0] text-sm placeholder-[#555] resize-none focus:outline-none focus:border-[#2a2a2a] max-h-32 disabled:opacity-50"
                    />
                    <button
                      type="submit"
                      disabled={!input.trim() || loading}
                      className="px-6 py-3 bg-[#141414] hover:bg-[#1a1a1a] disabled:opacity-50 border border-[#1a1a1a] rounded text-[#e0e0e0] text-sm font-medium transition-colors"
                    >
                      {loading ? '...' : 'Send'}
                    </button>
                  </div>
                </form>
              </div>
            </div>
          ) : (
            <SystemTab />
          )}
        </div>
      </div>
    </div>
  )
}
