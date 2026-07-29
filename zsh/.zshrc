# Add latest uv-installed Python to PATH (so python/python3 -> uv's cpython)
_uv_python_root="${HOME}/.local/share/uv/python"
if [[ -d "$_uv_python_root" ]]; then
  _latest_uv_python=$(print -l "$_uv_python_root"/cpython-*/bin(N) | sort -V | tail -1)
  if [[ -n "$_latest_uv_python" ]]; then
    export PATH="$_latest_uv_python:$PATH"
  fi
fi
unset _uv_python_root _latest_uv_python

# fnm (Node version manager). --use-on-cd auto-switches Node when entering a
# directory with an .nvmrc / .node-version.
if command -v fnm >/dev/null 2>&1; then
  eval "$(fnm env --use-on-cd --shell zsh)"
fi

# Zoxide integration
if command -v zoxide >/dev/null 2>&1; then
  eval "$(zoxide init zsh)"
fi

# Claude Code
alias cc='claude --dangerously-skip-permissions'

# Android SDK
export ANDROID_HOME="$HOME/Library/Android/sdk"
export PATH="$PATH:$ANDROID_HOME/platform-tools"

# Added by LM Studio CLI (lms)
export PATH="$PATH:/Users/sem/.lmstudio/bin"
# End of LM Studio CLI section
