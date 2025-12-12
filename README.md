# safe-code-executor

This is a safe code executor project that runs untrusted Python code safely using Docker.

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

**Install Flask:**

```
pip install flask

```

**To check installation:**

```
pip show flask

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

## Test the API:

**Open the web UI**

- In your browser visit:

```
http://localhost:5000

```

- Type code and click Run. Output will appear below.

**curl (Linux/macOS)**

```
curl -s -X POST http://localhost:5000/run \
  -H "Content-Type: application/json" \
  -d '{"code":"print(2+2)"}' | jq

```

**curl (Windows CMD)**

```
curl -s -X POST http://localhost:5000/run -H "Content-Type: application/json" -d "{\"code\":\"print(2+2)\"}"

```

**Postman**

```
POST http://localhost:5000/run with JSON body: { "code": "for i in range(3): print(i)" }

```

## Test safety features (examples)

**Infinite loop**

```
while True:
    pass

```

- Expect: Execution timed out after 10 seconds

**Memory bomb**

```
x = "a" * 1000000000
print("done")

```

- Expect: container killed or OOM error (returned as stderr/exit code)

**Network blocking**

```
import socket
socket.gethostbyname("example.com")
```
- Expect: network error due to --network none
