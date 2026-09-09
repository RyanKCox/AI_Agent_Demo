import os
import asyncio
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.sessions import Session
from google.adk.runners import Runner
from google.genai import types
from typing import Optional


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

AGENT_MODEL = 'gemini-3.5-flash'
weather_agent = Agent(
    model=AGENT_MODEL,
    name='weather_agent',
    description="Provides weather information for the given cities.",
    instruction="You provide weather information to the user."
    "When the user asks for the weather from a city, use the 'get_weather' tool to retrieve the information."
    "If the tool returns an error, inform the user politely,"
                "if the tool is successful, present the report clearly",
    tools=["get_weather"],
)


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
def say_goodbye() -> str:
    return "Goodbye!"

greeting_agent = Agent(
    model=AGENT_MODEL,
    name='greeting_agent',
    instruction="You are the greeting agent. Your only task is to provide a friendly greeting to the user."
    "Use the 'say_hello' tool to generate the greeting "
    "If the user provides their name, make sure to pass it to the tool"
    "Do not engage in any other conversations or tasks",
    description="Handles simple greetings and hellos using the 'say_hello' tool",
    tools=["say_hello"],
)

farewall_agent = Agent(
    model=AGENT_MODEL,
    name='farewall_agent',
    description="handles simple farewell and goodbys using the 'say_goodbye' tool.",
    tools=["say_goodbye"],
    instruction="You are the farewell agent. Your only task is to provide a polite farewell message to the user"
    "Use the 'say_goodbye' tool to handle the farewell message when the user indicates they are leaving or ending the conversatiuon"
    "Do not engage in any other conversations or tasks"
)

root_agent = Agent(
    name="weather_agent_team",
    model=AGENT_MODEL,
    description="The main coordinator agent/ Handles weather requests and delegated greetings/farewells to specialists",
    instruction="You are the main weather agent coordinating a team. Your primary responsibility is to provide weather related information."
    "Use the 'get_weather' tool to retrieve the weather information."
    "You have specialized sub-agents:"
                "1. 'greetings_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for greetings"
                "2. 'farwell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for farewells"
                "Analyze the user's query. If it is a greeting delegate it to the greetings_agent, if it is a farewell delgate it to the 'farewell_agent'"
                "If it is a weather requiest, handle it yourself using the 'get_weather' tool."
                "For anything else respond appropriately or state you cannot handle the request",
    tools=["get_weather"],
    sub_agents=["greetings_agent", "farewell_agent"],
)