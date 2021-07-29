FROM python:3.9-slim-buster as base
# Install poetry
RUN pip install poetry
WORKDIR /app
# Expose the port that we want the host to listen to
EXPOSE 5000
# Copy across the project files
COPY . /app

FROM base as production
ENV FLASK_ENV=production
# Install the project dependencies
RUN poetry install --no-dev
# Set the script to run as production on startup of the container
ENTRYPOINT ["poetry", "run", "gunicorn", "--config", "gunicorn_config.py", "todo_app.app:create_app()"]

FROM base as development
ENV FLASK_ENV=development
# Install the project dependencies
RUN poetry install
# Set the script to run as development on startup of the container
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5000"]
