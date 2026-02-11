import chromadb
from chromadb.utils import embedding_functions
from typing import Optional
import hashlib
import json

class TavilyVectorCache:
    def __init__(self, persist_directory: str = "./chroma_cache", similarity_threshold: float = 0.85):
        """
        Initialize ChromaDB cache for Tavily responses.
        
        Args:
            persist_directory: Directory to persist ChromaDB data
            similarity_threshold: Minimum similarity score to consider a cache hit (0-1)
        """
        self.similarity_threshold = similarity_threshold
        
        # Initialize ChromaDB with persistence
        self.client = chromadb.PersistentClient(path=persist_directory)
        
        # Use sentence-transformers for embeddings
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        # Get or create collection for fitness queries
        self.collection = self.client.get_or_create_collection(
            name="tavily_fitness_cache",
            embedding_function=self.embedding_function,
            metadata={"description": "Cache for Tavily fitness search responses"}
        )
    
    def _generate_id(self, query: str) -> str:
        """Generate a unique ID for a query."""
        return hashlib.md5(query.lower().strip().encode()).hexdigest()
    
    def get_cached_response(self, query: str) -> Optional[str]:
        """
        Search for a similar query in the cache.
        
        Args:
            query: The user's search query
            
        Returns:
            Cached response if found and similar enough, None otherwise
        """
        if self.collection.count() == 0:
            return None
        
        # Search for similar queries
        results = self.collection.query(
            query_texts=[query],
            n_results=1,
            include=["documents", "metadatas", "distances"]
        )
        
        if not results["documents"] or not results["documents"][0]:
            return None
        
        # ChromaDB returns L2 distance, convert to similarity
        # Lower distance = higher similarity
        distance = results["distances"][0][0]
        # Convert L2 distance to similarity score (approximate)
        similarity = 1 / (1 + distance)
        
        if similarity >= self.similarity_threshold:
            cached_response = results["metadatas"][0][0].get("response")
            original_query = results["documents"][0][0]
            print(f"📦 Cache HIT! Similarity: {similarity:.2f}")
            print(f"   Original query: '{original_query}'")
            return cached_response
        
        print(f"📭 Cache MISS. Best similarity: {similarity:.2f} (threshold: {self.similarity_threshold})")
        return None
    
    def store_response(self, query: str, response: str) -> None:
        """
        Store a query and its response in the cache.
        
        Args:
            query: The original search query
            response: The Tavily response to cache
        """
        query_id = self._generate_id(query)
        
        # Check if this exact query already exists
        existing = self.collection.get(ids=[query_id])
        
        if existing["ids"]:
            # Update existing entry
            self.collection.update(
                ids=[query_id],
                documents=[query],
                metadatas=[{"response": response, "query": query}]
            )
            print(f"📝 Cache UPDATED for query: '{query[:50]}...'")
        else:
            # Add new entry
            self.collection.add(
                ids=[query_id],
                documents=[query],
                metadatas=[{"response": response, "query": query}]
            )
            print(f"💾 Cache STORED for query: '{query[:50]}...'")
    
    def clear_cache(self) -> None:
        """Clear all cached responses."""
        self.client.delete_collection("tavily_fitness_cache")
        self.collection = self.client.get_or_create_collection(
            name="tavily_fitness_cache",
            embedding_function=self.embedding_function
        )
        print("🗑️ Cache cleared!")
    
    def get_cache_stats(self) -> dict:
        """Get cache statistics."""
        return {
            "total_entries": self.collection.count(),
            "collection_name": self.collection.name
        }


# Singleton instance
_cache_instance: Optional[TavilyVectorCache] = None

def get_cache() -> TavilyVectorCache:
    """Get the singleton cache instance."""
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = TavilyVectorCache()
    return _cache_instance