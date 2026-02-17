from fastapi import APIRouter, Query, HTTPException
from app.schemas.response import AssociationResponse, AssociatedWord
from app.services.embedding import embedding_service

router = APIRouter(tags=["連想語"])

@router.get("/associate", response_model=AssociationResponse)
async def get_associations(
    word: str = Query(..., description="連想元のキーワード", examples=["猫"]),
    topn: int = Query(10, ge=1, le=100, description="取得する連想語の数"),
):
    """
    キーワードから連想語を取得する。

    chiVeモデル（Word2Vec）で学習された単語ベクトルの類似度に基づき、
    意味的に近い単語をランキングで返します。
    """
    if not embedding_service.check_vocab(word):
        raise HTTPException(
            status_code=404,
            detail=f"'{word}' はモデルの語彙に含まれていません。別の表記を試してください。",
        )

    try:
        similar_words = embedding_service.get_most_similar(word, topn=topn)
        results = [
            AssociatedWord(word=w, similarity=round(score, 4))
            for w, score in similar_words
        ]
        return AssociationResponse(query=word, results=results, count=len(results))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"類似語の取得中にエラーが発生しました: {str(e)}")
