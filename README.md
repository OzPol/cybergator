# cybergator
CyberGator: A Dynamic Framework for Cyber Resilience Assessment

## Project Overview
CyberGator is a cyber resilience assessment framework designed for dynamic risk evaluation, attack simulation, and adaptive defense strategy generation. It integrates Flask, Plotly Dash, Neo4j, PostgreSQL (via Supabase), and AI-driven simulations to model and improve system resilience against Advanced Persistent Threats (APTs).

---

## Configuring Environment Variables
This project relies on environment variables. Follow the instructions in `.env.template` file to create your `.env`:

---

Prerequisites

Make sure you have the following installed on your system:
- **[Docker](https://www.docker.com/get-started)**
- **[Poetry](https://python-poetry.org/docs/#installation)**

Verify installations:

    docker --version
    poetry --version

Running the Application (Development Mode)

For now, to run the app locally:
    poetry run python app.py

Note: If running inside VS Code (or your IDE terminal) causes issues, open PowerShell and execute the command there.

Run the container with (triggered by CI/CD on push as well):
    docker-compose up --build


## 1. Repository Structure

    cybergator/
    │── .github/
    │   │── workflows/
    │   │   │── deploy.yml
    │   │   │── test.yml
    │
    │── api/
    │   │── __init__.py
    │   │── auth_routes.py               
    │   │── cve_routes.py
    │   │── dashboard_routes.py
    │   │── inventory_routes.py           
    │   │── neo4j_routes.py              
    │   │── pg_routes.py                 
    │   │── risk_routes.py
    │   │── simulation_routes.py           
    │
    │── backend/
    │   │── algorithms/
    │   │   │── bayesian_networks.py
    │   │   │── fuzzy_logic.py
    │   │   │── nearest_neighbors.py
    │   │   │── neural_network.py
    │   │   │── __init__.py
    │   │── simulations/
    │   │   │── apt_simulation.py
    │   │   │── attack_simulations.py
    │   │   │── bayesian_simulation.py
    │   │   │── cve_simulation.py
    │   │   │── fsm_bn_simulation.py
    │   │   │── fsm_simulation.py
    │   │   │── nns_simulation.py
    │   │   │── __init__.py
    │   │── fsm_engine.py
    │   │── graph_processing.py
    │   │── json_handler.py
    │   │── resilience_calculator.py
    │   │── __init__.py
    │
    │── frontend/
    │   │── callbacks/
    │   │   │── bayesian_callbacks.py
    │   │   │── cve_callbacks.py
    │   │   │── dashboard_callbacks.py
    │   │   │── fsm_callbacks.py
    │   │   │── graph_callbacks.py
    │   │   │── inventory_callbacks.py
    │   │   │── login_callbacks.py
    │   │   │── register_callbacks.py
    │   │   │── simulation_callbacks.py
    │   │   │── __init__.py
    │   │── components/
    │   │   │── buttons.py
    │   │   │── charts.py
    │   │   │── navbar.py
    │   │   │── sidebar.py
    │   │   │── tables.py
    │   │   │── __init__.py
    │   │── layouts/
    │   │   │── bayesian_simulation.py
    │   │   │── cve_dashboard.py
    │   │   │── dashboard.py
    │   │   │── fsm_simulation.py
    │   │   │── holistic_simulation.py
    │   │   │── homepage.py
    │   │   │── login.py
    │   │   │── network_graph.py
    │   │   │── register.py
    │   │   │── __init__.py
    │   │── static/
    │   │── templates/
    │
    │── database/
    │   │── neo4j.py
    │   │── supabase.py
    │   │── db_initializer.py
    │   │── __init__.py
    │
    │── data/
    │   │── json/
    │   │   │── cve_data.json
    │   │   │── nodes_complete.json
    │   │   │── risk_factors.json
    |   │   │── critical_functions.json
    │   │── neo4j/
    │   │   │── graph_schema.cql
    │   │── postgresql/
    │   │   │── schema.sql
    │
    │── logs/
    │   │── attack_logs.json
    │   │── bayesian_logs.json
    │   │── fsm_logs.json
    │
    │── tests/
    │   │── test_api.py
    │   │── test_database.py
    │   │── test_fsm.py
    │   │── test_graph.py
    │   │── test_simulation.py
    │   │── __init__.py
    │
    │── app.py
    │── config.py
    │── .env
    │── .gitignore
    │── docker-compose.yml
    │── Dockerfile
    │── README.md
    │── requirements.txt
    │── pyproject.toml
    │── setup.sh
    │── setup.bat
    │── build_executable.sh

---

## 2. Setting Up the Development Environment

### Clone the Repository

    git clone https://github.com/your-org/cybergator.git
    cd cybergator

### Running the Application (Cross-Platform Setup)

#### **For macOS/Linux Users:**
    chmod +x setup.sh
    ./setup.sh

#### **For Windows Users:**
    setup.bat

---

## 3. Development Workflow

### Creating a New Branch

    git checkout -b feature-xyz

### Committing and Pushing Changes

    git add .
    git commit -m "Added feature XYZ"
    git push origin feature-xyz

### Running Tests

    docker-compose exec app poetry run pytest

---

## 4. CI/CD and Deployment

- Every time a new commit is pushed to main, GitHub Actions:
  - Runs tests
  - Builds the Docker image
  - Pushes the image to Docker Hub

- To manually build and run locally:

    docker build -t cybergator:latest .
    docker run -p 5000:5000 cybergator:latest

---

### Installing PyInstaller (Only Needed Once)

Inside Docker or locally:

poetry add pyinstaller

### Creating the PyInstaller Build Script

Inside build_executable.sh file:

#!/bin/bash
poetry run pyinstaller --onefile --name CyberGator app.py

This script packages the entire application into a single standalone executable.

### Running the Build Process

To generate the executable, run:

chmod +x build_executable.sh
./build_executable.sh

This will create a **single executable file** inaside the dist/ folder.
Once complete, the dist/ folder will contain:

    dist/
      ├── CyberGator.exe  # Windows
      ├── CyberGator  # macOS/Linux


The build_executable.sh script runs pyinstaller to package the application into a self-contained executable, including:
- All Python dependencies
- The Flask and Dash backend
- The compiled Python scripts for resilience calculations and simulations

### **Distributing the Application**
To distribute the application:
1. **Zip the dist/ folder**
2. **Send the ZIP file to users**
3. **Users unzip and double-click the executable (CyberGator.exe or CyberGator)**

### **Running the Application Without Any Setup**
- **Windows users:** Double-click CyberGator.exe
- **macOS/Linux users:** Open a terminal in dist/ and run:

    ./CyberGator

---