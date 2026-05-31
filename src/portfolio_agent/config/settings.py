"""Configuration and settings for the portfolio agent."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings."""
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # ADK Configuration
    GOOGLE_GENAI_USE_VERTEXAI: str = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "False")
    
    # Model Configuration
    # Use Gemini Flash for specialist agents (cost-effective)
    SPECIALIST_MODEL: str = "gemini-2.0-flash-exp"
    
    # Use more capable model for coordinator (better reasoning)
    COORDINATOR_MODEL: str = "gemini-2.0-flash-exp"  # Can upgrade to "gemini-exp-1206" if needed
    
    # Session Configuration
    APP_NAME: str = "portfolio_research_agent"
    DEFAULT_SESSION_ID: str = "research_session_001"
    DEFAULT_USER_ID: str = "user_001"
    
    # Yahoo Finance Configuration
    DEFAULT_PRICE_HISTORY_PERIOD: str = "1y"  # 1 year of historical data
    TECHNICAL_ANALYSIS_PERIOD: str = "6mo"    # 6 months for technical indicators
    
    # Google Search Configuration
    ENABLE_GOOGLE_SEARCH_GROUNDING: bool = True
    NEWS_SEARCH_DAYS: int = 30  # Look back 30 days for news
    
    @classmethod
    def validate_api_keys(cls) -> dict:
        """Validate that required API keys are set."""
        validation = {
            "google_api_key": bool(cls.GOOGLE_API_KEY),
            "openai_api_key": bool(cls.OPENAI_API_KEY),
            "anthropic_api_key": bool(cls.ANTHROPIC_API_KEY),
        }
        return validation
    
    @classmethod
    def setup_environment(cls):
        """Set up environment variables for ADK."""
        os.environ["GOOGLE_API_KEY"] = cls.GOOGLE_API_KEY
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = cls.GOOGLE_GENAI_USE_VERTEXAI
        
        if cls.OPENAI_API_KEY:
            os.environ["OPENAI_API_KEY"] = cls.OPENAI_API_KEY
        
        if cls.ANTHROPIC_API_KEY:
            os.environ["ANTHROPIC_API_KEY"] = cls.ANTHROPIC_API_KEY


# Create settings instance
settings = Settings()
