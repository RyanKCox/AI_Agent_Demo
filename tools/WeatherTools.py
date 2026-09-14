
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

