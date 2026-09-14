from google.adk.agents.llm_agent import Agent
from tools import WeatherTools
from SubAgents import GreetingAgents
from config import AGENT_MODEL

root_agent = Agent(
    model=AGENT_MODEL,
    name='root_agent',
    description="Allows the user to check the time and weather in the given city..",
    instruction="You are a helpful assistant that tells the current time or weather in cities. "
                "Use the 'get_current_time' tool for giving the time."
                "Use the 'get_weather' tool for giving the weather."
                "Start the conversation by greeting the user and asking for their name."
                "use the 'greeting_agent' to greet and respond to the user."
                "Use the 'farewell_agent' when the user signifies they are ending the conversation",
    tools=[WeatherTools.get_current_time, WeatherTools.get_weather],
    sub_agents=[GreetingAgents.farewall_agent, GreetingAgents.greeting_agent],
)