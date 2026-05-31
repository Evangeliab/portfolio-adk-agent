"""Technical Analysis Agent - analyzes price trends and indicators."""

from google.adk.agents import Agent
from portfolio_agent.config.settings import settings
from portfolio_agent.tools.market_data import get_price_history
from portfolio_agent.tools.technical_analysis import (
    calculate_moving_averages,
    calculate_rsi,
    calculate_macd,
    identify_support_resistance,
    get_comprehensive_technical_indicators
)


def create_technical_analyst() -> Agent:
    """
    Creates the Technical Analysis Agent.
    
    This agent analyzes price trends, calculates technical indicators,
    and identifies chart patterns and support/resistance levels.
    
    Returns:
        Agent: Configured technical analyst agent
    """
    
    agent = Agent(
        name="technical_analyst",
        model=settings.SPECIALIST_MODEL,
        description=(
            "Performs technical analysis on stocks, evaluating price trends, "
            "momentum indicators, moving averages, and chart patterns. "
            "Identifies support/resistance levels and provides trading signals."
        ),
        instruction="""You are a Technical Analysis Specialist with expertise in chart analysis and technical indicators.

Your responsibilities:
1. First, use get_price_history() to retrieve price data for the stock
2. Then use get_comprehensive_technical_indicators() with the price data to calculate all indicators
3. Analyze trend direction (bullish, bearish, or neutral)
4. Evaluate momentum indicators (RSI, MACD)
5. Assess moving average positions and crossovers
6. Identify support and resistance levels
7. Generate buy/sell signals based on technical analysis

When analyzing:
- RSI: Below 30 is oversold (bullish), above 70 is overbought (bearish)
- MACD: Positive histogram is bullish, negative is bearish
- Moving Averages: Price above SMAs is bullish, below is bearish
- Golden Cross (50 SMA crosses above 200 SMA) is very bullish
- Death Cross (50 SMA crosses below 200 SMA) is very bearish
- Consider multiple timeframes and indicators for confirmation

Return a structured analysis with:
- Overall trend (bullish/bearish/neutral) and strength
- Buy signals (list of bullish indicators)
- Sell signals (list of bearish indicators)
- Support and resistance levels
- Technical summary with actionable insights

Be specific about indicator values and what they suggest for short-term and medium-term price action.
If some indicators cannot be calculated due to insufficient data, work with what's available.
""",
        tools=[
            get_price_history,
            calculate_moving_averages,
            calculate_rsi,
            calculate_macd,
            identify_support_resistance,
            get_comprehensive_technical_indicators,
        ],
    )
    
    return agent
