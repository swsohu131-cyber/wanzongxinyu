import { useState, useEffect } from 'react'
import { useAuthStore } from './stores/auth'
import Login from './components/Login'
import Chat from './components/Chat'
import AdminApp from './components/admin/AdminApp'

function App() {
  const [route, setRoute] = useState<'user' | 'admin'>('user')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // 根据路径判断是用户端还是管理端
    const path = window.location.pathname
    if (path.startsWith('/admin')) {
      setRoute('admin')
    }

    // 检查设备免密登录（仅用户端）
    if (route === 'user') {
      const init = async () => {
        const { checkDeviceLogin } = useAuthStore.getState()
        await checkDeviceLogin()
        setLoading(false)
      }
      init()
    } else {
      setLoading(false)
    }
  }, [route])

  if (loading) {
    return (
      <div className="min-h-screen bg-primary-100 flex items-center justify-center">
        <div className="text-primary-700 text-lg">加载中...</div>
      </div>
    )
  }

  // 管理端
  if (route === 'admin') {
    return <AdminApp />
  }

  // 用户端
  const { token } = useAuthStore()
  return (
    <div className="min-h-screen bg-primary-100">
      {token ? <Chat /> : <Login />}
    </div>
  )
}

export default App
