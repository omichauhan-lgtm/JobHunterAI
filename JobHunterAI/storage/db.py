import json
from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, ForeignKey, Text, DateTime, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import datetime
from config import DB_PATH

Base = declarative_base()

# Many-to-many relationship helper for graph links
class RelationshipTable(Base):
    __tablename__ = 'relationships'
    id = Column(Integer, primary_key=True)
    source_type = Column(String(50), nullable=False) # e.g. 'Skill', 'Project', 'Evidence'
    source_id = Column(Integer, nullable=False)
    target_type = Column(String(50), nullable=False) # e.g. 'Project', 'Experience', 'Application'
    target_id = Column(Integer, nullable=False)
    rel_type = Column(String(50), nullable=False) # e.g. 'uses_skill', 'demonstrated_by', 'referenced_in'

class CandidateTable(Base):
    __tablename__ = 'candidates'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(50))
    github = Column(String(150))
    linkedin = Column(String(150))
    website = Column(String(150))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    experiences = relationship("ExperienceTable", back_populates="candidate", cascade="all, delete-orphan")
    projects = relationship("ProjectTable", back_populates="candidate", cascade="all, delete-orphan")
    skills = relationship("SkillTable", back_populates="candidate", cascade="all, delete-orphan")
    star_stories = relationship("STARStoryTable", back_populates="candidate", cascade="all, delete-orphan")
    resumes = relationship("ResumeVariantTable", back_populates="candidate", cascade="all, delete-orphan")
    applications = relationship("ApplicationTable", back_populates="candidate", cascade="all, delete-orphan")

class ExperienceTable(Base):
    __tablename__ = 'experiences'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    company = Column(String(100), nullable=False)
    role = Column(String(100), nullable=False)
    org_type = Column(String(100)) # e.g. YC-backed startup
    is_open_source = Column(Boolean, default=False)
    start_date = Column(String(50))
    end_date = Column(String(50))
    bullets_json = Column(Text, nullable=False) # JSON list of bullets
    skills_json = Column(Text, default="[]") # JSON list of skills utilized
    
    candidate = relationship("CandidateTable", back_populates="experiences")
    evidence = relationship("EvidenceTable", back_populates="experience", cascade="all, delete-orphan")

class ProjectTable(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(100)) # e.g. Backend
    description_json = Column(Text, nullable=False) # JSON list of bullets
    skills_json = Column(Text, default="[]") # JSON list of skills
    github_url = Column(String(200))
    
    candidate = relationship("CandidateTable", back_populates="projects")
    evidence = relationship("EvidenceTable", back_populates="project", cascade="all, delete-orphan")

class SkillTable(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    name = Column(String(100), nullable=False)
    category = Column(String(100)) # e.g. Languages
    
    candidate = relationship("CandidateTable", back_populates="skills")

class EvidenceTable(Base):
    __tablename__ = 'evidence'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    experience_id = Column(Integer, ForeignKey('experiences.id'), nullable=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    type = Column(String(50), nullable=False) # e.g. PR, Commit, Issue
    description = Column(Text, nullable=False)
    url = Column(String(250))
    metrics = Column(String(250)) # e.g. 15ms latency improvement
    
    experience = relationship("ExperienceTable", back_populates="evidence")
    project = relationship("ProjectTable", back_populates="evidence")

class STARStoryTable(Base):
    __tablename__ = 'star_stories'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    project_or_company = Column(String(150), nullable=False)
    situation = Column(Text, nullable=False)
    task = Column(Text, nullable=False)
    action = Column(Text, nullable=False)
    result = Column(Text, nullable=False)
    
    candidate = relationship("CandidateTable", back_populates="star_stories")

class JobOpportunityTable(Base):
    __tablename__ = 'job_opportunities'
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    company_name = Column(String(100), nullable=False)
    jd_text = Column(Text, nullable=False)
    url = Column(String(300))
    source = Column(String(100), nullable=False) # e.g. Greenhouse
    salary_range = Column(String(100))
    remote_status = Column(String(50), default="Remote")
    tech_stack_json = Column(Text, default="[]") # JSON list
    requirements_json = Column(Text, default="[]") # JSON list
    ats_keywords_json = Column(Text, default="[]") # JSON list
    overall_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    status = Column(String(50), default="discovered") # discovered, processing, applied, rejected

    applications = relationship("ApplicationTable", back_populates="job")

class ResumeVariantTable(Base):
    __tablename__ = 'resume_variants'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    version = Column(Integer, nullable=False)
    resume_type = Column(String(50), default="backend") # backend, frontend
    latex_source = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    candidate = relationship("CandidateTable", back_populates="resumes")
    applications = relationship("ApplicationTable", back_populates="resume_variant")

class ApplicationTable(Base):
    __tablename__ = 'applications'
    id = Column(Integer, primary_key=True)
    candidate_id = Column(Integer, ForeignKey('candidates.id'), nullable=False)
    job_id = Column(Integer, ForeignKey('job_opportunities.id'), nullable=False)
    resume_variant_id = Column(Integer, ForeignKey('resume_variants.id'), nullable=True)
    cover_letter_path = Column(String(300))
    outreach_sequence_path = Column(String(300))
    status = Column(String(50), default="Applied") # Applied, OA, Interview, Rejected, Offer
    experiment_group = Column(String(50), default="A") # A/B testing group
    date_applied = Column(DateTime, default=datetime.datetime.utcnow)
    outcomes_log = Column(Text) # Notes/Logs for interview feedback
    compensation_details = Column(Text) # JSON structure for offer details if status == 'Offer'
    
    candidate = relationship("CandidateTable", back_populates="applications")
    job = relationship("JobOpportunityTable", back_populates="applications")
    resume_variant = relationship("ResumeVariantTable", back_populates="applications")
    recruiters = relationship("RecruiterCRMTable", back_populates="application")

class RecruiterCRMTable(Base):
    __tablename__ = 'recruiter_crm'
    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey('applications.id'), nullable=False)
    name = Column(String(100), nullable=False)
    title = Column(String(100)) # e.g. Technical Recruiter
    contact_info = Column(String(150)) # e.g. email or linkedin url
    message_history_json = Column(Text, default="[]") # JSON list of messages
    last_interacted = Column(DateTime, default=datetime.datetime.utcnow)

    application = relationship("ApplicationTable", back_populates="recruiters")

# Database initialization helper
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
