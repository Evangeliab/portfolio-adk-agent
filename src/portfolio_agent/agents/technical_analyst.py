"""Technical Analysis Agent - analyzes price trends and indicators."""

import logging
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
from portfolio_agent.prompts.loader import load_prompt


def create_technical_analyst() -> Agent:
    """
    Creates the Technical Analysis Agent.
    
    This agent analyzes price trends, calculates technical indicators,
    and identifies chart patterns and support/resistance levels.
    
    Returns:
        Agent: Configured technical analyst agent
    """
    
    instruction = load_prompt("technical_analyst.jinja")
    
    agent = Agent(
        name="technical_analyst",
        model=settings.SPECIALIST_MODEL,
        description=(
            "Performs technical analysis on stocks, evaluating price trends, "
            "momentum indicators, moving averages, and chart patterns. "
            "Identifies support/resistance levels and provides trading signals."
        ),
        instruction=instruction,
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
