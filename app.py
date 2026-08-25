from flask import Flask, jsonify, render_template

from database import execute_query, verify_connection

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/people/<person_name>/skills")
def get_person_skills(person_name):

    query = """
    MATCH (person:Person)-[:HAS_SKILL]->(skill:Skill)
    WHERE person.name = $person_name
    RETURN person.name AS person, skill.name AS skill
    ORDER BY skill.name
    """

    parameters = {
        "person_name": person_name
    }

    results = execute_query(query, parameters)

    if not results:
        return jsonify({
            "message": "Person not found or no skills available"
        }), 404

    return jsonify({
        "person": results[0]["person"],
        "skills": [row["skill"] for row in results]
    })



@app.route("/api/people/<person_name>/jobs")
def get_person_jobs(person_name):

    query = """
    MATCH (person:Person {name: $person_name})-[:HAS_SKILL]->(skill:Skill)
    MATCH (job:Job)-[:REQUIRES_SKILL]->(skill)

    WITH
        person,
        job,
        collect(DISTINCT skill.name) AS matching_skills

    MATCH (job)-[:REQUIRES_SKILL]->(required_skill:Skill)

    WITH
        person,
        job,
        matching_skills,
        collect(DISTINCT required_skill.name) AS required_skills

    WITH
        person,
        job,
        matching_skills,
        required_skills,
        size(matching_skills) AS matching_count,
        size(required_skills) AS required_count

    RETURN
        job.title AS job,
        matching_skills,
        required_skills,
        [skill IN required_skills
            WHERE NOT skill IN matching_skills] AS missing_skills,
        matching_count,
        required_count,
        toFloat(matching_count) / required_count * 100 AS match_percentage

    ORDER BY match_percentage DESC
    """

    parameters = {
        "person_name": person_name
    }

    results = execute_query(query, parameters)

    if not results:
        return jsonify({
            "message": "No matching jobs found for this person"
        }), 404

    for result in results:
        result["match_percentage"] = round(
            result["match_percentage"], 1
        )

    return jsonify({
        "person": person_name,
        "recommendations": results
    })


@app.route("/api/people/<person_name>/career-path")
def get_career_path(person_name):

    query = """
    MATCH (person:Person {name: $person_name})
          -[:HAS_SKILL]->(skill:Skill)
          <-[:REQUIRES_SKILL]-(job:Job)
          -[:OFFERED_BY]->(company:Company)
          -[:IN_INDUSTRY]->(industry:Industry)

    RETURN DISTINCT
        person.name AS person,
        skill.name AS skill,
        job.title AS job,
        company.name AS company,
        company.location AS location,
        industry.name AS industry

    ORDER BY job.title, skill.name
    """

    parameters = {
        "person_name": person_name
    }

    results = execute_query(query, parameters)

    if not results:
        return jsonify({
            "message": "No career paths found for this person"
        }), 404

    return jsonify({
        "person": person_name,
        "career_paths": results
    })


@app.route("/api/skills/<skill_name>")
def get_skill_explorer(skill_name):

    query = """
    MATCH (skill:Skill)
    WHERE toLower(skill.name) = toLower($skill_name)

    OPTIONAL MATCH (person:Person)-[:HAS_SKILL]->(skill)

    OPTIONAL MATCH (job:Job)-[:REQUIRES_SKILL]->(skill)
    OPTIONAL MATCH (job)-[:OFFERED_BY]->(company:Company)
    OPTIONAL MATCH (company)-[:IN_INDUSTRY]->(industry:Industry)

    RETURN
        skill.name AS skill,
        collect(DISTINCT person.name) AS people,
        collect(DISTINCT {
            job: job.title,
            company: company.name,
            location: company.location,
            industry: industry.name
        }) AS opportunities
    """

    parameters = {
        "skill_name": skill_name.strip()
    }

    results = execute_query(query, parameters)

    if not results or not results[0]["skill"]:
        return jsonify({
            "message": "Skill not found"
        }), 404

    result = results[0]

    return jsonify({
        "skill": result["skill"],
        "people": result["people"],
        "opportunities": result["opportunities"]
    })


if __name__ == "__main__":
    verify_connection()
    app.run(debug=True)