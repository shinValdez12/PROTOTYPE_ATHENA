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

def parse_intent(text):
    text = text.lower().strip()

    if any(word in text for word in ["time", "clock"]):
            return {"intent": "get_time", "data": None}
        
    if any(word in text for word in ["date", "today", "day is it"]):
            return {"intent": "get_date", "data": None}
    
    if "weather" in text:
        return {"intent": "get_weather", "data": None}
    software_apps = {
        "visual studio code": "vscode",
        "vs code": "vscode",
        "notepad": "notepad",
        "calculator": "calculator",
        "chrome": "chrome"
    }

    if "open" in text or "launch" in text:
        for name, app_id in software_apps.items():
            if name in text:
                return {"intent": "open_app", "data": app_id}
    
    if "open" in text or "launch" in text:
        if "visual studio code" in text or "vs code" in text:
            return {"intent": "open_app", "data": "vscode"}

    if "play" in text:
        query = text.replace("play", "").replace("on youtube", "").strip()
        return {"intent": "open_youtube", "data": None}
    
    elif "search for" in text and "youtube" in text:
        query = text.replace("search for ", "").replace("on youtube", "").strip()
        return {"intent": "open_youtube", "data": None}
    
    if "work mode" in text:
        return {"intent": "work_mode", "data": None}
    
    if "take a note" in text:
        note = text.replace("take a note", "").strip()
        return {"intent": "save_note", "data": note}
    
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

    if any(trigger in text for trigger in ["open google", "open my", "go to my"]):
        for keyword, internal_name in gsuite_apps.items():
            if keyword in text:
                return {"intent": "open_gsuite", "data": internal_name}
    
    if "search for" in text:
        query = text.split("search for")[-1].strip()
        return {"intent": "search_google", "data": query}
    elif text.startswith("search"):
        query = text.replace("search", "", 1).strip()
        return {"intent": "search_google", "data": query}

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