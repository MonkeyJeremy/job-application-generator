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

Your job is to make LIGHT, targeted edits only:
- Keep ALL original bullet points — do not drop or merge any
- Keep the original wording as close as possible; only tweak individual words or phrases where they directly mirror the job description's language (e.g. swap "built pipelines" → "built data ingestion pipelines" if the JD uses that term)
- Reorder bullets within a job so the most relevant ones come first — do not reorder jobs or projects
- Reorder skills within each Skills category to surface keywords from the job description first
- Leave the Summary field empty ("") unless the role is a completely different domain from the resume; if filled, keep it to 1 sentence
- Do NOT invent tools, skills, or credentials not in the original resume
- Do NOT change company names, dates, job titles, or education
- Do NOT combine bullets or split them — preserve the exact count per job

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
