# Retail Multi-Agent AI System

A production-grade Agentic AI platform designed for a large retail enterprise. This system allows business users to interact with multiple enterprise systems (ERP, OMS, WMS, CRM, etc.) using natural language via a **React/Vite Web UI**.

The platform employs a **Supervisor (Orchestrator)** pattern using [LangGraph](https://langchain-ai.github.io/langgraph/). Complex queries are dynamically routed to specialized domain agents, which execute specific tasks using integrated tools and return the results for synthesis. Conversation memory is persistently stored in a PostgreSQL database using LangGraph Checkpointers.

## 🧠 Multi-Agent Architecture

The system consists of the following agents:

1. **Orchestrator Agent**: The supervisor that detects user intent, creates execution plans, routes tasks to specialists, and synthesizes the final answer.
2. **Inventory Agent**: Checks stock levels and forecasts depletion (integrates with WMS).
3. **Sales Agent**: Analyzes revenue, sales volume, and YoY growth (integrates with CRM/Sales systems).
4. **Order Agent**: Tracks fulfillment status and shipment delays (integrates with OMS).
5. **Finance Agent**: Generates P&L summaries and calculates margins (integrates with ERP).
6. **Supply Chain Agent**: Analyzes vendor lead times and generates replenishment orders.
7. **Analytics Agent**: Dedicated to root-cause analysis and complex data synthesis.

## 🚀 Setup & Installation

This project uses [`uv`](https://docs.astral.sh/uv/) for fast dependency management.

1. Ensure you have Python >= 3.12 installed.
2. Clone the repository and navigate into the project root.
3. Install dependencies:
   ```bash
   uv sync
   ```
   *(Alternatively, `uv run` handles dependency resolution automatically).*

## ⚙️ Configuration

Create a `.env` file in the root directory and provide your preferred LLM provider's API keys, as well as your Supabase database credentials. By default, the system uses OpenAI's `gpt-4o`, but it also supports Anthropic's Claude models.

```env
# Choose 'openai' or 'anthropic'
LLM_PROVIDER=openai

# LLM API Keys
OPENAI_API_KEY=your_openai_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Supabase Credentials (REST API)
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_anon_or_service_role_key

# PostgreSQL Connection String (For LangGraph Conversation Memory)
DATABASE_URL=postgresql://user:password@host:port/dbname
```

## 🗄️ Database Setup & Seeding

The platform agents dynamically fetch real-time data from a **Supabase PostgreSQL** database.

1. **Create Tables**: Open your Supabase Dashboard's SQL Editor, paste the contents of `supabase_schema.sql`, and run it.
2. **Generate Dummy Data (Optional)**: The `data/` directory contains pre-generated CSV files (`inventory.csv`, `sales.csv`, `orders.csv`, `products.csv`), but you can generate a fresh batch of 50 randomized records at any time:
   ```bash
   uv run python data/generate.py
   ```

3. **Seed Database**: Once your CSV files are ready, run the seeding script to inject the data directly into your Supabase project:
   ```bash
   uv run python scripts/seed_supabase.py
   ```

## 💻 Usage

To run the application locally, you will need two terminal windows:

### 1. Start the FastAPI Backend
```bash
uv run uvicorn api:app --reload
```
*(Runs on `http://localhost:8000`)*

### 2. Start the React Frontend
Open a new terminal and navigate to the frontend directory:
```bash
cd frontend
npm run dev
```
*(Runs on `http://localhost:5173`)*

Open the Vite URL in your browser to access the beautiful glassmorphism chat UI!

### Example Queries
Try asking the system complex, cross-domain questions in the chat:
- *"Compare sales versus inventory levels for the top 50 products."*
- *"Why did online sales drop yesterday?"*
- *"Create a replenishment recommendation for low-stock items."*
- *"List orders delayed more than 3 days."*

## ☁️ Deployment
Ready to go to production? Check out the **[DEPLOYMENT.md](DEPLOYMENT.md)** guide to securely containerize and host the React frontend and FastAPI backend on **Google Cloud Run**.
