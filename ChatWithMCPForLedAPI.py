
import os
import requests
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "your-openai-api-key"
MCP_URL = "http://localhost:8000/intent"

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are an assistant for controlling a hardware LED system.
Given a natural language command, extract an intent and parameters.

Supported intents:
- TurnOnLed {color: red|yellow|green|blue}
- TurnOffLed {}
- SetMood {mood: calm|alert|focus|idle}
- SetPattern {pattern: string of 4 binary digits, e.g., "1010"}
- PowerDown {}
- GetStatus {}

Only return valid JSON like:
{ "intent": "TurnOnLed", "parameters": { "color": "green" } }
"""

def parse_command_to_intent(user_input: str):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        temperature=0.0
    )
    return response.choices[0].message.content.strip()

def send_to_mcp(intent_json: dict):
    response = requests.post(MCP_URL, json=intent_json)
    return response.json()

def main():
    print("ChatGPT-to-MCP bridge ready. Type a command like 'Turn on the red light' (type 'exit' to quit).")
    while True:
        user_input = input("🗣️ > ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break

        try:
            intent_str = parse_command_to_intent(user_input)
            print(f"Parsed intent: {intent_str}")
            intent_json = json.loads(intent_str)
            mcp_response = send_to_mcp(intent_json)
            print(f"MCP response: {mcp_response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
