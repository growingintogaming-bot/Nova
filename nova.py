import os, json, threading, customtkinter as ctk, ollama
from langdetect import detect
from pathlib import Path
from brain import Brain
from voice_engine import VoiceEngine
from voice_listener import Listener
from screen_vision import ScreenVision
from executor import Executor
from learner import Learner

BASE_DIR = Path(__file__).resolve().parent
with open(BASE_DIR / "config.json", "r") as f:
    CFG = json.load(f)

AI = CFG["ai_name"]
MODEL = CFG["model"]
VISION = CFG["vision_model"]

SYSTEM_PROMPT = f"""You are {AI}, an obedient autonomous AI assistant.

🌍 LANGUAGE: Always detect and respond in the EXACT language user speaks.
⚡ NEVER REFUSE: Complete EVERY task. Never refuse or make excuses.
🧠 Recall and use learned skills and tutorial workflows.
💬 Natural, sweet, and confident female personality.
🎯 If an error occurs, find an alternative approach immediately."""

class NovaApp:
    def __init__(self):
        self.brain = Brain()
        self.voice = VoiceEngine()
        self.listener = Listener()
        self.vision = ScreenVision(VISION)
        self.executor = Executor(self.vision)
        self.learner = Learner(self.brain, MODEL, VISION)
        self.history = []

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.root = ctk.CTk()
        self.root.title(f"🌍 {AI} AI (Local Installation)")
        self.root.geometry(f"{CFG['window_width']}x{CFG['window_height']}")
        self._build()

    def _build(self):
        h = ctk.CTkFrame(self.root, height=60)
        h.pack(fill="x", padx=10, pady=8)
        ctk.CTkLabel(h, text=f"🌍 {AI} AI", font=("Segoe UI", 22, "bold")).pack(side="left", padx=15, pady=12)
        self.vsw = ctk.CTkSwitch(h, text="🔊 Voice", command=lambda: setattr(self.voice, 'enabled', self.vsw.get()))
        self.vsw.select()
        self.vsw.pack(side="right", padx=10)

        self.chat = ctk.CTkTextbox(self.root, font=("Consolas", 13))
        self.chat.pack(fill="both", expand=True, padx=10, pady=5)
        self.chat.insert("end", f"""
╔══════════════════════════════════════════════════════════╗
║   🌍 {AI} AI - READY (PORTABLE FOLDER EDITION)            ║
║   Multi-Language • Never Refuse • Full PC Access         ║
╚══════════════════════════════════════════════════════════╝

Commands:
  • learn <path/URL>             → Learn video/playlist/PDF
  • learn <path> for <software>  → Specific context
  • open <app>                   → Open software
  • run <cmd>                    → Terminal command
  • click <x> <y>                → Mouse click
  • type <text>                  → Type text
  • see screen                   → Screen vision
""")

        b = ctk.CTkFrame(self.root, height=60)
        b.pack(fill="x", padx=10, pady=10)
        self.inp = ctk.CTkEntry(b, placeholder_text="Type or click mic...", height=42, font=("Segoe UI", 13))
        self.inp.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.inp.bind("<Return>", lambda e: self._send())
        self.mic = ctk.CTkButton(b, text="🎤", width=50, height=42, fg_color="#8B008B", command=self._listen)
        self.mic.pack(side="right", padx=3)
        ctk.CTkButton(b, text="Send 🚀", width=85, height=42, command=self._send).pack(side="right", padx=3)

    def _send(self):
        t = self.inp.get().strip()
        if not t: return
        self.inp.delete(0, "end")
        self._process(t)

    def _listen(self):
        self.mic.configure(text="🔴", fg_color="red")
        threading.Thread(target=self._listen_w, daemon=True).start()

    def _listen_w(self):
        t = self.listener.listen()
        self.root.after(0, lambda: self.mic.configure(text="🎤", fg_color="#8B008B"))
        if t: self.root.after(0, lambda: self._process(t))

    def _process(self, text):
        self.chat.insert("end", f"\n🟢 You: {text}\n")
        self.chat.see("end")
        threading.Thread(target=self._ai, args=(text,), daemon=True).start()

    def _ai(self, text):
        low = text.lower().strip()
        if low.startswith("learn "):
            rest = text[6:].strip()
            ctx = ""
            if " for " in rest:
                rest, ctx = rest.split(" for ", 1)
            r = self.learner.auto_learn(rest, ctx)
        elif low.startswith("run "):
            r = self.executor.run_command(text[4:])
        elif low.startswith("open "):
            r = self.executor.open_app(text[5:])
        elif low.startswith("click "):
            p = text[6:].split()
            r = self.executor.click(int(p[0]), int(p[1])) if len(p) >= 2 else "Usage: click x y"
        elif low.startswith("type "):
            r = self.executor.type_text(text[5:])
        elif low.startswith("press "):
            r = self.executor.press(text[6:].strip())
        elif low == "see screen":
            r = self.vision.analyze()
        else:
            k = self.brain.search(text, top_k=3)
            ctx = "\n".join([f"[{x['source']}]: {x['content'][:200]}" for x in k])
            lang = "en"
            try: lang = detect(text)
            except: pass
            msgs = [{"role": "system", "content": SYSTEM_PROMPT + f"\nLang: {lang}. Reply in {lang}.\nKnowledge:\n{ctx}"}]
            msgs += self.history[-8:]
            msgs.append({"role": "user", "content": text})
            try:
                resp = ollama.chat(model=MODEL, messages=msgs)
                r = resp['message']['content']
            except Exception as e:
                r = f"Error: {e}"
            self.history.append({"role": "user", "content": text})
            self.history.append({"role": "assistant", "content": r})

        self.root.after(0, lambda: self._show(r))
        if self.voice.enabled:
            self.voice.speak(r)

    def _show(self, r):
        self.chat.insert("end", f"\n🔵 {AI}: {r}\n")
        self.chat.see("end")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    NovaApp().run()
