"""
👤 NOVA USER PROFILE ENGINE
- Automatically extracts and remembers Boss's personal facts, preferences, habits, projects
- Injects Boss Context into every AI thought
"""

import os
import re
import json
from pathlib import Path
import ollama

BASE_DIR = Path(__file__).resolve().parent
PROFILE_FILE = BASE_DIR / "data" / "user_profile.json"


class UserProfileEngine:
    DEFAULT_PROFILE = {
        "boss_name": "Boss",
        "primary_skills": ["Video Editing", "Programming", "Content Creation"],
        "favorite_software": ["Premiere Pro", "VS Code", "Photoshop"],
        "working_language": "Urdu / English Mix",
        "current_projects": [],
        "habits_and_rules": [],
        "personal_facts": {}
    }

    def __init__(self, model="llama3.2"):
        self.model = model
        self.profile = self._load()

    def _load(self) -> dict:
        if PROFILE_FILE.exists():
            try:
                with open(PROFILE_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    p = self.DEFAULT_PROFILE.copy()
                    p.update(data)
                    return p
            except Exception:
                pass
        return self.DEFAULT_PROFILE.copy()

    def save(self):
        PROFILE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PROFILE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.profile, f, indent=2)

    def extract_personal_facts(self, text: str):
        """Checks if the user stated a personal fact and updates profile in background"""
        triggers = [
            "mera naam", "my name is", "mujhe pasand", "i like", "i prefer",
            "mera project", "my project", "yaad rakhna", "remember that",
            "main kaam karta hoon", "i work on", "meri routine", "call me"
        ]

        low = text.lower()
        if not any(t in low for t in triggers):
            return

        prompt = (
            "Extract any user personal facts, names, preferences, or rules from this statement.\n\n"
            f"STATEMENT: {text}\n\n"
            "Return ONLY JSON:\n"
            "{\n"
            '    "boss_name": "name if mentioned, else null",\n'
            '    "new_preference": "preference if mentioned, else null",\n'
            '    "new_project": "project name if mentioned, else null",\n'
            '    "fact_key": "short key like birthday or hobby",\n'
            '    "fact_val": "value or null"\n'
            "}"
        )

        try:
            resp = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.1, "num_ctx": 1024}
            )
            raw = resp["message"]["content"]
            start = raw.find("{")
            end = raw.rfind("}") + 1
            extracted = json.loads(raw[start:end])

            updated = False
            if extracted.get("boss_name"):
                self.profile["boss_name"] = extracted["boss_name"].capitalize()
                updated = True

            if extracted.get("new_preference"):
                pref = extracted["new_preference"]
                if pref not in self.profile["habits_and_rules"]:
                    self.profile["habits_and_rules"].append(pref)
                    updated = True

            if extracted.get("new_project"):
                proj = extracted["new_project"]
                if proj not in self.profile["current_projects"]:
                    self.profile["current_projects"].append(proj)
                    updated = True

            if extracted.get("fact_key") and extracted.get("fact_val"):
                self.profile["personal_facts"][extracted["fact_key"]] = extracted["fact_val"]
                updated = True

            if updated:
                self.save()
                print(f"👤 User Profile Auto-Updated: {self.profile['boss_name']}")

        except Exception as e:
            print(f"Profile extract note: {e}")

    def get_boss_context(self) -> str:
        """Returns a compact context string to inject into LLM system prompt"""
        p = self.profile
        rules = ", ".join(p.get("habits_and_rules", [])) or "None"
        projects = ", ".join(p.get("current_projects", [])) or "None"
        facts = ", ".join([f"{k}: {v}" for k, v in p.get("personal_facts", {}).items()]) or "None"

        return (
            f"\n\n👤 BOSS PROFILE:\n"
            f"- Boss Name: {p.get('boss_name', 'Boss')}\n"
            f"- Known Preferences: {rules}\n"
            f"- Active Projects: {projects}\n"
            f"- Personal Facts: {facts}\n"
            f"Always treat this user as your Boss with utmost loyalty and respect.\n"
        )