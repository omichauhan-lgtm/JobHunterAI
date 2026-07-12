import sys
import argparse
from storage.db import SessionLocal, init_db
from engines.discovery import discover_job_from_url, run_mock_discovery
from orchestrator import run_application_pipeline, run_daily_autonomous_loop
from config import logger

def main():
    parser = argparse.ArgumentParser(description="JobHunterAI Command Line Interface")
    parser.add_argument("--discover", action="store_true", help="Run job discovery to find new openings")
    parser.add_argument("--url", type=str, help="Ingest a specific Lever or Greenhouse Job URL")
    parser.add_argument("--apply-job", type=int, help="Run the tailored application pipeline for a Job ID")
    parser.add_argument("--daily-loop", action="store_true", help="Run the daily autonomous career pipeline")
    parser.add_argument("--init-db", action="store_true", help="Initialize database tables")

    args = parser.parse_args()
    
    db = SessionLocal()
    try:
        if args.init_db:
            print("Initializing database...")
            init_db()
            print("Done.")
            return

        if args.daily_loop:
            print("Starting Daily Autonomous Career Agent Loop...")
            res = run_daily_autonomous_loop(db)
            print("\n=== DAILY LOOP COMPLETE ===")
            print(f"Opportunities Processed: {res['processed']}")
            print(f"Matches Tailored: {res['matched']}")
            print(f"Briefing Sent: {res['briefing_sent']}")
            return

        if args.discover:

            print("Running job discovery engine...")
            jobs = run_mock_discovery(db)
            print(f"Discovered {len(jobs)} new opportunities:")
            for j in jobs:
                print(f"- [{j.id}] {j.title} at {j.company_name} (Source: {j.source}, Score: {j.overall_score})")
            return
            
        if args.url:
            print(f"Ingesting job from URL: {args.url}...")
            job = discover_job_from_url(db, args.url)
            if job:
                print(f"Successfully ingested [{job.id}] {job.title} at {job.company_name}!")
            else:
                print(f"Failed to ingest job details. Ensure the URL is an active, public Greenhouse or Lever job posting.")
            return

        if args.apply_job:
            print(f"Starting pipeline for Job ID: {args.apply_job}...")
            res = run_application_pipeline(db, args.apply_job)
            if res["success"]:
                print("\n=== PIPELINE SUCCESS ===")
                print(f"Tailored Resume: {res['resume_path']}")
                print(f"Cover Letter: {res['cover_letter_path']}")
                print(f"Outreach draft: {res['outreach_path']}")
                print(f"Explainability Report: {res['explainability_path']}")
                if res["critic_warnings"]:
                    print("\nWarnings:")
                    for w in res["critic_warnings"]:
                        print(f"- {w}")
            else:
                print(f"\nPipeline failed: {res.get('error')}")
                if "report" in res:
                    print("Critic report errors:")
                    for err in res["report"]["errors"]:
                        print(f"- {err}")
            return

        parser.print_help()
    finally:
        db.close()

if __name__ == "__main__":
    main()
