# Stock Research Multi-Agent System

A sophisticated multi-agent investment research system built with Google's ADK (Agent Development Kit) framework. The system analyzes stocks through fundamental analysis, technical analysis, and news sentiment, then generates comprehensive investment reports.

## Features

- 🤖 **Multi-Agent Architecture**: Specialized agents for different analysis types.
- 💬 **Natural Language Queries**: Ask "analyze Apple stock" instead of needing ticker symbols.
- 📊 **Comprehensive Analysis**:
  - Fundamental analysis (financial metrics, valuation ratios, profitability metrics).
  - Technical analysis (moving averages, RSI, MACD trend indicators).
  - News sentiment (grounded via Google Search integration).
- 📝 **Detailed Reports**: AI-generated investment reports with recommendations.
- 🔄 **Session State**: Tracks research progress across agent interactions.

---

## Architecture

```
User Query: "analyze apple stock"
    ↓
Research Coordinator Agent
    ↓
Ticker Resolver Agent → Resolves to "AAPL"
    ↓
┌──────────────┬─────────────────┬──────────────────┐
│ Fundamental  │ Technical       │ News Sentiment   │
│ Analyst      │ Analyst         │ (Google Search)  │
└──────────────┴─────────────────┴──────────────────┘
    ↓
Report Generator Agent
    ↓
Final Investment Report with Recommendation
```

---

## Prerequisites

- Python 3.11 or higher
- [UV](https://github.com/astral-sh/uv) package manager
- Google API Key (for Gemini models and Google Search grounding)

---

## Installation

1. **Clone the repository** (or navigate to the project directory)

2. **Install UV** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # Or using Homebrew:
   brew install uv
   ```

3. **Synchronize dependencies and setup virtualenv**:
   ```bash
   # Automatically creates a .venv and installs all dependencies and CLI tools
   uv sync --all-extras
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GOOGLE_API_KEY
   ```

---

## Configuration

Edit the `.env` file with your authentication details:

### Option 1: Gemini Developer API (Default)
```env
GOOGLE_API_KEY=your_google_api_key_here
```
> [!TIP]
> Get your Google API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Option 2: GCP Vertex AI
```env
GOOGLE_GENAI_USE_VERTEXAI=True
GOOGLE_CLOUD_PROJECT=your_gcp_project_id_here
GOOGLE_CLOUD_LOCATION=us-central1
```
> [!IMPORTANT]
> When using Vertex AI, ensure you are authenticated locally with GCP using:
> ```bash
> gcloud auth application-default login
> ```

### Optional Multi-Model Config
```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

---

## Usage

You can run the agent either through the dedicated CLI shortcut or using standard Python module execution.

### CLI shortcut (Recommended)
```bash
uv run portfolio-agent "analyze apple stock"
```

### Python module execution
```bash
uv run python -m portfolio_agent.main "analyze apple stock"
```

### Example Queries
```bash
# Natural language
uv run portfolio-agent "analyze Tesla"
uv run portfolio-agent "what do you think about Microsoft stock?"
uv run portfolio-agent "research NVIDIA"

# Direct ticker symbols
uv run portfolio-agent "analyze AAPL"
uv run portfolio-agent "TSLA analysis"
```

---

## Project Structure

```
portfolio-management-agent/
├── src/
│   └── portfolio_agent/
│       ├── agents/           # Agent definitions
│       │   ├── coordinator.py
│       │   ├── ticker_resolver.py
│       │   ├── fundamental_analyst.py
│       │   ├── technical_analyst.py
│       │   ├── news_analyst.py
│       │   └── report_generator.py
│       ├── tools/            # Agent tools
│       │   ├── market_data.py
│       │   ├── fundamental_analysis.py
│       │   ├── technical_analysis.py
│       │   └── ticker_resolution.py
│       ├── models/           # Pydantic schemas
│       │   ├── stock_data.py
│       │   ├── analysis.py
│       │   ├── report.py
│       │   └── state.py
│       ├── prompts/          # Jinja prompt templates
│       │   ├── loader.py
│       │   └── ... jinja files
│       ├── config/
│       │   └── settings.py
│       └── main.py
├── tests/                    # Test suite
│   ├── __init__.py
│   └── test_basic.py
├── pyproject.toml            # Project dependencies & scripts metadata
├── .env.example
└── README.md
```

---

## Agents Overview

### 1. Research Coordinator
- Orchestrates the entire research workflow.
- Routes queries to appropriate specialist agents.
- Synthesizes final recommendations.

### 2. Ticker Resolver
- Converts natural language to stock tickers (e.g., "analyze Apple" → "AAPL").

### 3. Fundamental Analyst
- Analyzes financial statements and valuation ratios (P/E, P/B, etc.).
- Evaluates profitability and growth metrics.

### 4. Technical Analyst
- Analyzes price trends, support/resistance levels, and indicators (RSI, MACD, SMAs).

### 5. News Sentiment Analyst
- Integrates Google Search grounding to retrieve and analyze recent news.
- Evaluates market sentiment.

### 6. Report Generator
- Synthesizes all findings into a structured, markdown-formatted investment report.

---

## Development & Testing

### Running Tests
The project uses `pytest` and `pytest-asyncio` for testing:
```bash
uv run pytest tests/
```

### Code Formatting & Linting
```bash
# Check formatting
uv run ruff check src/

# Format code
uv run black src/
```

---

## Troubleshooting & Debugging

### Enable Debug Logging
If you need to trace how the LLM or ADK runners process events internally, enable debug logging by adding this at the top of `src/portfolio_agent/main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Common Issues

* **Issue: "GOOGLE_API_KEY is required"**
  * **Solution:** Verify that your `.env` file exists in the root directory, matches `.env.example`, and has a valid key configured without quotes.

* **Issue: Yahoo Finance rate limits**
  * **Solution:** Yahoo Finance API has transient rate limits. Wait a few minutes or reduce the frequency of query runs.

* **Issue: Import/Module errors in IDE (like red underlines)**
  * **Solution:** Run `uv sync --all-extras` in your workspace terminal to ensure all optional dev packages like `pytest` are fully installed in the local virtual environment.

---

## Limitations

- Data from Yahoo Finance may be delayed by 15-20 minutes.
- Focuses on US stocks initially.
- Uses `InMemorySessionService` (no persistence across restarts).
- Free tier API rate-limiting restrictions apply.

---

## License

MIT License
