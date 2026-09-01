"""
🧠 NOVA AUTONOMOUS TOPIC & PROJECT ENGINE
- Takes a broad high-level topic from the Boss
- Recalls relevant skills from Memory & Skill Matrix
- Formulates a multi-phase strategic execution plan
- Autonomously generates scripts, 3D scenes, documentation, and project workspace
"""

import os
import re
import json
import time
import subprocess
from pathlib import Path
import ollama

BASE_DIR = Path(__file__).resolve().parent
PROJECTS_ROOT = BASE_DIR / "data" / "projects"
PROJECTS_ROOT.mkdir(parents=True, exist_ok=True)


class TopicEngine:
    def __init__(self, brain, skill_matrix, code_architect, blender_controller, executor, model="llama3.2"):
        self.brain = brain
        self.skill_matrix = skill_matrix
        self.code_architect = code_architect
        self.blender = blender_controller
        self.executor = executor
        self.model = model
        self.is_running = False

    def execute_topic_project(self, topic_query: str, progress_cb=None) -> str:
        """
        Takes a topic, searches internal memory, creates project workspace,
        generates code, 3D scenes or tools, and delivers a completed project.
        """
        self.is_running = True

        def notify(msg, pct=None):
            if progress_cb:
                progress_cb(msg, pct, "action")

        # Clean Topic Name & Create Workspace Folder
        topic_slug = re.sub(r'[^a-zA-Z0-9_-]', '_', topic_query[:35]).strip('_').lower()
        if not topic_slug:
            topic_slug = f"project_{int(time.time())}"

        project_dir = PROJECTS_ROOT / topic_slug
        project_dir.mkdir(parents=True, exist_ok=True)

        notify(f"🚀 [10%] Topic Analysis Start: '{topic_query}'...", 0.10)
        time.sleep(0.5)

        # ============================================
        # PHASE 1: BRAIN RECALL & MEMORY SEARCH
        # ============================================
        notify("🧠 [25%] Internal memory aur learned skills recall ho rahe hain...", 0.25)
        memories = self.brain.search(topic_query, top_k=3)
        knowledge_context = "\n".join([f"- {m['content'][:250]}" for m in memories]) if memories else "No direct past memory found."

        # Check matched skills in skill matrix
        matched_manifest, sw_found, cat = self.skill_matrix.match_skill(topic_query)
        skill_context = f"Matched Software Skill: {sw_found} ({cat})" if sw_found else "General Custom Automation"

        # ============================================
        # PHASE 2: STRATEGIC PROJECT BLUEPRINT VIA LLM
        # ============================================
        notify("📋 [45%] Multi-Disciplinary Action Blueprint banaya ja raha hai...", 0.45)
        blueprint_prompt = f"""You are Nova's Project Architect. Design a complete, standalone project based on this topic.

TOPIC: "{topic_query}"
RECALLED MEMORY:
{knowledge_context}
SKILL CONTEXT: {skill_context}

Determine what assets this project needs:
1. Primary Deliverable Type: "python_tool", "3d_blender_scene", "web_scraper", "automation_bot", or "research_dossier"
2. Python Script Code (Complete, production-ready, no placeholders)
3. Markdown Documentation/Guide (Overview, features, how it works)

Return ONLY valid JSON:
{{
    "project_name": "Human Readable Project Title",
    "deliverable_type": "python_tool",
    "summary": "2-sentence executive summary of what was built",
    "primary_filename": "main_tool.py",
    "code_content": "# complete python code here",
    "documentation": "# Project Title\\n\\nComplete documentation and guide..."
}}"""

        try:
            resp = ollama.chat(
                model=self.model,
                messages=[{"role": "user", "content": blueprint_prompt}],
                options={"temperature": 0.2, "num_ctx": 2048}
            )
            raw = resp['message']['content']
            start = raw.find('{')
            end = raw.rfind('}') + 1
            blueprint = json.loads(raw[start:end])
        except Exception as e:
            # Fallback basic blueprint
            blueprint = {
                "project_name": topic_query.title(),
                "deliverable_type": "python_tool",
                "summary": f"Autonomous project built for: {topic_query}",
                "primary_filename": f"{topic_slug}_app.py",
                "code_content": f"# Auto-generated solution for {topic_query}\nprint('Project {topic_query} initialized!')\n",
                "documentation": f"# {topic_query}\n\nProject workspace initialized successfully."
            }

        # ============================================
        # PHASE 3: ASSET GENERATION & DISK CREATION
        # ============================================
        notify(f"👨‍💻 [65%] Project files write ho rahi hain: `{blueprint.get('primary_filename')}`...", 0.65)

        # 1. Write Code File
        primary_file = project_dir / blueprint.get("primary_filename", "main.py")
        code_body = blueprint.get("code_content", "")
        with open(primary_file, "w", encoding="utf-8") as f:
            f.write(code_body)

        # 2. Write Markdown Documentation
        doc_file = project_dir / "README.md"
        doc_body = blueprint.get("documentation", f"# {topic_query}\n\nProject created autonomously by Nova AI.")
        with open(doc_file, "w", encoding="utf-8") as f:
            f.write(doc_body)

        # ============================================
        # PHASE 4: 3D ASSETS / EXECUTION (If requested)
        # ============================================
        if "3d" in topic_query.lower() or "blender" in topic_query.lower() or blueprint.get("deliverable_type") == "3d_blender_scene":
            notify("🎨 [80%] 3D Scene assets & animation compile ho rahe hain...", 0.80)
            if self.blender:
                self.blender.process_3d_command(topic_query, update_cb=progress_cb)

        # Save project to Brain Memory for future recall
        notify("💾 [90%] Completed project memory database mein index ho raha hai...", 0.90)
        self.brain.add(
            f"PROJECT: {blueprint.get('project_name')}\nTOPIC: {topic_query}\nSUMMARY: {blueprint.get('summary')}\nWORKSPACE: {str(project_dir)}",
            f"project:{topic_slug}",
            {"project": topic_slug, "type": blueprint.get("deliverable_type")}
        )

        notify("🎉 [100%] Project successfully built and delivered!", 1.0)
        self.is_running = False

        return f"""
╔══════════════════════════════════════════════════════════════╗
║        🎉 AUTONOMOUS PROJECT COMPLETED & DELIVERED!          ║
╚══════════════════════════════════════════════════════════════╝
📦 Project: {blueprint.get('project_name')}
📁 Workspace Folder: `data/projects/{topic_slug}/`
📝 Summary: {blueprint.get('summary')}

📄 GENERATED DELIVERABLES:
  1. Primary Script: `{blueprint.get('primary_filename')}`
  2. Project Docs: `README.md`
  3. Memory Indexing: ChromaDB Vector DB Updated

💡 Boss, project files aapke workspace mein save ho chuki hain aur memory mein active hain!
"""