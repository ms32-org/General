@echo off
wsl -u root -e sh -c "docker start honeygain || docker run -d --name honeygain --restart unless-stopped --device /dev/net/tun --cap-add NET_ADMIN honeygain/honeygain -tou-accept -email ms32-org@outlook.com -pass ms32147258369 -device HGDoc"
