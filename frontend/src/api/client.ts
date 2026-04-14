import axios, { AxiosError, AxiosResponse } from 'axios'
import { useAuthStore } from '../stores/auth'

// API基础配置
const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export interface ApiResponse<T = any> {
  data: T
  message?: string
  code?: number
}

export const api = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器 - 从Zustand store获取Token
api.interceptors.request.use(
  (config) => {
    // 从Zustand store获取token，而不是直接从localStorage读取
    const token = useAuthStore.getState().token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器 - 统一错误处理
api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    if (error.response) {
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          // Token无效，清除本地存储并重载
          useAuthStore.getState().logout()
          window.location.reload()
          break
        case 403:
          console.error('权限不足')
          break
        case 404:
          console.error('请求的资源不存在')
          break
        case 500:
          console.error('服务器内部错误')
          break
        default:
          // 其他错误，尝试提取错误消息
          const errorMsg = (data as any)?.detail || (data as any)?.message || '请求失败'
          console.error(`API错误 (${status}):`, errorMsg)
      }
    } else if (error.request) {
      // 请求已发出但没有收到响应
      console.error('网络错误，请检查您的网络连接')
    } else {
      // 请求配置出错
      console.error('请求配置错误:', error.message)
    }
    
    return Promise.reject(error)
  }
)

// 封装常用的API方法
export const apiClient = {
  // GET请求
  get: <T = any>(url: string, params?: object): Promise<ApiResponse<T>> => {
    return api.get(url, { params })
  },

  // POST请求
  post: <T = any>(url: string, data?: object): Promise<ApiResponse<T>> => {
    return api.post(url, data)
  },

  // PUT请求
  put: <T = any>(url: string, data?: object): Promise<ApiResponse<T>> => {
    return api.put(url, data)
  },

  // DELETE请求
  delete: <T = any>(url: string, params?: object): Promise<ApiResponse<T>> => {
    return api.delete(url, { params })
  },

  // 文件上传（语音等）
  upload: <T = any>(
    url: string, 
    file: Blob | File, 
    fieldName: string = 'file',
    additionalData?: Record<string, string>
  ): Promise<ApiResponse<T>> => {
    const formData = new FormData()
    formData.append(fieldName, file)
    
    if (additionalData) {
      Object.entries(additionalData).forEach(([key, value]) => {
        formData.append(key, value)
      })
    }

    return api.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      timeout: 60000 // 文件上传需要更长的超时时间
    })
  },

  // 获取当前API基础URL
  getBaseUrl: () => BASE_URL
}
