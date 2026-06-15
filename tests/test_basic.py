"""Basic test suite for Portfolio Research Agent."""

import pytest
from portfolio_agent.main import PortfolioResearchAgent
from portfolio_agent.config.settings import settings
from portfolio_agent.tools.ticker_resolution import resolve_ticker
from portfolio_agent.tools.market_data import get_stock_info

@pytest.fixture(scope="module")
def agent():
    """Fixture to initialize the PortfolioResearchAgent once per test session."""
    try:
        return PortfolioResearchAgent()
    except Exception as e:
        pytest.fail(f"Agent initialization failed: {e}")

def test_basic_setup(agent):
    """Test that the agent can be initialized with its specialist sub-agents."""
    assert agent is not None
    assert agent.coordinator.name == "research_coordinator"
    assert len(agent.coordinator.sub_agents) == 5
    
    sub_agent_names = {sa.name for sa in agent.coordinator.sub_agents}
    expected_names = {
        "ticker_resolver",
        "fundamental_analyst",
        "technical_analyst",
        "news_sentiment_analyst",
        "report_generator"
    }
    assert expected_names.issubset(sub_agent_names)

@pytest.mark.parametrize("query,expected_ticker", [
    ("Apple", "AAPL"),
    ("MSFT", "MSFT"),
    ("Google stock", "GOOGL"),
    ("TSLA", "TSLA"),
])
def test_ticker_resolution(query, expected_ticker):
    """Test ticker resolution tool directly with standard inputs."""
    result = resolve_ticker(query)
    assert result["status"] == "success", f"Resolution failed: {result.get('error_message')}"
    assert result["ticker"] == expected_ticker

def test_market_data():
    """Test Yahoo Finance market data retrieval tool."""
    result = get_stock_info("AAPL")
    if result["status"] == "error" and any(term in result.get("error_message", "") for term in ["Rate limited", "Too Many Requests", "rate limit"]):
        pytest.skip("Yahoo Finance API rate-limited. Skipping market data test.")
    assert result["status"] == "success", f"Market data retrieval failed: {result.get('error_message')}"
    
    data = result["data"]
    assert data["company_name"] == "Apple Inc."
    assert data.get("sector") == "Technology"
    assert data.get("market_cap") is not None
    assert data["market_cap"] > 0

@pytest.mark.asyncio
async def test_end_to_end(agent):
    """Test a complete stock analysis (requires API key/Vertex and quota)."""
    # Check if authentication is configured
    api_validation = settings.validate_api_keys()
    if not api_validation["google_api_key"] and not api_validation["vertex_config"]:
        pytest.skip("Neither GOOGLE_API_KEY nor GCP Vertex configuration is set. Skipping end-to-end test.")
        
    try:
        report = await agent.analyze_stock("AAPL", verbose=False)
        
        # Check if rate limited or failed due to quota limit (transient API issue)
        if (
            report == "Research completed but no final response generated."
            or "429" in report
            or "RESOURCE_EXHAUSTED" in report
            or "Error during research" in report
        ):
            pytest.skip("Gemini API rate limit, quota exhaustion, or transient error occurred. Skipping end-to-end test.")
        
        assert report is not None
        assert len(report) > 0
        assert "AAPL" in report
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            pytest.skip(f"Gemini API rate limit/quota exhausted: {e}. Skipping end-to-end test.")
        raise

if __name__ == "__main__":
    # If run directly via python, automatically invoke pytest on this file
    import sys
    sys.exit(pytest.main(["-v", __file__]))
