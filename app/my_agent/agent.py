"""Agent definition for the bidi-workshop.

Live API対応モデルの最新情報:
- Google AI Studio: https://ai.google.dev/gemini-api/docs/models#live-models
- Vertex AI: https://cloud.google.com/vertex-ai/generative-ai/docs/live-api#supported-models
"""

from google.adk.agents import Agent
from google.adk.tools import google_search

# Define the agent
# モデル名は変更される可能性があります。上記リンクで最新を確認してください。
agent = Agent(
    name="workshop_agent",
    model="gemini-2.5-flash-native-audio-preview-12-2025",  # Google AI Studio Live API用
    instruction="""あなたは有能なAIアシスタントです。ユーザーの質問に答え、必要に応じてGoogle検索ツールを使用して最新情報を取得します。
    回答は関西弁で、親しみやすく親身に回答してください。
    """,
    tools=[google_search],
)
