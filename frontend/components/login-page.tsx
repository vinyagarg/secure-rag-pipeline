'use client'

import { useState } from 'react'
import { ShieldMark } from './shield-mark'
import type { Role } from '@/lib/types'

const DEMO_CREDENTIALS: Record<Role, string> = {
  user: 'user123',
  admin: 'admin123',
}

function LoginCard({
  role,
  onSignIn,
}: {
  role: Role
  onSignIn: (role: Role) => void
}) {
  const [password, setPassword] = useState('')
  const [error, setError] = useState(false)

  const title = role === 'admin' ? 'Continue as Admin' : 'Continue as User'
  const description =
    role === 'admin'
      ? 'Full access with the system monitoring panel.'
      : 'Ask questions grounded in the shared knowledge base.'

  function submit(e: React.FormEvent) {
    e.preventDefault()
    if (password === DEMO_CREDENTIALS[role] || password.trim() === '') {
      // allow empty for frictionless demo, but validate if typed
      if (password.trim() !== '' && password !== DEMO_CREDENTIALS[role]) {
        setError(true)
        return
      }
      onSignIn(role)
    } else {
      setError(true)
    }
  }

  return (
    <form
      onSubmit={submit}
      className="flex w-full flex-col rounded-lg border border-border bg-card p-6"
    >
      <h2 className="text-[15px] font-medium text-foreground">{title}</h2>
      <p className="mt-1 text-[13px] leading-relaxed text-muted-foreground">
        {description}
      </p>

      <label
        htmlFor={`pw-${role}`}
        className="mt-5 mb-2 text-[10px] font-medium uppercase tracking-[0.14em] text-muted-foreground"
      >
        Password
      </label>
      <input
        id={`pw-${role}`}
        type="password"
        value={password}
        onChange={(e) => {
          setPassword(e.target.value)
          setError(false)
        }}
        placeholder="••••••••"
        className="h-9 rounded-md border border-border bg-background px-3 text-[13px] text-foreground outline-none transition-colors placeholder:text-muted-foreground focus:border-border-strong"
      />
      {error && (
        <span className="mt-2 text-[12px] text-[color:var(--confidence-low)]">
          Incorrect password for this role.
        </span>
      )}

      <button
        type="submit"
        className="mt-4 h-9 rounded-md bg-primary text-[13px] font-medium text-primary-foreground transition-opacity hover:opacity-90"
      >
        Sign in
      </button>

      <p className="mt-3 text-[11px] leading-relaxed text-muted-foreground">
        Demo — password{' '}
        <span className="font-mono text-[color:var(--foreground)]/70">
          {DEMO_CREDENTIALS[role]}
        </span>{' '}
        or leave blank
      </p>
    </form>
  )
}

export function LoginPage({ onSignIn }: { onSignIn: (role: Role) => void }) {
  return (
    <main className="flex min-h-svh w-full flex-col items-center justify-center bg-background px-4 py-10">
      <div className="mb-8 flex flex-col items-center text-center">
        <div className="flex items-center gap-2">
          <ShieldMark size={20} />
          <span className="text-[19px] font-semibold tracking-tight text-foreground">
            RAGuard
          </span>
        </div>
        <p className="mt-3 text-[13px] text-muted-foreground">
          AI assistant grounded in source documents
        </p>
      </div>

      <div className="grid w-full max-w-[640px] grid-cols-1 gap-4 sm:grid-cols-2">
        <LoginCard role="user" onSignIn={onSignIn} />
        <LoginCard role="admin" onSignIn={onSignIn} />
      </div>

      <p className="mt-8 text-[11px] tracking-wide text-muted-foreground">
        Next.js · pgvector · text-embedding-3 · Reranker v2
      </p>
    </main>
  )
}
