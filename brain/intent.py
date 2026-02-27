from openai import OpenAI
import config

client = OpenAI(
    base_url="https://models.inference.ai.azure.com", 
    api_key=config.GITHUB_TOKEN,
)

def parse_intent(text):
    text = text.lower().strip()
    
    if "open youtube" in text:
        return {"intent": "open_youtube", "data": None}
    
    elif "search for" in text:
        query = text.split("search for")[-1].strip()
        return {"intent": "search_google", "data": query}
        
    return {"intent": "unknown", "data": None}

def ask_athena(user_input):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are Athena, a helpful AI assistant. Give short, witty responses."
                },
                {
                    "role": "user", 
                    "content": user_input
                },
            ],
            model="gpt-4o",
            temperature=1,
            max_tokens=4096,
            top_p=1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Brain Error: {str(e)}"