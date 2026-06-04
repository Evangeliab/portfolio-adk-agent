"""Fundamental Analysis Agent - analyzes financial statements and metrics."""

import logging
from google.adk.agents import Agent
from portfolio_agent.config.settings import settings
from portfolio_agent.tools.market_data import get_financial_statements
from portfolio_agent.tools.financial_calc import (
    calculate_valuation_ratios,
    calculate_profitability_metrics,
    calculate_growth_metrics,
    get_comprehensive_financial_metrics
)
from portfolio_agent.prompts.loader import load_prompt


def create_fundamental_analyst() -> Agent:
    """
    Creates the Fundamental Analysis Agent.
    
    This agent analyzes company financials, assesses valuation,
    and compares metrics to industry standards.
    
    Returns:
        Agent: Configured fundamental analyst agent
    """
    
    instruction = load_prompt("fundamental_analyst.jinja")
    
    agent = Agent(
        name="fundamental_analyst",
        model=settings.SPECIALIST_MODEL,
        description=(
            "Performs fundamental analysis on stocks, evaluating financial health, "
            "valuation ratios, profitability metrics, and growth potential. "
            "Analyzes income statements, balance sheets, and cash flow statements."
        ),
        instruction=instruction,
        tools=[
            get_financial_statements,
            calculate_valuation_ratios,
            calculate_profitability_metrics,
            calculate_growth_metrics,
            get_comprehensive_financial_metrics,
        ],
    )
    
    return agent
