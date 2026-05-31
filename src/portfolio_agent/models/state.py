"""Pydantic models for session state management."""

from typing import Optional, Dict
from pydantic import BaseModel, Field
from portfolio_agent.models.analysis import FinancialMetrics, TechnicalIndicators, NewsSentiment
from portfolio_agent.models.reports import InvestmentReport


class ResearchSessionState(BaseModel):
    """Session state tracking research workflow progress."""
    
    # Original Query
    query: str = Field(..., description="Original user query")
    
    # Ticker Resolution
    resolved_ticker: Optional[str] = Field(
        None,
        description="Resolved ticker symbol (e.g., AAPL)"
    )
    company_name: Optional[str] = Field(
        None,
        description="Full company name"
    )
    ticker_resolution_confidence: Optional[float] = Field(
        None,
        description="Confidence score for ticker resolution (0-1)"
    )
    
    # Progress Tracking
    progress: Dict[str, bool] = Field(
        default_factory=lambda: {
            "ticker_resolved": False,
            "fundamental_analysis": False,
            "technical_analysis": False,
            "news_sentiment": False,
            "report_generated": False,
        },
        description="Progress tracker for each research phase"
    )
    
    # Analysis Results
    fundamental_analysis: Optional[FinancialMetrics] = Field(
        None,
        description="Fundamental analysis results"
    )
    technical_analysis: Optional[TechnicalIndicators] = Field(
        None,
        description="Technical analysis results"
    )
    news_sentiment: Optional[NewsSentiment] = Field(
        None,
        description="News sentiment analysis results"
    )
    
    # Final Output
    final_report: Optional[InvestmentReport] = Field(
        None,
        description="Complete investment research report"
    )
    
    # Metadata
    errors: list = Field(
        default_factory=list,
        description="Any errors encountered during research"
    )
    warnings: list = Field(
        default_factory=list,
        description="Warnings or limitations to note"
    )
    
    class Config:
        """Pydantic configuration."""
        arbitrary_types_allowed = True
