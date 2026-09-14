import asyncio
from dotenv import load_dotenv; load_dotenv()
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent
from config import tag_celsius, tag_fahrenheit

APP_NAME="AI Tutorial App"
USER_ID="user1"
SESSION_ID="session1"
initial_state={
    "user_prefered_temperature_unit":tag_fahrenheit,
}

RESET = "\033[0m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
MAGENTA = "\033[35m"
GREEN = "\033[32m"
GREY = "\033[90m"

def color(text,code):
    return f"{code}{text}{RESET}"

def print_event(event, main_agent:str):
    """Show text, tool calls/results, and sub-agent transfers"""
    author = getattr(event, "author", "?")
    for call in event.get_function_calls():
        if call.name == "transfer_to_agent":
            target = (call.args or {}).get("agent_name", "?")
            print(color(f"  --> {author}: transfering to sub-agent: {target}", CYAN))
        else:
            print(color(f"  --> {author}: calling tool: {call.name}({dict(call.args or {})})",GREEN))
    for resp in event.get_function_responses():
        print(color(f"  <-- {author} tool '{resp.name}' returned: {resp.response}",YELLOW))

    for part in event.content.parts:
        if getattr(part, "thought", False) and part.text:
            print(color(f"{author} thinking: {part.text.strip()}",GREY))
        elif part.text and part.text.strip():
            print(f"[{main_agent}]: {part.text}")


async def call_agent_async(runner: Runner, query: str) -> None:
    """Send one user turn and print the agents final response."""
    content = types.Content(role="user", parts=[types.Part(text=query)])

    async for event in runner.run_async(
        user_id=USER_ID, session_id=SESSION_ID,new_message=content
    ):
        print_event(event, "Tutorial Bot")

async def main():
    session_service = InMemorySessionService()
    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initial_state,
    )
    runner = Runner(
        app_name=APP_NAME,
        agent=root_agent,
        session_service=session_service,
    )

    print("Type 'exit' to quit")
    while True:
        query = input("[user]: ")
        if not query.strip():
            continue
        if query == "exit":
            break
        await call_agent_async(runner,query)

if __name__ == "__main__":
    asyncio.run(main())