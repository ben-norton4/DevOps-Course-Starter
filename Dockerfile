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
# Run as production on startup of the container
#ENTRYPOINT ["poetry", "run", "gunicorn", "--config", "gunicorn_config.py", "todo_app.app:create_app()"]
RUN chmod +x ./entrypoint.sh
ENTRYPOINT ./entrypoint.sh

FROM base as development
ENV FLASK_ENV=development
# Install the project dependencies
RUN poetry install
# Run as development on startup of the container
ENTRYPOINT ["poetry", "run", "flask", "run", "--host=0.0.0.0", "--port=5000"]

FROM base as test
ENV FLASK_ENV=development

RUN apt-get update -qqy && apt-get install -qqy wget gnupg unzip
# Install Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
&& echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
&& apt-get update -qqy \
&& apt-get -qqy install google-chrome-stable \
&& rm /etc/apt/sources.list.d/google-chrome.list \
&& rm -rf /var/lib/apt/lists/* /var/cache/apt/*

# Install Chrome WebDriver
RUN CHROME_MAJOR_VERSION=$(google-chrome --version | sed -E "s/.* ([0-9]+)(\.[0-9]+){3}.*/\1/") \
&& CHROME_DRIVER_VERSION=$(wget --no-verbose -O - "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_MAJOR_VERSION}") \
&& echo "Using chromedriver version: "$CHROME_DRIVER_VERSION \
&& wget --no-verbose -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip \
&& unzip /tmp/chromedriver_linux64.zip -d /usr/bin \
&& rm /tmp/chromedriver_linux64.zip \
&& chmod 755 /usr/bin/chromedriver

# Install the project dependencies
RUN poetry install

# Run test suite
ENTRYPOINT ["poetry", "run", "pytest"]
