# How to Run - Resume Screening System

## Quick Start (5 minutes)

### Step 1: Install Python
- Download Python 3.10+ from python.org
- IMPORTANT: Check "Add Python to PATH" during installation

### Step 2: Install VS Code
- Download from code.visualstudio.com
- Install the Python extension (by Microsoft)

### Step 3: Extract & Open Project
1. Extract FUTURE_ML_03.zip to a folder
2. Open VS Code
3. Click File -> Open Folder -> Select FUTURE_ML_03

### Step 4: Open Terminal in VS Code
- Press Ctrl + ` (backtick) OR
- Click Terminal -> New Terminal

### Step 5: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

You should see (venv) in your terminal prompt.

### Step 6: Install Dependencies
```bash
pip install -r requirements.txt
```

This may take 2-5 minutes.

### Step 7: Download NLTK Data
```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
```

### Step 8: Train Models (One-time setup)
```bash
python train_models.py
```

### Step 9: Run the Web App
```bash
python app.py
```

Open your browser and go to: http://localhost:5000

---

## File Structure Overview

```
FUTURE_ML_03/
├── app.py              <- Flask web server (run this for UI)
├── main.py             <- CLI tool (for command line usage)
├── train_models.py     <- Train ML models (run once)
├── config.py           <- Settings and configuration
├── requirements.txt    <- Python packages to install
├── README.md           <- Project documentation
├── HOW_TO_RUN.md       <- This file
│
├── data/               <- Datasets
│   ├── job_descriptions.csv
│   ├── skills_database.json
│   └── sample_resumes/ <- Add your test resumes here
│
├── models/             <- Trained models (auto-generated)
├── utils/              <- Core ML modules
│   ├── parser.py       <- PDF/DOCX/TXT parser
│   ├── extractor.py    <- Skill extraction
│   ├── matcher.py      <- Resume-job matching
│   ├── analyzer.py     <- Resume quality analysis
│   └── visualizer.py   <- Chart generation
│
├── templates/          <- HTML pages
│   ├── index.html      <- Upload dashboard
│   ├── results.html    <- Results page
│   └── compare.html    <- Comparison page
│
└── notebooks/          <- Jupyter notebooks
```

---

## Using the Web Dashboard

1. Upload Resumes - Click upload area or drag & drop files
2. Enter Job Description - Paste text or select template
3. Click "Analyze Resumes" - Wait for processing
4. View Results - See rankings, details, charts

---

## Using Command Line (CLI)

Single Resume:
```bash
python main.py --resume "resume.pdf" --job-desc "Job description"
```

Batch Processing:
```bash
python main.py --batch "resumes_folder/" --job "job.txt" --output results.json
```

---

## Troubleshooting

"ModuleNotFoundError" -> Run: pip install -r requirements.txt
"Cant find model" -> Run: python -m spacy download en_core_web_lg
"Port 5000 in use" -> Change port in app.py to 5001

---

## GitHub Upload

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/FUTURE_ML_03.git
git push -u origin main
```

Repository name must be: FUTURE_ML_03
