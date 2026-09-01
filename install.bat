@echo off
echo ========================================
echo   NOVA AI - INSTALLING EVERYTHING
echo ========================================
pip install -r requirements.txt
echo.
echo Installing Ollama models...
ollama pull llama3.2
ollama pull llava-phi3
ollama pull nomic-embed-text
echo.
echo ✅ INSTALLATION COMPLETE!
echo Run start.bat to launch Nova AI
pause