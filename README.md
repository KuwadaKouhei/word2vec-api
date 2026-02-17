# 連想語API

chiVe（Word2Vec学習済み日本語モデル）を用いた連想語API。  
キーワードを渡すと、意味的に近い単語をランキングで返します。

## 技術スタック

- **Python 3.12** + **FastAPI**
- **Gensim** - Word2Vec モデルの読み込み・類似語検索
- **chiVe v1.3** - 国立国語研究所 NWJC ベースの日本語単語ベクトル
- **Docker** - コンテナ化・デプロイ

## セットアップ

### 1. モデルのダウンロード

```bash
pip install -r requirements.txt

# mc90（軽量・推奨）をダウンロード
python download_model.py --model v1.3-mc90

# より高精度なモデルが必要な場合
# python download_model.py --model v1.3-mc5
```

### 2. モデルパスの確認

解凍後、`models/` 以下に `.kv` ファイルが配置されます。
パスを環境変数で指定します：

```bash
export CHIVE_MODEL_PATH="models/chive-1.3-mc90.kv"
```

> ⚠️ 解凍後のディレクトリ構造によっては
> `models/chive-1.3-mc90_gensim/chive-1.3-mc90.kv` のようにサブディレクトリが作られる場合があります。
> 実際のパスに合わせて調整してください。

### 3. サーバー起動

```bash
# 直接起動
uvicorn app.main:app --reload --port 8000

# Docker で起動
docker compose up --build
```

### 4. APIドキュメント確認

<http://localhost:8000/docs（Swagger> UI）

## APIエンドポイント

### `GET /associate` - 連想語取得

```bash
curl "http://localhost:8000/associate?word=猫&topn=5"
```

```json
{
  "query": "猫",
  "results": [
    {"word": "子猫", "similarity": 0.7823},
    {"word": "飼い猫", "similarity": 0.7456},
    {"word": "犬", "similarity": 0.7102},
    {"word": "仔猫", "similarity": 0.6987},
    {"word": "野良猫", "similarity": 0.6834}
  ],
  "count": 5
}
```

### `POST /analogy` - アナロジー演算

「王 - 男 + 女 = ?」のようなベクトル演算。

```bash
curl -X POST "http://localhost:8000/analogy" \
  -H "Content-Type: application/json" \
  -d '{"positive": ["王", "女性"], "negative": ["男性"], "topn": 5}'
```

### `GET /similarity` - 2単語の類似度

```bash
curl "http://localhost:8000/similarity?word1=東京&word2=大阪"
```

### `GET /vocab/check` - 語彙チェック

```bash
curl "http://localhost:8000/vocab/check?word=猫"
```

### `GET /vocab/info` - モデル情報

```bash
curl "http://localhost:8000/vocab/info"
```

## chiVe モデルの選び方

| モデル | 語彙数 | サイズ | 用途 |
|--------|--------|--------|------|
| v1.3-mc90 | 41万語 | 0.5GB | **開発・テスト・軽量運用（推奨）** |
| v1.3-mc30 | 76万語 | 0.8GB | バランス型 |
| v1.3-mc15 | 119万語 | 1.3GB | 高精度 |
| v1.3-mc5 | 253万語 | 2.9GB | 最大語彙・最高精度 |

## Cloud Run へのデプロイ

```bash
# Dockerイメージをビルド & プッシュ
gcloud builds submit --tag gcr.io/YOUR_PROJECT/association-api

# Cloud Run にデプロイ（メモリ2GB以上推奨）
gcloud run deploy association-api \
  --image gcr.io/YOUR_PROJECT/association-api \
  --memory 2Gi \
  --cpu 1 \
  --min-instances 1 \
  --max-instances 5 \
  --region asia-northeast1
```

> **注意**: `--min-instances 1` でコールドスタートを回避できますが、
> 常時課金されます。コスト重視なら `0` にしてください。

## ライセンス

- chiVe: [Apache License 2.0](https://github.com/WorksApplications/chiVe/blob/master/LICENSE)
- このAPI: MIT License
# word2vec-api
