from gtts import gTTS
import os

def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        filename = "output.mp3"
        tts.save(filename)
        os.system(f"start {filename}")  # Windows
    except Exception as e:
        print(f"TTS Error: {e}")
