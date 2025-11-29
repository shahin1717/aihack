import google.generativeai as genai
import json
from app.config import get_settings

settings = get_settings()
genai.configure(api_key=settings.GEMINI_API_KEY)

def extract_clean_text(response):
    """
    Extracts FULL text from Gemini and removes any ```json fences.
    """
    try:
        parts = response.candidates[0].content.parts
        text = "".join([p.text for p in parts])
    except:
        text = response.text or ""

    # Remove code fences
    text = text.replace("```json", "").replace("```", "").strip()
    text = text.replace("`", "").strip()  # remove stray backticks
    return text


def generate_email_for_employee(employee_name: str,
                                topic: str,
                                tone: str = "urgent",
                                difficulty: str = "medium"):

    prompt = f"""
You generate corporate-style phishing simulation emails.

STRICT RULES:
- Personalize with employee name: {employee_name}
- Medium length (5–7 paragraphs)
- Realistic corporate tone
- HTML only (<p>, <a>, <strong>, <br>)
- MUST include exactly 1 phishing link inside the body
- DO NOT output ```json or ``` anywhere
- DO NOT output markdown
- DO NOT output placeholders like [Employee Name]
- Greeting MUST be only once: "Dear {employee_name},"
- FINAL OUTPUT MUST BE ONLY valid JSON:

{{
  "subject": "A realistic subject",
  "body_html": "<p>...</p>"
}}

Email structure required:
1. <p>Dear {employee_name},</p>
2. Paragraph describing suspicious activity
3. Paragraph creating urgency
4. Instructions + verification
5. One phishing link
6. Security notice
7. Closing paragraph
"""

    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(prompt)

    raw = extract_clean_text(response)

    # Ensure JSON is clean
    try:
        data = json.loads(raw)
    except:
        # Fallback, but KEEP only one greeting
        data = {
            "subject": f"{topic} Alert",
            "body_html": (
                f"<p>Dear {employee_name},</p>"
                f"<p>{raw}</p>"
            )
        }

    # Final safety: ensure greeting appears ONLY once
    body = data["body_html"]
    body = body.replace("Dear Employee", f"Dear {employee_name}")
    body = body.replace(f"Dear {employee_name},Dear {employee_name}", f"Dear {employee_name}")

    data["body_html"] = body
    return data
