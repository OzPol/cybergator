# Use the latest Python image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy the project metadata for Poetry
COPY pyproject.toml poetry.lock ./

# Install dependencies using Poetry (includes Neo4J driver)
RUN poetry install --no-root

# Copy the rest of the application
COPY . .

# Expose only the app port (Neo4J is handled by `docker-compose.yml`)
EXPOSE 8000  

# Command to start the application
CMD ["poetry", "run", "python", "app.py"]
