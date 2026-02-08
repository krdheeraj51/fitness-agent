from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor

from tools import  web_fitness_search
from prompts import fitness_prompt

load_dotenv()

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.3

)

tools = [
    web_fitness_search
]

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=fitness_prompt
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True
)

if __name__ == "__main__":
    while True:
        user_input = input("🏋️ Ask your fitness agent: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        response = agent_executor.invoke({"input": user_input})
        print("\n🤖 Fitness Agent:", response["output"])
