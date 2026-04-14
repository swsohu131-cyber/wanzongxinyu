import { create } from 'zustand'
import { api } from '../api/client'

interface Message {
  id: string
  session_id: string
  role: 'user' | 'assistant'
  content: string
  content_type: 'text' | 'voice'
  voice_url?: string
  voice_duration?: number
  created_at: string
  metadata: Record<string, any>
}

interface ChatState {
  messages: Message[]
  isLoading: boolean
  fetchHistory: () => Promise<void>
  sendMessage: (content: string, contentType?: 'text' | 'voice', voiceUrl?: string) => Promise<void>
  clearMessages: () => void
}

export const useChatStore = create<ChatState>((set) => ({
  messages: [],
  isLoading: false,

  fetchHistory: async () => {
    set({ isLoading: true })
    try {
      const response = await api.get('/user-api/history')
      set({ messages: response.data || [] })
    } catch (error) {
      console.error('获取历史消息失败:', error)
    } finally {
      set({ isLoading: false })
    }
  },

  sendMessage: async (content, contentType = 'text', voiceUrl) => {
    set({ isLoading: true })

    // 添加用户消息到本地
    const userMessage: Message = {
      id: `temp_${Date.now()}`,
      session_id: '',
      role: 'user',
      content,
      content_type: contentType,
      voice_url: voiceUrl,
      created_at: new Date().toISOString(),
      metadata: {}
    }

    set(state => ({
      messages: [...state.messages, userMessage]
    }))

    try {
      const response = await api.post('/user-api/conversation', {
        content,
        content_type: contentType,
        voice_url: voiceUrl
      })

      // 添加AI回复
      const aiMessage: Message = {
        id: response.data.message.id,
        session_id: response.data.message.session_id,
        role: 'assistant',
        content: response.data.message.content,
        content_type: response.data.message.content_type,
        voice_url: response.data.message.voice_url,
        created_at: response.data.message.created_at,
        metadata: response.data.message.metadata || {}
      }

      set(state => ({
        messages: [...state.messages, aiMessage]
      }))
    } catch (error) {
      console.error('发送消息失败:', error)
      // 移除临时消息
      set(state => ({
        messages: state.messages.filter(m => m.id !== userMessage.id)
      }))
    } finally {
      set({ isLoading: false })
    }
  },

  clearMessages: () => {
    set({ messages: [] })
  }
}))
