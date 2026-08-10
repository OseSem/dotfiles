import json
import subprocess
import sys

data = json.load(sys.stdin)
file = data.get("tool_input", {}).get("file_path", "")

if file.endswith(".py"):
    subprocess.run(["uvx", "ruff", "format", file])
    # F401 stays unfixable: autofix deletes unused imports, including ones just
    # added for code not written yet, which means fighting the agent mid-edit.
    subprocess.run(["uvx", "ruff", "check", "--fix", "--unfixable", "F401", file])
