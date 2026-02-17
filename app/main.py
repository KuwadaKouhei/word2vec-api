from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.services.embedding import embedding_service
from app.routers import association, analogy, vocabulary

@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリ起動時にモデルをロード"""
    # 起動時のモデルロード
    # 失敗してもアプリ自体は起動させるか、エラーで落とすかは要件次第だが、
    # ここではログを出して落とさない、あるいはService内でraiseされているので落ちる挙動になる
    try:
        embedding_service.load_model()
    except Exception:
        # ログはService内で出ている
        pass
    yield

app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(association.router)
app.include_router(analogy.router)
app.include_router(vocabulary.router)

@app.get("/", tags=["ヘルスチェック"])
async def root():
    return {"message": f"{settings.API_TITLE} is running", "model": settings.CHIVE_MODEL_PATH}
