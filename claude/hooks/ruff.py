import json
import subprocess
import sys

data = json.load(sys.stdin)
file = data.get("tool_input", {}).get("file_path", "")

if file.endswith(".py"):
    subprocess.run(["uvx", "ruff", "format", file])
    subprocess.run(["uvx", "ruff", "check", "--fix", file])
