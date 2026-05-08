---
name: apply
description: Generate a tailored cover letter and polished resume for a job application. Takes a company name and job description, calls the cover-letter-gen scripts, and saves .docx and .pdf files to Desktop/Resume/output/. Your resume is embedded in your local copy — no attachment needed.
---

You are helping [YOUR NAME] apply for jobs. Their full resume is below — you never need to ask for it.

## Your Resume

Paste your resume here. See `resume_context.example.py` for the expected format.

```
[YOUR RESUME TEXT HERE]
```

## How to run this skill

When the user invokes `/apply`, follow these steps:

### Step 1 — Collect inputs

If the user invoked `/apply` with no arguments, ask:
1. **Company name** (e.g. "Google")
2. **Job description** — ask them to paste it
3. **Tone** (optional, default Professional) — Professional / Enthusiastic / Concise
4. **What to generate** (optional, default Both) — Both / Cover Letter only / Resume only

If they provided arguments inline (e.g. `/apply Google`), use those and ask only for what's missing.

### Step 2 — Save the job description to a temp file

Write the pasted job description to a temporary file:
```
[YOUR TEMP PATH]\jd_input.txt
```
e.g. `C:\Users\YourName\AppData\Local\Temp\jd_input.txt`

### Step 3 — Run the generator

Run the following command from the project directory:
```bash
cd "[PATH TO cover-letter-gen]" && python generate.py \
  --company "<COMPANY>" \
  --jd "[YOUR TEMP PATH]\jd_input.txt" \
  --tone "<TONE>"
```

Add `--cover-only` or `--resume-only` flags if the user chose a single output.

### Step 4 — Report results

After the script runs, report the file paths that were saved (the script prints them).
Files are saved to `Desktop\Resume\output\`.

### Rules
- Never ask the user to attach or provide their resume — it is embedded above.
- If the script fails, suggest running `pip install -r requirements.txt` in the project directory.
