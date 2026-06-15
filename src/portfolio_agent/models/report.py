"""Pydantic models for investment reports and recommendations."""

from typing import Optional, List
from pydantic import BaseModel, Field


class ResearchRecommendation(BaseModel):
    """Investment recommendation."""
    
    recommendation: str = Field(
        ...,
        description="Investment recommendation (Strong Buy, Buy, Hold, Sell, Strong Sell)"
    )
    confidence_level: str = Field(
        ...,
        description="Confidence level (High, Medium, Low)"
    )
    target_price: Optional[float] = Field(
        None,
        description="Target price estimate"
    )
    risk_level: str = Field(
        ...,
        description="Risk assessment (Low, Medium, High)"
    )
    time_horizon: str = Field(
        default="Medium-term (6-12 months)",
        description="Investment time horizon"
    )
    key_reasons: List[str] = Field(
        ...,
        description="Key reasons supporting the recommendation"
    )


class InvestmentReport(BaseModel):
    """Comprehensive investment research report."""
    
    # Header Information
    ticker: str = Field(..., description="Stock ticker symbol")
    company_name: str = Field(..., description="Company name")
    report_date: str = Field(..., description="Report generation date")
    current_price: Optional[float] = Field(None, description="Current stock price")
    
    # Executive Summary
    executive_summary: str = Field(
        ...,
        description="High-level summary of investment thesis"
    )
    
    # Analysis Sections
    fundamental_summary: Optional[str] = Field(
        None,
        description="Summary of fundamental analysis findings"
    )
    technical_summary: Optional[str] = Field(
        None,
        description="Summary of technical analysis findings"
    )
    news_sentiment_summary: Optional[str] = Field(
        None,
        description="Summary of news and sentiment analysis"
    )
    
    # Investment Thesis
    bull_case: List[str] = Field(
        default_factory=list,
        description="Bullish arguments for the stock"
    )
    bear_case: List[str] = Field(
        default_factory=list,
        description="Bearish arguments or risks"
    )
    
    # Key Metrics Snapshot
    key_metrics: dict = Field(
        default_factory=dict,
        description="Important metrics at a glance"
    )
    
    # Recommendation
    recommendation: ResearchRecommendation = Field(
        ...,
        description="Final investment recommendation"
    )
    
    # Additional Considerations
    catalysts: List[str] = Field(
        default_factory=list,
        description="Potential catalysts that could move the stock"
    )
    risks: List[str] = Field(
        default_factory=list,
        description="Key risks to monitor"
    )
    
    # Disclaimer
    disclaimer: str = Field(
        default="This report is for informational purposes only and should not be considered "
                "investment advice. Always conduct your own research and consult with a financial "
                "advisor before making investment decisions.",
        description="Legal disclaimer"
    )
