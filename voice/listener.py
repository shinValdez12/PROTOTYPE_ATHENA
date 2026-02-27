import speech_recognition as sr

def listen():
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
            
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("Athena: My speech service is down.")
            return None
        except Exception:
            return None