import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Safe Gemini client init
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# ===============================
# ROADMAP GENERATION
# ===============================
def generate_roadmap(data):

    exp_text = f"with {data.get('years_exp')} years experience" if data.get('years_exp') else "as a fresher"

    prompt = f"""
You are a world-class AI Career Strategist and professional career coach.

Analyze the user's profile deeply and suggest the best 3 career paths.

Return ONLY clean HTML.

USER PROFILE:
Education: {data.get('edu')}
Skills: {data.get('skills')}
Interests: {data.get('interests')}
Goals: {data.get('goals')}
Experience: {exp_text}

FORMAT STRICTLY:

<h3>Path 1: [Career Title]</h3>
<b>Match Score:</b> XX/100<br>

<b>30 Day Roadmap:</b>
<ul>
<li>Step 1</li>
<li>Step 2</li>
<li>Step 3</li>
</ul>

<b>60 Day Roadmap:</b>
<ul>
<li>Step 1</li>
<li>Step 2</li>
<li>Step 3</li>
</ul>

<b>90 Day Roadmap:</b>
<ul>
<li>Step 1</li>
<li>Step 2</li>
<li>Step 3</li>
</ul>

<b>Skill Gaps:</b>
<ul>
<li>Skill</li>
<li>Skill</li>
<li>Skill</li>
</ul>

Repeat for Path 2 and Path 3.

[MOTIVATION]
Write 2 lines motivational message.
[/MOTIVATION]
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        # Safe text extraction
        raw = ""
        if hasattr(response, "text") and response.text:
            raw = response.text
        elif hasattr(response, "candidates"):
            raw = response.candidates[0].content.parts[0].text

        if not raw:
            return "<h3>Roadmap generation failed</h3>", ""

        motivation = ""
        html_report = raw

        if "[MOTIVATION]" in raw and "[/MOTIVATION]" in raw:
            parts = raw.split("[MOTIVATION]")
            html_report = parts[0]
            motivation = parts[1].split("[/MOTIVATION]")[0]

        return html_report, motivation

    except Exception as e:
        print("ROADMAP ERROR:", e)
        return "<h3>Error generating roadmap</h3>", ""


# ===============================
# CHATBOT FUNCTION
# ===============================
def chat_with_ai(user_message, context):

    try:
        prompt = f"""
You are a career mentor.

Format responses visually:
- use headings
- short paragraphs
- bullet points
- practical steps
- easy to scan



Student roadmap:
{context}

Answer clearly, practically and guide learning path.

Question:
{user_message}
"""

        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        # Safe response extraction
        if hasattr(response, "text") and response.text:
            return response.text

        elif hasattr(response, "candidates"):
            return response.candidates[0].content.parts[0].text

        else:
            return "I'm here to help with your roadmap and career guidance."

    except Exception as e:
        print("CHATBOT ERROR:", e)
        return "Chatbot temporarily unavailable."
