"""
万宗心悟AI疗愈智能体 - 对话服务
遵循白皮书六大核心原则：
- 正向疗愈原则
- 通俗适配与多模态一致原则
- 三元融合原则
"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID
import json
import httpx

from sqlalchemy.orm import Session

from app.models.database import User, UserProfile, ChatSession, Message, UserFeedback
from app.models.schemas import ConversationRequest, ConversationResponse, MessageResponse, UserProfileResponse
from app.services.dialogue_llm import DialogueLLM
from app.perception.perception import PerceptionService, get_perception_service
from app.memory.memory import MemoryService, get_memory_service
from app.knowledge.knowledge_base import knowledge_base, TrinityKnowledgeBase


class DialogueService:
    """对话服务"""

    def __init__(self, db: Session, user: User):
        self.db = db
        self.user = user
        self.profile = self._get_or_create_profile()
        self.perception_service = get_perception_service(db, user, self.profile)
        self.memory_service = get_memory_service(db, user)
        self.llm = DialogueLLM()

    def _get_or_create_profile(self) -> UserProfile:
        """获取或创建用户画像"""
        profile = self.db.query(UserProfile).filter(
            UserProfile.user_id == self.user.id
        ).first()

        if not profile:
            profile = UserProfile(user_id=self.user.id)
            self.db.add(profile)
            self.db.commit()
            self.db.refresh(profile)

        return profile

    def _get_or_create_session(self, content_type: str = "text") -> ChatSession:
        """获取或创建当前会话"""
        # 查找最近活跃会话
        session = self.db.query(ChatSession).filter(
            ChatSession.user_id == self.user.id,
            ChatSession.is_archived == False
        ).order_by(ChatSession.last_message_at.desc()).first()

        if not session:
            session = ChatSession(
                user_id=self.user.id,
                session_type=content_type
            )
            self.db.add(session)
            self.db.commit()
            self.db.refresh(session)

        return session

    async def _generate_ai_response(
        self, 
        user_message: str, 
        metadata: Dict[str, Any],
        context: Dict[str, Any]
    ) -> str:
        """
        调用LLM生成疗愈回复
        遵循白皮书：
        - 三元融合：哲学+心理学+宗教学
        - 通俗表达：杜绝一切专业术语
        - 正向疗愈：积极、治愈、向善
        """
        # 获取相关知识库条目
        knowledge_context = knowledge_base.get_knowledge_for_llm_context(
            query=user_message,
            user_profile=context.get("profile", {})
        )
        
        # 构建完整提示词
        full_prompt = self.llm.build_system_prompt(
            user_message=user_message,
            context=context,
            knowledge_context=knowledge_context
        )
        
        # 调用LLM
        response = await self.llm.generate_response(full_prompt)
        
        return response

    def _update_knowledge_weights(self, user_message: str, response: str) -> Dict[str, float]:
        """根据对话内容微调知识权重"""
        weights = self.profile.knowledge_weights or {"philosophy": 0.33, "psychology": 0.34, "religion": 0.33}
        # 知识权重已通过perception service的suggested_weights自动更新
        return weights

    async def process_conversation(self, request: ConversationRequest) -> ConversationResponse:
        """
        处理对话
        遵循白皮书标准化交互流程：
        1. 用户多模态自由倾诉
        2. 多维感知与逻辑校验
        3. 三元融合逻辑匹配
        4. 多模态通俗化转化
        5. 逻辑一致化回复
        6. 终身数据留存
        """
        session = self._get_or_create_session(request.content_type)

        # 1. 获取用户历史消息用于上下文分析
        user_history = self.db.query(Message).filter(
            Message.user_id == self.user.id,
            Message.session_id == session.id
        ).order_by(Message.created_at.desc()).limit(20).all()

        # 2. 感知洞察：使用LLM分析用户输入
        perception_result = await self.perception_service.analyze_input(
            content=request.content,
            user_history=user_history
        )

        # 3. 更新用户画像（基于感知结果）
        self.perception_service.update_profile(perception_result, request.content)

        # 4. 获取完整上下文（短期记忆+情节记忆+用户画像）
        full_context = await self.memory_service.get_full_context()
        
        # 添加感知结果到上下文
        full_context["current_perception"] = {
            "emotions": perception_result.emotions,
            "psychological_type": perception_result.psychological_type,
            "topics": perception_result.topics,
            "severity": perception_result.severity
        }

        # 5. 存储用户消息
        user_metadata = {
            "content_type": request.content_type,
            "perception": {
                "emotions": perception_result.emotions,
                "cultural_hints": perception_result.cultural_hints,
                "psychological_type": perception_result.psychological_type,
                "topics": perception_result.topics,
                "severity": perception_result.severity
            }
        }

        user_message = Message(
            session_id=session.id,
            user_id=self.user.id,
            role="user",
            content=request.content,
            content_type=request.content_type,
            voice_url=request.voice_url,
            voice_duration=request.voice_duration,
            metadata=user_metadata
        )
        self.db.add(user_message)

        # 6. 生成AI响应（使用LLM + 知识库 + 上下文）
        ai_response_content = await self._generate_ai_response(
            request.content, 
            user_metadata,
            full_context
        )

        # 7. 存储AI消息
        ai_metadata = {
            "content_type": request.content_type,
            "knowledge_weights_snapshot": self.profile.knowledge_weights,
            "cultural_background_used": self.profile.cultural_background,
            "perception_snapshot": {
                "psychological_type": perception_result.psychological_type,
                "topics": perception_result.topics
            }
        }

        ai_message = Message(
            session_id=session.id,
            user_id=self.user.id,
            role="assistant",
            content=ai_response_content,
            content_type=request.content_type,
            metadata=ai_metadata
        )
        self.db.add(ai_message)

        # 8. 更新会话统计
        session.message_count += 2
        session.last_message_at = datetime.utcnow()

        # 9. 存储情节记忆
        await self.memory_service.store_episodic(
            event_type="conversation",
            content={
                "user_message": request.content[:200],
                "ai_response": ai_response_content[:200],
                "perception": {
                    "emotions": perception_result.emotions,
                    "psychological_type": perception_result.psychological_type,
                    "topics": perception_result.topics
                },
                "session_id": str(session.id)
            },
            importance=5
        )

        # 10. 更新短期记忆中的最近上下文
        await self.memory_service.store_short_term(
            "recent_context",
            {
                "last_message": request.content[:100],
                "emotions": perception_result.emotions,
                "topics": perception_result.topics,
                "timestamp": datetime.utcnow().isoformat()
            },
            ttl=3600
        )

        # 11. 更新知识权重（已由perception service处理）
        new_weights = self._update_knowledge_weights(request.content, ai_response_content)
        self.profile.knowledge_weights = new_weights

        # 12. 更新用户画像
        self.profile.updated_at = datetime.utcnow()

        self.db.commit()

        return ConversationResponse(
            message=MessageResponse.model_validate(ai_message),
            updated_profile=UserProfileResponse.model_validate(self.profile)
        )

    def get_conversation_history(self, session_id: Optional[UUID] = None) -> List[MessageResponse]:
        """获取对话历史"""
        query = self.db.query(Message).filter(Message.user_id == self.user.id)

        if session_id:
            query = query.filter(Message.session_id == session_id)

        messages = query.order_by(Message.created_at.asc()).all()

        return [MessageResponse.model_validate(m) for m in messages]

    def submit_feedback(self, feedback_type: str, message_id: UUID, content: Optional[str] = None) -> bool:
        """提交反馈 - 用于知识库学习"""
        # 验证消息属于当前用户
        message = self.db.query(Message).filter(
            Message.id == message_id,
            Message.user_id == self.user.id
        ).first()

        if not message:
            return False

        feedback = UserFeedback(
            user_id=self.user.id,
            message_id=message_id,
            feedback_type=feedback_type,
            content=content
        )
        self.db.add(feedback)
        self.db.commit()

        # TODO: 根据反馈更新知识库
        return True


def get_dialogue_service(db: Session, user: User) -> DialogueService:
    """获取对话服务实例"""
    return DialogueService(db, user)
