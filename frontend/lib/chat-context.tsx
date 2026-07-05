'use client'

import React, { createContext, useContext, useState } from 'react'

export type ConfidenceLevel = 'high' | 'medium' | 'low'

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  confidence?: ConfidenceLevel
  sources?: string[]
}

interface ChatContextType {
  messages: Message[]
  addMessage: (message: Message) => void
  clearMessages: () => void
}

const ChatContext = createContext<ChatContextType | undefined>(undefined)

export function ChatProvider({ children }: { children: React.ReactNode }) {
  const [messages, setMessages] = useState<Message[]>([])

  const addMessage = (message: Message) => {
    setMessages((prev) => [...prev, message])
  }

  const clearMessages = () => {
    setMessages([])
  }

  const value: ChatContextType = {
    messages,
    addMessage,
    clearMessages,
  }

  return <ChatContext.Provider value={value}>{children}</ChatContext.Provider>
}

export function useChat() {
  const context = useContext(ChatContext)
  if (!context) {
    throw new Error('useChat must be used within ChatProvider')
  }
  return context
}
