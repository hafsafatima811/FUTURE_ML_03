"""
CLI Entry Point for Resume Screening System
"""
import os
import sys
import argparse
import json
from datetime import datetime

from utils.parser import ResumeParser
from utils.extractor import SkillExtractor
from utils.matcher import ResumeJobMatcher
from utils.analyzer import ResumeQualityAnalyzer
from utils.visualizer import Visualizer


def process_resume(file_path: str, job_desc: str, job_skills: list):
    """Process a single resume"""
    # Parse resume
    parser = ResumeParser()
    resume_data = parser.parse(file_path)

    # Extract skills
    extractor = SkillExtractor()
    skills_data = extractor.extract_skills(resume_data["cleaned_text"])
    resume_data["extracted_skills"] = skills_data

    # Extract experience
    exp_data = extractor.extract_experience_years(resume_data["cleaned_text"])
    resume_data["experience"] = exp_data

    # Extract education
    edu_data = extractor.extract_education(resume_data["cleaned_text"])
    resume_data["education"] = edu_data

    # Calculate match
    matcher = ResumeJobMatcher()
    match_result = matcher.calculate_match_score(resume_data, job_desc, job_skills)

    # Analyze quality
    analyzer = ResumeQualityAnalyzer()
    quality_analysis = analyzer.analyze(resume_data)

    return {
        "resume_data": resume_data,
        "match_result": match_result,
        "quality_analysis": quality_analysis
    }


def print_results(results: dict):
    """Print formatted results to console"""
    print("\n" + "=" * 70)
    print(f"📄 RESUME ANALYSIS: {results['resume_data']['file_name']}")
    print("=" * 70)

    # Match Score
    match = results["match_result"]
    print(f"\n🎯 OVERALL MATCH SCORE: {match['total_score']}/100")
    print(f"   Level: {match['match_level']}")
    print(f"   Recommendation: {match['recommendation']}")

    print("\n📊 Score Breakdown:")
    for category, score in match["breakdown"].items():
        bar = "█" * int(score / 5) + "░" * (20 - int(score / 5))
        print(f"   {category.replace('_', ' ').title():20s} | {bar} | {score:.1f}%")

    # Skills
    skills = results["resume_data"]["extracted_skills"]
    print(f"\n💡 Extracted Skills ({skills['skill_count']} total):")
    for category, skill_list in skills["skills_by_category"].items():
        if skill_list:
            print(f"   {category.title()}: {', '.join(skill_list[:10])}")

    # Skill Gaps
    if match["skill_gaps"]:
        print(f"\n⚠️  Skill Gaps ({len(match['skill_gaps'])}):")
        for gap in match["skill_gaps"][:5]:
            print(f"   • {gap['skill']} ({gap['importance']})")

    # Strengths
    if match["strengths"]:
        print(f"\n✨ Strengths:")
        for strength in match["strengths"]:
            print(f"   • {strength}")

    # Quality Analysis
    quality = results["quality_analysis"]
    print(f"\n📈 Resume Quality Score: {quality['overall_score']}/100")
    print(f"   ATS Score: {quality['ats_score']}/100")
    print(f"   Formatting: {quality['formatting_score']}/100")
    print(f"   Content: {quality['content_score']}/100")

    # Suggestions
    if quality["suggestions"]:
        print(f"\n💡 Improvement Suggestions:")
        for sugg in quality["suggestions"][:5]:
            priority_icon = "🔴" if sugg["priority"] == "high" else "🟡" if sugg["priority"] == "medium" else "🟢"
            print(f"   {priority_icon} [{sugg['category']}] {sugg['message']}")

    print("\n" + "=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="AI Resume Screening System - CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --resume "john_doe.pdf" --job "job_desc.txt"
  python main.py --batch "resumes/" --job "job_desc.txt" --output results.json
  python main.py --resume "resume.pdf" --job-desc "Looking for Python developer"
        """
    )

    parser.add_argument("--resume", type=str, help="Path to resume file (PDF/DOCX/TXT)")
    parser.add_argument("--job", type=str, help="Path to job description file")
    parser.add_argument("--job-desc", type=str, help="Job description text (inline)")
    parser.add_argument("--job-skills", type=str, help="Comma-separated required skills")
    parser.add_argument("--batch", type=str, help="Directory containing multiple resumes")
    parser.add_argument("--output", type=str, default="screening_results.json", help="Output file path")
    parser.add_argument("--compare", nargs="+", help="Compare multiple resumes")

    args = parser.parse_args()

    # Get job description
    job_desc = ""
    if args.job:
        with open(args.job, "r", encoding="utf-8") as f:
            job_desc = f.read()
    elif args.job_desc:
        job_desc = args.job_desc
    else:
        job_desc = "Looking for a skilled software engineer with experience in Python, machine learning, and cloud technologies."

    # Get job skills
    job_skills = []
    if args.job_skills:
        job_skills = [s.strip() for s in args.job_skills.split(",")]
    else:
        # Extract skills from job description
        extractor = SkillExtractor()
        skills_data = extractor.extract_skills(job_desc)
        job_skills = skills_data["all_skills"]

    # Process single resume
    if args.resume:
        print(f"\n🔄 Processing: {args.resume}")
        results = process_resume(args.resume, job_desc, job_skills)
        print_results(results)

        # Save results
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n💾 Results saved to: {args.output}")

    # Batch processing
    elif args.batch:
        print(f"\n🔄 Batch processing directory: {args.batch}")

        supported_exts = (".pdf", ".docx", ".txt", ".rtf")
        resume_files = [
            os.path.join(args.batch, f) 
            for f in os.listdir(args.batch)
            if f.lower().endswith(supported_exts)
        ]

        print(f"Found {len(resume_files)} resume(s)")

        all_results = []
        matcher = ResumeJobMatcher()

        for file_path in resume_files:
            try:
                print(f"  Processing: {os.path.basename(file_path)}...", end=" ")
                result = process_resume(file_path, job_desc, job_skills)
                all_results.append(result)
                print(f"✅ Score: {result['match_result']['total_score']:.1f}")
            except Exception as e:
                print(f"❌ Error: {e}")

        # Rank candidates
        candidates = [r["resume_data"] for r in all_results]
        ranked = matcher.rank_candidates(candidates, job_desc, job_skills)

        print("\n" + "=" * 70)
        print("📊 RANKING RESULTS")
        print("=" * 70)

        for item in ranked:
            print(f"\n  #{item['rank']} {item['candidate']['file_name']}")
            print(f"     Score: {item['match_result']['total_score']:.1f}% | "
                  f"{item['match_result']['match_level']}")

        # Save batch results
        batch_output = {
            "timestamp": datetime.now().isoformat(),
            "job_description": job_desc,
            "total_processed": len(all_results),
            "rankings": [
                {
                    "rank": item["rank"],
                    "file_name": item["candidate"]["file_name"],
                    "score": item["match_result"]["total_score"],
                    "match_level": item["match_result"]["match_level"]
                }
                for item in ranked
            ],
            "detailed_results": all_results
        }

        with open(args.output, "w") as f:
            json.dump(batch_output, f, indent=2, default=str)
        print(f"\n💾 Batch results saved to: {args.output}")

    # Compare mode
    elif args.compare:
        print(f"\n🔄 Comparing {len(args.compare)} resumes")

        all_results = []
        for file_path in args.compare:
            try:
                result = process_resume(file_path, job_desc, job_skills)
                all_results.append(result)
            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")

        # Print comparison table
        print("\n" + "=" * 90)
        print(f"{'Candidate':<25} {'Score':<10} {'Skills':<10} {'Exp':<8} {'Level':<20}")
        print("=" * 90)

        for result in sorted(all_results, 
                           key=lambda x: x["match_result"]["total_score"], 
                           reverse=True):
            r = result["resume_data"]
            m = result["match_result"]
            print(f"{r['file_name']:<25} {m['total_score']:<10.1f} "
                  f"{r['extracted_skills']['skill_count']:<10} "
                  f"{r['experience']['total_years']:<8} "
                  f"{m['match_level']:<20}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
