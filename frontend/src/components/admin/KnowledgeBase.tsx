import { useState, useEffect } from 'react'
import { api } from '../../api/adminClient'

interface KnowledgeEntry {
  id: string
  domain: string  // 哲学/心理学/宗教学
  category: string
  title: string
  content: string
  keywords: string[]
  target_issues: string[]
  cultural_tags: string[]
  created_at: string
  updated_at: string
}

interface KnowledgeFormData {
  domain: string
  category: string
  title: string
  content: string
  keywords: string
  target_issues: string
  cultural_tags: string
}

const DOMAINS = ['哲学', '心理学', '宗教学']
const DOMAIN_COLORS: Record<string, string> = {
  '哲学': 'bg-purple-100 text-purple-700',
  '心理学': 'bg-blue-100 text-blue-700',
  '宗教学': 'bg-amber-100 text-amber-700'
}

export default function KnowledgeBase() {
  const [entries, setEntries] = useState<KnowledgeEntry[]>([])
  const [loading, setLoading] = useState(true)
  const [selectedDomain, setSelectedDomain] = useState<string>('全部')
  const [searchKeyword, setSearchKeyword] = useState('')
  const [showModal, setShowModal] = useState(false)
  const [editingEntry, setEditingEntry] = useState<KnowledgeEntry | null>(null)
  const [formData, setFormData] = useState<KnowledgeFormData>({
    domain: '哲学',
    category: '',
    title: '',
    content: '',
    keywords: '',
    target_issues: '',
    cultural_tags: ''
  })
  const [saving, setSaving] = useState(false)
  const [viewingEntry, setViewingEntry] = useState<KnowledgeEntry | null>(null)

  useEffect(() => {
    fetchEntries()
  }, [selectedDomain])

  const fetchEntries = async () => {
    setLoading(true)
    try {
      const params: Record<string, string> = {}
      if (selectedDomain !== '全部') {
        params.domain = selectedDomain
      }
      if (searchKeyword) {
        params.keyword = searchKeyword
      }
      const response = await api.get('/admin-api/knowledge', { params })
      setEntries(response.data.entries || [])
    } catch (error) {
      console.error('获取知识库失败:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    fetchEntries()
  }

  const openAddModal = () => {
    setEditingEntry(null)
    setFormData({
      domain: '哲学',
      category: '',
      title: '',
      content: '',
      keywords: '',
      target_issues: '',
      cultural_tags: ''
    })
    setShowModal(true)
  }

  const openEditModal = (entry: KnowledgeEntry) => {
    setEditingEntry(entry)
    setFormData({
      domain: entry.domain,
      category: entry.category,
      title: entry.title,
      content: entry.content,
      keywords: entry.keywords.join(', '),
      target_issues: entry.target_issues.join(', '),
      cultural_tags: entry.cultural_tags.join(', ')
    })
    setShowModal(true)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setSaving(true)

    const payload = {
      domain: formData.domain,
      category: formData.category,
      title: formData.title,
      content: formData.content,
      keywords: formData.keywords.split(',').map(k => k.trim()).filter(Boolean),
      target_issues: formData.target_issues.split(',').map(k => k.trim()).filter(Boolean),
      cultural_tags: formData.cultural_tags.split(',').map(k => k.trim()).filter(Boolean)
    }

    try {
      if (editingEntry) {
        await api.put(`/admin-api/knowledge/${editingEntry.id}`, payload)
      } else {
        await api.post('/admin-api/knowledge', payload)
      }
      setShowModal(false)
      fetchEntries()
    } catch (error) {
      console.error('保存知识库条目失败:', error)
      alert('保存失败，请重试')
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async (id: string) => {
    if (!confirm('确定要删除该知识库条目吗？')) return
    try {
      await api.delete(`/admin-api/knowledge/${id}`)
      fetchEntries()
    } catch (error) {
      console.error('删除知识库条目失败:', error)
    }
  }

  const filteredEntries = entries

  return (
    <div className="space-y-6">
      {/* 标题栏 */}
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-medium text-primary-800">三元融合知识库</h2>
        <button
          onClick={openAddModal}
          className="px-4 py-2 bg-accent-green text-white rounded-xl hover:bg-accent-green/90 transition"
        >
          + 添加条目
        </button>
      </div>

      {/* 筛选栏 */}
      <div className="bg-white rounded-2xl p-4 shadow-sm">
        <div className="flex flex-wrap gap-4 items-center">
          {/* 领域筛选 */}
          <div className="flex gap-2">
            <button
              onClick={() => setSelectedDomain('全部')}
              className={`px-4 py-2 rounded-xl text-sm font-medium transition ${
                selectedDomain === '全部'
                  ? 'bg-primary-700 text-white'
                  : 'bg-primary-100 text-primary-600 hover:bg-primary-200'
              }`}
            >
              全部
            </button>
            {DOMAINS.map(domain => (
              <button
                key={domain}
                onClick={() => setSelectedDomain(domain)}
                className={`px-4 py-2 rounded-xl text-sm font-medium transition ${
                  selectedDomain === domain
                    ? DOMAIN_COLORS[domain]
                    : 'bg-primary-100 text-primary-600 hover:bg-primary-200'
                }`}
              >
                {domain}
              </button>
            ))}
          </div>

          {/* 搜索框 */}
          <form onSubmit={handleSearch} className="flex-1 flex gap-2 min-w-[200px]">
            <input
              type="text"
              value={searchKeyword}
              onChange={(e) => setSearchKeyword(e.target.value)}
              placeholder="搜索标题/内容/关键词..."
              className="flex-1 px-4 py-2 rounded-xl border border-primary-200 focus:border-accent-green focus:ring-2 focus:ring-accent-green/20 outline-none"
            />
            <button
              type="submit"
              className="px-4 py-2 bg-primary-700 text-white rounded-xl hover:bg-primary-800 transition"
            >
              搜索
            </button>
          </form>
        </div>
      </div>

      {/* 知识库列表 */}
      <div className="bg-white rounded-2xl shadow-sm overflow-hidden">
        {loading ? (
          <div className="text-center py-12 text-primary-500">加载中...</div>
        ) : filteredEntries.length === 0 ? (
          <div className="text-center py-12 text-primary-400">暂无知识库条目</div>
        ) : (
          <div className="divide-y divide-primary-100">
            {filteredEntries.map((entry) => (
              <div
                key={entry.id}
                className="p-4 hover:bg-primary-50/50 transition cursor-pointer"
                onClick={() => setViewingEntry(entry)}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-2 mb-2">
                      <span className={`px-2 py-0.5 rounded text-xs font-medium ${DOMAIN_COLORS[entry.domain]}`}>
                        {entry.domain}
                      </span>
                      <span className="text-xs text-primary-400">{entry.category}</span>
                    </div>
                    <h3 className="text-lg font-medium text-primary-800 mb-1">{entry.title}</h3>
                    <p className="text-sm text-primary-500 line-clamp-2 mb-2">{entry.content}</p>
                    <div className="flex flex-wrap gap-1">
                      {entry.keywords.slice(0, 5).map((keyword, idx) => (
                        <span
                          key={idx}
                          className="px-2 py-0.5 bg-primary-100 text-primary-500 rounded text-xs"
                        >
                          {keyword}
                        </span>
                      ))}
                      {entry.keywords.length > 5 && (
                        <span className="text-xs text-primary-400">+{entry.keywords.length - 5}</span>
                      )}
                    </div>
                  </div>
                  <div className="flex gap-2 ml-4">
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        openEditModal(entry)
                      }}
                      className="px-3 py-1 text-sm bg-primary-100 text-primary-700 rounded-lg hover:bg-primary-200 transition"
                    >
                      编辑
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation()
                        handleDelete(entry.id)
                      }}
                      className="px-3 py-1 text-sm bg-red-50 text-red-600 rounded-lg hover:bg-red-100 transition"
                    >
                      删除
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* 添加/编辑弹窗 */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl w-full max-w-2xl max-h-[90vh] overflow-hidden">
            <div className="px-6 py-4 border-b border-primary-100 flex items-center justify-between">
              <h3 className="text-lg font-medium text-primary-800">
                {editingEntry ? '编辑知识库条目' : '添加知识库条目'}
              </h3>
              <button
                onClick={() => setShowModal(false)}
                className="text-primary-400 hover:text-primary-600 transition"
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSubmit} className="p-6 overflow-y-auto max-h-[calc(90vh-120px)] space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-primary-700 text-sm mb-2">领域</label>
                  <select
                    value={formData.domain}
                    onChange={(e) => setFormData({ ...formData, domain: e.target.value })}
                    className="w-full px-4 py-2 rounded-xl border border-primary-200 focus:border-accent-green focus:ring-2 focus:ring-accent-green/20 outline-none"
                    required
                  >
                    {DOMAINS.map(domain => (
                      <option key={domain} value={domain}>{domain}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-primary-700 text-sm mb-2">分类</label>
                  <input
                    type="text"
                    value={formData.category}
                    onChange={(e) => setFormData({ ...formData, category: e.target.value })}
                    placeholder="如：人生哲学、情绪管理"
                    className="w-full px-4 py-2 rounded-xl border border-primary-200 focus:border-accent-green focus:ring-2 focus:ring-accent-green/20 outline-none"
                    required
                  />
                </div>
              </div>

              <div>
                <label className="block text-primary-700 text-sm mb-2">标题</label>
                <input
                  type="text"
                  value={formData.title}
                  onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                  placeholder="请输入标题"
                  className="w-full px-4 py-2 rounded-xl border border-primary-200 focus:border-accent-green focus:ring-2 focus:ring-accent-green/20 outline-none"
                  required
                />
              </div>

              <div>
                <label className="block text-primary-700 text-sm mb-2">内容</label>
                <textarea
                  value={formData.content}
                  onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                  placeholder="请输入知识库内容..."
                  rows={6}
                  className="w-full px-4 py-2 rounded-xl border border-primary-200 focus:border-accent-green focus:ring-2 focus:ring-accent-green/20 outline-none resize-none"
                  required
                />
              </div>

              <div>
                <label className="block text-primary-700 text-sm mb-2">关键词（逗号分隔）</label>
                <input
                  type="text"
                  value={formData.keywords}
                  onChange={(e) => setFormData({ ...formData, keywords: e.target.value })}
                  placeholder="如：存在主义, 自我实现, 生命意义"
                  className="w-full px-4 py-2 rounded-xl border border-primary-200 focus:border-accent-green focus:ring-2 focus:ring-accent-green/20 outline-none"
                />
              </div>

              <div>
                <label className="block text-primary-700 text-sm mb-2">针对问题（逗号分隔）</label>
                <input
                  type="text"
                  value={formData.target_issues}
                  onChange={(e) => setFormData({ ...formData, target_issues: e.target.value })}
                  placeholder="如：焦虑, 迷茫, 情感困扰"
                  className="w-full px-4 py-2 rounded-xl border border-primary-200 focus:border-accent-green focus:ring-2 focus:ring-accent-green/20 outline-none"
                />
              </div>

              <div>
                <label className="block text-primary-700 text-sm mb-2">文化标签（逗号分隔）</label>
                <input
                  type="text"
                  value={formData.cultural_tags}
                  onChange={(e) => setFormData({ ...formData, cultural_tags: e.target.value })}
                  placeholder="如：东方, 西方, 佛教, 道家"
                  className="w-full px-4 py-2 rounded-xl border border-primary-200 focus:border-accent-green focus:ring-2 focus:ring-accent-green/20 outline-none"
                />
              </div>

              <div className="flex gap-4 pt-4">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="flex-1 py-3 bg-primary-100 text-primary-700 rounded-xl hover:bg-primary-200 transition"
                >
                  取消
                </button>
                <button
                  type="submit"
                  disabled={saving}
                  className="flex-1 py-3 bg-accent-green text-white rounded-xl hover:bg-accent-green/90 transition disabled:opacity-50"
                >
                  {saving ? '保存中...' : '保存'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* 查看详情弹窗 */}
      {viewingEntry && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl w-full max-w-3xl max-h-[90vh] overflow-hidden">
            <div className="px-6 py-4 border-b border-primary-100 flex items-center justify-between">
              <h3 className="text-lg font-medium text-primary-800">知识库详情</h3>
              <button
                onClick={() => setViewingEntry(null)}
                className="text-primary-400 hover:text-primary-600 transition"
              >
                ✕
              </button>
            </div>

            <div className="p-6 overflow-y-auto max-h-[calc(90vh-60px)]">
              <div className="flex items-center gap-2 mb-4">
                <span className={`px-3 py-1 rounded-lg text-sm font-medium ${DOMAIN_COLORS[viewingEntry.domain]}`}>
                  {viewingEntry.domain}
                </span>
                <span className="text-primary-400">{viewingEntry.category}</span>
              </div>

              <h2 className="text-2xl font-medium text-primary-800 mb-4">{viewingEntry.title}</h2>

              <div className="prose prose-primary max-w-none mb-6">
                <p className="text-primary-700 whitespace-pre-wrap leading-relaxed">{viewingEntry.content}</p>
              </div>

              <div className="space-y-4">
                <div>
                  <h4 className="text-sm font-medium text-primary-600 mb-2">关键词</h4>
                  <div className="flex flex-wrap gap-2">
                    {viewingEntry.keywords.map((keyword, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-primary-100 text-primary-600 rounded-lg text-sm"
                      >
                        {keyword}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-primary-600 mb-2">针对问题</h4>
                  <div className="flex flex-wrap gap-2">
                    {viewingEntry.target_issues.map((issue, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-blue-50 text-blue-600 rounded-lg text-sm"
                      >
                        {issue}
                      </span>
                    ))}
                  </div>
                </div>

                <div>
                  <h4 className="text-sm font-medium text-primary-600 mb-2">文化标签</h4>
                  <div className="flex flex-wrap gap-2">
                    {viewingEntry.cultural_tags.map((tag, idx) => (
                      <span
                        key={idx}
                        className="px-3 py-1 bg-amber-50 text-amber-600 rounded-lg text-sm"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="text-xs text-primary-400 pt-4 border-t border-primary-100">
                  创建于 {new Date(viewingEntry.created_at).toLocaleString('zh-CN')} · 
                  更新于 {new Date(viewingEntry.updated_at).toLocaleString('zh-CN')}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
