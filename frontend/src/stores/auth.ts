import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import { api } from '../api/client'

interface User {
  id: string
  nickname: string
  phone?: string
  email?: string
  created_at: string
  last_login_at?: string
  status: string
}

interface AuthState {
  token: string | null
  user: User | null
  deviceFingerprint: string | null
  setToken: (token: string, user: User) => void
  checkDeviceLogin: () => Promise<void>
  sendCode: (phone: string) => Promise<void>
  verifyCode: (phone: string, code: string, nickname: string) => Promise<void>
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      token: null,
      user: null,
      deviceFingerprint: null,

      setToken: (token, user) => {
        // 持久化设备指纹
        const fp = generateFingerprint()
        localStorage.setItem('wanzongxinyu-fp', fp)
        set({ token, user, deviceFingerprint: fp })
      },

      checkDeviceLogin: async () => {
        // 生成设备指纹
        const fp = generateFingerprint()
        set({ deviceFingerprint: fp })

        try {
          const response = await api.post('/user-api/auth/device-login', {
            device_fingerprint: fp
          })
          if (response.data.access_token) {
            set({ token: response.data.access_token, user: response.data.user })
          }
        } catch (error) {
          // 设备未绑定，正常流程
          console.log('设备未绑定，需要登录')
        }
      },

      sendCode: async (phone: string) => {
        await api.post('/user-api/auth/send-code', { phone })
      },

      verifyCode: async (phone: string, code: string, nickname: string) => {
        const fp = get().deviceFingerprint || generateFingerprint()
        const response = await api.post('/user-api/auth/verify', {
          phone,
          code,
          nickname,
          device_fingerprint: fp
        })
        if (response.data.access_token) {
          set({
            token: response.data.access_token,
            user: response.data.user,
            deviceFingerprint: fp
          })
        }
      },

      logout: () => {
        set({ token: null, user: null })
      }
    }),
    {
      name: 'wanzongxinyu-auth',
      partialize: (state) => ({
        token: state.token,
        user: state.user,
        deviceFingerprint: state.deviceFingerprint
      })
    }
  )
)

// 生成设备指纹 - 持久化存储确保同一设备获得相同指纹
function generateFingerprint(): string {
  const STORAGE_KEY = 'wanzongxinyu-fp'
  
  // 检查是否已存储过指纹
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored) return stored
  
  // 生成新指纹
  const fp = [
    navigator.userAgent,
    navigator.language,
    screen.width,
    screen.height,
    screen.colorDepth,
    new Date().getTimezoneOffset()
  ].join('|')

  // 简单哈希
  let hash = 0
  for (let i = 0; i < fp.length; i++) {
    const char = fp.charCodeAt(i)
    hash = ((hash << 5) - hash) + char
    hash = hash & hash
  }

  const fingerprint = 'fp_' + Math.abs(hash).toString(36)
  
  // 持久化存储
  localStorage.setItem(STORAGE_KEY, fingerprint)
  return fingerprint
}
