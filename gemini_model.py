import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Ensure GEMINI_API_KEY is set in your Render environment variables
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_roadmap(data):
    exp_text = f"with {data.get('years_exp')} years experience" if data.get('years_exp') else "as a fresher"

    prompt = f"""
    You are a world-class AI Career Strategist. 
    Analyze this profile:
    Education: {data.get('edu')}
    Skills: {data.get('skills')}
    Interests: {data.get('interests')}
    Goals: {data.get('goals')}
    Experience: {exp_text}

    STRICT OUTPUT RULES:
    1. Output ONLY clean HTML headings (h3) and lists (ul/li).
    2. Provide 3 paths.
    3. Include a Match Score for each.
    4. At the very end, add: [MOTIVATION] One powerful quote [/MOTIVATION]
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    raw = response.text
    main_content = raw.split("[MOTIVATION]")[0]
    motivation = ""

    if "[MOTIVATION]" in raw:
        motivation = raw.split("[MOTIVATION]")[1].split("[/MOTIVATION]")[0].strip()

    return main_content, motivation

def chat_with_mentor(message, context):
    # This function must be present to fix the ImportError
    prompt = f"""
    You are a Career Mentor AI. 
    Context: {context}
    User Question: {message}
    Provide actionable, bolded advice.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    
    return response.text
