# 🤖 FUTURE_ML_03 — AI Resume Screening & Candidate Ranking System

> **Task 3: Resume/Candidate Screening System** | Future Interns ML Internship

An intelligent, full-featured ML system that automatically screens, ranks, and analyzes resumes against job descriptions using NLP, TF-IDF semantic similarity, and beautiful visual analytics.

---

## ✨ Features

### Core Features (Required)
- ✅ **Resume Text Parsing** — Extract text from PDF, DOCX, TXT, RTF files
- ✅ **Skill Extraction & Matching** — Match candidate skills with job requirements using a comprehensive skills database
- ✅ **Candidate Ranking** — Score and rank candidates by role fit with a weighted algorithm
- ✅ **Skill Gap Identification** — Highlight missing skills for candidates with improvement suggestions

### Extra Features (Added)
- 🔥 **AI-Powered Semantic Matching** — Using TF-IDF + Cosine Similarity for deep text similarity analysis
- 🔥 **Interactive Web Dashboard** — Beautiful Flask-based UI with real-time results and drag-drop upload
- 🔥 **Batch Processing** — Upload and analyze multiple resumes at once
- 🔥 **ATS Score Calculator** — Automated Applicant Tracking System compatibility scoring
- 🔥 **Resume Quality Analyzer** — Check formatting, length, keyword density, readability, and content quality
- 🔥 **Candidate Comparison Tool** — Side-by-side candidate comparison with detailed metrics
- 🔥 **Export Reports** — JSON export of screening results
- 🔥 **Skill Visualization** — Interactive charts including radar charts, word clouds, quality gauges, and ranking bar charts
- 🔥 **Persistent Results History** — All analyses saved with timestamps for future reference
- 🔥 **Job Description Templates** — Pre-built templates for common ML/AI roles

---

## 📁 Project Structure

```
FUTURE_ML_03/
├── 📂 data/                          # Datasets & sample files
│   ├── job_descriptions.csv          # Sample job descriptions
│   ├── skills_database.json          # Comprehensive skills taxonomy
│   └── sample_resumes/               # Demo resumes (PDF/DOCX/TXT)
│
├── 📂 models/                        # Trained ML models (auto-generated)
│   ├── skill_classifier.pkl          # Skill classification model
│   ├── vectorizer.pkl                # TF-IDF vectorizer
│   └── model_info.json               # Model metadata
│
├── 📂 results/                       # Saved analysis results (auto-generated)
│   └── result_YYYYMMDD_HHMMSS.json
│
├── 📂 templates/                     # HTML templates for web UI
│   ├── index.html                    # Main dashboard — upload & analyze
│   ├── results.html                  # Results page with rankings & details
│   ├── compare.html                  # Side-by-side candidate comparison
│   ├── history.html                  # Past analyses history
│   ├── semantic-match.html           # AI Semantic Matching info page
│   ├── visuals.html                  # Visual Analytics info page
│   ├── ats-check.html                # ATS Compatibility info page
│   └── skill-gaps.html               # Skill Gap Analysis info page
│
├── 📂 uploads/                       # Temporary upload folder (auto-generated)
│
├── app.py                            # Flask web application (run this for UI)
├── main.py                           # CLI entry point (command line usage)
├── train_models.py                   # Model training script (run once)
├── config.py                         # Configuration settings
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
└── HOW_TO_RUN.md                     # Detailed setup guide

# Core ML Modules
├── parser.py                         # Resume parsers (PDF/DOCX/TXT/RTF)
├── extractor.py                      # Skill extractor with regex + skills database
├── matcher.py                        # Resume-job matching (TF-IDF + Cosine + rules)
├── analyzer.py                       # Resume quality analyzer (ATS, formatting, content)
└── visualizer.py                     # Chart generators (radar, word cloud, gauge, bar)
```

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+**
- **pip** package manager

### Installation

```bash
# 1. Clone or extract the project
cd FUTURE_ML_03

# 2. Create virtual environment
python -m venv venv

# Windows
venv\\Scripts\\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train models (one-time setup)
python train_models.py

# 5. Run the web application
python app.py
```

Open your browser and go to: **http://localhost:5000**

---

## 📊 Usage Guide

### Web Dashboard (Recommended)

1. **Upload Resumes** — Drag & drop or click to select multiple PDF/DOCX/TXT files
2. **Select Job Template** — Choose from pre-built templates (ML Engineer, Data Scientist, etc.) or enter a custom job description
3. **Enter Required Skills** — Comma-separated skills (auto-filled from templates)
4. **Click "Analyze Resumes"** — Wait for processing
5. **View Results** — See ranked candidates with scores, skill gaps, and detailed insights
6. **Explore Details** — Click **"Details"** on any candidate to see:
   - **Overview:** Match score breakdown, recommendations, strengths
   - **Skills:** Technical skills, soft skills, top skills by frequency
   - **Quality:** ATS score, formatting score, content score, improvement suggestions
   - **Visuals:** Radar chart, word cloud, quality gauge

### CLI Mode

```bash
# Single resume screening
python main.py --resume "resume.pdf" --job-desc "Job description text here"

# Batch processing
python main.py --batch "resumes_folder/" --job "job_description.txt" --output results.json

# Compare multiple candidates
python main.py --compare "resume1.pdf" "resume2.pdf" --job "job_desc.txt"
```

---

## 🎯 How It Works

### Scoring Algorithm

| Component | Algorithm | Weight |
|-----------|-----------|--------|
| Skills Match | Regex + Skills Database | 35% |
| Experience Match | Years extraction + comparison | 25% |
| Education Match | Degree hierarchy matching | 15% |
| Semantic Similarity | TF-IDF + Cosine Similarity | 15% |
| Resume Quality | Rule-based + heuristic analysis | 10% |

### Skill Extraction

Uses a comprehensive `skills_database.json` with **100+ skills** across categories:
- **Programming:** Python, Java, C++, etc.
- **ML Frameworks:** TensorFlow, PyTorch, Scikit-learn, etc.
- **Databases:** SQL, MongoDB, PostgreSQL, etc.
- **Cloud/DevOps:** AWS, Docker, Kubernetes, etc.
- **Soft Skills:** Communication, Leadership, etc.

### ATS Compatibility Check

- Standard section headers detection
- Contact information validation
- Date format checking
- Bullet point formatting
- Resume length optimization (300–1500 words)
- Keyword density analysis

---

## 📈 Sample Results

The system generates:
- **Ranking Bar Chart** — Color-coded by performance (Green ≥70%, Yellow 50–69%, Red <50%)
- **Radar Chart** — 5-dimensional match score breakdown
- **Word Cloud** — Most frequent keywords from resume
- **Quality Gauge** — Overall resume quality score (0–100)
- **Skills Comparison** — Matched vs missing skills visualization

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| **Backend** | Python, Flask |
| **ML/NLP** | scikit-learn, NLTK, TF-IDF, Cosine Similarity |
| **PDF Parsing** | PyPDF2, pdfplumber |
| **DOCX Parsing** | python-docx |
| **Visualization** | Matplotlib, Seaborn, WordCloud |
| **Frontend** | HTML5, CSS3, JavaScript (vanilla) |
| **Data** | Pandas, NumPy, JSON |

---

## 📋 Requirements

See `requirements.txt` for the full list. Key dependencies:

```
flask>=3.0.0
flask-cors>=5.0.0
scikit-learn>=1.5.0
numpy>=2.1.0
pandas>=2.2.0
matplotlib>=3.9.0
seaborn>=0.13.0
wordcloud>=1.9.3
PyPDF2>=3.0.0
python-docx>=1.1.0
pdfplumber>=0.11.0
nltk>=3.9.0
```

---

## 🎓 Future Interns ML Task 3

This project was built as part of the **Future Interns Machine Learning Internship**.

### Task Requirements Met:
- ✅ Resume text cleaning & parsing
- ✅ Skill extraction & matching with job descriptions
- ✅ Candidate ranking based on role fit
- ✅ Skill gap identification
- ✅ **Additional:** Web UI, visualizations, ATS scoring, persistent history

---

## 📝 License

This project is created for educational purposes as part of the Future Interns ML Internship.

---

## 🙏 Acknowledgments

- **Future Interns** for the internship opportunity
- Built with ❤️ using Python & Flask
