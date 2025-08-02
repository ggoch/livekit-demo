import datetime
from livekit.api.access_token import AccessToken, VideoGrants

# 設定 API 金鑰和密鑰
api_key = "devkey"
api_secret = "devsecret"

# 建立權限
grants = VideoGrants(
    room="test-room",
    room_join=True,
    room_create=True,
    ingress_admin=True,
)

# 建立 AccessToken 實例
token = AccessToken(api_key, api_secret)
token.with_identity("admin-client")
token.with_grants(grants)
token.with_ttl(datetime.timedelta(hours=10))  # 設定權杖有效期限為 10 小時

# 生成 JWT 權杖
jwt = token.to_jwt()

print("✅ 你的 JWT 權杖：")
print(jwt)

