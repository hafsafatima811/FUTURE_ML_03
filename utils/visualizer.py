"""
Visualizer Module
Generates charts and visualizations for resume analysis
"""
import json
import base64
from io import BytesIO
from typing import Dict, List
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import numpy as np


class Visualizer:
    """Generate visualizations for resume screening results"""

    def __init__(self):
        plt.style.use("seaborn-v0_8-whitegrid")
        self.colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A", "#19D3F3"]

    def _fig_to_base64(self, fig) -> str:
        """Convert matplotlib figure to base64 string"""
        buf = BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", dpi=100)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode("utf-8")
        plt.close(fig)
        return img_base64

    def create_radar_chart(self, scores: Dict, title: str = "Match Score Breakdown") -> str:
        """Create radar chart for match scores"""
        categories = list(scores.keys())
        values = list(scores.values())

        # Close the radar chart
        values += values[:1]
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        ax.fill(angles, values, color="#636EFA", alpha=0.25)
        ax.plot(angles, values, color="#636EFA", linewidth=2, marker="o")

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([c.replace("_", " ").title() for c in categories], size=10)
        ax.set_ylim(0, 100)
        ax.set_title(title, size=14, fontweight="bold", pad=20)
        ax.grid(True)

        return self._fig_to_base64(fig)

    def create_bar_chart(self, data: Dict, title: str = "Scores", horizontal: bool = False) -> str:
        """Create bar chart"""
        labels = list(data.keys())
        values = list(data.values())

        fig, ax = plt.subplots(figsize=(10, 6))

        if horizontal:
            bars = ax.barh(labels, values, color=self.colors[:len(labels)])
            ax.set_xlim(0, 100)
        else:
            bars = ax.bar(labels, values, color=self.colors[:len(labels)])
            ax.set_ylim(0, 100)

        # Add value labels on bars
        for bar in bars:
            if horizontal:
                width = bar.get_width()
                ax.text(width + 1, bar.get_y() + bar.get_height()/2, 
                       f"{width:.1f}", ha="left", va="center", fontweight="bold")
            else:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                       f"{height:.1f}", ha="center", va="bottom", fontweight="bold")

        ax.set_title(title, size=14, fontweight="bold")
        if horizontal:
            ax.set_xlabel("Score", fontsize=12)
        else:
            ax.set_ylabel("Score", fontsize=12)

        plt.tight_layout()
        return self._fig_to_base64(fig)

    def create_skills_comparison(self, resume_skills: List[str], job_skills: List[str]) -> str:
        """Create skills comparison chart"""
        matched = []
        missing = []

        resume_lower = [s.lower() for s in resume_skills]
        for skill in job_skills:
            if any(skill.lower() in rs or rs in skill.lower() for rs in resume_lower):
                matched.append(skill)
            else:
                missing.append(skill)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # Matched skills
        if matched:
            ax1.barh(range(len(matched)), [100]*len(matched), color="#00CC96")
            ax1.set_yticks(range(len(matched)))
            ax1.set_yticklabels(matched, fontsize=10)
            ax1.set_xlim(0, 100)
            ax1.set_title(f"Matched Skills ({len(matched)})", fontweight="bold", color="#00CC96")
            ax1.set_xlabel("Match %")
        else:
            ax1.text(0.5, 0.5, "No matched skills", ha="center", va="center", transform=ax1.transAxes)
            ax1.set_title("Matched Skills (0)", fontweight="bold")

        # Missing skills
        if missing:
            ax2.barh(range(len(missing)), [100]*len(missing), color="#EF553B")
            ax2.set_yticks(range(len(missing)))
            ax2.set_yticklabels(missing, fontsize=10)
            ax2.set_xlim(0, 100)
            ax2.set_title(f"Missing Skills ({len(missing)})", fontweight="bold", color="#EF553B")
            ax2.set_xlabel("Gap %")
        else:
            ax2.text(0.5, 0.5, "No missing skills!", ha="center", va="center", transform=ax2.transAxes)
            ax2.set_title("Missing Skills (0)", fontweight="bold")

        plt.tight_layout()
        return self._fig_to_base64(fig)

    def create_wordcloud(self, text: str, title: str = "Resume Word Cloud") -> str:
        """Create word cloud from resume text"""
        fig, ax = plt.subplots(figsize=(12, 8))

        wordcloud = WordCloud(
            width=800, height=500,
            background_color="white",
            colormap="viridis",
            max_words=100,
            relative_scaling=0.5,
            min_font_size=10
        ).generate(text)

        ax.imshow(wordcloud, interpolation="bilinear")
        ax.axis("off")
        ax.set_title(title, size=16, fontweight="bold", pad=20)

        plt.tight_layout()
        return self._fig_to_base64(fig)

    def create_ranking_chart(self, candidates: List[Dict]) -> str:
        """Create candidate ranking horizontal bar chart"""
        names = [c["candidate"]["file_name"][:20] for c in candidates]
        scores = [c["match_result"]["total_score"] for c in candidates]

        fig, ax = plt.subplots(figsize=(10, max(6, len(candidates) * 0.8)))

        colors = ["#00CC96" if s >= 70 else "#FFA15A" if s >= 50 else "#EF553B" for s in scores]
        bars = ax.barh(range(len(names)), scores, color=colors)

        ax.set_yticks(range(len(names)))
        ax.set_yticklabels(names, fontsize=10)
        ax.set_xlim(0, 100)
        ax.invert_yaxis()
        ax.set_xlabel("Match Score (%)", fontsize=12)
        ax.set_title("Candidate Ranking", size=14, fontweight="bold")

        # Add score labels
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax.text(score + 1, i, f"{score:.1f}", va="center", fontweight="bold")

        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor="#00CC96", label="Excellent (≥70%)"),
            Patch(facecolor="#FFA15A", label="Good (50-69%)"),
            Patch(facecolor="#EF553B", label="Needs Improvement (<50%)")
        ]
        ax.legend(handles=legend_elements, loc="lower right")

        plt.tight_layout()
        return self._fig_to_base64(fig)

    def create_quality_gauge(self, score: float, title: str = "Quality Score") -> str:
        """Create gauge chart for quality score"""
        fig, ax = plt.subplots(figsize=(8, 5))

        # Create gauge
        theta = np.linspace(0, np.pi, 100)
        r = 1.0

        # Background arc
        ax.fill_between(np.cos(theta), np.sin(theta), 0, alpha=0.1, color="gray")

        # Color zones
        zone_colors = ["#EF553B", "#FFA15A", "#00CC96"]
        zone_ranges = [(0, 50), (50, 75), (75, 100)]

        for (start, end), color in zip(zone_ranges, zone_colors):
            start_angle = np.pi * (1 - start/100)
            end_angle = np.pi * (1 - end/100)
            theta_zone = np.linspace(end_angle, start_angle, 30)
            ax.fill_between(np.cos(theta_zone), np.sin(theta_zone), 0, alpha=0.3, color=color)

        # Needle
        needle_angle = np.pi * (1 - score/100)
        ax.annotate("", xy=(np.cos(needle_angle) * 0.9, np.sin(needle_angle) * 0.9),
                   xytext=(0, 0),
                   arrowprops=dict(arrowstyle="->", color="black", lw=3))

        # Score text
        ax.text(0, -0.3, f"{score:.1f}", ha="center", va="center", 
               fontsize=36, fontweight="bold")
        ax.text(0, -0.6, title, ha="center", va="center", fontsize=14)

        ax.set_xlim(-1.2, 1.2)
        ax.set_ylim(-0.8, 1.2)
        ax.set_aspect("equal")
        ax.axis("off")

        plt.tight_layout()
        return self._fig_to_base64(fig)

    def create_comparison_radar(self, candidates: List[Dict], job_skills: List[str]) -> str:
        """Create radar chart comparing multiple candidates"""
        if len(candidates) > 5:
            candidates = candidates[:5]

        categories = ["Skills", "Experience", "Education", "Semantic", "Quality"]

        fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
        angles += angles[:1]

        for i, candidate in enumerate(candidates):
            breakdown = candidate["match_result"]["breakdown"]
            values = [
                breakdown["skills_match"],
                breakdown["experience_match"],
                breakdown["education_match"],
                breakdown["semantic_similarity"],
                breakdown["resume_quality"]
            ]
            values += values[:1]

            ax.plot(angles, values, "o-", linewidth=2, 
                   label=candidate["candidate"]["file_name"][:15],
                   color=self.colors[i % len(self.colors)])
            ax.fill(angles, values, alpha=0.1, color=self.colors[i % len(self.colors)])

        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, size=11)
        ax.set_ylim(0, 100)
        ax.set_title("Candidate Comparison", size=14, fontweight="bold", pad=20)
        ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
        ax.grid(True)

        plt.tight_layout()
        return self._fig_to_base64(fig)
