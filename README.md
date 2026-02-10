# 🏋️ Fitness Agent

An AI-powered fitness assistant that answers questions about fitness, nutrition, and health using LangChain, OpenAI, and Tavily search with intelligent semantic caching.

## 🌟 Features

- **AI-Powered Responses**: Uses GPT-5.1 for intelligent fitness advice
- **Web Search**: Real-time fitness information via Tavily API
- **Semantic Caching**: ChromaDB vector database caches responses to reduce API calls
- **Smart Query Matching**: Similar questions return cached results instantly

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Query                             │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                    Fitness Agent                            │
│                  (LangChain + GPT-5.1)                      │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                  web_fitness_search Tool                    │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│               ChromaDB Semantic Cache                       │
│          (Query Embeddings + Similarity Search)             │
└─────────────────────────┬───────────────────────────────────┘
                          │
              ┌───────────┴───────────┐
              │                       │
      Similarity >= 0.85      Similarity < 0.85
              │                       │
              ▼                       ▼
       ┌──────────┐           ┌──────────────┐
       │  Return  │           │   Tavily     │
       │  Cached  │           │   API Call   │
       │ Response │           └──────┬───────┘
       └──────────┘                  │
                                     ├──► Store in Cache
                                     │
                                     ▼
                              Return Response
```

## 📁 Project Structure

```
fitness-agent/
├── backend/
│   ├── agents-flow/
│   │   ├── agent.py           # Main agent entry point
│   │   ├── tools.py           # Tavily search tool with caching
│   │   ├── prompts.py         # System prompts for the agent
│   │   ├── query_cache.py     # ChromaDB vector cache implementation
│   │   └── chroma_cache/      # Persistent cache storage (auto-generated)
│   └── .env                   # Environment variables
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

## 🚀 Installation

### Prerequisites

- Python 3.10+
- OpenAI API Key
- Tavily API Key

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fitness-agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create `backend/.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   TAVILY_API_KEY=your_tavily_api_key
   ```

5. **Run the FastApi server**
   ```bash
   cd backend/agents-flow
   fastapi dev main.py
   ```
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

## 💾 Semantic Cache System

### How It Works

The cache uses **ChromaDB** with **sentence-transformers** to create embeddings of user queries. When a new query comes in:

1. **Embedding Generation**: Query is converted to a vector using `all-MiniLM-L6-v2` model
2. **Similarity Search**: ChromaDB finds the most similar cached query
3. **Threshold Check**: If similarity ≥ 85%, return cached response
4. **API Call**: If no match, call Tavily API and store the result

### Cache Benefits

| Benefit | Description |
|---------|-------------|
| **Cost Reduction** | Fewer Tavily API calls = lower costs |
| **Faster Responses** | Cached responses return instantly |
| **Semantic Matching** | "best exercises for muscle" matches "top workouts for building muscle" |
| **Persistent Storage** | Cache survives application restarts |

### Cache Configuration

```python
# In query_cache.py
TavilyVectorCache(
    persist_directory="./chroma_cache",  # Storage location
    similarity_threshold=0.85             # Match threshold (0-1)
)
```


## 🎯 Usage Examples

```bash
🏋️ Ask your fitness agent: What are the best exercises for building muscle?
🔍 Calling Tavily API for: 'What are the best exercises for building muscle?'
💾 Cache STORED for query: 'What are the best exercises for building muscle?'
🤖 Based on the latest research, the best exercises for building muscle include...

🏋️ Ask your fitness agent: Top workouts for muscle growth
📦 Cache HIT! Similarity: 0.89
   Original query: 'What are the best exercises for building muscle?'
🤖 [From Cache] Based on the latest research...
```
## 📊 Performance

| Metric | Without Cache | With Cache (Hit) |
|--------|---------------|------------------|
| Response Time | 2-5 seconds | <100ms |
| API Cost | Per query | Zero |
| Accuracy | Real-time | Cached data |
