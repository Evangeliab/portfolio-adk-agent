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
- 🛡️ **Production-Ready Reliability**:
  - Automatic retry with exponential backoff (3 attempts)
  - Timeout protection (prevents infinite loops and hanging)
  - Comprehensive error handling with user-friendly messages
  - Data validation and edge case handling
  - TTL caching (5-minute fresh data, no stale results)
  - Handles API failures, network issues, and malformed data gracefully

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
│       │   ├── news_search.py
│       │   ├── retry_utils.py      # Retry logic
│       │   ├── yfinance_utils.py   # Timeout config
│       │   └── cache_utils.py      # TTL cache
│       ├── models/           # Pydantic schemas
│       │   ├── stock_data.py
│       │   ├── analysis.py
│       │   ├── reports.py
│       │   └── state.py
│       ├── prompts/          # Agent instruction templates
│       │   ├── coordinator.jinja
│       │   ├── ticker_resolver.jinja
│       │   ├── fundamental_analyst.jinja
│       │   ├── technical_analyst.jinja
│       │   ├── news_analyst.jinja
│       │   ├── report_generator.jinja
│       │   └── loader.py
│       ├── config/
│       │   ├── settings.py
│       │   └── logging_config.py
│       └── main.py
├── test_p1_fixes.py      # P1 critical tests
├── test_basic.py         # Basic integration tests
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

## Reliability & Robustness

The system includes production-grade reliability features:

### Error Handling & Recovery
- **Automatic Retry**: API failures automatically retry up to 3 times with exponential backoff (2-10s)
- **Timeout Protection**: All operations have timeouts (5s connect, 30s read, 180s analysis)
- **Graceful Degradation**: Failures return user-friendly error messages instead of crashes
- **Comprehensive Exception Handling**: Every component handles errors appropriately

### Data Quality & Validation
- **Input Validation**: Query validation, ticker format checks, data type verification
- **DataFrame Validation**: Validates required columns, checks for NaN values, validates OHLC relationships
- **Edge Case Handling**: Handles division by zero, missing data, delisted stocks, penny stocks
- **Price Validation**: Ensures positive prices, validates high ≥ low, detects anomalies

### Performance & Caching
- **TTL Cache**: 5-minute cache prevents stale data while improving performance
- **Smart Eviction**: LRU eviction when cache is full
- **No Error Caching**: Failed requests don't pollute the cache

### Testing
- **10 P1 Tests**: Comprehensive test suite for critical functionality
- **Edge Case Coverage**: Tests division by zero, all gains/losses, invalid data
- **Cache Testing**: Validates TTL expiry, eviction, hit/miss behavior

Run tests:
```bash
uv run pytest test_p1_fixes.py -v
```

## Technologies

- **Google ADK**: Multi-agent framework
- **Gemini**: LLM for agent intelligence
- **Yahoo Finance**: Market data source
- **Pydantic**: Data validation
- **Tenacity**: Retry logic with exponential backoff
- **UV**: Fast Python package manager
- **Pytest**: Testing framework

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run P1 critical tests with verbose output
uv run pytest test_p1_fixes.py -v

# Run with coverage
uv run pytest test_p1_fixes.py --cov=portfolio_agent.tools

# Run specific test class
uv run pytest test_p1_fixes.py::TestRSIEdgeCases -v
```

The test suite includes:
- **RSI Edge Cases**: Division by zero, all gains/losses, no movement, invalid data
- **TTL Cache**: Cache hit/miss, expiry, eviction, argument handling
- **Data Validation**: DataFrame validation, error handling

### Code Formatting

```bash
uv run black src/
uv run ruff check src/
```

### Verification

```bash
# Verify all imports work
python -c "from portfolio_agent.tools.retry_utils import yfinance_retry; \
from portfolio_agent.tools.yfinance_utils import create_yf_ticker; \
from portfolio_agent.tools.cache_utils import ttl_cache; \
print('✅ All utilities OK')"

# Test basic functionality (requires API key)
uv run python -m portfolio_agent.main "analyze AAPL"
```

## Limitations

- Data from Yahoo Finance may be delayed 15-20 minutes
- Focuses on US stocks initially (limited international ticker support)
- Uses InMemorySessionService (no persistence across restarts)
- Free data sources only (no Bloomberg/Reuters integration)
- News sentiment relies on Google Search grounding (quality depends on ADK capabilities)
- Ticker resolution limited to ~34 common companies (fuzzy matching not yet implemented)

## Known Reliable Behaviors

✅ **Handles gracefully:**
- API failures and network issues (automatic retry)
- Timeouts and hanging requests (automatic timeout)
- Invalid tickers and delisted stocks (clear error messages)
- Malformed data from Yahoo Finance (validation and filtering)
- Division by zero in technical indicators (edge case handling)
- Stale cached data (5-minute TTL)
- User input errors (validation with helpful feedback)

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
