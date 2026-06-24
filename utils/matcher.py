"""
Resume-Job Matching Module
Calculates match scores using multiple algorithms
"""
import numpy as np
from typing import Dict, List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re


class ResumeJobMatcher:
    """Match resumes against job descriptions"""

    def __init__(self, embedding_model=None):
        self.embedding_model = embedding_model
        self.vectorizer = TfidfVectorizer(
            max_features=5000,
            stop_words="english",
            ngram_range=(1, 2)
        )

    def calculate_match_score(
        self,
        resume_data: Dict,
        job_description: str,
        job_skills: List[str],
        weights: Dict[str, float] = None
    ) -> Dict:
        """Calculate comprehensive match score"""

        if weights is None:
            weights = {
                "skills_match": 0.35,
                "experience_match": 0.25,
                "education_match": 0.15,
                "semantic_similarity": 0.15,
                "resume_quality": 0.10
            }

        resume_text = resume_data.get("cleaned_text", "")
        resume_skills = resume_data.get("extracted_skills", {}).get("all_skills", [])
        resume_exp = resume_data.get("experience", {})
        resume_edu = resume_data.get("education", {})

        # 1. Skills Match Score
        skills_score = self._calculate_skills_match(resume_skills, job_skills)

        # 2. Experience Match Score
        exp_score = self._calculate_experience_match(resume_exp, job_description)

        # 3. Education Match Score
        edu_score = self._calculate_education_match(resume_edu, job_description)

        # 4. Semantic Similarity Score
        semantic_score = self._calculate_semantic_similarity(resume_text, job_description)

        # 5. Resume Quality Score
        quality_score = self._calculate_resume_quality(resume_data)

        # Weighted total score
        total_score = (
            weights["skills_match"] * skills_score +
            weights["experience_match"] * exp_score +
            weights["education_match"] * edu_score +
            weights["semantic_similarity"] * semantic_score +
            weights["resume_quality"] * quality_score
        )

        # Skill gap analysis
        skill_gaps = self._identify_skill_gaps(resume_skills, job_skills)

        # Strengths
        strengths = self._identify_strengths(resume_skills, job_skills, resume_exp)

        return {
            "total_score": round(total_score * 100, 2),
            "breakdown": {
                "skills_match": round(skills_score * 100, 2),
                "experience_match": round(exp_score * 100, 2),
                "education_match": round(edu_score * 100, 2),
                "semantic_similarity": round(semantic_score * 100, 2),
                "resume_quality": round(quality_score * 100, 2)
            },
            "skill_gaps": skill_gaps,
            "strengths": strengths,
            "match_level": self._get_match_level(total_score),
            "recommendation": self._get_recommendation(total_score, skill_gaps)
        }

    def _calculate_skills_match(self, resume_skills: List[str], job_skills: List[str]) -> float:
        """Calculate skills match percentage"""
        if not job_skills:
            return 0.5

        resume_skills_lower = [s.lower() for s in resume_skills]
        job_skills_lower = [s.lower() for s in job_skills]

        matched = sum(1 for js in job_skills_lower if any(
            js in rs or rs in js for rs in resume_skills_lower
        ))

        return matched / len(job_skills_lower) if job_skills_lower else 0.0

    def _calculate_experience_match(self, resume_exp: Dict, job_desc: str) -> float:
        """Calculate experience match score"""
        # Extract required years from job description
        year_patterns = [
            r"(\d+)\+?\s*years?\s*(?:of\s*)?experience",
            r"minimum\s*(\d+)\s*years?",
            r"at\s*least\s*(\d+)\s*years?"
        ]

        required_years = 0
        for pattern in year_patterns:
            matches = re.findall(pattern, job_desc.lower())
            if matches:
                required_years = max([int(m) for m in matches])
                break

        candidate_years = resume_exp.get("total_years", 0)

        if required_years == 0:
            return 0.7  # Neutral if not specified

        if candidate_years >= required_years:
            return min(1.0, 0.7 + (candidate_years - required_years) * 0.05)
        else:
            return max(0.0, candidate_years / required_years)

    def _calculate_education_match(self, resume_edu: Dict, job_desc: str) -> float:
        """Calculate education match score"""
        degree_hierarchy = {"phd": 3, "masters": 2, "bachelors": 1, "unknown": 0}

        candidate_degree = resume_edu.get("highest_degree", "unknown")
        candidate_level = degree_hierarchy.get(candidate_degree, 0)

        # Check job requirements
        job_lower = job_desc.lower()
        required_level = 0

        if "phd" in job_lower or "doctorate" in job_lower:
            required_level = 3
        elif "master" in job_lower or "m.tech" in job_lower or "mba" in job_lower:
            required_level = 2
        elif "bachelor" in job_lower or "b.tech" in job_lower:
            required_level = 1

        if required_level == 0:
            return 0.8

        if candidate_level >= required_level:
            return 1.0
        else:
            return max(0.3, candidate_level / required_level)

    def _calculate_semantic_similarity(self, resume_text: str, job_desc: str) -> float:
        """Calculate semantic similarity using TF-IDF + Cosine"""
        try:
            texts = [resume_text, job_desc]
            tfidf_matrix = self.vectorizer.fit_transform(texts)
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            return float(similarity)
        except Exception:
            return 0.5

    def _calculate_resume_quality(self, resume_data: Dict) -> float:
        """Calculate resume quality score"""
        scores = []

        # Length check (ideal: 300-1500 words)
        word_count = resume_data.get("word_count", 0)
        if 300 <= word_count <= 1500:
            scores.append(1.0)
        elif word_count < 200:
            scores.append(0.3)
        elif word_count > 2000:
            scores.append(0.7)
        else:
            scores.append(0.8)

        # Section completeness
        sections = resume_data.get("sections", {})
        required_sections = ["experience", "education", "skills"]
        has_sections = sum(1 for s in required_sections if sections.get(s, "").strip())
        scores.append(has_sections / len(required_sections))

        # Skill diversity
        skill_count = resume_data.get("extracted_skills", {}).get("skill_count", 0)
        if skill_count >= 10:
            scores.append(1.0)
        elif skill_count >= 5:
            scores.append(0.7)
        else:
            scores.append(0.4)

        return sum(scores) / len(scores) if scores else 0.5

    def _identify_skill_gaps(self, resume_skills: List[str], job_skills: List[str]) -> List[Dict]:
        """Identify missing skills"""
        gaps = []
        resume_skills_lower = [s.lower() for s in resume_skills]

        for skill in job_skills:
            skill_lower = skill.lower()
            is_present = any(skill_lower in rs or rs in skill_lower for rs in resume_skills_lower)

            if not is_present:
                gaps.append({
                    "skill": skill,
                    "importance": "high" if len(gaps) < 3 else "medium",
                    "suggestion": f"Consider learning {skill} or taking a certification course."
                })

        return gaps[:10]  # Limit to top 10 gaps

    def _identify_strengths(self, resume_skills: List[str], job_skills: List[str], resume_exp: Dict) -> List[str]:
        """Identify candidate strengths"""
        strengths = []
        resume_skills_lower = [s.lower() for s in resume_skills]
        job_skills_lower = [s.lower() for s in job_skills]

        # Matched key skills
        matched = [js for js in job_skills_lower if any(js in rs or rs in js for rs in resume_skills_lower)]
        if matched:
            strengths.append(f"Strong alignment with {len(matched)} key job requirements")

        # Experience
        years = resume_exp.get("total_years", 0)
        if years >= 5:
            strengths.append(f"Extensive experience ({years}+ years) in the field")
        elif years >= 3:
            strengths.append(f"Solid experience ({years}+ years)")

        # Skill diversity
        if len(resume_skills) >= 15:
            strengths.append("Diverse technical skill set")

        return strengths[:5]

    def _get_match_level(self, score: float) -> str:
        """Get match level description"""
        if score >= 0.8:
            return "Excellent Match"
        elif score >= 0.65:
            return "Good Match"
        elif score >= 0.5:
            return "Average Match"
        elif score >= 0.35:
            return "Below Average"
        else:
            return "Poor Match"

    def _get_recommendation(self, score: float, skill_gaps: List[Dict]) -> str:
        """Get hiring recommendation"""
        if score >= 0.8:
            return "Strongly Recommended - Top candidate with excellent fit"
        elif score >= 0.65:
            gap_count = len(skill_gaps)
            if gap_count <= 2:
                return "Recommended - Good fit with minor skill gaps"
            else:
                return "Recommended with Training - Good potential, needs skill development"
        elif score >= 0.5:
            return "Consider with Caution - Moderate fit, significant gaps"
        else:
            return "Not Recommended - Poor fit for this role"

    def rank_candidates(
        self,
        candidates: List[Dict],
        job_description: str,
        job_skills: List[str]
    ) -> List[Dict]:
        """Rank multiple candidates"""
        ranked = []

        for candidate in candidates:
            match_result = self.calculate_match_score(
                candidate, job_description, job_skills
            )
            ranked.append({
                "candidate": candidate,
                "match_result": match_result,
                "rank": 0
            })

        # Sort by total score descending
        ranked.sort(key=lambda x: x["match_result"]["total_score"], reverse=True)

        # Assign ranks
        for i, item in enumerate(ranked):
            item["rank"] = i + 1

        return ranked
