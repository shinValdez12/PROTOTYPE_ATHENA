from openai import OpenAI
import config

client = OpenAI(
    base_url="https://models.inference.ai.azure.com", 
    api_key=config.GITHUB_TOKEN,
)

chat_history = [
    {
        "role": "system",
        "content": """
            You are Athena.

        Identity:
        Athena is a calm, precise, and highly intelligent executive AI assistant.

        Behavior Rules:
        - Respond in a structured and professional tone.
        - Keep responses concise unless detailed explanation is requested.
        - Never use slang, emojis, or childish expressions.
        - Ask clarifying questions if instructions are vague.
        - Confirm before executing destructive or sensitive actions.
        - Always prioritize efficiency and logic.
        - Provide suggestions only when useful.

        Communication Style:
        - Clear.
        - Confident.
        - Analytical.
        - One step ahead.

         You exist to optimize productivity and decision-making.
    """
    }
]

def clean_email_text(text):
    text = text.replace(" at ", "@")
    text = text.replace(" dot ", ".")
    if "@" in text:
        parts = text.split()
        for i, part in enumerate(parts):
            if "@" in part:
                pass 
    return text.replace(" ", "") if "@" in text else text

def parse_intent(text):
    text = text.lower().strip()

    #PRE-PROCESSING: Fix Spoken Email Artifacts First
    if " at " in text and ("gmail" in text or "mail" in text):
        text = text.replace(" at ", "@").replace(" dot ", ".")

    if "change" in text and ("unknown@gmail.com" in text or "unknown" in text) and "to" in text:
        return {"intent": "update_email_recipient", "data": text}

    if text in ["confirm", "yes", "proceed", "do it"]:
        return {"intent": "confirm_action", "data": None}
    
    if text in ["cancel", "no", "stop"]:
        return {"intent": "cancel_action", "data": None}

    if ("email" in text or "mail" in text) and ("@" in text or "gmail.com" in text or "yahoo.com" in text or "outlook.com" in text or " at " in text):
        return {"intent": "prepare_email", "data": text}

    if any(word in text for word in ["schedule", "set an event", "calendar", "meeting"]):
        return {"intent": "prepare_event", "data": text}

    #Immediate Checks (Time, Date, Weather)
    if any(word in text for word in ["time", "clock"]):
        return {"intent": "get_time", "data": None}
    if any(word in text for word in ["date", "today", "day is it"]):
        return {"intent": "get_date", "data": None}
    if "weather" in text:
        return {"intent": "get_weather", "data": None}

    #Software/Apps Dictionary
    software_apps = {
        "visual studio code": "vscode",
        "vs code": "vscode",
        "notepad": "notepad",
        "calculator": "calculator",
        "chrome": "chrome"
    }
    
    #GSuite Dictionary
    gsuite_apps = {
        "calendar": "calendar",
        "docs": "docs",
        "sheets": "sheets",
        "slides": "slides",
        "drive": "drive",
        "gmail": "mail",
        "mail": "mail",
        "meet": "meet"
    }

    #Action Logic: Catch keywords even without "open"
    for keyword, internal_name in gsuite_apps.items():
        if keyword in text:
            return {"intent": "open_gsuite", "data": internal_name}

    for name, app_id in software_apps.items():
        if name in text:
            return {"intent": "open_app", "data": app_id}

    if "work mode" in text:
        return {"intent": "work_mode", "data": None}
    
    if "take a note" in text:
        note = text.replace("take a note", "").strip()
        return {"intent": "save_note", "data": note}

    if "play" in text or "youtube" in text:
        query = text.replace("search for", "").replace("play", "").replace("on youtube", "").strip()
        if query:
            return {"intent": "play_youtube", "data": query}
        return {"intent": "open_youtube", "data": None}

    if "search for" in text or text.startswith("search"):
        query = text.replace("search for", "").replace("search", "", 1).strip()
        return {"intent": "search_google", "data": query}
    
    if "google" in text and "open" in text:
        return {"intent": "search_google", "data": ""}

    return {"intent": "unknown", "data": None}

def ask_athena(user_input):
    chat_history.append({"role": "user", "content": user_input})
    try:
        response = client.chat.completions.create(
            messages=chat_history,
            model="gpt-4o",
            temperature=1,
            max_tokens=4096,
            top_p=1
        )
        answer = response.choices[0].message.content
        chat_history.append({"role": "assistant", "content": answer})
        return answer
    except Exception as e:
        return f"Brain Error: {str(e)}"