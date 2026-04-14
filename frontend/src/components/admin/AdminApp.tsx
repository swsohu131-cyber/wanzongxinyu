import { useState, useEffect } from 'react'
import AdminLogin from './AdminLogin'
import Dashboard from './Dashboard'
import UserList from './UserList'
import KnowledgeBase from './KnowledgeBase'

type Tab = 'dashboard' | 'users' | 'knowledge'

export default function AdminApp() {
  const [token, setToken] = useState<string | null>(null)
  const [currentTab, setCurrentTab] = useState<Tab>('dashboard')

  useEffect(() => {
    // 检查本地存储的管理员token
    const stored = localStorage.getItem('wanzongxinyu-admin-token')
    if (stored) {
      setToken(stored)
    }
  }, [])

  const handleLogin = (newToken: string) => {
    setToken(newToken)
    localStorage.setItem('wanzongxinyu-admin-token', newToken)
  }

  const handleLogout = () => {
    setToken(null)
    localStorage.removeItem('wanzongxinyu-admin-token')
  }

  if (!token) {
    return <AdminLogin onLogin={handleLogin} />
  }

  return (
    <div className="min-h-screen bg-primary-100">
      {/* 顶部导航 */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-3 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <h1 className="text-xl font-medium text-primary-800">万宗心悟 · 管理后台</h1>
            <nav className="flex gap-2">
              <button
                onClick={() => setCurrentTab('dashboard')}
                className={`px-4 py-2 rounded-xl text-sm font-medium transition ${
                  currentTab === 'dashboard'
                    ? 'bg-accent-green text-white'
                    : 'text-primary-600 hover:bg-primary-100'
                }`}
              >
                数据概览
              </button>
              <button
                onClick={() => setCurrentTab('users')}
                className={`px-4 py-2 rounded-xl text-sm font-medium transition ${
                  currentTab === 'users'
                    ? 'bg-accent-green text-white'
                    : 'text-primary-600 hover:bg-primary-100'
                }`}
              >
                用户管理
              </button>
              <button
                onClick={() => setCurrentTab('knowledge')}
                className={`px-4 py-2 rounded-xl text-sm font-medium transition ${
                  currentTab === 'knowledge'
                    ? 'bg-accent-green text-white'
                    : 'text-primary-600 hover:bg-primary-100'
                }`}
              >
                知识库
              </button>
            </nav>
          </div>

          <button
            onClick={handleLogout}
            className="text-sm text-primary-400 hover:text-primary-600 transition"
          >
            退出登录
          </button>
        </div>
      </header>

      {/* 主内容 */}
      <main className="max-w-7xl mx-auto px-4 py-6">
        {currentTab === 'dashboard' && <Dashboard />}
        {currentTab === 'users' && <UserList />}
        {currentTab === 'knowledge' && <KnowledgeBase />}
      </main>
    </div>
  )
}
