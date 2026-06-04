"""Utilities for yfinance API interactions."""

import yfinance as yf
import requests
from typing import Optional
import logging

# Configure default timeouts (connect_timeout, read_timeout)
DEFAULT_TIMEOUT = (5, 30)  # 5 seconds to connect, 30 seconds to read


def create_yf_ticker(ticker: str, timeout: Optional[tuple] = None) -> yf.Ticker:
    """
    Create a yfinance Ticker with configured timeout.
    
    Args:
        ticker: Stock ticker symbol
        timeout: Tuple of (connect_timeout, read_timeout) in seconds
                 Default: (5, 30)
    
    Returns:
        yf.Ticker: Configured ticker object with timeout
    """
    timeout = timeout or DEFAULT_TIMEOUT
    
    # Create custom session with timeout
    session = requests.Session()
    
    # Monkey-patch the request method to add timeout
    original_request = session.request
    
    def request_with_timeout(*args, **kwargs):
        """Wrapper that adds timeout to all requests."""
        kwargs.setdefault('timeout', timeout)
        return original_request(*args, **kwargs)
    
    session.request = request_with_timeout
    
    # Create ticker with custom session
    try:
        stock = yf.Ticker(ticker, session=session)
        logging.debug(f"Created yfinance Ticker for {ticker} with timeout {timeout}")
        return stock
    except Exception as e:
        logging.error(f"Failed to create Ticker for {ticker}: {e}")
        raise
