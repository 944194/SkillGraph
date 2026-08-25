from database import execute_query, verify_connection


def seed_database():
    print("Clearing existing graph data...")

    execute_query("""
        MATCH (n)
        DETACH DELETE n
    """)

    print("Creating SkillGraph data...")

    query = """
    // Create industries
    CREATE
        (software:Industry {
            id: "industry_1",
            name: "Software"
        }),
        (fintech:Industry {
            id: "industry_2",
            name: "FinTech"
        }),
        (healthcare:Industry {
            id: "industry_3",
            name: "Healthcare"
        }),
        (ecommerce:Industry {
            id: "industry_4",
            name: "E-Commerce"
        })

    // Create companies
    CREATE
        (technova:Company {
            id: "company_1",
            name: "TechNova",
            location: "Hyderabad"
        }),
        (dataworks:Company {
            id: "company_2",
            name: "DataWorks",
            location: "Bangalore"
        }),
        (cloudsoft:Company {
            id: "company_3",
            name: "CloudSoft",
            location: "Pune"
        }),
        (innovatelabs:Company {
            id: "company_4",
            name: "InnovateLabs",
            location: "Hyderabad"
        })

    // Create skills
    CREATE
        (python:Skill {
            id: "skill_1",
            name: "Python",
            category: "Programming"
        }),
        (django:Skill {
            id: "skill_2",
            name: "Django",
            category: "Backend"
        }),
        (flask:Skill {
            id: "skill_3",
            name: "Flask",
            category: "Backend"
        }),
        (javascript:Skill {
            id: "skill_4",
            name: "JavaScript",
            category: "Frontend"
        }),
        (react:Skill {
            id: "skill_5",
            name: "React",
            category: "Frontend"
        }),
        (sql:Skill {
            id: "skill_6",
            name: "SQL",
            category: "Database"
        }),
        (rest:Skill {
            id: "skill_7",
            name: "REST API",
            category: "Backend"
        }),
        (ml:Skill {
            id: "skill_8",
            name: "Machine Learning",
            category: "AI"
        })

    // Create jobs
    CREATE
        (backend:Job {
            id: "job_1",
            title: "Backend Developer",
            experience: "0-2 years"
        }),
        (fullstack:Job {
            id: "job_2",
            title: "Full Stack Developer",
            experience: "1-3 years"
        }),
        (python_dev:Job {
            id: "job_3",
            title: "Python Developer",
            experience: "0-2 years"
        }),
        (data_analyst:Job {
            id: "job_4",
            title: "Data Analyst",
            experience: "0-2 years"
        }),
        (ml_engineer:Job {
            id: "job_5",
            title: "ML Engineer",
            experience: "1-3 years"
        })

    // Create people
    CREATE
        (rahul:Person {
            id: "person_1",
            name: "Rahul",
            email: "rahul@example.com"
        }),
        (priya:Person {
            id: "person_2",
            name: "Priya",
            email: "priya@example.com"
        }),
        (arjun:Person {
            id: "person_3",
            name: "Arjun",
            email: "arjun@example.com"
        }),
        (sneha:Person {
            id: "person_4",
            name: "Sneha",
            email: "sneha@example.com"
        }),
        (kiran:Person {
            id: "person_5",
            name: "Kiran",
            email: "kiran@example.com"
        })

    // Person -> Skill
    CREATE
        (rahul)-[:HAS_SKILL]->(python),
        (rahul)-[:HAS_SKILL]->(django),
        (rahul)-[:HAS_SKILL]->(sql),
        (rahul)-[:HAS_SKILL]->(rest),

        (priya)-[:HAS_SKILL]->(python),
        (priya)-[:HAS_SKILL]->(javascript),
        (priya)-[:HAS_SKILL]->(react),
        (priya)-[:HAS_SKILL]->(sql),

        (arjun)-[:HAS_SKILL]->(python),
        (arjun)-[:HAS_SKILL]->(flask),
        (arjun)-[:HAS_SKILL]->(rest),

        (sneha)-[:HAS_SKILL]->(sql),
        (sneha)-[:HAS_SKILL]->(python),
        (sneha)-[:HAS_SKILL]->(ml),

        (kiran)-[:HAS_SKILL]->(javascript),
        (kiran)-[:HAS_SKILL]->(react),
        (kiran)-[:HAS_SKILL]->(sql)

    // Job -> Skill
    CREATE
        (backend)-[:REQUIRES_SKILL]->(python),
        (backend)-[:REQUIRES_SKILL]->(django),
        (backend)-[:REQUIRES_SKILL]->(sql),
        (backend)-[:REQUIRES_SKILL]->(rest),

        (fullstack)-[:REQUIRES_SKILL]->(python),
        (fullstack)-[:REQUIRES_SKILL]->(javascript),
        (fullstack)-[:REQUIRES_SKILL]->(react),
        (fullstack)-[:REQUIRES_SKILL]->(sql),

        (python_dev)-[:REQUIRES_SKILL]->(python),
        (python_dev)-[:REQUIRES_SKILL]->(flask),
        (python_dev)-[:REQUIRES_SKILL]->(rest),

        (data_analyst)-[:REQUIRES_SKILL]->(python),
        (data_analyst)-[:REQUIRES_SKILL]->(sql),

        (ml_engineer)-[:REQUIRES_SKILL]->(python),
        (ml_engineer)-[:REQUIRES_SKILL]->(sql),
        (ml_engineer)-[:REQUIRES_SKILL]->(ml)

    // Job -> Company
    CREATE
        (backend)-[:OFFERED_BY]->(technova),
        (fullstack)-[:OFFERED_BY]->(technova),
        (python_dev)-[:OFFERED_BY]->(cloudsoft),
        (data_analyst)-[:OFFERED_BY]->(dataworks),
        (ml_engineer)-[:OFFERED_BY]->(innovatelabs)

    // Company -> Industry
    CREATE
        (technova)-[:IN_INDUSTRY]->(software),
        (cloudsoft)-[:IN_INDUSTRY]->(software),
        (dataworks)-[:IN_INDUSTRY]->(fintech),
        (innovatelabs)-[:IN_INDUSTRY]->(healthcare)

    // Person -> Company
    CREATE
        (rahul)-[:WORKED_AT]->(technova),
        (priya)-[:WORKED_AT]->(dataworks),
        (arjun)-[:WORKED_AT]->(cloudsoft),
        (sneha)-[:WORKED_AT]->(innovatelabs),
        (kiran)-[:WORKED_AT]->(technova)
    """

    execute_query(query)

    print("SkillGraph data created successfully!")


if __name__ == "__main__":
    verify_connection()
    seed_database()