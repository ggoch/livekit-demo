### 使用說明

1. **Python 環境配置**  
   請先參考 `requirements` 文件完成 Python 環境的初始配置，並安裝相關套件。

2. **生成 LiveKit Token**  
   執行 `tools` 資料夾下的 `get-token.py` 腳本，生成 `liveKitToken`，並將其更新至以下檔案：  
   - `create-ingress.http`  
   - `demo-web.html`

3. **啟動 LiveKit Docker 容器**  
   執行 `etc` 資料夾下的 `run.ps1` 腳本，啟動 LiveKit 相關的 Docker 容器。  
   **注意：** 第一次啟動時，`ffmpeg` 可能無法正常運作。請使用 `create-ingress` 取得 `stream-key`，並修改以下配置後重新啟動：

   ```yaml
   entrypoint: >
     ffmpeg -re -stream_loop -1 -i /videos/8.mp4
            -vf "scale=1280:720"
            -pix_fmt yuv420p -r 25 -g 50 -keyint_min 50 -sc_threshold 0
            -c:v libx264 -preset veryfast -tune zerolatency -bf 0
            -c:a aac -b:a 128k
            -f flv rtmp://livekit-ingress:1935/live/{{stream-key}}
   ```

4. **啟動 Demo 頁面**  
   使用 VS Code 的 Live Server 擴充套件啟動 `demo-web.html`，打開後點擊「加入房間」即可看到影像。
