
from google.genai.types import ThinkingConfig
from google.adk.planners import BuiltInPlanner

AGENT_MODEL = 'gemini-3.5-flash-lite'
tag_celsius="Celsius"
tag_fahrenheit="Fahrenheit"
keywords_blocked=["BLOCKED","Restricted"]


AGENT_PLANNER = BuiltInPlanner(
    thinking_config=ThinkingConfig(
        include_thoughts=True,
        thinking_budget=256
    ),
)