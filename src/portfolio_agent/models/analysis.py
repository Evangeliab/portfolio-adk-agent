"""Pydantic models for analysis results."""

from typing import Optional, List
from pydantic import BaseModel, Field


class FinancialMetrics(BaseModel):
    """Financial analysis metrics."""
    
    ticker: str = Field(..., description="Stock ticker symbol")
    
    # Valuation Ratios
    pe_ratio: Optional[float] = Field(None, description="Price-to-Earnings ratio")
    forward_pe: Optional[float] = Field(None, description="Forward P/E ratio")
    peg_ratio: Optional[float] = Field(None, description="Price/Earnings to Growth ratio")
    price_to_book: Optional[float] = Field(None, description="Price-to-Book ratio")
    price_to_sales: Optional[float] = Field(None, description="Price-to-Sales ratio")
    enterprise_value: Optional[float] = Field(None, description="Enterprise value")
    ev_to_revenue: Optional[float] = Field(None, description="EV/Revenue ratio")
    ev_to_ebitda: Optional[float] = Field(None, description="EV/EBITDA ratio")
    
    # Profitability Metrics
    profit_margin: Optional[float] = Field(None, description="Net profit margin (%)")
    operating_margin: Optional[float] = Field(None, description="Operating margin (%)")
    gross_margin: Optional[float] = Field(None, description="Gross margin (%)")
    return_on_assets: Optional[float] = Field(None, description="ROA (%)")
    return_on_equity: Optional[float] = Field(None, description="ROE (%)")
    
    # Growth Metrics
    revenue_growth: Optional[float] = Field(None, description="Revenue growth rate (%)")
    earnings_growth: Optional[float] = Field(None, description="Earnings growth rate (%)")
    
    # Dividend Metrics
    dividend_yield: Optional[float] = Field(None, description="Dividend yield (%)")
    payout_ratio: Optional[float] = Field(None, description="Dividend payout ratio (%)")
    
    # Analysis
    valuation_assessment: Optional[str] = Field(
        None, 
        description="Valuation assessment (undervalued, fairly valued, overvalued)"
    )
    strengths: List[str] = Field(default_factory=list, description="Key strengths")
    concerns: List[str] = Field(default_factory=list, description="Key concerns")


class TechnicalIndicators(BaseModel):
    """Technical analysis indicators."""
    
    ticker: str = Field(..., description="Stock ticker symbol")
    
    # Moving Averages
    sma_20: Optional[float] = Field(None, description="20-day Simple Moving Average")
    sma_50: Optional[float] = Field(None, description="50-day Simple Moving Average")
    sma_200: Optional[float] = Field(None, description="200-day Simple Moving Average")
    ema_12: Optional[float] = Field(None, description="12-day Exponential Moving Average")
    ema_26: Optional[float] = Field(None, description="26-day Exponential Moving Average")
    
    # Momentum Indicators
    rsi: Optional[float] = Field(None, description="Relative Strength Index (0-100)")
    macd: Optional[float] = Field(None, description="MACD value")
    macd_signal: Optional[float] = Field(None, description="MACD signal line")
    macd_histogram: Optional[float] = Field(None, description="MACD histogram")
    
    # Price Levels
    support_level: Optional[float] = Field(None, description="Support price level")
    resistance_level: Optional[float] = Field(None, description="Resistance price level")
    
    # Trend Analysis
    trend: Optional[str] = Field(
        None,
        description="Overall trend (bullish, bearish, neutral)"
    )
    trend_strength: Optional[str] = Field(
        None,
        description="Trend strength (strong, moderate, weak)"
    )
    
    # Signals
    buy_signals: List[str] = Field(default_factory=list, description="Bullish signals")
    sell_signals: List[str] = Field(default_factory=list, description="Bearish signals")
    
    # Analysis
    technical_summary: Optional[str] = Field(
        None,
        description="Overall technical analysis summary"
    )


class NewsArticle(BaseModel):
    """Individual news article."""
    
    title: str = Field(..., description="Article title")
    source: Optional[str] = Field(None, description="News source")
    published_date: Optional[str] = Field(None, description="Publication date")
    summary: Optional[str] = Field(None, description="Article summary")
    url: Optional[str] = Field(None, description="Article URL")
    sentiment: Optional[str] = Field(
        None,
        description="Article sentiment (positive, negative, neutral)"
    )


class NewsSentiment(BaseModel):
    """News sentiment analysis results."""
    
    ticker: str = Field(..., description="Stock ticker symbol")
    company_name: str = Field(..., description="Company name")
    
    # Overall Sentiment
    overall_sentiment: str = Field(
        ...,
        description="Overall sentiment (positive, negative, neutral, mixed)"
    )
    sentiment_score: Optional[float] = Field(
        None,
        description="Sentiment score (-1.0 to 1.0, negative to positive)"
    )
    
    # Key Themes
    key_themes: List[str] = Field(
        default_factory=list,
        description="Main themes from news analysis"
    )
    positive_developments: List[str] = Field(
        default_factory=list,
        description="Positive news developments"
    )
    negative_developments: List[str] = Field(
        default_factory=list,
        description="Negative news developments or concerns"
    )
    
    # Articles (optional detailed list)
    recent_articles: List[NewsArticle] = Field(
        default_factory=list,
        description="Recent news articles analyzed"
    )
    
    # Analysis
    news_summary: str = Field(
        ...,
        description="Summary of news sentiment analysis"
    )
