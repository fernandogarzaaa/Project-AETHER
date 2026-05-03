# Project AETHER

AETHER is a privacy-first agentic operating system designed to run locally and transparently within a user's own environment, rather than relying on cloud-scraping or invasive UI automation. It bundles the CHIMERA local-LLM server, the OpenClaw agent runtime, swarm/consensus orchestration, and supporting RAG, routing, and skills tooling into a single workspace.

For the full description of the lightweight CHIMERA Simple API server (the local + Hugging Face failover layer that most clients connect to), see [CHIMERA_SIMPLE_README.md](CHIMERA_SIMPLE_README.md).

## Setup

This repo is a polyglot workspace. The two primary stacks:

**Python (CHIMERA, swarm, RAG, agents)**

```bash
pip install -r requirements.txt
```

Some submodules (`token_fracture`, `swarm_v2`, `smart_router`, `quantum_consensus_v2`, `simple_rag`, `qwen-agent`) are local packages — install them from their own folders if not already on `PYTHONPATH`.

**Node / Playwright (e2e tests)**

```bash
npm install
npx playwright install
```

**Starting the local CHIMERA server (Windows)**

```bat
start_chimera_simple.bat
```

The server listens on `http://localhost:7861/v1` and exposes an OpenAI-compatible API. See [CHIMERA_SIMPLE_README.md](CHIMERA_SIMPLE_README.md) for client configuration.

## Status

Active development / pre-release. The repository is a working monorepo containing multiple in-progress subsystems:

- **CHIMERA Simple** — running, used as the primary local LLM endpoint.
- **OpenClaw / agent runtime** — integrated, see `openclaw.toml` and the `lossless-claw/` subtree.
- **Swarm v2 / v3** — present, under iteration.
- **AetherFS, senses, cctv_vision, vision_sentinel** — experimental subsystems.
- **Project-EVO, ruvnet, skills** — supporting research and tooling.

Numerous capability, research, and audit notes live at the repo root (`CAPABILITIES.md`, `CAPABILITIES_ROADMAP.md`, `RESEARCH_*.md`, `QUANTUM_*.md`, `SWARM_V2_ARCH_COMPLETE*.md`, etc.) — these document specific subsystems and are not yet consolidated into a single guide.
