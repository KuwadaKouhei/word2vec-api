from fastapi import APIRouter, HTTPException
from app.schemas.response import AnalogyResponse, AnalogySeed, AssociatedWord
from app.services.embedding import embedding_service

router = APIRouter(tags=["アナロジー"])

@router.post("/analogy", response_model=AnalogyResponse)
async def get_analogy(seed: AnalogySeed):
    """
    ベクトル演算による連想語を取得する（アナロジー）。

    例: positive=["王様", "女性"], negative=["男性"] → "女王" に近い単語
    """
    if not seed.positive:
        raise HTTPException(status_code=400, detail="positive に最低1つの単語が必要です")

    try:
        results_raw = embedding_service.calculate_analogy(
            positive=seed.positive,
            negative=seed.negative,
            topn=seed.topn,
        )
        results = [
            AssociatedWord(word=w, similarity=round(score, 4))
            for w, score in results_raw
        ]
        return AnalogyResponse(
            positive=seed.positive,
            negative=seed.negative,
            results=results,
            count=len(results),
        )
    except ValueError as e:
        # 語彙不足などのエラー
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"アナロジー演算中にエラーが発生しました: {str(e)}")
