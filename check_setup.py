import os
import sys
import subprocess
import importlib

# Colors for terminal
class C:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

if os.name == 'nt':
    os.system('color')

def check_cmd(cmd):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        return r.returncode == 0, r.stdout
    except:
        return False, ""

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{C.CYAN}{C.BOLD}╔══════════════════════════════════════════════════════════════╗{C.END}")
    print(f"{C.CYAN}{C.BOLD}║             🔍 NOVA AI - SYSTEM STATUS CHECKER               ║{C.END}")
    print(f"{C.CYAN}{C.BOLD}╚══════════════════════════════════════════════════════════════╝{C.END}\n")

    passed = 0
    total = 0

    # 1. PYTHON VERSION
    total += 1
    py_ver = sys.version.split()[0]
    print(f"{C.BOLD}1. PYTHON ENVIRONMENT:{C.END}")
    if sys.version_info.major == 3 and 9 <= sys.version_info.minor <= 12:
        print(f"   {C.GREEN}✅ Python Version: {py_ver} (Compatible!){C.END}")
        passed += 1
    else:
        print(f"   {C.RED}❌ Python Version: {py_ver} (Recommended: 3.11.x){C.END}")

    # 2. EXTERNAL SYSTEM TOOLS
    print(f"\n{C.BOLD}2. SYSTEM TOOLS (FFmpeg, Tesseract, Ollama):{C.END}")
    
    tools = {
        "Ollama (Local AI Engine)": "ollama --version",
        "FFmpeg (Video/Audio Processing)": "ffmpeg -version",
        "Tesseract OCR (Image Text)": "tesseract --version",
    }
    
    for name, cmd in tools.items():
        total += 1
        ok, out = check_cmd(cmd)
        if ok:
            ver = out.splitlines()[0] if out else "Installed"
            print(f"   {C.GREEN}✅ {name}: OK ({ver[:35]}){C.END}")
            passed += 1
        else:
            # Special check for tesseract in default folder
            if "Tesseract" in name and os.path.exists("C:\\Program Files\\Tesseract-OCR\\tesseract.exe"):
                print(f"   {C.GREEN}✅ {name}: OK (Found in Program Files){C.END}")
                passed += 1
            else:
                print(f"   {C.RED}❌ {name}: NOT FOUND / NOT IN PATH{C.END}")

    # 3. OLLAMA MODELS
    print(f"\n{C.BOLD}3. OLLAMA AI MODELS (Brain, Vision, Memory):{C.END}")
    ok, out = check_cmd("ollama list")
    models = ["llama3.2", "llava-phi3", "nomic-embed-text"]
    
    if ok:
        for m in models:
            total += 1
            if m in out:
                print(f"   {C.GREEN}✅ Model '{m}': DOWNLOADED{C.END}")
                passed += 1
            else:
                print(f"   {C.RED}❌ Model '{m}': MISSING (Run: ollama pull {m}){C.END}")
    else:
        for m in models:
            total += 1
            print(f"   {C.RED}❌ Model '{m}': Ollama not running/installed{C.END}")

    # 4. PYTHON PACKAGES
    print(f"\n{C.BOLD}4. PYTHON LIBRARIES:{C.END}")
    packages = {
        "ollama": "ollama",
        "chromadb": "chromadb",
        "customtkinter": "customtkinter",
        "Pillow": "PIL",
        "pyautogui": "pyautogui",
        "mss": "mss",
        "opencv-python": "cv2",
        "numpy": "numpy",
        "pynput": "pynput",
        "edge-tts": "edge_tts",
        "pygame": "pygame",
        "pyttsx3": "pyttsx3",
        "SpeechRecognition": "speech_recognition",
        "langdetect": "langdetect",
        "yt-dlp": "yt_dlp",
        "openai-whisper": "whisper",
        "torch (PyTorch)": "torch",
    }

    for display_name, import_name in packages.items():
        total += 1
        try:
            mod = importlib.import_module(import_name)
            ver = getattr(mod, '__version__', 'OK')
            print(f"   {C.GREEN}✅ {display_name:<20}: Installed ({ver}){C.END}")
            passed += 1
        except ImportError:
            print(f"   {C.RED}❌ {display_name:<20}: MISSING{C.END}")

    # 5. PROJECT FILES
    print(f"\n{C.BOLD}5. PROJECT CORE FILES:{C.END}")
    files = ["nova.py", "brain.py", "voice_engine.py", "voice_listener.py", "screen_vision.py", "executor.py", "learner.py", "config.json"]
    
    for f in files:
        total += 1
        if os.path.exists(f):
            print(f"   {C.GREEN}✅ File '{f}': Found{C.END}")
            passed += 1
        else:
            print(f"   {C.RED}❌ File '{f}': Missing{C.END}")

    # SUMMARY
    print(f"\n{C.CYAN}{C.BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.END}")
    score = (passed / total) * 100
    if score == 100:
        print(f"{C.GREEN}{C.BOLD}🎉 STATUS: 100% READY! ({passed}/{total} Checks Passed){C.END}")
        print(f"{C.GREEN}Aap bina kisi maslay ke 'python nova.py' run kar sakte hain!{C.END}")
    elif score >= 80:
        print(f"{C.YELLOW}{C.BOLD}⚠️ STATUS: ALMOST READY ({passed}/{total} Passed, {total - passed} Missing){C.END}")
        print(f"{C.YELLOW}Niche diye gaye missing items install karein.{C.END}")
    else:
        print(f"{C.RED}{C.BOLD}❌ STATUS: INCOMPLETE ({passed}/{total} Passed, {total - passed} Missing){C.END}")
    print(f"{C.CYAN}{C.BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{C.END}\n")

if __name__ == "__main__":
    main()