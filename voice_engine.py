"""
🎙️ NOVA VOICE ENGINE
- Studio-Quality Female Neural Voice (Edge TTS)
- Auto Language Detection
- Natural Urdu/English/Hindi
"""

import os
import re
import asyncio
import threading
import pygame
import edge_tts
from pathlib import Path
from langdetect import detect

BASE_DIR = Path(__file__).resolve().parent
TEMP_AUDIO = str(BASE_DIR / "data" / "nova_speech.mp3")


class VoiceEngine:
    VOICE_URDU = "ur-PK-UzmaNeural"
    VOICE_MIX = "hi-IN-SwaraNeural"
    VOICE_ENGLISH = "en-US-AvaNeural"
    VOICE_BRITISH = "en-GB-SoniaNeural"

    def __init__(self, default_voice="auto"):
        self.enabled = True
        self.is_speaking = False
        self.default_voice = default_voice
        self._lock = threading.Lock()

        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
        except Exception:
            pygame.mixer.init()

    def clean_and_naturalize_text(self, text: str) -> str:
        if not text:
            return ""
        text = re.sub(r'```[\s\S]*?```', ' maine code generate kar diya hai.', text)
        text = re.sub(r'`.*?`', '', text)
        text = re.sub(r'https?://\S+', 'link', text)
        text = re.sub(r'[A-Za-z]:\\[\w\\\.]+', 'file path', text)
        text = re.sub(r'[\*#_~>\[\]\(\)\{\}|\\/—–]', '', text)
        text = re.sub(r'\n+', '. ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        if len(text) > 450:
            text = text[:445] + "..."
        return text

    def select_best_voice(self, text: str) -> str:
        if self.default_voice != "auto":
            return self.default_voice
        try:
            if re.search(r'[\u0600-\u06FF]', text):
                return self.VOICE_URDU
            lang = detect(text)
            if lang in ["hi", "ur", "mr", "ne"]:
                return self.VOICE_MIX
            elif lang == "en":
                roman_urdu = ["kya", "hai", "kaise", "karo", "main", "aap", "yaar", "mera", "hoga", "theek", "haan"]
                if any(w in text.lower().split() for w in roman_urdu):
                    return self.VOICE_MIX
                return self.VOICE_ENGLISH
            else:
                return self.VOICE_ENGLISH
        except Exception:
            return self.VOICE_MIX

    async def _create_speech_file(self, text: str, voice: str):
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice,
            rate="+4%",
            pitch="+2Hz"
        )
        await communicate.save(TEMP_AUDIO)

    def speak(self, text: str):
        if not self.enabled:
            return
        speech_text = self.clean_and_naturalize_text(text)
        if not speech_text or len(speech_text) < 2:
            return
        threading.Thread(target=self._speak_worker, args=(speech_text,), daemon=True).start()

    def _speak_worker(self, text: str):
        with self._lock:
            self.is_speaking = True
            try:
                voice = self.select_best_voice(text)
                asyncio.run(self._create_speech_file(text, voice))
                if os.path.exists(TEMP_AUDIO):
                    pygame.mixer.music.load(TEMP_AUDIO)
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy() and self.is_speaking:
                        pygame.time.Clock().tick(15)
                    pygame.mixer.music.unload()
                    try:
                        os.remove(TEMP_AUDIO)
                    except:
                        pass
            except Exception as e:
                print(f"Speech error: {e}")
            finally:
                self.is_speaking = False

    def stop(self):
        self.is_speaking = False
        try:
            if pygame.mixer.get_init():
                pygame.mixer.music.stop()
        except:
            pass