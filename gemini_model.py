import os
from dotenv import load_dotenv
from google import genai
import markdown

load_dotenv()

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_roadmap(data):

    exp_text = f"with {data.get('years_exp')} years experience" if data.get('years_exp') else "as a fresher"

    prompt = f"""
You are a world-class AI Career Strategist and professional career coach.

Analyze the user's profile deeply and suggest the best 3 career paths.
The output must look premium, structured, and professional.

USER PROFILE:
Education: {data.get('edu')}
Skills: {data.get('skills')}
Interests: {data.get('interests')}
Goals: {data.get('goals')}
Experience: {exp_text}

⚠️ STRICT OUTPUT RULES (VERY IMPORTANT)

1. Output ONLY in clean HTML (no markdown, no ```).
2. Use professional formatting.
3. All section headings must be bold.
4. Each path must be detailed but clean and readable.
5. Keep points concise and impressive.
6. Use bullet points for roadmap steps.
7. Include realistic skill gaps.
8. Match score should be realistic.

══════════════════════════════════

FORMAT TO FOLLOW STRICTLY:

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
<li>Missing skill 1</li>
<li>Missing skill 2</li>
<li>Missing skill 3</li>
</ul>

Repeat same structure for:

<h3>Path 2: ...</h3>
<h3>Path 3: ...</h3>

══════════════════════════════════

At the end add:

[MOTIVATION]
Write one powerful 2-line motivational quote for career growth.
[/MOTIVATION]

⚠️ Do NOT explain anything outside this format.
⚠️ Do NOT use markdown.
⚠️ Only structured HTML output.
"""

    response = client.models.generate_content(
        model="models/gemini-2.5-flash",
        contents=prompt
    )

    raw = response.text
    print("GEMINI OUTPUT:\n", raw)

    main_content = raw.split("[MOTIVATION]")[0]
    motivation = ""

    if "[MOTIVATION]" in raw:
        motivation = raw.split("[MOTIVATION]")[1].split("[/MOTIVATION]")[0]

    html_report = markdown.markdown(main_content, extensions=['extra', 'nl2br'])
    return html_report, motivation
