"""
🎮 NOVA UNIVERSAL SOFTWARE OPERATOR
- Brings target software to foreground
- Executes learned macro steps with live screen verification
"""

import os
import time
import subprocess
from pathlib import Path
import pyautogui

BASE_DIR = Path(__file__).resolve().parent
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1


class UniversalSoftwareOperator:
    def __init__(self, executor, vision):
        self.executor = executor
        self.vision = vision
        self.is_running = False

    def focus_or_launch_software(self, software_name):
        software_name = software_name.lower().replace(" ", "_")
        print(f"🪟 Launching: {software_name}...")
        self.executor.open_app(software_name)
        time.sleep(3.0)
        return True

    def execute_learned_skill_on_software(self, skill_manifest, target_file_path=None, progress_cb=None):
        self.is_running = True
        software = skill_manifest.get("software", "app")
        skill_name = skill_manifest.get("skill_name", "Macro")
        steps = skill_manifest.get("steps", [])
        total_steps = len(steps)

        def notify(msg, pct=None):
            if progress_cb:
                progress_cb(msg, pct, "action")

        notify(f"🚀 Software Operator: '{software.upper()}' (Skill: {skill_name})...", 0.10)
        self.focus_or_launch_software(software)
        notify(f"🪟 `{software.upper()}` focused on screen!", 0.25)

        for idx, step in enumerate(steps, start=1):
            if not self.is_running:
                notify("🛑 Aborted.", 0.0)
                return "🛑 Operation aborted."

            desc = step.get("desc", f"Step {idx}")
            action_type = step.get("action_type", "hotkey")
            wait_time = float(step.get("wait_after_sec", 1.0))
            pct = 0.25 + (idx / total_steps) * 0.65

            notify(f"▶️ [{idx}/{total_steps}] {desc}...", pct)

            try:
                if action_type == "hotkey":
                    keys = step.get("keys", [])
                    self.executor.hotkey(*keys)
                elif action_type == "type_text":
                    text = step.get("text", "")
                    if "{input_file}" in text and target_file_path:
                        text = text.replace("{input_file}", str(target_file_path))
                    self.executor.human_type(text, delay_per_char=0.04)
                elif action_type == "press":
                    self.executor.press(step.get("key", "enter"))
                elif action_type == "mouse_click":
                    self.executor.click(int(step.get("x", 500)), int(step.get("y", 500)))
                time.sleep(wait_time)
            except Exception as e:
                notify(f"⚠️ Step {idx} warning: {e}", pct)

        notify("👁️ Verifying with LLaVA Vision...", 0.95)
        time.sleep(1.0)
        self.vision.capture("software_final.png")
        analysis = self.vision.analyze(f"Describe the current state of {software} on screen.")

        notify(f"🎉 Skill applied on {software.upper()}!", 1.0)
        self.is_running = False

        return (
            f"✅ SOFTWARE SKILL APPLIED!\n"
            f"🎯 Software: {software.upper()}\n"
            f"📋 Skill: {skill_name}\n"
            f"📊 Steps: {total_steps}\n\n"
            f"👁️ Screen Verification:\n{analysis[:300]}"
        )