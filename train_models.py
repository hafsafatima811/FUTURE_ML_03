"""
Model Training Script
Trains and saves ML models for resume screening
"""
import os
import pickle
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import numpy as np


def train_models():
    """Train and save all models"""
    print("=" * 60)
    print("🚀 Training Resume Screening Models")
    print("=" * 60)

    models_dir = "models"
    os.makedirs(models_dir, exist_ok=True)

    # 1. TF-IDF Vectorizer
    print("\n📊 Training TF-IDF Vectorizer...")

    # Sample training texts (synthetic data for demonstration)
    sample_texts = [
        "Python machine learning data analysis SQL pandas numpy scikit-learn tensorflow",
        "Java spring boot microservices docker kubernetes AWS cloud development",
        "React javascript typescript node.js frontend web development HTML CSS",
        "Data scientist python R statistics machine learning deep learning NLP",
        "DevOps engineer AWS Azure docker kubernetes CI/CD terraform ansible",
        "Product manager agile scrum Jira confluence stakeholder management strategy",
        "Computer vision engineer OpenCV PyTorch CNN image processing deep learning",
        "NLP engineer transformers BERT GPT spaCy NLTK text classification",
        "Full stack developer python django react javascript postgresql redis",
        "Data engineer ETL spark hadoop airflow python SQL data warehouse",
        "Business analyst SQL excel tableau power BI data visualization reporting",
        "Mobile developer swift kotlin iOS android flutter react native",
        "Cybersecurity engineer network security penetration testing SIEM firewall",
        "Cloud architect AWS Azure GCP infrastructure terraform cloudformation",
        "UX designer figma sketch adobe XD user research wireframing prototyping"
    ]

    vectorizer = TfidfVectorizer(
        max_features=1000,
        stop_words="english",
        ngram_range=(1, 2),
        min_df=1
    )

    X = vectorizer.fit_transform(sample_texts)

    with open(f"{models_dir}/vectorizer.pkl", "wb") as f:
        pickle.dump(vectorizer, f)
    print("✅ Vectorizer saved to models/vectorizer.pkl")

    # 2. Skill Classification Model
    print("\n🤖 Training Skill Classification Model...")

    # Synthetic labels for demonstration
    labels = [
        "ml_engineer", "backend_dev", "frontend_dev", "data_scientist",
        "devops", "product_manager", "cv_engineer", "nlp_engineer",
        "fullstack_dev", "data_engineer", "business_analyst", "mobile_dev",
        "security_engineer", "cloud_architect", "ux_designer"
    ]

    classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    classifier.fit(X, labels)

    with open(f"{models_dir}/skill_classifier.pkl", "wb") as f:
        pickle.dump(classifier, f)
    print("✅ Classifier saved to models/skill_classifier.pkl")

    # 3. Save skills database reference
    print("\n💾 Saving reference data...")

    reference_data = {
        "vectorizer_features": vectorizer.get_feature_names_out().tolist(),
        "label_classes": labels,
        "training_samples": len(sample_texts)
    }

    with open(f"{models_dir}/model_info.json", "w") as f:
        json.dump(reference_data, f, indent=2)
    print("✅ Model info saved to models/model_info.json")

    print("\n" + "=" * 60)
    print("✅ All models trained and saved successfully!")
    print("=" * 60)
    print("\nModels ready for use in the application.")


if __name__ == "__main__":
    train_models()
