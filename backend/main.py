from fastapi import FastAPI
from pydantic import BaseModel
import sys
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
sys.path.insert(0,str(Path(__file__).parent /'agents-flow'))  # Add the agents-flow directory to the path

from agent import agent

app = FastAPI()

# add middleware for CORS if needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (use specific origins in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
class Item(BaseModel):
    name: str
    price: float

class PromptRequest(BaseModel):
    prompt: str

class AgentResponse(BaseModel):
    response: str
    status: str


@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.post("/agent/")
async def process_with_agent(request: PromptRequest):
    """
    Send a prompt to the fitness agent and get a response.
    """
    try:
        response = agent.invoke({"messages": [{"role": "user", "content": request.prompt}]})

        # Extract the agent's response from the returned structure
        if "messages" in response and len(response["messages"]) > 0:
            agent_reply = response["messages"][-1].content
        else:
            agent_reply = "No response from agent."
        
        return AgentResponse(response=agent_reply, status="success")

    except Exception as e:
        return AgentResponse(response=str(e), status="error")

# @app.post("/items/")
# def create_item(item: Item):
#     return {"item_name": item.name, "item_price": item.price}