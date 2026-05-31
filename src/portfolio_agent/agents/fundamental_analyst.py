"""Fundamental Analysis Agent - analyzes financial statements and metrics."""

from google.adk.agents import Agent
from portfolio_agent.config.settings import settings
from portfolio_agent.tools.market_data import get_financial_statements
from portfolio_agent.tools.financial_calc import (
    calculate_valuation_ratios,
    calculate_profitability_metrics,
    calculate_growth_metrics,
    get_comprehensive_financial_metrics
)


def create_fundamental_analyst() -> Agent:
    """
    Creates the Fundamental Analysis Agent.
    
    This agent analyzes company financials, assesses valuation,
    and compares metrics to industry standards.
    
    Returns:
        Agent: Configured fundamental analyst agent
    """
    
    agent = Agent(
        name="fundamental_analyst",
        model=settings.SPECIALIST_MODEL,
        description=(
            "Performs fundamental analysis on stocks, evaluating financial health, "
            "valuation ratios, profitability metrics, and growth potential. "
            "Analyzes income statements, balance sheets, and cash flow statements."
        ),
        instruction="""You are a Fundamental Analysis Specialist with expertise in financial statement analysis.

Your responsibilities:
1. Use get_comprehensive_financial_metrics() to gather all financial data for the stock
2. Analyze valuation ratios (P/E, P/B, P/S, PEG, EV/EBITDA)
3. Evaluate profitability (margins, ROE, ROA)
4. Assess growth metrics (revenue growth, earnings growth)
5. Identify financial strengths and concerns
6. Provide valuation assessment (undervalued, fairly valued, or overvalued)

When analyzing:
- Compare ratios to industry averages and historical norms
- Consider both absolute values and trends
- Identify red flags (high debt, declining margins, negative cash flow)
- Highlight competitive advantages (high ROE, strong margins, consistent growth)
- Be objective and data-driven in your assessment

Return a structured analysis with:
- Valuation assessment
- Key strengths (list of positive financial indicators)
- Key concerns (list of risks or weaknesses)
- Overall fundamental score or rating

If tools fail, explain what data is missing and provide analysis based on available information.
""",
        tools=[
            get_financial_statements,
            calculate_valuation_ratios,
            calculate_profitability_metrics,
            calculate_growth_metrics,
            get_comprehensive_financial_metrics,
        ],
    )
    
    return agent
