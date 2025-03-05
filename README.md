# cybergator

CyberGator: A Dynamic Framework for Cyber Resilience Assessment

## Project Overview

CyberGator is a cyber resilience assessment framework designed for dynamic risk evaluation, attack simulation, and adaptive defense strategy generation. It integrates Flask, Plotly Dash, Neo4j, PostgreSQL (via Supabase), and AI-driven simulations to model and improve system resilience against Advanced Persistent Threats (APTs).

---

## Pre-requisites

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

## How to add and install new dependencies to the application

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
