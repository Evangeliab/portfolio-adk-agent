"""Main entry point for the Portfolio Research Agent."""

import asyncio
import sys
from typing import Optional
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from portfolio_agent.config.settings import settings
from portfolio_agent.agents.coordinator import create_research_coordinator
from portfolio_agent.models.state import ResearchSessionState


class PortfolioResearchAgent:
    """Main application class for portfolio research."""
    
    def __init__(self):
        """Initialize the research agent."""
        # Setup environment
        settings.setup_environment()
        
        # Validate API keys
        api_validation = settings.validate_api_keys()
        if not api_validation["google_api_key"]:
            raise ValueError(
                "GOOGLE_API_KEY is required. Please set it in your .env file. "
                "Get your API key from: https://aistudio.google.com/app/apikey"
            )
        
        print("✅ API keys validated")
        print(f"📊 Using model: {settings.COORDINATOR_MODEL}")
        print(f"🔍 Google Search grounding: {'Enabled' if settings.ENABLE_GOOGLE_SEARCH_GROUNDING else 'Disabled'}")
        
        # Create session service
        self.session_service = InMemorySessionService()
        
        # Create coordinator agent
        self.coordinator = create_research_coordinator()
        
        # Create runner
        self.runner = Runner(
            agent=self.coordinator,
            app_name=settings.APP_NAME,
            session_service=self.session_service
        )
        
        print(f"✅ Research Coordinator initialized with {len(self.coordinator.sub_agents)} specialist agents")
        
    async def create_session(self, user_id: str, session_id: str, query: str) -> None:
        """
        Create a new research session.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
            query: User's research query
        """
        # Initialize session with empty state
        initial_state = ResearchSessionState(query=query).model_dump()
        
        await self.session_service.create_session(
            app_name=settings.APP_NAME,
            user_id=user_id,
            session_id=session_id,
            state=initial_state
        )
        
        print(f"✅ Session created: user_id={user_id}, session_id={session_id}")
    
    async def analyze_stock(
        self, 
        query: str, 
        user_id: str = None,
        session_id: str = None,
        verbose: bool = True
    ) -> str:
        """
        Analyze a stock based on user query.
        
        Args:
            query: Natural language query or ticker symbol
            user_id: User identifier (optional, uses default if not provided)
            session_id: Session identifier (optional, generates new if not provided)
            verbose: Whether to print progress updates
        
        Returns:
            str: Final analysis report
        """
        # Use defaults if not provided
        user_id = user_id or settings.DEFAULT_USER_ID
        session_id = session_id or f"session_{asyncio.get_event_loop().time():.0f}"
        
        # Create session
        await self.create_session(user_id, session_id, query)
        
        if verbose:
            print(f"\n{'='*80}")
            print(f"🔍 Starting stock research for: {query}")
            print(f"{'='*80}\n")
        
        # Prepare message
        content = types.Content(role='user', parts=[types.Part(text=query)])
        
        # Track final response
        final_response_text = "Research completed but no final response generated."
        
        try:
            # Run the agent
            if verbose:
                print("📡 Delegating to Research Coordinator...\n")
            
            async for event in self.runner.run_async(
                user_id=user_id,
                session_id=session_id,
                new_message=content
            ):
                # Print progress events
                if verbose and hasattr(event, 'author'):
                    if event.author and event.author != 'user':
                        if hasattr(event, 'content') and event.content:
                            if hasattr(event.content, 'parts') and event.content.parts:
                                text = event.content.parts[0].text if event.content.parts[0].text else ""
                                if text and len(text) > 0:
                                    # Print agent activity
                                    print(f"🤖 [{event.author}]: {text[:150]}...")
                
                # Capture final response
                if event.is_final_response():
                    if event.content and event.content.parts:
                        final_response_text = event.content.parts[0].text
                    elif event.actions and event.actions.escalate:
                        final_response_text = f"Error: {event.error_message or 'Agent escalated without specific message.'}"
                    break
            
            if verbose:
                print(f"\n{'='*80}")
                print("✅ Research Complete!")
                print(f"{'='*80}\n")
            
            return final_response_text
            
        except Exception as e:
            error_msg = f"❌ Error during research: {str(e)}"
            print(error_msg)
            return error_msg
    
    async def get_session_state(self, user_id: str, session_id: str) -> Optional[dict]:
        """
        Retrieve session state for inspection.
        
        Args:
            user_id: User identifier
            session_id: Session identifier
        
        Returns:
            dict: Session state or None if not found
        """
        session = await self.session_service.get_session(
            app_name=settings.APP_NAME,
            user_id=user_id,
            session_id=session_id
        )
        
        if session:
            return session.state
        return None


async def main():
    """Main entry point for CLI usage."""
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python -m portfolio_agent.main <query>")
        print("\nExamples:")
        print('  python -m portfolio_agent.main "analyze Apple stock"')
        print('  python -m portfolio_agent.main "research MSFT"')
        print('  python -m portfolio_agent.main "what do you think about Tesla?"')
        sys.exit(1)
    
    # Get query from arguments
    query = " ".join(sys.argv[1:])
    
    try:
        # Create agent
        agent = PortfolioResearchAgent()
        
        # Run analysis
        report = await agent.analyze_stock(query, verbose=True)
        
        # Print final report
        print("\n" + "="*80)
        print("📊 INVESTMENT RESEARCH REPORT")
        print("="*80 + "\n")
        print(report)
        print("\n" + "="*80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Research interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
