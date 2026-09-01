"""
👁️ NOVA SCREEN VISION
- Real-time Screen Capture
- LLaVA AI Analysis
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SHOT_DIR = str(BASE_DIR / "data" / "screenshots")

try:
    import cv2
    import numpy as np
    import mss
    import ollama
    VISION_OK = True
except ImportError as e:
    print(f"Vision packages missing: {e}")
    VISION_OK = False


class ScreenVision:
    def __init__(self, model="llava-phi3"):
        self.model = model
        os.makedirs(SHOT_DIR, exist_ok=True)
        if VISION_OK:
            self.sct = mss.mss()

    def capture(self, name="current.png"):
        if not VISION_OK:
            return None
        try:
            img = np.array(self.sct.grab(self.sct.monitors[1]))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            path = os.path.join(SHOT_DIR, name)
            cv2.imwrite(path, img)
            return path
        except Exception as e:
            print(f"Capture error: {e}")
            return None

    def analyze(self, question="What do you see on the screen?"):
        path = self.capture()
        if not path:
            return "Vision not available"
        try:
            r = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": question, "images": [path]}]
            )
            return r['message']['content']
        except Exception as e:
            return f"Vision error: {e}"