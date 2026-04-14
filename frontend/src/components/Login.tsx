import { useState } from 'react'
import { useAuthStore } from '../stores/auth'

export default function Login() {
  const [step, setStep] = useState<'phone' | 'code'>('phone')
  const [phone, setPhone] = useState('')
  const [code, setCode] = useState('')
  const [nickname, setNickname] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const { sendCode, verifyCode } = useAuthStore()

  const handleSendCode = async () => {
    if (!phone || phone.length !== 11) {
      setError('请输入正确的11位手机号')
      return
    }

    setLoading(true)
    setError('')

    try {
      await sendCode(phone)
      setStep('code')
    } catch (e: any) {
      setError(e.response?.data?.detail || '发送验证码失败')
    } finally {
      setLoading(false)
    }
  }

  const handleVerify = async () => {
    if (!code || code.length !== 6) {
      setError('请输入6位验证码')
      return
    }
    if (!nickname) {
      setError('请输入您的称呼')
      return
    }

    setLoading(true)
    setError('')

    try {
      await verifyCode(phone, code, nickname)
    } catch (e: any) {
      setError(e.response?.data?.detail || '验证失败，请重试')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white rounded-3xl shadow-lg p-8">
        {/* Logo和标题 */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-medium text-primary-800 mb-2">万宗心悟</h1>
          <p className="text-primary-500 text-sm">AI疗愈智能体</p>
        </div>

        {step === 'phone' ? (
          /* 手机号输入步骤 */
          <div className="space-y-6">
            <div>
              <label className="block text-primary-700 text-sm mb-2">手机号</label>
              <input
                type="tel"
                value={phone}
                onChange={(e) => setPhone(e.target.value.replace(/\D/g, '').slice(0, 11))}
                placeholder="请输入手机号"
                className="w-full px-4 py-3 rounded-xl border border-primary-200 focus:border-accent-green focus:ring-2 focus:ring-accent-green/20 outline-none transition"
                maxLength={11}
              />
            </div>

            {error && (
              <p className="text-red-500 text-sm text-center">{error}</p>
            )}

            <button
              onClick={handleSendCode}
              disabled={loading}
              className="w-full py-3 bg-accent-green text-white rounded-xl font-medium hover:bg-accent-green/90 transition disabled:opacity-50"
            >
              {loading ? '发送中...' : '获取验证码'}
            </button>

            <p className="text-primary-400 text-xs text-center">
              首次验证即完成注册，同设备永久免密登录
            </p>
          </div>
        ) : (
          /* 验证码和昵称步骤 */
          <div className="space-y-6">
            <div className="text-center text-primary-600 text-sm mb-4">
              验证码已发送至 {phone}
              <button
                onClick={() => setStep('phone')}
                className="ml-2 text-accent-green underline"
              >
                更改
              </button>
            </div>

            <div>
              <label className="block text-primary-700 text-sm mb-2">验证码</label>
              <input
                type="text"
                value={code}
                onChange={(e) => setCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                placeholder="请输入6位验证码"
                className="w-full px-4 py-3 rounded-xl border border-primary-200 focus:border-accent-green focus:ring-2 focus:ring-accent-green/20 outline-none transition text-center text-2xl tracking-widest"
                maxLength={6}
                autoFocus
              />
            </div>

            <div>
              <label className="block text-primary-700 text-sm mb-2">您的称呼</label>
              <input
                type="text"
                value={nickname}
                onChange={(e) => setNickname(e.target.value)}
                placeholder="请输入您的称呼"
                className="w-full px-4 py-3 rounded-xl border border-primary-200 focus:border-accent-green focus:ring-2 focus:ring-accent-green/20 outline-none transition"
                maxLength={20}
              />
            </div>

            {error && (
              <p className="text-red-500 text-sm text-center">{error}</p>
            )}

            <button
              onClick={handleVerify}
              disabled={loading}
              className="w-full py-3 bg-accent-green text-white rounded-xl font-medium hover:bg-accent-green/90 transition disabled:opacity-50"
            >
              {loading ? '验证中...' : '开始疗愈之旅'}
            </button>
          </div>
        )}

        {/* 底部说明 */}
        <div className="mt-8 pt-6 border-t border-primary-100">
          <p className="text-primary-400 text-xs text-center leading-relaxed">
            遵循六大核心原则：非传教 · 文化尊重 · 正向疗愈 · 隐私独立 · 通俗适配 · 三元融合
          </p>
        </div>
      </div>
    </div>
  )
}
