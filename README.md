# safe-code-executor

A secure, containerized Python code execution API built with Flask and Docker. Users can submit Python code through an API or simple web UI, and the application executes it inside an isolated Docker container with strict safety limits.

## Project Structure

safe-code-executor/

├── app.py                         # Flask API

├── run_in_docker.py               # Docker execution helper

├── requirements.txt               # Python dependencies

├── .gitignore

└── static/

    └── index.html                 # Simple Web UI

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
<img width="1414" height="918" alt="Screenshot 2025-12-13 004305" src="https://github.com/user-attachments/assets/602986f8-5263-4f65-943e-2e1af20f24be" />

<img width="1465" height="929" alt="Screenshot 2025-12-13 002126" src="https://github.com/user-attachments/assets/69e6a7c6-b067-46a4-9c0c-5e38316f5d45" />

## Test the API:

**Open the web UI**

- In your browser visit:

```
http://localhost:5000
```

- Type code and click Run. Output will appear below.

**Web UI**

- To print "Hello World".

<img width="977" height="635" alt="Screenshot 2025-12-13 001302" src="https://github.com/user-attachments/assets/4a107aed-b9c6-4ff8-ac59-cd60710d320e" />

- To print numbers from 1 to 10 using range().

<img width="1046" height="760" alt="Screenshot 2025-12-13 001707" src="https://github.com/user-attachments/assets/c8690f40-134a-4a49-8e00-dda496e4ad70" />


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
<img width="946" height="616" alt="Screenshot 2025-12-13 002747" src="https://github.com/user-attachments/assets/45171e27-9a73-44df-836e-85a4caa72af0" />

**Memory bomb**

```
x = "a" * 1000000000
print("done")
```

- Expect: container killed or OOM error (returned as stderr/exit code)
<img width="962" height="605" alt="Screenshot 2025-12-13 003232" src="https://github.com/user-attachments/assets/16f8b2b2-2c52-4e22-8b1f-ff5d9175da17" />

**Network blocking**

```
import socket
socket.gethostbyname("example.com")
```
- Expect: network error due to --network none

**Write to FS test**

```
with open('/tmp/test.txt','w') as f:
    f.write('hello')
print("wrote")
```
- Expect: OSError when --read-only is set

## Troubleshooting

**Browser shows "127.0.0.1 refused to connect"**
- Make sure Flask is still running (terminal must remain open)
- Check with:

```
netstat -ano | findstr ":5000"
```

**Docker permission errors**
- Run Docker Desktop as Administrator.

**PowerShell: script execution blocked**
- Run:
```
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
```

**curl errors in PowerShell**
- Use PowerShell-native:
```
Invoke-RestMethod ...
```

## Conclusion

The Safe Code Executor project shows how to securely run untrusted Python code using Docker and Flask. By applying timeouts, memory limits, network isolation, and read-only filesystems, it demonstrates practical techniques for sandboxing code and preventing harmful behavior. This project provides a solid foundation for understanding execution security and can be extended with more languages, features, or UI improvements.
