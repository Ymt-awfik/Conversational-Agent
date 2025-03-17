import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=API_KEY)

def get_current_weather(location):
    """Retrieve the current weather for a given location."""
    url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={location}&aqi=no"
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        return f"Error: {data['error']['message']}"
    weather_info = data["current"]
    return json.dumps({
        "location": data["location"]["name"],
        "temperature_c": weather_info["temp_c"],
        "condition": weather_info["condition"]["text"]
    })

def get_weather_forecast(location, days=3):
    """Retrieve a weather forecast for a given location and number of days."""
    url = f"http://api.weatherapi.com/v1/forecast.json?key={WEATHER_API_KEY}&q={location}&days={days}&aqi=no"
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        return f"Error: {data['error']['message']}"
    forecast_data = [{
        "date": day["date"],
        "max_temp_c": day["day"]["maxtemp_c"],
        "min_temp_c": day["day"]["mintemp_c"],
        "condition": day["day"]["condition"]["text"]
    } for day in data["forecast"]["forecastday"]]
    return json.dumps({"location": data["location"]["name"], "forecast": forecast_data})

def process_messages(client, messages, tools, available_functions):
    """Process messages and invoke tools as needed."""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools
    )
    response_message = response.choices[0].message
    messages.append(response_message)
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions.get(function_name)
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })
    return messages

def run_conversation(client):
    """Run a conversation with the user."""
    messages = [{"role": "system", "content": "You are a helpful weather assistant."}]
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        messages.append({"role": "user", "content": user_input})
        messages = process_messages(client, messages, weather_tools, available_functions)
        last_message = messages[-1]
        if last_message["role"] == "assistant" and last_message.get("content"):
            print(f"Assistant: {last_message['content']}")

# Define available tools
weather_tools = [
    {"type": "function", "function": {"name": "get_current_weather", "description": "Get current weather.", "parameters": {"type": "object", "properties": {"location": {"type": "string"}}}}},
    {"type": "function", "function": {"name": "get_weather_forecast", "description": "Get weather forecast.", "parameters": {"type": "object", "properties": {"location": {"type": "string"}, "days": {"type": "integer"}}}}}
]

available_functions = {"get_current_weather": get_current_weather, "get_weather_forecast": get_weather_forecast}

if __name__ == "__main__":
    run_conversation(client)