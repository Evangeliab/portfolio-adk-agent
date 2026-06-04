"""Tools for calculating financial metrics and ratios."""

import yfinance as yf
from typing import Optional
from portfolio_agent.models.analysis import FinancialMetrics
from portfolio_agent.tools.retry_utils import yfinance_retry
from portfolio_agent.tools.yfinance_utils import create_yf_ticker
from portfolio_agent.tools.cache_utils import ttl_cache


@yfinance_retry
@ttl_cache(seconds=300, maxsize=128)
def calculate_valuation_ratios(ticker: str) -> dict:
    """
    Calculates valuation ratios (P/E, P/B, P/S, PEG, EV ratios).
    
    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL")
    
    Returns:
        dict: Dictionary with 'status' and valuation metrics
    """
    print(f"--- Tool: calculate_valuation_ratios called for ticker: {ticker} ---")
    
    try:
        stock = create_yf_ticker(ticker)
        info = stock.info
        
        metrics = {
            "ticker": ticker.upper(),
            "pe_ratio": info.get('trailingPE'),
            "forward_pe": info.get('forwardPE'),
            "peg_ratio": info.get('pegRatio'),
            "price_to_book": info.get('priceToBook'),
            "price_to_sales": info.get('priceToSalesTrailing12Months'),
            "enterprise_value": info.get('enterpriseValue'),
            "ev_to_revenue": info.get('enterpriseToRevenue'),
            "ev_to_ebitda": info.get('enterpriseToEbitda'),
        }
        
        print(f"--- Tool: Calculated valuation ratios for {ticker} ---")
        return {
            "status": "success",
            "data": metrics
        }
        
    except Exception as e:
        print(f"--- Tool: Error calculating valuation ratios: {str(e)} ---")
        return {
            "status": "error",
            "error_message": f"Error calculating valuation ratios for '{ticker}': {str(e)}"
        }


@yfinance_retry
@ttl_cache(seconds=300, maxsize=128)
def calculate_profitability_metrics(ticker: str) -> dict:
    """
    Calculates profitability metrics (margins, ROA, ROE).
    
    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL")
    
    Returns:
        dict: Dictionary with 'status' and profitability metrics
    """
    print(f"--- Tool: calculate_profitability_metrics called for ticker: {ticker} ---")
    
    try:
        stock = create_yf_ticker(ticker)
        info = stock.info
        
        metrics = {
            "ticker": ticker.upper(),
            "profit_margin": info.get('profitMargins'),
            "operating_margin": info.get('operatingMargins'),
            "gross_margin": info.get('grossMargins'),
            "return_on_assets": info.get('returnOnAssets'),
            "return_on_equity": info.get('returnOnEquity'),
        }
        
        # Convert to percentages if they're in decimal form
        for key in ['profit_margin', 'operating_margin', 'gross_margin', 
                    'return_on_assets', 'return_on_equity']:
            if metrics.get(key) is not None and metrics[key] < 1:
                metrics[key] = metrics[key] * 100
        
        print(f"--- Tool: Calculated profitability metrics for {ticker} ---")
        return {
            "status": "success",
            "data": metrics
        }
        
    except Exception as e:
        print(f"--- Tool: Error calculating profitability metrics: {str(e)} ---")
        return {
            "status": "error",
            "error_message": f"Error calculating profitability metrics for '{ticker}': {str(e)}"
        }


@yfinance_retry
@ttl_cache(seconds=300, maxsize=128)
def calculate_growth_metrics(ticker: str) -> dict:
    """
    Calculates growth metrics (revenue growth, earnings growth).
    
    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL")
    
    Returns:
        dict: Dictionary with 'status' and growth metrics
    """
    print(f"--- Tool: calculate_growth_metrics called for ticker: {ticker} ---")
    
    try:
        stock = create_yf_ticker(ticker)
        info = stock.info
        
        metrics = {
            "ticker": ticker.upper(),
            "revenue_growth": info.get('revenueGrowth'),
            "earnings_growth": info.get('earningsGrowth'),
            "dividend_yield": info.get('dividendYield'),
            "payout_ratio": info.get('payoutRatio'),
        }
        
        # Convert to percentages if needed
        if metrics.get('revenue_growth') is not None and metrics['revenue_growth'] < 1:
            metrics['revenue_growth'] = metrics['revenue_growth'] * 100
        if metrics.get('earnings_growth') is not None and metrics['earnings_growth'] < 1:
            metrics['earnings_growth'] = metrics['earnings_growth'] * 100
        if metrics.get('dividend_yield') is not None and metrics['dividend_yield'] < 1:
            metrics['dividend_yield'] = metrics['dividend_yield'] * 100
        if metrics.get('payout_ratio') is not None and metrics['payout_ratio'] < 1:
            metrics['payout_ratio'] = metrics['payout_ratio'] * 100
        
        print(f"--- Tool: Calculated growth metrics for {ticker} ---")
        return {
            "status": "success",
            "data": metrics
        }
        
    except Exception as e:
        print(f"--- Tool: Error calculating growth metrics: {str(e)} ---")
        return {
            "status": "error",
            "error_message": f"Error calculating growth metrics for '{ticker}': {str(e)}"
        }


def get_comprehensive_financial_metrics(ticker: str) -> dict:
    """
    Gets comprehensive financial metrics by combining all calculations.
    This is a convenience function that calls all other metric functions.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL")
    
    Returns:
        dict: Dictionary with comprehensive FinancialMetrics
    """
    print(f"--- Tool: get_comprehensive_financial_metrics called for ticker: {ticker} ---")
    
    try:
        # Get all metrics
        valuation = calculate_valuation_ratios(ticker)
        profitability = calculate_profitability_metrics(ticker)
        growth = calculate_growth_metrics(ticker)
        
        # Check for errors
        if valuation.get("status") == "error":
            return valuation
        if profitability.get("status") == "error":
            return profitability
        if growth.get("status") == "error":
            return growth
        
        # Combine all metrics
        combined_metrics = {
            **valuation.get("data", {}),
            **profitability.get("data", {}),
            **growth.get("data", {}),
        }
        
        # Create FinancialMetrics model
        financial_metrics = FinancialMetrics(**combined_metrics)
        
        print(f"--- Tool: Compiled comprehensive financial metrics for {ticker} ---")
        return {
            "status": "success",
            "data": financial_metrics.model_dump()
        }
        
    except Exception as e:
        print(f"--- Tool: Error getting comprehensive metrics: {str(e)} ---")
        return {
            "status": "error",
            "error_message": f"Error calculating comprehensive metrics for '{ticker}': {str(e)}"
        }
