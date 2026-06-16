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
        
        # Validate API keys or Vertex configuration
        api_validation = settings.validate_api_keys()
        if not api_validation["google_api_key"] and not api_validation["vertex_config"]:
            raise ValueError(
                "Authentication required. Please configure one of the following in your .env:\n"
                "  1) GOOGLE_API_KEY (for Gemini Developer API)\n"
                "  2) GOOGLE_GENAI_USE_VERTEXAI=True and GOOGLE_CLOUD_PROJECT=your_project_id (for GCP Vertex AI)"
            )
        
        if api_validation["vertex_config"]:
            print(f"✅ GCP Vertex AI configured (Project: {settings.GOOGLE_CLOUD_PROJECT}, Location: {settings.GOOGLE_CLOUD_LOCATION})")
        else:
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
        
        # Check if session exists first to avoid overwriting state in multi-turn conversations
        try:
            session = await self.session_service.get_session(
                app_name=settings.APP_NAME,
                user_id=user_id,
                session_id=session_id
            )
        except Exception:
            session = None
            
        if not session:
            # Create session only if it doesn't already exist
            await self.create_session(user_id, session_id, query)
        
        if verbose:
            print(f"\n{'='*80}")
            print(f"🔍 Research query: {query}")
            print(f"{'='*80}\n")
        
        # Prepare message
        content = types.Content(role='user', parts=[types.Part(text=query)])
        
        # Track final response
        final_response_text = "Research completed but no final response generated."
        
        try:
            # Run the agent
            if verbose:
                print("📡 Processing through Research Coordinator...\n")
            
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
                
                # Capture final response - ONLY from the root coordinator, not sub-agents
                if event.is_final_response() and event.author == 'research_coordinator':
                    if event.content and event.content.parts:
                        final_response_text = event.content.parts[0].text
                    elif event.actions and event.actions.escalate:
                        final_response_text = f"Error: {event.error_message or 'Agent escalated without specific message.'}"
                    break
            
            if verbose:
                print(f"\n{'='*80}")
                print("✅ Run Complete!")
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


async def interactive_loop():
    """Run an interactive chat session with the portfolio agent."""
    try:
        agent = PortfolioResearchAgent()
    except Exception as e:
        print(f"\n❌ Initialization error: {str(e)}")
        sys.exit(1)
        
    user_id = settings.DEFAULT_USER_ID
    session_id = f"chat_{asyncio.get_event_loop().time():.0f}"
    
    print("\n" + "="*80)
    print("💬 INTERACTIVE PORTFOLIO RESEARCH CHAT")
    print("Ask any questions or type a company name/ticker to start research.")
    print("Type 'exit' or 'quit' to end the session.")
    print("="*80 + "\n")
    
    loop = asyncio.get_event_loop()
    
    while True:
        try:
            # Get user query in a non-blocking executor
            query = await loop.run_in_executor(None, lambda: input("💬 You: "))
            
            query = query.strip()
            if not query:
                continue
                
            if query.lower() in ["exit", "quit"]:
                print("\n👋 Goodbye!")
                break
                
            # Run analysis (verbose mode prints progress updates)
            report = await agent.analyze_stock(
                query=query, 
                user_id=user_id, 
                session_id=session_id, 
                verbose=True
            )
            
            print("\n" + "="*80)
            print("📊 AGENT RESPONSE / REPORT")
            print("="*80 + "\n")
            print(report)
            print("\n" + "="*80 + "\n")
            
        except KeyboardInterrupt:
            print("\n👋 Session interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error during turn: {str(e)}\n")


async def async_main():
    """Main entry point for CLI usage (async)."""
    # Parse command line arguments
    # If no arguments or is interactive flag, enter interactive loop
    if len(sys.argv) < 2 or sys.argv[1].lower() in ["--interactive", "-i", "chat"]:
        await interactive_loop()
        sys.exit(0)
    
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


def main():
    """CLI entrypoint wrapper."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
