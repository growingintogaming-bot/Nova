Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "ollama serve", 0, False
WScript.Sleep 3000
WshShell.Run "pythonw nova_studio.py", 0, False