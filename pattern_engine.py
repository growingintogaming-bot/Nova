"""
🧬 NOVA UNIVERSAL PATTERN ENGINE (Ultra-Fast & No-Freeze Edition)
- 2-Second YouTube Transcript Fetcher
- Fast 'tiny' Whisper Fallback (No CPU hanging)
- GitHub Architecture Cloner
"""

import os
import re
import json
import shutil
import zipfile
import urllib.request
import ssl
import subprocess
from pathlib import Path
import ollama

ssl._create_default_https_context = ssl._create_unverified_context

BASE_DIR = Path(__file__).resolve().parent
REPO_DIR = BASE_DIR / "data" / "github_repos"
YT_DIR = BASE_DIR / "data" / "youtube_courses"
PATTERNS_DIR = BASE_DIR / "data" / "patterns"
ACTIVE_PATTERN_FILE = PATTERNS_DIR / "active_pattern.json"

REPO_DIR.mkdir(parents=True, exist_ok=True)
YT_DIR.mkdir(parents=True, exist_ok=True)
PATTERNS_DIR.mkdir(parents=True, exist_ok=True)


class PatternEngine:
    def __init__(self, model="llama3.2"):
        self.model = model

    def adopt_universal_pattern(self, url: str, custom_instruction: str = "", progress_cb=None) -> str:
        url = url.strip().strip('"').strip("'")

        if "youtube.com" in url or "youtu.be" in url:
            return self._adopt_youtube_pattern(url, custom_instruction, progress_cb)
        elif "github.com" in url:
            return self._adopt_github_pattern(url, custom_instruction, progress_cb)
        else:
            return "❌ Unsupported link. Please provide a GitHub repo or YouTube guide URL."

    # ============================================
    # 🎥 FAST YOUTUBE STEP-BY-STEP PATTERN ADOPTER
    # ============================================
    def _extract_youtube_id(self, url: str) -> str:
        match = re.search(r'(?:v=|\/|youtu\.be\/)([0-9A-Za-z_-]{11})', url)
        return match.group(1) if match else None

    def _adopt_youtube_pattern(self, yt_url: str, custom_instruction: str, progress_cb=None) -> str:
        def notify(msg, pct):
            if progress_cb:
                progress_cb(msg, pct)

        notify("🚀 [15%] YouTube guide fetch shuru ho raha hai...", 0.15)
        video_id = self._extract_youtube_id(yt_url)
        transcript = ""
        title = "YouTube Video Guide"

        # --- METHOD 1: 2-Second Instant Transcript API (NO CPU LOAD) ---
        if video_id:
            try:
                notify("⚡ [30%] Online subtitles/transcript fetch ho raha hai (Fast Mode)...", 0.30)
                from youtube_transcript_api import YouTubeTranscriptApi
                
                # Fetch English, Urdu, or Hindi transcripts
                transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'ur', 'hi', 'en-US'])
                transcript = " ".join([item['text'] for item in transcript_list])[:5000]
                notify("✅ [65%] Transcript 2 seconds mein fetch ho gaya!", 0.65)
            except Exception:
                pass  # Fallback to local audio below

        # --- METHOD 2: Fast Whisper 'tiny' Fallback ---
        if not transcript:
            notify("📥 [35%] Audio stream download ho rahi hai...", 0.35)
            import yt_dlp
            target_dir = YT_DIR / f"pattern_temp_{int(os.getpid())}"
            target_dir.mkdir(parents=True, exist_ok=True)

            opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(target_dir / 'audio.%(ext)s'),
                'quiet': True,
                'no_warnings': True
            }

            try:
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(yt_url, download=True)
                    title = info.get('title', 'YouTube Guide')
            except Exception as e:
                shutil.rmtree(target_dir, ignore_errors=True)
                notify(f"❌ Download error: {e}", 0.0)
                return f"❌ YouTube download failed: {e}"

            notify("🎙️ [55%] Fast Whisper (tiny) se audio extract ho rahi hai...", 0.55)
            audio_files = list(target_dir.glob("audio.*"))
            if audio_files:
                try:
                    # Cut audio to first 6 minutes for ultra-fast processing
                    fast_audio = str(target_dir / "fast_audio.wav")
                    subprocess.run(
                        f'ffmpeg -i "{str(audio_files[0])}" -t 360 -vn -acodec pcm_s16le -ar 16000 -ac 1 "{fast_audio}" -y -loglevel error',
                        shell=True, capture_output=True
                    )
                    
                    import whisper
                    # Using 'tiny' model - 5x faster than 'base' on CPU!
                    m = whisper.load_model("tiny")
                    res = m.transcribe(fast_audio if os.path.exists(fast_audio) else str(audio_files[0]), fp16=False)
                    transcript = res.get('text', '')[:4000]
                except Exception as e:
                    print(f"Whisper fallback note: {e}")

            shutil.rmtree(target_dir, ignore_errors=True)

        if not transcript:
            notify("❌ Transcript extract nahi ho saka.", 0.0)
            return "❌ Could not extract text from video. Please check URL."

        # --- STEP 3: Extract Step-by-Step Blueprint via LLM ---
        notify("🧠 [80%] Step-by-Step workflow rules extract ho rahe hain...", 0.80)
        prompt = (
            "Extract the exact STEP-BY-STEP execution workflow, rules, and methodology from this tutorial transcript.\n\n"
            f"GUIDE: {title}\n"
            f"INSTRUCTION: {custom_instruction}\n"
            f"TRANSCRIPT:\n{transcript}\n\n"
            "Return ONLY a clean JSON object:\n"
            "{\n"
            f'    "pattern_name": "{title[:30]} Blueprint",\n'
            '    "description": "Step-by-step workflow adopted from YouTube guide",\n'
            '    "response_style": "How Nova should structure replies following this exact guide",\n'
            '    "step_by_step_rules": "Core steps (Step 1, Step 2, Step 3) taught in the video",\n'
            '    "system_prompt_addon": "You must strictly follow this methodology: [Summary of the exact steps to follow]"\n'
            "}"
        )

        try:
            resp = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.2, "num_ctx": 2048}
            )
            raw = resp['message']['content']
            start = raw.find('{')
            end = raw.rfind('}') + 1
            pattern_json = json.loads(raw[start:end])

            # Save
            notify("💾 [95%] Active Workflow profile mein save ho raha hai...", 0.95)
            with open(ACTIVE_PATTERN_FILE, "w", encoding="utf-8") as f:
                json.dump(pattern_json, f, indent=2)

            notify("🎉 [100%] Guide successfully adopted as active workflow!", 1.0)

            return (
                "\n╔══════════════════════════════════════════════════════════════╗\n"
                "║     🎬 YOUTUBE GUIDE STEP-BY-STEP PATTERN ADOPTED!           ║\n"
                "╚══════════════════════════════════════════════════════════════╝\n"
                f"📹 Guide: {title}\n"
                f"📋 Workflow: {pattern_json.get('pattern_name')}\n"
                f"📝 Summary: {pattern_json.get('description')}\n\n"
                "✨ Nova ne is video ka exact step-by-step tareeqa adopt kar liya hai!"
            )

        except Exception as e:
            notify(f"❌ Analysis error: {e}", 0.0)
            return f"❌ Pattern extraction error: {e}"

    # ============================================
    # 🐙 GITHUB ARCHITECTURE PATTERN ADOPTER
    # ============================================
    def _adopt_github_pattern(self, github_url: str, custom_instruction: str, progress_cb=None) -> str:
        def notify(msg, pct):
            if progress_cb:
                progress_cb(msg, pct)

        repo_name = github_url.rstrip("/").split("/")[-1].replace(".git", "")
        target_path = REPO_DIR / repo_name

        notify(f"🚀 [15%] GitHub repo pipeline start: {repo_name}...", 0.15)

        cloned = False
        try:
            if target_path.exists():
                shutil.rmtree(target_path)
            subprocess.run(f'git clone --depth 1 "{github_url}" "{target_path}"', shell=True, check=True, capture_output=True)
            cloned = True
            notify("📥 [35%] Git repository cloned!", 0.35)
        except Exception:
            notify("⚠️ [25%] Direct ZIP fallback download...", 0.25)
            cloned = self._download_github_zip(github_url, target_path, progress_cb)

        if not cloned or not target_path.exists():
            notify("❌ [0%] Download fail ho gaya.", 0.0)
            return f"❌ Download failed for: {github_url}"

        notify("🔍 [55%] Architecture scan ho rahi hai...", 0.55)
        summary_content = ""
        for readme_name in ["README.md", "readme.md", "README.txt"]:
            readme = target_path / readme_name
            if readme.exists():
                try:
                    with open(readme, "r", encoding="utf-8", errors="ignore") as f:
                        summary_content += "--- CORE DOCS ---\n" + f.read()[:2000] + "\n"
                        break
                except:
                    pass

        summary_content = summary_content[:3000]

        notify("🧠 [80%] Cognitive style extract ho raha hai...", 0.80)
        prompt = (
            "Extract the thinking style, personality, and instructions from this repo summary as JSON.\n\n"
            f"REPO: {repo_name}\n"
            f"CONTEXT:\n{summary_content}\n\n"
            "Return ONLY clean JSON:\n"
            "{\n"
            f'    "pattern_name": "{repo_name} Style",\n'
            '    "description": "One sentence summary of this style",\n'
            '    "response_style": "Short rules on how to speak and reason",\n'
            '    "code_rules": "Core code conventions",\n'
            '    "system_prompt_addon": "A 2-3 line prompt instruction embodying this repo\'s essence"\n'
            "}"
        )

        try:
            resp = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                options={"temperature": 0.2, "num_ctx": 2048}
            )
            raw = resp['message']['content']
            start = raw.find('{')
            end = raw.rfind('}') + 1
            pattern_json = json.loads(raw[start:end])

            notify("💾 [95%] Pattern profile save ho raha hai...", 0.95)
            pattern_file = PATTERNS_DIR / f"{repo_name}_pattern.json"
            with open(pattern_file, "w", encoding="utf-8") as f:
                json.dump(pattern_json, f, indent=2)

            with open(ACTIVE_PATTERN_FILE, "w", encoding="utf-8") as f:
                json.dump(pattern_json, f, indent=2)

            notify(f"🎉 [100%] Complete! '{repo_name}' pattern active!", 1.0)

            return (
                "\n╔══════════════════════════════════════════════════════════════╗\n"
                "║         🚀 GITHUB PATTERN ADOPTED SUCCESSFULLY!              ║\n"
                "╚══════════════════════════════════════════════════════════════╝\n"
                f"📦 Repository: {repo_name}\n"
                f"🎯 Pattern Name: {pattern_json.get('pattern_name')}\n"
                f"📝 Style: {pattern_json.get('description')}\n\n"
                f"✨ Nova ne '{repo_name}' ka pattern adopt kar liya hai!"
            )

        except Exception as e:
            notify(f"❌ Error: {e}", 0.0)
            return f"❌ Pattern extraction error: {e}"

    def _download_github_zip(self, github_url: str, target_path: Path, progress_cb=None) -> bool:
        try:
            clean_url = github_url.rstrip("/").replace(".git", "")
            parts = clean_url.split("/")
            if len(parts) < 5:
                return False
            owner, repo = parts[-2], parts[-1]
            zip_url = f"https://api.github.com/repos/{owner}/{repo}/zipball"
            zip_temp = REPO_DIR / f"{repo}_temp.zip"

            req = urllib.request.Request(zip_url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=30) as response, open(zip_temp, "wb") as f:
                f.write(response.read())

            with zipfile.ZipFile(zip_temp, "r") as z:
                z.extractall(REPO_DIR)

            for item in os.listdir(REPO_DIR):
                full_item = REPO_DIR / item
                if full_item.is_dir() and (owner in item.lower() or repo in item.lower()):
                    if target_path.exists():
                        shutil.rmtree(target_path)
                    shutil.move(str(full_item), str(target_path))
                    break

            if zip_temp.exists():
                os.remove(zip_temp)

            return target_path.exists()
        except Exception:
            return False

    @staticmethod
    def get_active_system_prompt_addon() -> str:
        if ACTIVE_PATTERN_FILE.exists():
            try:
                with open(ACTIVE_PATTERN_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return (
                        f"\n\n🔥 ACTIVE ADOPTED WORKFLOW/PATTERN ({data.get('pattern_name')}):\n"
                        f"{data.get('system_prompt_addon', '')}\n"
                        f"Rules/Steps: {data.get('step_by_step_rules', data.get('response_style', ''))}\n"
                    )
            except:
                pass
        return ""