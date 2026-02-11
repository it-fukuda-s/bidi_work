"""Doctor - Trivia expert sub-agent."""

from google.adk.agents import Agent
from google.adk.tools import google_search

from .prompt import DOCTOR_INSTRUCTION
from .tools import get_trivia

doctor_agent = Agent(
    name="doctor",
    model="gemini-2.5-flash-native-audio-preview-12-2025",
    description="博士。豆知識や「教えて」系の質問を担当します。",
    instruction=DOCTOR_INSTRUCTION,
    tools=[get_trivia, google_search],
)
