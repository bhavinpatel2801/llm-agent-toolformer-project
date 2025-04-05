"""
Tool: Weather API
Fetches weather forecast using OpenWeatherMap API.
"""

import requests
import os

def get_weather(city, api_key=None):
    api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "[Weather API] No API key provided."

    endpoint = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    try:
        response = requests.get(endpoint, params=params)
        data = response.json()
        if data.get("cod") != 200:
            return f"[Weather API] Error: {data.get('message', 'Unknown error')}"
        weather = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The weather in {city} is {weather} with {temp}°C."
    except Exception as e:
        return f"[Weather API] Exception occurred: {e}"
