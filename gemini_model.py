import os
from dotenv import load_dotenv
from google import genai
import markdown

load_dotenv()

# Ensure GEMINI_API_KEY is set in your Render environment variables
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_roadmap(data):
    exp_text = f"with {data.get('years_exp')} years experience" if data.get('years_exp') else "as a fresher"

    prompt = f"""
    You are a world-class AI Career Strategist. Analyze this profile and suggest 3 paths.
    USER PROFILE:
    Education: {data.get('edu')}
    Skills: {data.get('skills')}
    Interests: {data.get('interests')}
    Goals: {data.get('goals')}
    Experience: {exp_text}

    STRICT FORMAT:
    <h3>Path 1: [Title]</h3>
    <b>Match Score:</b> XX/100<br>
    <b>30/60/90 Day Roadmap:</b> [Detailed steps in <ul> format]
    <b>Skill Gaps:</b> [List in <ul> format]

    Repeat for Path 2 and Path 3.
    At the end, add: [MOTIVATION] One powerful quote [/MOTIVATION]
    """

    # Using gemini-2.0-flash for speed and reliability
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
    # This function was missing, causing your deployment to fail
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
