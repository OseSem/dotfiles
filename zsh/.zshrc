# Add latest uv-installed Python to PATH (so python/python3 -> uv's cpython)
_uv_python_root="${HOME}/.local/share/uv/python"
if [[ -d "$_uv_python_root" ]]; then
  _latest_uv_python=$(print -l "$_uv_python_root"/cpython-*/bin(N) | sort -V | tail -1)
  if [[ -n "$_latest_uv_python" ]]; then
    export PATH="$_latest_uv_python:$PATH"
  fi
fi
unset _uv_python_root _latest_uv_python

# Claude Code
alias cc='claude --dangerously-skip-permissions'
