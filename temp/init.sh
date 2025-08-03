
#!/bin/bash
# 啟用 Docker
systemctl enable docker
systemctl start docker

# 清理舊容器（若有）
docker rm -f portainer || true

# 拉取最新版 Portainer CE
docker pull portainer/portainer-ce:latest

# 執行 Portainer 容器（用 9443 管理介面）
docker run -d \
  --name portainer \
  --restart=always \
  -p 9443:9443 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest

# 建立網路（如果尚未存在）
docker network create abp-network

# 建立 volume（如果尚未存在）

docker volume create nginx-proxy-manager-data
docker volume create nginx-proxy-manager-letsencrypt

# 執行容器
docker run -d \
  --name nginx-proxy-manager \
  --restart always \
  -v nginx-proxy-manager-data:/data \
  -v nginx-proxy-manager-letsencrypt:/etc/letsencrypt \
  -p 80:80 \
  -p 443:443 \
  -p 81:81 \
  jc21/nginx-proxy-manager:latest

# 建立外部服務Volume
docker volume create livekit-config
docker volume create livekit-ingress-config

# 刪除腳本自身
rm -f /tmp/init.sh

# 重開機生效
reboot