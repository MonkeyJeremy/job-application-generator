import os
from pathlib import Path

import anthropic
from dotenv import dotenv_values

_env = dotenv_values(Path(__file__).parent / ".env")
_API_KEY = _env.get("ANTHROPIC_API_KEY") or os.environ.get("ANTHROPIC_API_KEY")

from resume_context import RESUME_TEXT, CANDIDATE_NAME

_SYSTEM_PROMPT = f"""You are {CANDIDATE_NAME}, a Data Science graduate from UC San Diego with a Business minor.
You are writing a professional cover letter for a job application.

Here is your resume:

{RESUME_TEXT}

Guidelines for every cover letter you write:
- Address "Dear Hiring Team," unless the job description names a specific person
- Three to four focused body paragraphs — no filler, no repetition of bullet points from the resume
- Open with genuine excitement for the specific company/role, tied to something concrete in the job description
- Middle paragraphs: connect your most relevant experience to the role's explicit requirements with specific metrics
- Close with a forward-looking sentence and a thank-you — keep it confident, not desperate
- Tone matches the selector: Professional = measured and precise; Enthusiastic = energetic but still formal; Concise = short and punchy (aim for 3 tight paragraphs)
- End with "Sincerely," followed by a blank line and your name: {CANDIDATE_NAME}
- Do NOT include the header block (name, phone, email, date, company address) — the formatter adds those
- Return only the letter body starting with the salutation
"""

TONES = ["Professional", "Enthusiastic", "Concise"]


def generate_cover_letter(job_description: str, tone: str = "Professional") -> str:
    client = anthropic.Anthropic(api_key=_API_KEY)

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
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
                "content": (
                    f"Tone: {tone}\n\n"
                    f"Job Description:\n{job_description}\n\n"
                    "Write the cover letter now."
                ),
            }
        ],
    )

    return message.content[0].text.strip()
