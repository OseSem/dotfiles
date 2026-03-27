# Initialize Oh My Posh + Theme
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\star.omp.json" | Invoke-Expression

# Tell Windows Terminal the current directory (for split pane inheritance)
[System.Environment]::SetEnvironmentVariable("PROMPT_COMMAND", "", "Process")
$global:__OriginalPrompt = $function:prompt
function prompt {
    $loc = $executionContext.SessionState.Path.CurrentLocation
    [Console]::Write("`e]9;9;$loc`e\")
    & $global:__OriginalPrompt
}

# Initialize GitHub Copilot
. "C:\Users\info\OneDrive\Documenten\WindowsPowerShell\gh-copilot.ps1"

# Make a shortcut to activate venv
function venv {
    & "$PWD\.venv\Scripts\Activate.ps1"
}

# Make a shortcut to activate venv
function pym {
    python "$PWD\main.py"
}

# Claude with Dangerously Skip Permissions
function cly { claude --dangerously-skip-permissions @args }
function cc { claude --dangerously-skip-permissions @args }

# Set the right claude code binary
Set-Alias claude "$env:USERPROFILE\.local\bin\claude.exe"

# Import the Chocolatey Profile that contains the necessary code to enable
# tab-completions to function for `choco`.
# Be aware that if you are missing these lines from your profile, tab completion
# for `choco` will not function.
# See https://ch0.co/tab-completion for details.
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
    Import-Module "$ChocolateyProfile"
}
