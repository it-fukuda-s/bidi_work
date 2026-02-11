"""Main agent definition for the bidi-workshop.

Live API対応モデルの最新情報:
- Google AI Studio: https://ai.google.dev/gemini-api/docs/models#live-models
- Vertex AI: https://cloud.google.com/vertex-ai/generative-ai/docs/live-api#supported-models

サブエージェント構成:
- メイン: 関西弁のアシスタント（google_search）
- ミスティ: 占い師（fortune tool）
- ドクター: 博士（trivia tool + google_search）
"""

from google.adk.agents import Agent
from google.adk.tools import google_search

from .prompt import MAIN_INSTRUCTION
from .sub_agents import doctor_agent, mysty_agent

# Define the agent
# モデル名は変更される可能性があります。上記リンクで最新を確認してください。
agent = Agent(
    name="workshop_agent",
    model="gemini-2.5-flash-native-audio-preview-12-2025",  # Google AI Studio Live API用
    instruction=MAIN_INSTRUCTION,
    tools=[google_search],
    sub_agents=[mysty_agent, doctor_agent],
)
