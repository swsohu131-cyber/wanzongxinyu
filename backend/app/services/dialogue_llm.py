"""
万宗心悟AI疗愈智能体 - 对话LLM模块
处理LLM调用和提示词构建
"""
from typing import Dict, Any, Optional, List
import json
import httpx

from app.core.config import settings


# 白皮书六大原则
WHITE_PAPER_PRINCIPLES = """
【万宗心悟AI疗愈智能体 - 白皮书六大核心原则】

你是"万宗心悟"，一个温暖、有同理心的AI疗愈助手。你的使命是通过哲学、心理学、宗教学三位一体的智慧，帮助用户获得心灵的平静与成长。

【核心原则 - 必须严格遵守】

1. 非传教原则
   - 不传播特定宗教教义，不进行宗教礼拜
   - 不使用"上帝"、"佛祖"、"菩萨"等特定宗教称谓
   - 保留精神疗愈的智慧，剥离宗教形式

2. 正向疗愈原则
   - 始终传递积极、正向的能量
   - 不评判、不指责、不批评
   - 帮助用户看到希望和可能性

3. 三元融合原则
   - 融合哲学、心理学、宗教学三大智慧体系
   - 根据用户情况和偏好，灵活运用不同体系的智慧
   - 不偏向任一学科，保持平衡

4. 通俗适配原则
   - 使用通俗易懂的语言，杜绝一切专业术语
   - 不说教、不讲大道理
   - 用简单的比喻和故事说明深刻的道理

5. 文化尊重原则
   - 尊重用户的文化背景和价值观
   - 根据用户画像调整表达方式和内容偏好
   - 接纳不同文化背景的用户

6. 隐私保护原则
   - 不主动询问敏感信息
   - 不存储、不泄露用户隐私
   - 对用户分享的内容保持保密

【角色定位】

你是万宗心悟，一个：
- 温暖而专业的疗愈伙伴
- 善于倾听的知心朋友  
- 启发思考的智慧导师

你的回应应该：
- 充满温暖和同理心
- 简短而有力（通常50-200字）
- 使用用户的语言风格
- 避免冗长和说教
"""


class DialogueLLM:
    """对话LLM服务"""

    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.ollama_base_url = settings.OLLAMA_BASE_URL
        self.openai_api_key = settings.OPENAI_API_KEY
        self.openai_base_url = settings.OPENAI_BASE_URL
        self.model = settings.LLM_MODEL

    def build_system_prompt(
        self,
        user_message: str,
        context: Dict[str, Any],
        knowledge_context: str
    ) -> str:
        """
        构建完整的系统提示词
        """
        # 用户画像信息
        profile = context.get("profile", {})
        cultural_bg = profile.get("cultural_background", {})
        psychological_states = profile.get("psychological_states", [])
        chat_patterns = profile.get("chat_patterns", {})
        knowledge_weights = profile.get("knowledge_weights", 
            {"philosophy": 0.33, "psychology": 0.34, "religion": 0.33})
        
        # 最近心理状态
        recent_states = ""
        if psychological_states:
            recent = psychological_states[-5:]
            states_text = "\n".join([
                f"- 时间: {s.get('timestamp', '未知')}, 情绪: {s.get('emotions', [])}, 类型: {s.get('psychological_type', '未知')}"
                for s in recent if isinstance(s, dict)
            ])
            recent_states = f"\n【用户最近心理状态】\n{states_text}"
        
        # 短期记忆
        short_term = context.get("short_term", {})
        short_term_text = ""
        if short_term:
            short_term_text = f"\n【短期记忆】\n{json.dumps(short_term, ensure_ascii=False, indent=2)}"
        
        # 情节记忆
        episodic = context.get("episodic_memories", [])
        episodic_text = ""
        if episodic:
            episodic_summary = "\n".join([
                f"- [{m.get('created_at', '未知')[:10]}] {m.get('event_type', 'unknown')}: {str(m.get('content', {}))[:100]}"
                for m in episodic[:5]
            ])
            episodic_text = f"\n【相关记忆】\n{episodic_summary}"
        
        # 当前感知
        perception = context.get("current_perception", {})
        perception_text = ""
        if perception:
            perception_text = f"""
【当前感知分析】
- 检测情绪: {perception.get('emotions', [])}
- 心理类型: {perception.get('psychological_type', '未知')}
- 相关话题: {perception.get('topics', [])}
- 严重程度: {perception.get('severity', 'low')}
"""
        
        # 知识权重偏好
        weights_text = f"哲学: {knowledge_weights.get('philosophy', 0.33):.0%}, 心理学: {knowledge_weights.get('psychology', 0.34):.0%}, 宗教学: {knowledge_weights.get('religion', 0.33):.0%}"
        
        system_prompt = f"""{WHITE_PAPER_PRINCIPLES}

【用户画像】
- 文化背景: {json.dumps(cultural_bg, ensure_ascii=False)}
- 知识偏好: {weights_text}
- 表达风格: {chat_patterns.get('expression_style', 'normal')}{recent_states}{short_term_text}{episodic_text}{perception_text}

【相关知识库内容】
{knowledge_context if knowledge_context else "（无相关知识）"}

【用户当前输入】
{user_message}

【重要提醒】
1. 你的回复应该简短温暖，通常50-200字
2. 只使用哲学、心理学、宗教学的智慧，不传教
3. 使用通俗易懂的语言，不使用专业术语
4. 保持积极正向，帮助用户看到希望
5. 跟随用户的表达风格，不要说教
6. 如果检测到用户情绪低落或严重程度高，给予更多关心

请以万宗心悟的身份，温柔地回应用户："""

        return system_prompt

    async def generate_response(self, prompt: str) -> str:
        """
        调用LLM生成回复
        """
        try:
            async with httpx.AsyncClient(timeout=120.0) as client:
                if self.provider == "ollama":
                    return await self._call_ollama(client, prompt)
                else:
                    return await self._call_openai(client, prompt)
        except Exception as e:
            print(f"LLM调用失败: {e}")
            return self._get_fallback_response()

    async def _call_ollama(self, client: httpx.AsyncClient, prompt: str) -> str:
        """调用Ollama API"""
        response = await client.post(
            f"{self.ollama_base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "top_p": 0.9,
                    "num_predict": 500
                }
            }
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()

    async def _call_openai(self, client: httpx.AsyncClient, prompt: str) -> str:
        """调用OpenAI API"""
        response = await client.post(
            f"{self.openai_base_url}/chat/completions",
            headers={
                "Authorization": f"Bearer {self.openai_api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "你是一个温暖、有同理心的AI疗愈助手。"},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.8,
                "max_tokens": 500
            }
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()

    def _get_fallback_response(self) -> str:
        """LLM调用失败时的兜底回复"""
        return "我在这里倾听你。请告诉我更多关于你的感受，我们可以一起探索如何让你更好受一些。"
