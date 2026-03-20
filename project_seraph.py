import os
import cv2
import time
import pygetwindow as gw
import pyttsx3
import threading
from dotenv import load_dotenv

load_dotenv()
ADMIN_NAME = os.getenv("ADMIN_NAME", "Inan")

class SeraphPersonalSwarm:
    """
    Project SERAPH: Personal Autonomous Companion.
    Monitors host desktop state (active windows) and presence via webcam.
    Communicates via local TTS.
    """
    def __init__(self):
        self.voice_engine = pyttsx3.init()
        self.voice_engine.setProperty('rate', 175)
        self.active_session = True
        print(f"⚡ SERAPH V1: Personal Companion Online. Monitoring {ADMIN_NAME}...")

    def speak(self, text):
        print(f"SERAPH: {text}")
        self.voice_engine.say(text)
        self.voice_engine.runAndWait()

    def track_desktop(self):
        """Monitors active windows/tabs to understand work context."""
        while self.active_session:
            active_win = gw.getActiveWindow()
            if active_win:
                # Basic telemetry for pattern recognition
                # In a real impl, this updates a state-log
                pass 
            time.sleep(5)

    def watch_presence(self):
        """Webcam presence detection."""
        cap = cv2.VideoCapture(0)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        while self.active_session:
            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, 20) # Simulate grayscale conversion
                faces = face_cascade.detectMultiScale(gray, 1.1, 4)
                if len(faces) > 0:
                    # Logic for "talk when user enters room"
                    pass
            time.sleep(2)
        cap.release()

    def start(self):
        threading.Thread(target=self.track_desktop, daemon=True).start()
        threading.Thread(target=self.watch_presence, daemon=True).start()
        self.speak(f"Good morning, {ADMIN_NAME}. I am online and observing.")

if __name__ == "__main__":
    seraph = SeraphPersonalSwarm()
    seraph.start()
