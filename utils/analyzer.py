"""
Resume Quality Analyzer Module
Analyzes resume quality, ATS compatibility, and provides improvement suggestions
"""
import re
from typing import Dict, List
from collections import Counter


class ResumeQualityAnalyzer:
    """Analyze resume quality and ATS compatibility"""

    def __init__(self):
        self.ats_keywords = [
            "experience", "education", "skills", "projects", "certifications",
            "summary", "objective", "achievements", "awards", "publications"
        ]

        self.action_verbs = [
            "developed", "designed", "implemented", "created", "built", "managed",
            "led", "optimized", "improved", "achieved", "delivered", "launched",
            "architected", "engineered", "automated", "streamlined", "reduced",
            "increased", "generated", "resolved", "coordinated", "collaborated"
        ]

        self.buzzwords_to_avoid = [
            "synergy", "think outside the box", "go-getter", "team player",
            "hard worker", "self-starter", "dynamic", "proactive", "motivated"
        ]

    def analyze(self, resume_data: Dict) -> Dict:
        """Full resume quality analysis"""
        text = resume_data.get("cleaned_text", "")
        sections = resume_data.get("sections", {})

        analysis = {
            "overall_score": 0,
            "ats_score": self._calculate_ats_score(text, sections),
            "formatting_score": self._calculate_formatting_score(resume_data),
            "content_score": self._calculate_content_score(text, sections),
            "keyword_score": self._calculate_keyword_score(text),
            "readability_score": self._calculate_readability(text),
            "suggestions": self._generate_suggestions(text, sections, resume_data),
            "strengths": self._identify_strengths(text, sections),
            "metrics": self._get_metrics(text, sections)
        }

        # Calculate overall score
        weights = {"ats": 0.25, "formatting": 0.20, "content": 0.25, "keyword": 0.15, "readability": 0.15}
        analysis["overall_score"] = round(
            analysis["ats_score"] * weights["ats"] +
            analysis["formatting_score"] * weights["formatting"] +
            analysis["content_score"] * weights["content"] +
            analysis["keyword_score"] * weights["keyword"] +
            analysis["readability_score"] * weights["readability"],
            1
        )

        return analysis

    def _calculate_ats_score(self, text: str, sections: Dict) -> float:
        """Calculate ATS (Applicant Tracking System) compatibility score"""
        score = 0

        # Check for standard section headers
        section_headers = [s.lower() for s in sections.keys()]
        found_headers = sum(1 for h in self.ats_keywords if any(h in sh for sh in section_headers))
        score += (found_headers / len(self.ats_keywords)) * 40

        # Check for contact info
        if re.search(r"[\w.-]+@[\w.-]+\.\w+", text):
            score += 10
        if re.search(r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b", text):
            score += 10

        # Check for standard date formats
        date_patterns = [r"\d{1,2}/\d{4}", r"\d{4}-\d{4}", r"Jan\w*\s+\d{4}"]
        has_dates = any(re.search(p, text) for p in date_patterns)
        if has_dates:
            score += 10

        # Check for bullet points
        if "•" in text or "-" in text:
            score += 10

        # Check for tables/images (would be negative but we can\'t detect easily)
        # Check length
        word_count = len(text.split())
        if 300 <= word_count <= 1500:
            score += 20
        elif word_count < 300:
            score += 10
        else:
            score += 15

        return min(100, score)

    def _calculate_formatting_score(self, resume_data: Dict) -> float:
        """Calculate formatting quality score"""
        score = 0
        text = resume_data.get("cleaned_text", "")

        word_count = len(text.split())

        # Ideal length: 400-800 words
        if 400 <= word_count <= 800:
            score += 30
        elif 300 <= word_count < 400:
            score += 20
        elif 800 < word_count <= 1200:
            score += 20
        else:
            score += 10

        # Consistent formatting (check for headers)
        header_patterns = [r"\n[A-Z][A-Z\s]{2,30}\n", r"\n[A-Z][a-z]+\s+[A-Z][a-z]+\n"]
        has_headers = any(re.search(p, text) for p in header_patterns)
        if has_headers:
            score += 25

        # Proper spacing
        lines = text.split("\n")
        avg_line_length = sum(len(l) for l in lines) / max(len(lines), 1)
        if 30 <= avg_line_length <= 100:
            score += 20

        # No excessive special characters
        special_chars = sum(1 for c in text if c in "!@#$%^&*()_+=[]{}|;:\'\"<>,?/")
        if special_chars / max(len(text), 1) < 0.05:
            score += 25

        return min(100, score)

    def _calculate_content_score(self, text: str, sections: Dict) -> float:
        """Calculate content quality score"""
        score = 0

        # Action verbs usage
        action_count = sum(1 for verb in self.action_verbs if verb in text.lower())
        if action_count >= 10:
            score += 30
        elif action_count >= 5:
            score += 20
        elif action_count >= 2:
            score += 10

        # Quantifiable achievements
        quant_patterns = [r"\d+%", r"\$\d+", r"\d+\s*(million|billion|thousand)", r"increased?\s+by\s+\d+"]
        quant_count = sum(len(re.findall(p, text.lower())) for p in quant_patterns)
        if quant_count >= 3:
            score += 25
        elif quant_count >= 1:
            score += 15

        # Section completeness
        required = ["experience", "education", "skills"]
        has_required = sum(1 for r in required if sections.get(r, "").strip())
        score += (has_required / len(required)) * 25

        # No buzzwords
        buzz_count = sum(1 for b in self.buzzwords_to_avoid if b in text.lower())
        score -= buzz_count * 5

        # Summary/Objective present
        if sections.get("summary", "").strip():
            score += 20

        return max(0, min(100, score))

    def _calculate_keyword_score(self, text: str) -> float:
        """Calculate keyword optimization score"""
        score = 0
        text_lower = text.lower()

        # Technical skills density
        tech_keywords = ["python", "machine learning", "data", "analysis", "sql", "api"]
        tech_count = sum(1 for k in tech_keywords if k in text_lower)
        score += (tech_count / len(tech_keywords)) * 40

        # Industry terms
        industry_terms = ["agile", "scrum", "ci/cd", "cloud", "aws", "docker"]
        industry_count = sum(1 for t in industry_terms if t in text_lower)
        score += (industry_count / len(industry_terms)) * 30

        # Soft skills
        soft_skills = ["leadership", "communication", "collaboration", "problem-solving"]
        soft_count = sum(1 for s in soft_skills if s in text_lower)
        score += (soft_count / len(soft_skills)) * 30

        return min(100, score)

    def _calculate_readability(self, text: str) -> float:
        """Calculate readability score (simplified Flesch)"""
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        words = text.split()

        if not sentences or not words:
            return 50

        avg_sentence_length = len(words) / len(sentences)
        avg_word_length = sum(len(w) for w in words) / len(words)

        # Simplified score (higher is better/easier)
        score = 100 - (avg_sentence_length * 1.5) - (avg_word_length * 5)

        # Normalize to 0-100
        score = max(0, min(100, score))

        return score

    def _generate_suggestions(self, text: str, sections: Dict, resume_data: Dict) -> List[Dict]:
        """Generate improvement suggestions"""
        suggestions = []

        # Length suggestions
        word_count = len(text.split())
        if word_count < 300:
            suggestions.append({
                "priority": "high",
                "category": "Length",
                "message": f"Resume is too short ({word_count} words). Aim for 400-800 words."
            })
        elif word_count > 1500:
            suggestions.append({
                "priority": "medium",
                "category": "Length",
                "message": f"Resume is too long ({word_count} words). Consider condensing to 1-2 pages."
            })

        # Missing sections
        if not sections.get("summary", "").strip():
            suggestions.append({
                "priority": "high",
                "category": "Structure",
                "message": "Add a professional summary or objective statement at the top."
            })

        if not sections.get("skills", "").strip():
            suggestions.append({
                "priority": "high",
                "category": "Structure",
                "message": "Add a dedicated Skills section to highlight your technical abilities."
            })

        # Action verbs
        action_count = sum(1 for verb in self.action_verbs if verb in text.lower())
        if action_count < 5:
            suggestions.append({
                "priority": "medium",
                "category": "Content",
                "message": f"Use more action verbs (found {action_count}). Start bullet points with strong verbs like Developed, Implemented, Led."
            })

        # Quantifiable results
        quant_patterns = [r"\d+%", r"\$\d+", r"increased?\s+by\s+\d+"]
        quant_count = sum(len(re.findall(p, text.lower())) for p in quant_patterns)
        if quant_count < 2:
            suggestions.append({
                "priority": "medium",
                "category": "Content",
                "message": "Add quantifiable achievements (e.g., 'Increased efficiency by 30%')."
            })

        # Buzzwords
        buzz_count = sum(1 for b in self.buzzwords_to_avoid if b in text.lower())
        if buzz_count > 0:
            suggestions.append({
                "priority": "low",
                "category": "Language",
                "message": f"Remove cliché buzzwords ({buzz_count} found). Use specific examples instead."
            })

        # Contact info
        if not re.search(r"[\w.-]+@[\w.-]+\.\w+", text):
            suggestions.append({
                "priority": "high",
                "category": "Contact",
                "message": "Add a professional email address."
            })

        return suggestions

    def _identify_strengths(self, text: str, sections: Dict) -> List[str]:
        """Identify resume strengths"""
        strengths = []

        if sections.get("experience", "").strip():
            strengths.append("Has detailed work experience section")

        if sections.get("education", "").strip():
            strengths.append("Education section is present")

        action_count = sum(1 for verb in self.action_verbs if verb in text.lower())
        if action_count >= 5:
            strengths.append(f"Strong use of action verbs ({action_count} found)")

        quant_patterns = [r"\d+%", r"\$\d+"]
        quant_count = sum(len(re.findall(p, text.lower())) for p in quant_patterns)
        if quant_count >= 3:
            strengths.append("Good use of quantifiable achievements")

        if sections.get("projects", "").strip():
            strengths.append("Includes projects section")

        if sections.get("certifications", "").strip():
            strengths.append("Lists relevant certifications")

        return strengths

    def _get_metrics(self, text: str, sections: Dict) -> Dict:
        """Get detailed metrics"""
        words = text.split()
        sentences = re.split(r"[.!?]+", text)
        sentences = [s.strip() for s in sentences if s.strip()]

        return {
            "word_count": len(words),
            "sentence_count": len(sentences),
            "avg_sentence_length": round(len(words) / max(len(sentences), 1), 1),
            "avg_word_length": round(sum(len(w) for w in words) / max(len(words), 1), 1),
            "section_count": sum(1 for s in sections.values() if s.strip()),
            "action_verbs_count": sum(1 for verb in self.action_verbs if verb in text.lower()),
            "bullet_points": text.count("•") + text.count("-")
        }
