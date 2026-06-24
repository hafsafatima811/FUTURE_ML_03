"""
Configuration settings for Resume Screening System
"""
import os

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODELS_DIR = os.path.join(BASE_DIR, "models")
STATIC_DIR = os.path.join(BASE_DIR, "static")
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

# File upload settings
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "rtf"}

# Model settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Sentence-BERT model
SKILL_SIMILARITY_THRESHOLD = 0.75
SEMANTIC_MATCH_THRESHOLD = 0.65

# Scoring weights
WEIGHTS = {
    "skills_match": 0.35,
    "experience_match": 0.25,
    "education_match": 0.15,
    "semantic_similarity": 0.15,
    "resume_quality": 0.10
}

# Quality thresholds
MIN_RESUME_LENGTH = 200
MAX_RESUME_LENGTH = 5000
IDEAL_RESUME_PAGES = 2

# Visualization settings
CHART_THEME = "plotly_white"
COLOR_PALETTE = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A", "#19D3F3"]

# Flask settings
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
FLASK_DEBUG = True
SECRET_KEY = "future-interns-ml-2024-secret-key"
