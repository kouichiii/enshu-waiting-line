from fastapi import FastAPI
from api.endpoints import receive, fetch
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() #fastapiのサーバを作成

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # セキュリティが必要な場合は特定のIPのみ許可
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(receive.router, prefix="/api") #/api/endpoints/receive.pyにアクセス時の処理がある
app.include_router(fetch.router, prefix="/api")