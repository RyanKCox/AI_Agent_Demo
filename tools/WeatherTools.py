from google.adk.tools.tool_context import ToolContext
from config import tag_celsius
from config import tag_fahrenheit

# Mock weather
mock_weather_db = {
    "newyork": {"condition": "The weather in New York is sunny",
                "temp_c": 25},
    "london": {"condition": "Its a cloudy day in London",
               "temp_c": 15},
    "tokyo": {"condition": "In Tokyo it is raining",
              "temp_c": 18}
}

def get_weather(city:str, tool_context:ToolContext) -> dict:
    """Retrieve the current weather report for a specified city.

    Args:
        citi (str) : the name of the city

    Returns:
        dict: A dictionary containing the weather information.
        Includes a 'status' key (success or error)
        If 'success', includes a 'report' key with weather details.
        If 'error', includes an 'error_message' key.
    """
    prefered_unit = tool_context.state.get("user_prefered_temperature_unit",'Celsius')
    city_normalized = city.lower().replace(" ", "")


    if city_normalized in mock_weather_db:
        data = mock_weather_db[city_normalized]
        temp_c = data["temp_c"]
        condition = data["condition"]

        if prefered_unit == tag_fahrenheit:
            temp_value = (temp_c * 9/5) + 32
            temp_unit = "F"
        else:
            temp_value = temp_c
            temp_unit = "C"
        report = f"{condition} with a temperature of {temp_value:.0f} {temp_unit}."
        result = {"status": "success", "report": report}
        tool_context.state["last_city_checked"] = city
        return result
    else:
        return {"status": "error", "error_message": "City not found."}
