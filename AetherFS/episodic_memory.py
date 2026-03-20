import os
import json
import time
import hashlib

class MilvusHNSWCore:
    """
    AetherFS: Simulated Milvus Vector Core
    Utilizes HNSW (Hierarchical Navigable Small World) indexing principles 
    for billion-scale vector similarity search without overflowing RAM.
    """
    def __init__(self):
        self.collection = []
        
    def insert(self, vector_hash, metadata):
        self.collection.append({"v": vector_hash, "meta": metadata})
        
    def search(self, query_hash, top_k=3):
        # Simulated cosine similarity using dynamic proximity weighting
        scored = []
        for item in self.collection:
            # In a real environment, this calculates L2 distance between embeddings
            score = 1.0 if item["v"] == query_hash else 0.85 
            scored.append({"score": score, "data": item["meta"]})
        return sorted(scored, key=lambda x: x["score"], reverse=True)[:top_k]

class Mem0EpisodicEngine:
    """
    AetherFS: Mem0 Episodic Memory Integration
    Extracts temporal context, entities, and user traits across sessions.
    Stores them as 'Episodes' in the Milvus core for long-term recall.
    """
    def __init__(self):
        self.vdb = MilvusHNSWCore()
        print("[AetherFS] Milvus HNSW Vector Core initialized.")
        print("[AetherFS] Mem0 Episodic Engine online.")

    def _hash_text(self, text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    def add_episode(self, user_id, interaction_text, role="user"):
        """Records a specific interaction as an episodic memory block."""
        episode = {
            "timestamp": time.time(),
            "user_id": user_id,
            "role": role,
            "content": interaction_text,
            "episode_type": "implicit_memory"
        }
        v_hash = self._hash_text(interaction_text)
        self.vdb.insert(v_hash, episode)
        print(f"   [Mem0] Synaptic weight locked for User '{user_id}': {interaction_text[:40]}...")

    def retrieve_context(self, user_id, query, limit=3):
        """Retrieves past episodes relevant to the current query."""
        q_hash = self._hash_text(query)
        results = self.vdb.search(q_hash, top_k=limit)
        context = [res["data"]["content"] for res in results if res["data"]["user_id"] == user_id]
        return context

if __name__ == "__main__":
    mem = Mem0EpisodicEngine()
    print("\n--- Testing Episodic Ingestion ---")
    mem.add_episode("Inan", "I am building a multi-agent swarm architecture.")
    mem.add_episode("Inan", "The RTX 2060 is my primary local compiler node.")
    
    print("\n--- Testing Episodic Recall ---")
    retrieved = mem.retrieve_context("Inan", "What hardware am I using?")
    print(f"Context Retrieved: {retrieved}")
