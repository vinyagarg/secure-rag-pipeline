'use client'

import { useState } from 'react'
import { useAuth } from '@/lib/auth-context'

export function LoginPage() {
  const { login } = useAuth()
  const [userPassword, setUserPassword] = useState('')
  const [adminPassword, setAdminPassword] = useState('')
  const [userError, setUserError] = useState('')
  const [adminError, setAdminError] = useState('')

  const handleUserLogin = (e: React.FormEvent) => {
    e.preventDefault()
    setUserError('')
    
    if (userPassword === 'user123') {
      login('user')
    } else {
      setUserError('Invalid password')
      setUserPassword('')
    }
  }

  const handleAdminLogin = (e: React.FormEvent) => {
    e.preventDefault()
    setAdminError('')
    
    if (adminPassword === 'admin123') {
      login('admin')
    } else {
      setAdminError('Invalid password')
      setAdminPassword('')
    }
  }

  return (
    <div className="min-h-screen bg-[#080808] flex items-center justify-center px-4">
      <div className="w-full max-w-2xl">
        {/* Logo and Title */}
        <div className="text-center mb-12">
          <div className="text-5xl mb-3 flex items-center justify-center gap-2">
            <span>🛡️</span>
            <h1 className="text-3xl font-semibold tracking-tight text-[#e0e0e0]">RAGuard</h1>
          </div>
          <p className="text-[#555] text-sm">Premium AI Chat with Role-Based Access</p>
        </div>

        {/* Two Login Cards */}
        <div className="grid md:grid-cols-2 gap-6">
          {/* User Login */}
          <div className="bg-[#0d0d0d] border border-[#1a1a1a] rounded-lg p-8">
            <h2 className="text-[#e0e0e0] font-medium mb-6">Sign in as User</h2>
            
            <form onSubmit={handleUserLogin} className="space-y-4">
              <div>
                <label className="text-[#555] text-xs uppercase tracking-wider block mb-2">
                  Password
                </label>
                <input
                  type="password"
                  value={userPassword}
                  onChange={(e) => setUserPassword(e.target.value)}
                  placeholder="Enter password"
                  className="w-full px-3 py-2 bg-[#141414] border border-[#1a1a1a] rounded text-[#e0e0e0] text-sm focus:outline-none focus:border-[#2a2a2a]"
                />
              </div>
              
              {userError && (
                <p className="text-[#ef4444] text-xs">{userError}</p>
              )}
              
              <button
                type="submit"
                className="w-full px-4 py-2 bg-[#141414] hover:bg-[#1a1a1a] border border-[#1a1a1a] rounded text-[#e0e0e0] text-sm font-medium transition-colors"
              >
                Sign in
              </button>
            </form>
            
            <p className="text-[#555] text-xs mt-4">Demo: password is <span className="text-[#e0e0e0] font-mono">user123</span></p>
          </div>

          {/* Admin Login */}
          <div className="bg-[#0d0d0d] border border-[#1a1a1a] rounded-lg p-8">
            <h2 className="text-[#e0e0e0] font-medium mb-6">Sign in as Admin</h2>
            
            <form onSubmit={handleAdminLogin} className="space-y-4">
              <div>
                <label className="text-[#555] text-xs uppercase tracking-wider block mb-2">
                  Password
                </label>
                <input
                  type="password"
                  value={adminPassword}
                  onChange={(e) => setAdminPassword(e.target.value)}
                  placeholder="Enter password"
                  className="w-full px-3 py-2 bg-[#141414] border border-[#1a1a1a] rounded text-[#e0e0e0] text-sm focus:outline-none focus:border-[#2a2a2a]"
                />
              </div>
              
              {adminError && (
                <p className="text-[#ef4444] text-xs">{adminError}</p>
              )}
              
              <button
                type="submit"
                className="w-full px-4 py-2 bg-[#141414] hover:bg-[#1a1a1a] border border-[#1a1a1a] rounded text-[#e0e0e0] text-sm font-medium transition-colors"
              >
                Sign in
              </button>
            </form>
            
            <p className="text-[#555] text-xs mt-4">Demo: password is <span className="text-[#e0e0e0] font-mono">admin123</span></p>
          </div>
        </div>
      </div>
    </div>
  )
}
