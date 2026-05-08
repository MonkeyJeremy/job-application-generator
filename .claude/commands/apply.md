---
name: apply
description: Generate a tailored cover letter and polished resume for a job application. Takes a company name and job description, calls the cover-letter-gen scripts, and saves .docx and .pdf files to Desktop/Resume/output/. Jeremy's resume is embedded — no attachment needed.
---

You are helping Jeremy Zhang apply for jobs. His full resume is below — you never need to ask him for it.

## Jeremy's Resume

```
Jeremy Zhang
(858) 405-5600 | jeremiahzhang1999@gmail.com | U.S. Citizen

EDUCATION
University of California, San Diego — La Jolla, CA
Bachelor of Science in Data Science, Business Minor | Sept 2018 – Sept 2024
Relevant Coursework: Data Analytics, Business Analytics, Strategic Planning, Financial Analytics,
Risk Assessment, Data Structures & Algorithms, Probability & Statistics, Machine Learning &
Deep Learning, Data Science, Market Management

SKILLS
Programming: Python (Pandas, NumPy, Scikit-learn, SciPy, Requests, BeautifulSoup), SQL (MySQL,
SQL Server), R, Excel, Stata, MATLAB
Analytical: A/B testing, Logistic Regression, Random Forest, XGBoost, SVM, Imputation, Correlation Analysis
Data Visualization: Tableau, Power BI, Matplotlib, Seaborn, ggplot
Software & Tools: Looker Studio, AWS (S3, EC2, Redshift, RDS), Jupyter Notebook, VS Code, GitHub, Claude Code

PROFESSIONAL EXPERIENCE

Sciencia AI — Remote, USA
Data Analytics Intern | Feb 2026 – Apr 2026
- Built modular web scraping pipelines using Python (BeautifulSoup, Requests), collecting 100K+
  user reviews with >95% extraction success rate
- Designed relational database schemas in PostgreSQL, improving query performance by ~40%
- Developed automated data cleaning and ingestion workflows, ensuring >98% data completeness
- Trained sentiment analysis models achieving ~85% classification accuracy, informing product strategy
- Created Tableau dashboards visualizing sentiment trends and KPIs, cutting reporting time by 50%

Bray & Co — Remote, USA
Marketing Analytics Intern | Oct 2024 – Jan 2025
- Built advertisement metric dashboard reporting CTR and ROI to guide CS Disco's digital marketing strategy
- Identified ad effectiveness trends using correlation and logistic regression (Python sklearn, scipy)
- Visualized best-performing channels and regression trends with Matplotlib and Looker Studio

Unilever — Shanghai, China
Business Insights Intern | Sept 2021 – Dec 2021
- Forecasted industry growth in fragrance, pet care, and virtual IP using industry reports and consumer data
- Led development of Slogan Builder, an ML platform using n-gram and bag-of-words models

PROJECT EXPERIENCE

Detecting Fraud with Oversampling Techniques and Sparsity Constraints | Sept 2023 – Mar 2024
- Built fraud detection for Amazon, Yelp, and Reddit using GraphSMOTE and GNN models, achieving 7%+ accuracy gain
- Led three-person team; implemented synthetic node generation and cosine similarity via single-layer GCN embedding

ER Game Market Strategy Analysis | Mar 2023 – Jun 2023
- Conducted global market analysis of video game genres across North America, Europe, and Japan
- Performed KPI analysis and A/B testing on platform, genre, and geography vs. game sales
- Identified strategic partnership opportunities with Bethesda Softworks and Nintendo
```

## How to run this skill

When the user invokes `/apply`, follow these steps:

### Step 1 — Collect inputs

If the user invoked `/apply` with no arguments, ask:
1. **Company name** (e.g. "Dialpad")
2. **Job description** — ask them to paste it
3. **Tone** (optional, default Professional) — Professional / Enthusiastic / Concise
4. **What to generate** (optional, default Both) — Both / Cover Letter only / Resume only

If they provided arguments inline (e.g. `/apply Dialpad`), use those and ask only for what's missing.

### Step 2 — Save the job description to a temp file

Write the pasted job description to a temporary file:
```
C:\Users\Jeremy Zhang\AppData\Local\Temp\jd_input.txt
```

### Step 3 — Run the generator

Run the following Bash command from the project directory:
```bash
cd "E:\张竞予\Claude Code\cover-letter-gen" && python generate.py \
  --company "<COMPANY>" \
  --jd "C:\Users\Jeremy Zhang\AppData\Local\Temp\jd_input.txt" \
  --tone "<TONE>"
```

Add `--cover-only` or `--resume-only` flags if the user chose a single output.

### Step 4 — Report results

After the script runs, report the file paths that were saved (the script prints them).
Tell the user the files are in `Desktop\Resume\Generated\`.

### Rules
- Never ask Jeremy to attach or provide his resume — it is already above.
- If the script fails, show the error and suggest running `pip install -r requirements.txt` in the project directory.
- Output directory is always `C:\Users\Jeremy Zhang\Desktop\Resume\output\`.
