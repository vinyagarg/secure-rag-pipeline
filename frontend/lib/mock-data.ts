import type { Confidence, Source } from './types'

export const SUGGESTED_QUESTIONS = [
  'What is retrieval augmented generation?',
  'How do guardrails protect AI systems?',
  'Compare fine-tuning vs RAG',
  'What are chunking strategies for RAG?',
  'How does prompt injection work?',
  'How does LLM evaluation work?',
]

export const INITIAL_HISTORY: string[] = []

export const TECH_STACK = 'FastAPI · ChromaDB · Llama 3.3 · Jina AI'

export const DEFAULT_DOCS: never[] = []

export const CONFIDENCE_META: Record<Confidence, { label: string; varName: string }> = {
  high:   { label: 'High confidence',   varName: 'var(--confidence-high)'   },
  medium: { label: 'Medium confidence', varName: 'var(--confidence-medium)' },
  low:    { label: 'Low confidence',    varName: 'var(--confidence-low)'    },
}