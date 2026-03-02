from datetime import datetime
import webbrowser
import config
import os
import subprocess
import pywhatkit
import urllib.parse
import re

pending_draft = None
current_task = None

import re

import re

#Helper for fixing the emailtoXXX@gmail.com to Xx@gmail.com
def _cleanup_name_part(name_part: str) -> str:
    name_part = name_part.strip()
    while re.match(r"^(?:athena|please|kindly|send|email|mail|to|compose|draft|message|for|about)\b", name_part, flags=re.I):
        name_part = re.sub(
            r"^(?:athena|please|kindly|send|email|mail|to|compose|draft|message|for|about)\s+",
            "",
            name_part,
            flags=re.I
        ).strip()
    return name_part

#Helper to fix the at and dots tp @ and .
def extract_email_smart(text: str) -> str | None:
    t = text.lower().strip()

    t = re.sub(r"\s+at\s+", " @ ", t, flags=re.I)
    t = re.sub(r"\s+dot\s+", " . ", t, flags=re.I)

    m_name_at = re.search(
        r"\b((?:[a-z]+\s+){1,3}[a-z]+)\s*@\s*([a-z0-9.-]+\.[a-z]{2,})\b",
        t,
        flags=re.I
    )
    if m_name_at:
        name_part = _cleanup_name_part(m_name_at.group(1))
        domain_part = m_name_at.group(2)

        name_part = re.sub(r"^(mr|mrs|ms|sir)\s+", "", name_part, flags=re.I).strip()

        local = "".join(name_part.split())
        local = re.sub(r"[^a-z0-9._%+-]", "", local)
        return f"{local}@{domain_part}"

    m_name_domain = re.search(
        r"\b((?:[a-z]+\s+){1,3}[a-z]+)\s+(gmail\.com|yahoo\.com|outlook\.com)\b",
        t,
        flags=re.I
    )
    if m_name_domain:
        name_part = _cleanup_name_part(m_name_domain.group(1))
        domain_part = m_name_domain.group(2)

        name_part = re.sub(r"^(mr|mrs|ms|sir)\s+", "", name_part, flags=re.I).strip()

        local = "".join(name_part.split())  # no dots
        local = re.sub(r"[^a-z0-9._%+-]", "", local)
        return f"{local}@{domain_part}"

    m = re.search(r"\b[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}\b", t, flags=re.I)
    if m:
        return m.group(0)

    return None

def execute_action(intent, data, ai_function):
    global current_task
    global pending_draft

    if intent == "prepare_email":
        clean_text = data.lower().replace(" at ", "@").replace(" dot ", ".")

        recipient = extract_email_smart(clean_text) or "unknown@gmail.com"

        if not recipient:
            return "I couldn't find an email address. Please say: 'send email to jara valdez at gmail dot com about ...'"

        prompt = f"Write ONLY the email body (no subject line). Topic: {data}. Keep it concise."
        draft_body = ai_function(prompt)
        draft_body = re.sub(r"(?im)^subject:\s*.*\n?", "", draft_body).strip()

        current_task = {
            "type": "email",
            "to": recipient,
            "subject": "Project Update",
            "body": draft_body
        }

        return f"I've drafted a message for {recipient}:\n\n\"{draft_body}\"\n\nShall I proceed?"
    
    #update email
    elif intent == "update_email_recipient":
        if not current_task or current_task.get("type") != "email":
            return "No email draft is active to update."

        new_recipient = extract_email_smart(data)
        if not new_recipient:
            return "I couldn't detect the new email. Say it like: 'jahara valdez at gmail dot com'."

        current_task["to"] = new_recipient
        return f"Updated recipient to {new_recipient}. Shall I proceed?"
    
    #PREPARE CALENDAR
    elif intent == "prepare_event":
        current_task = {"type": "calendar", "content": data}
        return f"I've prepared a schedule request for: '{data}'. Shall I add this to your calendar?"

    elif current_task and current_task.get("type") == "calendar":
        url = "https://calendar.google.com/calendar/u/0/r/eventedit"
            
        open_url(url)
        current_task = None
        return "Confirmed. Opening the calendar event editor."

    #CONFIRM
    elif intent == "confirm_action":
        if not current_task:
            return "I don't have a task waiting for confirmation."

        if current_task["type"] == "email":
            to = current_task["to"]
            su = urllib.parse.quote(current_task["subject"])
            bo = urllib.parse.quote(current_task["body"])
            url = f"https://mail.google.com/mail/?view=cm&fs=1&to={to}&su={su}&body={bo}"
            
            open_url(url)
            current_task = None 
            return f"Confirmed. Opening Gmail now."

        elif current_task and current_task.get("type") == "calendar":
            url = "https://calendar.google.com/calendar/u/0/r/eventedit"
            open_url(url)
            current_task = None
            return "Confirmed. Opening the calendar event editor."

    #CANCEL
    elif intent == "cancel_action":
        current_task = None
        return "Understood. I've cancelled the pending action."

    #ime, Date, Weather
    if intent == "get_time":
        now = datetime.now().strftime("%I:%M %p")
        return f"The current time is {now}."
    elif intent == "get_date":
        today = datetime.now().strftime("%B %d, %Y")
        return f"Today is {today}."
    elif intent == "get_weather":
        open_url("https://www.google.com/search?q=weather")
        return "Opening the local weather forecast for you."
    
    #COMBINED: Software Launcher
    elif intent == "open_app":
        if data == "vscode":
            try:
                os.system('start code') 
                return "Launching Visual Studio Code."
            except:
                path = os.path.expanduser("~") + r"\AppData\Local\Programs\Microsoft VS Code\Code.exe"
                if os.path.exists(path):
                    subprocess.Popen(path)
                    return "Opening Visual Studio Code."
                return "I could not find VS Code on your system path or folder."
        
        elif data == "notepad":
            subprocess.Popen("notepad.exe")
            return "Opening Notepad."
        elif data == "calculator":
            subprocess.Popen("calc.exe")
            return "Opening Calculator."

    #YouTube & Google Handling
    elif intent == "open_youtube":
        open_url("https://youtube.com")
        return "Opening YouTube."
    elif intent == "play_youtube":  
        try:
            pywhatkit.playonyt(data)
            return f"Playing {data} immediately on YouTube."
        except Exception as e:
            open_url(f"https://www.youtube.com/results?search_query={data}")
            return f"I couldn't start the video automatically, but here are the results for {data}."
        
    elif intent == "search_google":
        if data == "":
            open_url("https://google.com")
            return "Opening Google."
        search_google(data)
        return f"Searching for {data}."

    #GSuite & Productivity
    elif intent == "open_gsuite":
        urls = {
            "calendar": "https://calendar.google.com",
            "docs": "https://docs.google.com",
            "sheets": "https://sheets.google.com",
            "drive": "https://drive.google.com",
            "mail": "https://mail.google.com",
            "meet": "https://meet.google.com"
        }
        url = urls.get(data)
        if url:
            open_url(url)
            return f"Opening your Google {data}."

    elif intent == "work_mode":
        open_url("https://github.com")
        open_url("https://web.whatsapp.com")
        os.system('start code')
        return "Work mode activated. Opening GitHub, WhatsApp, and VS Code."

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