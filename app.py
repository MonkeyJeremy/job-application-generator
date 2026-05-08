import os

import streamlit as st

from generator import generate_cover_letter, TONES
from exporter import to_docx, to_pdf
from resume_polisher import polish_resume
from resume_exporter import resume_to_docx, resume_to_pdf

st.set_page_config(page_title="Job Application Generator", page_icon="📄", layout="wide")

st.title("📄 Job Application Generator")
st.caption("Paste a job description → get a tailored cover letter and polished resume → download as PDF")

# ── Sidebar ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("Settings")
    company = st.text_input("Company name", placeholder="e.g. Dialpad",
                            help="Used in the cover letter header and file names")
    tone = st.selectbox("Cover letter tone", TONES, index=0)
    st.divider()
    st.markdown("**How to use**")
    st.markdown(
        "1. Enter the company name\n"
        "2. Paste the job description\n"
        "3. Click **Generate Both** (or individual tab buttons)\n"
        "4. Edit either document\n"
        "5. Download `.docx` or `.pdf`"
    )

# ── Job description input ──────────────────────────────────────────────────
job_description = st.text_area(
    "Job description",
    height=220,
    placeholder="Paste the full job description here…",
    key="jd_input",
)

col_gen1, col_gen2, col_gen3 = st.columns([2, 2, 4])
with col_gen1:
    gen_both = st.button("✨ Generate Both", type="primary", disabled=not job_description.strip())
with col_gen2:
    gen_cl = st.button("📝 Cover Letter only", disabled=not job_description.strip())
with col_gen3:
    gen_resume = st.button("📋 Polish Resume only", disabled=not job_description.strip())

# ── Session state init ─────────────────────────────────────────────────────
for key in ("cover_letter", "resume_data"):
    if key not in st.session_state:
        st.session_state[key] = None

# ── Generation logic ───────────────────────────────────────────────────────
if (gen_both or gen_cl) and job_description.strip():
    with st.spinner("Writing cover letter…"):
        st.session_state.cover_letter = generate_cover_letter(job_description, tone)

if (gen_both or gen_resume) and job_description.strip():
    with st.spinner("Polishing resume…"):
        st.session_state.resume_data = polish_resume(job_description)

# ── Output tabs ────────────────────────────────────────────────────────────
if st.session_state.cover_letter or st.session_state.resume_data:
    st.divider()
    tab_cl, tab_resume = st.tabs(["📝 Cover Letter", "📋 Resume"])

    # ── Cover Letter tab ───────────────────────────────────────────────────
    with tab_cl:
        if st.session_state.cover_letter:
            edited_cl = st.text_area(
                "Review and edit",
                value=st.session_state.cover_letter,
                height=380,
                key="cl_editor",
            )
            safe_co = company.strip().replace(" ", "_") if company.strip() else "Cover_Letter"
            cl_docx = to_docx(edited_cl, company=company.strip())
            cl_pdf = to_pdf(cl_docx)

            c1, c2 = st.columns(2)
            with c1:
                st.download_button(
                    "⬇️ Download Cover Letter .docx",
                    data=cl_docx,
                    file_name=f"{safe_co}_Cover_Letter.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            with c2:
                if cl_pdf:
                    st.download_button(
                        "⬇️ Download Cover Letter .pdf",
                        data=cl_pdf,
                        file_name=f"{safe_co}_Cover_Letter.pdf",
                        mime="application/pdf",
                    )
                else:
                    st.button("⬇️ Download Cover Letter .pdf", disabled=True,
                              help="Requires Microsoft Word")
        else:
            st.info("Click **Generate Both** or **Cover Letter only** to generate.")

    # ── Resume tab ─────────────────────────────────────────────────────────
    with tab_resume:
        if st.session_state.resume_data:
            data = st.session_state.resume_data

            # Editable skills
            st.subheader("Skills")
            skills = data.get("skills", {})
            edited_skills = {}
            for cat, items in skills.items():
                edited_skills[cat] = st.text_input(cat, value=items, key=f"skill_{cat}")
            data["skills"] = edited_skills

            # Editable summary
            st.subheader("Summary (optional)")
            data["summary"] = st.text_area(
                "Leave blank to omit",
                value=data.get("summary", ""),
                height=80,
                key="resume_summary",
            )

            # Read-only preview of experience bullets
            st.subheader("Experience & Projects")
            st.caption("Bullet points are shown below. To edit further, download the .docx and edit in Word.")
            for job in data.get("experience", []):
                with st.expander(f"{job['company']} — {job['title']}"):
                    for b in job.get("bullets", []):
                        st.markdown(f"- {b}")
            for proj in data.get("projects", []):
                with st.expander(proj["name"]):
                    for b in proj.get("bullets", []):
                        st.markdown(f"- {b}")

            safe_co = company.strip().replace(" ", "_") if company.strip() else "Resume"
            res_docx = resume_to_docx(data)
            res_pdf = resume_to_pdf(res_docx)

            c1, c2 = st.columns(2)
            with c1:
                st.download_button(
                    "⬇️ Download Resume .docx",
                    data=res_docx,
                    file_name=f"{safe_co}_Resume.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                )
            with c2:
                if res_pdf:
                    st.download_button(
                        "⬇️ Download Resume .pdf",
                        data=res_pdf,
                        file_name=f"{safe_co}_Resume.pdf",
                        mime="application/pdf",
                    )
                else:
                    st.button("⬇️ Download Resume .pdf", disabled=True,
                              help="Requires Microsoft Word")
        else:
            st.info("Click **Generate Both** or **Polish Resume only** to tailor your resume.")
