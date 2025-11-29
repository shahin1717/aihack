import google.generativeai as genai
import json
from app.config import get_settings

settings = get_settings()
genai.configure(api_key=settings.GEMINI_API_KEY)


def extract_clean_text(response):
    """
    Extracts Gemini text cleanly and removes ALL backticks, fences,
    invisible junk, and markdown.
    """
    try:
        parts = response.candidates[0].content.parts
        text = "".join([p.text for p in parts])
    except:
        text = response.text or ""

    for fence in ["```json", "```JSON", "```", "`"]:
        text = text.replace(fence, "")
    text = text.strip()
    return text


def generate_email_for_employee(employee_name: str,
                                topic: str,
                                tone: str = "urgent",
                                difficulty: str = "medium"):

    prompt = f"""
You generate CORPORATE phishing-simulation emails.

YOU MUST OUTPUT ONLY VALID JSON.  
NOTHING BEFORE IT.  
NOTHING AFTER IT.  
NO markdown, NO backticks.

JSON FORMAT (MANDATORY):
{{
  "subject": "string",
  "body_html": "<p>HTML only...</p>"
}}

RULES:
- Personalize fully with: {employee_name}
- Medium length: 5–7 paragraphs
- 1 greeting ONLY: <p>Dear {employee_name},</p>
- MUST include EXACTLY ONE phishing link in HTML:
  <a href="https://verify-secure-login.com/{employee_name}">Verify Your Account</a>
- HTML ONLY (p, br, strong, a)
- NO \\n, NO markdown
- NO placeholders
- Do NOT write ```json
- Do NOT explain yourself
- Do NOT add extra text outside JSON

Now produce the JSON only.
Subject must be realistic for the topic: {topic}.
"""

    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(prompt)
    raw = extract_clean_text(response)

    try:
        data = json.loads(raw)
    except Exception:
        # Safe fallback — but NEVER duplicate greeting
        data = {
            "subject": f"{topic} Alert",
            "body_html": (
                f"<p>Dear {employee_name},</p>"
                f"<p>{raw}</p>"
            )
        }

    # Ensure personalization
    body = data["body_html"]
    body = body.replace("Dear Employee", f"Dear {employee_name}")
    body = body.replace(f"Dear {employee_name},Dear {employee_name}", f"Dear {employee_name}")

    # Final safety cleanup
    body = body.replace("\\n", "<br>").replace("\n", "<br>")

    data["body_html"] = body
    return data
