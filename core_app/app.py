"""
Flask Web Application for Resume Screening System
Beautiful UI/UX with real-time analysis and persistent results
"""
import os
import json
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS

from utils.parser import ResumeParser
from utils.extractor import SkillExtractor
from utils.matcher import ResumeJobMatcher
from utils.analyzer import ResumeQualityAnalyzer
from utils.visualizer import Visualizer

app = Flask(__name__)
CORS(app)

# Configuration
app.config["SECRET_KEY"] = "future-interns-ml-2024-secret-key"
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["RESULTS_FOLDER"] = "results"
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024  # 10MB

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
os.makedirs(app.config["RESULTS_FOLDER"], exist_ok=True)

# Initialize components
parser = ResumeParser()
extractor = SkillExtractor()
matcher = ResumeJobMatcher()
analyzer = ResumeQualityAnalyzer()
visualizer = Visualizer()

ALLOWED_EXTENSIONS = {"pdf", "docx", "txt", "rtf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    """Main dashboard page"""
    return render_template("index.html")


@app.route("/results")
def results():
    """Results page"""
    return render_template("results.html")


@app.route("/compare")
def compare():
    """Comparison page"""
    return render_template("compare.html")


@app.route("/history")
def history():
    """History page - all past analyses"""
    return render_template("history.html")

@app.route("/semantic-match")
def semantic_match():
    """AI Semantic Matching info page"""
    return render_template("semantic-match.html")

@app.route("/visuals")
def visuals():
    """Visual Analytics info page"""
    return render_template("visuals.html")

@app.route("/ats-check")
def ats_check():
    """ATS Compatibility info page"""
    return render_template("ats-check.html")

@app.route("/skill-gaps")
def skill_gaps():
    """Skill Gap Analysis info page"""
    return render_template("skill-gaps.html")


@app.route("/api/upload", methods=["POST"])
def upload_resumes():
    """Upload and process resumes"""
    if "resumes" not in request.files:
        return jsonify({"error": "No files uploaded"}), 400

    files = request.files.getlist("resumes")
    job_desc = request.form.get("job_description", "")
    job_skills_text = request.form.get("job_skills", "")

    if not job_desc:
        return jsonify({"error": "Job description is required"}), 400

    job_skills = [s.strip() for s in job_skills_text.split(",") if s.strip()]

    processed = []
    errors = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"],
                                    f"{uuid.uuid4()}_{filename}")
            file.save(file_path)

            try:
                # Parse resume
                resume_data = parser.parse(file_path)

                # Extract skills
                skills_data = extractor.extract_skills(resume_data["cleaned_text"])
                resume_data["extracted_skills"] = skills_data

                # Extract experience & education
                resume_data["experience"] = extractor.extract_experience_years(
                    resume_data["cleaned_text"]
                )
                resume_data["education"] = extractor.extract_education(
                    resume_data["cleaned_text"]
                )

                # Calculate match
                match_result = matcher.calculate_match_score(
                    resume_data, job_desc, job_skills
                )

                # Analyze quality
                quality_analysis = analyzer.analyze(resume_data)

                # Generate visualizations
                radar_chart = visualizer.create_radar_chart(match_result["breakdown"])
                wordcloud = visualizer.create_wordcloud(resume_data["cleaned_text"])
                quality_gauge = visualizer.create_quality_gauge(
                    quality_analysis["overall_score"]
                )

                processed.append({
                    "id": str(uuid.uuid4()),
                    "file_name": resume_data["file_name"],
                    "word_count": resume_data["word_count"],
                    "match_result": match_result,
                    "skills": skills_data,
                    "experience": resume_data["experience"],
                    "education": resume_data["education"],
                    "quality_analysis": quality_analysis,
                    "visualizations": {
                        "radar_chart": radar_chart,
                        "wordcloud": wordcloud,
                        "quality_gauge": quality_gauge
                    }
                })

            except Exception as e:
                errors.append({"file": filename, "error": str(e)})
            finally:
                # Clean up uploaded file
                if os.path.exists(file_path):
                    os.remove(file_path)

    # Rank candidates
    if len(processed) > 1:
        candidates = []
        for p in processed:
            candidates.append({
                "file_name": p["file_name"],
                "cleaned_text": "",
                "extracted_skills": p["skills"],
                "experience": p["experience"],
                "education": p["education"],
                "word_count": p["word_count"],
                "sections": {}
            })

        ranked = matcher.rank_candidates(candidates, job_desc, job_skills)

        # Update processed with ranks
        for p in processed:
            for r in ranked:
                if r["candidate"]["file_name"] == p["file_name"]:
                    p["rank"] = r["rank"]
                    break

        # Generate ranking chart
        ranking_chart = visualizer.create_ranking_chart(ranked)
    else:
        ranking_chart = None
        if processed:
            processed[0]["rank"] = 1

    # SAVE RESULTS TO FILE (Persistent!)
    result_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_data = {
        "result_id": result_id,
        "timestamp": datetime.now().isoformat(),
        "job_description": job_desc,
        "job_skills": job_skills,
        "total_processed": len(processed),
        "errors": errors,
        "candidates": processed,
        "ranking_chart": ranking_chart
    }

    # Save to results folder
    result_file = os.path.join(app.config["RESULTS_FOLDER"], f"result_{result_id}.json")
    with open(result_file, "w") as f:
        json.dump(result_data, f, indent=2, default=str)

    return jsonify({
        "success": True,
        "result_id": result_id,
        "total_processed": len(processed),
        "errors": errors,
        "candidates": processed,
        "ranking_chart": ranking_chart
    })


@app.route("/api/results", methods=["GET"])
def get_all_results():
    """Get all saved results"""
    results = []
    for filename in sorted(os.listdir(app.config["RESULTS_FOLDER"]), reverse=True):
        if filename.endswith(".json"):
            filepath = os.path.join(app.config["RESULTS_FOLDER"], filename)
            with open(filepath, "r") as f:
                data = json.load(f)
                results.append({
                    "result_id": data.get("result_id"),
                    "timestamp": data.get("timestamp"),
                    "total_candidates": data.get("total_processed", 0),
                    "file": filename
                })
    return jsonify(results)


@app.route("/api/results/<result_id>", methods=["GET"])
def get_result(result_id):
    """Get a specific result by ID"""
    filepath = os.path.join(app.config["RESULTS_FOLDER"], f"result_{result_id}.json")
    if os.path.exists(filepath):
        with open(filepath, "r") as f:
            return jsonify(json.load(f))
    return jsonify({"error": "Result not found"}), 404


@app.route("/api/results/<result_id>", methods=["DELETE"])
def delete_result(result_id):
    """Delete a specific result"""
    filepath = os.path.join(app.config["RESULTS_FOLDER"], f"result_{result_id}.json")
    if os.path.exists(filepath):
        os.remove(filepath)
        return jsonify({"success": True, "message": "Result deleted"})
    return jsonify({"error": "Result not found"}), 404


@app.route("/api/job-templates", methods=["GET"])
def get_job_templates():
    """Get sample job description templates"""
    templates = [
        {
            "id": 1,
            "title": "Machine Learning Engineer",
            "description": "We are seeking a skilled Machine Learning Engineer to design and implement ML models. You will work with large datasets, build predictive models, and deploy solutions to production. The ideal candidate has strong Python skills and experience with deep learning frameworks.",
            "skills": "Python, Machine Learning, Deep Learning, TensorFlow, PyTorch, SQL, Scikit-learn, AWS, Docker"
        },
        {
            "id": 2,
            "title": "Data Scientist",
            "description": "Join our data science team to extract insights from complex data. You will build statistical models, create visualizations, and communicate findings to stakeholders. Experience with NLP and time-series analysis is a plus.",
            "skills": "Python, R, SQL, Statistics, Machine Learning, Data Visualization, Tableau, Pandas, NumPy"
        },
        {
            "id": 3,
            "title": "Software Engineer - AI/ML",
            "description": "Build scalable AI-powered features for our product. Integrate ML models into production systems. Optimize inference speed and model performance.",
            "skills": "Python, Java, Machine Learning, REST APIs, Microservices, Docker, Kubernetes, Git, SQL"
        },
        {
            "id": 4,
            "title": "NLP Engineer",
            "description": "Specialize in natural language processing solutions. Build chatbots, sentiment analysis systems, and text classification models. Experience with transformers and large language models preferred.",
            "skills": "Python, NLP, Transformers, BERT, spaCy, NLTK, Deep Learning, Machine Learning, FastAPI"
        },
        {
            "id": 5,
            "title": "Data Analyst",
            "description": "Analyze business data to drive strategic decisions. Create dashboards, reports, and automated data pipelines. Work closely with business teams to understand requirements.",
            "skills": "SQL, Excel, Tableau, Power BI, Python, Pandas, Data Visualization, Statistics, ETL"
        }
    ]
    return jsonify(templates)


@app.route("/api/skills-database", methods=["GET"])
def get_skills_database():
    """Get skills database"""
    try:
        with open("data/skills_database.json", "r") as f:
            skills_db = json.load(f)
        return jsonify(skills_db)
    except FileNotFoundError:
        return jsonify({"error": "Skills database not found"}), 404


@app.route("/api/export/<result_id>", methods=["GET"])
def export_result(result_id):
    """Export a specific result"""
    filepath = os.path.join(app.config["RESULTS_FOLDER"], f"result_{result_id}.json")
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True, download_name=f"screening_result_{result_id}.json")
    return jsonify({"error": "Result not found"}), 404


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })


if __name__ == "__main__":
    print("=" * 60)
    print("Resume Screening System - Web Dashboard")
    print("=" * 60)
    print("\nOpen your browser and go to: http://localhost:5000")
    print("\nPress Ctrl+C to stop the server\n")
    app.run(host="0.0.0.0", port=5000, debug=True)
