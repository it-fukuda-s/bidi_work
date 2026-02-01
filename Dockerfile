FROM python:3.11-slim

WORKDIR /workspace

# 依存関係をコピーしてインストール
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# アプリケーションコードをコピー
COPY app/ ./app/

# 作業ディレクトリをappに変更
WORKDIR /workspace/app

# 環境変数（Cloud Runで上書き設定する）
ENV GOOGLE_GENAI_USE_VERTEXAI=FALSE

# ポート8080で起動
EXPOSE 8080
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
