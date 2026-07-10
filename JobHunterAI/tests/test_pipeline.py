import json
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from storage.db import Base, CandidateTable, ExperienceTable, ProjectTable, SkillTable, JobOpportunityTable
from storage.crud import import_master_profile, get_candidate_profile_data
from models.schemas import MasterProfile, Experience, Project, Skill, Evidence, STARStory
from engines.ranking import compute_job_score, rank_projects
from engines.critic import run_truth_validation
from engines.ats import calculate_ats_score

class TestJobHunterAI(unittest.TestCase):
    def setUp(self):
        # Setup an in-memory SQLite database for testing
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = self.SessionLocal()

    def tearDown(self):
        self.db.close()
        Base.metadata.drop_all(bind=self.engine)

    def test_database_seeding_and_retrieval(self):
        """Test that the candidate database seeds correctly and recovers graph records."""
        profile = MasterProfile(
            name="Test Dev",
            email="test@test.com",
            github="github.com/test",
            linkedin="linkedin.com/test",
            skills=[Skill(name="Python", category="Languages")],
            experiences=[
                Experience(
                    company="ADEN",
                    role="Open Source Contributor",
                    org_type="YC-backed startup",
                    is_open_source=True,
                    skills=["Python"],
                    bullets=["Contributed engineering improvements."],
                    evidence=[Evidence(type="PR", description="PR #123")]
                )
            ],
            projects=[
                Project(
                    name="Project A",
                    category="Backend",
                    skills=["Python"],
                    description_bullets=["Built gateway."],
                    evidence=[]
                )
            ]
        )
        
        import_master_profile(self.db, profile)
        
        # Retrieve
        retrieved = get_candidate_profile_data(self.db, candidate_id=1)
        
        self.assertEqual(retrieved["name"], "Test Dev")
        self.assertEqual(retrieved["email"], "test@test.com")
        self.assertEqual(len(retrieved["experiences"]), 1)
        self.assertEqual(retrieved["experiences"][0]["company"], "ADEN")
        self.assertEqual(retrieved["experiences"][0]["is_open_source"], True)
        self.assertEqual(len(retrieved["experiences"][0]["evidence"]), 1)
        self.assertEqual(retrieved["experiences"][0]["evidence"][0]["description"], "PR #123")

    def test_deterministic_scoring(self):
        """Verify job scoring handles skill matching and YC preference correctly."""
        skills = ["Python", "FastAPI", "Docker"]
        jd = "Seeking a Backend developer proficient in Python, FastAPI, and Kubernetes."
        
        score = compute_job_score(
            job_jd=jd,
            job_title="Software Engineer",
            company_yc=False,
            remote_status="Onsite",
            candidate_skills=skills
        )
        
        self.assertAlmostEqual(score, 45.0, places=1)

    def test_ats_matching(self):
        """Verify ATS percentage scoring evaluates intersection cleanly."""
        bullets = [
            "Implemented caching inside FastAPI backend routing system.",
            "Built deployment configurations using Docker."
        ]
        keywords = ["FastAPI", "Docker", "PostgreSQL", "React"]
        
        score = calculate_ats_score(bullets, keywords)
        self.assertEqual(score, 50.0)

    def test_programmatic_rule_engine(self):
        """Enforce that the critic rules block resumes altering ADEN contributor role or dates."""
        profile = MasterProfile(
            name="Omi",
            email="omi@test.com",
            github="github.com/omi",
            linkedin="linkedin.com/omi",
            skills=[],
            experiences=[
                Experience(
                    company="ADEN",
                    role="Open Source Contributor",
                    org_type="YC Startup",
                    is_open_source=True,
                    skills=[],
                    bullets=["Contributed improvements."],
                    evidence=[Evidence(type="PR", description="PR #123")]
                )
            ],
            projects=[]
        )
        
        import_master_profile(self.db, profile)
        db_profile = get_candidate_profile_data(self.db, candidate_id=1)
        
        # 1. Invalid Case: Altered Role for ADEN
        invalid_gen_data = {
            "experiences": [
                {
                    "company": "ADEN",
                    "role": "Lead Software Engineer", # Violates ADEN Open Source role constraint!
                    "org_type": "YC Startup",
                    "bullets": ["Lead engineering core in Commit a1b2c3."]
                }
            ],
            "projects": []
        }
        
        report = run_truth_validation(invalid_gen_data, db_profile)
        self.assertEqual(report["passed"], False)
        self.assertTrue(any("ADEN Rule Violation" in err for err in report["errors"]))
        
        # 2. Invalid Case: Evidence Grounding Violation (untraceable PR)
        grounding_invalid_data = {
            "experiences": [
                {
                    "company": "ADEN",
                    "role": "Open Source Contributor",
                    "org_type": "YC Startup",
                    "bullets": ["Contributed engineering improvements to open source gateway in PR #999."]
                }
            ],
            "projects": []
        }
        
        report_grounding = run_truth_validation(grounding_invalid_data, db_profile)
        self.assertEqual(report_grounding["passed"], False)
        self.assertTrue(any("Evidence Grounding Violation" in err for err in report_grounding["errors"]))

        # 3. Valid Case: Kept Role and Evidence intact
        valid_gen_data = {
            "experiences": [
                {
                    "company": "ADEN",
                    "role": "Open Source Contributor",
                    "org_type": "YC Startup",
                    "bullets": ["Contributed engineering improvements to open source gateway in PR #123."]
                }
            ],
            "projects": []
        }
        
        valid_report = run_truth_validation(valid_gen_data, db_profile)
        self.assertEqual(valid_report["passed"], True)

if __name__ == "__main__":
    unittest.main()
