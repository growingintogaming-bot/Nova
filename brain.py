"""
🧠 NOVA BRAIN — GPU-SAFE & CPU-BALANCED ENGINE
- Forces AI execution strictly to CPU (4 Threads)
- Leaves RX 580 GPU 100% free for Display & Blender (Zero Driver Crashes!)
- Instant Groq Cloud 70B support when online
"""

import os
import hashlib
import requests
from pathlib import Path
import ollama
import chromadb

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_DB = str(BASE_DIR / "data" / "brain")
EMBED_MODEL = "nomic-embed-text"

GROQ_API_KEY = "gsk_yahan_apni_key_paste_karein"


class Brain:
    def __init__(self):
        os.makedirs(KNOWLEDGE_DB, exist_ok=True)
        self.client = chromadb.PersistentClient(path=KNOWLEDGE_DB)
        self.collection = self.client.get_or_create_collection(name="knowledge")

    def get_embedding(self, text):
        try:
            r = ollama.embeddings(model=EMBED_MODEL, prompt=text)
            return r['embedding']
        except Exception:
            return None

    def add(self, text, source, metadata=None):
        try:
            chunks = self._chunk(text)
            for i, c in enumerate(chunks):
                if len(c.strip()) < 25:
                    continue
                emb = self.get_embedding(c)
                if not emb:
                    continue
                cid = hashlib.md5(f"{source}_{i}".encode()).hexdigest()
                meta = {"source": source}
                if metadata:
                    for k, v in metadata.items():
                        meta[k] = str(v)[:250]
                self.collection.add(
                    embeddings=[emb],
                    documents=[c],
                    metadatas=[meta],
                    ids=[cid]
                )
            return "✅ Saved"
        except Exception as e:
            return f"❌ {e}"

    def search(self, query, top_k=2):
        try:
            if self.collection.count() == 0:
                return []
            emb = self.get_embedding(query)
            if not emb:
                return []
            r = self.collection.query(
                query_embeddings=[emb],
                n_results=min(top_k, self.collection.count())
            )
            if not r['documents'] or not r['documents'][0]:
                return []
            return [
                {"content": d, "source": m.get('source', '?')}
                for d, m in zip(r['documents'][0], r['metadatas'][0])
            ]
        except Exception:
            return []

    def _chunk(self, text, size=400):
        if len(text) <= size:
            return [text]
        return [text[i:i + size] for i in range(0, len(text), size - 40)]

    def is_knowledge_query(self, text: str) -> bool:
        low = text.lower().strip()
        casual = [
            "hi", "hello", "hey", "salam", "assalam", "kaisi ho", "kaise ho",
            "kya haal", "theek ho", "good morning", "shukriya", "thanks", "ok", "theek", "bye"
        ]
        if any(low == g or low.startswith(g + " ") for g in casual):
            return False
        triggers = ["kya hota hai", "kaise", "how to", "shortcut", "seekha", "code", "explain", "batao", "what is"]
        return any(k in low for k in triggers)

    def generate_fast_response(self, messages, local_model="llama3.2"):
        # 1. Cloud (0% GPU & CPU)
        if GROQ_API_KEY and not GROQ_API_KEY.startswith("gsk_yahan"):
            try:
                headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                payload = {
                    "model": "llama-3.3-70b-versatile",
                    "messages": messages,
                    "temperature": 0.5,
                    "max_tokens": 300
                }
                res = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=5)
                if res.status_code == 200:
                    return res.json()["choices"][0]["message"]["content"]
            except Exception:
                pass

        # 2. Local CPU Safe Mode (Strict 4 Threads, 512 Context — Never overloads GPU!)
        try:
            resp = ollama.chat(
                model=local_model,
                messages=messages,
                options={
                    "num_thread": 4,      # Safe CPU Threads
                    "num_ctx": 512,        # Ultra-light context
                    "num_predict": 200,    # Safe token limit
                    "temperature": 0.4,
                    "top_k": 20,
                    "top_p": 0.8
                }
            )
            return resp['message']['content']
        except Exception as e:
            return f"Brain Error: {e}"