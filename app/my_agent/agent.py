"""Main agent definition for the bidi-workshop.

Live API対応モデルの最新情報:
- Google AI Studio: https://ai.google.dev/gemini-api/docs/models#live-models
- Vertex AI: https://cloud.google.com/vertex-ai/generative-ai/docs/live-api#supported-models

設定フラグ USE_SUB_AGENTS で構成を切り替え可能:
- False: シンプル版（セッション永続化OK）
- True:  サブエージェント版（セッション永続化NG、詳細は prompt_sub_agents.py 参照）
"""

from google.adk.agents import Agent
from google.adk.tools import google_search

# =============================================================================
# 設定フラグ
# =============================================================================
# True:  サブエージェント版（占い師ミスティ、博士ドクター）
#        ※ DatabaseSessionService との併用で問題あり（GitHub Issue #3395）
# False: シンプル版（セッション永続化OK）
USE_SUB_AGENTS = False

# =============================================================================
# エージェント構成
# =============================================================================
if USE_SUB_AGENTS:
    # サブエージェント版
    # 注意: この構成では DatabaseSessionService を使うとセッション再開時にエラーが発生します
    #       詳細は prompt_sub_agents.py のコメントを参照
    from .prompt_sub_agents import MAIN_INSTRUCTION
    from .sub_agents import doctor_agent, mysty_agent

    agent = Agent(
        name="workshop_agent",
        model="gemini-2.5-flash-native-audio-preview-12-2025",
        instruction=MAIN_INSTRUCTION,
        tools=[google_search],
        sub_agents=[mysty_agent, doctor_agent],
    )
else:
    # シンプル版（現在使用中）
    from .prompt_simple import MAIN_INSTRUCTION

    agent = Agent(
        name="workshop_agent",
        model="gemini-2.5-flash-native-audio-preview-12-2025",
        instruction=MAIN_INSTRUCTION,
        tools=[google_search],
    )
