import { useState, useEffect } from 'react'
import { api } from '../../api/adminClient'

interface User {
  id: string
  nickname: string
  phone?: string
  email?: string
  created_at: string
  last_login_at?: string
  status: string
}

interface UserListResponse {
  users: User[]
  total: number
  page: number
  page_size: number
}

export default function UserList() {
  const [users, setUsers] = useState<User[]>([])
  const [loading, setLoading] = useState(true)
  const [keyword, setKeyword] = useState('')
  const [page, setPage] = useState(1)
  const [total, setTotal] = useState(0)
  const [selectedUser, setSelectedUser] = useState<User | null>(null)
  const pageSize = 20

  useEffect(() => {
    fetchUsers()
  }, [page, keyword])

  const fetchUsers = async () => {
    setLoading(true)
    try {
      const response = await api.get('/admin-api/users', {
        params: { page, page_size: pageSize, keyword: keyword || undefined }
      })
      const data: UserListResponse = response.data
      setUsers(data.users)
      setTotal(data.total)
    } catch (error) {
      console.error('获取用户列表失败:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    setPage(1)
    fetchUsers()
  }

  const handleBan = async (userId: string) => {
    if (!confirm('确定要封禁该用户吗？')) return
    try {
      await api.post(`/admin-api/users/${userId}/ban`)
      fetchUsers()
    } catch (error) {
      console.error('封禁用户失败:', error)
    }
  }

  const handleUnban = async (userId: string) => {
    try {
      await api.post(`/admin-api/users/${userId}/unban`)
      fetchUsers()
    } catch (error) {
      console.error('解封用户失败:', error)
    }
  }

  const totalPages = Math.ceil(total / pageSize)

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-medium text-primary-800">用户管理</h2>

        {/* 搜索框 */}
        <form onSubmit={handleSearch} className="flex gap-2">
          <input
            type="text"
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            placeholder="搜索用户昵称/手机/邮箱..."
            className="px-4 py-2 rounded-xl border border-primary-200 focus:border-accent-green focus:ring-2 focus:ring-accent-green/20 outline-none"
          />
          <button
            type="submit"
            className="px-4 py-2 bg-accent-green text-white rounded-xl hover:bg-accent-green/90 transition"
          >
            搜索
          </button>
        </form>
      </div>

      {/* 用户列表 */}
      <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
        <table className="w-full">
          <thead className="bg-primary-50">
            <tr>
              <th className="px-6 py-3 text-left text-sm font-medium text-primary-600">用户</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-primary-600">联系方式</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-primary-600">注册时间</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-primary-600">最后登录</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-primary-600">状态</th>
              <th className="px-6 py-3 text-left text-sm font-medium text-primary-600">操作</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-primary-100">
            {loading ? (
              <tr>
                <td colSpan={6} className="px-6 py-12 text-center text-primary-500">
                  加载中...
                </td>
              </tr>
            ) : users.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-6 py-12 text-center text-primary-400">
                  暂无用户
                </td>
              </tr>
            ) : (
              users.map((user) => (
                <tr key={user.id} className="hover:bg-primary-50/50">
                  <td className="px-6 py-4">
                    <div className="font-medium text-primary-800">{user.nickname}</div>
                    <div className="text-sm text-primary-400">{user.id.slice(0, 8)}...</div>
                  </td>
                  <td className="px-6 py-4 text-primary-600">
                    {user.phone || user.email || '-'}
                  </td>
                  <td className="px-6 py-4 text-primary-600">
                    {new Date(user.created_at).toLocaleDateString('zh-CN')}
                  </td>
                  <td className="px-6 py-4 text-primary-600">
                    {user.last_login_at
                      ? new Date(user.last_login_at).toLocaleDateString('zh-CN')
                      : '-'}
                  </td>
                  <td className="px-6 py-4">
                    <span
                      className={`inline-flex px-2 py-1 text-xs font-medium rounded-full ${
                        user.status === 'active'
                          ? 'bg-accent-green/10 text-accent-green'
                          : 'bg-red-100 text-red-600'
                      }`}
                    >
                      {user.status === 'active' ? '正常' : '已封禁'}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex gap-2">
                      <button
                        onClick={() => setSelectedUser(user)}
                        className="px-3 py-1 text-sm bg-primary-100 text-primary-700 rounded-lg hover:bg-primary-200 transition"
                      >
                        查看详情
                      </button>
                      {user.status === 'active' ? (
                        <button
                          onClick={() => handleBan(user.id)}
                          className="px-3 py-1 text-sm bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition"
                        >
                          封禁
                        </button>
                      ) : (
                        <button
                          onClick={() => handleUnban(user.id)}
                          className="px-3 py-1 text-sm bg-accent-green/10 text-accent-green rounded-lg hover:bg-accent-green/20 transition"
                        >
                          解封
                        </button>
                      )}
                    </div>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* 分页 */}
      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-2">
          <button
            onClick={() => setPage(Math.max(1, page - 1))}
            disabled={page === 1}
            className="px-3 py-1 rounded-lg bg-primary-100 text-primary-700 disabled:opacity-50 hover:bg-primary-200 transition"
          >
            上一页
          </button>
          <span className="text-primary-600">
            第 {page} / {totalPages} 页，共 {total} 条
          </span>
          <button
            onClick={() => setPage(Math.min(totalPages, page + 1))}
            disabled={page === totalPages}
            className="px-3 py-1 rounded-lg bg-primary-100 text-primary-700 disabled:opacity-50 hover:bg-primary-200 transition"
          >
            下一页
          </button>
        </div>
      )}

      {/* 用户详情弹窗 */}
      {selectedUser && (
        <UserDetailModal user={selectedUser} onClose={() => setSelectedUser(null)} />
      )}
    </div>
  )
}

// 用户详情弹窗组件
function UserDetailModal({ user, onClose }: { user: User; onClose: () => void }) {
  const [detail, setDetail] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchUserDetail()
  }, [user.id])

  const fetchUserDetail = async () => {
    try {
      const response = await api.get(`/admin-api/users/${user.id}`)
      setDetail(response.data)
    } catch (error) {
      console.error('获取用户详情失败:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-2xl w-full max-w-4xl max-h-[80vh] overflow-hidden">
        <div className="px-6 py-4 border-b border-primary-100 flex items-center justify-between">
          <h3 className="text-lg font-medium text-primary-800">用户详情</h3>
          <button
            onClick={onClose}
            className="text-primary-400 hover:text-primary-600 transition"
          >
            ✕
          </button>
        </div>

        <div className="p-6 overflow-y-auto max-h-[calc(80vh-60px)]">
          {loading ? (
            <div className="text-center py-12 text-primary-500">加载中...</div>
          ) : detail ? (
            <div className="space-y-6">
              {/* 基本信息 */}
              <div className="bg-primary-50 rounded-xl p-4">
                <h4 className="text-sm font-medium text-primary-600 mb-3">基本信息</h4>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <div className="text-xs text-primary-400">昵称</div>
                    <div className="text-primary-800">{detail.user.nickname}</div>
                  </div>
                  <div>
                    <div className="text-xs text-primary-400">手机号</div>
                    <div className="text-primary-800">{detail.user.phone || '-'}</div>
                  </div>
                  <div>
                    <div className="text-xs text-primary-400">邮箱</div>
                    <div className="text-primary-800">{detail.user.email || '-'}</div>
                  </div>
                  <div>
                    <div className="text-xs text-primary-400">状态</div>
                    <div className="text-primary-800">
                      {detail.user.status === 'active' ? '正常' : '已封禁'}
                    </div>
                  </div>
                </div>
              </div>

              {/* 用户画像 */}
              {detail.profile && (
                <div className="bg-primary-50 rounded-xl p-4">
                  <h4 className="text-sm font-medium text-primary-600 mb-3">用户画像</h4>
                  <div className="space-y-3">
                    <div>
                      <div className="text-xs text-primary-400">文化背景</div>
                      <pre className="text-sm text-primary-700 mt-1">
                        {JSON.stringify(detail.profile.cultural_background, null, 2)}
                      </pre>
                    </div>
                    <div>
                      <div className="text-xs text-primary-400">知识偏好</div>
                      <pre className="text-sm text-primary-700 mt-1">
                        {JSON.stringify(detail.profile.knowledge_weights, null, 2)}
                      </pre>
                    </div>
                  </div>
                </div>
              )}

              {/* 会话列表 */}
              <div>
                <h4 className="text-sm font-medium text-primary-600 mb-3">
                  对话会话 ({detail.sessions?.length || 0})
                </h4>
                <div className="space-y-2">
                  {detail.sessions?.map((session: any) => (
                    <div
                      key={session.id}
                      className="bg-primary-50 rounded-xl p-3 text-sm"
                    >
                      <div className="flex justify-between text-primary-600">
                        <span>会话 {session.id.slice(0, 8)}...</span>
                        <span>{session.message_count} 条消息</span>
                      </div>
                      <div className="text-primary-400 text-xs mt-1">
                        开始于 {new Date(session.started_at).toLocaleString('zh-CN')}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="text-center py-12 text-primary-500">暂无数据</div>
          )}
        </div>
      </div>
    </div>
  )
}
