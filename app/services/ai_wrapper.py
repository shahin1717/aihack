import os
import json
import google.generativeai as genai

from app.schemas.ai_personalized_schemas import (
    AIEmailPersonalizedRequest,
    AIEmailResponse
)

# Configure Gemini client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-1.5-flash"   # fast, cheap, ideal for phishing email generation


def build_prompt(data: AIEmailPersonalizedRequest) -> str:
    return f"""
You are an AI system generating phishing simulation emails for a cybersecurity awareness program.

Generate a realistic, personalized phishing email in HTML.

=== Employee Information ===
Name: {data.employee_name}
Department: {data.department}
Role: {data.role}

=== Phishing Scenario ===
Scenario: {data.scenario}
Tone: {data.tone}
Difficulty: {data.difficulty}

=== Additional Personal Context ===
{data.personal_context}

=== Friend Impersonation (Optional) ===
Friend Name: {data.friend_name}
Friend Relation: {data.friend_relation}
Friend Context: {data.friend_context}

=== Requirements ===
- Generate a convincing phishing email.
- Return HTML only inside the JSON field "body_html".
- Include the placeholder {{click_url}} exactly once.
- Do NOT output explanations.
- Return ONLY valid JSON in this exact structure:

{{
  "subject": "string",
  "body_html": "string"
}}
"""


def safe_json_parse(text: str):
    """
    Gemini sometimes adds text around the JSON.
    This function extracts the first valid JSON block.
    """
    try:
        return json.loads(text)
    except:
        # Try to extract JSON between braces
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])


def generate_phishing_email(data: AIEmailPersonalizedRequest) -> AIEmailResponse:
    """
    Generates a personalized phishing email using Gemini.
    Returns AIEmailResponse(subject, body_html).
    """

    prompt = build_prompt(data)

    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    text_output = response.text
    parsed = safe_json_parse(text_output)

    return AIEmailResponse(
        subject=parsed["subject"],
        body_html=parsed["body_html"]
    )
