@echo off
title Nova AI
cd /d "%~dp0"

echo ==========================================
echo   🚀 STARTING NOVA AI (LOCAL DIRECTORY)
echo ==========================================

echo Starting Ollama background...
start "Ollama" /min ollama serve
timeout /t 4 /nobreak >nul

echo Launching Nova UI...
python nova.py
pause
