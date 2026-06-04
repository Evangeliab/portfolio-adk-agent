"""Tools for fetching market data from Yahoo Finance."""

import yfinance as yf
import pandas as pd
import logging
from typing import Optional
from portfolio_agent.models.stock_data import CompanyData, PriceHistory, FinancialStatements
from portfolio_agent.tools.retry_utils import yfinance_retry
from portfolio_agent.tools.yfinance_utils import create_yf_ticker
from portfolio_agent.tools.cache_utils import ttl_cache


@yfinance_retry
@ttl_cache(seconds=300, maxsize=128)
def get_stock_info(ticker: str) -> dict:
    """
    Retrieves basic company information for a given stock ticker.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL", "MSFT")
    
    Returns:
        dict: A dictionary containing company information with 'status' key.
              If successful, includes 'data' key with CompanyData.
              If error, includes 'error_message' key.
    """
    print(f"--- Tool: get_stock_info called for ticker: {ticker} ---")
    
    try:
        stock = create_yf_ticker(ticker)
        info = stock.info
        
        if not info or 'symbol' not in info:
            return {
                "status": "error",
                "error_message": f"Could not find information for ticker '{ticker}'. "
                                 "Please verify the ticker symbol is correct."
            }
        
        company_data = CompanyData(
            ticker=ticker.upper(),
            company_name=info.get('longName', info.get('shortName', ticker)),
            sector=info.get('sector'),
            industry=info.get('industry'),
            market_cap=info.get('marketCap'),
            description=info.get('longBusinessSummary'),
            website=info.get('website'),
            employees=info.get('fullTimeEmployees')
        )
        
        print(f"--- Tool: Successfully retrieved info for {company_data.company_name} ---")
        return {
            "status": "success",
            "data": company_data.model_dump()
        }
        
    except Exception as e:
        print(f"--- Tool: Error retrieving stock info: {str(e)} ---")
        return {
            "status": "error",
            "error_message": f"Error fetching stock info for '{ticker}': {str(e)}"
        }


@yfinance_retry
@ttl_cache(seconds=300, maxsize=128)
def get_price_history(ticker: str, period: str = "1y") -> dict:
    """
    Retrieves historical price data and current price information.
    
    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL")
        period (str): Time period - valid values: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
    
    Returns:
        dict: A dictionary with 'status' key. If successful, includes 'data' with PriceHistory
              and 'history' with historical price data as list of dicts.
    """
    print(f"--- Tool: get_price_history called for {ticker}, period: {period} ---")
    
    try:
        stock = create_yf_ticker(ticker)
        info = stock.info
        
        # Get current price information
        price_history = PriceHistory(
            ticker=ticker.upper(),
            period=period,
            current_price=info.get('currentPrice', info.get('regularMarketPrice')),
            previous_close=info.get('previousClose', info.get('regularMarketPreviousClose')),
            day_high=info.get('dayHigh', info.get('regularMarketDayHigh')),
            day_low=info.get('dayLow', info.get('regularMarketDayLow')),
            volume=info.get('volume', info.get('regularMarketVolume')),
            avg_volume=info.get('averageVolume'),
            fifty_two_week_high=info.get('fiftyTwoWeekHigh'),
            fifty_two_week_low=info.get('fiftyTwoWeekLow')
        )
        
        # Get historical data
        hist = stock.history(period=period)
        
        if hist.empty:
            return {
                "status": "error",
                "error_message": f"No historical data available for '{ticker}' for period '{period}'"
            }
        
        # Validate required columns exist
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in hist.columns]
        
        if missing_columns:
            return {
                "status": "error",
                "error_message": (
                    f"Historical data for '{ticker}' is missing required columns: "
                    f"{', '.join(missing_columns)}. Available columns: {', '.join(hist.columns)}"
                )
            }
        
        # Validate data quality - check for NaN values in critical columns
        if hist[['Close']].isna().all().any():
            return {
                "status": "error",
                "error_message": f"Historical data for '{ticker}' contains all NaN values in Close prices"
            }
        
        # Convert to list of dicts for easier consumption
        history_data = []
        for date, row in hist.iterrows():
            # Skip rows with NaN close price
            if pd.isna(row['Close']):
                continue
            
            try:
                price_point = {
                    "date": date.strftime("%Y-%m-%d"),
                    "open": float(row['Open']) if not pd.isna(row['Open']) else float(row['Close']),
                    "high": float(row['High']) if not pd.isna(row['High']) else float(row['Close']),
                    "low": float(row['Low']) if not pd.isna(row['Low']) else float(row['Close']),
                    "close": float(row['Close']),
                    "volume": int(row['Volume']) if not pd.isna(row['Volume']) else 0
                }
                
                # Validate OHLC relationship
                if price_point['high'] < price_point['low']:
                    logging.warning(f"Invalid OHLC data for {ticker} on {date}: High < Low")
                    continue
                
                # Validate positive prices
                if any(price_point[k] <= 0 for k in ['open', 'high', 'low', 'close']):
                    logging.warning(f"Invalid price data for {ticker} on {date}: Non-positive prices")
                    continue
                
                history_data.append(price_point)
                
            except (ValueError, TypeError) as e:
                logging.warning(f"Error processing price data for {ticker} on {date}: {e}")
                continue
        
        if not history_data:
            return {
                "status": "error",
                "error_message": f"No valid historical data points for '{ticker}' after validation"
            }
        
        print(f"--- Tool: Retrieved {len(history_data)} days of price history ---")
        return {
            "status": "success",
            "data": price_history.model_dump(),
            "history": history_data
        }
        
    except Exception as e:
        print(f"--- Tool: Error retrieving price history: {str(e)} ---")
        return {
            "status": "error",
            "error_message": f"Error fetching price history for '{ticker}': {str(e)}"
        }


@yfinance_retry
@ttl_cache(seconds=300, maxsize=128)
def get_financial_statements(ticker: str) -> dict:
    """
    Retrieves financial statement data (income statement, balance sheet, cash flow).
    
    Args:
        ticker (str): Stock ticker symbol (e.g., "AAPL")
    
    Returns:
        dict: A dictionary with 'status' key. If successful, includes 'data' with FinancialStatements.
    """
    print(f"--- Tool: get_financial_statements called for ticker: {ticker} ---")
    
    try:
        stock = create_yf_ticker(ticker)
        info = stock.info
        
        financials = FinancialStatements(
            ticker=ticker.upper(),
            # Income Statement
            revenue=info.get('totalRevenue'),
            revenue_growth=info.get('revenueGrowth'),
            gross_profit=info.get('grossProfits'),
            operating_income=info.get('operatingIncome', info.get('ebit')),
            net_income=info.get('netIncomeToCommon'),
            earnings_per_share=info.get('trailingEps'),
            # Balance Sheet
            total_assets=info.get('totalAssets'),
            total_liabilities=info.get('totalDebt'),
            shareholders_equity=info.get('totalStockholderEquity'),
            total_debt=info.get('totalDebt'),
            cash_and_equivalents=info.get('totalCash'),
            # Cash Flow
            operating_cash_flow=info.get('operatingCashflow'),
            free_cash_flow=info.get('freeCashflow'),
            capital_expenditures=info.get('capitalExpenditures')
        )
        
        print(f"--- Tool: Successfully retrieved financial statements for {ticker} ---")
        return {
            "status": "success",
            "data": financials.model_dump()
        }
        
    except Exception as e:
        print(f"--- Tool: Error retrieving financial statements: {str(e)} ---")
        return {
            "status": "error",
            "error_message": f"Error fetching financial statements for '{ticker}': {str(e)}"
        }
