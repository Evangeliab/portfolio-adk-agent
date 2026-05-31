"""Tools for news search using Google Search grounding."""

from typing import Optional


def search_company_news(company_name: str, ticker: str, days: int = 30) -> str:
    """
    Searches for recent news about a company using Google Search.
    This tool is designed to work with ADK's Google Search grounding capability.
    
    Note: The actual Google Search grounding is configured at the agent level.
    This tool provides the search query construction and returns guidance
    for the LLM to analyze search results.
    
    Args:
        company_name (str): Full company name (e.g., "Apple Inc.")
        ticker (str): Stock ticker symbol (e.g., "AAPL")
        days (int): Number of days to look back for news (default 30)
    
    Returns:
        str: Search query string that will be used with Google Search grounding.
             The LLM will receive actual search results and analyze them.
    """
    print(f"--- Tool: search_company_news called for {company_name} ({ticker}) ---")
    
    # Construct an effective search query for Google Search grounding
    # The query should be specific enough to get relevant financial news
    search_query = (
        f"{company_name} {ticker} stock news analysis recent developments "
        f"financial performance earnings market sentiment"
    )
    
    print(f"--- Tool: Constructed search query for Google Search grounding ---")
    print(f"--- Search Query: {search_query} ---")
    
    # Return the search query
    # When used with Google Search grounding, the LLM will:
    # 1. Use this query to search Google
    # 2. Receive actual search results
    # 3. Analyze the results for sentiment and key themes
    # 4. Return structured analysis
    
    return search_query


def analyze_news_sentiment_from_results(search_results: str, company_name: str, ticker: str) -> str:
    """
    Provides guidance for analyzing news sentiment from Google Search results.
    This is a helper tool that returns instructions for the LLM.
    
    Args:
        search_results (str): Search results from Google (provided by grounding)
        company_name (str): Company name
        ticker (str): Ticker symbol
    
    Returns:
        str: Instructions for the LLM to analyze the search results
    """
    print(f"--- Tool: analyze_news_sentiment_from_results called for {ticker} ---")
    
    instructions = f"""
    Analyze the following search results about {company_name} ({ticker}) and provide:
    
    1. Overall Sentiment (positive, negative, neutral, or mixed)
    2. Sentiment Score (-1.0 to 1.0, where -1 is very negative, 0 is neutral, 1 is very positive)
    3. Key Themes (main topics from the news)
    4. Positive Developments (bullish news or positive factors)
    5. Negative Developments (bearish news or concerns)
    6. News Summary (comprehensive summary of recent news sentiment)
    
    Focus on:
    - Financial performance and earnings
    - Product launches or innovations
    - Management changes
    - Market share and competition
    - Regulatory issues or legal matters
    - Analyst ratings and price target changes
    - Industry trends affecting the company
    
    Search Results to Analyze:
    {search_results}
    
    Provide a structured analysis in the format of the NewsSentiment model.
    """
    
    return instructions
