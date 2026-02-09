# Fitness Agent 🏋️

A full-stack AI-powered fitness assistant application built with **Angular** (frontend) and **FastAPI + LangChain** (backend). The agent can answer fitness, nutrition, and health-related questions using web search for up-to-date information.

## Project Structure

```
fitness-agent/
├── backend/                 # Python FastAPI backend
│   ├── agents-flow/         # LangChain agent logic
│   │   ├── agent.py         # Agent configuration
│   │   ├── prompts.py       # System prompts
│   │   └── tools.py         # Web search tools (Tavily)
│   ├── main.py              # FastAPI server
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables (API keys)
│
├── ui/                      # Angular frontend
│   ├── src/
│   │   ├── app/             # Root application component
│   │   ├── chat-bot/        # Chat bot component
│   │   └── services/        # API services
│   ├── angular.json         # Angular configuration
│   └── package.json         # Node dependencies
│
└── README.md
```

## Features

- 💬 Interactive chat interface for fitness questions
- 🔍 Web search integration via Tavily API for real-time information
- 🤖 GPT-powered responses with fitness coach persona
- ⚡ Real-time streaming responses
- 🎨 Clean, responsive UI

## Prerequisites

- **Node.js** (v18+) and npm
- **Python** (3.10+)
- **OpenAI API Key**
- **Tavily API Key**

## Setup

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the `backend/` directory:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

5. Run the FastAPI server:
   ```bash
   fastapi dev main.py
   ```
   
   The backend will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the UI directory:
   ```bash
   cd ui
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```
   
   The frontend will be available at `http://localhost:4200`

## API Endpoints

| Method | Endpoint   | Description                        |
|--------|------------|------------------------------------|
| GET    | `/`        | Health check                       |
| POST   | `/agent/`  | Send a prompt to the fitness agent |

### Example Request

```bash
curl -X POST http://localhost:8000/agent/ \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What are the best exercises for building muscle?"}'
```

### Example Response

```json
{
  "response": "Here are the best exercises for building muscle...",
  "status": "success"
}
```

## Usage

1. Start both the backend and frontend servers
2. Open `http://localhost:4200` in your browser
3. Type your fitness-related question in the chat box
4. Press **Ctrl+Enter** or click **Send** to submit
5. Receive AI-powered fitness advice!

### Example Questions

- "What are the latest trends in fitness for 2024?"
- "What are the best exercises for building muscle?"
- "What are the health benefits of a ketogenic diet?"
- "How many calories should I eat to lose weight?"

## Tech Stack

### Frontend
- Angular 21
- RxJS
- TypeScript

### Backend
- FastAPI
- LangChain
- OpenAI GPT
- Tavily Search API
- Python 3.10+

## Development

### Running Tests

**Frontend:**
```bash
cd ui
npm test
```

**Backend:**
```bash
cd backend
pytest
```

### Building for Production

**Frontend:**
```bash
cd ui
npm run build
```