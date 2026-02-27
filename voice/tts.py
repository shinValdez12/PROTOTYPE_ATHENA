import pyttsx3

engine = pyttsx3.init()

voices = engine.getProperty('voices')

engine.setProperty('voice', voices[1].id)

def speak(text):
    print(f"Athena: {text}")
    engine.say(text)
    engine.runAndWait()