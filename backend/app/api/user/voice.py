"""
万宗心悟AI疗愈智能体 - 语音API
遵循白皮书：语音入语音出、文字入文字出
"""
import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.models.database import get_db, User
from app.services.voice import tts_synthesize, asr_recognize
from app.api.user.auth import get_current_user_from_token

router = APIRouter(prefix="/user-api/voice", tags=["语音处理"])


@router.post("/recognize", summary="语音识别")
async def recognize_speech(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    语音转文字
    用户上传语音，AI识别为文字
    """
    if not file:
        raise HTTPException(status_code=400, detail="请上传语音文件")

    # 读取音频数据
    audio_data = await file.read()

    try:
        # 调用ASR服务
        text = await asr_recognize(audio_data)

        return {
            "text": text,
            "duration": len(audio_data) // 16000  # 估算时长
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"语音识别失败: {str(e)}")


@router.post("/synthesize", summary="语音合成")
async def synthesize_speech(
    text: str,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    文字转语音
    AI回复的文字转为语音返回
    """
    if not text:
        raise HTTPException(status_code=400, detail="请提供要转换的文字")

    # 生成唯一文件名
    filename = f"{uuid.uuid4()}.mp3"
    output_dir = "/app/data/voices"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    try:
        # 调用TTS服务
        await tts_synthesize(text, output_path)

        # 返回语音文件URL
        voice_url = f"/voices/{filename}"

        return {
            "voice_url": voice_url,
            "filename": filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"语音合成失败: {str(e)}")


@router.post("/upload", summary="上传语音消息")
async def upload_voice(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    """
    上传用户语音消息
    同时识别为文字用于对话处理
    """
    if not file:
        raise HTTPException(status_code=400, detail="请上传语音文件")

    # 生成唯一文件名
    filename = f"{uuid.uuid4()}.webm"
    upload_dir = "/app/data/voices"
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)

    # 保存文件
    audio_data = await file.read()
    with open(file_path, "wb") as f:
        f.write(audio_data)

    # 识别语音内容
    try:
        text = await asr_recognize(audio_data)
    except:
        text = ""  # 识别失败时返回空文字

    # 返回结果
    voice_url = f"/voices/{filename}"

    return {
        "voice_url": voice_url,
        "text": text,
        "filename": filename
    }
