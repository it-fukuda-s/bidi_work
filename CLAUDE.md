# CLAUDE.md

このファイルはClaude Codeがリポジトリ操作時に自動読み込みするコンテキストです。

## プロジェクト概要

ADK (Agent Development Kit) Bidi-streaming を使用したリアルタイム音声AIアプリケーション。
Google AI Studio の Gemini Live API を利用。

- **GitHub**: https://github.com/it-fukuda-s/bidi_work.git
- **ベース**: [adk-streaming-guide](https://github.com/kazunori279/adk-streaming-guide)

## プロジェクト構成

```
/Users/pei/Desktop/develop/bidi_work/
├── git/                        # ← このリポジトリ（gitルート）
│   ├── app/
│   │   ├── main.py            # FastAPI サーバー（RunConfig含む）
│   │   ├── my_agent/
│   │   │   └── agent.py       # エージェント定義
│   │   ├── static/            # フロントエンド
│   │   ├── .env               # 環境変数（gitignore対象）
│   │   └── .env.template      # 環境変数テンプレート
│   ├── pyproject.toml         # Python パッケージ設定
│   ├── Dockerfile             # Docker/Cloud Run デプロイ用
│   └── CLAUDE.md              # 本ファイル
├── terminal/                   # 作業管理
│   ├── issue/                 # 作業依頼
│   └── cloude_work_step/      # 作業進捗・手順
├── intelligence/              # ドキュメント
│   ├── setup/環境構築手順.md
│   └── customization/カスタマイズガイド.md
├── presentation/              # 発表資料
└── sample/                    # 参考リポジトリ（adk-streaming-guide）
```

## 現在の設定

### エージェント (app/my_agent/agent.py)
- **モデル**: `gemini-2.5-flash-native-audio-preview-12-2025`（Google AI Studio Live API用）
- **インストラクション**: 関西弁、親しみやすく親身に回答
- **ツール**: google_search

### 音声・対話設定 (app/main.py RunConfig)
- **音声**: Aoede（フレンドリーで温かい女性の声）
- **感情的対話**: `enable_affective_dialog=True`
- **プロアクティブ応答**: `proactivity=ProactivityConfig(proactive_audio=True)`

### セッション永続化 (実装済み・動作確認中)
- **バックエンド**: `DatabaseSessionService(db_url="sqlite+aiosqlite:///...")`
  - SQLite + aiosqlite で会話履歴をDBに保存
  - 依存関係: `sqlalchemy>=2.0.0`, `aiosqlite>=0.19.0` を pyproject.toml に追加済み
- **フロントエンド**: `localStorage` でセッションIDを保持
  - `app/static/js/app.js` を修正済み
  - リロード時に同じセッションIDを使用
- **注意**: ブラウザキャッシュが残っている場合、`Cmd+Shift+R` で強制リロードが必要

### デプロイ
- **Docker操作スクリプト**: `./docker.sh {build|start|stop|restart|logs|status|rebuild}`
- **ポート**: 8080
- **アクセス**: http://localhost:8080
- **セッションDB**: `app/data/sessions.db`（ボリュームマウントで永続化）

## 完了済みの作業

1. [x] 基本環境構築（FastAPI + ADK Bidi-streaming）
2. [x] Docker対応
3. [x] GitHubプッシュ
4. [x] インストラクション変更（関西弁の個性）
5. [x] 音声設定（Aoede - 女性声）
6. [x] 感情的対話の有効化
7. [x] プロアクティブ応答の有効化
8. [x] 音声変更の動作確認（Charon男性声 ↔ Aoede女性声）
9. [x] セッション永続化（実装済み・動作確認中）
   - DatabaseSessionService (SQLite + aiosqlite)
   - フロントエンドでlocalStorageにsessionId保存
   - ブラウザキャッシュクリア後に動作確認が必要

## 次にやるべき作業（未着手）

### 直近の課題
- [ ] **セッション永続化の動作確認**: ブラウザで `Cmd+Shift+R` 強制リロード後に確認

### カスタマイズ作業（ユーザーの要望順）
- [ ] **カスタムツールの作成**: agent.pyに独自ツールを追加
  - 参考: カスタマイズガイド レベル3
  - Python関数をtools=[]に渡すだけで登録可能
- [ ] **サブエージェントの実装**: 複数エージェントの連携
  - `sub_agents=[]` パラメータで定義
  - 各サブエージェントに異なる音声(speech_config)を設定可能

### その他
- [ ] GitHubへの変更プッシュ（音声設定等の変更をコミット）
- [ ] 発表資料の更新
- [ ] Cloud Run デプロイテスト

## 技術メモ

### 利用可能な音声（Live API）
| 声 | 特徴 |
|----|------|
| **Aoede** | フレンドリーで温かい女性（現在の設定） |
| Kore | 柔らかい女性 |
| Charon | プロフェッショナルな男性 |
| Puck | 明るく元気 |
| Leda, Fenrir, Orus, Zephyr | その他 |

### Native Audioモデル専用機能
- `enable_affective_dialog` - 感情的対話
- `proactivity` - プロアクティブ応答
- `speech_config` - 音声設定

### 参考ドキュメント（sampleディレクトリ）
- `sample/adk-streaming-guide-main/docs/part4.md` - RunConfig詳細
- `sample/adk-streaming-guide-main/docs/part5.md` - 音声/感情的対話/VAD
- `sample/adk-streaming-guide-main/docs/part1.md` - アーキテクチャ全体

### 参考リンク
- ADK ドキュメント: https://google.github.io/adk-docs/
- Gemini Live API: https://ai.google.dev/gemini-api/docs/live
- Live API対応モデル: https://ai.google.dev/gemini-api/docs/models#live-models
- カスタムツール: https://google.github.io/adk-docs/tools-custom/
- マルチエージェント: https://google.github.io/adk-docs/agents/
