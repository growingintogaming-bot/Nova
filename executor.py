"""
🖱️ NOVA HUMAN-LIKE GHOST EXECUTOR
- Universal App Launcher via Windows Search
- Smooth Visible Mouse Gliding
- Real Keystroke Typing with human-like delay
"""

import os
import time
import subprocess
import pyautogui

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1


class Executor:
    def __init__(self, vision=None):
        self.vision = vision

    def smooth_move_to(self, x: int, y: int, duration: float = 0.5):
        try:
            pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeInOutQuad)
        except Exception as e:
            print(f"Mouse move error: {e}")

    def click(self, x: int, y: int, button: str = "left"):
        self.smooth_move_to(x, y, duration=0.4)
        time.sleep(0.1)
        pyautogui.click(button=button)
        return f"✅ Clicked at ({x}, {y})"

    def human_type(self, text: str, delay_per_char: float = 0.06):
        try:
            pyautogui.typewrite(text, interval=delay_per_char)
            return f"✅ Typed: {text}"
        except Exception as e:
            return f"❌ Type error: {e}"

    def hotkey(self, *keys):
        try:
            pyautogui.hotkey(*keys)
            time.sleep(0.3)
            return f"✅ Hotkey: {' + '.join(keys)}"
        except Exception as e:
            return f"❌ Hotkey error: {e}"

    def press(self, key: str):
        try:
            pyautogui.press(key)
            return f"✅ Pressed: {key}"
        except Exception as e:
            return f"❌ Press error: {e}"

    def open_app(self, app_name: str):
        """Universal App Launcher - Uses Windows Start Search for 100% accuracy"""
        clean_app = app_name.lower().replace("open", "").replace("run", "").replace("launch", "").strip()
        print(f"🚀 Universally launching app: {clean_app}")

        # Method 1: Try Windows Run dialog for standard built-ins (notepad, chrome, calc, cmd)
        built_ins = ["notepad", "chrome", "calc", "cmd", "explorer", "mspaint", "taskmgr"]
        if clean_app in built_ins:
            try:
                self.hotkey("win", "r")
                time.sleep(0.4)
                self.human_type(clean_app, delay_per_char=0.04)
                self.press("enter")
                time.sleep(1.5)
                return f"✅ Launched: {clean_app}"
            except:
                pass

        # Method 2: Windows Start Search (Works for Blender, Premiere, Photoshop, VS Code, etc.)
        try:
            pyautogui.press("win")
            time.sleep(0.6)
            pyautogui.typewrite(clean_app, interval=0.08)
            time.sleep(0.8)
            pyautogui.press("enter")
            time.sleep(2.5)
            return f"✅ `{clean_app}` ko screen par open kar diya hai!"
        except Exception as e:
            # Fallback Popen
            try:
                subprocess.Popen(f"start {clean_app}", shell=True)
                return f"✅ Attempted launch: {clean_app}"
            except Exception as ex:
                return f"❌ Launch failed: {ex}"

    def run_command(self, cmd: str):
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return r.stdout or r.stderr or "Done"
        except Exception as e:
            return f"❌ {e}"