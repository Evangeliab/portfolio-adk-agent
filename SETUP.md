# Setup Guide

## Quick Start

### 1. Install UV (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using Homebrew
brew install uv
```

### 2. Clone/Navigate to Project

```bash
cd /Users/bf40fo/PycharmProjects/portfolio_management_agent
```

### 3. Create Virtual Environment and Install Dependencies

```bash
# Create virtual environment with UV
uv venv

# Activate the virtual environment
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate    # On Windows

# Install all dependencies
uv sync
```

This will install:
- google-adk (Agent Development Kit)
- pydantic (data validation)
- yfinance (market data)
- pandas, numpy (data processing)
- python-dotenv (environment variables)

### 4. Configure API Keys

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Google API key
nano .env  # or use your preferred editor
```

**Required:** Add your Google API key:
```env
GOOGLE_API_KEY=your_actual_google_api_key_here
```

**Get your Google API key:**
1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key and paste it into `.env`

**Optional:** Add OpenAI or Anthropic keys for multi-model support (not required)

### 5. Test the Installation

```bash
# Test that everything is set up correctly
python -c "from portfolio_agent.config.settings import settings; print('✅ Setup successful!')"
```

### 6. Run Your First Stock Analysis

```bash
# Analyze Apple stock
uv run python -m portfolio_agent.main "analyze Apple stock"

# Or try with a direct ticker
uv run python -m portfolio_agent.main "research MSFT"

# Or conversational query
uv run python -m portfolio_agent.main "what do you think about Tesla?"
```

## Common Issues & Solutions

### Issue: "GOOGLE_API_KEY is required"
**Solution:** Make sure you've:
1. Created the `.env` file from `.env.example`
2. Added your actual Google API key (not the placeholder text)
3. The `.env` file is in the project root directory

### Issue: "Module not found" errors
**Solution:** 
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
uv sync
```

### Issue: Yahoo Finance rate limits
**Solution:** Yahoo Finance has rate limits. If you hit them:
- Wait a few minutes before retrying
- Reduce the number of requests
- Consider caching results for frequently queried stocks

### Issue: Google Search grounding not working
**Solution:** 
1. Ensure your Google API key has Google Search API enabled
2. Check your Google Cloud Console for API quotas
3. If needed, disable grounding temporarily in `config/settings.py`:
   ```python
   ENABLE_GOOGLE_SEARCH_GROUNDING = False
   ```

## Project Structure

```
portfolio_management_agent/
├── src/
│   └── portfolio_agent/
│       ├── agents/           # Agent definitions
│       │   ├── coordinator.py          # Main orchestrator
│       │   ├── ticker_resolver.py      # Ticker resolution
│       │   ├── fundamental_analyst.py  # Financial analysis
│       │   ├── technical_analyst.py    # Technical analysis
│       │   ├── news_analyst.py         # News sentiment
│       │   └── report_generator.py     # Report synthesis
│       ├── tools/            # Agent tools
│       │   ├── market_data.py          # Yahoo Finance data
│       │   ├── financial_calc.py       # Financial metrics
│       │   ├── technical_analysis.py   # Technical indicators
│       │   ├── ticker_resolver.py      # Ticker resolution
│       │   └── news_search.py          # Google Search integration
│       ├── models/           # Pydantic models
│       │   ├── stock_data.py           # Company/price data models
│       │   ├── analysis.py             # Analysis result models
│       │   ├── reports.py              # Report models
│       │   └── state.py                # Session state
│       ├── config/
│       │   └── settings.py             # Configuration
│       └── main.py                     # Application entry point
├── tests/                    # Test suite (to be added)
├── pyproject.toml           # Project dependencies
├── .env                     # Your API keys (create from .env.example)
├── .env.example             # Template for environment variables
└── README.md                # Project documentation
```

## Next Steps

1. **Try Different Queries:**
   ```bash
   uv run python -m portfolio_agent.main "analyze NVDA"
   uv run python -m portfolio_agent.main "research Amazon"
   uv run python -m portfolio_agent.main "what's the investment case for Netflix?"
   ```

2. **Customize Models:**
   - Edit `src/portfolio_agent/config/settings.py`
   - Change `SPECIALIST_MODEL` or `COORDINATOR_MODEL`
   - Try different Gemini models or use OpenAI/Anthropic

3. **Extend Functionality:**
   - Add new tools in `src/portfolio_agent/tools/`
   - Create new specialist agents
   - Enhance the report format
   - Add more technical indicators

4. **Add Persistence:**
   - Replace `InMemorySessionService` with a database-backed service
   - Store historical research reports
   - Cache market data to reduce API calls

5. **Build a Web UI:**
   - Use ADK's `adk web` command (requires additional setup)
   - Or integrate with FastAPI/Flask
   - Create a dashboard for portfolio tracking

## Troubleshooting

### Enable Debug Logging

Edit `src/portfolio_agent/main.py` to see more details:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Tool Execution

Look for lines like:
```
--- Tool: get_stock_info called for ticker: AAPL ---
--- Tool: Successfully retrieved info for Apple Inc. ---
```

### Verify Agent Delegation

You should see agents being invoked:
```
🤖 [ticker_resolver]: Resolved to AAPL...
🤖 [fundamental_analyst]: Analyzing financial metrics...
🤖 [technical_analyst]: Calculating technical indicators...
🤖 [news_sentiment_analyst]: Searching recent news...
🤖 [report_generator]: Synthesizing final report...
```

## Getting Help

If you encounter issues:
1. Check the error message carefully
2. Verify your `.env` file configuration
3. Make sure all dependencies are installed: `uv sync`
4. Check that your virtual environment is activated
5. Review the logs for tool execution failures

## Resources

- **ADK Documentation:** https://adk.dev/
- **Yahoo Finance Python:** https://pypi.org/project/yfinance/
- **Pydantic Documentation:** https://docs.pydantic.dev/
- **Google AI Studio:** https://aistudio.google.com/

---

**You're all set!** 🚀 Start analyzing stocks with your new multi-agent research system.
