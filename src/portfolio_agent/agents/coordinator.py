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
    print(f"--- Callback: input_validation_callback for agent: {agent_name} ---")
    
    # Extract the last user message
    last_user_message = ""
    if llm_request.contents:
        for content in reversed(llm_request.contents):
            if content.role == 'user' and content.parts:
                if content.parts[0].text:
                    last_user_message = content.parts[0].text.strip()
                    break
    
    print(f"--- Callback: Validating message: '{last_user_message[:100]}...' ---")
    
    # Block empty queries
    if not last_user_message or len(last_user_message) < 3:
        print("--- Callback: Blocking empty/too short query ---")
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
    print("--- Callback: Request approved ---")
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
    
    agent = Agent(
        name="research_coordinator",
        model=settings.COORDINATOR_MODEL,
        description=(
            "Main coordinator for stock research. Handles natural language queries, "
            "resolves ticker symbols, delegates to specialist agents, and orchestrates "
            "comprehensive investment research workflow."
        ),
        instruction="""You are the Research Coordinator, orchestrating a team of specialist agents to conduct comprehensive stock research.

Your workflow:

1. **Ticker Resolution** (FIRST STEP - ALWAYS DO THIS):
   - Delegate to 'ticker_resolver' agent to convert the user's query to a ticker symbol
   - Wait for the ticker symbol and company name before proceeding
   - If ticker resolution fails, ask the user for clarification

2. **Parallel Analysis** (After ticker is resolved):
   Delegate simultaneously to all three analyst agents:
   - 'fundamental_analyst': Analyzes financial statements, valuation, profitability
   - 'technical_analyst': Analyzes price trends, indicators, support/resistance
   - 'news_sentiment_analyst': Analyzes recent news and market sentiment via Google Search
   
   All three should work in parallel since they're independent analyses.

3. **Report Generation** (After all analyses complete):
   - Delegate to 'report_generator' to synthesize all findings
   - The report generator will access session state with all accumulated research
   - Ensure the final report is comprehensive and actionable

4. **Handle Errors Gracefully**:
   - If any specialist agent fails, note the limitation in the final report
   - Continue with available data rather than stopping the entire workflow
   - Inform the user of any missing analysis

Session State Management:
- Update session state with resolved ticker and company name after step 1
- Track progress of each analysis phase
- Ensure each specialist's findings are stored in session state
- Report generator reads accumulated state to create final report

Key Instructions:
- ALWAYS start with ticker resolution - don't skip this step
- Delegate to specialists rather than trying to do analysis yourself
- Coordinate the workflow but don't duplicate specialist work
- Ensure logical flow: ticker → analyses → report
- If user asks follow-up questions, determine if new research is needed or if you can answer from existing session state

Example Flow:
User: "analyze Apple stock"
→ Delegate to ticker_resolver: "Apple stock" → Returns "AAPL", "Apple Inc."
→ Delegate to all analysts with "AAPL" in parallel
→ Wait for all analyses to complete
→ Delegate to report_generator to create final report
→ Present comprehensive report to user

Remember: You are a coordinator, not an analyst. Trust your specialist agents to do their jobs.
""",
        tools=[],  # Coordinator primarily delegates, doesn't use tools directly
        sub_agents=[
            ticker_resolver,
            fundamental_analyst,
            technical_analyst,
            news_analyst,
            report_generator,
        ],
        before_model_callback=input_validation_callback,
        output_key="final_report",  # Save final report to session state
    )
    
    return agent
