"""
🎓 NOVA SOFTWARE MASTERY ENGINE (v4.0 — Quality-First Deep Learning)
- Hyper-specific prompts that extract REAL professional knowledge
- Every shortcut, workflow, glitch, and industry secret saved to brain
- Learning takes time but results are PROFESSIONAL GRADE
- During execution, recalls saved knowledge for impressive output
"""

import os
import json
import time
import threading
from pathlib import Path
import ollama

BASE_DIR = Path(__file__).resolve().parent
MASTERY_DIR = BASE_DIR / "data" / "software_mastery"
MASTERY_DIR.mkdir(parents=True, exist_ok=True)


class SoftwareMasteryEngine:

    # ============================================
    # 🎯 DEEP PROFESSIONAL CURRICULUM
    # Each topic has a hyper-specific prompt that forces
    # the LLM to output REAL expert-level knowledge
    # ============================================
    DEEP_CURRICULUM = {
        "blender": [
            {
                "id": "interface_navigation",
                "title": "Interface & Navigation Mastery",
                "prompt": """You are a Senior Blender Technical Director at a VFX studio.
Explain Blender 4.x interface and navigation in DEEP DETAIL.

Cover ALL of these with EXACT values and shortcuts:

1. VIEWPORT NAVIGATION:
   - Orbit (MMB), Pan (Shift+MMB), Zoom (Scroll)
   - Numpad views (1=Front, 3=Right, 7=Top, 5=Ortho toggle)
   - Fly mode (Shift+`) vs Walk mode — exact settings
   - Local view isolation (Numpad /) — when and why pros use it
   - Camera lock to view (N-panel > View > Lock Camera to View)

2. ESSENTIAL PANELS:
   - N-Panel (N key) — which tabs matter: Item, View, Tool
   - T-Panel (T key) — tool settings
   - Properties Panel — exact tab order and what each does
   - Outliner — display modes (View Layer vs Collections)
   - Timeline vs Dope Sheet vs Graph Editor — when to use which

3. WORKSPACE SWITCHING:
   - Layout > Modeling > Sculpting > UV Editing > Texture Paint > Shading > Animation > Rendering > Compositing
   - Custom workspace creation shortcut

4. PERFORMANCE SETTINGS:
   - Viewport Shading modes (Wireframe > Solid > Material Preview > Rendered)
   - Simplify settings (Render > Simplify > Max Subdivision)
   - VSync and undo steps (Edit > Preferences > System)
   - The ONE setting that causes 90% of viewport lag

Return a JSON object with:
{
    "topic": "Interface & Navigation",
    "shortcuts": [{"keys": "exact keys", "action": "what it does", "pro_context": "when/why pros use it"}],
    "panels": [{"name": "panel name", "key": "shortcut", "important_tabs": ["tab1"]}],
    "workspaces": ["list of workspaces with purpose"],
    "performance_tips": ["exact setting with value"],
    "hidden_features": ["feature most users miss"]
}"""
            },
            {
                "id": "modeling_topology",
                "title": "Professional Modeling & Topology",
                "prompt": """You are a Lead 3D Modeler at Pixar/Disney.
Teach PROFESSIONAL modeling techniques in Blender with EXACT details.

Cover ALL:

1. MESH PRIMITIVES & WHEN TO USE:
   - Cube vs UV Sphere vs Ico Sphere vs Cylinder — exact use cases
   - Subdivision levels for game (1-2) vs film (3-4) vs close-up (5-6)

2. TOPOLOGY RULES (CRITICAL):
   - Why quads ONLY for animation (deformation)
   - Where to place poles (5-edge vertices) — NEVER on deformation areas
   - Edge flow for facial animation (loops around eyes, mouth)
   - Ngons — when acceptable (flat surfaces, no deformation) vs NEVER
   - Triangle usage — only in final game export, never during modeling

3. ESSENTIAL MODELING TOOLS (with exact shortcuts):
   - Extrude (E) vs Extrude Individual vs Extrude Along Normals
   - Inset (I) — exact use for face detailing
   - Bevel (Ctrl+B) — segments, profile, clamp overlap settings
   - Loop Cut (Ctrl+R) — even cuts, edge slide
   - Knife (K) — angle snap (Ctrl), cut through (Z)
   - Bridge Edge Loops — connecting two edge rings
   - Spin tool — for cylindrical objects
   - Poly Build — for retopology

4. MODIFIER STACK ORDER (PROFESSIONAL):
   - Mirror → Armature → Subdivision Surface → Bevel
   - WHY this order matters (Mirror before Subsurf = clean symmetry)
   - When to Apply vs Keep Live

5. HARD SURFACE vs ORGANIC:
   - Hard surface: Boolean + Bevel + Weighted Normals
   - Organic: Sculpt + Multires + Dyntopo settings

Return JSON:
{
    "topic": "Professional Modeling",
    "topology_rules": [{"rule": "exact rule", "why": "reason", "exception": "when to break"}],
    "modeling_tools": [{"tool": "name", "shortcut": "keys", "settings": "exact values", "use_case": "when"}],
    "modifier_order": ["ordered list with reasoning"],
    "hard_surface_workflow": ["step by step"],
    "organic_workflow": ["step by step"],
    "quality_checks": ["check before finalizing"],
    "common_glitches": [{"glitch": "problem", "cause": "why", "fix": "exact solution"}]
}"""
            },
            {
                "id": "materials_pbr",
                "title": "PBR Materials & Texturing",
                "prompt": """You are a Senior LookDev Artist at ILM/Weta Digital.
Teach PROFESSIONAL PBR material creation in Blender with EXACT values.

Cover ALL:

1. PRINCIPLED BSDF COMPLETE BREAKDOWN:
   - Base Color: sRGB values, when to use texture vs solid
   - Metallic: 0.0 (dielectric) vs 1.0 (conductor) — NEVER in between except edge cases
   - Roughness: 0.0 (mirror) to 1.0 (chalk) — real-world values for common materials
   - IOR: 1.45 (glass), 1.52 (crown glass), 2.42 (diamond), 1.0 (air)
   - Normal map: strength 0.5-1.0, tangent space vs object space
   - Clearcoat: for car paint, lacquered wood (0.5-1.0)
   - Sheen: for fabric, velvet (0.3-0.8)
   - Transmission: for glass, liquids (1.0 = fully transparent)
   - Emission: for screens, LEDs, neon (strength 5-50)

2. REAL-WORLD PBR VALUES (Exact):
   - Gold: Base=#FFD700, Metallic=1.0, Roughness=0.15
   - Chrome: Base=#FFFFFF, Metallic=1.0, Roughness=0.05
   - Rubber: Base=#1A1A1A, Metallic=0.0, Roughness=0.85
   - Skin: Base=#E8B89D, Metallic=0.0, Roughness=0.6, SSS=0.3
   - Glass: Base=#FFFFFF, Metallic=0.0, Roughness=0.0, Transmission=1.0, IOR=1.45
   - Concrete: Base=#808080, Metallic=0.0, Roughness=0.95
   - Wood: Base=#8B6914, Metallic=0.0, Roughness=0.7

3. NODE RECIPES (Procedural):
   - Brushed Metal: Noise Texture(0.5) → ColorRamp → Roughness
   - Scratches: Voronoi → ColorRamp → Bump → Normal
   - Dust Layer: Noise → ColorRamp → Mix Shader (Dust/Original)
   - Fingerprints: Noise(200) → Bump(0.02) → Roughness

4. UV UNWRAPPING:
   - Seam placement strategy (hide seams in less visible areas)
   - Smart UV Project vs Unwrap vs Lightmap Pack
   - Texel density — consistent across all objects

5. COLOR MANAGEMENT:
   - AgX (Blender 4.0+) vs Filmic — AgX is better for realistic highlights
   - View Transform: AgX, Look: High Contrast for cinematic
   - Display Device: sRGB for monitors

Return JSON:
{
    "topic": "PBR Materials",
    "principled_bsdf": [{"slider": "name", "range": "0-1", "real_values": {"material": "value"}}],
    "pbr_library": [{"material": "name", "base_color": "hex", "metallic": 0.0, "roughness": 0.0, "extra": {}}],
    "node_recipes": [{"name": "effect", "nodes": "exact node chain", "settings": "values"}],
    "uv_workflow": ["step by step"],
    "color_management": {"view_transform": "AgX", "look": "High Contrast"}
}"""
            },
            {
                "id": "lighting_cinematic",
                "title": "Cinematic Lighting & Rendering",
                "prompt": """You are a Director of Photography who uses Blender for pre-visualization.
Teach PROFESSIONAL cinematic lighting with EXACT Blender values.

Cover ALL:

1. THREE-POINT LIGHTING (Exact Blender Setup):
   - Key Light: Area Light, Size=5m, Energy=500W, Color=FFF5E0 (warm), Angle=45° high, 30° side
   - Fill Light: Area Light, Size=8m, Energy=150W (1/3 of key), Color=E0E8FF (cool), opposite side
   - Rim/Back Light: Area Light, Size=3m, Energy=300W, Color=FFFFFF, behind subject, high angle
   - WHY these ratios: Key:Fill = 3:1 for dramatic, 2:1 for commercial

2. HDRI WORKFLOW:
   - World Properties > Surface > Environment Texture
   - Best free HDRIs: Poly Haven (polyhaven.com)
   - Rotation for mood: 0°=front light, 90°=side, 180°=back
   - Strength: 0.5-1.0 for subtle, 2.0-3.0 for dominant
   - Mapping: Equirectangular

3. VOLUMETRIC LIGHTING (God Rays):
   - Add Volume Scatter to World: Density=0.02, Anisotropy=0.7
   - Add Volume Absorption for colored fog: Density=0.01
   - Light energy must be HIGH (1000W+) to penetrate volume
   - Render Samples: 256+ for clean volumetrics

4. PRACTICAL LIGHTS:
   - Neon signs: Mesh with Emission shader, Strength=20-50
   - Screens/monitors: Emission + Light Probe (Irradiance Volume)
   - Car headlights: Spot Light, Angle=30°, Blend=0.5, Energy=500W

5. EEVEE PRO SETTINGS (Make it look like Cycles):
   - Render > Bloom: ON, Threshold=0.8, Knee=0.5, Radius=5, Intensity=0.3
   - Render > Screen Space Reflections: ON, Refraction ON
   - Render > Shadows: High (1024px), Soft Shadows ON
   - Render > Ambient Occlusion: ON, Distance=0.5m, Factor=0.5
   - Render > Motion Blur: ON, Shutter=0.5
   - Render > Color Management: AgX, High Contrast
   - Samples: Render=64, Viewport=32

6. RENDER EXPORT (YouTube Professional):
   - Resolution: 1920x1080 (or 3840x2160 for 4K)
   - Frame Rate: 24fps (cinematic) or 30fps (YouTube)
   - Output: FFmpeg Video, Container=MPEG-4
   - Codec: H.264, Quality: CRF 18 (visually lossless)
   - Audio: AAC, 320kbps

Return JSON:
{
    "topic": "Cinematic Lighting",
    "three_point": {"key": {"type": "Area", "energy": 500, "color": "#FFF5E0"}, "fill": {}, "rim": {}},
    "hdri_setup": {"source": "polyhaven.com", "strength": 1.0},
    "volumetric": {"density": 0.02, "anisotropy": 0.7},
    "eevee_settings": {"bloom": {}, "ssr": {}, "shadows": {}, "ao": {}},
    "export_youtube": {"resolution": "1920x1080", "fps": 24, "codec": "H.264", "crf": 18},
    "lighting_mistakes": ["mistake and fix"]
}"""
            },
            {
                "id": "animation_rigging",
                "title": "Animation & Rigging Mastery",
                "prompt": """You are a Senior Character Animator at DreamWorks Animation.
Teach PROFESSIONAL animation and rigging in Blender with EXACT techniques.

Cover ALL:

1. 12 PRINCIPLES OF ANIMATION (Applied in Blender):
   - Squash & Stretch: Scale keyframes (Z=0.7, XY=1.2 at impact)
   - Anticipation: 3-5 frames before main action (pull back before jump)
   - Staging: Camera angle + lighting to focus attention
   - Straight Ahead vs Pose-to-Pose: Use pose-to-pose for control
   - Follow Through: Hair/cloth continues 5-10 frames after stop
   - Slow In/Out: Bezier handles in Graph Editor (Auto Clamped)
   - Arcs: Motion paths should curve, not straight lines
   - Secondary Action: Subtle breathing, blinking during dialogue
   - Timing: 24fps standard — walk cycle = 24 frames (1 sec)
   - Exaggeration: Push poses 20-30% beyond realistic
   - Solid Drawing: Maintain volume during squash/stretch
   - Appeal: Silhouette test — pose readable in shadow

2. GRAPH EDITOR MASTERY:
   - Handle types: Auto, Aligned, Free, Vector, Auto Clamped
   - PRO TIP: Use Auto Clamped for natural motion (no overshoot)
   - Ease In: Handle pulled RIGHT (slow start)
   - Ease Out: Handle pulled LEFT (slow end)
   - Bounce: Cycle modifier with decay
   - Keyframe interpolation: Bezier (default) vs Linear (robotic) vs Constant (snappy)

3. RIGGING WORKFLOW:
   - Armature creation: Shift+A > Armature > Single Bone
   - Bone hierarchy: Root > Spine > Chest > Neck > Head
   - IK vs FK: IK for legs/feet (ground contact), FK for arms (swinging)
   - Weight painting: Normalize All, Auto Normalize ON
   - Rigify addon: Add > Armature > Human (Meta-Rig) → Generate Rig
   - Bone constraints: Copy Rotation, Limit Location, Stretch To

4. WALK CYCLE (Exact Keyframes at 24fps):
   - Frame 1: Contact (right foot forward, left back)
   - Frame 4: Down (lowest point, weight on right)
   - Frame 7: Passing (left foot passes right)
   - Frame 10: Up (highest point, weight shifting)
   - Frame 13: Contact (left foot forward) — mirror of Frame 1
   - Frame 24: Back to Frame 1 (loop)

5. CAMERA ANIMATION:
   - Focal length: 35mm (wide), 50mm (standard), 85mm (portrait), 200mm (telephoto)
   - Depth of Field: F-Stop 2.8 (shallow) to 16 (deep)
   - Track To constraint for following subjects
   - Dolly zoom: Animate focal length + position simultaneously

Return JSON:
{
    "topic": "Animation & Rigging",
    "twelve_principles": [{"principle": "name", "blender_how": "exact technique", "frames": "timing"}],
    "graph_editor": [{"handle": "type", "when": "use case", "effect": "motion feel"}],
    "rigging_workflow": ["step by step with shortcuts"],
    "walk_cycle": {"fps": 24, "keyframes": [{"frame": 1, "pose": "contact"}]},
    "camera_settings": [{"focal": "35mm", "use": "wide establishing shot"}],
    "timing_secrets": ["pro timing tips"]
}"""
            },
            {
                "id": "vfx_compositing",
                "title": "VFX, Compositing & Final Polish",
                "prompt": """You are a VFX Compositor at a major film studio.
Teach PROFESSIONAL compositing and final polish in Blender.

Cover ALL:

1. COMPOSITOR NODE TREE (Cinematic Look):
   - Render Layers → Color Balance (Lift/Gamma/Gain) → Glare → Lens Distortion → Composite
   - Color Balance values: Lift=shadows (cool blue), Gamma=midtones, Gain=highlights (warm)
   - Glare node: Type=Streaks, Streaks=8, Threshold=0.9, Mix=0.3
   - Lens Distortion: Dispersion=0.02 (subtle chromatic aberration)

2. RENDER PASSES (Multi-Layer Workflow):
   - Beauty (combined) + Ambient Occlusion + Mist + Emission + Normal + Z-Depth
   - How to enable: View Layer Properties > Passes
   - Cryptomatte: For isolating objects without re-rendering

3. MOTION BLUR (Realistic Speed):
   - Render > Motion Blur: ON
   - Shutter: 0.5 (standard), 1.0 (dreamy), 0.25 (crisp action)
   - Object vs Camera blur: Both ON for realism
   - Rolling Shutter: For fast camera pans

4. DEPTH OF FIELD:
   - Camera > Depth of Field: ON
   - Focus Object: Select target object
   - F-Stop: 2.8 (cinematic shallow), 5.6 (moderate), 11 (landscape deep)
   - Blades: 6-8 for realistic bokeh shape

5. FINAL 5% POLISH (What separates pro from amateur):
   - Vignette: Lens Distortion node, Dispersion=-0.05 (darken edges)
   - Film Grain: Texture > Noise > Mix with original (Factor=0.02-0.05)
   - Chromatic Aberration: Separate RGB → Shift R/B channels 1-2px → Combine
   - Color Grading LUT: Import .cube file via Color Management
   - Sharpening: Filter > Sharpen (Factor=0.3) — subtle only
   - Letterboxing: Black bars for cinematic aspect ratio (2.39:1)

6. BLOOM THAT LOOKS NATURAL (Not overdone):
   - Threshold: 0.8-0.9 (only brightest areas)
   - Knee: 0.5 (smooth falloff)
   - Radius: 5-8 (spread)
   - Intensity: 0.2-0.4 (subtle)
   - Color: Match scene temperature

Return JSON:
{
    "topic": "VFX & Compositing",
    "compositor_tree": ["exact node chain with values"],
    "render_passes": ["list of passes to enable"],
    "motion_blur": {"shutter": 0.5, "type": "object+camera"},
    "dof": {"fstop": 2.8, "blades": 6},
    "final_polish": [{"effect": "vignette", "node": "exact setup", "value": 0.05}],
    "bloom_pro": {"threshold": 0.85, "knee": 0.5, "radius": 6, "intensity": 0.3},
    "amateur_vs_pro": ["difference and how to fix"]
}"""
            }
        ]
    }

    def __init__(self, brain, skill_matrix, learner, blender_controller, model="llama3.2"):
        self.brain = brain
        self.skill_matrix = skill_matrix
        self.learner = learner
        self.blender = blender_controller
        self.model = model

    # ============================================
    # 🎓 DEEP MASTERY (Quality-First, Time-No-Problem)
    # ============================================
    def master_software_autonomously(self, software_name: str, progress_cb=None) -> str:
        """Deep studies software with professional-grade prompts"""

        def notify(msg, pct=None):
            if progress_cb:
                progress_cb(msg, pct, "learn")

        software_key = software_name.lower().replace(" ", "_").strip()
        notify(f"🎓 [2%] Starting Deep Professional Mastery: {software_name}", 0.02)
        time.sleep(0.5)

        # Get curriculum
        curriculum = self.DEEP_CURRICULUM.get(software_key)
        if not curriculum:
            curriculum = self._generate_curriculum(software_name)

        total_topics = len(curriculum)
        all_knowledge = {}

        notify(f"📋 [5%] Curriculum loaded: {total_topics} deep topics to master", 0.05)
        notify(f"⏱️ Estimated time: {total_topics * 2}-{total_topics * 3} minutes (Quality takes time!)", 0.06)
        time.sleep(1.0)

        for idx, lesson in enumerate(curriculum):
            topic_id = lesson.get("id", f"topic_{idx}")
            title = lesson.get("title", f"Topic {idx+1}")
            prompt = lesson.get("prompt", "")

            base_pct = 0.05 + (idx / total_topics) * 0.90
            notify(f"\n{'━' * 50}", base_pct)
            notify(f"📚 [{int(base_pct*100)}%] DEEP STUDY: {title}", base_pct)
            notify(f"   This will take 1-3 minutes for professional quality...", base_pct + 0.01)

            # Live ticker while LLM generates
            topic_done = [False]
            topic_result = [None]
            topic_error = [None]

            def run_llm(p=prompt):
                try:
                    resp = ollama.chat(
                        model=self.model,
                        messages=[{"role": "user", "content": p}],
                        options={
                            "num_ctx": 2048,      # Full context for detailed knowledge
                            "num_predict": 800,    # Detailed output
                            "num_thread": 4,       # Balanced for i7 3rd Gen
                            "temperature": 0.15,   # Factual, not creative
                            "top_k": 20,
                            "top_p": 0.8
                        }
                    )
                    topic_result[0] = resp['message']['content']
                except Exception as e:
                    topic_error[0] = str(e)
                finally:
                    topic_done[0] = True

            worker = threading.Thread(target=run_llm, daemon=True)
            worker.start()

            # Live ticker updates
            tick_msgs = [
                "   🧠 Analyzing professional techniques...",
                "   ⌨️ Extracting keyboard shortcuts...",
                "   🔧 Compiling workflow steps...",
                "   ⚠️ Identifying common glitches...",
                "   💡 Gathering industry secrets...",
                "   📊 Formatting professional data...",
                "   ✅ Finalizing knowledge base..."
            ]
            tick = 0
            start = time.time()

            while not topic_done[0]:
                elapsed = time.time() - start
                if int(elapsed) % 4 == 0 and int(elapsed) > 0:
                    msg = tick_msgs[tick % len(tick_msgs)]
                    micro_pct = base_pct + min(elapsed / 180.0, 1.0) * (0.90 / total_topics)
                    notify(f"{msg} [{int(elapsed)}s]", micro_pct)
                    tick += 1
                time.sleep(1)

            # Process result
            if topic_result[0]:
                raw = topic_result[0]
                try:
                    s = raw.find('{')
                    e = raw.rfind('}') + 1
                    if s >= 0 and e > s:
                        parsed = json.loads(raw[s:e])
                    else:
                        parsed = {"raw_knowledge": raw[:3000]}
                except json.JSONDecodeError:
                    parsed = {"raw_knowledge": raw[:3000]}

                all_knowledge[topic_id] = {
                    "title": title,
                    "data": parsed
                }

                # Save to ChromaDB with rich metadata
                knowledge_text = json.dumps(parsed, indent=2, ensure_ascii=False)
                self.brain.add(
                    knowledge_text,
                    f"pro:{software_key}:{topic_id}",
                    {
                        "software": software_key,
                        "topic": title[:60],
                        "level": "professional",
                        "type": "deep_mastery",
                        "topic_id": topic_id
                    }
                )

                # Count what was saved
                shortcuts_count = len(parsed.get("shortcuts", parsed.get("pro_shortcuts", parsed.get("modeling_tools", []))))
                notify(f"   ✅ SAVED: {title} ({shortcuts_count} shortcuts/tips stored)", base_pct + (0.90 / total_topics))
            else:
                err = topic_error[0] or "Unknown error"
                notify(f"   ⚠️ FAILED: {title} — {err[:60]}", base_pct + (0.90 / total_topics))

        # Save mastery profile
        notify(f"\n💾 [97%] Saving complete mastery profile...", 0.97)

        mastery_file = MASTERY_DIR / f"{software_key}_deep_mastery.json"
        profile = {
            "software": software_name,
            "software_key": software_key,
            "mastery_level": "expert" if len(all_knowledge) >= 5 else "advanced" if len(all_knowledge) >= 3 else "intermediate",
            "topics_studied": len(all_knowledge),
            "total_topics": total_topics,
            "topic_details": {k: v["title"] for k, v in all_knowledge.items()},
            "completed_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(mastery_file, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=2)

        notify(f"🎉 [100%] DEEP MASTERY COMPLETE: {software_name}!", 1.0)

        topics_list = "\n".join([f"   ✅ {v['title']}" for v in all_knowledge.values()])

        return f"""
╔══════════════════════════════════════════════════════════════╗
║      🎓 DEEP PROFESSIONAL MASTERY ACHIEVED!                  ║
╚══════════════════════════════════════════════════════════════╝
📚 Software: {software_name}
🏆 Level: {profile['mastery_level'].upper()}
📖 Topics Mastered: {len(all_knowledge)}/{total_topics}

📋 DEEP KNOWLEDGE STORED IN BRAIN:
{topics_list}

💾 What's Now in Nova's Memory:
   • Exact keyboard shortcuts with pro context
   • Real-world PBR material values
   • Cinematic lighting setups with energy values
   • Animation timing & keyframe data
   • Render/export settings for YouTube/Film
   • Common glitches & prevention methods
   • Industry secrets & hidden features

🎬 Ab jab bhi aap {software_name} ka kaam denge,
   Nova yeh professional knowledge RECALL karke use karegi!
"""

    def _generate_curriculum(self, software_name: str) -> list:
        """Generate curriculum for unknown software"""
        return [
            {
                "id": "fundamentals",
                "title": f"{software_name} Fundamentals & Interface",
                "prompt": f"You are a world-class {software_name} expert. Provide DEEP professional knowledge about {software_name} fundamentals. Include exact shortcuts, interface navigation, workspace setup, performance tips. Return JSON with: shortcuts, workflow_tips, common_mistakes, hidden_features, performance_tips."
            },
            {
                "id": "core_techniques",
                "title": f"{software_name} Core Professional Techniques",
                "prompt": f"You are a senior {software_name} professional. Provide ADVANCED techniques with exact values and step-by-step workflows. Include industry standards, quality checks, glitch prevention. Return JSON with: techniques, industry_standards, quality_checks, common_glitches."
            },
            {
                "id": "expert_mastery",
                "title": f"{software_name} Expert-Level Mastery",
                "prompt": f"You are a master-level {software_name} artist. Provide EXPERT knowledge: optimization, automation, advanced features, industry secrets, export settings. Return JSON with: expert_techniques, optimization, automation, export_settings, industry_secrets."
            }
        ]

    # ============================================
    # 🎬 EXECUTE WITH RECALLED KNOWLEDGE
    # ============================================
    def execute_animation_from_script(self, software_name: str, user_script: str, progress_cb=None) -> str:
        """Execute animation using recalled professional knowledge"""
        def notify(msg, pct=None):
            if progress_cb:
                progress_cb(msg, pct, "action")

        notify(f"🎬 [10%] Analyzing: '{user_script[:50]}'...", 0.10)

        # Recall deep knowledge from brain
        notify("🧠 [30%] Recalling professional knowledge from memory...", 0.30)
        memories = self.brain.search(f"{software_name} {user_script[:40]}", top_k=5)
        knowledge = "\n".join([f"- {m['content'][:500]}" for m in memories])

        if "blender" in software_name.lower() and self.blender:
            notify("🎨 [60%] Building professional Blender scene...", 0.60)
            enhanced = f"{user_script}\n\nPROFESSIONAL KNOWLEDGE TO APPLY:\n{knowledge[:2000]}"
            return self.blender.process_3d_command(enhanced, update_cb=progress_cb)

        return f"🎬 Plan ready for '{user_script}' in {software_name}!"

    def get_mastery_status(self) -> str:
        if not MASTERY_DIR.exists():
            return "📚 No mastery yet. Try: 'learn blender' or 'deep study blender'"
        files = list(MASTERY_DIR.glob("*_mastery.json")) + list(MASTERY_DIR.glob("*_deep_mastery.json"))
        if not files:
            return "📚 No mastery yet."
        output = "╔══════════════════════════════════════════════════════════════╗\n"
        output += "║    🎓 NOVA MASTERY STATUS                                    ║\n"
        output += "╚══════════════════════════════════════════════════════════════╝\n\n"
        for mf in files:
            try:
                with open(mf, "r", encoding="utf-8") as f:
                    data = json.load(f)
                output += f"🎯 {data.get('software')}\n"
                output += f"   Level: {data.get('mastery_level', 'N/A').upper()}\n"
                output += f"   Topics: {data.get('topics_studied', 0)}\n"
                output += f"   Date: {data.get('completed_at', 'N/A')}\n\n"
            except:
                pass
        return output