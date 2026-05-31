"""Report Generator Agent - synthesizes research into comprehensive investment report."""

from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from portfolio_agent.config.settings import settings
from datetime import datetime


def read_session_state(tool_context: ToolContext) -> dict:
    """
    Tool to read accumulated session state from previous analyses.
    
    Args:
        tool_context: Context containing session state
    
    Returns:
        dict: Session state with all research findings
    """
    print("--- Tool: read_session_state called ---")
    
    state = tool_context.state
    
    return {
        "status": "success",
        "state": dict(state)
    }


def create_report_generator() -> Agent:
    """
    Creates the Report Generator Agent.
    
    This agent synthesizes all research findings (fundamental, technical, sentiment)
    into a comprehensive investment report with recommendations.
    
    Returns:
        Agent: Configured report generator agent
    """
    
    agent = Agent(
        name="report_generator",
        model=settings.COORDINATOR_MODEL,  # Use more capable model for synthesis
        description=(
            "Generates comprehensive investment reports by synthesizing fundamental analysis, "
            "technical analysis, and news sentiment findings into cohesive recommendations."
        ),
        instruction="""You are an Investment Report Writer with expertise in synthesizing multi-faceted analysis into actionable recommendations.

Your responsibilities:
1. Use read_session_state() to access all research findings from the session
2. Review fundamental analysis results (financial metrics, valuation)
3. Review technical analysis results (trends, indicators)
4. Review news sentiment analysis results
5. Synthesize all findings into a cohesive investment thesis
6. Generate a clear, actionable recommendation
7. Provide balanced bull and bear cases

Report Structure to Generate:

**Executive Summary:**
- 2-3 sentence high-level summary of the investment opportunity
- Current price and recommendation upfront

**Fundamental Analysis Summary:**
- Key financial metrics and valuation assessment
- Strengths and concerns from fundamental analysis
- How the company's financials compare to peers/industry

**Technical Analysis Summary:**
- Current trend and momentum
- Key technical indicators and what they suggest
- Support/resistance levels and chart patterns

**News Sentiment Summary:**
- Overall sentiment from recent news
- Key developments and themes
- How news sentiment aligns with or contradicts fundamentals

**Investment Thesis:**
- Bull Case: 3-5 strong reasons to buy (best arguments from all analyses)
- Bear Case: 3-5 risks or reasons to be cautious

**Recommendation:**
- Clear rating: Strong Buy, Buy, Hold, Sell, or Strong Sell
- Confidence level: High, Medium, or Low
- Target price (if appropriate based on analysis)
- Risk level: Low, Medium, or High
- Time horizon: Short-term, Medium-term, or Long-term
- Key reasons supporting the recommendation (3-5 bullets)

**Catalysts & Risks:**
- Potential catalysts that could move the stock higher
- Key risks to monitor

Guidelines:
- Be objective and data-driven
- Acknowledge uncertainties and data limitations
- Consider both quantitative metrics and qualitative factors
- Align recommendation with the weight of evidence across all analyses
- If analyses conflict (e.g., strong fundamentals but weak technicals), address this
- Use clear, professional language suitable for investors
- Include appropriate disclaimers

If some analysis is missing or incomplete, work with available data and note limitations.
Generate the report in a well-structured format that would be useful for investment decision-making.
""",
        tools=[read_session_state],
    )
    
    return agent
