"""
CLI entry point for the cover letter + resume generator.

Usage:
    python generate.py --company "Dialpad" --jd "path/to/jd.txt"
    python generate.py --company "Dialpad" --jd -          (reads from stdin)
    python generate.py --company "Dialpad" --tone Concise --resume-only
    python generate.py --company "Dialpad" --cover-only
"""
import argparse
import sys
from pathlib import Path

# Output directory: Desktop/Resume/Generated
OUTPUT_DIR = Path.home() / "Desktop" / "Resume" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

from generator import generate_cover_letter, TONES
from exporter import to_docx, to_pdf
from resume_polisher import polish_resume
from resume_exporter import resume_to_docx, resume_to_pdf


def save(data: bytes, path: Path) -> Path:
    path.write_bytes(data)
    return path


def run(company: str, jd: str, tone: str, cover_only: bool, resume_only: bool):
    safe = company.replace(" ", "_")
    results = []

    if not resume_only:
        print(f"  Generating cover letter ({tone})…", flush=True)
        letter = generate_cover_letter(jd, tone)
        cl_docx = to_docx(letter, company=company)
        cl_pdf = to_pdf(cl_docx)
        p = save(cl_docx, OUTPUT_DIR / f"{safe}_Cover_Letter.docx")
        results.append(f"Cover letter .docx  →  {p}")
        if cl_pdf:
            p = save(cl_pdf, OUTPUT_DIR / f"{safe}_Cover_Letter.pdf")
            results.append(f"Cover letter .pdf   →  {p}")

    if not cover_only:
        print("  Polishing resume…", flush=True)
        data = polish_resume(jd)
        res_docx = resume_to_docx(data)
        res_pdf = resume_to_pdf(res_docx)
        p = save(res_docx, OUTPUT_DIR / f"{safe}_Resume.docx")
        results.append(f"Resume .docx        →  {p}")
        if res_pdf:
            p = save(res_pdf, OUTPUT_DIR / f"{safe}_Resume.pdf")
            results.append(f"Resume .pdf         →  {p}")

    print("\nDone! Files saved:")
    for r in results:
        print(f"  {r}")


def main():
    parser = argparse.ArgumentParser(description="Generate cover letter and/or polished resume.")
    parser.add_argument("--company", required=True, help="Company name")
    parser.add_argument("--jd", required=True,
                        help="Path to job description text file, or '-' to read from stdin")
    parser.add_argument("--tone", choices=TONES, default="Professional")
    parser.add_argument("--cover-only", action="store_true")
    parser.add_argument("--resume-only", action="store_true")
    args = parser.parse_args()

    if args.jd == "-":
        jd = sys.stdin.read().strip()
    else:
        jd = Path(args.jd).read_text(encoding="utf-8").strip()

    if not jd:
        print("Error: job description is empty.", file=sys.stderr)
        sys.exit(1)

    run(args.company, jd, args.tone, args.cover_only, args.resume_only)


if __name__ == "__main__":
    main()
