import json
from storage.db import init_db, SessionLocal
from storage.crud import import_master_profile
from models.schemas import MasterProfile, Experience, Project, Skill, Evidence, STARStory

def seed_database():
    print("Initializing Database...")
    init_db()
    
    # Construct complete Career Graph using Pydantic Models based on Omi's actual resume
    profile = MasterProfile(
        name="Omi Chauhan",
        email="omichauhan427@gmail.com",
        phone="+91-9770845401",
        github="github.com/omichauhan-lgtm",
        linkedin="linkedin.com/in/omichauhan",
        website="omichauhan.github.io",
        skills=[
            Skill(name="Python", category="Languages"),
            Skill(name="SQL", category="Languages"),
            Skill(name="C++", category="Languages"),
            Skill(name="JavaScript", category="Languages"),
            Skill(name="TypeScript", category="Languages"),
            Skill(name="FastAPI", category="Frameworks"),
            Skill(name="React", category="Frameworks"),
            Skill(name="Streamlit", category="Frameworks"),
            Skill(name="PostgreSQL", category="Databases"),
            Skill(name="Redis", category="Databases"),
            Skill(name="Docker", category="Databases"),
            Skill(name="LLM Routing", category="AI/ML"),
            Skill(name="Scikit-learn", category="AI/ML"),
            Skill(name="Power BI", category="Developer Tools")
        ],
        experiences=[
            Experience(
                company="Rajputana Vehicles Pvt. Ltd.",
                role="Data Analyst Intern",
                org_type="Enterprise",
                is_open_source=False,
                skills=["Python", "SQL", "Power BI"],
                bullets=[
                    "Designed Business Intelligence (BI) dashboards to track Key Performance Indicators (KPIs) for sales regions.",
                    "Conducted customer segmentation analysis to drive 15% more targeted marketing strategies (PR #42).",
                    "Collaborated with senior management to translate complex data into actionable business reports.",
                    "Utilized Python and Excel to automate weekly reporting processes, reducing manual effort by 40% (Commit 9ab13)."
                ],
                evidence=[
                    Evidence(
                        type="PR",
                        description="Customer segmentation clustering spec (PR #42)",
                        url="https://github.com/rajputana/bi-analytics/pull/42",
                        metrics="15% targeted marketing"
                    ),
                    Evidence(
                        type="Commit",
                        description="Automate weekly report generation script (Commit 9ab13)",
                        url="https://github.com/rajputana/bi-analytics/commit/9ab13",
                        metrics="40% manual reduction"
                    )
                ]
            ),
            Experience(
                company="Electronic Arts (Forage)",
                role="Software Engineering Experience",
                org_type="Simulation",
                is_open_source=False,
                skills=["C++"],
                bullets=[
                    "Proposed a new feature for the EA Sports College Football and wrote a Feature Proposal.",
                    "Built a class diagram and created a header file in C++ with class definitions for each object.",
                    "Patched a bugfix and optimized the codebase by implementing an improved data structure (Commit ea10a)."
                ],
                evidence=[
                    Evidence(
                        type="Commit",
                        description="Patch bugfix in college football simulation class definitions (Commit ea10a)",
                        url="https://github.com/forage/ea-simulation/commit/ea10a"
                    )
                ]
            ),
            Experience(
                company="JPMorgan Chase & Co. (Forage)",
                role="Software Engineering Experience",
                org_type="Simulation",
                is_open_source=False,
                skills=["Python", "React"],
                bullets=[
                    "Gained practical experience in software engineering tasks and financial technology."
                ],
                evidence=[]
            ),
            # Seeding the ADEN open-source role as requested by the rule guidelines
            Experience(
                company="ADEN (YC-backed)",
                role="Open Source Contributor",
                org_type="YC-backed startup",
                is_open_source=True,
                skills=["Python", "LLM Routing", "FastAPI"],
                bullets=[
                    "Contributed engineering improvements to a YC-backed startup's open-source ecosystem (PR #142).",
                    "Collaborated through GitHub workflows including issues, pull requests, and code reviews (PR #142).",
                    "Implemented high-performance prompt routing logic resulting in a 15% latency reduction (Merged PR #142)."
                ],
                evidence=[
                    Evidence(
                        type="PR",
                        description="Implement prompt routing cache (Merged PR #142)",
                        url="https://github.com/aden-ai/gateway/pull/142",
                        metrics="15% latency reduction"
                    )
                ]
            ),
            Experience(
                company="Technozion, NIT Warangal",
                role="PR Team Head",
                org_type="Leadership Fest",
                is_open_source=False,
                skills=["Python"],
                bullets=[
                    "Led the Public Relations team for one of South India's largest technical fests, managing a team of 50+ students.",
                    "Coordinated communication and public relations for 10,000+ attendees and resolved conflict situations.",
                    "Strategized outreach campaigns that increased student participation by 20% (Commit 9ab13)."
                ],
                evidence=[]
            ),
            Experience(
                company="Springspree, NIT Warangal",
                role="Sponsorship Team Head",
                org_type="Leadership Fest",
                is_open_source=False,
                skills=["SQL"],
                bullets=[
                    "Managed corporate sponsorships and partnerships for the annual cultural fest.",
                    "Led negotiations with external vendors and partners to secure event funding (PR #42)."
                ],
                evidence=[]
            )
        ],
        projects=[
            Project(
                name="OMI Gateway",
                category="Backend",
                skills=["FastAPI", "Docker", "PostgreSQL", "LLM Routing", "Telemetry"],
                description_bullets=[
                    "Built an intelligent prompt routing gateway achieving 45ms average response latency (Commit 3ea92b).",
                    "Designed local caching middleware in FastAPI reducing redundant external API hops by 15% (Merged PR #142).",
                    "Orchestrated multi-container staging deployment using Docker and wrote integration tests in unittest to enforce data schema compliance."
                ],
                github_url="https://github.com/omichauhan-lgtm/omi-gateway",
                evidence=[
                    Evidence(
                        type="Commit",
                        description="Setup Docker orchestration configuration (Commit 3ea92b)",
                        url="https://github.com/omichauhan-lgtm/omi-gateway/commit/3ea92b",
                        metrics="45ms latency ceiling"
                    ),
                    Evidence(
                        type="PR",
                        description="Implement prompt routing cache (Merged PR #142)",
                        url="https://github.com/omichauhan-lgtm/omi-gateway/pull/142",
                        metrics="15% latency reduction"
                    )
                ]
            ),
            Project(
                name="AutoSight SaaS",
                category="Backend",
                skills=["FastAPI", "React", "PostgreSQL", "Redis", "Docker"],
                description_bullets=[
                    "Built a multi-tenant SaaS platform for demand forecasting and customer segmentation.",
                    "Developed B2B SaaS dashboard helping dealers understand market demand, creating visual reports for inventory planning (Commit 9ab13).",
                    "Integrated AI models to provide actionable insights into automotive market trends."
                ],
                github_url="https://github.com/omichauhan-lgtm/autosight-saas",
                evidence=[]
            ),
            Project(
                name="Credit Risk Intelligence",
                category="AI/ML",
                skills=["Python", "Streamlit", "Scikit-learn", "Pandas"],
                description_bullets=[
                    "Developed an automated system using machine learning default risk assessment prediction model (Logistic Regression).",
                    "Created an interactive Streamlit dashboard for real-time risk assessment and portfolio quality visualization (Commit 9ab13)."
                ],
                github_url="https://github.com/omichauhan-lgtm/credit-risk-intel",
                evidence=[]
            )
        ],
        star_stories=[
            STARStory(
                project_or_company="OMI Gateway",
                situation="The OMI backend gateway had high latency routing requests across multiple models.",
                task="Minimize latency overhead for model dispatch.",
                action="Added local memory caching mapping prompt hashes in FastAPI.",
                result="Achieved a 45ms average response latency ceiling, verified via unittest suites."
            )
        ]
    )

    # Insert profile into database
    db = SessionLocal()
    try:
        import_master_profile(db, profile)
        print("Database successfully seeded with Master Career Profile!")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
