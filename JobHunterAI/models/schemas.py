from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Skill(BaseModel):
    name: str
    category: str = Field(description="e.g., Languages, Frameworks, Developer Tools, Databases")

class Evidence(BaseModel):
    type: str = Field(description="e.g., PR, Commit, Issue, Doc, Deploy")
    description: str
    url: Optional[str] = None
    metrics: Optional[str] = None

class Project(BaseModel):
    name: str
    category: str = Field(description="e.g., Backend, Frontend, AI/ML, Data Engineering")
    skills: List[str]
    description_bullets: List[str]
    github_url: Optional[str] = None
    evidence: List[Evidence] = Field(default_factory=list)

class Experience(BaseModel):
    company: str
    role: str
    org_type: str = Field(description="e.g., YC-backed startup, Enterprise, Open Source Organization")
    is_open_source: bool = False
    skills: List[str]
    bullets: List[str]
    evidence: List[Evidence] = Field(default_factory=list)

class STARStory(BaseModel):
    situation: str
    task: str
    action: str
    result: str
    project_or_company: str

class MasterProfile(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    github: str
    linkedin: str
    website: Optional[str] = None
    experiences: List[Experience]
    projects: List[Project]
    skills: List[Skill]
    star_stories: List[STARStory] = Field(default_factory=list)

class JobIntelligence(BaseModel):
    company_name: str
    industry: str
    tech_stack: List[str]
    ats_keywords: List[str]
    recent_news: Optional[str] = None
    hiring_manager_persona: Optional[str] = None

class CompanyProfile(BaseModel):
    name: str
    funding_stage: str
    funding_amount: Optional[str] = None
    investors: List[str]
    is_yc: bool = False
    tech_stack: List[str]
    recent_news: Optional[str] = None
    products: List[str] = Field(default_factory=list)

class JobOpportunity(BaseModel):
    title: str
    company_name: str
    jd_text: str
    url: Optional[str] = None
    source: str = Field(description="e.g., Greenhouse, Lever, Ashby, YC Jobs")
    salary_range: Optional[str] = None
    remote_status: str = Field(description="e.g., Remote, Hybrid, Onsite")
    tech_stack: List[str] = Field(default_factory=list)
    requirements: List[str] = Field(default_factory=list)
    overall_score: float = 0.0

class TailoredApplication(BaseModel):
    selected_projects: List[Project]
    tailored_bullets: Dict[str, List[str]] = Field(description="Mapping of company/project name to tailored bullets")
    cover_letter_text: str
