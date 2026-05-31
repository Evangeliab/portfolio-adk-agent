"""Tools for resolving company names to stock ticker symbols."""

import yfinance as yf
from typing import Optional, List, Dict


# Common company name to ticker mappings for quick resolution
COMMON_TICKERS = {
    "apple": "AAPL",
    "microsoft": "MSFT",
    "google": "GOOGL",
    "alphabet": "GOOGL",
    "amazon": "AMZN",
    "tesla": "TSLA",
    "meta": "META",
    "facebook": "META",
    "nvidia": "NVDA",
    "netflix": "NFLX",
    "disney": "DIS",
    "walmart": "WMT",
    "jpmorgan": "JPM",
    "jp morgan": "JPM",
    "visa": "V",
    "mastercard": "MA",
    "boeing": "BA",
    "coca cola": "KO",
    "coca-cola": "KO",
    "pepsi": "PEP",
    "intel": "INTC",
    "amd": "AMD",
    "qualcomm": "QCOM",
    "ibm": "IBM",
    "oracle": "ORCL",
    "salesforce": "CRM",
    "adobe": "ADBE",
    "paypal": "PYPL",
    "uber": "UBER",
    "lyft": "LYFT",
    "airbnb": "ABNB",
    "spotify": "SPOT",
    "twitter": "TWTR",
    "x": "X",
    "snap": "SNAP",
    "snapchat": "SNAP",
}


def resolve_ticker(query: str) -> dict:
    """
    Converts natural language stock queries to ticker symbols.
    Handles queries like "Apple stock", "Microsoft", "analyze Tesla", etc.
    
    Args:
        query (str): Natural language query containing company name or ticker
    
    Returns:
        dict: Dictionary with 'status', and if successful:
              - 'ticker': Resolved ticker symbol
              - 'company_name': Full company name
              - 'confidence': Confidence score (0-1)
              - 'alternatives': List of alternative matches if ambiguous
    """
    print(f"--- Tool: resolve_ticker called with query: '{query}' ---")
    
    try:
        # Clean up the query
        query_lower = query.lower().strip()
        
        # Remove common words
        for word in ["stock", "analyze", "research", "company", "corporation", 
                     "inc", "the", "what", "about", "think", "of"]:
            query_lower = query_lower.replace(word, "").strip()
        
        # Check if it's already a valid ticker (all caps, 1-5 chars)
        potential_ticker = query_lower.upper()
        if len(potential_ticker) <= 5 and potential_ticker.isalpha():
            # Try to validate it's a real ticker
            try:
                stock = yf.Ticker(potential_ticker)
                info = stock.info
                if info and 'symbol' in info:
                    company_name = info.get('longName', info.get('shortName', potential_ticker))
                    print(f"--- Tool: Recognized as direct ticker: {potential_ticker} ({company_name}) ---")
                    return {
                        "status": "success",
                        "ticker": potential_ticker,
                        "company_name": company_name,
                        "confidence": 1.0,
                        "alternatives": []
                    }
            except:
                pass  # Not a valid ticker, continue with name search
        
        # Check common mappings first
        for name, ticker in COMMON_TICKERS.items():
            if name in query_lower or query_lower in name:
                stock = yf.Ticker(ticker)
                info = stock.info
                company_name = info.get('longName', info.get('shortName', ticker))
                print(f"--- Tool: Found in common mappings: {ticker} ({company_name}) ---")
                return {
                    "status": "success",
                    "ticker": ticker,
                    "company_name": company_name,
                    "confidence": 0.95,
                    "alternatives": []
                }
        
        # Use yfinance search for more complex queries
        # Note: yfinance doesn't have a built-in search, so we'll try a heuristic approach
        # We'll attempt to extract potential company names and validate
        
        # Try the cleaned query as a company name directly
        potential_matches = []
        
        # Split into words and try each as potential ticker or company name
        words = query_lower.split()
        for word in words:
            if len(word) > 2:  # Skip very short words
                ticker_candidate = word.upper()
                try:
                    stock = yf.Ticker(ticker_candidate)
                    info = stock.info
                    if info and 'symbol' in info:
                        potential_matches.append({
                            "ticker": ticker_candidate,
                            "company_name": info.get('longName', info.get('shortName', ticker_candidate)),
                            "confidence": 0.7
                        })
                except:
                    continue
        
        if potential_matches:
            # Return the first match
            best_match = potential_matches[0]
            alternatives = potential_matches[1:] if len(potential_matches) > 1 else []
            
            print(f"--- Tool: Found potential match: {best_match['ticker']} ---")
            return {
                "status": "success",
                "ticker": best_match["ticker"],
                "company_name": best_match["company_name"],
                "confidence": best_match["confidence"],
                "alternatives": alternatives
            }
        
        # If all else fails, return error
        print(f"--- Tool: Could not resolve ticker from query: '{query}' ---")
        return {
            "status": "error",
            "error_message": f"Could not resolve '{query}' to a stock ticker. "
                           f"Please provide a valid ticker symbol (e.g., AAPL, MSFT) "
                           f"or a well-known company name (e.g., Apple, Microsoft)."
        }
        
    except Exception as e:
        print(f"--- Tool: Error resolving ticker: {str(e)} ---")
        return {
            "status": "error",
            "error_message": f"Error resolving ticker from query '{query}': {str(e)}"
        }


def validate_ticker(ticker: str) -> dict:
    """
    Validates that a ticker symbol exists and is tradable.
    
    Args:
        ticker (str): Ticker symbol to validate
    
    Returns:
        dict: Dictionary with 'status' and validation result
    """
    print(f"--- Tool: validate_ticker called for: {ticker} ---")
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        if not info or 'symbol' not in info:
            return {
                "status": "error",
                "error_message": f"'{ticker}' is not a valid ticker symbol."
            }
        
        company_name = info.get('longName', info.get('shortName', ticker))
        print(f"--- Tool: Validated ticker: {ticker} ({company_name}) ---")
        
        return {
            "status": "success",
            "ticker": ticker.upper(),
            "company_name": company_name,
            "is_valid": True
        }
        
    except Exception as e:
        print(f"--- Tool: Error validating ticker: {str(e)} ---")
        return {
            "status": "error",
            "error_message": f"Error validating ticker '{ticker}': {str(e)}"
        }
