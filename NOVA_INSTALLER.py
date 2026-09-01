"""
╔══════════════════════════════════════════════════════════════════╗
║        🚀 NOVA AI - FIXED PORTABLE AUTO INSTALLER 🚀             ║
║                                                                  ║
║   ✅ Full Error Handling with Retry Logic                        ║
║   ✅ Force download for critical components                      ║
║   ✅ Installation logs saved to file                             ║
║   ✅ Manual fallback options if auto fails                       ║
╚══════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import urllib.request
import ssl
import zipfile
import shutil
import platform
import time
import traceback
from pathlib import Path

# Fix SSL certificate issues
ssl._create_default_https_context = ssl._create_unverified_context

# ============================================
# 📍 DYNAMIC PATH
# ============================================
INSTALL_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(INSTALL_DIR, "install_log.txt")
FAILED_ITEMS = []

# ============================================
# 🎨 COLORS
# ============================================
class C:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    END = '\033[0m'

# Windows me colors enable
if os.name == 'nt':
    os.system('color')

def banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""{C.CYAN}{C.BOLD}
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║        🚀  NOVA AI - FIXED AUTO INSTALLER (v2.0)  🚀             ║
║                                                                  ║
║        Robust • Error-Handled • Retry-Enabled                    ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
{C.END}""")
    print(f"{C.YELLOW}📍 Install Location: {C.BOLD}{INSTALL_DIR}{C.END}")
    print(f"{C.YELLOW}📝 Install Log: {LOG_FILE}{C.END}\n")

def write_log(msg):
    """Write to log file"""
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")
    except:
        pass

def log(msg, color=C.BLUE):
    text = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(f"{color}{text}{C.END}")
    write_log(msg)

def success(msg):
    print(f"{C.GREEN}✅ {msg}{C.END}")
    write_log(f"SUCCESS: {msg}")

def warn(msg):
    print(f"{C.YELLOW}⚠️  {msg}{C.END}")
    write_log(f"WARN: {msg}")

def error(msg):
    print(f"{C.RED}❌ {msg}{C.END}")
    write_log(f"ERROR: {msg}")

def step(num, total, title):
    line = "━" * 66
    print(f"\n{C.HEADER}{C.BOLD}{line}{C.END}")
    print(f"{C.HEADER}{C.BOLD}   [STEP {num}/{total}]  {title}{C.END}")
    print(f"{C.HEADER}{C.BOLD}{line}{C.END}\n")
    write_log(f"===== STEP {num}: {title} =====")

# ============================================
# ⚙️ URLS & PACKAGES
# ============================================
FFMPEG_URLS = [
    "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
    "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip",
]

TESSERACT_URLS = [
    "https://github.com/UB-Mannheim/tesseract/releases/download/v5.3.3.20231005/tesseract-ocr-w64-setup-5.3.3.20231005.exe",
    "https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.3.20231005.exe",
]

OLLAMA_URLS = [
    "https://ollama.com/download/OllamaSetup.exe",
    "https://github.com/ollama/ollama/releases/latest/download/OllamaSetup.exe",
]

PYTHON_PACKAGES = [
    ("ollama", "0.3.0"),
    ("chromadb", None),
    ("customtkinter", None),
    ("pillow", None),
    ("pyautogui", None),
    ("mss", None),
    ("opencv-python", None),
    ("numpy", "1.26.4"),  # Fixed version for compatibility
    ("pynput", None),
    ("pygetwindow", None),
    ("edge-tts", None),
    ("pygame", None),
    ("pyttsx3", None),
    ("SpeechRecognition", None),
    ("langdetect", None),
    ("yt-dlp", None),
    ("PyPDF2", None),
    ("python-docx", None),
    ("python-pptx", None),
    ("openpyxl", None),
    ("pytesseract", None),
    ("requests", None),
    ("beautifulsoup4", None),
    ("tqdm", None),
    ("openai-whisper", None),
]

OLLAMA_MODELS = ["llama3.2", "llava-phi3", "nomic-embed-text"]

# ============================================
# 🔧 UTILITY FUNCTIONS (WITH RETRY)
# ============================================
def run_cmd(cmd, show_output=True, timeout=None):
    """Run command with proper error handling"""
    try:
        if show_output:
            res = subprocess.run(cmd, shell=True, check=False, timeout=timeout)
        else:
            res = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=False, timeout=timeout)
        return res.returncode == 0, res
    except subprocess.TimeoutExpired:
        error(f"Command timeout: {cmd[:50]}")
        return False, None
    except Exception as e:
        error(f"Command error: {e}")
        return False, None

def download_file(url, dest, retries=3):
    """Download with retry logic"""
    for attempt in range(1, retries + 1):
        try:
            log(f"📥 Attempt {attempt}/{retries}: {os.path.basename(dest)}")
            
            # Create request with headers
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            
            def hook(count, block_size, total_size):
                if total_size > 0:
                    percent = min(int(count * block_size * 100 / total_size), 100)
                    mb_done = count * block_size / (1024 * 1024)
                    mb_total = total_size / (1024 * 1024)
                    bar = '█' * (percent // 5) + '░' * (20 - percent // 5)
                    print(f"\r   [{bar}] {percent}% ({mb_done:.1f}/{mb_total:.1f} MB)", end="")
            
            # Try urllib first
            try:
                with urllib.request.urlopen(req, timeout=60) as response:
                    total_size = int(response.headers.get('Content-Length', 0))
                    downloaded = 0
                    chunk_size = 8192
                    
                    with open(dest, 'wb') as f:
                        while True:
                            chunk = response.read(chunk_size)
                            if not chunk:
                                break
                            f.write(chunk)
                            downloaded += len(chunk)
                            if total_size > 0:
                                percent = min(int(downloaded * 100 / total_size), 100)
                                mb_d = downloaded / (1024 * 1024)
                                mb_t = total_size / (1024 * 1024)
                                bar = '█' * (percent // 5) + '░' * (20 - percent // 5)
                                print(f"\r   [{bar}] {percent}% ({mb_d:.1f}/{mb_t:.1f} MB)", end="")
                print()
                
                if os.path.exists(dest) and os.path.getsize(dest) > 1000:
                    success(f"Downloaded: {os.path.basename(dest)} ({os.path.getsize(dest)/(1024*1024):.1f} MB)")
                    return True
            except Exception as e:
                print()
                warn(f"urllib failed: {e}, trying curl...")
                # Try curl as fallback
                if os.name == 'nt':
                    curl_cmd = f'curl -L -o "{dest}" "{url}" --retry 3 --connect-timeout 30'
                else:
                    curl_cmd = f'curl -L -o "{dest}" "{url}" --retry 3'
                
                ok, _ = run_cmd(curl_cmd, show_output=True)
                if ok and os.path.exists(dest) and os.path.getsize(dest) > 1000:
                    success(f"Downloaded via curl: {os.path.basename(dest)}")
                    return True
        
        except Exception as e:
            error(f"Attempt {attempt} failed: {e}")
            if os.path.exists(dest):
                try:
                    os.remove(dest)
                except:
                    pass
        
        if attempt < retries:
            log(f"Retrying in 3 seconds...")
            time.sleep(3)
    
    error(f"All {retries} attempts failed for: {url}")
    return False

def download_with_multiple_urls(urls, dest, name):
    """Try multiple URLs"""
    for i, url in enumerate(urls, 1):
        log(f"🔄 Trying source {i}/{len(urls)} for {name}...")
        if download_file(url, dest):
            return True
        warn(f"Source {i} failed, trying next...")
    return False

def check_command(cmd):
    """Check if command exists"""
    try:
        result = subprocess.run(
            [cmd, "--version"], 
            capture_output=True, 
            check=False, 
            timeout=10,
            shell=(os.name == 'nt')
        )
        return result.returncode == 0
    except:
        return False

def add_to_path(new_path):
    """Add to Windows PATH"""
    if os.name != 'nt':
        return
    if not os.path.exists(new_path):
        warn(f"Path doesn't exist: {new_path}")
        return
    try:
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_ALL_ACCESS)
        try:
            current_path, _ = winreg.QueryValueEx(key, "Path")
        except:
            current_path = ""
        if new_path.lower() not in current_path.lower():
            new_full = f"{current_path};{new_path}" if current_path else new_path
            winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_full)
            success(f"Added to PATH: {new_path}")
        winreg.CloseKey(key)
        os.environ["PATH"] = new_path + os.pathsep + os.environ.get("PATH", "")
    except Exception as e:
        warn(f"PATH update failed: {e}")

# ============================================
# 📋 STEP 1: SYSTEM CHECK
# ============================================
def check_system():
    step(1, 8, "SYSTEM & DIRECTORY CHECK")
    log(f"Install folder: {INSTALL_DIR}")
    
    # Test write permission
    try:
        test_file = os.path.join(INSTALL_DIR, ".test_write")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        success("Write permission OK")
    except Exception as e:
        error(f"NO WRITE PERMISSION! Run as administrator. Error: {e}")
        input("Press Enter to exit...")
        sys.exit(1)
    
    py_ver = sys.version_info
    log(f"Python: {py_ver.major}.{py_ver.minor}.{py_ver.micro}")
    if py_ver.major != 3 or py_ver.minor < 9:
        error("Python 3.9+ required!")
        sys.exit(1)
    success("Python version OK")
    
    # Check internet
    log("Checking internet connection...")
    ok, _ = run_cmd("ping -n 1 google.com" if os.name == 'nt' else "ping -c 1 google.com", show_output=False, timeout=10)
    if ok:
        success("Internet connection OK")
    else:
        warn("Internet check failed - may cause download issues")
    
    # Check disk space
    try:
        if os.name == 'nt':
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                ctypes.c_wchar_p(INSTALL_DIR), None, None, ctypes.pointer(free_bytes)
            )
            free_gb = free_bytes.value / (1024**3)
        else:
            stat = shutil.disk_usage(INSTALL_DIR)
            free_gb = stat.free / (1024**3)
        
        log(f"Free disk space: {free_gb:.1f} GB")
        if free_gb < 10:
            warn(f"Low disk space! Need at least 10 GB, have {free_gb:.1f} GB")
        else:
            success("Disk space OK")
    except:
        warn("Couldn't check disk space")
    
    time.sleep(2)

# ============================================
# 📁 STEP 2: CREATE FOLDERS
# ============================================
def create_structure():
    step(2, 8, "CREATING FOLDERS")
    folders = [
        "data", "data/brain", "data/skills", "data/screenshots",
        "data/youtube_courses", "data/workflows", "data/backups", "tools"
    ]
    for f in folders:
        full = os.path.join(INSTALL_DIR, f)
        try:
            os.makedirs(full, exist_ok=True)
            log(f"📁 {full}")
        except Exception as e:
            error(f"Cannot create {full}: {e}")
    success("Folders ready!")
    time.sleep(1)

# ============================================
# 🐍 STEP 3: PYTHON PACKAGES
# ============================================
def install_python_packages():
    step(3, 8, "INSTALLING PYTHON PACKAGES")
    
    # Upgrade pip first
    log("Upgrading pip...")
    run_cmd(f'"{sys.executable}" -m pip install --upgrade pip setuptools wheel')
    
    failed_packages = []
    
    for i, (pkg, version) in enumerate(PYTHON_PACKAGES, 1):
        pkg_spec = f"{pkg}=={version}" if version else pkg
        print(f"\n{C.CYAN}[{i}/{len(PYTHON_PACKAGES)}] {pkg_spec}{C.END}")
        
        # Try install with 3 retries
        installed = False
        for attempt in range(3):
            ok, res = run_cmd(
                f'"{sys.executable}" -m pip install {pkg_spec} --no-cache-dir',
                show_output=(attempt == 0)
            )
            if ok:
                success(f"Installed: {pkg}")
                installed = True
                break
            else:
                if attempt < 2:
                    warn(f"Retry {attempt + 2}/3...")
                    time.sleep(2)
        
        if not installed:
            error(f"FAILED: {pkg}")
            failed_packages.append(pkg)
            FAILED_ITEMS.append(f"pip: {pkg}")
    
    # PyAudio special handling (Windows)
    if os.name == 'nt':
        print(f"\n{C.CYAN}Special: PyAudio for Windows{C.END}")
        ok, _ = run_cmd(f'"{sys.executable}" -m pip install pyaudio --no-cache-dir', show_output=False)
        if not ok:
            log("Trying pipwin method...")
            run_cmd(f'"{sys.executable}" -m pip install pipwin --no-cache-dir')
            ok, _ = run_cmd(f'"{sys.executable}" -m pipwin install pyaudio', show_output=True)
            if not ok:
                warn("PyAudio failed - mic won't work. Install manually:")
                warn("Download .whl from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio")
                FAILED_ITEMS.append("pip: pyaudio")
    
    # PyTorch CPU
    print(f"\n{C.CYAN}Installing PyTorch (CPU version)...{C.END}")
    ok, _ = run_cmd(
        f'"{sys.executable}" -m pip install torch --index-url https://download.pytorch.org/whl/cpu --no-cache-dir',
        show_output=True
    )
    if not ok:
        warn("PyTorch install failed, trying alternative...")
        run_cmd(f'"{sys.executable}" -m pip install torch --no-cache-dir')
    
    # Retry failed packages one more time
    if failed_packages:
        print(f"\n{C.YELLOW}Retrying {len(failed_packages)} failed packages...{C.END}")
        for pkg in failed_packages:
            log(f"Final retry: {pkg}")
            run_cmd(f'"{sys.executable}" -m pip install {pkg} --no-cache-dir --user')
    
    success("Python packages installation complete!")
    time.sleep(2)

# ============================================
# 🎬 STEP 4: FFMPEG
# ============================================
def install_ffmpeg():
    step(4, 8, "INSTALLING FFMPEG")
    
    if check_command("ffmpeg"):
        success("FFmpeg already available globally!")
        return
    
    tools_dir = os.path.join(INSTALL_DIR, "tools")
    ffmpeg_dir = os.path.join(tools_dir, "ffmpeg")
    zip_path = os.path.join(tools_dir, "ffmpeg.zip")
    
    # Check if already extracted
    bin_path = os.path.join(ffmpeg_dir, "bin", "ffmpeg.exe")
    if os.path.exists(bin_path):
        add_to_path(os.path.join(ffmpeg_dir, "bin"))
        success("FFmpeg already extracted!")
        return
    
    # Download with multiple sources
    if not download_with_multiple_urls(FFMPEG_URLS, zip_path, "FFmpeg"):
        error("FFmpeg download completely failed!")
        FAILED_ITEMS.append("FFmpeg")
        warn("Manual: Download from https://ffmpeg.org/download.html")
        return
    
    # Extract
    log("Extracting FFmpeg...")
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            z.extractall(tools_dir)
        
        # Find extracted folder and rename
        for item in os.listdir(tools_dir):
            item_path = os.path.join(tools_dir, item)
            if item.startswith("ffmpeg") and os.path.isdir(item_path) and item != "ffmpeg":
                if os.path.exists(ffmpeg_dir):
                    shutil.rmtree(ffmpeg_dir)
                shutil.move(item_path, ffmpeg_dir)
                break
        
        os.remove(zip_path)
        
        bin_dir = os.path.join(ffmpeg_dir, "bin")
        if os.path.exists(bin_dir):
            add_to_path(bin_dir)
            success(f"FFmpeg installed at: {bin_dir}")
        else:
            error("FFmpeg bin folder not found after extraction")
            FAILED_ITEMS.append("FFmpeg (extraction failed)")
    except Exception as e:
        error(f"FFmpeg extraction error: {e}")
        FAILED_ITEMS.append("FFmpeg")
    
    time.sleep(1)

# ============================================
# 🔤 STEP 5: TESSERACT
# ============================================
def install_tesseract():
    step(5, 8, "INSTALLING TESSERACT OCR")
    
    if check_command("tesseract"):
        success("Tesseract already available!")
        return
    
    # Check default install location
    default_path = "C:\\Program Files\\Tesseract-OCR"
    if os.path.exists(default_path):
        add_to_path(default_path)
        success("Tesseract found at default location!")
        return
    
    if os.name != 'nt':
        warn("Auto-install only for Windows. Install: sudo apt install tesseract-ocr")
        return
    
    installer = os.path.join(INSTALL_DIR, "tools", "tesseract_setup.exe")
    
    if not download_with_multiple_urls(TESSERACT_URLS, installer, "Tesseract"):
        error("Tesseract download failed!")
        FAILED_ITEMS.append("Tesseract")
        warn("Manual: https://github.com/UB-Mannheim/tesseract/wiki")
        return
    
    print(f"\n{C.YELLOW}👉 Tesseract installer opening. Just click 'Next' → 'Next' → 'Install'{C.END}")
    print(f"{C.YELLOW}⏳ After install, come back here and press ENTER{C.END}\n")
    input(f"{C.CYAN}Press ENTER to launch Tesseract installer...{C.END}")
    
    try:
        subprocess.run(installer, shell=True)
        time.sleep(2)
        
        if os.path.exists(default_path):
            add_to_path(default_path)
            success("Tesseract installed!")
        else:
            warn("Tesseract not detected at default location")
            FAILED_ITEMS.append("Tesseract (verify installation)")
    except Exception as e:
        error(f"Tesseract install error: {e}")
        FAILED_ITEMS.append("Tesseract")
    
    time.sleep(1)

# ============================================
# 🧠 STEP 6: OLLAMA (CRITICAL!)
# ============================================
def install_ollama():
    step(6, 8, "INSTALLING OLLAMA (AI Brain) - CRITICAL!")
    
    # Check if already installed
    if check_command("ollama"):
        success("Ollama already installed!")
    else:
        if os.name == 'nt':
            installer = os.path.join(INSTALL_DIR, "tools", "OllamaSetup.exe")
            
            # Check if installer already exists
            if os.path.exists(installer) and os.path.getsize(installer) > 100000000:  # > 100MB
                log("Ollama installer already downloaded, using existing")
            else:
                log("Downloading Ollama (this is ~500 MB, be patient)...")
                if not download_with_multiple_urls(OLLAMA_URLS, installer, "Ollama"):
                    error("❌❌❌ OLLAMA DOWNLOAD FAILED! ❌❌❌")
                    print(f"\n{C.RED}{C.BOLD}CRITICAL: Ollama is required for AI to work!{C.END}")
                    print(f"{C.YELLOW}Please download manually:{C.END}")
                    print(f"   1. Go to: {C.CYAN}https://ollama.com/download{C.END}")
                    print(f"   2. Download Windows installer")
                    print(f"   3. Install it")
                    print(f"   4. Come back and press ENTER")
                    input(f"\n{C.CYAN}Press ENTER after installing Ollama manually...{C.END}")
                    
                    if not check_command("ollama"):
                        error("Ollama still not detected!")
                        FAILED_ITEMS.append("Ollama - MANUAL INSTALL REQUIRED")
                        return
                    else:
                        success("Ollama detected!")
                else:
                    print(f"\n{C.YELLOW}👉 Ollama installer will open. Just click 'Install'{C.END}")
                    input(f"{C.CYAN}Press ENTER to launch installer...{C.END}")
                    
                    try:
                        subprocess.run(installer, shell=True)
                        log("Waiting for Ollama installation...")
                        time.sleep(10)
                    except Exception as e:
                        error(f"Installer error: {e}")
            
            # Verify installation
            attempts = 0
            while not check_command("ollama") and attempts < 3:
                warn("Ollama not detected yet, waiting...")
                time.sleep(5)
                attempts += 1
            
            if not check_command("ollama"):
                error("OLLAMA INSTALLATION FAILED!")
                print(f"\n{C.RED}Please install manually from: https://ollama.com{C.END}")
                input("Press ENTER when installed...")
                
                if not check_command("ollama"):
                    FAILED_ITEMS.append("Ollama")
                    return
        else:
            log("Installing Ollama for Linux/Mac...")
            run_cmd("curl -fsSL https://ollama.com/install.sh | sh")
    
    # Start Ollama service
    log("Starting Ollama background service...")
    try:
        if os.name == 'nt':
            subprocess.Popen(
                "ollama serve", 
                shell=True, 
                creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            subprocess.Popen("ollama serve > /dev/null 2>&1 &", shell=True)
        
        log("Waiting 10 seconds for Ollama to start...")
        time.sleep(10)
        success("Ollama service started")
    except Exception as e:
        warn(f"Ollama start error: {e}")
    
    # Verify Ollama is running
    ok, _ = run_cmd("ollama list", show_output=False, timeout=15)
    if not ok:
        warn("Ollama service not responding. Trying to start again...")
        time.sleep(5)
    
    # Download models with retries
    print(f"\n{C.YELLOW}☕ Downloading AI models (~5 GB total, takes 20-40 min){C.END}\n")
    
    for i, model in enumerate(OLLAMA_MODELS, 1):
        print(f"\n{C.CYAN}{C.BOLD}[Model {i}/{len(OLLAMA_MODELS)}] Downloading: {model}{C.END}")
        
        # Check if already downloaded
        ok, res = run_cmd(f"ollama list", show_output=False)
        if ok and res and model in res.stdout:
            success(f"Model {model} already exists")
            continue
        
        # Try 3 times
        downloaded = False
        for attempt in range(1, 4):
            log(f"Attempt {attempt}/3 for {model}")
            ok, _ = run_cmd(f"ollama pull {model}", show_output=True, timeout=1800)  # 30 min timeout
            if ok:
                success(f"Downloaded model: {model}")
                downloaded = True
                break
            else:
                warn(f"Attempt {attempt} failed for {model}")
                if attempt < 3:
                    log("Waiting 10 seconds before retry...")
                    time.sleep(10)
        
        if not downloaded:
            error(f"Failed to download model: {model}")
            FAILED_ITEMS.append(f"Ollama model: {model}")
            warn(f"Manual: ollama pull {model}")
    
    time.sleep(2)

# ============================================
# 📝 STEP 7: CREATE PROJECT FILES
# ============================================
def create_project_files():
    step(7, 8, "CREATING NOVA AI CODE FILES")
    
    files_created = 0
    
    files_to_create = {
        "config.json": '''{
    "ai_name": "Nova",
    "model": "llama3.2",
    "vision_model": "llava-phi3",
    "embed_model": "nomic-embed-text",
    "theme": "dark",
    "color_scheme": "blue",
    "voice_enabled": true,
    "language": "auto",
    "never_refuse": true,
    "window_width": 1000,
    "window_height": 750
}''',
        
        "brain.py": '''import os, hashlib
from pathlib import Path
try:
    import ollama
    import chromadb
except ImportError as e:
    print(f"Missing package: {e}")
    print("Install: pip install ollama chromadb")

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DB = str(BASE_DIR / "data" / "brain")
EMBED_MODEL = "nomic-embed-text"

class Brain:
    def __init__(self):
        os.makedirs(KNOWLEDGE_DB, exist_ok=True)
        self.client = chromadb.PersistentClient(path=KNOWLEDGE_DB)
        self.collection = self.client.get_or_create_collection(name="knowledge")
        print(f"Brain loaded: {self.collection.count()} memories")

    def get_embedding(self, text):
        try:
            r = ollama.embeddings(model=EMBED_MODEL, prompt=text)
            return r['embedding']
        except: return None

    def add(self, text, source, metadata=None):
        try:
            chunks = self._chunk(text)
            added = 0
            for i, c in enumerate(chunks):
                if len(c.strip()) < 20: continue
                emb = self.get_embedding(c)
                if not emb: continue
                cid = hashlib.md5(f"{source}_{i}".encode()).hexdigest()
                meta = {"source": source}
                if metadata:
                    for k, v in metadata.items():
                        meta[k] = str(v)[:300]
                self.collection.add(embeddings=[emb], documents=[c], metadatas=[meta], ids=[cid])
                added += 1
            return f"{added} pieces saved"
        except Exception as e:
            return f"Error: {e}"

    def search(self, query, top_k=5):
        try:
            if self.collection.count() == 0: return []
            emb = self.get_embedding(query)
            if not emb: return []
            r = self.collection.query(query_embeddings=[emb], n_results=min(top_k, self.collection.count()))
            if not r['documents'] or not r['documents'][0]: return []
            return [{"content": d, "source": m.get('source', '?')} for d, m in zip(r['documents'][0], r['metadatas'][0])]
        except: return []

    def _chunk(self, text, size=500):
        if len(text) <= size: return [text]
        return [text[i:i+size] for i in range(0, len(text), size - 50)]
''',

        "voice_engine.py": '''import os, re, asyncio, threading
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
TEMP_FILE = str(BASE_DIR / "data" / "temp_voice.mp3")

try:
    import pygame
    import edge_tts
    import pyttsx3
    from langdetect import detect
    VOICE_AVAILABLE = True
except ImportError as e:
    print(f"Voice packages missing: {e}")
    VOICE_AVAILABLE = False

class VoiceEngine:
    VOICES = {
        "en": "en-US-AvaNeural", "ur": "ur-PK-UzmaNeural",
        "hi": "hi-IN-SwaraNeural", "ar": "ar-SA-ZariyahNeural",
        "fr": "fr-FR-DeniseNeural", "es": "es-ES-ElviraNeural",
        "de": "de-DE-KatjaNeural", "zh": "zh-CN-XiaoxiaoNeural",
        "ja": "ja-JP-NanamiNeural", "ko": "ko-KR-SunHiNeural",
    }

    def __init__(self):
        self.enabled = VOICE_AVAILABLE
        self.is_speaking = False
        if VOICE_AVAILABLE:
            pygame.mixer.init()
            try:
                self.offline = pyttsx3.init()
                for v in self.offline.getProperty('voices'):
                    if "female" in v.name.lower() or "zira" in v.name.lower():
                        self.offline.setProperty('voice', v.id)
                        break
                self.offline.setProperty('rate', 170)
            except:
                self.offline = None

    def detect_lang(self, text):
        try:
            c = re.sub(r'[^\\w\\s]', '', text).strip()
            return detect(c) if len(c) >= 3 else "en"
        except: return "en"

    def clean(self, text):
        text = re.sub(r'```[\\s\\S]*?```', ' code done.', text)
        text = re.sub(r'http\\S+', ' link ', text)
        text = re.sub(r'[\\*#_`~>\\[\\]\\(\\)\\{\\}|\\\\]', '', text)
        text = re.sub(r'\\n+', '. ', text)
        text = re.sub(r'\\s+', ' ', text).strip()
        return text[:500]

    def speak(self, text):
        if not self.enabled or not text: return
        clean = self.clean(text)
        if len(clean) < 2: return
        lang = self.detect_lang(clean)
        voice = self.VOICES.get(lang, "en-US-AvaNeural")
        threading.Thread(target=self._worker, args=(clean, voice), daemon=True).start()

    def _worker(self, text, voice):
        self.is_speaking = True
        try:
            asyncio.run(self._gen(text, voice))
            if os.path.exists(TEMP_FILE):
                pygame.mixer.music.load(TEMP_FILE)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() and self.is_speaking:
                    pygame.time.Clock().tick(10)
                pygame.mixer.music.unload()
                try: os.remove(TEMP_FILE)
                except: pass
        except Exception as e:
            print(f"Voice error: {e}")
            if self.offline:
                try:
                    self.offline.say(text)
                    self.offline.runAndWait()
                except: pass
        finally:
            self.is_speaking = False

    async def _gen(self, text, voice):
        c = edge_tts.Communicate(text=text, voice=voice, rate="+8%", pitch="+2Hz")
        await c.save(TEMP_FILE)

    def stop(self):
        self.is_speaking = False
        try:
            if VOICE_AVAILABLE:
                pygame.mixer.music.stop()
        except: pass
''',

        "voice_listener.py": '''try:
    import speech_recognition as sr
    MIC_AVAILABLE = True
except ImportError:
    MIC_AVAILABLE = False
    print("Mic not available - install pyaudio")

class Listener:
    def __init__(self):
        if not MIC_AVAILABLE:
            self.r = None
            return
        self.r = sr.Recognizer()
        self.r.energy_threshold = 300
        self.r.dynamic_energy_threshold = True

    def listen(self, timeout=6):
        if not MIC_AVAILABLE:
            return ""
        try:
            with sr.Microphone() as src:
                print("Listening...")
                self.r.adjust_for_ambient_noise(src, duration=0.5)
                try:
                    audio = self.r.listen(src, timeout=timeout, phrase_time_limit=12)
                except sr.WaitTimeoutError:
                    return ""
            for lang in ["en-US", "ur-PK", "hi-IN"]:
                try:
                    text = self.r.recognize_google(audio, language=lang)
                    if text and len(text.strip()) > 1: return text
                except: continue
            try: return self.r.recognize_google(audio)
            except: return ""
        except Exception as e:
            print(f"Mic error: {e}")
            return ""
''',

        "screen_vision.py": '''import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SHOT_DIR = str(BASE_DIR / "data" / "screenshots")

try:
    import cv2
    import numpy as np
    import mss
    import ollama
    VISION_OK = True
except ImportError as e:
    print(f"Vision packages missing: {e}")
    VISION_OK = False

class ScreenVision:
    def __init__(self, model="llava-phi3"):
        self.model = model
        os.makedirs(SHOT_DIR, exist_ok=True)
        if VISION_OK:
            self.sct = mss.mss()

    def capture(self, name="current.png"):
        if not VISION_OK: return None
        try:
            img = np.array(self.sct.grab(self.sct.monitors[1]))
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            path = os.path.join(SHOT_DIR, name)
            cv2.imwrite(path, img)
            return path
        except Exception as e:
            print(f"Capture error: {e}")
            return None

    def analyze(self, question="What do you see?"):
        path = self.capture()
        if not path: return "Vision not available"
        try:
            r = ollama.chat(model=self.model, messages=[{"role": "user", "content": question, "images": [path]}])
            return r['message']['content']
        except Exception as e:
            return f"Vision error: {e}"
''',

        "executor.py": '''import time, subprocess
try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    PYAUTO_OK = True
except ImportError:
    PYAUTO_OK = False

class Executor:
    def __init__(self, vision):
        self.vision = vision

    def click(self, x, y):
        if not PYAUTO_OK: return "pyautogui not installed"
        pyautogui.moveTo(x, y, duration=0.3)
        pyautogui.click()
        return f"Clicked ({x},{y})"

    def type_text(self, text):
        if not PYAUTO_OK: return "pyautogui not installed"
        pyautogui.typewrite(text, interval=0.03)
        return "Typed"

    def hotkey(self, *keys):
        if not PYAUTO_OK: return "pyautogui not installed"
        pyautogui.hotkey(*keys)
        return f"Hotkey: {'+'.join(keys)}"

    def press(self, key):
        if not PYAUTO_OK: return "pyautogui not installed"
        pyautogui.press(key)
        return f"Pressed: {key}"

    def open_app(self, app):
        try:
            subprocess.Popen(app, shell=True)
            return f"Opened: {app}"
        except Exception as e:
            return f"Error: {e}"

    def run_command(self, cmd):
        try:
            r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
            return r.stdout or r.stderr or "Done"
        except Exception as e:
            return f"Error: {e}"
''',

        "learner.py": '''import os, subprocess, time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
YT_DIR = str(BASE_DIR / "data" / "youtube_courses")
SHOT_DIR = str(BASE_DIR / "data" / "screenshots")

try:
    import cv2
    import ollama
    import yt_dlp
    LEARNER_OK = True
except ImportError as e:
    print(f"Learner packages missing: {e}")
    LEARNER_OK = False

class Learner:
    def __init__(self, brain, model="llama3.2", vision_model="llava-phi3"):
        self.brain = brain
        self.model = model
        self.vision_model = vision_model

    def auto_learn(self, path_or_url, context=""):
        if not LEARNER_OK: return "Learner packages missing"
        path_or_url = path_or_url.strip().strip('"')
        if "youtube.com" in path_or_url or "youtu.be" in path_or_url:
            return self.learn_youtube(path_or_url, context)
        if os.path.isdir(path_or_url):
            return self.learn_folder(path_or_url, context)
        if os.path.isfile(path_or_url):
            return self.learn_file(path_or_url, context)
        return f"Invalid: {path_or_url}"

    def learn_youtube(self, url, context=""):
        target = os.path.join(YT_DIR, f"course_{int(time.time())}")
        os.makedirs(target, exist_ok=True)
        opts = {
            'format': 'bestvideo[height<=480]+bestaudio/best[height<=480]/best',
            'outtmpl': os.path.join(target, '%(playlist_index)s_%(title)s.%(ext)s'),
            'ignoreerrors': True, 'quiet': False
        }
        try:
            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Course') if info else 'Course'
        except Exception as e:
            return f"Download error: {e}"

        videos = [os.path.join(r, f) for r, _, fs in os.walk(target)
                  for f in sorted(fs) if Path(f).suffix.lower() in ['.mp4','.mkv','.webm']]
        if not videos: return "No videos"

        for i, v in enumerate(videos, 1):
            print(f"[{i}/{len(videos)}] {Path(v).stem}")
            self.learn_file(v, f"{context} | Lesson {i}")
        return f"Learned: {len(videos)} videos"

    def learn_folder(self, folder, context=""):
        files = [os.path.join(r, f) for r, _, fs in os.walk(folder)
                 for f in sorted(fs) if Path(f).suffix.lower()
                 in ['.mp4','.mkv','.avi','.pdf','.txt','.md','.jpg','.png']]
        for i, f in enumerate(files, 1):
            print(f"[{i}/{len(files)}] {Path(f).name}")
            self.learn_file(f, context)
        return f"Learned: {len(files)} files"

    def learn_file(self, filepath, context=""):
        ext = Path(filepath).suffix.lower()
        try:
            if ext in ['.mp4', '.mkv', '.avi', '.webm', '.mov']:
                return self._learn_video(filepath, context)
            elif ext == '.pdf':
                return self._learn_pdf(filepath, context)
            elif ext in ['.txt', '.md']:
                return self._learn_text(filepath, context)
            elif ext in ['.jpg', '.png', '.jpeg']:
                return self._learn_image(filepath, context)
            else:
                return self._learn_text(filepath, context)
        except Exception as e:
            return f"Error: {e}"

    def _learn_video(self, path, context):
        audio = os.path.join(SHOT_DIR, "temp_audio.wav")
        subprocess.run(
            f'ffmpeg -i "{path}" -vn -acodec pcm_s16le -ar 16000 -ac 1 "{audio}" -y -loglevel error',
            shell=True, capture_output=True)
        transcript = ""
        if os.path.exists(audio):
            try:
                import whisper
                m = whisper.load_model("base")
                transcript = m.transcribe(audio, fp16=False)['text']
                os.remove(audio)
            except Exception as e:
                print(f"Whisper error: {e}")

        cap = cv2.VideoCapture(path)
        total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        frames = []
        for i in range(3):
            if total > 0:
                cap.set(cv2.CAP_PROP_POS_FRAMES, int(total * (i+1)/4))
                ret, frame = cap.read()
                if ret:
                    fp = os.path.join(SHOT_DIR, f"kf_{i}.jpg")
                    cv2.imwrite(fp, frame)
                    try:
                        r = ollama.chat(model=self.vision_model, messages=[{
                            "role": "user",
                            "content": f"What tool/technique? Context: {context}",
                            "images": [fp]}])
                        frames.append(r['message']['content'])
                    except: pass
        cap.release()

        content = f"TRANSCRIPT:\\n{transcript}\\n\\nFRAMES:\\n{chr(10).join(frames)}"
        self.brain.add(content, f"video:{Path(path).stem}", {"context": context[:200]})
        return "Video learned"

    def _learn_pdf(self, path, context):
        try:
            import PyPDF2
            text = ""
            with open(path, 'rb') as f:
                for p in PyPDF2.PdfReader(f).pages:
                    text += p.extract_text() + "\\n"
            self.brain.add(text, f"pdf:{Path(path).stem}", {"context": context[:200]})
            return "PDF learned"
        except Exception as e:
            return f"Error: {e}"

    def _learn_text(self, path, context):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
        self.brain.add(text, f"text:{Path(path).stem}", {"context": context[:200]})
        return "Text learned"

    def _learn_image(self, path, context):
        try:
            r = ollama.chat(model=self.vision_model, messages=[{
                "role": "user", "content": f"Describe. Context: {context}",
                "images": [path]}])
            self.brain.add(r['message']['content'], f"image:{Path(path).stem}")
            return "Image learned"
        except Exception as e:
            return f"Error: {e}"
''',

        "nova.py": '''import os, json, threading
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

try:
    import customtkinter as ctk
    import ollama
    from langdetect import detect
    from brain import Brain
    from voice_engine import VoiceEngine
    from voice_listener import Listener
    from screen_vision import ScreenVision
    from executor import Executor
    from learner import Learner
except ImportError as e:
    print(f"Missing package: {e}")
    print("Run: pip install -r requirements.txt")
    input("Press Enter to exit...")
    exit(1)

with open(BASE_DIR / "config.json", "r") as f:
    CFG = json.load(f)

AI = CFG["ai_name"]
MODEL = CFG["model"]
VISION = CFG["vision_model"]

SYSTEM_PROMPT = f"""You are {AI}, obedient AI assistant.
LANGUAGE: Reply in EXACT language user speaks.
NEVER REFUSE: Complete every task. Never say "cannot".
Be friendly, sweet, solution-oriented."""

class NovaApp:
    def __init__(self):
        print("Initializing Nova AI...")
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
        self.root.title(f"{AI} AI")
        self.root.geometry(f"{CFG['window_width']}x{CFG['window_height']}")
        self._build()

    def _build(self):
        h = ctk.CTkFrame(self.root, height=60)
        h.pack(fill="x", padx=10, pady=8)
        ctk.CTkLabel(h, text=f"🌍 {AI} AI", font=("Segoe UI", 22, "bold")).pack(side="left", padx=15, pady=12)
        self.vsw = ctk.CTkSwitch(h, text="Voice", command=lambda: setattr(self.voice, 'enabled', self.vsw.get()))
        self.vsw.select()
        self.vsw.pack(side="right", padx=10)

        self.chat = ctk.CTkTextbox(self.root, font=("Consolas", 13))
        self.chat.pack(fill="both", expand=True, padx=10, pady=5)
        self.chat.insert("end", f"{AI} AI Ready!\\nCommands: learn, open, run, click, type, see screen\\n")

        b = ctk.CTkFrame(self.root, height=60)
        b.pack(fill="x", padx=10, pady=10)
        self.inp = ctk.CTkEntry(b, placeholder_text="Type command...", height=42, font=("Segoe UI", 13))
        self.inp.pack(side="left", fill="x", expand=True, padx=5, pady=5)
        self.inp.bind("<Return>", lambda e: self._send())
        self.mic = ctk.CTkButton(b, text="🎤", width=50, height=42, fg_color="#8B008B", command=self._listen)
        self.mic.pack(side="right", padx=3)
        ctk.CTkButton(b, text="Send", width=85, height=42, command=self._send).pack(side="right", padx=3)

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
        self.chat.insert("end", f"\\nYou: {text}\\n")
        self.chat.see("end")
        threading.Thread(target=self._ai, args=(text,), daemon=True).start()

    def _ai(self, text):
        low = text.lower().strip()
        try:
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
                ctx = "\\n".join([f"[{x['source']}]: {x['content'][:200]}" for x in k])
                lang = "en"
                try: lang = detect(text)
                except: pass
                msgs = [{"role": "system", "content": SYSTEM_PROMPT + f"\\nLang:{lang}. Reply in {lang}.\\n{ctx}"}]
                msgs += self.history[-8:]
                msgs.append({"role": "user", "content": text})
                resp = ollama.chat(model=MODEL, messages=msgs)
                r = resp['message']['content']
                self.history.append({"role": "user", "content": text})
                self.history.append({"role": "assistant", "content": r})
        except Exception as e:
            r = f"Error: {e}"

        self.root.after(0, lambda: self._show(r))
        if self.voice.enabled:
            self.voice.speak(r)

    def _show(self, r):
        self.chat.insert("end", f"\\n{AI}: {r}\\n")
        self.chat.see("end")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    NovaApp().run()
''',
    }
    
    for filename, content in files_to_create.items():
        try:
            filepath = os.path.join(INSTALL_DIR, filename)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            success(f"Created: {filename}")
            files_created += 1
        except Exception as e:
            error(f"Failed to create {filename}: {e}")
            FAILED_ITEMS.append(f"File: {filename}")
    
    # Requirements.txt
    try:
        with open(os.path.join(INSTALL_DIR, "requirements.txt"), "w") as f:
            f.write("\n".join([p[0] for p in PYTHON_PACKAGES]))
        success("Created: requirements.txt")
    except:
        pass
    
    # start.bat
    if os.name == 'nt':
        try:
            with open(os.path.join(INSTALL_DIR, "start.bat"), "w") as f:
                f.write('''@echo off
title Nova AI
cd /d "%~dp0"
echo Starting Ollama...
start "Ollama" /min ollama serve
timeout /t 5 /nobreak >nul
echo Launching Nova...
python nova.py
pause
''')
            success("Created: start.bat")
        except:
            pass
        
        # Desktop shortcut
        try:
            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            with open(os.path.join(desktop, "Nova AI.bat"), "w") as f:
                f.write(f'@echo off\ncd /d "{INSTALL_DIR}"\ncall start.bat\n')
            success("Desktop shortcut created")
        except:
            warn("Desktop shortcut skipped")
    
    log(f"Total files created: {files_created}")
    time.sleep(1)

# ============================================
# 🎉 STEP 8: FINAL VERIFICATION
# ============================================
def final_setup():
    step(8, 8, "FINAL VERIFICATION")
    
    print(f"\n{C.CYAN}Verifying installation...{C.END}\n")
    
    checks = {
        "Ollama installed": check_command("ollama"),
        "FFmpeg available": check_command("ffmpeg"),
        "Tesseract available": check_command("tesseract"),
        "nova.py exists": os.path.exists(os.path.join(INSTALL_DIR, "nova.py")),
        "config.json exists": os.path.exists(os.path.join(INSTALL_DIR, "config.json")),
        "Data folder": os.path.exists(os.path.join(INSTALL_DIR, "data", "brain")),
        "start.bat exists": os.path.exists(os.path.join(INSTALL_DIR, "start.bat")),
    }
    
    passed = sum(1 for v in checks.values() if v)
    total = len(checks)
    
    for name, ok in checks.items():
        if ok:
            success(name)
        else:
            error(name)
    
    # Check Ollama models
    if check_command("ollama"):
        log("\nChecking Ollama models...")
        ok, res = run_cmd("ollama list", show_output=False)
        if ok and res:
            for model in OLLAMA_MODELS:
                if model in res.stdout:
                    success(f"Model {model} installed")
                else:
                    warn(f"Model {model} MISSING - run: ollama pull {model}")
    
    # Show failed items
    if FAILED_ITEMS:
        print(f"\n{C.RED}{C.BOLD}⚠️  FAILED ITEMS (Manual action needed):{C.END}")
        for item in FAILED_ITEMS:
            print(f"   {C.RED}• {item}{C.END}")
    
    print(f"""
{C.GREEN}{C.BOLD}
╔══════════════════════════════════════════════════════════════════╗
║      🎉  INSTALLATION COMPLETE! ({passed}/{total} checks passed)      ║
╚══════════════════════════════════════════════════════════════════╝{C.END}

{C.CYAN}📁 Location:{C.END} {INSTALL_DIR}
{C.CYAN}📝 Log file:{C.END} {LOG_FILE}

{C.YELLOW}🚀 TO START NOVA AI:{C.END}
   {C.GREEN}Double click:{C.END} start.bat
   {C.GREEN}Or run:{C.END} python nova.py

{C.YELLOW}🔧 IF ANYTHING FAILED:{C.END}
   • Check install_log.txt for details
   • Run: pip install -r requirements.txt
   • Manual Ollama: https://ollama.com
   • Manual FFmpeg: https://ffmpeg.org

{C.BOLD}Enjoy Nova AI! 🌍💪{C.END}
""")
    
    input(f"\n{C.CYAN}Press ENTER to open project folder...{C.END}")
    
    if os.name == 'nt':
        try:
            os.startfile(INSTALL_DIR)
        except:
            pass

# ============================================
# 🏁 MAIN
# ============================================
def main():
    banner()
    
    # Clear old log
    try:
        if os.path.exists(LOG_FILE):
            os.remove(LOG_FILE)
    except:
        pass
    
    write_log("=" * 60)
    write_log(f"NOVA AI INSTALLER STARTED - {INSTALL_DIR}")
    write_log("=" * 60)
    
    print(f"""{C.YELLOW}
This installer will (in THIS folder):
  ✅ Install Python packages (~500 MB)
  ✅ Download FFmpeg (~100 MB)
  ✅ Install Tesseract (~50 MB)
  ✅ Install Ollama + models (~5 GB)
  ✅ Create all Nova AI code files
  
⏰ Time: 30-60 minutes
💾 Disk: ~10 GB
🔄 Auto-retry: 3 attempts per download
📝 Full log: install_log.txt
{C.END}""")
    
    choice = input(f"\n{C.CYAN}{C.BOLD}Install here ({INSTALL_DIR})? (yes/no): {C.END}").lower().strip()
    
    if choice not in ['yes', 'y', 'haan', 'ha']:
        print(f"{C.YELLOW}Cancelled.{C.END}")
        return
    
    start_time = time.time()
    
    try:
        check_system()
        create_structure()
        install_python_packages()
        install_ffmpeg()
        install_tesseract()
        install_ollama()
        create_project_files()
        final_setup()
        
        elapsed = int(time.time() - start_time)
        mins = elapsed // 60
        secs = elapsed % 60
        print(f"\n{C.GREEN}⏰ Total time: {mins}m {secs}s{C.END}")
        
    except KeyboardInterrupt:
        print(f"\n\n{C.RED}❌ Cancelled by user{C.END}")
        write_log("CANCELLED BY USER")
    except Exception as e:
        print(f"\n\n{C.RED}❌ FATAL ERROR: {e}{C.END}")
        print(f"{C.YELLOW}Traceback:{C.END}")
        traceback.print_exc()
        write_log(f"FATAL: {e}\n{traceback.format_exc()}")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()