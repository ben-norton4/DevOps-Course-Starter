# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie. 

To call the Trello API you will need to set environment variables for a [TRELLO_API_KEY] and [TRELLO_API_TOKEN] in the .env file. To create these you will need to set up a Trello account here: https://trello.com/signup and generate an API key and API token by following the instructions here: https://trello.com/app-key.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

## Testing the App

Testing is done in this app using pytest.

The end-to-end tests use a FireFox driver for the tests. You will need to have FireFox installed on your system. You will also need to download the GeckoDriver executable and place it in the root of the project. FireFox and GeckoDriver will need to be the same version to work together. GeckoDriver can be downloaded from here: https://github.com/mozilla/geckodriver/releases

You can test the app in a number of ways.

1. From the command line:
```
$ poetry run pytest
```

2. Configure VSCode:
    
Install Python extension if not already installed. Then select the Python interpreter to use. Use the below command to find the correct interpreter for your virtual environment:

Mac / Linux / WSL
```
$ poetry run which python
```

Windows Powershell
```
 $ poetry run where python
```

Select the Python executable from the status bar that corresponds to the virtual environment

In VSCode settings add these values:
```
"python.testing.unittestEnabled": false,
"python.testing.nosetestsEnabled": false,
"python.testing.pytestEnabled": true
```
Run (Ctrl + Shift + P) "Discover Tests" then "Run Tests" from the command palette to check it's working. You can run tests for the whole suite or individually from the Testing view in the VSCode sidebar.
