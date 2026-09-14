from google.adk.agents.llm_agent import Agent
from tools import WeatherTools
from config import AGENT_MODEL


weather_agent = Agent(
    model=AGENT_MODEL,
    name='weather_agent',
    instruction="You are the weather agent (state-aware). Use the get_weather tool to "
                "fetch weather information for the city provided by the user.",
    description="Handles fetching of weather data for user input",
    tools=[WeatherTools.get_weather],
)