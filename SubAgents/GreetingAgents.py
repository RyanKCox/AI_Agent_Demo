from google.adk.agents.llm_agent import Agent
from tools import GreetingTools
from config import AGENT_MODEL

greeting_agent = Agent(
    model=AGENT_MODEL,
    name='greeting_agent',
    instruction="You are the greeting agent. Your only task is to provide a friendly greeting to the user."
    "Use the 'say_hello' tool to generate the greeting "
    "If the user makes a greeting without giving their name, give a generic greeting and ask for their name. If a user "
                "gives their name first or is responding with their name, greet them using their name and ask 'How may I assist you?'"
    "Do not engage in any other conversations or tasks",
    description="Handles simple greetings and hellos using the 'say_hello' tool",
    tools=[GreetingTools.say_hello],
)

farewall_agent = Agent(
    model=AGENT_MODEL,
    name='farewall_agent',
    description="handles simple farewell and goodbys using the 'say_goodbye' tool.",
    tools=[GreetingTools.say_goodbye],
    instruction="You are the farewell agent. Your only task is to provide a polite farewell message to the user"
    "Use the 'say_goodbye' tool to handle the farewell message when the user indicates they are leaving or ending the "
                "conversation. If the user has provided their name pass it along to the tool."
    "Do not engage in any other conversations or tasks"
)