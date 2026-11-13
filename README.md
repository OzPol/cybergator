# CyberGator

CyberGator is a research prototype for exploring cyber resilience using a bundled
System Under Evaluation (SUE) dataset from the Navy CRAM Challenge. It combines
Flask, Plotly Dash, Cytoscape, NetworkX, and JSON/CSV data.

The default application runs without login, PostgreSQL, Neo4j, API keys, or a
`.env` file. Its scores are experimental research outputs.

## Start with Docker

Install and start Docker Desktop (or Docker Engine with Compose). Python and
Poetry are installed during the image build; they are not needed on your host.

```sh
git clone https://github.com/OzPol/cybergator.git
cd cybergator
docker compose up --build --wait
```

Open **http://localhost:8000**. Stop with `docker compose down`.

After pulling dependency or Dockerfile changes, refresh the image with:

```sh
docker compose build --pull
docker compose up --wait
```

Building a replacement does not patch old images or already-running containers.
Remove obsolete images through Docker Desktop after confirming the new build works.

## Run locally

Use Python 3.12 or 3.13 and Poetry 2.5.1. From the repository root:

```sh
poetry install --only main --no-root
poetry run python app.py
```

Open **http://localhost:8000**. The local server listens on loopback and does not
enable Flask's debugger. Keep the working directory at the repository root.

## Data and scope

- Demo changes affect the shared sample dataset within that instance.
- Docker stores data and generated graph assets in named volumes. They survive
  `docker compose down`; use the in-app reset controls to restore sample inputs.
- `docker compose down --volumes` deletes the demo volumes and all edits in them.
  The next startup initializes fresh copies from the image.
- Local runs update files under `app/data` and generated assets under `assets`.
- APT/CVE simulations can use the bundled CVSS metadata. Optional live NVD lookups
  need network access; `NVD_API_KEY` is optional.
- The app is a local, shared-data demo. Authentication, private uploads, and
  isolated user workspaces are future work. Do not use this version for private
  user data or expose it as an authenticated multi-user service.

## Optional Neo4j

The JSON System Graph works independently of Neo4j. For an existing Neo4j 5
instance, copy `.env.example` to `.env` and set:

```dotenv
INSTALL_EXTRAS=neo4j
NEO4J_ENABLED=true
NEO4J_URI=neo4j+s://YOUR_INSTANCE.databases.neo4j.io
NEO4J_USER=neo4j
NEO4J_PASSWORD=YOUR_NEW_PASSWORD
```

Rebuild with `docker compose up --build --wait`. For a local Python installation,
use `poetry install --only main --no-root --extras neo4j` instead.

The Neo4j menu appears only when enabled. Connections are created on demand,
and an unavailable backend leaves the JSON demo usable. Importing nodes through
`POST /api/neo4j/import` writes the bundled dataset to your configured database.
No database is provisioned automatically.

Previously committed Neo4j credentials must be revoked or rotated with the
provider. Deleting them from the current source cannot revoke them or erase
existing Git history.

## PostgreSQL and authentication

The old authentication modules remain for reference and their unit tests, but
the application does not register their API routes or login callbacks. It never
connects to PostgreSQL during demo startup. An optional `postgres` dependency
extra retains driver support for future development; installing it does not
enable authentication. Redesign server-side authorization and per-user data
isolation before restoring those routes.

## Dependencies and checks

Poetry and `poetry.lock` define the environment. Pillow and Matplotlib are no
longer dependencies: the legacy static graph now renders as SVG. The interactive
Cytoscape and Plotly views retain their existing implementations.

```sh
poetry install --no-root
poetry run python -m unittest discover -s tests -p '*test*.py'
poetry run pip-audit --strict
poetry run python scripts/smoke_test.py
```

The smoke check requires the application to be running at localhost:8000.
For another address, pass its URL as an argument. CI tests without database
secrets, checks dependencies, builds the runtime image, and exercises HTTP APIs
and page callbacks. Browser navigation, chart rendering, graph rendering, and
recalculation are checked with Playwright in CI.

## Project background

The repository preserves the senior-project application and experimental scoring
logic. Documentation and earlier prototypes in other CyberGator repositories
describe project evolution; they are not runtime dependencies.
