import asyncio
from my_agent import agent
from datetime import datetime
from typing import Annotated
from pydantic import Field
from agent_framework import tool

import os
import requests

@tool(
    name="weather_tool", description="Retrieves weather information for any location"
)
def get_weather(
    city: Annotated[str, Field(description="The city to get the weather for.  MUST be in English.")],
    country_code: Annotated[str, Field(description="The ISO 3166 country code of the city. MUST be in English.")],
) -> str:
    """Get the weather for a given city."""
    print(f"[Function call] get_weather with city: {city}")
    api_key = os.getenv("OPEN_WEATHER_MAP_API_KEY")
    if not api_key:
        return {
            "status": "error",
            "error_message": "API key for OpenWeatherMap is not set.",
        }
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        print(data)
        if data["cod"] != 200:
            return {
                "status": "error",
                "error_message": f"Weather information for '{city}' is not available.",
            }
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        report = (
            f"The weather in {city} is {weather_description} with a temperature of "
            f"{temperature} degrees Celsius."
        )
        print(f"[Function response] {report}")
        return {"status": "success", "report": report}
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error_message": f"An error occurred while fetching the weather data: {str(e)}",
        }

this_session = agent.create_session()

agent.name = "WeatherAgent"
agent.instructions = """
You are a helpful assistant that provides weather information. 
You have access to a tool called 'weather_tool' that can retrieve weather information for any location.
When you call get weather tool, you must send the city name and the country code in English.
使用繁體中文回答問題。
"""

async def main():
    while True:
        question = input("請輸入問題:(輸入'exit'或'quit'或按下Enter離開) ")
        if not question or question.lower() in ["exit", "quit"]:
            break
        print(f"問: {question}")
        start_time = datetime.now()
        result = await agent.run(
            question,
            session=this_session,
            tools=[get_weather]
        )
        print(f"答: {result.text}")
        end_time = datetime.now()
        print(f"耗時: {(end_time - start_time).total_seconds():.2f} 秒")

asyncio.run(main())