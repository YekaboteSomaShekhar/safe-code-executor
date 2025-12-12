import subprocess
import shlex
import os
import uuid

def run_code_in_docker(script_host_path, container_name=None, memory="128m", timeout_seconds=10, read_only=True):
    """
    Runs the script file (absolute host path) inside a python:3.11-slim container.
    Returns (returncode, stdout, stderr, timed_out_bool)
    """
    if container_name is None:
        container_name = f"runner-{uuid.uuid4().hex[:12]}"

    # prepare volume mapping: use absolute host path
    host_path = os.path.abspath(script_host_path)
    container_path = "/code/script.py"

    # docker run command as list
    cmd = [
        "docker", "run", "--rm",
        "--name", container_name,
        f"--memory={memory}",
        "--network", "none",
    ]

    if read_only:
        cmd.append("--read-only")

    # mount script as read-only
    cmd += ["-v", f"{host_path}:{container_path}:ro", "python:3.11-slim",
            "python", container_path]

    try:
        # run and enforce timeout on the docker CLI process
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout_seconds)
        return (result.returncode, result.stdout, result.stderr, False)
    except subprocess.TimeoutExpired as e:
        # docker process didn't finish in time → forcibly kill container
        subprocess.run(["docker", "rm", "-f", container_name], capture_output=True)
        return (-1, "", f"Execution timed out after {timeout_seconds} seconds", True)
    except Exception as e:
        return (-2, "", str(e), False)
