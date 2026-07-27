

<h1 align="center">
  <img class="orb" width="50" src="assets/orb.png" alt="" aria-hidden="true">
  
  Caspian Concierge
</h1>

<p align="center">
  <a href="https://trycaspianai.com">Website</a>
  ·
  <a href="https://github.com/TryCaspian/caspian-sdk">Caspian SDK</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white" alt="Google Gemini" />
  <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy" />
  <img src="https://img.shields.io/badge/Caspian_SDK-000000?style=for-the-badge&logo=github&logoColor=white" alt="Caspian SDK" />
</p>

<p align="center">
  <strong>The Unofficial AI support agent for the Caspian SDK.<br/>One agent identity, answering questions across Email and Telegram</strong>
</p>

---

Built for the **Caspian Internship Challenge (#118)**, the Caspian Concierge helps developers set up Caspian, troubleshoot integration issues, and understand channel connections—all without ever leaving the communication channels they already use.

## The Architecture

Your agent's reasoning decides **what** to say. Caspian is **how it exists** across channels. 
This repository proves Caspian's core product value: one `on_message` handler powering interactions across multiple distinct platforms simultaneously.

### RAG Engine
The agent doesn't blindly stuff docs into its prompt. It uses a custom-built, lightweight Retrieval-Augmented Generation (RAG) pipeline powered by `numpy` and `gemini-embedding-2`. When a user asks a question, the agent instantly retrieves the Top 3 most relevant documentation chunks to answer flawlessly.

**Indexed Knowledge Base:**
- The official website documentation (`index`, `quickstart`, `authentication`, `concepts`, `rich-messages`)
- All channel-specific guides (Email, Slack, Discord, Telegram, SMS, WhatsApp, X, iMessage)
- The Python SDK Reference
- Internal repository guides (`llms.txt`, `CONTRIBUTING.md`)

## Get started in 30 seconds

**Prerequisites:**
- **Python 3.10+** (Strictly required by Caspian SDK)
- A Google Gemini API Key

**Set it up:**

```bash
git clone https://github.com/Shaikh-Suja-Rahaman/caspian-concierge.git
cd caspian-concierge

# Create and activate a virtual environment
python3.11 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

Copy `.env.example` to `.env`:

```env
CASPIAN_API_KEY=comm_sandbox_xxxxxxxxxxxxx
CASPIAN_BASE_URL=https://api.trycaspianai.com
GEMINI_API_KEY=your_gemini_api_key_here
TELEGRAM_BOT_TOKEN=your_telegram_token_here
```

Then run the agent:

```bash
python main.py
```

## Docker Support

This project is fully containerized and production-ready! You can run it on your machine or deploy it to any cloud provider (Render, AWS, Railway) seamlessly without dealing with Python virtual environments.

**Build the image:**
```bash
docker build -t caspian-concierge .
```

**Run the container:**
```bash
docker run --env-file .env caspian-concierge
```

## Talk to the Agent

You can interact with the Caspian Concierge right now! 
- **Telegram**: [t.me/caspian_concierge_bot](https://t.me/caspian_concierge_bot)
- **Email**: `caspian-concierge@agents.trycaspianai.com`

*Try asking it: "How do I install a Discord bot using the SDK?" or "What's the difference between connect_slack and install_slack?"*

## Evaluation Rubric Addressed

<table>
<tr>

</tr>
<tr>
<td><b>Problem solved</b></td>
<td>Directly reduces the developer support burden for Caspian itself.</td>
</tr>
<tr>
<td><b>Code quality</b></td>
<td>Minimal, readable surface area using standard <code>.env</code> secrets. RAG eliminates context-bloat.</td>
</tr>
<tr>
<td><b>Adoption</b></td>
<td>Plausible, immediate use case for other challenge participants.</td>
</tr>
<tr>
<td><b>Caspian integration</b></td>
<td>The agent doesn't just <i>use</i> Caspian, it <i>proves</i> Caspian's core thesis.</td>
</tr>
</table>
