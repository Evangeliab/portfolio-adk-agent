"""Retry utilities for external API calls."""

from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
    before_sleep_log
)
import logging

# Configure retry for yfinance API calls
yfinance_retry = retry(
    # Retry on common network/API errors
    retry=retry_if_exception_type((
        ConnectionError,
        TimeoutError,
        OSError,  # Network errors
    )),
    # Stop after 3 attempts
    stop=stop_after_attempt(3),
    # Exponential backoff: 2^x * 1 seconds, min 2s, max 10s
    wait=wait_exponential(multiplier=1, min=2, max=10),
    # Log before sleeping
    before_sleep=before_sleep_log(logging.getLogger(__name__), logging.WARNING),
    # Re-raise the exception after all retries exhausted
    reraise=True
)
