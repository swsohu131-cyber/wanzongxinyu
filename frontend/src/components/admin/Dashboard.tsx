import { useState, useEffect } from 'react'
import { api } from '../../api/adminClient'

interface Stats {
  total_users: number
  active_users_today: number
  total_messages: number
  total_sessions: number
  avg_messages_per_user: number
  users_by_day?: { date: string; count: number }[]
  messages_by_day?: { date: string; count: number }[]
}

export default function Dashboard() {
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    setRefreshing(true)
    try {
      const response = await api.get('/admin-api/stats')
      setStats(response.data)
    } catch (error) {
      console.error('获取统计数据失败:', error)
      // 使用模拟数据展示UI
      setStats({
        total_users: 0,
        active_users_today: 0,
        total_messages: 0,
        total_sessions: 0,
        avg_messages_per_user: 0,
        users_by_day: [],
        messages_by_day: []
      })
    } finally {
      setLoading(false)
      setRefreshing(false)
    }
  }

  // 简单的CSS条形图组件
  const SimpleBarChart = ({ data, maxValue, color, title }: {
    data: { label: string; value: number }[]
    maxValue: number
    color: string
    title: string
  }) => {
    if (!data || data.length === 0) {
      return (
        <div className="bg-white rounded-2xl p-6 shadow-sm">
          <h3 className="text-lg font-medium text-primary-700 mb-4">{title}</h3>
          <div className="text-primary-400 text-sm text-center py-8">暂无数据</div>
        </div>
      )
    }

    return (
      <div className="bg-white rounded-2xl p-6 shadow-sm">
        <h3 className="text-lg font-medium text-primary-700 mb-4">{title}</h3>
        <div className="space-y-2">
          {data.map((item, idx) => (
            <div key={idx} className="flex items-center gap-3">
              <span className="text-xs text-primary-400 w-12 text-right">{item.label}</span>
              <div className="flex-1 h-6 bg-primary-100 rounded-full overflow-hidden">
                <div
                  className={`h-full ${color} rounded-full transition-all duration-500`}
                  style={{ width: `${maxValue > 0 ? (item.value / maxValue) * 100 : 0}%` }}
                />
              </div>
              <span className="text-xs text-primary-600 w-8">{item.value}</span>
            </div>
          ))}
        </div>
      </div>
    )
  }

  // 简单的CSS饼图/环形图组件
  const SimpleRingChart = ({ segments, title }: {
    segments: { label: string; value: number; color: string }[]
    title: string
  }) => {
    const total = segments.reduce((sum, s) => sum + s.value, 0)
    if (total === 0) {
      return (
        <div className="bg-white rounded-2xl p-6 shadow-sm">
          <h3 className="text-lg font-medium text-primary-700 mb-4">{title}</h3>
          <div className="text-primary-400 text-sm text-center py-8">暂无数据</div>
        </div>
      )
    }

    let cumulativePercent = 0

    return (
      <div className="bg-white rounded-2xl p-6 shadow-sm">
        <h3 className="text-lg font-medium text-primary-700 mb-4">{title}</h3>
        <div className="flex items-center gap-6">
          {/* 环形图 */}
          <div className="relative w-32 h-32">
            <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
              {segments.map((segment, idx) => {
                const percent = (segment.value / total) * 100
                const startPercent = cumulativePercent
                cumulativePercent += percent
                
                const startX = Math.cos(2 * Math.PI * startPercent / 100)
                const startY = Math.sin(2 * Math.PI * startPercent / 100)
                const endX = Math.cos(2 * Math.PI * (startPercent + percent) / 100)
                const endY = Math.sin(2 * Math.PI * (startPercent + percent) / 100)
                
                const largeArcFlag = percent > 50 ? 1 : 0
                
                const pathData = [
                  `M 50 50`,
                  `L ${50 + startX * 45} ${50 + startY * 45}`,
                  `A 45 45 0 ${largeArcFlag} 1 ${50 + endX * 45} ${50 + endY * 45}`,
                  'Z'
                ].join(' ')

                return (
                  <path
                    key={idx}
                    d={pathData}
                    fill={segment.color}
                    className="transition-all duration-300"
                  />
                )
              })}
              <circle cx="50" cy="50" r="30" fill="white" />
            </svg>
            <div className="absolute inset-0 flex items-center justify-center">
              <span className="text-lg font-semibold text-primary-700">{total}</span>
            </div>
          </div>

          {/* 图例 */}
          <div className="flex-1 space-y-2">
            {segments.map((segment, idx) => (
              <div key={idx} className="flex items-center gap-2">
                <span
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: segment.color }}
                />
                <span className="text-sm text-primary-600 flex-1">{segment.label}</span>
                <span className="text-sm text-primary-400">
                  {total > 0 ? Math.round((segment.value / total) * 100) : 0}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-primary-500">加载中...</div>
      </div>
    )
  }

  // 准备图表数据
  const userChartData = (stats?.users_by_day || []).slice(-7).map(item => ({
    label: item.date.slice(5), // MM-DD格式
    value: item.count
  }))
  const messageChartData = (stats?.messages_by_day || []).slice(-7).map(item => ({
    label: item.date.slice(5),
    value: item.count
  }))
  const maxUserValue = Math.max(...userChartData.map(d => d.value), 1)
  const maxMessageValue = Math.max(...messageChartData.map(d => d.value), 1)

  // 用户状态分布（模拟数据）
  const userStatusSegments = [
    { label: '活跃用户', value: stats?.active_users_today || 0, color: '#10b981' },
    { label: '普通用户', value: Math.max((stats?.total_users || 0) - (stats?.active_users_today || 0), 0), color: '#829ab1' }
  ]

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-medium text-primary-800">数据概览</h2>
        <button
          onClick={fetchStats}
          disabled={refreshing}
          className="px-4 py-2 bg-primary-100 text-primary-700 rounded-xl hover:bg-primary-200 transition disabled:opacity-50"
        >
          {refreshing ? '刷新中...' : '刷新数据'}
        </button>
      </div>

      {/* 核心指标卡片 */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {/* 总用户数 */}
        <div className="bg-white rounded-2xl p-6 shadow-sm">
          <div className="text-primary-400 text-sm mb-2">总用户数</div>
          <div className="text-3xl font-semibold text-primary-800">
            {stats?.total_users?.toLocaleString() || 0}
          </div>
        </div>

        {/* 今日活跃 */}
        <div className="bg-white rounded-2xl p-6 shadow-sm">
          <div className="text-primary-400 text-sm mb-2">今日活跃</div>
          <div className="text-3xl font-semibold text-accent-green">
            {stats?.active_users_today?.toLocaleString() || 0}
          </div>
        </div>

        {/* 总消息数 */}
        <div className="bg-white rounded-2xl p-6 shadow-sm">
          <div className="text-primary-400 text-sm mb-2">总消息数</div>
          <div className="text-3xl font-semibold text-primary-800">
            {stats?.total_messages?.toLocaleString() || 0}
          </div>
        </div>

        {/* 总会话数 */}
        <div className="bg-white rounded-2xl p-6 shadow-sm">
          <div className="text-primary-400 text-sm mb-2">总会话数</div>
          <div className="text-3xl font-semibold text-primary-800">
            {stats?.total_sessions?.toLocaleString() || 0}
          </div>
        </div>

        {/* 平均消息 */}
        <div className="bg-white rounded-2xl p-6 shadow-sm col-span-2 md:col-span-1">
          <div className="text-primary-400 text-sm mb-2">人均消息</div>
          <div className="text-3xl font-semibold text-primary-800">
            {stats?.avg_messages_per_user?.toFixed(1) || '0.0'}
          </div>
        </div>
      </div>

      {/* 图表区域 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* 用户趋势图 */}
        <SimpleBarChart
          data={userChartData}
          maxValue={maxUserValue}
          color="bg-accent-green"
          title="近7日用户增长"
        />

        {/* 消息趋势图 */}
        <SimpleBarChart
          data={messageChartData}
          maxValue={maxMessageValue}
          color="bg-primary-500"
          title="近7日消息统计"
        />
      </div>

      {/* 用户分布 */}
      <SimpleRingChart
        segments={userStatusSegments}
        title="用户活跃分布"
      />

      {/* 快捷操作 */}
      <div className="bg-white rounded-2xl p-6 shadow-sm">
        <h3 className="text-lg font-medium text-primary-700 mb-4">快捷操作</h3>
        <div className="flex flex-wrap gap-4">
          <a
            href="/admin/users"
            className="px-4 py-2 bg-accent-green text-white rounded-xl hover:bg-accent-green/90 transition"
          >
            用户管理
          </a>
          <a
            href="/admin/knowledge"
            className="px-4 py-2 bg-primary-700 text-white rounded-xl hover:bg-primary-800 transition"
          >
            知识库管理
          </a>
        </div>
      </div>
    </div>
  )
}
