'use client'

import React, { createContext, useContext, useState } from 'react'

type UserRole = 'user' | 'admin'

interface AuthContextType {
  role: UserRole | null
  isAuthenticated: boolean
  login: (role: UserRole) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [role, setRole] = useState<UserRole | null>(null)

  const login = (userRole: UserRole) => {
    setRole(userRole)
  }

  const logout = () => {
    setRole(null)
  }

  const value: AuthContextType = {
    role,
    isAuthenticated: role !== null,
    login,
    logout,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider')
  }
  return context
}
