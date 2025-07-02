
# ChatGPT MCP Bridge

This project provides a simple **Python command-line interface** that uses the **OpenAI ChatGPT API** to control a local hardware automation system (such as Arduino LEDs) via a **Model Context Protocol (MCP)** server. Use this with project MCPForLedAPI.

It lets you type natural language commands like `"turn on the blue light"` or `"set mood to calm"`, and it will:
1. Send the input to **ChatGPT** to extract a structured intent
2. POST that intent to your local **MCP server**
3. Display the result

The file ChatwithMCPForLeadAPI.py contains a version with only LED intents.
The file ChatWithMCPForLeadAPIMixedMode.py contains a versin where ChatGPT also answers regular requests. Use this for optimal results.
---

## Features

- Integrates with **OpenAI Chat API** (GPT-4)
- Translates user phrases into structured LED control commands
- Communicates with your local **MCP FastAPI server**
- Supports multiple hardware-level intents

---

## Example Intents

| Intent       | Description                            | Parameters                    |
|--------------|----------------------------------------|-------------------------------|
| TurnOnLed    | Turns on a specific LED                | `{ "color": "green" }`        |
| TurnOffLed   | Turns off all LEDs                     | `{}`                          |
| SetMood      | Mood-based pattern control             | `{ "mood": "calm" }`          |
| SetPattern   | Direct bit-pattern for LED control     | `{ "pattern": "1010" }`       |
| PowerDown    | Alias for turning everything off       | `{}`                          |
| GetStatus    | Query current LED state                | `{}`                          |

---

## Setup

1. Clone/download this project.

2. Install dependencies:

```bash
pip install openai requests python-dotenv
```

3. Add your API key to `.env`:

```env
OPENAI_API_KEY=sk-xxxxxxx
```

4. Start your **MCP FastAPI server** locally:
```bash
uvicorn MCPForLedAPI:app --reload
```

5. Run the bridge:

```bash
python ChatWithMCPForLedAPI.py
```

---

## Usage

You can now type commands like:
- `Turn on the red light`
- `Set mood to focus`
- `Turn everything off`

It will send them to ChatGPT → MCP → Arduino

---


## License

MIT
