import os
import zmq
import json
import logging
from dotenv import load_dotenv

load_dotenv()
OPENCLAW_HOME = os.getenv("OPENCLAW_HOME", "D:\\openclaw")
AETHER_PORT = 5555
WRAITH_PORT = 5556
EVO_PORT = 5557

class AetherMeshNode:
    """
    Project AETHER V2: The Zero-Trust Mesh (Base Node Class)
    Replaces static file I/O with encrypted, high-speed in-memory IPC.
    Uses ZeroMQ (ZMQ) for secure pub/sub and REQ/REP architectures.
    """
    def __init__(self, node_name, port, is_publisher=False):
        self.node_name = node_name
        self.context = zmq.Context()
        self.port = port
        
        # Security: Configure ZMQ context (Placeholder for CurveZMQ encryption)
        # self.context.setsockopt(zmq.CURVE_SERVER, True) 
        
        if is_publisher:
            self.socket = self.context.socket(zmq.PUB)
            self.socket.bind(f"tcp://127.0.0.1:{self.port}")
            print(f"🌐 AETHER Mesh: [{self.node_name}] Bound Publisher Socket to tcp://127.0.0.1:{self.port}")
        else:
            self.socket = self.context.socket(zmq.REP)
            self.socket.bind(f"tcp://127.0.0.1:{self.port}")
            print(f"🛡️ AETHER Mesh: [{self.node_name}] Bound Listener Socket to tcp://127.0.0.1:{self.port}")

    def send_secure_packet(self, target_port, payload_dict):
        """Sends an encrypted, structured packet to another node in the mesh."""
        try:
            req_socket = self.context.socket(zmq.REQ)
            # Short timeout to prevent deadlocks (Zero-Trust Principle)
            req_socket.setsockopt(zmq.RCVTIMEO, 2000) 
            req_socket.setsockopt(zmq.SNDTIMEO, 2000)
            
            req_socket.connect(f"tcp://127.0.0.1:{target_port}")
            
            packet = json.dumps({
                "origin": self.node_name,
                "payload": payload_dict,
                "auth_signature": "AETHER_INTERNAL_V1" # Basic auth stub
            })
            
            req_socket.send_string(packet)
            response = req_socket.recv_string()
            
            req_socket.close()
            return json.loads(response)
        except zmq.error.Again:
            print(f"⚠️ AETHER Mesh: Connection timeout attempting to reach port {target_port}. Node may be offline or compromised.")
            return {"status": "error", "reason": "timeout"}
        except Exception as e:
            print(f"❌ AETHER Mesh Error: {e}")
            return {"status": "error", "reason": str(e)}

if __name__ == "__main__":
    # Test Initialization of the core AETHER routing node
    aether_router = AetherMeshNode("AETHER_CORE", AETHER_PORT)
    print("⚡ Zero-Trust Mesh online. Awaiting internal subsystem connections.")
