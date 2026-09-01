"""
👨‍💻 NOVA CODE ARCHITECT
- Autonomous Code Generation
- Self-Update / Self-Patching
- Syntax Verification with Auto-Rollback
"""

import os
import re
import ast
import time
import shutil
from pathlib import Path
import ollama

BASE_DIR = Path(__file__).resolve().parent
BACKUP_DIR = BASE_DIR / "data" / "backups"
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


class CodeArchitect:
    def __init__(self, model="llama3.2"):
        self.model = model

    def _extract_pure_code(self, raw_response: str) -> str:
        match = re.search(r'```(?:python)?\s*([\s\S]*?)\s*```', raw_response, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        lines = [line for line in raw_response.splitlines() if not line.strip().startswith("```")]
        return "\n".join(lines).strip()

    def _verify_python_syntax(self, code_content: str):
        try:
            ast.parse(code_content)
            return True, "Syntax OK"
        except SyntaxError as e:
            return False, f"Syntax Error on line {e.lineno}: {e.msg}"

    def create_new_script(self, instruction: str, output_filename: str = None) -> str:
        print("👨‍💻 CodeArchitect: Generating script...")

        prompt = (
            "You are an expert Python engineer. Write complete, production-ready code.\n\n"
            f"TASK: {instruction}\n\n"
            "RULES:\n"
            "1. Provide COMPLETE working code. NO placeholders.\n"
            "2. Include error handling (try-except).\n"
            "3. Include library installation as comment at top if needed.\n"
            "4. Output MUST be inside a single ```python ``` block.\n\n"
            "Write the code now:"
        )

        try:
            resp = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
            raw_code = resp['message']['content']
            clean_code = self._extract_pure_code(raw_code)

            # Verify syntax
            is_valid, msg = self._verify_python_syntax(clean_code)
            if not is_valid:
                fix_prompt = f"Fix this Python syntax error ({msg}) and return ONLY valid code:\n\n" + clean_code
                fix_resp = ollama.chat(model=self.model, messages=[{"role": "user", "content": fix_prompt}])
                clean_code = self._extract_pure_code(fix_resp['message']['content'])

            # Filename detection
            if not output_filename:
                name_match = re.search(r'([a-zA-Z0-9_-]+\.py)', instruction)
                if name_match:
                    output_filename = name_match.group(1)
                else:
                    output_filename = f"tool_{int(time.time())}.py"

            if not output_filename.endswith(".py") and "." not in output_filename:
                output_filename += ".py"

            file_path = BASE_DIR / output_filename
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(clean_code)

            return f"✅ File `{output_filename}` created successfully!\n📁 Path: `{file_path}`\n\nPreview:\n{clean_code[:300]}..."

        except Exception as e:
            return f"❌ Code creation failed: {e}"

    def update_self_code(self, target_file_name: str, update_instruction: str) -> str:
        target_path = BASE_DIR / target_file_name

        if not target_path.exists():
            return f"❌ File `{target_file_name}` not found."

        print(f"🔧 Self-Updating `{target_file_name}`...")

        # Backup first
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        backup_path = BACKUP_DIR / f"{target_file_name}_{timestamp}.bak"
        shutil.copy2(target_path, backup_path)

        with open(target_path, "r", encoding="utf-8") as f:
            current_code = f.read()

        prompt = (
            "You are modifying your own codebase.\n\n"
            f"TARGET FILE: {target_file_name}\n"
            f"INSTRUCTION: {update_instruction}\n\n"
            "CURRENT CODE:\n```python\n"
            + current_code
            + "\n```\n\n"
            "RULES:\n"
            "1. Return ENTIRE updated file inside ```python ``` block.\n"
            "2. Keep existing functions intact unless told to change.\n"
            "3. No syntax errors.\n\n"
            "Provide full updated code:"
        )

        try:
            resp = ollama.chat(model=self.model, messages=[{"role": "user", "content": prompt}])
            updated_code = self._extract_pure_code(resp['message']['content'])

            is_valid, msg = self._verify_python_syntax(updated_code)
            if not is_valid:
                shutil.copy2(backup_path, target_path)
                return f"❌ Update rejected: {msg}. File restored from backup."

            with open(target_path, "w", encoding="utf-8") as f:
                f.write(updated_code)

            return f"🚀 `{target_file_name}` updated successfully!\n🛡️ Backup: `{backup_path.name}`"

        except Exception as e:
            shutil.copy2(backup_path, target_path)
            return f"❌ Update failed: {e}. Original restored."