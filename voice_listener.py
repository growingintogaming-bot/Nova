"""
🎤 NOVA VOICE LISTENER
- Multi-language Microphone Input
- Auto-detects Urdu, English, Hindi
"""

try:
    import speech_recognition as sr
    MIC_AVAILABLE = True
except ImportError:
    MIC_AVAILABLE = False
    print("⚠️ Mic not available - install pyaudio")


class Listener:
    def __init__(self):
        if not MIC_AVAILABLE:
            self.r = None
            return
        self.r = sr.Recognizer()
        self.r.energy_threshold = 300
        self.r.dynamic_energy_threshold = True

    def listen(self, timeout=6):
        if not MIC_AVAILABLE:
            return ""
        try:
            with sr.Microphone() as src:
                print("🎤 Listening...")
                self.r.adjust_for_ambient_noise(src, duration=0.5)
                try:
                    audio = self.r.listen(src, timeout=timeout, phrase_time_limit=12)
                except sr.WaitTimeoutError:
                    return ""

            # Try multiple languages
            for lang in ["en-US", "ur-PK", "hi-IN"]:
                try:
                    text = self.r.recognize_google(audio, language=lang)
                    if text and len(text.strip()) > 1:
                        return text
                except:
                    continue

            try:
                return self.r.recognize_google(audio)
            except:
                return ""
        except Exception as e:
            print(f"Mic error: {e}")
            return ""