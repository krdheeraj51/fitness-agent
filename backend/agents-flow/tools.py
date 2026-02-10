from langchain_core.tools import tool
from dotenv import load_dotenv
from pathlib import Path
# from langchain_tavily import TavilySearch  
from tavily import TavilyClient
from query_cache import get_cache
import os

env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)
tavily_key = os.getenv("TAVILY_API_KEY")

if not tavily_key:
    raise ValueError("TAVILY_API_KEY not found")
# Initialize Tavily client

tavily_client = TavilyClient(api_key=tavily_key)

# tavily_tool = TavilySearch (
#     max_results=5,
#     search_depth="advanced"
# )

@tool
def web_fitness_search(query: str) -> str:
    """
    Search the web for fitness, nutrition, or health-related information.
    Uses ChromaDB cache to avoid redundant API calls for similar queries.
    
    Args:
        query: The search query about fitness, nutrition, or health
        
    Returns:
        Search results from cache or Tavily
    """
    cache = get_cache()
    
    # Check cache first
    cached_response = cache.get_cached_response(query)
    if cached_response:
        return f"[From Cache]\n{cached_response}"
    
    # If not in cache, call Tavily
    print(f"🔍 Calling Tavily API for: '{query[:50]}...'")
    
    try:
        response = tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=True
        )
        
        # Format the response
        if response.get("answer"):
            result = f"Answer: {response['answer']}\n\nSources:\n"
        else:
            result = "Search Results:\n"
        
        for idx, res in enumerate(response.get("results", []), 1):
            result += f"{idx}. {res.get('title', 'No title')}\n"
            result += f"   URL: {res.get('url', 'No URL')}\n"
            result += f"   {res.get('content', 'No content')[:200]}...\n\n"
        
        # Store in cache
        cache.store_response(query, result)
        
        return result
        
    except Exception as e:
        return f"Error searching: {str(e)}"

# @tool
# def web_fitness_search(query: str) -> str:
#     """
#     Search the web for up-to-date fitness, nutrition, or health information.
#     """
#     results = tavily_tool.invoke({"query": query})
#     return results