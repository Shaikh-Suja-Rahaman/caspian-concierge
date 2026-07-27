# Caspian Concierge

## Problem Statement
The **Caspian Concierge** is an official AI support agent designed to help developers successfully integrate the Caspian SDK. It solves a real support burden: new developers often have questions about how to connect channels (Slack, Discord, Telegram, WhatsApp) or structure their single `on_message` handler. Instead of searching through docs, developers can chat with the concierge across the channels they already use. 

## Features
- **Multi-channel Reachability**: Built entirely on the Caspian SDK, the agent can be reached via Email, Telegram, Slack, or any other supported channel. It maintains one identity.
- **Powered by Caspian**: Leverages a single `on_message` handler for all incoming queries.
- **Context-Aware**: Injects Caspian's `llms.txt` and authentication guides into its system prompt to give perfectly accurate answers.
- **LLM Integration**: Uses Google Gemini to generate helpful, friendly responses.

## Setup & Local Run Steps

### 1. Requirements
- Python 3.10+
- Caspian SDK installed
- A Google Gemini API key

### 2. Environment Variables
Copy the provided `.env.example` to `.env` or set these in your environment:
```bash
CASPIAN_API_KEY=comm_sandbox_xxxxxxxxxxxxx
CASPIAN_BASE_URL=https://api.trycaspianai.com
GEMINI_API_KEY=your_gemini_api_key
```
*(Note: A sandbox key for Caspian is sufficient for free channels. If you wish to use paid channels like X or iMessage, you must sign in via the OAuth device flow to get a paid key.)*

### 3. Installation
```bash
# Clone the repository
git clone <repository_url>
cd caspian-concierge

# Create virtual environment
python3 -m venv venv

# Activate it (Bash/Zsh)
source venv/bin/activate
# Or if you are using Fish shell:
# source venv/bin/activate.fish

# Install dependencies
pip install -r requirements.txt
```

### 4. Running the Agent
```bash
python main.py
```
Upon running, the agent will instantly connect to an email sandbox channel and block to listen for incoming messages across all connected channels.

## How to talk to the Agent
- If you're running it locally using a free sandbox key, you can connect your Telegram bot token or Discord app to the agent by adding a line in `main.py` (e.g., `client.connect_telegram(bot_token="...")`).
- You can also test it by sending a test event to the local handler via the Caspian CLI or by using `POST {base}/v1/test-emails`.

## Evaluation Criteria Addressed
- **Problem it solves**: Concrete developer support for the Caspian SDK itself.
- **Code Quality**: Concise, readable `main.py` utilizing standard Python best practices and `.env` for secrets.
- **Adoption / Usage**: The bot can genuinely be deployed and a Telegram/Discord link shared in the intern challenge issue to help other participants unblock themselves.
- **How Caspian fits**: It's not bolted on—the product thesis *is* the Caspian framework. One handler, multiple channels. 
