import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from caspian_sdk import CommClient
# pyrefly: ignore [missing-import]
from google import genai

# Load environment variables
load_dotenv()

# Initialize Caspian Client
client = CommClient()

# Initialize Gemini Client
gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def get_context():
    # Attempt to load llms.txt for SDK instructions
    context_text = ""
    try:
        with open("../caspian-sdk/llms.txt", "r") as f:
            context_text += f.read() + "\n\n"
    except Exception as e:
        print(f"Warning: could not load llms.txt: {e}")
        
    try:
        with open("auth.txt", "r") as f:
            context_text += f.read() + "\n\n"
    except Exception as e:
        print(f"Warning: could not load auth.txt: {e}")
        
    return context_text

CONTEXT = get_context()

SYSTEM_PROMPT = f"""You are the Caspian Concierge, an official AI support agent for the Caspian SDK.
Your job is to help developers integrate Caspian into their apps. You can answer questions about API keys, channels, handlers, and the SDK surface.
You speak clearly and concisely. You are friendly and encouraging.

Here is the official documentation you must use to answer questions:

{CONTEXT}

Important Instructions:
- Only answer questions related to the Caspian SDK, integrations, or messaging channels.
- Emphasize that Caspian uses a single `on_message` handler for all channels.
- Do not invent code snippets that use non-existent methods; rely on the provided documentation.
"""

@client.on_message
def handle(message):
    print(f"Received message from {message.sender} on {message.conversation_id}: {message.text}")
    
    # We maintain minimal history here, just passing the system prompt and the user's message
    # In a full production bot, we would fetch previous messages in the thread if needed.
    
    try:
        response = gemini_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
            config=genai.types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
            )
        )
        reply_text = response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        reply_text = "I encountered an error trying to process your request. Please try again later."
        
    message.reply(reply_text)

if __name__ == "__main__":
    print("Starting Caspian Concierge...")
    # Optional: connect a free channel instantly for testing (like email)
    client.connect_email(username="caspian-concierge")
    
    # Connect Telegram using the token from .env
    telegram_token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if telegram_token:
        client.connect_telegram(bot_token=telegram_token)
        print("Connected to Telegram!")
        
    client.listen()
