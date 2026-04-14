# 万宗心悟AI疗愈智能体

融合人类全量哲学、全体系心理学、全球宗教正向核心底层逻辑的三位一体AI心理疗愈服务。

## 项目概述

遵循白皮书六大核心原则：
1. **非传教原则** - 彻底剥离宗教属性，保留精神疗愈属性
2. **文化尊重与逻辑一致原则** - 尊重全球所有文化，全程保持沟通逻辑一致
3. **正向疗愈原则** - 所有输出积极、治愈、向善
4. **隐私独立与跨时长记忆原则** - 用户数据绝对独立，永久存储
5. **通俗适配与多模态一致原则** - 语音入语音出、文字入文字出
6. **三元融合原则** - 哲学、心理学、宗教学有机融合

## 技术架构

| 层级 | 技术选型 |
|------|---------|
| 前端 | Tauri + React + TypeScript + Vite + TailwindCSS |
| 后端 | Python FastAPI |
| 主数据库 | PostgreSQL |
| 向量数据库 | Qdrant |
| 缓存 | Redis |
| 对象存储 | MinIO |
| 语音合成 | Edge-TTS |
| 语音识别 | Whisper |
| 部署 | Docker Compose |

## 项目目录结构

```
万宗心语/
├── backend/              # 后端服务
│   ├── app/
│   │   ├── api/         # API路由
│   │   │   ├── user/   # 用户端API
│   │   │   └── admin/  # 管理端API
│   │   ├── core/        # 核心配置
│   │   ├── models/      # 数据库模型
│   │   └── services/    # 业务服务
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/            # 前端应用
│   ├── src/
│   │   ├── components/  # React组件
│   │   ├── stores/      # Zustand状态管理
│   │   ├── api/         # API客户端
│   │   └── styles/      # 样式文件
│   ├── package.json
│   └── vite.config.ts
├── docker/               # Docker配置
│   ├── docker-compose.yml
│   └── nginx.conf
├── docs/                 # 项目文档
└── data/                 # 数据目录
    ├── knowledge_base/   # 知识库
    └── user_data/       # 用户数据
```

## 快速启动

### 1. 环境要求

- Docker & Docker Compose
- Node.js 18+ (前端开发)
- Python 3.11+ (后端开发，可选)

### 2. 启动所有服务

```bash
cd docker
docker-compose up -d
```

### 3. 访问应用

- 用户端界面: http://localhost
- 后端API文档: http://localhost:8000/docs
- 管理端API: http://localhost:8000/admin-api

### 4. 开发模式

**后端开发：**
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

**前端开发：**
```bash
cd frontend
npm install
npm run dev
```

## 核心功能

### 用户端功能

| 功能 | 说明 |
|------|------|
| 同源设备终身免密登录 | 首次验证后，同设备永久免密 |
| 跨时长永久记忆 | 间隔任意时长，数据完整保留 |
| 多模态一致交互 | 文字入文字出、语音入语音出 |
| 三位一体知识库 | 哲学+心理学+宗教学融合 |

### 管理端功能

| 功能 | 说明 |
|------|------|
| 用户管理 | 查看、搜索、封禁用户 |
| 数据查看 | 查看用户完整对话历史 |
| 数据统计 | 用户数、消息数等统计 |
| 审计日志 | 数据访问完整记录 |

## API接口

### 用户端API (/user-api/)

| 接口 | 方法 | 说明 |
|------|------|------|
| /auth/send-code | POST | 发送验证码 |
| /auth/verify | POST | 验证登录 |
| /auth/device-login | POST | 设备免密登录 |
| /conversation | POST | 发送对话 |
| /history | GET | 获取对话历史 |
| /profile | GET | 获取用户画像 |

### 管理端API (/admin-api/)

| 接口 | 方法 | 说明 |
|------|------|------|
| /auth/login | POST | 管理员登录 |
| /users | GET | 用户列表 |
| /users/{id} | GET | 用户详情 |
| /stats | GET | 统计数据 |

## 数据库模型

核心数据表：
- `users` - 用户表
- `user_devices` - 设备表（免密登录）
- `chat_sessions` - 对话会话表
- `messages` - 消息表（永久存储）
- `user_profiles` - 用户画像表
- `admins` - 管理员表
- `audit_log` - 审计日志

## 开发说明

### 前端开发

前端采用极简设计原则：
- 仅保留单一对话界面，无二级页面
- 禅意治愈风格配色
- 语音按钮支持按住说话

### 后端开发

后端遵循白皮书六大原则实现：
- 三元融合逻辑调度
- 文化属性感知
- 心理状态追踪
- 通俗化输出转化

## 许可证

专有项目
