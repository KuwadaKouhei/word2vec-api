FROM python:3.12-slim

WORKDIR /app

# 依存関係インストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションコピー
# アプリケーションコピー
COPY app/ app/
COPY download_model.py .

# モデルはビルド時 or ボリュームマウントで配置
# docker build 前に models/ にダウンロードしておく
COPY models/ models/

# 環境変数（解凍後のパスに合わせて変更）
ENV CHIVE_MODEL_PATH="models/chive-1.3-mc90.kv"

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
