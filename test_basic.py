"""Simple test to verify basic functionality."""

import asyncio
from portfolio_agent.main import PortfolioResearchAgent
from portfolio_agent.config.settings import settings


async def test_basic_setup():
    """Test that the agent can be initialized."""
    print("Testing agent initialization...")
    
    try:
        agent = PortfolioResearchAgent()
        print("✅ Agent initialized successfully")
        print(f"   - Coordinator agent: {agent.coordinator.name}")
        print(f"   - Sub-agents: {len(agent.coordinator.sub_agents)}")
        for sub_agent in agent.coordinator.sub_agents:
            print(f"     • {sub_agent.name}")
        return True
    except Exception as e:
        print(f"❌ Agent initialization failed: {str(e)}")
        return False


async def test_ticker_resolution():
    """Test ticker resolution tool directly."""
    print("\nTesting ticker resolution...")
    
    from portfolio_agent.tools.ticker_resolver import resolve_ticker
    
    test_queries = ["Apple", "MSFT", "Google stock", "TSLA"]
    
    for query in test_queries:
        result = resolve_ticker(query)
        if result["status"] == "success":
            print(f"✅ '{query}' → {result['ticker']} ({result['company_name']})")
        else:
            print(f"⚠️  '{query}' → {result.get('error_message', 'Unknown error')}")


async def test_market_data():
    """Test market data retrieval."""
    print("\nTesting market data retrieval...")
    
    from portfolio_agent.tools.market_data import get_stock_info
    
    result = get_stock_info("AAPL")
    if result["status"] == "success":
        data = result["data"]
        print(f"✅ Retrieved data for: {data['company_name']}")
        print(f"   - Sector: {data.get('sector', 'N/A')}")
        print(f"   - Market Cap: ${data.get('market_cap', 0):,.0f}" if data.get('market_cap') else "   - Market Cap: N/A")
    else:
        print(f"❌ Failed: {result.get('error_message')}")


async def test_end_to_end():
    """Test a complete stock analysis (requires API key)."""
    print("\nTesting end-to-end analysis...")
    print("(This will make a real API call and may take 30-60 seconds)")
    
    # Check if API key is set
    if not settings.GOOGLE_API_KEY or settings.GOOGLE_API_KEY == "your_google_api_key_here":
        print("⚠️  Skipping end-to-end test: GOOGLE_API_KEY not configured")
        print("   Set your API key in .env to run this test")
        return
    
    try:
        agent = PortfolioResearchAgent()
        
        # Run a simple analysis
        print("\n" + "="*60)
        print("Running analysis for 'AAPL'...")
        print("="*60)
        
        report = await agent.analyze_stock("AAPL", verbose=True)
        
        print("\n" + "="*60)
        print("Analysis completed!")
        print("="*60)
        print(f"\nReport preview (first 500 chars):\n{report[:500]}...")
        print("\n✅ End-to-end test passed!")
        
    except Exception as e:
        print(f"\n❌ End-to-end test failed: {str(e)}")
        import traceback
        traceback.print_exc()


async def main():
    """Run all tests."""
    print("="*60)
    print("Portfolio Research Agent - Test Suite")
    print("="*60)
    
    # Test 1: Basic setup
    setup_ok = await test_basic_setup()
    if not setup_ok:
        print("\n⚠️  Basic setup failed. Please check your installation.")
        return
    
    # Test 2: Ticker resolution
    await test_ticker_resolution()
    
    # Test 3: Market data
    await test_market_data()
    
    # Test 4: End-to-end (optional, requires API key)
    response = input("\nRun full end-to-end test? This requires a valid GOOGLE_API_KEY (y/n): ")
    if response.lower() == 'y':
        await test_end_to_end()
    else:
        print("Skipping end-to-end test")
    
    print("\n" + "="*60)
    print("Tests completed!")
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
