"""Mysty - Fortune teller sub-agent."""

from google.adk.agents import Agent

from .prompt import MYSTY_INSTRUCTION
from .tools import get_fortune

mysty_agent = Agent(
    name="mysty",
    model="gemini-2.5-flash-native-audio-preview-12-2025",
    description="占い師。占いや運勢に関する質問を担当します。",
    instruction=MYSTY_INSTRUCTION,
    tools=[get_fortune],
)
