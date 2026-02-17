from fastapi import APIRouter, Query, HTTPException
from app.schemas.response import SimilarityResponse, VocabInfoResponse
from app.services.embedding import embedding_service

router = APIRouter()

@router.get("/similarity", response_model=SimilarityResponse, tags=["類似度"])
async def get_similarity(
    word1: str = Query(..., description="単語1"),
    word2: str = Query(..., description="単語2"),
):
    """
    2つの単語間のコサイン類似度を計算する。
    """
    try:
        similarity = embedding_service.get_similarity(word1, word2)
        return SimilarityResponse(
            word1=word1, word2=word2, similarity=round(similarity, 4)
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"類似度計算中にエラーが発生しました: {str(e)}")

@router.get("/vocab/check", tags=["語彙"])
async def check_vocab(word: str = Query(..., description="チェックする単語")):
    """単語がモデルの語彙に含まれているかチェックする。"""
    exists = embedding_service.check_vocab(word)
    return {"word": word, "exists": exists}

@router.get("/vocab/info", response_model=VocabInfoResponse, tags=["語彙"])
async def vocab_info():
    """モデルの語彙情報を取得する。"""
    info = embedding_service.get_vocab_info()
    return VocabInfoResponse(**info)
