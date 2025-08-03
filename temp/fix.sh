docker run -d \
  --name nginx-proxy-manager \
  --restart always \
  -v nginx-proxy-manager-data:/data \
  -v nginx-proxy-manager-letsencrypt:/etc/letsencrypt \
  --network host \
  jc21/nginx-proxy-manager:latest

  # -p 80:80 \
  # -p 443:443 \
  # -p 81:81 \