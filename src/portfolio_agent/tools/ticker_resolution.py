"""Tools for resolving company names to stock ticker symbols using yfinance search."""

import yfinance as yf

# Common company name to ticker mappings for quick resolution without API calls
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
                try:
                    # Retrieve the cached ticker info
                    stock = yf.Ticker(ticker)
                    info = stock.info
                    company_name = info.get('longName', info.get('shortName', ticker))
                except:
                    company_name = ticker
                print(f"--- Tool: Found in common mappings: {ticker} ({company_name}) ---")
                return {
                    "status": "success",
                    "ticker": ticker,
                    "company_name": company_name,
                    "confidence": 0.95,
                    "alternatives": []
                }
        
        # Use native yfinance search for fallback
        print(f"--- Tool: Querying yf.Search for '{query_lower}' ---")
        search = yf.Search(query_lower)
        if search.quotes:
            best_match = search.quotes[0]
            ticker = best_match.get("symbol")
            company_name = best_match.get("shortname", best_match.get("longname", best_match.get("symbol")))
            
            # Extract alternatives
            alternatives = []
            for q in search.quotes[1:5]:
                if "symbol" in q:
                    alternatives.append({
                        "ticker": q["symbol"],
                        "company_name": q.get("shortname", q.get("longname", q["symbol"])),
                        "confidence": 0.8
                    })
            
            print(f"--- Tool: Found match via yf.Search: {ticker} ({company_name}) ---")
            return {
                "status": "success",
                "ticker": ticker,
                "company_name": company_name,
                "confidence": 0.9,
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
