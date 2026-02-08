from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from pathlib import Path
# from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
# from langchain_classic.agents import create_tool_calling_agent, AgentExecutor   

from tools import  web_fitness_search
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

prompt = "You are a professional fitness coach AI.\n" \
         "You can access the internet for real-time or factual information.\n" \

# agent = create_agent(llm,prompt)
# agent = create_agent(llm, tools=[web_fitness_search], prompt=fitness_prompt)

agent = create_agent(llm, tools=[web_fitness_search])
print("🤖 Fitness Agent is ready! Ask your questions about fitness, nutrition, or health. Type 'exit' to quit." )
print("💡 Example: 'What are the latest trends in fitness for 2024?'")
print("💡 Example: 'What are the best exercises for building muscle?'")
print("💡 Example: 'What are the health benefits of a ketogenic diet?'")
print("agebt:", agent)



# if __name__ == "__main__":
#     while True:
#         user_input = input("🏋️ Ask your fitness agent: ")
#         if user_input.lower() in ["exit", "quit"]:
#             break

#         response = agent.invoke({"input": user_input})
#         print("\n🤖 Fitness Agent:", response["output"])

if __name__ == "__main__":
    user_input = input("Ask fitness question: ")
    response = agent.invoke({
        "messages": [{"role": "user", "content": user_input}]  # ✅ FIXED!
    })
    print("\n🤖", response["messages"][-1].content)