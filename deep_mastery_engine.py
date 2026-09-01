"""
🎓 NOVA DEEP MASTERY ENGINE (v2.0 — Delegates to SoftwareMasteryEngine)
- Deep study triggers the same professional curriculum
- Professional Blender execution with knowledge recall
"""

import os
import json
import time
from pathlib import Path
import ollama

BASE_DIR = Path(__file__).resolve().parent
MASTERY_DIR = BASE_DIR / "data" / "deep_mastery"
MASTERY_DIR.mkdir(parents=True, exist_ok=True)


class DeepMasteryEngine:

    def __init__(self, brain, skill_matrix, learner, blender_controller, model="llama3.2"):
        self.brain = brain
        self.skill_matrix = skill_matrix
        self.learner = learner
        self.blender = blender_controller
        self.model = model

    def deep_study_software(self, software_name: str, progress_cb=None) -> str:
        """Delegates to the comprehensive curriculum in SoftwareMasteryEngine"""
        from software_mastery import SoftwareMasteryEngine
        mastery = SoftwareMasteryEngine(
            self.brain, self.skill_matrix, self.learner, self.blender, self.model
        )
        return mastery.master_software_autonomously(software_name, progress_cb=progress_cb)

    def think_before_action(self, user_request: str, software: str) -> dict:
        """Chain-of-thought reasoning before execution"""
        prompt = f"""You are a SENIOR {software} Professional.
Analyze this request and plan execution:
REQUEST: "{user_request}"

Return JSON:
{{
    "goal_analysis": "specific goal",
    "professional_strategy": "best approach",
    "quality_standards": ["standard 1"],
    "potential_glitches": ["glitch and prevention"],
    "execution_phases": [{{"phase": 1, "task": "specific task"}}]
}}"""
        try:
            resp = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"num_ctx": 1024, "num_predict": 400, "num_thread": 4, "temperature": 0.15}
            )
            raw = resp['message']['content']
            s, e = raw.find('{'), raw.rfind('}') + 1
            return json.loads(raw[s:e]) if s >= 0 else {"goal_analysis": user_request}
        except:
            return {"goal_analysis": user_request}

    def execute_professional_blender_scene(self, user_request: str, progress_cb=None) -> str:
        """Execute with deep knowledge recall"""
        def notify(msg, pct=None):
            if progress_cb:
                progress_cb(msg, pct, "action")

        notify("🧠 [10%] Professional thinking...", 0.10)
        thinking = self.think_before_action(user_request, "Blender")

        notify("🧠 [30%] Recalling deep knowledge...", 0.30)
        memories = self.brain.search(f"blender professional {user_request[:40]}", top_k=5)
        knowledge = "\n".join([f"- {m['content'][:500]}" for m in memories])

        notify("🎨 [50%] Generating professional scene...", 0.50)
        if self.blender:
            enhanced = f"{user_request}\n\nPROFESSIONAL KNOWLEDGE:\n{knowledge[:2000]}"
            result = self.blender.process_3d_command(enhanced, update_cb=progress_cb)
            return result

        return "❌ Blender controller not available"

    def get_deep_mastery_status(self) -> str:
        from software_mastery import SoftwareMasteryEngine
        mastery = SoftwareMasteryEngine(
            self.brain, self.skill_matrix, self.learner, self.blender, self.model
        )
        return mastery.get_mastery_status()