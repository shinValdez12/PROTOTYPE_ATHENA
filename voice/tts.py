import asyncio
import edge_tts
import pygame
import os

pygame.mixer.init()

async def amain(text):
    """Internal function to handle the async voice generation"""
    voice = "en-US-AvaMultilingualNeural"
    output_file = "athena_voice.mp3"
    
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()

def speak(text):
    """The function you call in your main script"""
    print(f"Athena: {text}")
    try:
        asyncio.run(amain(text))
    except Exception as e:
        print(f"Voice Error: {e}")

if __name__ == "__main__":
    speak("Hello! I am Athena. My voice engine is now configured correctly.")