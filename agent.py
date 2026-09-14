from google.adk.agents.llm_agent import Agent
from typing import Optional
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types


# Mock tool implementation
def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city."""
    return {"status": "success", "city": city, "time": "10:30 AM"}

def get_weather(city:str) -> dict:
    """Retrieve the current weather report for a specifed city.

    Args:
        citi (str) : the name of the city

    Returns:
        dict: A dictionary containing the weather information.
        Includes a 'status' key (success or error)
        If 'success', includes a 'report' key with weather details.
        If 'error', includes an 'error_message' key.
    """
    city_normalized = city.lower().replace(" ", "")

    #Mock weather
    mock_weather_db = {
        "newyork" : {"status": "success", "report": "The weather in New York is sunny"},
        "london" : {"status": "success", "report": "Its a cloudy day in London"},
        "tokyo" : {"status": "success", "report": "In Tokyo it is raining!"}
    }

    if city_normalized in mock_weather_db:
        return mock_weather_db[city_normalized]
    else:
        return {"status": "error", "error_message": "I cant fetch that right now"}


AGENT_MODEL = 'gemini-3.5-flash-lite'

def say_hello(name: Optional[str] = None) -> str:
    """Provides a simple greeting, if name is provided it will be used
    Args:
        name(str, option): The name of the person to greet. Defaults to a generic greeting if not given.

    Returns:
        str: A friendly greeting message
        """
    if name:
        greeting = f"Hello, {name}!"
    else:
        greeting = "Hello There!"
    return greeting
def say_goodbye(name: Optional[str] = None) -> str:
    if name:
        return f"Goodbye, {name}!"
    else :
        return "Goodbye!"

greeting_agent = Agent(
    model=AGENT_MODEL,
    name='greeting_agent',
    instruction="You are the greeting agent. Your only task is to provide a friendly greeting to the user."
    "Use the 'say_hello' tool to generate the greeting "
    "If the user makes a greeting without giving their name, give a generic greeting and ask for their name. If a user "
                "gives their name first or is responding with their name, greet them using their name and ask 'How may I assist you?'"
    "Do not engage in any other conversations or tasks",
    description="Handles simple greetings and hellos using the 'say_hello' tool",
    tools=[say_hello],
)

farewall_agent = Agent(
    model=AGENT_MODEL,
    name='farewall_agent',
    description="handles simple farewell and goodbys using the 'say_goodbye' tool.",
    tools=[say_goodbye],
    instruction="You are the farewell agent. Your only task is to provide a polite farewell message to the user"
    "Use the 'say_goodbye' tool to handle the farewell message when the user indicates they are leaving or ending the "
                "conversation. If the user has provided their name pass it along to the tool."
    "Do not engage in any other conversations or tasks"
)

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
    tools=[get_current_time, get_weather],
    sub_agents=[farewall_agent, greeting_agent],
)