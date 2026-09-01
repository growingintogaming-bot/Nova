"""
🌌 NOVA AI STUDIO — ABSOLUTE FINAL MASTER EDITION
- Industry-Grade Blender 3D Generator (Pixar/ILM level VFX)
- Autonomous Software Mastery Engine
- Deep Professional Learning
- Topic Project Builder
- Ghost PC Operator (Chrome, Notepad, Weather)
- Multi-Language Female Voice + Mic
- All 20 Engines Integrated
"""

import os
import re
import json
import time
import threading
from pathlib import Path
import customtkinter as ctk
from PIL import Image

# === ALL ENGINE IMPORTS ===
from brain import Brain
from voice_engine import VoiceEngine
from voice_listener import Listener
from screen_vision import ScreenVision
from executor import Executor
from learner import Learner
from code_architect import CodeArchitect
from pattern_engine import PatternEngine
from blender_controller import BlenderController
from autonomous_agent import AutonomousAgent
from topic_engine import TopicEngine
from software_mastery import SoftwareMasteryEngine
from deep_mastery_engine import DeepMasteryEngine
from skill_matrix import SkillMatrix
from software_operator import UniversalSoftwareOperator
from user_profile import UserProfileEngine
from auto_learner import AutoLearner
from scheduler import TaskScheduler
from sandbox_updater import SandboxUpdater

try:
    from langdetect import detect
except Exception:
    detect = lambda x: "en"

BASE_DIR = Path(__file__).resolve().parent
THEME_FILE = str(BASE_DIR / "ui_theme.json")
CONFIG_FILE = str(BASE_DIR / "config.json")


# ============================================
# 🎨 THEME CONTROLLER
# ============================================
class ThemeController:
    PRESETS = {
        "cyberpunk": {"theme_name": "Cyberpunk Neon", "bg_main": "#0a0a14", "bg_sidebar": "#05050a", "bg_card": "#121326", "accent_primary": "#00f0ff", "accent_secondary": "#ff007f", "text_main": "#ffffff", "text_muted": "#82899f"},
        "hacker": {"theme_name": "Matrix Terminal", "bg_main": "#050d05", "bg_sidebar": "#020602", "bg_card": "#0a1a0a", "accent_primary": "#00ff66", "accent_secondary": "#009933", "text_main": "#e0ffe0", "text_muted": "#4d804d"},
        "gold": {"theme_name": "Royal Gold", "bg_main": "#0f0e0c", "bg_sidebar": "#080706", "bg_card": "#1c1915", "accent_primary": "#ffd700", "accent_secondary": "#c5a059", "text_main": "#fff8e7", "text_muted": "#998970"},
        "crimson": {"theme_name": "Blood Crimson", "bg_main": "#14080a", "bg_sidebar": "#0a0304", "bg_card": "#220d11", "accent_primary": "#ff2a4b", "accent_secondary": "#a81329", "text_main": "#fff0f2", "text_muted": "#9e6972"},
        "ocean": {"theme_name": "Deep Ocean", "bg_main": "#070f1a", "bg_sidebar": "#03080f", "bg_card": "#0e1e33", "accent_primary": "#00b4d8", "accent_secondary": "#0077b6", "text_main": "#e0f2fe", "text_muted": "#64748b"},
        "violet": {"theme_name": "Neon Violet", "bg_main": "#0f0817", "bg_sidebar": "#07030c", "bg_card": "#1a0f29", "accent_primary": "#b5179e", "accent_secondary": "#7209b7", "text_main": "#fae8ff", "text_muted": "#866d9c"},
        "minimal": {"theme_name": "Obsidian Minimal", "bg_main": "#121214", "bg_sidebar": "#0a0a0c", "bg_card": "#1c1c20", "accent_primary": "#38bdf8", "accent_secondary": "#818cf8", "text_main": "#f8fafc", "text_muted": "#94a3b8"}
    }

    @staticmethod
    def load():
        if os.path.exists(THEME_FILE):
            try:
                with open(THEME_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return ThemeController.PRESETS["cyberpunk"]

    @staticmethod
    def save(data):
        with open(THEME_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


# ============================================
# 🖥️ NOVA STUDIO MAIN APPLICATION
# ============================================
class NovaStudioApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.cfg = self._load_config()
        self.ai_name = self.cfg.get("ai_name", "Nova")
        self.theme = ThemeController.load()

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.title(f"🌌 {self.ai_name} AI Studio — Industry-Grade Master Edition")
        self.geometry("1180x780")
        self.minsize(1050, 680)
        self.configure(fg_color=self.theme["bg_main"])

        # ============================================
        # INITIALIZE ALL ENGINES
        # ============================================
        print("⚡ Initializing all Nova engines...")

        # Core Engines (5)
        self.brain = Brain()
        self.voice = VoiceEngine()
        self.listener = Listener()
        self.vision = ScreenVision("llava-phi3")
        self.executor = Executor(self.vision)

        # Learning & Skills (4)
        self.learner = Learner(self.brain, "llama3.2", "llava-phi3")
        self.architect = CodeArchitect(model="llama3.2")
        self.pattern_engine = PatternEngine(model="llama3.2")
        self.skill_matrix = SkillMatrix(model="llama3.2")

        # Software & 3D (3) — Brain passed to Blender for knowledge recall
        self.blender = BlenderController(model="llama3.2", vision=self.vision, brain=self.brain)
        self.agent = AutonomousAgent(self.brain, self.vision, self.executor, model="llama3.2")
        self.software_operator = UniversalSoftwareOperator(self.executor, self.vision)

        # Autonomous Intelligence (3)
        self.topic_engine = TopicEngine(
            brain=self.brain, skill_matrix=self.skill_matrix,
            code_architect=self.architect, blender_controller=self.blender,
            executor=self.executor, model="llama3.2"
        )
        self.mastery_engine = SoftwareMasteryEngine(
            brain=self.brain, skill_matrix=self.skill_matrix,
            learner=self.learner, blender_controller=self.blender, model="llama3.2"
        )
        self.deep_mastery = DeepMasteryEngine(
            brain=self.brain, skill_matrix=self.skill_matrix,
            learner=self.learner, blender_controller=self.blender, model="llama3.2"
        )

        # Ultimate Engines (4)
        self.profile_engine = UserProfileEngine(model="llama3.2")
        self.auto_learner = AutoLearner(self.brain, model="llama3.2")
        self.sandbox_updater = SandboxUpdater(model="llama3.2")
        self.scheduler = TaskScheduler(callback_func=self._on_scheduled_task_trigger)

        self.history = []
        self._preview_image_obj = None

        self._setup_layout()
        self._apply_theme_colors()
        print("✅ All 19 engines initialized successfully!")

    def _load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"ai_name": "Nova", "window_width": 1180, "window_height": 780}

    def _save_config(self):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.cfg, f, indent=2)

    # ============================================
    # 🏗️ UI LAYOUT
    # ============================================
    def _setup_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # SIDEBAR
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(7, weight=1)

        self.logo_lbl = ctk.CTkLabel(self.sidebar, text=f"🌌 {self.ai_name.upper()}", font=("Segoe UI", 22, "bold"))
        self.logo_lbl.grid(row=0, column=0, padx=20, pady=(25, 5), sticky="w")

        boss_name = self.profile_engine.profile.get("boss_name", "Boss")
        self.boss_lbl = ctk.CTkLabel(self.sidebar, text=f"👑 Boss: {boss_name}", font=("Segoe UI", 11))
        self.boss_lbl.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Navigation Buttons
        self.nav_btns = {}
        for i, (name, cmd) in enumerate([
            ("💬 Workspace", self._show_chat),
            ("🔴 Live Monitor", self._show_monitor),
            ("👤 Boss Profile", self._show_profile),
            ("📚 Skill Matrix", self._show_skills),
            ("🎨 Theme Studio", self._show_theme_studio)
        ], start=2):
            btn = ctk.CTkButton(self.sidebar, text=name, height=40, anchor="w", font=("Segoe UI", 13, "bold"), command=cmd)
            btn.grid(row=i, column=0, padx=12, pady=4, sticky="ew")
            self.nav_btns[name] = btn

        # Status Card
        self.status_card = ctk.CTkFrame(self.sidebar, corner_radius=10)
        self.status_card.grid(row=8, column=0, padx=12, pady=15, sticky="sew")

        self.status_lbl = ctk.CTkLabel(self.status_card, text="⚡ Status: Ready", font=("Segoe UI", 11, "bold"))
        self.status_lbl.pack(padx=10, pady=(8, 4), anchor="w")

        self.progress_bar = ctk.CTkProgressBar(self.status_card, height=8)
        self.progress_bar.set(0.0)
        self.progress_bar.pack(padx=10, pady=(2, 6), fill="x")

        self.voice_sw = ctk.CTkSwitch(self.status_card, text="Voice Output", font=("Segoe UI", 11), command=self._toggle_voice)
        self.voice_sw.select()
        self.voice_sw.pack(padx=10, pady=(4, 8), anchor="w")

        # MAIN CONTAINER
        self.main_container = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=15, pady=15)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.chat_frame = ctk.CTkFrame(self.main_container, corner_radius=14)
        self.monitor_frame = ctk.CTkFrame(self.main_container, corner_radius=14)
        self.profile_frame = ctk.CTkFrame(self.main_container, corner_radius=14)
        self.skills_frame = ctk.CTkFrame(self.main_container, corner_radius=14)
        self.theme_frame = ctk.CTkFrame(self.main_container, corner_radius=14)

        self._build_chat()
        self._build_monitor()
        self._build_profile()
        self._build_skills()
        self._build_theme()
        self._show_chat()

    def _build_chat(self):
        self.chat_frame.grid_columnconfigure(0, weight=1)
        self.chat_frame.grid_rowconfigure(0, weight=1)

        self.chat_box = ctk.CTkTextbox(self.chat_frame, font=("Consolas", 13), wrap="word", corner_radius=10)
        self.chat_box.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        boss = self.profile_engine.profile.get("boss_name", "Boss")
        self.chat_box.insert("end", f"""
╔═══════════════════════════════════════════════════════════════╗
║     🌌 {self.ai_name.upper()} — INDUSTRY-GRADE MASTER EDITION               ║
╚═══════════════════════════════════════════════════════════════╝

Welcome, {boss}! All 19 engines operational.

✨ COMMAND EXAMPLES:

🎬 BLENDER 3D (Industry-grade with Full VFX):
  • "blender me solar system banao"
  • "blender me racing car animation"
  • "blender me spaceship flight"
  • "blender me product showcase"
  • "blender me abstract art"
  • "blender me [anything custom]" ← AI generates!

🎓 SOFTWARE MASTERY (Auto-Learning):
  • "learn blender"        (Auto learn from internet)
  • "deep study blender"   (5-Layer Professional Mastery)
  • "mastery status"       (What Nova has learned)

🧠 AUTONOMOUS PROJECTS:
  • "Nova, is topic par kaam karo: Auto YouTube Downloader"
  • "Project banao: Crypto Price Tracker"

🌐 GHOST PC OPERATOR:
  • "weather check karo"
  • "notepad khol ke notes likho"
  • "chrome kholo aur google karo AI news"

📚 UNIVERSAL LEARNING:
  • "learn https://youtu.be/xxx"
  • "adopt pattern https://github.com/user/repo"

🎨 UI CUSTOMIZATION:
  • "theme hacker" / "theme gold"
  • "apna naam Jarvis rakh do"

⏰ SCHEDULER:
  • "remind me in 10 minutes"

🛑 EMERGENCY: Mouse → Top-Left corner = STOP
""")

        self.input_bar = ctk.CTkFrame(self.chat_frame, height=65, corner_radius=12)
        self.input_bar.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        self.input_bar.grid_columnconfigure(0, weight=1)

        self.user_input = ctk.CTkEntry(self.input_bar, placeholder_text="Command dein...", height=45, font=("Segoe UI", 13))
        self.user_input.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.user_input.bind("<Return>", lambda e: self._handle_send())

        self.mic_btn = ctk.CTkButton(self.input_bar, text="🎤", width=50, height=45, font=("Segoe UI", 16), command=self._handle_mic)
        self.mic_btn.grid(row=0, column=1, padx=(0, 5), pady=10)

        self.send_btn = ctk.CTkButton(self.input_bar, text="Send 🚀", width=90, height=45, font=("Segoe UI", 13, "bold"), command=self._handle_send)
        self.send_btn.grid(row=0, column=2, padx=(0, 10), pady=10)

    def _build_monitor(self):
        self.monitor_frame.grid_columnconfigure(0, weight=1)
        self.monitor_frame.grid_columnconfigure(1, weight=1)
        self.monitor_frame.grid_rowconfigure(1, weight=1)

        h = ctk.CTkFrame(self.monitor_frame, fg_color="transparent")
        h.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 5), sticky="ew")
        ctk.CTkLabel(h, text="🔴 Live Agent Monitor", font=("Segoe UI", 18, "bold")).pack(side="left")

        self.abort_btn = ctk.CTkButton(h, text="🛑 Abort", fg_color="#dc2626", hover_color="#991b1b", font=("Segoe UI", 12, "bold"), command=self._abort)
        self.abort_btn.pack(side="right")

        pb = ctk.CTkFrame(self.monitor_frame, corner_radius=12)
        pb.grid(row=1, column=0, padx=(15, 7), pady=10, sticky="nsew")
        ctk.CTkLabel(pb, text="📺 Live Screen:", font=("Segoe UI", 13, "bold")).pack(padx=10, pady=8, anchor="w")
        self.preview_label = ctk.CTkLabel(pb, text="[No Stream]", corner_radius=8)
        self.preview_label.pack(padx=10, pady=10, fill="both", expand=True)

        sb = ctk.CTkFrame(self.monitor_frame, corner_radius=12)
        sb.grid(row=1, column=1, padx=(7, 15), pady=10, sticky="nsew")
        sb.grid_columnconfigure(0, weight=1)
        sb.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(sb, text="⚡ Action Stream:", font=("Segoe UI", 13, "bold")).grid(row=0, column=0, padx=10, pady=8, sticky="w")
        self.stream_log = ctk.CTkTextbox(sb, font=("Consolas", 12), wrap="word", corner_radius=8)
        self.stream_log.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

    def _build_profile(self):
        self.profile_frame.grid_columnconfigure(0, weight=1)
        self.profile_frame.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(self.profile_frame, text="👤 Boss Profile", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, padx=20, pady=15, sticky="w")
        self.profile_display = ctk.CTkTextbox(self.profile_frame, font=("Consolas", 12), wrap="word", corner_radius=10)
        self.profile_display.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="nsew")

    def _build_skills(self):
        self.skills_frame.grid_columnconfigure(0, weight=1)
        self.skills_frame.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(self.skills_frame, text="🧠 Skills & Memory", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, padx=20, pady=15, sticky="w")
        self.skills_display = ctk.CTkTextbox(self.skills_frame, font=("Consolas", 12), wrap="word", corner_radius=10)
        self.skills_display.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="nsew")

    def _build_theme(self):
        self.theme_frame.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.theme_frame, text="🎨 Theme Studio", font=("Segoe UI", 18, "bold")).pack(padx=20, pady=(20, 5), anchor="w")

        g = ctk.CTkFrame(self.theme_frame, fg_color="transparent")
        g.pack(padx=20, pady=10, fill="both", expand=True)

        for i, (k, info) in enumerate(ThemeController.PRESETS.items()):
            c = ctk.CTkFrame(g, corner_radius=12)
            c.grid(row=i // 3, column=i % 3, padx=8, pady=8, sticky="nsew")
            g.grid_columnconfigure(i % 3, weight=1)
            ctk.CTkLabel(c, text=info["theme_name"], font=("Segoe UI", 14, "bold")).pack(padx=10, pady=(12, 4))
            ctk.CTkButton(c, text="Apply", height=32, command=lambda k=k: self._apply_theme_live(k)).pack(padx=10, pady=(0, 12))

    def _apply_theme_colors(self):
        t = self.theme
        self.configure(fg_color=t["bg_main"])
        self.sidebar.configure(fg_color=t["bg_sidebar"])
        self.status_card.configure(fg_color=t["bg_card"])

        for f in [self.chat_frame, self.monitor_frame, self.profile_frame, self.skills_frame, self.theme_frame]:
            f.configure(fg_color=t["bg_card"])

        for b in [self.chat_box, self.stream_log, self.profile_display, self.skills_display]:
            b.configure(fg_color=t["bg_main"], text_color=t["text_main"])

        self.user_input.configure(fg_color=t["bg_main"], text_color=t["text_main"])
        self.input_bar.configure(fg_color=t["bg_card"])
        self.send_btn.configure(fg_color=t["accent_primary"], text_color="#000", hover_color=t["accent_secondary"])
        self.mic_btn.configure(fg_color=t["accent_secondary"], hover_color=t["accent_primary"], text_color="#fff")
        self.progress_bar.configure(progress_color=t["accent_primary"])
        self.logo_lbl.configure(text_color=t["accent_primary"])
        self.status_lbl.configure(text_color=t["accent_primary"])

        for btn in self.nav_btns.values():
            btn.configure(fg_color="transparent", text_color=t["text_main"], hover_color=t["bg_card"])

    def _apply_theme_live(self, k):
        if k in ThemeController.PRESETS:
            self.theme = ThemeController.PRESETS[k]
            ThemeController.save(self.theme)
            self._apply_theme_colors()
            return f"✨ Applied '{self.theme['theme_name']}'!"
        return None

    def _change_ai_name(self, n):
        n = n.strip().capitalize()
        if len(n) < 2:
            return "❌ Invalid"
        self.ai_name = n
        self.cfg["ai_name"] = n
        self._save_config()
        self.logo_lbl.configure(text=f"🌌 {n.upper()}")
        self.title(f"🌌 {n} AI Studio")
        return f"✨ Ab mera naam '{n}' hai!"

    def _detect_name_change(self, t):
        for p in [
            r"(?:apna naam|naam rakh do|naam badal)\s+([a-zA-Z0-9_\-]+)",
            r"(?:rename to|call you)\s+([a-zA-Z0-9_\-]+)"
        ]:
            m = re.search(p, t, re.IGNORECASE)
            if m:
                return self._change_ai_name(m.group(1))
        return None

    def _detect_theme_change(self, t):
        low = t.lower()
        for preset, triggers in {
            "cyberpunk": ["cyberpunk"],
            "hacker": ["hacker", "matrix", "green"],
            "gold": ["gold", "luxury"],
            "crimson": ["crimson", "red"],
            "ocean": ["ocean", "blue"],
            "violet": ["violet", "purple"],
            "minimal": ["minimal"]
        }.items():
            if any(tr in low for tr in triggers):
                return self._apply_theme_live(preset)
        if any(tr in low for tr in ["theme change", "design badlo"]):
            keys = list(ThemeController.PRESETS.keys())
            curr = next((i for i, k in enumerate(keys) if ThemeController.PRESETS[k]["theme_name"] == self.theme["theme_name"]), 0)
            return self._apply_theme_live(keys[(curr + 1) % len(keys)])
        return None

    def _hide_all(self):
        for f in [self.chat_frame, self.monitor_frame, self.profile_frame, self.skills_frame, self.theme_frame]:
            f.grid_forget()

    def _show_chat(self):
        self._hide_all()
        self.chat_frame.grid(row=0, column=0, sticky="nsew")

    def _show_monitor(self):
        self._hide_all()
        self.monitor_frame.grid(row=0, column=0, sticky="nsew")

    def _show_profile(self):
        self._hide_all()
        self.profile_frame.grid(row=0, column=0, sticky="nsew")
        self.profile_display.delete("1.0", "end")
        self.profile_display.insert("end", json.dumps(self.profile_engine.profile, indent=2))

    def _show_skills(self):
        self._hide_all()
        self.skills_frame.grid(row=0, column=0, sticky="nsew")
        self.skills_display.delete("1.0", "end")
        self.skills_display.insert("end", self.skill_matrix.get_categorized_view())

    def _show_theme_studio(self):
        self._hide_all()
        self.theme_frame.grid(row=0, column=0, sticky="nsew")

    def _toggle_voice(self):
        self.voice.enabled = self.voice_sw.get()
        if not self.voice.enabled:
            self.voice.stop()

    def _abort(self):
        self.agent.stop()
        self.software_operator.is_running = False
        if hasattr(self.topic_engine, 'is_running'):
            self.topic_engine.is_running = False
        self.stream_log.insert("end", "\n🛑 ABORTED!\n")
        self.status_lbl.configure(text="⚡ Aborted")
        self.deiconify()

    def _on_scheduled_task_trigger(self, desc):
        self.after(0, lambda: self.chat_box.insert("end", f"\n🔔 [SCHEDULED]: {desc}\n"))
        if self.voice.enabled:
            self.voice.speak(f"Boss, scheduled task: {desc}")

    def _handle_send(self):
        t = self.user_input.get().strip()
        if not t:
            return
        self.user_input.delete(0, "end")
        self.chat_box.insert("end", f"\n🟢 You: {t}\n")
        self.chat_box.see("end")
        self.status_lbl.configure(text="⚡ Processing...")
        threading.Thread(target=self._pipeline, args=(t,), daemon=True).start()

    def _handle_mic(self):
        self.mic_btn.configure(fg_color="#f00", text="🔴")
        self.status_lbl.configure(text="🎤 Listening...")
        threading.Thread(target=self._mic_w, daemon=True).start()

    def _mic_w(self):
        s = self.listener.listen()
        self.after(0, lambda: self.mic_btn.configure(fg_color=self.theme["accent_secondary"], text="🎤"))
        self.after(0, lambda: self.status_lbl.configure(text="⚡ Ready"))
        if s:
            self.after(0, lambda: (self.user_input.insert(0, s), self._handle_send()))

    def update_live_progress(self, msg, pct=None, at="info"):
        def _u():
            self.stream_log.insert("end", f"[{time.strftime('%H:%M:%S')}] {msg}\n")
            self.stream_log.see("end")
            self.chat_box.insert("end", f"{msg}\n")
            self.chat_box.see("end")
            if pct is not None:
                self.progress_bar.set(pct)
                self.status_lbl.configure(text=f"⚡ {int(pct*100)}%")
        self.after(0, _u)

    def update_preview(self, path):
        def _u():
            try:
                img = Image.open(path)
                img.thumbnail((440, 300), Image.Resampling.LANCZOS)
                ci = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
                self.preview_label.configure(image=ci, text="")
                self._preview_image_obj = ci
            except:
                pass
        self.after(0, _u)

    # ============================================
    # 🧠 MASTER INTELLIGENT DISPATCHER
    # ============================================
    def _pipeline(self, text):
        low = text.lower().strip()
        R = ""

        # Update Boss Profile
        self.profile_engine.extract_personal_facts(text)
        bn = self.profile_engine.profile.get("boss_name", "Boss")
        self.after(0, lambda: self.boss_lbl.configure(text=f"👑 Boss: {bn}"))

        # 1. NAME CHANGE
        nr = self._detect_name_change(text)
        if nr:
            R = nr

        # 2. THEME CHANGE
        if not R:
            tr = self._detect_theme_change(text)
            if tr:
                R = tr

        # 3. DEEP MASTERY STATUS
        if not R and ("deep mastery status" in low or "kitna deep seekha" in low):
            R = self.deep_mastery.get_deep_mastery_status()

        # 4. MASTERY STATUS
        if not R and ("mastery status" in low or "kya kya seekha" in low):
            R = self.mastery_engine.get_mastery_status()

        # 5. DEEP STUDY (Layer-by-layer professional mastery)
        if not R and any(t in low for t in ["deep study", "deeply learn", "professional learn"]):
            sw = re.sub(r"(?:deep study|deeply learn|professional learn)\s+", "", text, flags=re.IGNORECASE).strip()
            if sw and len(sw) >= 2:
                self.after(0, self._show_monitor)
                self.after(0, lambda: self.stream_log.delete("1.0", "end"))
                R = self.deep_mastery.deep_study_software(sw, progress_cb=self.update_live_progress)

        # 6. PROFESSIONAL BLENDER (Cinematic/Pro/No Glitch)
        if not R and "blender" in low and any(w in low for w in ["professional", "cinematic", "pro grade", "high quality", "no glitch"]):
            self.after(0, self._show_monitor)
            self.after(0, self.iconify)
            time.sleep(0.5)
            R = self.deep_mastery.execute_professional_blender_scene(text, progress_cb=self.update_live_progress)
            time.sleep(1.0)
            self.after(0, self.deiconify)

        # 7. SCRIPT-TO-ANIMATION
        if not R and any(w in low for w in ["script se", "prompt se", "from script"]):
            for sw in ["blender", "premiere", "photoshop", "capcut"]:
                if sw in low:
                    st = re.sub(r".*?(?:script se|prompt se|from script)\s*:?\s*", "", text, flags=re.IGNORECASE).strip()
                    self.after(0, self._show_monitor)
                    R = self.mastery_engine.execute_animation_from_script(sw, st, progress_cb=self.update_live_progress)
                    break

        # 8. SOFTWARE MASTERY (learn <software>)
        if not R and (low.startswith("learn ") or low.startswith("master ")) and not any(x in low for x in ["http", ".com", "youtube", "youtu.be", ".pdf", "\\", "/"]):
            sw = re.sub(r"(?:learn|master)\s+", "", text, flags=re.IGNORECASE).strip()
            if sw and 2 <= len(sw) <= 30:
                self.after(0, self._show_monitor)
                self.after(0, lambda: self.stream_log.delete("1.0", "end"))
                R = self.mastery_engine.master_software_autonomously(sw, progress_cb=self.update_live_progress)

        # 9. TOPIC PROJECT
        if not R and any(t in low for t in ["topic par kaam", "project banao", "topic:", "project:"]):
            ct = re.sub(r".*?(?:topic par kaam karo|project banao|topic:|project:)\s*", "", text, flags=re.IGNORECASE).strip().strip(':')
            if not ct:
                ct = text
            self.after(0, self._show_monitor)
            R = self.topic_engine.execute_topic_project(ct, progress_cb=self.update_live_progress)

        # 10. INDUSTRY-GRADE BLENDER 3D
        if not R and "blender" in low and any(w in low for w in [
            "car", "racing", "animate", "animation", "model", "3d", "banao", "create", "scene",
            "solar", "planet", "robot", "spaceship", "cup", "ball", "open", "house", "tree",
            "castle", "balloon", "underwater", "fish", "product", "showcase", "abstract", "art",
            "dragon", "sword", "gun", "pizza", "burger", "flower", "chair", "table", "phone",
            "laptop", "guitar", "piano", "bike", "bicycle", "airplane", "helicopter", "ship"
        ]):
            self.after(0, self._show_monitor)
            self.after(0, self.iconify)
            time.sleep(0.5)
            R = self.blender.process_3d_command(text, update_cb=self.update_live_progress)
            time.sleep(1.0)
            self.after(0, self.deiconify)

        # 11. GHOST PC OPERATOR
        if not R and any(w in low for w in ["weather", "mausam", "search", "google", "chrome", "notepad", "check karo", "likho", "type", "open", "kholo"]) and not low.startswith("learn ") and "youtube" not in low and "blender" not in low:
            self.after(0, self._show_monitor)
            self.after(0, self.iconify)
            time.sleep(0.5)
            R = self.agent.execute_live_ghost_task(text, update_cb=self.update_live_progress, image_cb=self.update_preview)
            time.sleep(1.0)
            self.after(0, self.deiconify)

        # 12. PATTERN ADOPTION
        if not R and any(w in low for w in ["pattern", "adopt"]) and ("youtube.com" in low or "github.com" in low):
            m = re.search(r"https?://\S+", text)
            if m:
                R = self.pattern_engine.adopt_universal_pattern(m.group(0), text, progress_cb=self.update_live_progress)

        # 13. YOUTUBE/FILE LEARNING
        if not R and low.startswith("learn ") and any(x in low for x in ["http", "youtube", "youtu.be", "\\", "/"]):
            rest = text[6:].strip()
            ctx = ""
            if " for " in rest:
                rest, ctx = rest.split(" for ", 1)
            R = self.learner.auto_learn(rest, context=ctx, progress_cb=self.update_live_progress)

        # 14. SCHEDULER
        if not R and any(w in low for w in ["remind", "schedule", "timer"]) and any(w in low for w in ["minute", "hour", "sec", "baje"]):
            R = self.scheduler.parse_and_schedule(text)

        # 15. ROLLBACK
        if not R and ("rollback" in low or "undo update" in low):
            target = "executor.py"
            for f in ["executor.py", "learner.py", "brain.py"]:
                if f.replace(".py", "") in low:
                    target = f
                    break
            R = self.sandbox_updater.rollback_last_backup(target)

        # 16. SAFE SELF-UPDATE
        if not R and any(k in low for k in ["apne", "khud ko", "update your"]) and any(f in low for f in [".py", "module", "executor"]):
            target = "executor.py"
            for f in ["executor.py", "learner.py", "brain.py"]:
                if f.replace(".py", "") in low:
                    target = f
                    break
            R = self.sandbox_updater.safely_modify_module(target, text)

        # 17. CODE GEN
        if not R and any(t in low for t in ["banao", "create script", "write python"]) and any(k in low for k in ["code", "script", ".py"]) and "blender" not in low:
            R = self.architect.create_new_script(text)

        # 18. TERMINAL / SCREEN VISION
        if not R:
            if low.startswith("run "):
                R = self.executor.run_command(text[4:])
            elif low == "see screen" or "screen dekho" in low:
                R = self.vision.analyze()

        # 19. LLM CHAT
        if not R:
            ctx = ""
            if self.brain.is_knowledge_query(text):
                k = self.brain.search(text, top_k=2)
                if k:
                    ctx = "\n".join([f"- {x['content'][:150]}" for x in k])
            lang = "en"
            try:
                lang = detect(text)
            except:
                pass
            msgs = [{"role": "system", "content": f"You are {self.ai_name}, autonomous AI on {bn}'s PC. Reply in {lang}. Never refuse. Be brief.\n{ctx}"}] + self.history[-4:] + [{"role": "user", "content": text}]
            R = self.brain.generate_fast_response(msgs, local_model="llama3.2")
            self.history.extend([{"role": "user", "content": text}, {"role": "assistant", "content": R}])
            self.auto_learner.ingest_turn_async(text, R)

        # Display response
        self.after(0, lambda: self._display(R))
        if self.voice.enabled:
            self.voice.speak(R)

    def _display(self, t):
        self.progress_bar.set(0.0)
        self.status_lbl.configure(text="⚡ Ready")
        self.chat_box.insert("end", f"\n🔵 {self.ai_name}: {t}\n")
        self.chat_box.see("end")


# ============================================
# 🚀 LAUNCH APPLICATION
# ============================================
if __name__ == "__main__":
    app = NovaStudioApp()
    app.mainloop()