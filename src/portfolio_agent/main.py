"""Main entry point for the Portfolio Research Agent."""

import asyncio
import sys
import logging
import json
from typing import Optional
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from portfolio_agent.config.settings import settings
from portfolio_agent.config.logging_config import setup_logging
from portfolio_agent.agents.coordinator import create_research_coordinator
from portfolio_agent.models.state import ResearchSessionState


class PortfolioResearchAgent:
    """Main application class for portfolio research."""
    
    def __init__(self):
        """Initialize the research agent."""
        try:
            # Setup logging
            setup_logging()
            logging.info("Initializing Portfolio Research Agent...")
            
            # Setup environment
            settings.setup_environment()
            
            # Validate API keys
            api_validation = settings.validate_api_keys()
            if not api_validation["google_api_key"]:
                logging.error("GOOGLE_API_KEY is required. Please set it in your .env file.")
                raise ValueError(
                    "GOOGLE_API_KEY is required. Please set it in your .env file. "
                    "Get your API key from: https://aistudio.google.com/app/apikey"
                )
            
            logging.info("✅ API keys validated")
            logging.info(f"📊 Using model: {settings.COORDINATOR_MODEL}")
            logging.info(f"🔍 Google Search grounding: {'Enabled' if settings.ENABLE_GOOGLE_SEARCH_GROUNDING else 'Disabled'}")
            
            # Create session service
            try:
                self.session_service = InMemorySessionService()
                logging.info("✅ Session service initialized")
            except Exception as e:
                raise RuntimeError(f"Failed to initialize session service: {e}")
            
            # Create coordinator agent
            try:
                self.coordinator = create_research_coordinator()
                logging.info(f"✅ Coordinator created with {len(self.coordinator.sub_agents)} agents")
            except Exception as e:
                raise RuntimeError(f"Failed to create coordinator agent: {e}")
            
            # Create runner
            try:
                self.runner = Runner(
                    agent=self.coordinator,
                    app_name=settings.APP_NAME,
                    session_service=self.session_service
                )
                logging.info("✅ Runner initialized")
            except Exception as e:
                raise RuntimeError(f"Failed to initialize runner: {e}")
                
        except ValueError as e:
            # Re-raise validation errors
            raise
        except Exception as e:
            logging.error(f"Failed to initialize Portfolio Research Agent: {e}")
            raise RuntimeError(f"Agent initialization failed: {e}") from e
        
    async def create_session(self, user_id: str, session_id: str, query: str) -> None:
        """
        Create a new research session.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            query: User's research query
        """
        try:
            # Initialize session with empty state
            initial_state = ResearchSessionState(query=query).model_dump()
            
            await self.session_service.create_session(
                app_name=settings.APP_NAME,
                user_id=user_id,
                session_id=session_id,
                state=initial_state
            )
            
            logging.info(f"✅ Session created: user_id={user_id}, session_id={session_id}")
            
        except Exception as e:
            logging.error(f"Failed to create session: {e}")
            raise RuntimeError(f"Session creation failed for {user_id}/{session_id}: {e}") from e
    
    async def analyze_stock(
        self, 
        query: str, 
        user_id: str = None,
        session_id: str = None,
        verbose: bool = True,
        timeout: int = 180
    ) -> str:
        """
        Analyze a stock based on user query with comprehensive error handling.
        
        Args:
            query: Natural language query or ticker symbol
            user_id: User identifier (optional, uses default if not provided)
            session_id: Session identifier (optional, generates new if not provided)
            verbose: Whether to print progress updates
            timeout: Maximum seconds to wait for completion (default 180)
        
        Returns:
            str: Final analysis report
            
        Raises:
            ValueError: If query is invalid
            TimeoutError: If analysis exceeds timeout
            RuntimeError: If analysis fails
        """
        # Validate inputs
        if not query or len(query.strip()) < 3:
            raise ValueError("Query must be at least 3 characters long")
        
        # Use defaults if not provided
        user_id = user_id or settings.DEFAULT_USER_ID
        session_id = session_id or f"session_{asyncio.get_event_loop().time():.0f}"
        
        try:
            # Create session
            await self.create_session(user_id, session_id, query)
            
            if verbose:
                logging.info(f"\n{'='*80}")
                logging.info(f"🔍 Starting stock research for: {query}")
                logging.info(f"{'='*80}\n")
            
            # Get initial state
            last_turn_id = None
            final_turn = False
            
            # Trigger the first turn
            try:
                await self.runner.run_turn(
                    user_id=user_id,
                    session_id=session_id,
                    llm_request_content=types.Content(
                        role="user", parts=[types.Part(text=query)]
                    ),
                )
            except Exception as e:
                logging.error(f"Failed to start analysis: {e}")
                raise RuntimeError(f"Failed to initiate analysis: {e}") from e
            
            # Wait for completion with timeout
            start_time = asyncio.get_event_loop().time()
            iteration = 0
            max_iterations = 200  # Safety limit
            
            if verbose:
                spinner = ['-', '\\', '|', '/']
                i = 0
            
            try:
                while not final_turn and iteration < max_iterations:
                    # Check timeout
                    elapsed = asyncio.get_event_loop().time() - start_time
                    if elapsed > timeout:
                        raise TimeoutError(
                            f"Analysis timed out after {timeout} seconds. "
                            f"The analysis may be too complex or services are slow."
                        )
                    
                    if verbose:
                        print(f"\r🤖 Thinking... {spinner[i % len(spinner)]} ({elapsed:.0f}s)", 
                              end="", flush=True)
                        await asyncio.sleep(0.2)
                        i += 1
                    else:
                        await asyncio.sleep(1)
                    
                    # Check for new turns
                    try:
                        new_turns = await self.runner.get_new_turns(
                            user_id=user_id,
                            session_id=session_id,
                            last_known_turn_id=last_turn_id
                        )
                    except Exception as e:
                        logging.error(f"Error checking for new turns: {e}")
                        raise RuntimeError(f"Failed to retrieve analysis progress: {e}") from e
                    
                    if new_turns:
                        last_turn_id = new_turns[-1].id
                        final_turn = self.runner.is_final_turn(new_turns[-1])
                    
                    iteration += 1
                
                if verbose:
                    print("\r" + " " * 50 + "\r", end="")  # Clear spinner
                
                # Check if we hit max iterations
                if iteration >= max_iterations:
                    raise RuntimeError(
                        f"Analysis exceeded maximum iterations ({max_iterations}). "
                        f"This may indicate an agent loop or stuck process."
                    )
            
            except asyncio.CancelledError:
                logging.warning("Analysis was cancelled")
                raise
            
            # Fetch the final state and report
            try:
                final_state_dict = await self.session_service.get_session_state(
                    app_name=settings.APP_NAME,
                    user_id=user_id,
                    session_id=session_id
                )
            except Exception as e:
                logging.error(f"Failed to retrieve final state: {e}")
                raise RuntimeError(f"Failed to retrieve analysis results: {e}") from e
            
            # Deserialize state
            try:
                final_state = ResearchSessionState(**final_state_dict)
            except Exception as e:
                logging.error(f"Failed to deserialize final state: {e}")
                raise RuntimeError(f"Failed to parse analysis results: {e}") from e
            
            # Validate report exists
            if not final_state.final_report:
                error_info = ""
                if final_state.errors:
                    error_info = f"\nErrors encountered: {', '.join(map(str, final_state.errors))}"
                raise RuntimeError(
                    f"Analysis completed but no report was generated. "
                    f"This may indicate an error in the report generation phase.{error_info}"
                )
            
            if verbose:
                logging.info(f"\n{'='*80}")
                logging.info("✅ Research complete!")
                logging.info(f"{'='*80}\n")
            
            # Return report as string
            report = final_state.final_report
            if hasattr(report, 'model_dump_json'):
                return report.model_dump_json(indent=2)
            elif hasattr(report, 'dict'):
                return json.dumps(report.dict(), indent=2)
            else:
                return str(report)
        
        except (ValueError, TimeoutError) as e:
            # Re-raise expected errors
            raise
        except Exception as e:
            logging.error(f"Unexpected error during stock analysis: {e}")
            raise RuntimeError(f"Stock analysis failed: {e}") from e


async def main(query: str):
    """
    Main async function to run the agent with error handling.
    
    Args:
        query: The user's query for stock analysis.
    """
    try:
        agent = PortfolioResearchAgent()
        report = await agent.analyze_stock(query=query, verbose=True)
        print("\n\n--- FINAL REPORT ---")
        print(report)
    except ValueError as e:
        logging.error(f"Invalid input: {e}")
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    except TimeoutError as e:
        logging.error(f"Analysis timed out: {e}")
        print(f"\n⏱️  {e}")
        print("Try analyzing a different stock or check your internet connection.")
        sys.exit(1)
    except RuntimeError as e:
        logging.error(f"Analysis failed: {e}")
        print(f"\n❌ Analysis failed: {e}")
        print("Please check the logs for more details.")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"\n❌ An unexpected error occurred: {e}")
        print("Please report this issue with the full error trace.")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    # Example usage: python -m portfolio_agent.main "Analyze the financial health of Apple Inc. (AAPL)"
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
        asyncio.run(main(user_query))
    else:
        print("Usage: python -m portfolio_agent.main \"<your query>\"")
        print("Example: python -m portfolio_agent.main \"Is Tesla overvalued?\"")
