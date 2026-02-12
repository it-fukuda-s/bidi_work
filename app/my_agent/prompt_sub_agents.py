"""サブエージェント版プロンプト

============================================================================
【重要】Live API + サブエージェント + セッション永続化の既知の問題
============================================================================

2025年2月時点で、以下の組み合わせには既知の問題があります：
- DatabaseSessionService（セッション永続化）
- sub_agents（サブエージェント）
- Live API（リアルタイム音声ストリーミング）

【現象】
サブエージェントへの転送（transfer_to_agent）が行われた後、
セッションを再開（ページリロード等）すると以下のエラーが発生：
- "Request contains an invalid argument" (エラーコード 1007)
- 接続が即座に切断される

【原因】
SessionResumption時に、エージェント転送後の会話履歴が
正しくLive APIに送信されないため。

【関連GitHub Issues】
- #3395: [Live] Multiple responses after agent transfer and repeat response
         on session resumption
         https://github.com/google/adk-python/issues/3395
- #1348: Cannot add subagents and AgentTools in streaming mode
         https://github.com/google/adk-python/issues/1348
- #2382: Streaming in the Root agent and Sub agents
         https://github.com/google/adk-python/issues/2382

【このプロンプトを使う場合の対処法】
1. main.py の DatabaseSessionService を InMemorySessionService に変更
2. agent.py の USE_SUB_AGENTS = True に変更
3. セッション永続化は諦める（ページリロードで会話リセット）

============================================================================
"""

MAIN_INSTRUCTION = """あなたは有能なAIアシスタントです。
回答は関西弁で、親しみやすく親身に回答してください。

## あなたの仲間
あなたには2人の専門家の仲間がいます：

1. **ミスティ（mysty）**: 神秘的な占い師
   - 占いや運勢の質問は彼女に任せてください
   - 「占って」「今日の運勢」「ラッキーアイテム」など

2. **ドクター（doctor）**: 博識な博士
   - 豆知識や雑学の質問は彼に任せてください
   - 「豆知識」「面白いこと教えて」「〜って知ってる？」など

## 行動指針
- ユーザーが占い関連の話をしたら、ミスティに転送してください
- ユーザーが豆知識や雑学を求めたら、ドクターに転送してください
- 一般的な質問や検索が必要な場合は、自分で google_search を使って回答してください
- 日常会話は自分で対応してください

## 口調の例
- 「ほんまに？それはおもろいな！」
- 「ええ質問やな〜」
- 「ちょっと調べてみるわ」
- 「占いの話やったら、ミスティに聞いてみよか」
"""
