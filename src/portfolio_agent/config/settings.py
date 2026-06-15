"""Configuration and settings for the portfolio agent."""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def _get_bool_env(name: str, default: bool) -> bool:
    """Helper to parse boolean values from environment variables."""
    val = os.getenv(name)
    if val is None:
        return default
    return val.lower() in ("true", "1", "yes", "on")


class Settings:
    """Application settings."""
    
    # API Keys
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    
    # ADK Configuration
    GOOGLE_GENAI_USE_VERTEXAI: bool = _get_bool_env("GOOGLE_GENAI_USE_VERTEXAI", False)
    GOOGLE_CLOUD_PROJECT: str = os.getenv("GOOGLE_CLOUD_PROJECT", "")
    GOOGLE_CLOUD_LOCATION: str = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    
    # Model Configuration
    # Defaults to gemini-2.0-flash but allows environment overrides
    SPECIALIST_MODEL: str = os.getenv("SPECIALIST_MODEL", "gemini-2.0-flash")
    COORDINATOR_MODEL: str = os.getenv("COORDINATOR_MODEL", "gemini-2.0-flash")
    
    # Session Configuration
    APP_NAME: str = "portfolio_research_agent"
    DEFAULT_SESSION_ID: str = "research_session_001"
    DEFAULT_USER_ID: str = "user_001"
    
    # Yahoo Finance Configuration
    DEFAULT_PRICE_HISTORY_PERIOD: str = "1y"  # 1 year of historical data
    TECHNICAL_ANALYSIS_PERIOD: str = "6mo"    # 6 months for technical indicators
    
    # Google Search Configuration
    ENABLE_GOOGLE_SEARCH_GROUNDING: bool = _get_bool_env("ENABLE_GOOGLE_SEARCH_GROUNDING", True)
    NEWS_SEARCH_DAYS: int = int(os.getenv("NEWS_SEARCH_DAYS", "30"))  # Look back 30 days for news
    
    @classmethod
    def validate_api_keys(cls) -> dict:
        """Validate that required API keys or GCP Vertex AI config are set."""
        has_vertex_config = cls.GOOGLE_GENAI_USE_VERTEXAI and bool(cls.GOOGLE_CLOUD_PROJECT)
        validation = {
            "google_api_key": bool(cls.GOOGLE_API_KEY),
            "vertex_config": has_vertex_config,
            "openai_api_key": bool(cls.OPENAI_API_KEY),
            "anthropic_api_key": bool(cls.ANTHROPIC_API_KEY),
        }
        return validation
    
    @classmethod
    def setup_environment(cls):
        """Set up environment variables for ADK."""
        if cls.GOOGLE_API_KEY:
            os.environ["GOOGLE_API_KEY"] = cls.GOOGLE_API_KEY
            
        os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = str(cls.GOOGLE_GENAI_USE_VERTEXAI)
        
        if cls.GOOGLE_CLOUD_PROJECT:
            os.environ["GOOGLE_CLOUD_PROJECT"] = cls.GOOGLE_CLOUD_PROJECT
            
        if cls.GOOGLE_CLOUD_LOCATION:
            os.environ["GOOGLE_CLOUD_LOCATION"] = cls.GOOGLE_CLOUD_LOCATION
        
        if cls.OPENAI_API_KEY:
            os.environ["OPENAI_API_KEY"] = cls.OPENAI_API_KEY
        
        if cls.ANTHROPIC_API_KEY:
            os.environ["ANTHROPIC_API_KEY"] = cls.ANTHROPIC_API_KEY


# Create settings instance
settings = Settings()
