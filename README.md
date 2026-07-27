# Caspian Concierge 🎩

**An official AI support agent for the [Caspian SDK](https://github.com/TryCaspian/caspian-sdk).** 

Built for the Caspian Internship Challenge (#118), this agent helps developers set up Caspian, troubleshoot integration issues, and understand channel connections—all without ever leaving the communication channels they already use.

---

## ⚡ Features

- **Omnichannel Reachability**: Talk to the bot via Email, Telegram, Slack, or any channel supported by Caspian.
- **Single Handler Architecture**: Demonstrates the core thesis of Caspian—one `on_message` handler powering interactions across multiple distinct platforms simultaneously.
- **Context-Aware Formatting**: Automatically detects the channel (`message.channel`) and formats its output accordingly (e.g., plain text for Email, Markdown for Telegram).
- **Context-Injected Accuracy**: Injects the official Caspian `llms.txt`, `README.md`, and authentication guides directly into the prompt context for flawless answers.

---

## 🚀 Quickstart

### Prerequisites
- **Python 3.10+** (Strictly required by Caspian SDK)
- A [Google Gemini API Key](https://aistudio.google.com/)

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Shaikh-Suja-Rahaman/caspian-concierge.git
cd caspian-concierge

# Create and activate a virtual environment
python3.11 -m venv venv
source venv/bin/activate  # (Or activate.fish for Fish shell)

# Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configuration
Copy the provided `.env.example` (or create a `.env` file) in the root directory:

```env
CASPIAN_API_KEY=comm_sandbox_xxxxxxxxxxxxx
CASPIAN_BASE_URL=https://api.trycaspianai.com
GEMINI_API_KEY=your_gemini_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_token_here  # Optional
```

*Note: Free channels (Email, Telegram) use an anonymous sandbox key. Paid channels require signing in via the Caspian OAuth device flow.*

### 3. Run the Agent

```bash
python main.py
```
*The agent will immediately connect to its provisioned email address and any Telegram bots provided in your `.env`.*

---

## 💬 Talk to the Agent

You can interact with the Caspian Concierge right now! 
- **Telegram**: [t.me/caspian_concierge_bot](https://t.me/caspian_concierge_bot)
- **Email**: `caspian-concierge@agents.trycaspianai.com`

*Try asking it: "How do I install a Discord bot using the SDK?" or "What's the difference between connect_slack and install_slack?"*

---

## 🧠 Evaluation Rubric Addressed
- **Problem solved**: Directly reduces the developer support burden for Caspian itself.
- **Code quality**: Minimal, readable surface area using standard `.env` secrets.
- **Adoption**: Plausible, immediate use case for other challenge participants.
- **Caspian integration**: The agent doesn't just *use* Caspian, it *proves* Caspian's core product value.
