# SkillGraph

SkillGraph is a graph-powered career intelligence web application that helps users explore relationships between people, skills, jobs, companies, and industries.

## Features

- View skills associated with a person
- Recommend jobs based on a person's skills
- Calculate job match percentages
- Identify missing skills for jobs
- Explore multi-hop career paths
- Explore people and opportunities connected to a skill
- Case-insensitive skill search
- Interactive web interface
- Error handling for invalid people and skills

## Technology Stack

### Backend
- Python
- Flask
- Neo4j Python Driver
- python-dotenv

### Database
- Neo4j / CognoDB
- Cypher Query Language

### Frontend
- HTML
- CSS
- JavaScript
- Bootstrap

## Application Architecture

```text
User
  |
  v
Frontend
HTML / CSS / JavaScript
  |
  v
Flask REST API
  |
  v
Neo4j / CognoDB
  |
  v
Graph Relationships