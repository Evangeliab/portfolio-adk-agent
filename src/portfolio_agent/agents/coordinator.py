"""Research Coordinator Agent - orchestrates the multi-agent research workflow."""

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types
from typing import Optional
from portfolio_agent.config.settings import settings
from portfolio_agent.agents.ticker_resolver import create_ticker_resolver
from portfolio_agent.agents.fundamental_analyst import create_fundamental_analyst
from portfolio_agent.agents.technical_analyst import create_technical_analyst
from portfolio_agent.agents.news_analyst import create_news_sentiment_analyst
from portfolio_agent.agents.report_generator import create_report_generator
import logging
from portfolio_agent.prompts.loader import load_prompt


def input_validation_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    Validates user input before processing.
    Blocks empty queries or obvious invalid requests.
    
    Args:
        callback_context: Context with agent and session info
        llm_request: The request about to be sent to the LLM
    
    Returns:
        LlmResponse to block the request, or None to allow it
    """
    agent_name = callback_context.agent_name
    logging.info(f"--- Callback: input_validation_callback for agent: {agent_name} ---")
    
    # Extract the last user message
    last_user_message = ""
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.role == 'user' and content.parts:
                if content.parts[0].text:
                    last_user_message = content.parts[0].text.strip()
                    break
    
    logging.info(f"--- Callback: Validating message: '{last_user_message[:100]}...' ---")
    
    # Block empty queries
    if not last_user_message or len(last_user_message) < 3:
        logging.warning("--- Callback: Blocking empty/too short query ---")
        return LlmResponse(
            content=types.Content(
                role="model",
                parts=[types.Part(
                    text="Please provide a valid stock ticker or company name to analyze. "
                         "For example: 'analyze Apple stock' or 'research MSFT'"
                )],
            )
        )
    
    # Allow the request
    logging.info("--- Callback: Request approved ---")
    return None


def create_research_coordinator() -> Agent:
    """
    Creates the Research Coordinator Agent (root agent).
    
    This agent orchestrates the entire research workflow:
    1. Resolves natural language queries to ticker symbols
    2. Delegates to specialist agents (fundamental, technical, news)
    3. Coordinates report generation
    4. Manages session state throughout the workflow
    
    Returns:
        Agent: Configured research coordinator agent with all sub-agents
    """
    
    # Create all sub-agents
    ticker_resolver = create_ticker_resolver()
    fundamental_analyst = create_fundamental_analyst()
    technical_analyst = create_technical_analyst()
    news_analyst = create_news_sentiment_analyst()
    report_generator = create_report_generator()
    
    # Load instruction from Jinja template
    instruction = load_prompt("coordinator.jinja")
    
    agent = Agent(
        name="research_coordinator",
        model=settings.COORDINATOR_MODEL,
        description=(
            "Main coordinator for stock research. Handles natural language queries, "
            "resolves ticker symbols, delegates to specialist agents, and orchestrates "
            "comprehensive investment research workflow."
        ),
        instruction=instruction,
        sub_agents=[
            ticker_resolver,
            fundamental_analyst,
            technical_analyst,
            news_analyst,
            report_generator
        ],
        before_model_callback=input_validation_callback
    )
    
    return agent
