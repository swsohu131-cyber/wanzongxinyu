"""
万宗心悟AI疗愈智能体 - 语音服务
遵循白皮书：通俗适配与多模态一致原则
语音入语音出、文字入文字出
"""
import io
import asyncio
from typing import Optional
import edge_tts

from app.core.config import settings


class VoiceService:
    """语音服务"""

    def __init__(self):
        self.voice = settings.EDGE_TTS_VOICE
        self.whisper_model = settings.WHISPER_MODEL

    async def text_to_speech(self, text: str, output_path: str) -> str:
        """
        文字转语音 (TTS)
        使用 Edge-TTS 生成语音
        """
        try:
            # 使用 Edge-TTS 生成语音
            communicate = edge_tts.Communicate(text, self.voice)
            await communicate.save(output_path)
            return output_path
        except Exception as e:
            print(f"TTS生成失败: {e}")
            raise

    async def speech_to_text(self, audio_data: bytes) -> str:
        """
        语音转文字 (ASR)
        使用 Whisper 进行语音识别
        """
        try:
            import whisper
            import numpy as np

            # 加载模型（可缓存）
            if not hasattr(self, '_whisper_model'):
                self._whisper_model = whisper.load_model(self.whisper_model)

            # 将字节数据转换为音频
            import struct
            from scipy.io import wavfile
            import tempfile

            # 写入临时文件
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
                f.write(audio_data)
                temp_path = f.name

            # 加载音频
            audio = whisper.load_audio(temp_path)

            # 识别
            result = self._whisper_model.transcribe(audio, language='zh')

            # 清理临时文件
            import os
            os.unlink(temp_path)

            return result["text"]

        except Exception as e:
            print(f"ASR识别失败: {e}")
            raise

    def get_audio_duration(self, file_path: str) -> int:
        """获取音频时长（秒）"""
        try:
            from pydub import AudioSegment
            audio = AudioSegment.from_file(file_path)
            return len(audio) // 1000  # 毫秒转秒
        except:
            return 0


# 全局服务实例
voice_service = VoiceService()


async def tts_synthesize(text: str, output_path: str) -> str:
    """文字转语音"""
    return await voice_service.text_to_speech(text, output_path)


async def asr_recognize(audio_data: bytes) -> str:
    """语音转文字"""
    return await voice_service.speech_to_text(audio_data)
