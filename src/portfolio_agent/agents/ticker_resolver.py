"""Ticker Resolver Agent - converts natural language queries to stock tickers."""

import logging
from google.adk.agents import Agent
from portfolio_agent.config.settings import settings
from portfolio_agent.tools.ticker_resolver import resolve_ticker, validate_ticker
from portfolio_agent.prompts.loader import load_prompt


def create_ticker_resolver() -> Agent:
    """
    Creates the Ticker Resolver Agent.
    
    This agent converts natural language stock queries to ticker symbols.
    Handles queries like "analyze Apple", "Microsoft stock", etc.
    
    Returns:
        Agent: Configured ticker resolver agent
    """
    
    instruction = load_prompt("ticker_resolver.jinja")
    
    agent = Agent(
        name="ticker_resolver",
        model=settings.SPECIALIST_MODEL,
        description=(
            "Resolves company names and natural language queries to stock ticker symbols. "
            "Converts queries like 'Apple stock', 'analyze Microsoft', or 'Tesla' to ticker symbols like AAPL, MSFT, TSLA."
        ),
        instruction=instruction,
        tools=[resolve_ticker, validate_ticker],
    )
    
    return agent
