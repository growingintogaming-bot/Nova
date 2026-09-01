"""
🕐 NOVA AUTONOMOUS SCHEDULER
- Background daemon checking jobs every 5 seconds
- Timers, recurring daily tasks, and delayed execution
- Persists schedules to data/schedules.json
"""

import os
import re
import json
import time
import threading
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCHEDULE_FILE = BASE_DIR / "data" / "schedules.json"


class TaskScheduler:
    def __init__(self, callback_func=None):
        self.callback = callback_func  # Function to trigger (e.g. app.on_scheduled_task)
        self.tasks = self._load()
        self.running = True
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()
        print(f"🕐 Autonomous Scheduler started with {len(self.tasks)} active tasks.")

    def _load(self) -> list:
        if SCHEDULE_FILE.exists():
            try:
                with open(SCHEDULE_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        return []

    def _save(self):
        SCHEDULE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(SCHEDULE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, description: str, execute_at_timestamp: float, recurring_interval_sec: float = None):
        task = {
            "id": int(time.time() * 1000),
            "description": description,
            "execute_at": execute_at_timestamp,
            "recurring_sec": recurring_interval_sec,
            "created_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        self.tasks.append(task)
        self._save()
        dt_str = datetime.fromtimestamp(execute_at_timestamp).strftime("%H:%M:%S")
        return f"⏰ Task scheduled: '{description}' at {dt_str}"

    def parse_and_schedule(self, natural_command: str) -> str:
        """Parses natural language commands like 'remind me in 10 minutes to take medicine'"""
        low = natural_command.lower()
        now = time.time()

        # 1. In X minutes / seconds
        min_match = re.search(r"(\d+)\s*(?:minute|min|m)\b", low)
        sec_match = re.search(r"(\d+)\s*(?:second|sec|s)\b", low)
        hour_match = re.search(r"(\d+)\s*(?:hour|hr|h)\b", low)

        delay_seconds = 0
        if min_match:
            delay_seconds += int(min_match.group(1)) * 60
        if sec_match:
            delay_seconds += int(sec_match.group(1))
        if hour_match:
            delay_seconds += int(hour_match.group(1)) * 3600

        # Clean description
        desc = re.sub(r"(?:remind me|schedule|baad|in \d+\s*\w+|ko|mujhe)\s*", "", natural_command, flags=re.IGNORECASE).strip()
        if not desc:
            desc = "Scheduled Reminder Task"

        if delay_seconds > 0:
            exec_time = now + delay_seconds
            return self.add_task(desc, exec_time)

        # 2. Daily at HH:MM (e.g., 'roz 09:30 baje')
        time_match = re.search(r"(\d{1,2}):(\d{2})", low)
        if time_match:
            h = int(time_match.group(1))
            m = int(time_match.group(2))
            target_dt = datetime.now().replace(hour=h, minute=m, second=0, microsecond=0)
            if target_dt.timestamp() <= now:
                target_dt += timedelta(days=1)
            return self.add_task(desc, target_dt.timestamp(), recurring_interval_sec=86400)

        return "❌ Time samajh nahi aaya. Example: 'remind me in 10 minutes to stretch' ya 'roz 09:00 baje meeting'"

    def _loop(self):
        while self.running:
            now = time.time()
            remaining = []

            for task in self.tasks:
                if now >= task["execute_at"]:
                    print(f"\n🔔 EXECUTING SCHEDULED TASK: {task['description']}")
                    if self.callback:
                        self.callback(task["description"])

                    # If recurring, reschedule
                    if task.get("recurring_sec"):
                        task["execute_at"] = now + task["recurring_sec"]
                        remaining.append(task)
                else:
                    remaining.append(task)

            if len(remaining) != len(self.tasks):
                self.tasks = remaining
                self._save()

            time.sleep(5)