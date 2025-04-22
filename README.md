# CyberGator

CyberGator: A Dynamic Framework for Cyber Resilience Assessment

## Table of Contents
- [Project Overview](#project-overview)
- [Pre-Requisites](#pre-requisites)
- [Running the Application (Development)](#running-the-application-development)
- [How to Add and Install New Dependencies](#how-to-add-and-install-new-dependencies)
- [How to Run Unit Tests Manually](#how-to-run-unit-tests-manually)
- [Comprehensive User Guide](#comprehensive-user-guide)
- [FAQ](#faq)

---

## Project Overview

CyberGator is a cyber resilience assessment framework designed for dynamic risk evaluation, attack simulation, and adaptive defense strategy generation. It integrates Flask, Plotly Dash, Neo4j, PostgreSQL (via Supabase), and AI-driven simulations to model and improve system resilience against Advanced Persistent Threats (APTs).

---

## Pre-Requisites

- **[Docker](https://www.docker.com/get-started)**
- **[Docker Compose](https://docs.docker.com/compose/install/)**
- **[Python >= 3.12](https://www.datacamp.com/blog/how-to-install-python)**
- **[Poetry](https://python-poetry.org/docs/#installation)**

Verify installations:

    `docker --version`

    `poetry --version`

---

## Running the Application (Development)

1. Clone the Repository

```
git clone git@github.com:OzPol/cybergator.git 
cd cybergator
```

2. Create your .env file
Your .env file should be placed in the root of the project (same level as the Dockerfile)

3. Make sure your Docker desktop is running! :)

4. Build the container

```
docker-compose build
```

5. Run the container

```
docker-compose up
```

6. Check the homepage in the browser

```
http://localhost:8000
```

7. When you are done, you can stop the container

```
docker-compose down
```

### Important Notes

- In general, you only need to rebuild the container when there are changes to dependencies.
- It's recommended to install dependencies INSIDE the container to avoid issues. Your local `poetry.lock` and `pyproject.toml` files will be automatically updated :) You can find detailed instructions for this in the next section.

## How to Add and Install New Dependencies

1. Run the container in detached mode:

```
docker-compose up -d
```

2. Install the dependency/package

```
docker exec -it cybergator_app poetry add <your-package-name>
```

3. Rebuild and run the container

```
docker-compose up --build
```

4. Optional - clean old images

```
docker image prune -f
```

## How to run unit tests manually
1. Run the container in detached mode:

```
docker-compose up -d
```
2. Run the following command:
```
docker exec -it cybergator_app poetry run python -m unittest discover -s tests -p "*.py"
```

## Comprehensive User Guide

A comprehensive User Guide is available for viewing at the following link: https://drive.google.com/file/d/1U6wDDlsVGXUzn3bGqdGD2rHODRvabtrV/view?usp=drive_link

## FAQ

1. **I added CVEs but don’t see a change in the resilience score. Why?

After making changes to nodes or CVEs, you must click “Recalculate Resilience” to update scores. Without that step, the simulation results won't refresh.

2. **How do I undo a change or start over?

Use the “Reset System” button on any page to restore the original data. This reverts to backup JSON files and clears simulation state.

3. **What do the resilience scores actually mean?

CyberGator uses a combination of fuzzy logic, Bayesian inference, and finite state machines to estimate system resilience. These scores are experimental and designed for educational and research purposes—not for production decision-making.

4. **Can I simulate multiple attacks or changes at once?

Yes. You can inject multiple CVEs, change critical functions, and modify environmental risk factors before recalculating the score. All changes are reflected in the next simulation cycle.

5. **Is the Neo4j database live?

Not yet. The Neo4j view is a prototype meant to illustrate future integration. The current system runs off structured JSON and CSV files.

6. **Where are my changes stored?

Changes are written to output JSON files located in data/json/output, which persist across sessions until reset. These files include node metrics, system scores, and resilience breakdowns.

7. **Can I export my results?

Yes. Navigate to the Export tab to download tables in CSV format, including nodes, scores, and CVE data.

8. **What if I want to test my own system?
   
This version of CyberGator is a prototype based on a single System Under Evaluation (SUE) from the CRAM Challenge. Future versions will include the ability to upload and simulate your own system architecture. Users can also manipulate the uploaded system so that it accurately reflects their own enterprise system.
