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
│   │   │   ├── agent.py       # メインエージェント
│   │   │   ├── prompt.py      # メインプロンプト
│   │   │   └── sub_agents/    # サブエージェント（mysty, doctor）
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

### エージェント構成 (app/my_agent/)
- **モデル**: `gemini-2.5-flash-native-audio-preview-12-2025`（Google AI Studio Live API用）
- **メインエージェント**: 関西弁、親しみやすく親身に回答
- **ツール**: google_search
- **サブエージェント**:
  - `mysty`: 占い師（神秘的な口調、get_fortune ツール）
  - `doctor`: 博士（知的な口調、get_trivia + google_search ツール）

### 音声・対話設定 (app/main.py RunConfig)
- **音声**: Aoede（フレンドリーで温かい女性の声）
- **感情的対話**: `enable_affective_dialog=True`
- **プロアクティブ応答**: `proactivity=ProactivityConfig(proactive_audio=True)`

### セッション永続化 (完了)
- **バックエンド**: `DatabaseSessionService(db_url="sqlite+aiosqlite:///...")`
  - SQLite + aiosqlite で会話履歴をDBに保存
  - 依存関係: `sqlalchemy>=2.0.0`, `aiosqlite>=0.19.0`, `greenlet>=3.0.0`
- **フロントエンド**: `localStorage` でセッションIDを保持
- **Docker**: ボリュームマウントで `app/data/sessions.db` を永続化

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
9. [x] セッション永続化（Docker永続化含む）
   - DatabaseSessionService (SQLite + aiosqlite)
   - フロントエンドでlocalStorageにsessionId保存
   - docker.sh スクリプト作成
10. [x] カスタムツール作成
    - get_fortune(): 占い結果を返す
    - get_trivia(): 豆知識を返す
11. [x] サブエージェント実装
    - mysty: 占い師（神秘的な口調）
    - doctor: 博士（知的な口調）

## 次にやるべき作業（未着手）

- [ ] GitHubへの変更プッシュ（サブエージェント等の変更をコミット）
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
