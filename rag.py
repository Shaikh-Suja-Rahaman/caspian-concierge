import os
import json
# pyrefly: ignore [missing-import]
import httpx
# pyrefly: ignore [missing-import]
import numpy as np
# pyrefly: ignore [missing-import]
from bs4 import BeautifulSoup
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from google import genai

load_dotenv()

BASE_URL = "https://www.trycaspianai.com/docs/"
PAGES = [
    "index.html", "quickstart.html", "authentication.html", "concepts.html",
    "rich-messages.html", "sdk-python.html", "channel-email.html", 
    "channel-slack.html", "channel-discord.html", "channel-telegram.html",
    "channel-whatsapp.html", "channel-sms.html", "channel-x.html", "channel-imessage.html"
]

DB_FILE = "vector_db.json"
gemini_client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Remove script and style elements
    for script in soup(["script", "style", "nav", "header", "footer"]):
        script.decompose()
    text = soup.get_text(separator="\n")
    # Clean up excessive newlines and whitespace
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text

def chunk_text(text, chunk_size=800, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks

def build_index():
    print("Building RAG Index from Caspian docs...")
    all_chunks = []
    
    # We will also add the local SDK files for absolute completeness
    try:
        with open("../caspian-sdk/llms.txt", "r") as f:
            all_chunks.extend(chunk_text("--- Caspian llms.txt ---\n" + f.read()))
        with open("auth.txt", "r") as f:
            all_chunks.extend(chunk_text("--- Caspian Auth Guide ---\n" + f.read()))
        with open("../caspian-sdk/CONTRIBUTING.md", "r") as f:
            all_chunks.extend(chunk_text("--- Caspian Contributing ---\n" + f.read()))
    except Exception as e:
        print(f"Warning local files: {e}")

    # Fetch Web Docs
    for page in PAGES:
        url = BASE_URL + page
        try:
            print(f"Fetching {url}")
            r = httpx.get(url)
            if r.status_code == 200:
                text = extract_text_from_html(r.text)
                title = f"--- Website Page: {page} ---\n"
                page_chunks = chunk_text(title + text)
                all_chunks.extend(page_chunks)
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")

    print(f"Total chunks created: {len(all_chunks)}. Generating embeddings...")

    # Embed chunks (batching them if needed, but text-embedding-004 allows batching)
    db = []
    
    # We do them in small batches to avoid hitting limits
    batch_size = 50
    for i in range(0, len(all_chunks), batch_size):
        batch = all_chunks[i:i+batch_size]
        try:
            response = gemini_client.models.embed_content(
                model='gemini-embedding-2',
                contents=batch,
            )
            # Response returns a list of embeddings
            embeddings = [e.values for e in response.embeddings]
            for text_chunk, emb in zip(batch, embeddings):
                db.append({"text": text_chunk, "embedding": emb})
        except Exception as e:
            print(f"Embedding failed at batch {i}: {e}")

    with open(DB_FILE, "w") as f:
        json.dump(db, f)
    
    print(f"Successfully saved {len(db)} embedded chunks to {DB_FILE}!")

def retrieve(query, top_k=3):
    if not os.path.exists(DB_FILE):
        print("Vector DB not found. Run build_index() first.")
        return ""

    with open(DB_FILE, "r") as f:
        db = json.load(f)
        
    try:
        response = gemini_client.models.embed_content(
            model='gemini-embedding-2',
            contents=query,
        )
        query_emb = np.array(response.embeddings[0].values)
    except Exception as e:
        print(f"Failed to embed query: {e}")
        return ""
        
    # Compute cosine similarity
    scores = []
    for item in db:
        doc_emb = np.array(item["embedding"])
        # Cosine similarity formula
        sim = np.dot(query_emb, doc_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(doc_emb))
        scores.append((sim, item["text"]))
        
    # Sort by similarity descending
    scores.sort(key=lambda x: x[0], reverse=True)
    
    top_chunks = scores[:top_k]
    
    # Combine the top chunks into a single string
    retrieved_text = "\\n\\n...\\n\\n".join([chunk[1] for chunk in top_chunks])
    return retrieved_text

if __name__ == "__main__":
    build_index()
