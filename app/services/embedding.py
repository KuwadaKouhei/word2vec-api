import logging
import gensim
from app.core.config import settings

logger = logging.getLogger(__name__)

class EmbeddingService:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(EmbeddingService, cls).__new__(cls)
        return cls._instance

    def load_model(self):
        """モデルをロードする"""
        logger.info(f"モデルをロード中: {settings.CHIVE_MODEL_PATH}")
        try:
            self._model = gensim.models.KeyedVectors.load(settings.CHIVE_MODEL_PATH)
            logger.info(f"モデルロード完了 - 語彙数: {len(self._model)}")
        except Exception as e:
            logger.error(f"モデルロード失敗: {e}")
            raise e

    @property
    def model(self):
        """ロードされたモデルを返す"""
        if self._model is None:
            raise RuntimeError("モデルがロードされていません")
        return self._model

    def get_most_similar(self, word: str, topn: int = 10):
        """単語の類似語を取得"""
        if word not in self.model:
            return None
        return self.model.most_similar(word, topn=topn)

    def calculate_analogy(self, positive: list[str], negative: list[str], topn: int = 10):
        """アナロジー演算"""
        # 語彙チェック
        for w in positive + negative:
            if w not in self.model:
                raise ValueError(f"'{w}' はモデルの語彙に含まれていません。")

        return self.model.most_similar(
            positive=positive,
            negative=negative,
            topn=topn,
        )

    def get_similarity(self, word1: str, word2: str) -> float:
        """2単語間の類似度を取得"""
        if word1 not in self.model or word2 not in self.model:
             raise ValueError("単語がモデルの語彙に含まれていません。")
        return float(self.model.similarity(word1, word2))

    def check_vocab(self, word: str) -> bool:
        """単語が語彙に含まれているかチェック"""
        if self._model is None:
            return False
        return word in self.model

    def get_vocab_info(self) -> dict:
        """語彙情報を取得"""
        return {
            "vocab_size": len(self.model),
            "vector_size": self.model.vector_size
        }

embedding_service = EmbeddingService()
