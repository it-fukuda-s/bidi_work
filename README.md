# ADK Bidi-streaming リアルタイム音声AIエージェント

Google Agent Development Kit (ADK) を使用したリアルタイム音声AIアプリケーションです。

## 機能

- テキスト、音声、画像によるマルチモーダル入力
- リアルタイム音声応答
- 自然な割り込み対応
- Google Search ツール連携
- **サブエージェント**: 占い師（ミスティ）、博士（ドクター）
- **セッション永続化**: 会話履歴をSQLiteに保存
- **Aoede音声**: フレンドリーで温かい女性の声
- **感情的対話**: ユーザーの感情に応じた応答
- **プロアクティブ応答**: 積極的な提案とフォローアップ

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

### 3. Dockerで起動（推奨）

```bash
# 操作スクリプトで簡単起動
./docker.sh build   # イメージをビルド
./docker.sh start   # コンテナを起動

# ブラウザでアクセス
open http://localhost:8080
```

### 4. 使い方

- **普通の会話**: 何でも話しかけてください（関西弁で応答）
- **「占って」**: 占い師ミスティが運勢を占います
- **「豆知識教えて」**: 博士ドクターが面白い豆知識を教えます

## Docker操作スクリプト

`docker.sh` で簡単にDockerを操作できます：

```bash
./docker.sh build    # イメージをビルド
./docker.sh start    # コンテナを起動（セッションDB永続化付き）
./docker.sh stop     # コンテナを停止・削除
./docker.sh restart  # 再起動
./docker.sh logs     # ログをリアルタイム表示
./docker.sh status   # コンテナの状態確認
./docker.sh rebuild  # ビルド＆起動（フルデプロイ）
```

セッションDBは `app/data/sessions.db` に保存され、コンテナを再起動しても会話履歴が保持されます。

## ローカル開発

Dockerを使わない場合：

```bash
# 仮想環境を作成
python3 -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1

# 依存関係をインストール
pip install -e .

# サーバーを起動
cd app
python -m uvicorn main:app --host 0.0.0.0 --port 8080

# ブラウザでアクセス
open http://localhost:8080
```

## ディレクトリ構成

```
.
├── docker.sh           # Docker操作スクリプト
├── Dockerfile          # Dockerイメージ定義
├── pyproject.toml      # Python パッケージ設定
├── CLAUDE.md           # Claude Code用コンテキスト
└── app/
    ├── .env.template   # 環境変数テンプレート
    ├── main.py         # FastAPI サーバー（RunConfig含む）
    ├── data/           # セッションDB（gitignore対象）
    ├── my_agent/
    │   ├── agent.py    # メインエージェント
    │   ├── prompt.py   # メインプロンプト
    │   └── sub_agents/ # サブエージェント
    │       ├── mysty/  # 占い師（get_fortune ツール）
    │       └── doctor/ # 博士（get_trivia ツール）
    └── static/         # フロントエンド
```

## カスタマイズ

### エージェントの個性変更

`app/my_agent/prompt.py` を編集:

```python
MAIN_INSTRUCTION = """あなたは有能なAIアシスタントです。
回答は関西弁で、親しみやすく親身に回答してください。
...
"""
```

### サブエージェントの追加

1. `app/my_agent/sub_agents/` に新しいディレクトリを作成
2. `agent.py`, `prompt.py`, `tools/` を追加
3. `app/my_agent/agent.py` の `sub_agents` に追加

### 音声設定の変更

`app/main.py` の `RunConfig` を編集:

```python
run_config = RunConfig(
    speech_config=types.SpeechConfig(
        voice_config=types.VoiceConfig(
            prebuilt_voice_config=types.PrebuiltVoiceConfig(
                voice_name="Aoede"  # 声の種類を変更
            )
        )
    ),
    enable_affective_dialog=True,  # 感情的対話
    proactivity=types.ProactivityConfig(proactive_audio=True),  # プロアクティブ応答
)
```

#### 利用可能な声

| 声 | 特徴 |
|----|------|
| **Aoede** | フレンドリーで温かい女性（現在の設定） |
| Kore | 柔らかい女性 |
| Charon | プロフェッショナルな男性 |
| Puck | 明るく元気 |
| Leda, Fenrir, Orus, Zephyr | その他 |

詳細: [Gemini Live API Guide](https://ai.google.dev/gemini-api/docs/live-guide)

## Cloud Run へのデプロイ

```bash
gcloud run deploy bidi-demo \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_GENAI_USE_VERTEXAI=FALSE,GOOGLE_API_KEY=あなたのAPIキー" \
  --timeout 3600
```

## トラブルシューティング

### WebSocket接続エラー

- ブラウザで `http://localhost:8080` にアクセス（`0.0.0.0` ではなく）
- `./docker.sh logs` でサーバーログを確認

### セッションがリセットされる

- ブラウザを強制リロード（Cmd+Shift+R）してキャッシュをクリア
- `app/data/sessions.db` が存在するか確認

### 音声が認識されない

- ブラウザのマイク許可を確認
- 開発者ツール（F12）のConsoleでエラーを確認

## 参考リンク

- [ADK ドキュメント](https://google.github.io/adk-docs/)
- [Gemini Live API](https://ai.google.dev/gemini-api/docs/live)
- [Google AI Studio](https://aistudio.google.com/)
- [Live API対応モデル一覧](https://ai.google.dev/gemini-api/docs/models#live-models)
- [カスタムツール](https://google.github.io/adk-docs/tools-custom/)
- [マルチエージェント](https://google.github.io/adk-docs/agents/multi-agents/)

## 参考・ベース

このプロジェクトは [adk-streaming-guide](https://github.com/kazunori279/adk-streaming-guide) をベースにしています。
