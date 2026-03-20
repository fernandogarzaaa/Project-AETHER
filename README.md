# Project AETHER ⚡ (OpenClaw Backend Megastructure)

Welcome to **Project AETHER**, the centralized, autonomous backend engine powering the AppForge ecosystem. 

This repository houses a highly customized, production-ready implementation of [OpenClaw](https://github.com/openclaw/openclaw), configured to act as an operating system for autonomous agent workflows, local LLM orchestration, and self-healing infrastructure.

## 🏗️ The Core Pillars

Project AETHER is divided into four distinct architectural pillars:

### 1. Project WRAITH (The Orchestrator)
Located in `god_node.py`. WRAITH is the master task orchestrator. It manages background processes, scrapers, and agent swarms using exponential backoff algorithms and graceful degradation, ensuring that single-point failures never crash the master server.

### 2. Project EVO (The Immune System)
Located in `openclaw_audit.py`. EVO acts as the system's immune response. It actively monitors runtime integrity, configuration files, and cron jobs. If corruption is detected, EVO automatically triggers a self-healing protocol to restore the last known good state or factory defaults.

### 3. CHIMERA (The Intelligence Router)
Located in `chimera_ultimate.py` and associated scripts. CHIMERA is a local, multi-model consensus LLM server. It is optimized to run locally (e.g., on consumer GPUs like the RTX 2060 via `llama.cpp`) with seamless fallback to cloud APIs, providing the raw intelligence required by the autonomous swarms.

### 4. AETHER (The Standardization Protocol)
The namesake of this repository. AETHER is the security and environment standardization protocol that ensures this megastructure can run on *any* machine. It strictly enforces path agnosticism and environment variable decoupling, ensuring that no personal data, API keys, or hardcoded drive paths are ever committed.

## 🚀 Getting Started

To spin up the AETHER backend on your local machine:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/fernandogarzaaa/Project-AETHER.git
   cd Project-AETHER
   ```

2. **Configure your Environment:**
   Copy the `.env.example` file to a new file named `.env`:
   ```bash
   cp .env.example .env
   ```
   Open `.env` and fill in your specific local paths (e.g., `OPENCLAW_HOME`), hardware limits (e.g., `LLAMA_CPP_GPU_LAYERS`), and alert phone numbers. 

3. **Install Dependencies:**
   Ensure you have Python and `python-dotenv` installed.
   ```bash
   pip install python-dotenv fastapi uvicorn
   ```

4. **Initialize the Megastructure:**
   You can start the CHIMERA server or the WRAITH orchestrator directly:
   ```bash
   python chimera_ultimate.py
   python god_node.py
   ```

## 🔒 Security Notice
Certain proprietary monetization pipelines (the Automated Broadcasting Operations / ABO cluster) and experimental biological sandbox vectors (Project Prometheus) are explicitly `.gitignore`'d and airgapped by design. They are not included in this public open-source release.