import google.generativeai as genai
from app.config import get_settings

settings = get_settings()

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


def generate_email(topic: str, tone: str = "phishing", difficulty: str = "medium"):
    """
    Generate phishing-style email using Google Gemini (free tier).
    """

    prompt = f"""
    Generate a phishing simulation email for cybersecurity training.

    Requirements:
    - Topic: {topic}
    - Tone: {tone}
    - Difficulty: {difficulty}
    - Produce believable, corporate-style phishing content.
    - Respond ONLY in JSON with:
      {{
        "subject": "...",
        "body_html": "..."
      }}
    - Make body_html real HTML.
    - Do NOT include malicious code.
    - Keep tone urgent and realistic.
    """

    model = genai.GenerativeModel("gemini-1.5-flash")

    response = model.generate_content(prompt)

    import json
    try:
        data = json.loads(response.text)
    except:
        # fallback
        data = {
            "subject": f"{topic} Notification",
            "body_html": f"<p>{response.text}</p>"
        }

    return data
