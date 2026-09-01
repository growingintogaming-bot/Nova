"""
🔄 NOVA AUTO-LEARNING ENGINE
- Continuous background memory ingestion from conversation
- Learns from user corrections instantly
- Auto-extracts valuable solutions, insights, and facts into ChromaDB
"""

import threading
from pathlib import Path
import ollama

BASE_DIR = Path(__file__).resolve().parent


class AutoLearner:
    def __init__(self, brain, model="llama3.2"):
        self.brain = brain
        self.model = model

    def ingest_turn_async(self, user_text: str, ai_response: str):
        """Runs in a background thread after each chat turn to extract knowledge"""
        threading.Thread(
            target=self._analyze_and_learn,
            args=(user_text, ai_response),
            daemon=True
        ).start()

    def _analyze_and_learn(self, user_text: str, ai_response: str):
        low_user = user_text.lower()

        # Check for User Corrections or Verified Solutions
        is_correction = any(w in low_user for w in [
            "galat hai", "wrong", "nahi aise", "actually",
            "theek nahi", "correct method is", "remember", "suno"
        ])
        is_knowledge_heavy = len(user_text) > 60 or len(ai_response) > 300

        if not (is_correction or is_knowledge_heavy):
            return

        prompt = (
            "Analyze this user-AI exchange. If it contains a useful fact, code technique, user correction, or solution, extract it as a 2-3 line knowledge snippet.\n\n"
            f"USER: {user_text}\n"
            f"AI: {ai_response[:800]}\n\n"
            "If nothing new to learn, return 'SKIP'. Otherwise return the exact learning snippet:"
        )

        try:
            resp = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.1, "num_ctx": 1024}
            )
            extracted = resp["message"]["content"].strip()

            if extracted and "SKIP" not in extracted and len(extracted) > 25:
                tag = "correction" if is_correction else "auto_insight"
                self.brain.add(
                    text=extracted,
                    source=f"conversation_{tag}",
                    metadata={"type": tag, "auto_learned": True}
                )
                print(f"🧠 AutoLearner: New insight indexed in background ({tag})!")

        except Exception as e:
            print(f"Auto-learning note: {e}")