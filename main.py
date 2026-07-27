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

import rag

chat_sessions = {}

@client.on_message
def handle(message):
    print(f"Received message from {message.sender} on {message.conversation_id} via {message.channel}: {message.text}")
    
    # Retrieve relevant RAG context for this specific message
    retrieved_docs = rag.retrieve(message.text, top_k=3)
    
    system_instruction = f"""You are the Caspian Concierge, an official AI support agent for the Caspian SDK.
Your job is to help developers integrate Caspian into their apps. You can answer questions about API keys, channels, handlers, and the SDK surface.
You speak clearly and concisely. You are friendly and encouraging.

Here is the retrieved official documentation you must use to answer this specific question:

{retrieved_docs}

Important Instructions:
- Only answer questions related to the Caspian SDK, integrations, or messaging channels.
- Emphasize that Caspian uses a single `on_message` handler for all channels.
- Do not invent code snippets that use non-existent methods; rely on the provided documentation.

CHANNEL FORMATTING RULE:
- The user is currently chatting with you over the `{message.channel}` channel. 
- If the channel is `email`, DO NOT use markdown code blocks (```). Just use plain text indentation for code so it renders nicely in standard email clients like Gmail.
- If the channel is `telegram` or `discord`, you may use markdown code blocks.
"""

    global chat_sessions
    if message.conversation_id not in chat_sessions:
        chat_sessions[message.conversation_id] = gemini_client.chats.create(
            model='gemini-2.5-flash',
            config=genai.types.GenerateContentConfig(
                system_instruction=system_instruction,
            )
        )

    try:
        response = chat_sessions[message.conversation_id].send_message(message.text)
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
