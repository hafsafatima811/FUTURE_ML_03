"""
Skill Extractor Module
Extracts skills from resume text using pattern matching and NLTK
"""
import json
import re
from typing import List, Dict, Set, Tuple
from collections import Counter


class SkillExtractor:
    """Extract skills from resume text using regex and keyword matching"""

    def __init__(self, skills_db_path: str = "data/skills_database.json"):
        self.skills_db = self._load_skills_db(skills_db_path)
        self.all_skills = self._build_skill_list()

    def _load_skills_db(self, path: str) -> Dict:
        """Load skills database"""
        try:
            with open(path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "technical_skills": {
                    "programming": ["Python", "Java", "C++", "R", "SQL", "JavaScript", "TypeScript"],
                    "frameworks": ["TensorFlow", "PyTorch", "Scikit-learn", "Django", "Flask", "FastAPI"],
                    "databases": ["MySQL", "PostgreSQL", "MongoDB", "Redis", "Elasticsearch"],
                    "cloud": ["AWS", "Azure", "GCP", "Docker", "Kubernetes"]
                },
                "soft_skills": ["Communication", "Leadership", "Teamwork", "Problem Solving"]
            }

    def _build_skill_list(self) -> Set[str]:
        """Build flat list of all skills with variants"""
        skills = set()
        for category, skill_list in self.skills_db.get("technical_skills", {}).items():
            skills.update(skill_list)
        skills.update(self.skills_db.get("soft_skills", []))
        skills.update([s.lower() for s in skills])
        return skills

    def extract_skills(self, text: str) -> Dict:
        """Extract skills from text using pattern matching"""
        text_lower = text.lower()
        found_skills = {
            "technical": [],
            "soft": [],
            "programming": [],
            "frameworks": [],
            "databases": [],
            "cloud_devops": [],
            "other": []
        }

        # Pattern-based extraction with word boundaries
        for skill in self.all_skills:
            skill_lower = skill.lower()
            pattern = r"\b" + re.escape(skill_lower) + r"\b"
            if re.search(pattern, text_lower):
                self._categorize_skill(skill, found_skills)

        # Remove duplicates and sort
        for category in found_skills:
            found_skills[category] = sorted(list(set(found_skills[category])))

        skill_freq = self._calculate_frequency(text, found_skills)

        return {
            "skills_by_category": found_skills,
            "all_skills": sorted(list(set(
                [s for cat in found_skills.values() for s in cat]
            ))),
            "skill_count": sum(len(v) for v in found_skills.values()),
            "skill_frequency": skill_freq,
            "top_skills": self._get_top_skills(skill_freq, 10)
        }

    def _categorize_skill(self, skill: str, found_skills: Dict):
        """Categorize a skill into appropriate bucket"""
        skill_lower = skill.lower()
        categorized = False

        for category, skill_list in self.skills_db.get("technical_skills", {}).items():
            if skill in skill_list or skill.lower() in [s.lower() for s in skill_list]:
                if category == "programming":
                    found_skills["programming"].append(skill)
                elif category == "frameworks":
                    found_skills["frameworks"].append(skill)
                elif category == "databases":
                    found_skills["databases"].append(skill)
                elif category == "cloud_devops":
                    found_skills["cloud_devops"].append(skill)
                else:
                    found_skills["technical"].append(skill)
                categorized = True
                break

        if not categorized:
            soft_skills = self.skills_db.get("soft_skills", [])
            if skill in soft_skills or skill.lower() in [s.lower() for s in soft_skills]:
                found_skills["soft"].append(skill)
            else:
                found_skills["other"].append(skill)

    def _calculate_frequency(self, text: str, skills: Dict) -> Dict[str, int]:
        """Calculate how often each skill appears"""
        text_lower = text.lower()
        freq = Counter()
        all_skills = [s for cat in skills.values() for s in cat]
        for skill in all_skills:
            count = len(re.findall(r"\b" + re.escape(skill.lower()) + r"\b", text_lower))
            if count > 0:
                freq[skill] = count
        return dict(freq)

    def _get_top_skills(self, freq: Dict, n: int) -> List[Tuple[str, int]]:
        """Get top N skills by frequency"""
        return Counter(freq).most_common(n)

    def extract_experience_years(self, text: str) -> Dict:
        """Extract years of experience from text"""
        patterns = [
            r"(\d+)\+?\s*years?\s*(?:of\s*)?experience",
            r"experience\s*:?\s*(\d+)\+?\s*years?",
            r"(\d+)\+?\s*years?\s*(?:in\s*|of\s*)?(?:the\s*)?(?:industry|field)"
        ]
        years = []
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            years.extend([int(m) for m in matches if int(m) < 50])

        if years:
            return {"total_years": max(years), "mentions": years, "has_experience": True}
        return {"total_years": 0, "mentions": [], "has_experience": False}

    def extract_education(self, text: str) -> Dict:
        """Extract education information"""
        education_patterns = {
            "phd": r"(?i)(ph\.d\.|phd|doctorate|doctoral)",
            "masters": r"(?i)(master|m\.tech|m\.e\.|m\.s\.|mba)",
            "bachelors": r"(?i)(bachelor|b\.tech|b\.e\.|b\.s\.|b\.a\.)"
        }
        degrees = []
        for degree, pattern in education_patterns.items():
            if re.search(pattern, text):
                degrees.append(degree)

        field_pattern = r"(?i)(?:in|of)\s+([\w\s]+?)(?:\s+from|\s+at|\s*[,;]|\s*\n|$)"
        fields = re.findall(field_pattern, text)

        return {
            "highest_degree": degrees[0] if degrees else "unknown",
            "all_degrees": degrees,
            "field_of_study": [f.strip() for f in fields[:3]],
            "has_education": len(degrees) > 0
        }
