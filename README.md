# safe-code-executor

## Project Structure

safe-code-executor/

├── app.py

├── run_in_docker.py   

├── requirements.txt

├── .gitignore

└── static/

    └── index.html

## How to run locally

Make sure Docker is installed and the current user can run docker (on Linux you may need to add user to docker group, on Windows use Docker Desktop).

Create & activate virtualenv;

```
python3 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

```

- **install Flask:**

```
pip install flask

```

## Start Docker and run the app

1. Make sure Docker Desktop is running.
2. In VS Code terminal, with the virtualenv active, run:

```
python app.py

```
You should see Flask listening on port 5000:

```
Running on http://0.0.0.0:5000

```
