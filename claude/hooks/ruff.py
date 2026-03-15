import json
import subprocess
import sys

data = json.load(sys.stdin)
file = data.get("tool_input", {}).get("file_path", "")

if file.endswith(".py"):
    subprocess.run(["ruff", "format", file])
    subprocess.run(["ruff", "check", "--fix", file])
