# ADK Bidi-streaming リアルタイム音声AIエージェント

Google Agent Development Kit (ADK) を使用したリアルタイム音声AIアプリケーションです。

## 機能

- テキスト、音声、画像によるマルチモーダル入力
- リアルタイム音声応答
- 自然な割り込み対応
- Google Search ツール連携

## クイックスタート

### 1. APIキーを取得

1. [Google AI Studio](https://aistudio.google.com/) にアクセス
2. 「Get API key」でAPIキーを取得

### 2. 環境変数を設定

```bash
cd app
cp .env.template .env
```

`.env` ファイルを編集:
```env
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=あなたのAPIキー
```

### 3. 依存関係をインストール

```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
pip install -e .
```

### 4. サーバーを起動

```bash
cd app
python -m uvicorn main:app --host 0.0.0.0 --port 8080
```

### 5. ブラウザでアクセス

http://localhost:8080

## Dockerで起動

```bash
# イメージをビルド
docker build -t bidi-app .

# コンテナを起動
docker run -d -p 8080:8080 --env-file app/.env --name bidi-container bidi-app

# ブラウザでアクセス
# http://localhost:8080

# 停止する場合
docker stop bidi-container && docker rm bidi-container
```

## カスタマイズ

エージェントの個性を変更するには `app/my_agent/agent.py` を編集してください。

```python
agent = Agent(
    name="my_custom_agent",
    model="gemini-2.5-flash-native-audio-preview-12-2025",  # 最新モデル名を確認
    instruction="""あなたは関西弁で話すAIアシスタントです。
    フレンドリーで親しみやすい話し方をしてください。
    """,
    tools=[google_search],
)
```

## ディレクトリ構成

```
.
├── pyproject.toml      # Python パッケージ設定
├── Dockerfile          # Cloud Run デプロイ用
└── app/
    ├── .env.template   # 環境変数テンプレート
    ├── main.py         # FastAPI サーバー
    ├── my_agent/
    │   └── agent.py    # エージェント定義
    └── static/         # フロントエンド
```

## Cloud Run へのデプロイ

```bash
gcloud run deploy bidi-demo \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=FALSE,GOOGLE_API_KEY=あなたのAPIキー" \
  --timeout 3600
```

## 参考リンク

- [ADK ドキュメント](https://google.github.io/adk-docs/)
- [Gemini Live API](https://ai.google.dev/gemini-api/docs/live)
- [Google AI Studio](https://aistudio.google.com/)
- [Live API対応モデル一覧](https://ai.google.dev/gemini-api/docs/models#live-models) - モデル名の最新情報

## 参考・ベース

このプロジェクトは [adk-streaming-guide](https://github.com/kazunori279/adk-streaming-guide) をベースにしています。
