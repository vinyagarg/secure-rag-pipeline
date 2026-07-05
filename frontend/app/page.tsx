'use client'

import { AuthProvider, useAuth } from '@/lib/auth-context'
import { ChatProvider } from '@/lib/chat-context'
import { LoginPage } from '@/components/login-page'
import { ChatInterface } from '@/components/chat-interface'

function PageContent() {
  const { isAuthenticated } = useAuth()

  return isAuthenticated ? <ChatInterface /> : <LoginPage />
}

export default function Page() {
  return (
    <AuthProvider>
      <ChatProvider>
        <PageContent />
      </ChatProvider>
    </AuthProvider>
  )
}
