import { useState, useEffect, useRef, useCallback } from 'react'
import { useChatStore } from '../stores/chat'
import { useAuthStore } from '../stores/auth'
import { api } from '../api/client'

// API base URL for display
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

type ConnectionStatus = 'connected' | 'connecting' | 'error'

export default function Chat() {
  const [input, setInput] = useState('')
  const [isRecording, setIsRecording] = useState(false)
  const [connectionStatus, setConnectionStatus] = useState<ConnectionStatus>('connecting')
  const [recordingDuration, setRecordingDuration] = useState(0)
  const [failedMessages, setFailedMessages] = useState<Set<string>>(new Set())
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const audioChunksRef = useRef<Blob[]>([])
  const recordingTimerRef = useRef<number | null>(null)
  const audioRef = useRef<HTMLAudioElement | null>(null)

  const { messages, isLoading, sendMessage, fetchHistory } = useChatStore()
  const { user, logout } = useAuthStore()

  // 初始化获取历史消息
  useEffect(() => {
    fetchHistory().then(() => {
      setConnectionStatus('connected')
    }).catch(() => {
      setConnectionStatus('error')
    })
  }, [])

  // 自动滚动到底部
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // 清理录音计时器
  useEffect(() => {
    return () => {
      if (recordingTimerRef.current) {
        window.clearInterval(recordingTimerRef.current)
      }
    }
  }, [])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return
    const content = input.trim()
    setInput('')
    try {
      await sendMessage(content, 'text')
    } catch (error) {
      console.error('发送消息失败')
    }
  }

  const handleRetry = async (messageId: string, content: string, contentType: 'text' | 'voice', voiceUrl?: string) => {
    // 移除失败标记
    setFailedMessages(prev => {
      const next = new Set(prev)
      next.delete(messageId)
      return next
    })
    // 重新发送
    try {
      await sendMessage(content, contentType, voiceUrl)
    } catch (error) {
      console.error('重试发送失败')
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  // 完整的语音录制功能
  const toggleRecording = async () => {
    if (isRecording) {
      // 停止录制
      stopRecording()
    } else {
      // 开始录制
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
        const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' })
        mediaRecorderRef.current = mediaRecorder
        audioChunksRef.current = []

        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data)
          }
        }

        mediaRecorder.onstop = async () => {
          // 停止所有音轨
          stream.getTracks().forEach(track => track.stop())
          
          // 转换为 blob
          const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
          
          // 清理录音计时器
          if (recordingTimerRef.current) {
            window.clearInterval(recordingTimerRef.current)
            recordingTimerRef.current = null
          }
          setRecordingDuration(0)

          // 上传并识别
          await uploadAndRecognize(audioBlob)
        }

        // 开始录制
        mediaRecorder.start(100) // 每100ms收集一次数据
        setIsRecording(true)
        
        // 开始计时
        setRecordingDuration(0)
        recordingTimerRef.current = window.setInterval(() => {
          setRecordingDuration(prev => prev + 1)
        }, 1000)

      } catch (error) {
        console.error('无法访问麦克风:', error)
        alert('无法访问麦克风，请检查权限设置')
      }
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop()
    }
    setIsRecording(false)
  }

  // 上传音频并识别
  const uploadAndRecognize = async (audioBlob: Blob) => {
    try {
      const formData = new FormData()
      formData.append('file', audioBlob, 'recording.webm')

      const response = await api.post('/user-api/voice/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      const { text, voice_url } = response.data
      
      if (text) {
        // 发送识别后的文字
        await sendMessage(text, 'voice', voice_url)
      } else {
        console.error('语音识别失败')
      }
    } catch (error) {
      console.error('上传音频失败:', error)
    }
  }

  // 播放AI语音回复
  const playVoiceMessage = useCallback((voiceUrl: string) => {
    if (audioRef.current) {
      audioRef.current.pause()
    }
    audioRef.current = new Audio(voiceUrl)
    audioRef.current.play()
  }, [])

  // 格式化录音时长
  const formatDuration = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  // 获取状态颜色
  const getStatusColor = () => {
    switch (connectionStatus) {
      case 'connected': return 'bg-accent-green'
      case 'connecting': return 'bg-yellow-500'
      case 'error': return 'bg-red-500'
    }
  }

  // 获取状态文字
  const getStatusText = () => {
    switch (connectionStatus) {
      case 'connected': return '已连接'
      case 'connecting': return '连接中...'
      case 'error': return '连接异常'
    }
  }

  return (
    <div className="min-h-screen flex flex-col bg-primary-100">
      {/* 顶部栏 */}
      <header className="bg-white shadow-sm px-4 py-3 flex items-center justify-between safe-area-inset-top">
        <div className="flex items-center space-x-3">
          <h1 className="text-xl font-medium text-primary-800">万宗心悟</h1>
          <span className="text-xs text-primary-400 hidden sm:inline">AI疗愈智能体</span>
        </div>
        <div className="flex items-center space-x-4">
          {/* 连接状态 */}
          <div className="flex items-center space-x-2 text-xs">
            <span className={`w-2 h-2 rounded-full ${getStatusColor()}`} />
            <span className="text-primary-400 hidden sm:inline">{getStatusText()}</span>
            <span className="text-primary-300 hidden md:inline text-[10px]">{API_URL}</span>
          </div>
          {user && (
            <span className="text-sm text-primary-600 hidden sm:inline">{user.nickname}</span>
          )}
          <button
            onClick={logout}
            className="text-sm text-primary-400 hover:text-primary-600 transition"
          >
            退出
          </button>
        </div>
      </header>

      {/* 消息区域 */}
      <main className="flex-1 overflow-y-auto p-4 space-y-4 pb-20 md:pb-4">
        {messages.length === 0 && !isLoading && (
          <div className="text-center py-12">
            <p className="text-primary-500 mb-2">您好，我是万宗心悟</p>
            <p className="text-primary-400 text-sm">
              请随时向我倾诉，我会用心倾听，用爱陪伴
            </p>
          </div>
        )}

        {messages.map((message) => {
          const hasFailed = failedMessages.has(message.id)
          
          return (
            <div
              key={message.id}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div
                className={`max-w-[85%] sm:max-w-[80%] rounded-2xl px-4 py-3 ${
                  message.role === 'user'
                    ? 'bg-accent-green text-white rounded-br-md'
                    : 'bg-white text-primary-800 rounded-bl-md shadow-sm'
                } ${hasFailed ? 'ring-2 ring-red-400' : ''}`}
              >
                {message.content_type === 'text' ? (
                  <p className="leading-relaxed whitespace-pre-wrap">{message.content}</p>
                ) : message.voice_url ? (
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={() => playVoiceMessage(message.voice_url!)}
                      className={`w-10 h-10 rounded-full flex items-center justify-center ${
                        message.role === 'user' ? 'bg-white/20' : 'bg-primary-100'
                      }`}
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
                        <path d="M8 5v14l11-7z"/>
                      </svg>
                    </button>
                    <span className={`text-xs ${message.role === 'user' ? 'text-white/70' : 'text-primary-400'}`}>
                      {message.voice_duration ? `${Math.round(message.voice_duration)}秒` : '语音消息'}
                    </span>
                  </div>
                ) : null}
                
                <div className="flex items-center justify-between mt-1">
                  <span
                    className={`text-xs ${
                      message.role === 'user' ? 'text-white/70' : 'text-primary-400'
                    }`}
                  >
                    {new Date(message.created_at).toLocaleTimeString('zh-CN', {
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </span>
                  
                  {hasFailed && (
                    <button
                      onClick={() => handleRetry(message.id, message.content, message.content_type, message.voice_url)}
                      className="text-xs bg-red-100 text-red-600 px-2 py-0.5 rounded-full ml-2 hover:bg-red-200 transition"
                    >
                      重试
                    </button>
                  )}
                </div>
              </div>
            </div>
          )
        })}

        {/* 加载状态 */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white rounded-2xl rounded-bl-md px-4 py-3 shadow-sm">
              <div className="flex items-center space-x-2">
                <div className="flex space-x-1">
                  <span className="w-2 h-2 bg-primary-300 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
                  <span className="w-2 h-2 bg-primary-300 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
                  <span className="w-2 h-2 bg-primary-300 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
                </div>
                <span className="text-primary-400 text-sm">AI正在思考...</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </main>

      {/* 输入区域 */}
      <footer className="bg-white border-t border-primary-100 p-4 safe-area-inset-bottom">
        <div className="flex items-end space-x-3 max-w-4xl mx-auto">
          <div className="flex-1">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="请倾诉您的内心..."
              rows={1}
              className="w-full px-4 py-3 rounded-2xl border border-primary-200 focus:border-accent-green focus:ring-2 focus:ring-accent-green/20 outline-none resize-none transition"
              style={{ maxHeight: '120px' }}
            />
          </div>

          {/* 录音按钮 */}
          <button
            onClick={toggleRecording}
            className={`w-12 h-12 rounded-full flex items-center justify-center transition flex-shrink-0 ${
              isRecording
                ? 'bg-red-500 text-white'
                : 'bg-primary-100 text-primary-500 hover:bg-primary-200'
            }`}
            title={isRecording ? '停止录音' : '开始录音'}
          >
            {isRecording ? (
              <div className="flex flex-col items-center">
                <div className="w-4 h-4 bg-white rounded-sm animate-pulse" />
                <span className="text-[10px] mt-0.5 text-white/80">
                  {formatDuration(recordingDuration)}
                </span>
              </div>
            ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            )}
          </button>

          {/* 发送按钮 */}
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading || isRecording}
            className="w-12 h-12 rounded-full bg-accent-green text-white flex items-center justify-center hover:bg-accent-green/90 transition disabled:opacity-50 disabled:cursor-not-allowed flex-shrink-0"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
            </svg>
          </button>
        </div>

        <p className="text-center text-primary-400 text-xs mt-3">
          遵循六大核心原则：非传教 · 文化尊重 · 正向疗愈 · 隐私独立 · 通俗适配 · 三元融合
        </p>
      </footer>
    </div>
  )
}
