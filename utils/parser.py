"""
Resume Parser Module
Extracts text from PDF, DOCX, TXT, and RTF files
"""
import os
import re
from typing import Dict, Optional
import PyPDF2
import pdfplumber
from docx import Document


class ResumeParser:
    """Parse resumes from various file formats"""

    def __init__(self):
        self.supported_formats = [".pdf", ".docx", ".txt", ".rtf"]

    def parse(self, file_path: str) -> Dict:
        """Parse a resume file and return structured data"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        ext = os.path.splitext(file_path)[1].lower()

        if ext not in self.supported_formats:
            raise ValueError(f"Unsupported format: {ext}. Supported: {self.supported_formats}")

        # Extract raw text
        if ext == ".pdf":
            raw_text = self._parse_pdf(file_path)
        elif ext == ".docx":
            raw_text = self._parse_docx(file_path)
        elif ext in [".txt", ".rtf"]:
            raw_text = self._parse_text(file_path)
        else:
            raw_text = ""

        # Clean and structure the text
        cleaned_text = self._clean_text(raw_text)
        sections = self._extract_sections(cleaned_text)

        return {
            "file_name": os.path.basename(file_path),
            "file_path": file_path,
            "file_type": ext,
            "raw_text": raw_text,
            "cleaned_text": cleaned_text,
            "sections": sections,
            "word_count": len(cleaned_text.split()),
            "char_count": len(cleaned_text)
        }

    def _parse_pdf(self, file_path: str) -> str:
        """Extract text from PDF using multiple methods"""
        text = ""

        # Try pdfplumber first (better formatting)
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception:
            pass

        # Fallback to PyPDF2
        if not text.strip():
            try:
                with open(file_path, "rb") as f:
                    reader = PyPDF2.PdfReader(f)
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                print(f"Error parsing PDF: {e}")

        return text

    def _parse_docx(self, file_path: str) -> str:
        """Extract text from DOCX"""
        try:
            doc = Document(file_path)
            text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            return text
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            return ""

    def _parse_text(self, file_path: str) -> str:
        """Extract text from TXT/RTF"""
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        except Exception as e:
            print(f"Error parsing text file: {e}")
            return ""

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r"\s+", " ", text)
        # Remove special characters but keep useful ones
        text = re.sub(r"[^\w\s@.,;:#$%&*()_+-=\[\]{}|\"'<>?/]", "", text)
        # Normalize newlines
        text = re.sub(r"\n\s*\n", "\n", text)
        return text.strip()

    def _extract_sections(self, text: str) -> Dict:
        """Extract common resume sections"""
        sections = {
            "contact_info": "",
            "summary": "",
            "experience": "",
            "education": "",
            "skills": "",
            "projects": "",
            "certifications": ""
        }

        # Common section headers
        section_patterns = {
            "contact_info": r"(?i)(contact|personal info|profile)",
            "summary": r"(?i)(summary|objective|about me|professional summary)",
            "experience": r"(?i)(experience|work experience|employment|professional experience|career history)",
            "education": r"(?i)(education|academic|qualification|degree)",
            "skills": r"(?i)(skills|technical skills|core competencies|expertise)",
            "projects": r"(?i)(projects|personal projects|academic projects)",
            "certifications": r"(?i)(certifications|certificates|accreditations)"
        }

        lines = text.split("\n")
        current_section = "contact_info"

        for line in lines:
            line_stripped = line.strip().lower()

            # Check if line is a section header
            for section, pattern in section_patterns.items():
                if re.search(pattern, line_stripped) and len(line_stripped) < 50:
                    current_section = section
                    break
            else:
                sections[current_section] += line + "\n"

        return {k: v.strip() for k, v in sections.items()}

    def get_file_stats(self, file_path: str) -> Dict:
        """Get file statistics"""
        stats = os.stat(file_path)
        return {
            "size_bytes": stats.st_size,
            "size_kb": round(stats.st_size / 1024, 2),
            "modified": stats.st_mtime
        }
