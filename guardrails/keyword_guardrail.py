from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types
from typing import Optional
from config import keywords_blocked

def keyword_guardrail(callback_context: CallbackContext, llm_request: LlmRequest) -> Optional[LlmResponse]:
    """Inspect the latest user messsage for keywords. If found, blocks the LLM call and
    returns a predefined response. Otherwise, returns None."""
    agent_name = callback_context.agent_name
    last_user_msg = ""
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.parts[0].text:
                last_user_msg = content.parts[0].text
                break
    for keyword in keywords_blocked:
        if keyword.upper() in last_user_msg.upper():
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[types.Part(text=f"I cannot process this request because it contains the blocked keyword: {keyword}")]
                )
            )
    return None