import webbrowser
import config

def execute_action(intent, data):
    if intent == "open_youtube":
        open_url("https://youtube.com")
        return "Opening YouTube."
        
    elif intent == "search_google":
        search_google(data)
        return f"Searching Google for {data}."
        
    elif intent == "unknown":
        return "I'm sorry, I don't know how to do that yet."
    
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