
import os
import json
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "your-openai-api-key"
MCP_URL = "http://localhost:8000/intent"

client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """
You are a helpful assistant that can also control an LED system.
If it is general or unrelated to LED control, respond naturally as an assistant.

If the user's input is related to LED control, respond with a JSON intent like:
{ "intent": "TurnOnLed", "parameters": { "color": "green" } }
Supported intents:
- TurnOnLed {color: red|yellow|green|blue}
- TurnOffLed {}
- SetMood {mood: calm|alert|focus|idle}
- SetPattern {pattern: string of 4 binary digits, e.g., "1010"}
- PowerDown {}
- GetStatus {}

Do not respond with both text and JSON together.
"""

def is_json_intent(text):
    try:
        parsed = json.loads(text)
        return isinstance(parsed, dict) and "intent" in parsed
    except Exception:
        return False

def parse_command(user_input: str):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()

def send_to_mcp(intent_json: dict):
    response = requests.post(MCP_URL, json=intent_json)
    return response.json()

def main():
    print("ChatGPT-MCP agent ready. You can ask me anything. Type 'exit' to quit.")
    while True:
        user_input = input("> ").strip()
        if user_input.lower() in ["exit", "quit"]:
            break

        try:
            reply = parse_command(user_input)
            if is_json_intent(reply):
                print(f"Intent detected: {reply}")
                intent_json = json.loads(reply)
                mcp_response = send_to_mcp(intent_json)
                print(f"MCP responded: {mcp_response}")
            else:
                print(f"ChatGPT says: {reply}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
