import axios from 'axios'

// 管理端API配置
const ADMIN_API_URL = import.meta.env.VITE_ADMIN_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: ADMIN_API_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 添加管理员Token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('wanzongxinyu-admin-token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 处理错误
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('wanzongxinyu-admin-token')
      window.location.reload()
    }
    return Promise.reject(error)
  }
)
