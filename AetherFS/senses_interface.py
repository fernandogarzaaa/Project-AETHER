import os
import cv2
import time
import threading
import pyttsx3

class SensesInterfaceV8:
    """
    Project AETHER V8: The Senses Interface.
    Replaces the theoretical CCTV integration with a direct hook into the host laptop.
    Gives the CHIMERA LLM the ability to 'see' through the webcam and 'speak' via TTS.
    """
    def __init__(self):
        # Initialize Voice Synthesizer
        self.voice_engine = pyttsx3.init()
        voices = self.voice_engine.getProperty('voices')
        # Select a clear, sharp voice (often voice[1] or voice[0] depending on OS)
        if len(voices) > 1:
            self.voice_engine.setProperty('voice', voices[1].id)
        self.voice_engine.setProperty('rate', 170) # Slightly faster, decisive cadence
        
        self.vision_active = False

    def speak(self, text):
        """Translates text payloads into physical audio out of the laptop speakers."""
        print(f"[AETHER VOICE] -> {text}")
        self.voice_engine.say(text)
        self.voice_engine.runAndWait()

    def _vision_loop(self):
        """Background thread that captures frames from the laptop webcam."""
        cap = cv2.VideoCapture(0) # 0 is typically the default laptop webcam
        if not cap.isOpened():
            print("⚠️ [AETHER SENSES] Camera access denied or hardware not found.")
            return

        print("👁️ [AETHER SENSES] Visual cortex online. Monitoring laptop environment...")
        
        while self.vision_active:
            ret, frame = cap.read()
            if ret:
                # In a full integration, this frame would be passed to a 
                # local Vision model (like Qwen-VL) to extract semantic meaning.
                # For safety/sandbox testing, we just verify the feed is live.
                pass
            time.sleep(1.0) # Poll every 1 second to save CPU

        cap.release()

    def activate_vision(self):
        """Spawns the webcam monitor in an isolated thread."""
        self.vision_active = True
        vision_thread = threading.Thread(target=self._vision_loop, daemon=True)
        vision_thread.start()

    def deactivate_vision(self):
        self.vision_active = False
        print("👁️ [AETHER SENSES] Visual cortex offline.")

if __name__ == "__main__":
    senses = SensesInterfaceV8()
    
    print("\n--- Testing AETHER Senses Integration ---")
    senses.speak("Initializing visual cortex. I am now hooked directly into your machine.")
    
    # Briefly test camera activation (it will trigger the webcam light if available)
    senses.activate_vision()
    time.sleep(3)
    senses.deactivate_vision()
    senses.speak("Hardware test complete. Senses are active.")
