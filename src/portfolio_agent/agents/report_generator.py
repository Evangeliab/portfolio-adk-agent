"""Report Generator Agent - synthesizes research into comprehensive investment report."""

import logging
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext
from portfolio_agent.config.settings import settings
from datetime import datetime
from portfolio_agent.prompts.loader import load_prompt


def read_session_state(tool_context: ToolContext) -> dict:
    """
    Tool to read accumulated session state from previous analyses.
    
    Args:
        tool_context: Context containing session state
    
    Returns:
        dict: Session state with all research findings
    """
    logging.info("--- Tool: read_session_state called ---")
    
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
    
    instruction = load_prompt(
        "report_generator.jinja",
        current_date=datetime.now().strftime("%Y-%m-%d")
    )
    
    agent = Agent(
        name="report_generator",
        model=settings.COORDINATOR_MODEL,  # Use more capable model for synthesis
        description=(
            "Generates comprehensive investment reports by synthesizing fundamental analysis, "
            "technical analysis, and news sentiment findings into cohesive recommendations."
        ),
        instruction=instruction,
        tools=[read_session_state],
    )
    
    return agent
