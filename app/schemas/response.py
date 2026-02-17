from pydantic import BaseModel

class AssociatedWord(BaseModel):
    word: str
    similarity: float

class AssociationResponse(BaseModel):
    query: str
    results: list[AssociatedWord]
    count: int

class AnalogySeed(BaseModel):
    positive: list[str] = []
    negative: list[str] = []
    topn: int = 10

class AnalogyResponse(BaseModel):
    positive: list[str]
    negative: list[str]
    results: list[AssociatedWord]
    count: int

class SimilarityResponse(BaseModel):
    word1: str
    word2: str
    similarity: float

class VocabInfoResponse(BaseModel):
    vocab_size: int
    vector_size: int
