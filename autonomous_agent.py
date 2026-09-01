"""
🤖 NOVA VISUAL GHOST OPERATOR & AUTONOMOUS PC AGENT
- Controls Windows applications visibly on your physical monitor.
- Actively monitors the screen to sync progress with hardware loading times.
- Integrates with BlenderController for dynamic 3D Modeling (Solar System, Spaceship, etc.)
- Human-like cursor movements, visible hotkey clicks, and letter-by-letter typing.
"""

import os
import re
import json
import time
import subprocess
from pathlib import Path
import pyautogui

try:
    import pygetwindow as gw
except ImportError:
    gw = None

try:
    from blender_controller import BlenderController
except ImportError:
    BlenderController = None

BASE_DIR = Path(__file__).resolve().parent
PROJECTS_DIR = BASE_DIR / "data" / "agent_workspace"
SHOT_DIR = BASE_DIR / "data" / "screenshots"

PROJECTS_DIR.mkdir(parents=True, exist_ok=True)
SHOT_DIR.mkdir(parents=True, exist_ok=True)

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1


class AutonomousAgent:
    def __init__(self, brain, vision, executor, model="llama3.2"):
        self.brain = brain
        self.vision = vision
        self.executor = executor
        self.model = model
        self.is_running = False
        self._stop_requested = False
        self.blender = BlenderController(model=model, vision=vision) if BlenderController else None

    def stop(self):
        """Emergency stop trigger"""
        self._stop_requested = True
        self.is_running = False

    # ============================================
    # 👁️ WINDOW MONITOR & FOCUS ENGINE
    # ============================================
    def _wait_for_window_on_screen(self, title_keyword: str, timeout_sec=25, notify=None) -> bool:
        """Actively polls the OS to check if the target app window is physically visible"""
        start = time.time()
        while time.time() - start < timeout_sec:
            if self._stop_requested:
                return False
                
            elapsed = int(time.time() - start)

            if gw:
                try:
                    wins = [w for w in gw.getAllWindows() if title_keyword.lower() in w.title.lower()]
                    if wins and wins[0].visible and wins[0].width > 200:
                        if notify:
                            notify(f"👁️ Window '{title_keyword}' screen par detect ho gayi! [{elapsed}s]", 0.60)
                        try:
                            wins[0].activate()
                        except:
                            pass
                        time.sleep(1.0)
                        return True
                except Exception:
                    pass

            if notify and elapsed % 2 == 0:
                notify(f"⏳ Waiting for '{title_keyword}' to open on your monitor... [{elapsed}s]", 0.30 + min(elapsed * 0.02, 0.30))

            time.sleep(1.0)

        return False

    # ============================================
    # 🎮 GHOST OPERATOR PIPELINE (VISUALLY ACTIVE)
    # ============================================
    def execute_live_ghost_task(self, user_goal: str, update_cb=None, image_cb=None) -> str:
        """
        Executes real visible operations directly on the user's physical monitor.
        """
        self.is_running = True
        self._stop_requested = False
        low = user_goal.lower().strip()

        def notify(msg, pct=None, action_type="action"):
            if update_cb:
                update_cb(msg, pct, action_type)

        def update_screen_preview(img_path):
            if image_cb and os.path.exists(img_path):
                image_cb(img_path)

        notify(f"🚀 Goal: '{user_goal}' — Processing & Screen mapping shuru...", 0.10)
        time.sleep(0.3)

        # ============================================
        # 🎨 SCENARIO 1: BLENDER DYNAMIC 3D AGENT
        # ============================================
        if "blender" in low:
            notify("🎨 [1/2] Blender Engine initialize ho raha hai...", 0.20)
            
            if not self.blender:
                self.is_running = False
                return "❌ Error: Blender Controller module missing."

            # Take initial screenshot
            init_shot = self.vision.capture("agent_live.png")
            if init_shot:
                update_screen_preview(init_shot)

            # Let BlenderController generate and run the specific 3D prompt
            res = self.blender.process_3d_command(user_goal=user_goal, update_cb=update_cb)

            # Verify and update live monitor view
            live_shot = self.vision.capture("agent_live.png")
            if live_shot:
                update_screen_preview(live_shot)

            self.is_running = False
            return res

        # ============================================
        # 🌐 SCENARIO 2: GOOGLE CHROME / WEB SEARCH / WEATHER
        # ============================================
        elif any(w in low for w in ["weather", "mausam", "search", "google", "chrome", "dhoondo", "check karo"]):
            query = re.sub(
                r"(?:open chrome|search on google|search|check|karo|batao|weather of|weather in|weather|mausam)\s*",
                "",
                user_goal,
                flags=re.IGNORECASE
            ).strip()

            if not query or "weather" in low or "mausam" in low:
                query = "current weather today" if not query else f"weather in {query}"

            notify("🌐 [1/3] Google Chrome khola ja raha hai...", 0.25)
            self.executor.hotkey("win", "r")
            time.sleep(0.4)
            self.executor.human_type("chrome", delay_per_char=0.04)
            self.executor.press("enter")

            # Wait for Chrome window to render
            self._wait_for_window_on_screen("chrome", timeout_sec=15, notify=notify)

            notify(f"⌨️ [2/3] Live typing in progress: '{query}'...", 0.60)
            self.executor.hotkey("ctrl", "t")
            time.sleep(0.6)

            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            self.executor.human_type(search_url, delay_per_char=0.03)
            time.sleep(0.3)
            self.executor.press("enter")

            notify("👁️ [3/3] Google results screen par render ho rahe hain...", 0.85)
            time.sleep(4.0)

            screen_shot = self.vision.capture("weather_result.png")
            if screen_shot:
                update_screen_preview(screen_shot)

            # Vision AI reads results from screen
            analysis = self.vision.analyze(
                f"Look at this Google search result for '{query}'. "
                "What is the temperature, weather condition, or main answer shown? Be extremely brief."
            )
            notify("🎉 Search complete!", 1.0)
            self.is_running = False
            return f"✅ Chrome mein search complete ho gaya hai!\n\n👁️ Screen Result: {analysis}"

        # ============================================
        # 📝 SCENARIO 3: NOTEPAD / WRITING NOTES
        # ============================================
        elif any(w in low for w in ["notepad", "write", "type", "likho", "notes"]):
            notify("📝 [1/3] Notepad screen par launch ho raha hai...", 0.25)
            self.executor.hotkey("win", "r")
            time.sleep(0.4)
            self.executor.human_type("notepad", delay_per_char=0.04)
            self.executor.press("enter")

            # Monitor screen until Notepad is visible
            self._wait_for_window_on_screen("notepad", timeout_sec=10, notify=notify)

            text_to_write = re.sub(
                r"(?:open notepad and write|open notepad|write in notepad|type|likho)\s*",
                "",
                user_goal,
                flags=re.IGNORECASE
            ).strip()

            if not text_to_write:
                text_to_write = "Hello Boss! Nova AI is operating this PC live."

            notify("⌨️ [2/3] Notepad mein text live type ho raha hai...", 0.65)
            self.executor.human_type(f"\n{text_to_write}\n\n— Typed autonomously by Nova AI\n", delay_per_char=0.05)

            live_shot = self.vision.capture("agent_live.png")
            if live_shot:
                update_screen_preview(live_shot)

            notify("💾 [3/3] Notes ready on your screen!", 1.0)
            self.is_running = False
            return "✅ Notepad khol kar aapke samne text type kar diya hai!"

        # ============================================
        # 🎯 SCENARIO 4: GENERAL APP LAUNCH (Photoshop, VS Code, CapCut, etc.)
        # ============================================
        else:
            app_target = re.sub(r"(?:open|run|launch|kholo)\s*", "", user_goal, flags=re.IGNORECASE).strip()
            notify(f"🚀 [1/2] Windows Start search se '{app_target}' open kiya ja raha hai...", 0.40)

            res = self.executor.open_app(app_target)
            
            # Watch screen until window is focused
            self._wait_for_window_on_screen(app_target, timeout_sec=15, notify=notify)

            live_shot = self.vision.capture("agent_live.png")
            if live_shot:
                update_screen_preview(live_shot)

            notify(f"✅ [2/2] `{app_target}` screen par active hai.", 1.0)
            self.is_running = False
            return res

    def execute_autonomous_task(self, user_goal: str, update_cb=None, image_cb=None) -> str:
        """Alias for visual ghost task execution"""
        return self.execute_live_ghost_task(user_goal, update_cb, image_cb)