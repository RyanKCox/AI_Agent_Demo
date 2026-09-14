from google.adk.agents.llm_agent import Agent
from google.adk.tools.tool_context import ToolContext
from google.genai.types import ThinkingConfig

from sub_agents import GreetingAgents
from sub_agents import WeatherAgents
from config import AGENT_MODEL
from guardrails import keyword_guardrail, tool_guardrail
from google.adk.planners import BuiltInPlanner

# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}
def get_last_city(tool_context: ToolContext) -> str:
    city =  tool_context.state.get("last_city_checked", "None")
    return city

planner = BuiltInPlanner(
    thinking_config=ThinkingConfig(
        include_thoughts=True,
        thinking_budget=256
    ),
)

root_agent = Agent(
    model=AGENT_MODEL,
    name='root_agent',
    planner=planner,
    description="Allows the user to check the time and weather in the given city..",
    instruction="You are a helpful assistant that tells the current time or weather in cities. "
                "Use the 'get_current_time' tool for giving the time."
                "Use the 'weather_agent' to fetch weather conditions for the user."
                "Start the conversation by greeting the user and asking for their name."
                "use the 'greeting_agent' to greet and respond to the user."
                "Use the 'farewell_agent' when the user signifies they are ending the conversation"
                "Use the 'get_last_city'; tool to fetch fron context the last city checked",
    tools=[get_current_time, get_last_city],
    sub_agents=[GreetingAgents.farewall_agent, GreetingAgents.greeting_agent, WeatherAgents.weather_agent],
    before_model_callback=keyword_guardrail.keyword_guardrail,
    before_tool_callback=tool_guardrail.block_paris_tool_guardrail
)