"""Pydantic models for stock data and company information."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class StockQuery(BaseModel):
    """User query for stock research."""
    
    query: str = Field(..., description="Natural language query or ticker symbol")
    depth: str = Field(
        default="comprehensive",
        description="Analysis depth: quick, standard, or comprehensive"
    )


class CompanyData(BaseModel):
    """Basic company information."""
    
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL)")
    company_name: str = Field(..., description="Full company name")
    sector: Optional[str] = Field(None, description="Industry sector")
    industry: Optional[str] = Field(None, description="Specific industry")
    market_cap: Optional[float] = Field(None, description="Market capitalization in USD")
    description: Optional[str] = Field(None, description="Company description")
    website: Optional[str] = Field(None, description="Company website URL")
    employees: Optional[int] = Field(None, description="Number of employees")
    

class PriceHistory(BaseModel):
    """Historical price data."""
    
    ticker: str = Field(..., description="Stock ticker symbol")
    period: str = Field(..., description="Time period (e.g., '1mo', '3mo', '1y')")
    current_price: Optional[float] = Field(None, description="Current stock price")
    previous_close: Optional[float] = Field(None, description="Previous closing price")
    day_high: Optional[float] = Field(None, description="Today's high price")
    day_low: Optional[float] = Field(None, description="Today's low price")
    volume: Optional[int] = Field(None, description="Trading volume")
    avg_volume: Optional[int] = Field(None, description="Average volume")
    fifty_two_week_high: Optional[float] = Field(None, description="52-week high")
    fifty_two_week_low: Optional[float] = Field(None, description="52-week low")
    

class FinancialStatements(BaseModel):
    """Company financial statements summary."""
    
    ticker: str = Field(..., description="Stock ticker symbol")
    
    # Income Statement
    revenue: Optional[float] = Field(None, description="Total revenue (latest period)")
    revenue_growth: Optional[float] = Field(None, description="Revenue growth rate (%)")
    gross_profit: Optional[float] = Field(None, description="Gross profit")
    operating_income: Optional[float] = Field(None, description="Operating income")
    net_income: Optional[float] = Field(None, description="Net income")
    earnings_per_share: Optional[float] = Field(None, description="EPS")
    
    # Balance Sheet
    total_assets: Optional[float] = Field(None, description="Total assets")
    total_liabilities: Optional[float] = Field(None, description="Total liabilities")
    shareholders_equity: Optional[float] = Field(None, description="Shareholders equity")
    total_debt: Optional[float] = Field(None, description="Total debt")
    cash_and_equivalents: Optional[float] = Field(None, description="Cash and cash equivalents")
    
    # Cash Flow
    operating_cash_flow: Optional[float] = Field(None, description="Operating cash flow")
    free_cash_flow: Optional[float] = Field(None, description="Free cash flow")
    capital_expenditures: Optional[float] = Field(None, description="Capital expenditures")
