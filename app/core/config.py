from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    CHIVE_MODEL_PATH: str = "models/chive-1.3-mc90.kv"
    API_TITLE: str = "連想語API"
    API_DESCRIPTION: str = "chiVe (Word2Vec) を用いた日本語連想語API。キーワードから意味的に近い単語を返します。"
    API_VERSION: str = "1.0.0"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
