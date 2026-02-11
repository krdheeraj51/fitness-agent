from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from pathlib import Path

from tools import  web_fitness_search
from query_cache import get_cache
from prompts import fitness_prompt
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

llm = ChatOpenAI(
    model="gpt-5.1",
    temperature=0.3

)

# tools = [
#     web_fitness_search
# ]

system_content = fitness_prompt.messages[0].prompt.template


agent = create_agent(llm, tools=[web_fitness_search],system_prompt=system_content)

# Initialize cache and show stats
cache = get_cache()
stats = cache.get_cache_stats()

print("🤖 Fitness Agent is ready! Ask your questions about fitness, nutrition, or health. Type 'exit' to quit.")
print(f"📊 Cache Status: {stats['total_entries']} cached queries")
print("💡 Example: 'What are the latest trends in fitness for 2026?'")
print("💡 Example: 'What are the best exercises for building muscle?'")
print("💡 Example: 'What are the health benefits of a ketogenic diet?'")
print("💡 Type 'clear cache' to clear the vector cache")
print("💡 Type 'cache stats' to view cache statistics")


# if __name__ == "__main__":
#     user_input = input("Ask fitness question: ")
#     response = agent.invoke({
#         "messages": [{"role": "user", "content": user_input}]  # ✅ FIXED!
#     })
#     print("\n🤖", response["messages"][-1].content)

if __name__ == "__main__":
    while True:
        user_input = input("\n🏋️ Ask your fitness agent: ")
        
        if user_input.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        
        if user_input.lower() == "clear cache":
            cache.clear_cache()
            continue
        
        if user_input.lower() == "cache stats":
            stats = cache.get_cache_stats()
            print(f"📊 Cache Statistics: {stats}")
            continue
        
        response = agent.invoke({
            "messages": [{"role": "user", "content": user_input}]
        })
        print("\n🤖", response["messages"][-1].content)