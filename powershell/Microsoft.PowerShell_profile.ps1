# Initialize Oh My Posh + Theme
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH\star.omp.json" | Invoke-Expression
try {
    [Console]::InputEncoding = [System.Text.Encoding]::UTF8
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.UTF8Encoding]::new($false)
    chcp 65001 > $null
}
catch {}

Clear-Host

if (Get-Command fastfetch -ErrorAction SilentlyContinue) {
    fastfetch -c "$env:USERPROFILE/.config/fastfetch/config.jsonc"
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

# Import the Chocolatey Profile that contains the necessary code to enable
# tab-completions to function for `choco`.
# Be aware that if you are missing these lines from your profile, tab completion
# for `choco` will not function.
# See https://ch0.co/tab-completion for details.
$ChocolateyProfile = "$env:ChocolateyInstall\helpers\chocolateyProfile.psm1"
if (Test-Path($ChocolateyProfile)) {
    Import-Module "$ChocolateyProfile"
}
