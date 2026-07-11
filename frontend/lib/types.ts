export type Role = 'user' | 'admin'

export type Confidence = 'high' | 'medium' | 'low'

export interface Source {
  title: string
  url: string
  snippet: string
}

export interface ChatMessage {
  id: string
  role: 'user' | 'assistant'
  content: string
  /** true while the assistant response is still streaming */
  streaming?: boolean
  /** true while waiting for the first token (typing indicator) */
  pending?: boolean
  confidence?: Confidence
  sources?: Source[]
  blocked?: boolean
}

export interface UploadedDoc {
  id: string
  name: string
  size: number
  type: string
  /** extracted plain-text content used for retrieval; empty if not readable */
  content?: string
}

export interface ActivityItem {
  id: string
  query: string
  status: Confidence | 'blocked'
  time: string
}
