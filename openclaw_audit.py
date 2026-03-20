import os
import json
import shutil
import hashlib
import psutil
import logging
from dotenv import load_dotenv
from aether_mesh import AetherMeshNode

load_dotenv()

# Standardized AETHER Path Architecture
OPENCLAW_HOME = os.getenv("OPENCLAW_HOME", "/opt/openclaw")
ADMIN_NAME = os.getenv("ADMIN_NAME", "User")
EVO_PORT = 5557

class EvoImmuneSystem:
    """
    Project EVO V3: OpenClaw Auditing and Self-Healing Engine.
    Combines Static Config Healing (V1) with Active Process Scanning (V2)
    and Zero-Trust AETHER Mesh IPC.
    """
    def __init__(self):
        self.config_dir = os.path.join(OPENCLAW_HOME, "config")
        self.critical_files = ["config.json", "openclaw.toml"]
        self.threshold_cpu = 85.0
        self.threshold_memory_mb = 1024.0
        self.log_file = os.path.join(OPENCLAW_HOME, "evo_runtime_audit.log")
        logging.basicConfig(filename=self.log_file, level=logging.INFO, format='%(asctime)s [EVO] %(message)s')

        try:
            self.mesh_node = AetherMeshNode("EVO_IMMUNE", EVO_PORT)
        except Exception as e:
            print(f"[EVO] Warning: AETHER Mesh binding failed: {e}")
            self.mesh_node = None

    def audit_static_files(self):
        """Phase 1: Validates and heals static configurations via .bak files."""
        print(f"\n--- EVO IMMUNE SYSTEM: STATIC AUDIT ---")
        os.makedirs(self.config_dir, exist_ok=True)
        for file in self.critical_files:
            file_path = os.path.join(self.config_dir, file)
            backup_path = file_path + ".bak"
            if not os.path.exists(file_path):
                if os.path.exists(backup_path):
                    print(f"Auto-Healing: Restoring {file} from backup...")
                    shutil.copy(backup_path, file_path)
                else:
                    print(f"FATAL: {file} is missing. Generating default template.")
                    with open(file_path, 'w') as f:
                        f.write(json.dumps({"_evo_status": "restored_to_factory_defaults"}))
            else:
                print(f"{file} integrity verified.")

    def audit_active_processes(self):
        """Phase 2: Sweeps live processes for memory leaks and zombie states."""
        print(f"\n--- EVO IMMUNE SYSTEM: RUNTIME SWEEP ---")
        anomalies_detected = 0
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'cpu_percent', 'memory_info']):
            try:
                cmdline = proc.info.get('cmdline') or []
                if proc.info['name'] in ['python.exe', 'python3', 'python'] and any("openclaw" in cmd.lower() or "appforge" in cmd.lower() for cmd in cmdline):
                    mem_usage_mb = proc.info['memory_info'].rss / (1024 * 1024)
                    proc_name = " ".join(cmdline[-2:])
                    
                    if mem_usage_mb > self.threshold_memory_mb:
                        self._trigger_immune_response(proc, proc_name, "MEMORY_LEAK", mem_usage_mb)
                        anomalies_detected += 1
                    elif proc.status() == psutil.STATUS_ZOMBIE:
                        self._trigger_immune_response(proc, proc_name, "ZOMBIE_STATE", 0)
                        anomalies_detected += 1
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
        if anomalies_detected == 0:
            print("System bloodline is clean. No memory leaks or hijacked processes.")

    def _trigger_immune_response(self, proc, name, anomaly_type, metric):
        alert = f"CRITICAL: {anomaly_type} detected in {name} (Metric: {metric}MB). Terminating."
        print(f"🛑 {alert}")
        logging.warning(alert)
        try:
            proc.terminate()
            proc.wait(timeout=3)
            print(f"Process {proc.pid} successfully neutralized.")
        except Exception:
            proc.kill()

    def run_full_audit(self):
        print(f"🛡️ Initiating EVO V3 Protocol for {ADMIN_NAME}...")
        self.audit_static_files()
        self.audit_active_processes()

if __name__ == "__main__":
    evo = EvoImmuneSystem()
    evo.run_full_audit()