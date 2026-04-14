"""
万宗心悟AI疗愈智能体 - 向量知识库服务
使用Qdrant进行语义检索
"""
from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import uuid

from app.core.config import settings
from app.knowledge.knowledge_base import knowledge_base, KnowledgeDomain, KnowledgeEntry


class VectorKnowledgeService:
    """向量知识库服务"""

    def __init__(self):
        self.client = QdrantClient(url=settings.QDRANT_URL)
        self.collection_name = settings.QDRANT_COLLECTION_NAME
        self._init_collection()

    def _init_collection(self):
        """初始化向量集合"""
        try:
            collections = self.client.get_collections().collections
            collection_names = [c.name for c in collections]

            if self.collection_name not in collection_names:
                # 创建新集合
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
                # 导入初始知识
                self._import_initial_knowledge()
        except Exception as e:
            print(f"初始化向量集合失败: {e}")

    def _import_initial_knowledge(self):
        """导入初始知识到向量库"""
        for entry in knowledge_base.entries.values():
            self.add_entry(entry)

    def add_entry(self, entry: KnowledgeEntry):
        """添加知识条目到向量库"""
        try:
            # 简化向量表示（实际应用中应使用embedding模型）
            vector = self._text_to_vector(entry.content)

            point = PointStruct(
                id=str(uuid.uuid4()),
                vector=vector,
                payload={
                    "id": entry.id,
                    "domain": entry.domain.value,
                    "category": entry.category,
                    "title": entry.title,
                    "content": entry.content,
                    "keywords": entry.keywords,
                    "target_issues": entry.target_issues,
                    "cultural_tags": entry.cultural_tags,
                    "source": entry.source
                }
            )

            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
        except Exception as e:
            print(f"添加向量失败: {e}")

    def _text_to_vector(self, text: str) -> List[float]:
        """
        文本转向量
        简化实现：基于文本特征的固定向量
        实际应用中应使用sentence-transformers等embedding模型
        """
        import hashlib
        # 使用哈希生成伪随机但稳定的向量
        hash_value = int(hashlib.md5(text.encode()).hexdigest(), 16)

        vector = []
        for i in range(384):
            # 基于哈希值生成伪随机数
            seed = (hash_value + i * 31337) % 10000
            vector.append((seed % 100) / 100.0)

        # 归一化
        magnitude = sum(v ** 2 for v in vector) ** 0.5
        if magnitude > 0:
            vector = [v / magnitude for v in vector]

        return vector

    def search(
        self,
        query: str,
        domain: Optional[str] = None,
        target_issue: Optional[str] = None,
        cultural_tags: Optional[List[str]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        语义搜索知识库

        Args:
            query: 搜索查询
            domain: 知识领域过滤
            target_issue: 针对的心理问题
            cultural_tags: 文化标签
            limit: 返回数量

        Returns:
            匹配的知识条目列表
        """
        try:
            query_vector = self._text_to_vector(query)

            # 构建过滤器
            must_conditions = []

            if domain:
                must_conditions.append(
                    FieldCondition(
                        key="domain",
                        match=MatchValue(value=domain)
                    )
                )

            search_filter = Filter(must=must_conditions) if must_conditions else None

            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                query_filter=search_filter,
                limit=limit
            )

            return [
                {
                    "id": r.payload["id"],
                    "domain": r.payload["domain"],
                    "category": r.payload["category"],
                    "title": r.payload["title"],
                    "content": r.payload["content"],
                    "keywords": r.payload["keywords"],
                    "target_issues": r.payload["target_issues"],
                    "cultural_tags": r.payload["cultural_tags"],
                    "source": r.payload["source"],
                    "score": r.score
                }
                for r in results
            ]

        except Exception as e:
            print(f"向量搜索失败: {e}")
            return []

    def get_context_for_query(
        self,
        query: str,
        user_profile: Dict[str, Any],
        limit: int = 3
    ) -> str:
        """
        获取融合上下文用于LLM回复生成
        """
        weights = user_profile.get("knowledge_weights", {})

        contexts = []

        # 按权重从各领域获取知识
        for domain, weight in weights.items():
            if weight <= 0:
                continue

            count = max(1, int(limit * weight))
            results = self.search(
                query=query,
                domain=domain,
                limit=count
            )

            for r in results:
                contexts.append(f"【{r['source']}】{r['content']}")

        return "\n\n".join(contexts) if contexts else ""


# 全局向量服务实例
vector_service = VectorKnowledgeService()
