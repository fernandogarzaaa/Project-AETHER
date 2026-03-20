import os
import time
import zmq
import pyttsx3
import threading
import requests
from dotenv import load_dotenv

load_dotenv()
ADMIN_NAME = os.getenv("ADMIN_NAME", "Inan")
CHIMERA_URL = f"http://localhost:{os.getenv('CHIMERA_PORT', '7870')}/v1/chat/completions"

class SeraphPersonalSwarmV11:
    """
    Project SERAPH V11: Ascended Conversational Companion.
    - ZeroMQ Bridge for Voice Input (via Browser)
    - High-Fidelity XTTS (Simulated) / TTS Output
    - Persistent conversational context
    """
    def __init__(self):
        # Voice Engine
        self.engine = pyttsx3.init()
        voices = self.engine.getProperty('voices')
        if len(voices) > 1: self.engine.setProperty('voice', voices[1].id)
        self.engine.setProperty('rate', 175)
        
        # ZMQ Input Socket (Receives text from browser bridge)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.connect("tcp://127.0.0.1:5559")
        
        self.active_session = True
        print(f"⚡ SERAPH V11: Ascended Persona Online.")

    def speak(self, text):
        print(f"[SERAPH VOICE] -> {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def conversation_loop(self):
        """Listens for ZMQ stream."""
        print("🎙️ [SERAPH EARS] Listening to Browser Bridge...")
        while self.active_session:
            try:
                transcript = self.socket.recv_string()
                print(f"   [Processing] -> {transcript}")
                
                # Route to CHIMERA V6+ for LLM processing
                response = requests.post(CHIMERA_URL, json={"user_id": ADMIN_NAME, "message": transcript})
                data = response.json()
                
                self.speak(data.get("response", "I have processed that request."))
            except Exception as e:
                print(f"[Error] Bridge loop failure: {e}")
                time.sleep(1)

    def start(self):
        self.speak("Ascension complete. I am listening via the neural socket.")
        threading.Thread(target=self.conversation_loop, daemon=True).start()
        
        try:
            while self.active_session: time.sleep(1)
        except KeyboardInterrupt:
            self.active_session = False

if __name__ == "__main__":
    SeraphPersonalSwarmV11().start()
