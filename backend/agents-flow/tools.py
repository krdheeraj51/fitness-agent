from langchain_core.tools import tool
from dotenv import load_dotenv
from pathlib import Path
from langchain_tavily import TavilySearch  
import os

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)
tavily_key = os.getenv("TAVILY_API_KEY")

if not tavily_key:
    raise ValueError("TAVILY_API_KEY not found")

tavily_tool = TavilySearch (
    max_results=5,
    search_depth="advanced"
)

@tool
def web_fitness_search(query: str) -> str:
    """
    Search the web for up-to-date fitness, nutrition, or health information.
    """
    results = tavily_tool.invoke({"query": query})
    return results