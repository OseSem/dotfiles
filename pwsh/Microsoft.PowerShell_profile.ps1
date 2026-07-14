# --- BEGIN user-env merge (added for SSH/service sessions) ---
# Sessions spawned by a service (NetBird SSH, OpenSSH, scheduled tasks) inherit only the
# machine environment, so user-scope variables and PATH entries are missing. Merge them in.
# No-op in interactive sessions, where they are already present.
if (-not $env:__USER_ENV_MERGED) {
    foreach ($kv in [Environment]::GetEnvironmentVariables('User').GetEnumerator()) {
        if ($kv.Key -ne 'PATH' -and -not (Test-Path "Env:\$($kv.Key)")) {
            Set-Item "Env:\$($kv.Key)" $kv.Value
        }
    }
    $userPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
    if ($userPath) {
        $current = $env:PATH -split ';' | Where-Object { $_ }
        $missing = $userPath -split ';' | Where-Object { $_ } |
            ForEach-Object { [Environment]::ExpandEnvironmentVariables($_) } |
            Where-Object { $_ -and $current -notcontains $_ }
        if ($missing) { $env:PATH = (($current + $missing) -join ';') }
    }
    $env:__USER_ENV_MERGED = '1'
}
# --- END user-env merge ---

# Initialize Oh My Posh + Theme
oh-my-posh init pwsh --config "$env:LOCALAPPDATA\Programs\oh-my-posh\themes\star.omp.json" | Invoke-Expression
try {
    [Console]::InputEncoding = [System.Text.Encoding]::UTF8
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.UTF8Encoding]::new($false)
    chcp 65001 > $null
}
catch {}


# Tell Windows Terminal the current directory (for split pane inheritance)
[System.Environment]::SetEnvironmentVariable("PROMPT_COMMAND", "", "Process")
$global:__OriginalPrompt = $function:prompt
function prompt {
    $loc = $executionContext.SessionState.Path.CurrentLocation
    [Console]::Write("`e]9;9;$loc`e\")
    & $global:__OriginalPrompt
}

# Zoxide integration
Invoke-Expression (& { (zoxide init powershell | Out-String) })

# Add latest uv-installed Python to PATH
$uvPythonRoot = "$env:APPDATA\uv\python"
if (Test-Path $uvPythonRoot) {
    $latestPython = Get-ChildItem $uvPythonRoot -Directory |
        Where-Object { $_.Name -match 'cpython-(\d+\.\d+\.\d+)' } |
        Sort-Object { [version]($_.Name -replace '^cpython-(\d+\.\d+\.\d+).*','$1') } -Descending |
        Select-Object -First 1
    if ($latestPython) {
        $env:PATH = "$($latestPython.FullName);$($latestPython.FullName)\Scripts;$env:PATH"
    }
}
Set-Alias py python

if (-not [Console]::IsOutputRedirected) { Clear-Host }
if (-not [Console]::IsOutputRedirected -and (Get-Command fastfetch -ErrorAction SilentlyContinue)) {
    fastfetch -c "$env:USERPROFILE/.config/fastfetch/config.jsonc"
}

# Initialize GitHub Copilot
. "$PSScriptRoot\gh-copilot.ps1"

# Make a shortcut to activate venv
function venv {
    & "$PWD\.venv\Scripts\Activate.ps1"
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
(& uv generate-shell-completion powershell) | Out-String | Invoke-Expression
(& uvx --generate-shell-completion powershell) | Out-String | Invoke-Expression
