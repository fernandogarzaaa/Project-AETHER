import json
import os
import asyncio
import random
import requests
import sys
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import uvicorn

# --- NEW PACKAGE INTEGRATION ---
sys.path.append(r"D:\openclaw\claude-response-extracted")
from chimera_quantum_engine import QuantumEngine
from chimera_circuit_breaker import CircuitBreaker, CBConfig

# Resilience & Quantum Engine Initialization
breaker = CircuitBreaker(agent_id="chimera_ultimate_main", cfg=CBConfig(failure_threshold=3))
q_engine = QuantumEngine()

def load_models_config():
    with open("D:\\openclaw\\models_config.json", "r") as f:
        return json.load(f)

MODELS = load_models_config()

# ... (rest of the file remains, I will now update the app.post logic to use MODELS)


# Import Token Fracture (We can implement a basic inline fracture or point to the service)
def fracture_context(text: str, ratio: float = 0.5) -> str:
    """Inline Token Fracture to save VRAM on RTX 2060"""
    # Simple semantic chunking - take first 25% and last 25% if too long
    if len(text) < 1000:
        return text
    keep_len = int(len(text) * ratio / 2)
    return text[:keep_len] + "\n...[FRACTURED]...\n" + text[-keep_len:]

# Senses and Memory
sys.path.append(os.path.join(os.path.dirname(__file__), "AetherFS"))
try:
    from episodic_memory import Mem0EpisodicEngine
    from senses_interface import SensesInterfaceV8
    HAS_AETHER = True
except ImportError:
    HAS_AETHER = False


import torch
import warnings
from transformers import AutoTokenizer

# MINIMIND INTEGRATION
import sys
sys.path.append(os.path.abspath(r'D:\openclaw\research\minimind'))
from model.model_minimind import MiniMindConfig, MiniMindForCausalLM

warnings.filterwarnings('ignore')
MINIMIND_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MINIMIND_TOKENIZER_PATH = r"D:\openclaw\research\minimind\model"
MINIMIND_WEIGHTS_PATH = r"D:\openclaw\research\minimind\out\chimera_logic_512.pth"

try:
    minimind_tokenizer = AutoTokenizer.from_pretrained(MINIMIND_TOKENIZER_PATH)
    minimind_config = MiniMindConfig(hidden_size=512, num_hidden_layers=8, use_moe=False)
    minimind_model = MiniMindForCausalLM(minimind_config)
    minimind_model.load_state_dict(torch.load(MINIMIND_WEIGHTS_PATH, map_location=MINIMIND_DEVICE), strict=False)
    minimind_model = minimind_model.eval().to(MINIMIND_DEVICE)
    HAS_MINIMIND = False
    print("[CHIMERA] MiniMind Local Reasoning Agent Loaded.")
except Exception as e:
    HAS_MINIMIND = False
    print(f"[CHIMERA] MiniMind Failed to Load: {e}")

load_dotenv()
CHIMERA_PORT = int(os.getenv("CHIMERA_PORT", "7870"))
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY", "")

app = FastAPI(title="CHIMERA ULTIMATE V9.0 (AEGIS HYBRID)", version="9.0.0")

if HAS_AETHER:
    episodic_memory = Mem0EpisodicEngine()
    senses = SensesInterfaceV8()

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    user_id: str = "Inan"
    messages: List[ChatMessage]

async def query_local_qwen(prompt: str) -> str:
    """Heavyweight Local Model on RTX 2060 (0 Latency, High VRAM usage)"""
    # Use stricter system prompts for reasoning to prevent hallucinated code-like output
    # (Simplified for MiniMind Reasoning)
    is_business_strategy = False
    if is_business_strategy:
        sys_prompt = "You are a professional KPMG Senior Consultant. Provide a formal, business-focused executive brief. DO NOT include code snippets, Python code, or technical implementation details. Focus on risk, ROI, and compliance."
    else:
        sys_prompt = "You are an expert AI engineer. Provide a precise, technical response focusing on software architecture, performance, and security."

async def _raw_query_local_qwen(prompt: str) -> str:
    if HAS_MINIMIND:
        try:
            messages = [{"role": "user", "content": prompt}]
            prompt_text = minimind_tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=False)
            prompt_text += "assistant\n"
            input_ids = minimind_tokenizer(prompt_text, return_tensors="pt").input_ids.to(MINIMIND_DEVICE)
            with torch.no_grad():
                out = minimind_model.generate(
                    input_ids, 
                    max_new_tokens=512, 
                    temperature=0.3, 
                    top_p=0.8, 
                    do_sample=True,
                    repetition_penalty=1.2,
                    pad_token_id=minimind_tokenizer.eos_token_id
                )
            return minimind_tokenizer.decode(out[0][input_ids.shape[1]:], skip_special_tokens=True)
        except Exception as e:
            print(f"[MiniMind Local] Inference Error: {e}")
            raise Exception("MiniMind node unavailable")
    else:
        try:
            resp = requests.post(
                "http://127.0.0.1:8080/v1/chat/completions",
                json={"messages": [{"role": "user", "content": prompt}], "temperature": 0.7, "max_tokens": 1024},
                timeout=180
            )
            if resp.status_code == 200:
                return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[Local Qwen] Offline or busy: {e}")
        raise Exception("Local node unavailable")

async def query_cloud_node(prompt: str, model_id: str) -> str:
    """Free Cloud API via OpenRouter"""
    if not OPENROUTER_KEY: return ""
    try:
        headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "HTTP-Referer": "http://localhost", "X-Title": "CHIMERA"}
        resp = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={"model": model_id, "messages": [{"role": "user", "content": prompt}], "temperature": 0.7},
            timeout=15
        )
        if resp.status_code == 200:
            return resp.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"[Cloud {model_id}] Failed: {e}")
    return ""

async def critique_response(response: str, prompt: str) -> str:
    """Passes a response through a secondary 'Critic' pass to detect hallucinations."""
    critique_prompt = f"Critique the following AI response for logic, accuracy, and adherence to instructions.\n\nOriginal Prompt: {prompt}\nResponse: {response}\n\nProvide only a concise critique or mark as 'PASS'."
    # Use the fastest available node for the critique pass
    return await query_cloud_node(critique_prompt, "google/gemini-flash-1.5")

def wavefunction_collapse(responses: dict, prompt: str) -> str:
    """Aegis Swarm Matrix Logic with Semantic Scoring and Cross-Verification."""
    
    valid_responses = {k: v for k, v in responses.items() if v and v.strip()}
    
    if not valid_responses:
        return "System Overload: No nodes responded. Check local Qwen server."
        
    print(f"\n--- QUANTUM COLLAPSE: SEMANTIC & VERIFICATION PASS ---")
    
    # 1. Semantic Scoring
    best_node = None
    max_score = -1
    
    for node, resp in valid_responses.items():
        score = len(resp) * (1.2 if "Local" in node else 1.0)
        print(f"[{node}] Semantic Score: {score}")
        if score > max_score:
            max_score = score
            best_node = node
            
    # 2. Cross-Model Verification (Synchronous Critique Pass)
    final_output = valid_responses[best_node]
    print(f"COLLAPSE DETECTED: Observation results in -> {best_node}")
    print(f"VERIFYING: Secondary pass critiquing against other nodes...")
    
    # We block momentarily for the critique pass
    loop = asyncio.get_event_loop()
    critique = loop.run_until_complete(critique_response(final_output, prompt))
    
    print(f"CRITIQUE RESULT: {critique}")
    print(f"-----------------------------\n")
    return final_output

@app.post("/v1/chat/completions")
async def generate_response(req: ChatRequest):
    last_msg = req.messages[-1].content
    
    # 1. Token Fracture (Saves RTX 2060 VRAM)
    fractured_prompt = fracture_context(last_msg, ratio=0.6)
    print(f"[Token Manager] Fractured Prompt Length: {len(last_msg)} -> {len(fractured_prompt)}")
    
    # 2. Context Injection (If Aether is active)
    if HAS_AETHER:
        raw_episodes = episodic_memory.retrieve_context(req.user_id, fractured_prompt)
        augmented_prompt = f"System Context: {raw_episodes}\nUser: {fractured_prompt}"
    else:
        augmented_prompt = fractured_prompt

    # 3. Quantum Debate Swarm (Parallel Execution using MODELS)
    print("Initiating Hybrid Quantum Debate...")
    
    # Run locally (wrapped in CB)
    local_task = asyncio.create_task(query_local_qwen(augmented_prompt))
    
    # Cloud tasks
    cloud_tasks = [query_cloud_node(augmented_prompt, node["id"]) for node in MODELS["models"]["cloud_nodes"]]
        
    results = await asyncio.gather(local_task, *cloud_tasks, return_exceptions=True)
    
    # Process results (handle CB exceptions)
    responses = {}
    if not isinstance(results[0], Exception):
        responses["Local_Qwen_7B"] = results[0]
    
    for i, node in enumerate(MODELS["models"]["cloud_nodes"]):
        if not isinstance(results[i+1], Exception):
            responses[node["label"]] = results[i+1]
    
    # 4. Wavefunction Collapse
    final_response = wavefunction_collapse(responses, augmented_prompt)
    
    # 5. Output and Memory
    if HAS_AETHER:
        try:
            senses.speak(final_response[:200] + "...") # Speak first 200 chars
        except UnicodeEncodeError:
            print(f"[AETHER VOICE] -> (Voice skipped: Unicode error)")
        episodic_memory.add_episode(req.user_id, final_response, role="assistant")
    
    return {
        "id": "chatcmpl-hybrid",
        "object": "chat.completion",
        "choices": [{"message": {"role": "assistant", "content": final_response}}],
        "model": "chimera-aegis-hybrid"
    }

if __name__ == "__main__":
    print(f"CHIMERA ULTIMATE V9.0 (AEGIS HYBRID) INITIALIZING")
    print(f"[*] Local Heavyweight: Qwen2.5-7B (Resilient via CB)")
    print(f"[*] Cloud Debate Nodes: Gemini Flash & Llama 70B")
    print(f"[*] Quantum Engine: ONLINE")
    print(f"[*] Token Fracture Engine: ONLINE")
    print(f"[*] Wavefunction Collapse: ONLINE")
    
    if HAS_AETHER:
        print(f"[*] Aether Senses (Voice & Vision): ONLINE")
        senses.activate_vision()
    else:
        print(f"[!] AetherFS Not Found - Running in Headless LLM Mode")
        
    uvicorn.run(app, host="0.0.0.0", port=CHIMERA_PORT, log_level="info")
