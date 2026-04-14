"""
万宗心悟AI疗愈智能体 - 感知洞察模块
使用LLM深度分析用户输入，提取多维洞察
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
import httpx

from sqlalchemy.orm import Session

from app.models.database import User, UserProfile, Message
from app.core.config import settings


@dataclass
class PerceptionResult:
    """感知洞察结果"""
    emotions: List[str] = field(default_factory=list)  # ["焦虑", "失落", "愤怒"]
    cultural_hints: Dict[str, Any] = field(default_factory=dict)  # {"language": "chinese", "region": "china"}
    psychological_type: str = ""  # "存在焦虑", "人际关系问题"
    topics: List[str] = field(default_factory=list)  # ["工作", "家庭", "感情"]
    severity: str = "low"  # "low", "medium", "high"
    suggested_weights: Dict[str, float] = field(default_factory=lambda: {"philosophy": 0.33, "psychology": 0.34, "religion": 0.33})


class PerceptionService:
    """感知洞察服务 - 使用LLM分析用户输入"""

    def __init__(self, db: Session, user: User, profile: UserProfile):
        self.db = db
        self.user = user
        self.profile = profile

    async def analyze_input(self, content: str, user_history: Optional[List[Message]] = None) -> PerceptionResult:
        """
        LLM分析用户输入，返回洞察结果
        """
        # 构建分析提示词
        analysis_prompt = self._build_analysis_prompt(content, user_history)
        
        # 调用LLM进行分析
        llm_response = await self._call_llm_for_analysis(analysis_prompt)
        
        # 解析LLM响应
        result = self._parse_llm_response(llm_response)
        
        return result

    def _build_analysis_prompt(self, content: str, user_history: Optional[List[Message]] = None) -> str:
        """构建分析提示词"""
        
        # 获取用户画像上下文
        profile_context = {
            "cultural_background": self.profile.cultural_background or {},
            "psychological_states": self.profile.psychological_states or [],
            "knowledge_weights": self.profile.knowledge_weights or {"philosophy": 0.33, "psychology": 0.34, "religion": 0.33}
        }
        
        # 获取历史消息摘要
        history_summary = ""
        if user_history:
            recent_msgs = user_history[-10:]  # 最近10条消息
            history_summary = "\n".join([
                f"[{msg.role}]: {msg.content[:100]}..." if len(msg.content) > 100 else f"[{msg.role}]: {msg.content}"
                for msg in recent_msgs
            ])
        
        prompt = f"""你是一个专业的心理洞察分析师。请分析以下用户输入，提取多维度的心理和文化洞察。

【用户基本信息】
用户画像: {json.dumps(profile_context, ensure_ascii=False)}

【历史对话摘要】
{history_summary if history_summary else "无历史对话"}

【当前输入】
{content}

请以JSON格式返回分析结果，包含以下字段：
{{
    "emotions": ["情绪关键词列表，如：焦虑、失落、愤怒等"],
    "cultural_hints": {{"language": "语言", "region": "地区", "cultural_references": ["文化引用"]}},
    "psychological_type": "心理问题类型，如：存在焦虑、人际关系问题、工作压力等",
    "topics": ["话题标签列表，如：工作、家庭、感情、健康等"],
    "severity": "严重程度 low/medium/high",
    "suggested_weights": {{"哲学偏好": 0.0-1.0, "心理学偏好": 0.0-1.0, "宗教学偏好": 0.0-1.0}}
}}

请确保返回的是合法的JSON格式，不要包含其他文字。"""
        
        return prompt

    async def _call_llm_for_analysis(self, prompt: str) -> str:
        """调用LLM进行洞察分析"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                if settings.LLM_PROVIDER == "ollama":
                    response = await client.post(
                        f"{settings.OLLAMA_BASE_URL}/api/generate",
                        json={
                            "model": settings.LLM_MODEL,
                            "prompt": prompt,
                            "stream": False
                        }
                    )
                    response.raise_for_status()
                    result = response.json()
                    return result.get("response", "")
                else:
                    # OpenAI API
                    response = await client.post(
                        f"{settings.OPENAI_BASE_URL}/chat/completions",
                        headers={
                            "Authorization": f"Bearer {settings.OPENAI_API_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": settings.LLM_MODEL,
                            "messages": [{"role": "user", "content": prompt}],
                            "stream": False
                        }
                    )
                    response.raise_for_status()
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"LLM分析调用失败: {e}")
            return "{}"

    def _parse_llm_response(self, llm_response: str) -> PerceptionResult:
        """解析LLM响应"""
        try:
            # 尝试提取JSON
            json_str = llm_response.strip()
            if json_str.startswith("```json"):
                json_str = json_str[7:]
            if json_str.startswith("```"):
                json_str = json_str[3:]
            if json_str.endswith("```"):
                json_str = json_str[:-3]
            
            data = json.loads(json_str.strip())
            
            return PerceptionResult(
                emotions=data.get("emotions", []),
                cultural_hints=data.get("cultural_hints", {}),
                psychological_type=data.get("psychological_type", ""),
                topics=data.get("topics", []),
                severity=data.get("severity", "low"),
                suggested_weights=data.get("suggested_weights", {"philosophy": 0.33, "psychology": 0.34, "religion": 0.33})
            )
        except json.JSONDecodeError:
            # 解析失败，返回默认结果
            return PerceptionResult()

    def update_profile(self, perception_result: PerceptionResult, current_content: str):
        """
        将洞察结果更新到用户画像
        """
        # 更新文化背景
        cultural_bg = self.profile.cultural_background or {}
        if perception_result.cultural_hints:
            cultural_bg.update(perception_result.cultural_hints)
        self.profile.cultural_background = cultural_bg

        # 更新心理状态追踪
        psychological_states = self.profile.psychological_states or []
        current_state = {
            "timestamp": datetime.utcnow().isoformat(),
            "content_preview": current_content[:100],
            "emotions": perception_result.emotions,
            "psychological_type": perception_result.psychological_type,
            "topics": perception_result.topics,
            "severity": perception_result.severity
        }
        psychological_states.append(current_state)
        
        # 保持最近100条状态记录
        if len(psychological_states) > 100:
            psychological_states = psychological_states[-100:]
        
        self.profile.psychological_states = psychological_states

        # 更新聊天模式
        chat_patterns = self.profile.chat_patterns or {}
        chat_patterns["total_conversations"] = chat_patterns.get("total_conversations", 0) + 1
        chat_patterns["last_interaction"] = datetime.utcnow().isoformat()
        
        # 分析表达风格
        expression_style = self._analyze_expression_style(current_content)
        if expression_style:
            chat_patterns["expression_style"] = expression_style
        
        self.profile.chat_patterns = chat_patterns

        # 渐进式更新知识权重
        if perception_result.suggested_weights:
            current_weights = self.profile.knowledge_weights or {"philosophy": 0.33, "psychology": 0.34, "religion": 0.33}
            # 轻度融合，避免大幅波动
            learning_rate = 0.1
            for key in ["philosophy", "psychology", "religion"]:
                if key in perception_result.suggested_weights:
                    current_weights[key] = current_weights.get(key, 0.33) + \
                        learning_rate * (perception_result.suggested_weights[key] - current_weights.get(key, 0.33))
            
            # 归一化
            total = sum(current_weights.values())
            if total > 0:
                current_weights = {k: v/total for k, v in current_weights.items()}
            
            self.profile.knowledge_weights = current_weights

        self.profile.updated_at = datetime.utcnow()
        self.db.commit()

    def _analyze_expression_style(self, content: str) -> Dict[str, Any]:
        """分析用户表达风格"""
        style = {}
        
        # 文字长度
        if len(content) > 200:
            style["length"] = "long"
        elif len(content) > 50:
            style["length"] = "medium"
        else:
            style["length"] = "short"
        
        # 是否使用表情符号
        emoji_chars = [c for c in content if c in "😊😢😡😰🤔🙏✨💪😔🥰😤😭"]
        style["emoji_usage"] = "high" if len(emoji_chars) > 3 else "low" if len(emoji_chars) > 0 else "none"
        
        # 是否为问句
        question_marks = content.count("？") + content.count("?")
        style["questioning"] = "high" if question_marks > 2 else "normal"
        
        # 语言正式程度
        formal_words = ["请问", "希望", "期待", "希望您", "麻烦您"]
        informal_words = ["啦啦", "哈哈", "唉", "啥", "咋"]
        
        formal_count = sum(1 for w in formal_words if w in content)
        informal_count = sum(1 for w in informal_words if w in content)
        
        if formal_count > informal_count:
            style["formality"] = "formal"
        elif informal_count > formal_count:
            style["formality"] = "informal"
        else:
            style["formality"] = "neutral"
        
        return style


def get_perception_service(db: Session, user: User, profile: UserProfile) -> PerceptionService:
    """获取感知服务实例"""
    return PerceptionService(db, user, profile)
