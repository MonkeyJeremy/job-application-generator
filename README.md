# job-application-generator

A Claude Code `/apply` skill that generates tailored cover letters and polished resumes for job applications. Paste a job description, get job-ready `.docx` and `.pdf` files in seconds — powered by the Anthropic API.

## Features

- `/apply` slash command works in any Claude Code session — no resume attachment needed
- Tailors both cover letter and resume to the specific job description
- Exports `.docx` and `.pdf` for both documents
- Three tone options: Professional, Enthusiastic, Concise
- Streamlit web UI available as an alternative interface

**Stack:** Python · Anthropic API · python-docx · docx2pdf · Streamlit

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add your API key

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your-api-key-here
```

### 3. Update the resume

Edit `resume_context.py` with your own resume content, and update `CANDIDATE_NAME`, `CANDIDATE_EMAIL`, and `CANDIDATE_PHONE`.

Also update the resume block inside `.claude/commands/apply.md` so the `/apply` skill always has your latest resume in context.

### 4. Install the Claude Code skill

Copy the skill to your Claude Code commands directory:

```bash
# Mac / Linux
cp .claude/commands/apply.md ~/.claude/commands/apply.md

# Windows
copy .claude\commands\apply.md %USERPROFILE%\.claude\commands\apply.md
```

---

## Usage

### Option A — Claude Code skill (recommended)

In any Claude Code session (desktop app, CLI, or IDE extension):

```
/apply Google
```

Claude will ask for the job description, then generate and save files to `Desktop/Resume/Generated/`.

### Option B — CLI

```bash
python generate.py --company "Google" --jd path/to/jd.txt --tone Professional
```

Flags: `--cover-only`, `--resume-only`, `--tone [Professional|Enthusiastic|Concise]`

### Option C — Streamlit web UI

```bash
streamlit run app.py
```

Open `http://localhost:8501`, paste the job description, and download directly from the browser.

---

## Output

All files are saved to `Desktop/Resume/Generated/`:

```
Google_Cover_Letter.docx
Google_Cover_Letter.pdf
Google_Resume.docx
Google_Resume.pdf
```

---

## Project Structure

```
├── app.py                  # Streamlit UI
├── generate.py             # CLI entry point
├── generator.py            # Cover letter via Claude API
├── resume_polisher.py      # Resume tailoring via Claude API
├── exporter.py             # Cover letter → docx/pdf
├── resume_exporter.py      # Resume → docx/pdf
├── resume_context.py       # Your resume and contact info
├── requirements.txt
└── .claude/
    └── commands/
        └── apply.md        # Claude Code /apply skill
```
