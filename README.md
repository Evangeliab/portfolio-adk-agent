# Stock Research Multi-Agent System

A sophisticated multi-agent investment research system built with Google's ADK (Agent Development Kit) framework. The system analyzes stocks through fundamental analysis, technical analysis, and news sentiment, then generates comprehensive investment reports.

## Features

- 🤖 **Multi-Agent Architecture**: Specialized agents for different analysis types
- 💬 **Natural Language Queries**: Ask "analyze Apple stock" instead of needing ticker symbols
- 📊 **Comprehensive Analysis**:
  - Fundamental analysis (financial metrics, valuation ratios)
  - Technical analysis (moving averages, RSI, MACD)
  - News sentiment (via Google Search grounding)
- 📝 **Detailed Reports**: AI-generated investment reports with recommendations
- 🔄 **Session State**: Tracks research progress across agent interactions

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

## Prerequisites

- Python 3.11 or higher
- [UV](https://github.com/astral-sh/uv) package manager
- Google API Key (for Gemini models and Google Search grounding)
- Optional: OpenAI or Anthropic API keys for multi-model support

## Installation

1. **Clone the repository** (or navigate to project directory)

2. **Install UV** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Create and activate virtual environment with UV**:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   uv sync
   ```

5. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

## Configuration

Edit `.env` file with your API keys:

```env
# Required
GOOGLE_API_KEY=your_google_api_key_here

# Optional (for multi-model support)
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

Get your Google API key from: https://aistudio.google.com/app/apikey

## Usage

### CLI Interface

Run a stock analysis:

```bash
uv run python -m portfolio_agent.main "analyze apple stock"
```

Or with a direct ticker:

```bash
uv run python -m portfolio_agent.main "research MSFT"
```

### Example Queries

```bash
# Natural language
uv run python -m portfolio_agent.main "analyze Tesla"
uv run python -m portfolio_agent.main "what do you think about Microsoft stock?"
uv run python -m portfolio_agent.main "research NVIDIA"

# Direct ticker symbols
uv run python -m portfolio_agent.main "analyze AAPL"
uv run python -m portfolio_agent.main "TSLA analysis"
```

## Project Structure

```
portfolio_management_agent/
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
│       │   ├── financial_calc.py
│       │   ├── technical_analysis.py
│       │   ├── ticker_resolver.py
│       │   └── news_search.py
│       ├── models/           # Pydantic schemas
│       │   ├── stock_data.py
│       │   ├── analysis.py
│       │   ├── reports.py
│       │   └── state.py
│       ├── config/
│       │   └── settings.py
│       └── main.py
├── tests/
├── pyproject.toml
└── README.md
```

## Agents

### 1. Research Coordinator
- Orchestrates the entire research workflow
- Routes queries to appropriate specialist agents
- Synthesizes final recommendations

### 2. Ticker Resolver
- Converts natural language to stock tickers
- Handles queries like "analyze Apple" → "AAPL"

### 3. Fundamental Analyst
- Analyzes financial statements
- Calculates valuation ratios (P/E, P/B, etc.)
- Evaluates profitability and growth metrics

### 4. Technical Analyst
- Analyzes price trends and patterns
- Calculates technical indicators (RSI, MACD, moving averages)
- Identifies support/resistance levels

### 5. News Sentiment Analyst
- Uses Google Search grounding for recent news
- Analyzes sentiment and key themes
- Identifies market-moving developments

### 6. Report Generator
- Synthesizes all findings
- Generates comprehensive investment report
- Provides actionable recommendations

## Technologies

- **Google ADK**: Multi-agent framework
- **Gemini**: LLM for agent intelligence
- **Yahoo Finance**: Market data source
- **Pydantic**: Data validation
- **UV**: Fast Python package manager

## Development

### Running Tests

```bash
uv run pytest
```

### Code Formatting

```bash
uv run black src/
uv run ruff check src/
```

## Limitations

- Data from Yahoo Finance may be delayed 15-20 minutes
- Focuses on US stocks initially
- Uses InMemorySessionService (no persistence across restarts)
- Free data sources only (no Bloomberg/Reuters integration)

## Future Enhancements

- [ ] Portfolio-level analysis (multiple stocks)
- [ ] Backtesting strategies
- [ ] Real-time alerting
- [ ] Web UI interface
- [ ] Database persistence
- [ ] International market support
- [ ] Integration with brokerage APIs

## License

MIT License

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
