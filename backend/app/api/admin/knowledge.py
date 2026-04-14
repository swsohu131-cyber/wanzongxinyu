"""
万宗心悟AI疗愈智能体 - 知识库管理API
用于管理端查看和配置知识库
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from app.models.database import Admin
from app.api.admin.management import get_current_admin_from_token
from app.knowledge.knowledge_base import knowledge_base, KnowledgeDomain, KnowledgeEntry
from app.knowledge.vector_store import vector_service

router = APIRouter(prefix="/admin-api/knowledge", tags=["知识库管理"])


class KnowledgeEntryResponse(BaseModel):
    """知识条目响应"""
    id: str
    domain: str
    category: str
    title: str
    content: str
    keywords: List[str]
    target_issues: List[str]
    cultural_tags: List[str]
    source: str


@router.get("/", summary="获取知识库统计")
async def get_knowledge_stats(
    current_admin: Admin = Depends(get_current_admin_from_token)
):
    """获取知识库统计信息"""
    entries = list(knowledge_base.entries.values())

    stats = {
        "total": len(entries),
        "by_domain": {
            "philosophy": len([e for e in entries if e.domain == KnowledgeDomain.PHILOSOPHY]),
            "psychology": len([e for e in entries if e.domain == KnowledgeDomain.PSYCHOLOGY]),
            "religion": len([e for e in entries if e.domain == KnowledgeDomain.RELIGION]),
        },
        "categories": list(set(e.category for e in entries))
    }

    return stats


@router.get("/search", summary="搜索知识库")
async def search_knowledge(
    q: str = Query(..., description="搜索关键词"),
    domain: Optional[str] = Query(None, description="知识领域: philosophy/psychology/religion"),
    limit: int = Query(5, ge=1, le=20),
    current_admin: Admin = Depends(get_current_admin_from_token)
):
    """搜索知识库"""
    domain_enum = None
    if domain:
        try:
            domain_enum = KnowledgeDomain(domain)
        except ValueError:
            raise HTTPException(status_code=400, detail="无效的知识领域")

    results = knowledge_base.search(
        query=q,
        domain=domain_enum,
        limit=limit
    )

    return {
        "query": q,
        "domain": domain,
        "count": len(results),
        "results": [
            {
                "id": e.id,
                "domain": e.domain.value,
                "category": e.category,
                "title": e.title,
                "content": e.content,
                "keywords": e.keywords,
                "target_issues": e.target_issues,
                "cultural_tags": e.cultural_tags,
                "source": e.source
            }
            for e in results
        ]
    }


@router.get("/categories", summary="获取所有分类")
async def get_categories(
    current_admin: Admin = Depends(get_current_admin_from_token)
):
    """获取知识库所有分类"""
    entries = list(knowledge_base.entries.values())

    categories = {}
    for entry in entries:
        if entry.domain.value not in categories:
            categories[entry.domain.value] = set()
        categories[entry.domain.value].add(entry.category)

    return {
        domain: list(cats) for domain, cats in categories.items()
    }


@router.get("/by-domain/{domain}", summary="按领域获取知识")
async def get_by_domain(
    domain: str,
    current_admin: Admin = Depends(get_current_admin_from_token)
):
    """按知识领域获取所有条目"""
    try:
        domain_enum = KnowledgeDomain(domain)
    except ValueError:
        raise HTTPException(status_code=400, detail="无效的知识领域")

    entries = [
        e for e in knowledge_base.entries.values()
        if e.domain == domain_enum
    ]

    return {
        "domain": domain,
        "count": len(entries),
        "entries": [
            {
                "id": e.id,
                "category": e.category,
                "title": e.title,
                "content": e.content,
                "keywords": e.keywords,
                "target_issues": e.target_issues,
                "cultural_tags": e.cultural_tags,
                "source": e.source
            }
            for e in entries
        ]
    }
