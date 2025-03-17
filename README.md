# Conversational Agent

## Overview
This project implements a chatbot that provides weather information using OpenAI's GPT API and Weather API.

## Setup Instructions
1. **Install Dependencies**:
   ```sh
   pip install openai requests python-dotenv
   ```
2. **Create a `.env` file** and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   WEATHER_API_KEY=your_weather_api_key_here
   ```
3. **Run the chatbot**:
   ```sh
   python conversational_agent.py
   ```

## Features
- Fetches real-time weather data.
- Supports weather forecasts for multiple days.
- Uses OpenAI API for natural language interactions.

## Usage
Ask questions like:
```
You: What is the weather in New York?
Assistant: The current temperature in New York is 15°C with clear skies.
```
Type `exit` to end the conversation.

## Troubleshooting
- **Invalid API Key**: Check the `.env` file.
- **Quota Exceeded**: Verify OpenAI usage at [OpenAI Usage Page](https://platform.openai.com/usage).

## License
This project is for educational purposes only.

