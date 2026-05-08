"""
Calls Claude to tailor Jeremy's resume to a job description.
Returns a structured dict that resume_exporter.py renders into docx/pdf.
"""
import json
import os
from pathlib import Path

import anthropic
from dotenv import dotenv_values

_env = dotenv_values(Path(__file__).parent / ".env")
_API_KEY = _env.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")

from resume_context import RESUME_TEXT, CANDIDATE_NAME, CANDIDATE_EMAIL, CANDIDATE_PHONE

_SYSTEM_PROMPT = f"""You are a professional resume writer helping {CANDIDATE_NAME} tailor their resume \
to a specific job description.

Here is the candidate's full resume:
{RESUME_TEXT}

Your job:
- Reorder and reword bullet points to emphasize the most relevant experience for this specific role
- Sharpen bullet point language: stronger action verbs, tighter metrics, remove anything irrelevant
- Adjust the Skills section to surface keywords from the job description first
- You may add a 1-2 sentence "Summary" section if the role benefits from one; otherwise omit it
- Do NOT invent experience, tools, or credentials that are not in the original resume
- Do NOT change company names, dates, job titles, or education
- Keep every bullet under 2 lines when printed

Return ONLY valid JSON matching this exact schema (no markdown fences, no extra keys):

{{
  "summary": "<string or empty string>",
  "skills": {{
    "Programming Skills": "<comma-separated list>",
    "Analytical Skills": "<comma-separated list>",
    "Data Visualization": "<comma-separated list>",
    "Software & Tools": "<comma-separated list>"
  }},
  "experience": [
    {{
      "company": "<string>",
      "location": "<string>",
      "title": "<string>",
      "dates": "<string>",
      "bullets": ["<string>", ...]
    }}
  ],
  "projects": [
    {{
      "name": "<string>",
      "dates": "<string>",
      "bullets": ["<string>", ...]
    }}
  ]
}}
"""


def polish_resume(job_description: str) -> dict:
    client = anthropic.Anthropic(api_key=_API_KEY)

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        system=[
            {
                "type": "text",
                "text": _SYSTEM_PROMPT,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        messages=[
            {
                "role": "user",
                "content": f"Job Description:\n{job_description}\n\nReturn the tailored resume JSON now.",
            }
        ],
    )

    raw = message.content[0].text.strip()
    # Strip accidental markdown fences if the model adds them
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)
