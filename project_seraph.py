import os
import cv2
import time
import pygetwindow as gw
import threading
import sys
from dotenv import load_dotenv

# Path hack to import AetherFS modules
sys.path.append(os.path.join(os.path.dirname(__file__), "AetherFS"))
from seraph_xtts_bridge import CoquiXTTSIntegration

load_dotenv()
ADMIN_NAME = os.getenv("ADMIN_NAME", "Inan")
VOICE_FILE = "D:\\openclaw\\seraph_voice.txt"
OBSERVATION_FILE = "D:\\openclaw\\seraph_observations.txt"
INPUT_FILE = "D:\\openclaw\\seraph_input.txt"

class SeraphPersonalSwarm:
    """
    Project SERAPH V10: High-Fidelity Hybrid (Coqui XTTS).
    """
    def __init__(self):
        # Initialize high-fidelity engine
        self.xtts_bridge = CoquiXTTSIntegration()
        self.active_session = True
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        print(f"⚡ SERAPH V10: Hybrid Synthesis Layer Online. Monitoring {ADMIN_NAME}...")

    def speak(self, text):
        print(f"\n[SERAPH VOICE] -> {text}")
        # VRAM Balanced synthesis via XTTS
        self.xtts_bridge.speak_human_like(text)

    def voice_polling_loop(self):
        while self.active_session:
            if os.path.exists(VOICE_FILE):
                try:
                    with open(VOICE_FILE, 'r', encoding='utf-8') as f:
                        text = f.read().strip()
                    if text:
                        open(VOICE_FILE, 'w').close()
                        self.speak(text)
                except Exception:
                    pass
            time.sleep(0.5)

    def watch_presence(self):
        cap = cv2.VideoCapture(0)
        last_seen = 0
        cooldown = 60 
        while self.active_session:
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)
                if len(faces) > 0 and (time.time() - last_seen > cooldown):
                    self.speak(f"Welcome back to the terminal, {ADMIN_NAME}.")
                    last_seen = time.time()
            time.sleep(2)
        cap.release()

    def start(self):
        self.speak("Vocal cortex upgraded to Coqui XTTS. I am fully operational.")
        threading.Thread(target=self.voice_polling_loop, daemon=True).start()
        threading.Thread(target=self.watch_presence, daemon=True).start()
        
        try:
            while self.active_session:
                time.sleep(1)
        except KeyboardInterrupt:
            self.active_session = False
            print("\n[SERAPH] Offline.")

if __name__ == "__main__":
    seraph = SeraphPersonalSwarm()
    seraph.start()
