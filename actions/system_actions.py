from datetime import datetime
import webbrowser
import config
import os
import subprocess

def execute_action(intent, data):
    if intent == "get_time":
        now = datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."

    elif intent == "get_date":
        today = datetime.now().strftime("%B %d, %Y")
        return f"Today is {today}."
    
    elif intent == "get_weather":
            search_url = "https://www.google.com/search?q=weather"
            open_url(search_url)
            return "Opening the local weather forecast for you."
    
    if intent == "open_app":
        if data == "vscode":
            path = os.path.expanduser("~") + r"\AppData\Local\Programs\Microsoft VS Code\Code.exe"
            
            if os.path.exists(path):
                subprocess.Popen(path)
                return "Opening Visual Studio Code."
            else:
                try:
                    subprocess.Popen("code") 
                    return "Opening VS Code via system path."
                except:
                    return "I couldn't find the path for VS Code. Please check system_actions.py."

        elif data == "notepad":
            subprocess.Popen("notepad.exe")
            return "Opening Notepad."

        elif data == "calculator":
            subprocess.Popen("calc.exe")
            return "Opening Calculator."
    
    if intent == "search_youtube":
        url = f"https://www.youtube.com/results?search_query={data}"
        open_url(url)
        return f"Searching YouTube for {data}."
    
    elif intent == "play_youtube":
        url = f"https://www.youtube.com/results?search_query={data}"
        open_url(url)
        return f"Playing {data} on YouTube."

    elif intent == "open_youtube":
        open_url("https://youtube.com")
        return "Opening YouTube."

    elif intent == "search_google":
        if data == "":
            open_url("https://google.com")
            return "Opening Google."
        else:
            search_google(data)
            return f"Searching for {data}."
        
    elif intent == "open_app":
        if data == "vscode":
            try:
                os.system('start code') 
                return "Launching Visual Studio Code."
            except Exception as e:
                return f"Failed to open VS Code: {e}"

    elif intent == "open_gsuite":
        urls = {
            "calendar": "https://calendar.google.com",
            "docs": "https://docs.google.com",
            "sheets": "https://sheets.google.com",
            "slides": "https://slides.google.com",
            "drive": "https://drive.google.com",
            "gmail": "https://mail.google.com",
            "gmeet": "https://meet.google.com"
        }
        url = urls.get(data)
        if url:
            open_url(url)
            return f"Opening your Google {data}."

    elif intent == "work_mode":
        open_url("https://github.com")
        open_url("https://web.whatsapp.com")
        return "Work mode activated. Opening GitHub and communications."

    elif intent == "save_note":
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        file_path = os.path.join(desktop, "athena_notes.txt")
        with open(file_path, "a") as f:
            f.write(f"- {data}\n")
        return f"Note saved: {data}"
    
    return None

def open_url(url):
    """Helper to handle browser choice for any URL"""
    if hasattr(config, 'BROWSER_CHOICE') and config.BROWSER_CHOICE:
        webbrowser.get(config.BROWSER_CHOICE).open(url)
    else:
        webbrowser.open(url)

def search_google(query):
    """Specific helper for searching"""
    url = f"https://www.google.com/search?q={query}"
    open_url(url)

def parse_intent(text):
    text = text.lower().strip()
    
    if "open youtube" in text:
        return {"intent": "open_youtube", "data": None}
    
    elif "search for" in text:
        query = text.split("search for")[-1].strip()
        return {"intent": "search_google", "data": query}
        
    return {"intent": "unknown", "data": None}