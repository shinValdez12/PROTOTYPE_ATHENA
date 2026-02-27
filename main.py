import config
from voice.listener import listen
from voice.tts import speak
from brain.intent import parse_intent
from brain.intent import ask_athena
from actions.system_actions import execute_action

def start_athena():
    speak("Athena systems online.")
    
    while True:
        raw_text = listen() 
        
        if raw_text:
            if raw_text.startswith(config.WAKE_WORD):
                command = raw_text.replace(config.WAKE_WORD, "").strip()
                
                if not command:
                    speak("Yes? I am listening.")
                    continue

                print(f"Processing command: {command}")

                decision = parse_intent(command)

                if decision['intent'] != "unknown":
                    result = execute_action(decision['intent'], decision['data'])
                    speak(result)
                else:
                    print("Athena is thinking...")
                    ai_response = ask_athena(command)
                    speak(ai_response)
 
                result = execute_action(decision['intent'], decision['data'])

                if result:
                    speak(result)
            else:
                pass

if __name__ == "__main__":
    start_athena()