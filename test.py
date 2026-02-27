import asyncio
import edge_tts

TEXT = "Hello! I am Athena. I am currently using the Ava Multilingual voice. It is designed to sound natural, professional, and clear. How do I sound?"

VOICE = "en-US-AvaMultilingualNeural"
OUTPUT_FILE = "athena_ava.mp3"

async def generate_athena_voice():
    communicate = edge_tts.Communicate(TEXT, VOICE)

    await communicate.save(OUTPUT_FILE)
    print(f"Success! Athena's voice has been saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(generate_athena_voice())