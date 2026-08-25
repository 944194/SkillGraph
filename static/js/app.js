const findJobsBtn = document.getElementById("findJobsBtn");

findJobsBtn.addEventListener("click", findJobs);


async function findJobs() {

    const personName =
        document.getElementById("personName").value;

    const loading =
        document.getElementById("loading");

    const errorMessage =
        document.getElementById("errorMessage");

    const resultsSection =
        document.getElementById("resultsSection");

    const jobResults =
        document.getElementById("jobResults");


    loading.classList.remove("d-none");

    errorMessage.classList.add("d-none");

    resultsSection.classList.add("d-none");

    jobResults.innerHTML = "";


    try {

        const response = await fetch(
            `/api/people/${encodeURIComponent(personName)}/jobs`
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.message || "Unable to find recommendations."
            );

        }


        data.recommendations.forEach(job => {

            const card = document.createElement("div");

            card.className = "col-md-6 col-lg-4";


   card.innerHTML = `
    <div class="job-card">

        <div class="card-body">

            <div class="d-flex justify-content-between align-items-start">

                <div>
                    <div class="job-title">
                        ${job.job}
                    </div>
                </div>

                <span class="match-badge">
                    ${job.match_percentage}%
                </span>

            </div>

            <div class="match-info">
                ${job.matching_count}
                of
                ${job.required_count}
                required skills matched
            </div>

            <div>
                ${job.matching_skills.map(skill => `
                    <span class="skill-badge matching-skill">
                        ✓ ${skill}
                    </span>
                `).join("")}
            </div>

            ${
                job.missing_skills.length > 0
                ?
                `
                <div class="missing-label">
                    Skills to develop
                </div>

                <div>
                    ${job.missing_skills.map(skill => `
                        <span class="skill-badge missing-skill">
                            + ${skill}
                        </span>
                    `).join("")}
                </div>
                `
                :
                `
                <div class="all-matched">
                    ✓ All required skills matched
                </div>
                `
            }

        </div>

    </div>
  `;


            jobResults.appendChild(card);

        });


        resultsSection.classList.remove("d-none");

    }


    catch (error) {

        errorMessage.textContent =
            error.message;

        errorMessage.classList.remove("d-none");

    }


    finally {

        loading.classList.add("d-none");

    }

}


const exploreSkillBtn =
    document.getElementById("exploreSkillBtn");


exploreSkillBtn.addEventListener(
    "click",
    exploreSkill
);


async function exploreSkill() {

    const skillName =
        document.getElementById("skillName").value.trim();


    if (!skillName) {

        alert("Please enter a skill.");

        return;

    }


    const section =
        document.getElementById(
            "skillResultsSection"
        );

    const title =
        document.getElementById("skillTitle");

    const people =
        document.getElementById("skillPeople");

    const opportunities =
        document.getElementById(
            "skillOpportunities"
        );


    section.classList.add("d-none");

    people.innerHTML = "";

    opportunities.innerHTML = "";


    try {

        const response = await fetch(
            `/api/skills/${encodeURIComponent(skillName)}`
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.message || "Skill not found."
            );

        }


        title.textContent =
            `${data.skill} Skill Explorer`;


        data.people.forEach(person => {

            const badge =
                document.createElement("span");

            badge.className = "people-badge";

            badge.textContent =
                person;

            people.appendChild(badge);

        });


        data.opportunities.forEach(
            opportunity => {

                const card =
                    document.createElement("div");

                card.className =
                    "col-md-6";


   card.innerHTML = `
    <div class="opportunity-card">

        <h3>
            ${opportunity.job}
        </h3>

        <div class="opportunity-company">
            ${opportunity.company}
        </div>

        <div class="opportunity-meta">
            ${opportunity.location}
            •
            ${opportunity.industry}
        </div>

    </div>
   `;


                opportunities.appendChild(card);

            }
        );


        section.classList.remove("d-none");

    }


    catch (error) {

        alert(error.message);

    }

}




const exploreCareerBtn =
    document.getElementById("exploreCareerBtn");


exploreCareerBtn.addEventListener(
    "click",
    exploreCareer
);


async function exploreCareer() {

    const personName =
        document.getElementById("careerPerson").value;

    const section =
        document.getElementById(
            "careerResultsSection"
        );

    const title =
        document.getElementById(
            "careerTitle"
        );

    const paths =
        document.getElementById(
            "careerPaths"
        );


    section.classList.add("d-none");

    paths.innerHTML = "";


    try {

        const response = await fetch(
            `/api/people/${encodeURIComponent(personName)}/career-path`
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.message ||
                "No career paths found."
            );

        }


        title.textContent =
            `${data.person}'s Career Paths`;


        /*
         * The API returns one record for every
         * Person → Skill → Job → Company → Industry
         * combination.
         *
         * Group the records so the same job path
         * is displayed only once.
         */

        const groupedPaths = {};


        data.career_paths.forEach(path => {

            const key =
                `${path.job}|${path.company}|${path.industry}`;


            if (!groupedPaths[key]) {

                groupedPaths[key] = {
                    person: path.person,
                    skills: [],
                    job: path.job,
                    company: path.company,
                    location: path.location,
                    industry: path.industry
                };

            }


            if (
                !groupedPaths[key].skills.includes(
                    path.skill
                )
            ) {

                groupedPaths[key].skills.push(
                    path.skill
                );

            }

        });


        Object.values(groupedPaths)
            .forEach(path => {

                path.skills.forEach(skill => {

                    const pathElement =
                        document.createElement("div");

                    pathElement.className =
                        "career-path";


                    pathElement.innerHTML = `

                        <div class="path-node">

                            <span class="path-node-label">
                                Person
                            </span>

                            <span class="path-node-name">
                                ${path.person}
                            </span>

                        </div>


                        <div class="path-arrow">
                            →
                        </div>


                        <div class="path-node path-skill">

                            <span class="path-node-label">
                                Skill
                            </span>

                            <span class="path-node-name">
                                ${skill}
                            </span>

                        </div>


                        <div class="path-arrow">
                            →
                        </div>


                        <div class="path-node path-job">

                            <span class="path-node-label">
                                Job
                            </span>

                            <span class="path-node-name">
                                ${path.job}
                            </span>

                        </div>


                        <div class="path-arrow">
                            →
                        </div>


                        <div class="path-node path-company">

                            <span class="path-node-label">
                                Company
                            </span>

                            <span class="path-node-name">
                                ${path.company}
                            </span>

                        </div>


                        <div class="path-arrow">
                            →
                        </div>


                        <div class="path-node path-industry">

                            <span class="path-node-label">
                                Industry
                            </span>

                            <span class="path-node-name">
                                ${path.industry}
                            </span>

                        </div>

                    `;


                    paths.appendChild(
                        pathElement
                    );

                });

            });


        section.classList.remove("d-none");

    }


    catch (error) {

        alert(error.message);

    }

}