from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext
from typing import Optional, Dict, Any

def block_paris_tool_guardrail(
        tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
) -> Optional[Dict]:
    tool_name = tool.name
    agent_name = tool_context.agent_name
    target_tool_name = "get_weather"
    blocked_city = "paris"

    if tool_name == target_tool_name:
        city_arg = args.get("city","")
        if city_arg and city_arg.lower() == blocked_city.lower():
            tool_context.state["city_blocked"] = True
            return {
                "status": "error",
                "error_message": f"Policy restriction for {city_arg} city is blocked."
            }
    return None