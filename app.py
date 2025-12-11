from flask import Flask, request, jsonify, send_from_directory
import tempfile
import os
from run_in_docker import run_code_in_docker

app = Flask(__name__, static_folder="static", static_url_path="")

MAX_CODE_SIZE = 5000
MEMORY_LIMIT = "128m"
TIMEOUT_SECONDS = 10

@app.route("/")
def index():
    # serve the simple static UI
    return send_from_directory(app.static_folder, "index.html")

@app.post("/run")
def run_code():
    data = request.get_json(force=True, silent=True) or {}
    code = data.get("code", "")

    if not isinstance(code, str):
        return jsonify({"error": "Invalid request: 'code' must be a string"}), 400

    if len(code) > MAX_CODE_SIZE:
        return jsonify({"error": f"Code too long (max {MAX_CODE_SIZE} chars)"}), 400

    # create a temporary file to hold the script
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        script_path = f.name
        f.write(code)

    try:
        rc, stdout, stderr, timed_out = run_code_in_docker(
            script_host_path=script_path,
            memory=MEMORY_LIMIT,
            timeout_seconds=TIMEOUT_SECONDS,
            read_only=True
        )

        if timed_out:
            return jsonify({"error": f"Execution timed out after {TIMEOUT_SECONDS} seconds"}), 200

        # If docker returned non-zero but with stderr, include it
        if rc != 0:
            # If there is stderr, show it. Otherwise, return generic error
            output = stderr.strip() or stdout.strip()
            return jsonify({"output": output, "exit_code": rc}), 200

        return jsonify({"output": stdout.strip()}), 200

    finally:
        # remove the temporary script file
        try:
            os.remove(script_path)
        except Exception:
            pass

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
