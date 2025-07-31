@echo off
:: Ensure Docker is started inside WSL before running the container
wsl -u root -e sh -c "docker start honeygain || docker run -d --name honeygain --restart unless-stopped honeygain/honeygain -tou-accept -email ms32-org@outlook.com -pass ms32147258369 -device HGSBDoc"
