from pathlib import Path
from dotenv import load_dotenv
import os
from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
from rich import print

# --- Load .env explicitly ---
BASE_DIR = Path(__file__).resolve().parent
ENV_PATH = BASE_DIR / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

# --- Debug prints (VERY IMPORTANT for now) ---
api_key = os.getenv("TAVILY_API_KEY")

print("ENV PATH:", ENV_PATH)
print("ENV EXISTS:", ENV_PATH.exists())
print("TAVILY KEY LOADED:", bool(api_key))

# --- Initialize Tavily ---
if not api_key:
    raise ValueError("❌ TAVILY_API_KEY not found. Check your .env file.")

tavily = TavilyClient(api_key=api_key)

# --- Web Search Tool ---
@tool
def web_search(query: str) -> str:
    """Search the web for recent and reliable information on a topic. Returns titles, URLs, and snippets."""
    try:
        results = tavily.search(query=query, max_results=5)

        out = []
        for r in results.get("results", []):
            out.append(
                f"Title: {r.get('title')}\n"
                f"URL: {r.get('url')}\n"
                f"Snippet: {r.get('content', '')[:300]}\n"
            )

        return "\n----\n".join(out) if out else "No results found."

    except Exception as e:
        return f"Search error: {str(e)}"

# --- Scrape Tool ---
@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        return text[:3000] if text else "No readable content found."

    except Exception as e:
        return f"Could not scrape URL: {str(e)}"