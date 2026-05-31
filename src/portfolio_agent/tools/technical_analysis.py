"""Tools for technical analysis calculations."""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
from portfolio_agent.models.analysis import TechnicalIndicators


def calculate_moving_averages(price_data: List[Dict]) -> dict:
    """
    Calculates Simple Moving Averages (SMA) and Exponential Moving Averages (EMA).
    
    Args:
        price_data: List of dicts with 'date' and 'close' prices
    
    Returns:
        dict: Dictionary with calculated moving averages
    """
    print(f"--- Tool: calculate_moving_averages called with {len(price_data)} data points ---")
    
    try:
        if not price_data:
            return {"status": "error", "error_message": "No price data provided"}
        
        df = pd.DataFrame(price_data)
        df['close'] = pd.to_numeric(df['close'])
        
        # Calculate SMAs
        sma_20 = df['close'].rolling(window=20).mean().iloc[-1] if len(df) >= 20 else None
        sma_50 = df['close'].rolling(window=50).mean().iloc[-1] if len(df) >= 50 else None
        sma_200 = df['close'].rolling(window=200).mean().iloc[-1] if len(df) >= 200 else None
        
        # Calculate EMAs
        ema_12 = df['close'].ewm(span=12, adjust=False).mean().iloc[-1] if len(df) >= 12 else None
        ema_26 = df['close'].ewm(span=26, adjust=False).mean().iloc[-1] if len(df) >= 26 else None
        
        result = {
            "sma_20": float(sma_20) if sma_20 is not None and not pd.isna(sma_20) else None,
            "sma_50": float(sma_50) if sma_50 is not None and not pd.isna(sma_50) else None,
            "sma_200": float(sma_200) if sma_200 is not None and not pd.isna(sma_200) else None,
            "ema_12": float(ema_12) if ema_12 is not None and not pd.isna(ema_12) else None,
            "ema_26": float(ema_26) if ema_26 is not None and not pd.isna(ema_26) else None,
        }
        
        print(f"--- Tool: Calculated moving averages ---")
        return {"status": "success", "data": result}
        
    except Exception as e:
        print(f"--- Tool: Error calculating moving averages: {str(e)} ---")
        return {"status": "error", "error_message": f"Error calculating moving averages: {str(e)}"}


def calculate_rsi(price_data: List[Dict], period: int = 14) -> dict:
    """
    Calculates Relative Strength Index (RSI).
    
    Args:
        price_data: List of dicts with 'date' and 'close' prices
        period: RSI period (default 14)
    
    Returns:
        dict: Dictionary with RSI value
    """
    print(f"--- Tool: calculate_rsi called with {len(price_data)} data points ---")
    
    try:
        if not price_data or len(price_data) < period + 1:
            return {"status": "error", "error_message": f"Insufficient data for RSI calculation (need {period + 1} points)"}
        
        df = pd.DataFrame(price_data)
        df['close'] = pd.to_numeric(df['close'])
        
        # Calculate price changes
        delta = df['close'].diff()
        
        # Separate gains and losses
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        # Calculate RS and RSI
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        current_rsi = float(rsi.iloc[-1])
        
        print(f"--- Tool: Calculated RSI = {current_rsi:.2f} ---")
        return {
            "status": "success",
            "data": {"rsi": current_rsi if not pd.isna(current_rsi) else None}
        }
        
    except Exception as e:
        print(f"--- Tool: Error calculating RSI: {str(e)} ---")
        return {"status": "error", "error_message": f"Error calculating RSI: {str(e)}"}


def calculate_macd(price_data: List[Dict]) -> dict:
    """
    Calculates MACD (Moving Average Convergence Divergence).
    
    Args:
        price_data: List of dicts with 'date' and 'close' prices
    
    Returns:
        dict: Dictionary with MACD, signal, and histogram values
    """
    print(f"--- Tool: calculate_macd called with {len(price_data)} data points ---")
    
    try:
        if not price_data or len(price_data) < 26:
            return {"status": "error", "error_message": "Insufficient data for MACD calculation (need 26+ points)"}
        
        df = pd.DataFrame(price_data)
        df['close'] = pd.to_numeric(df['close'])
        
        # Calculate EMAs
        ema_12 = df['close'].ewm(span=12, adjust=False).mean()
        ema_26 = df['close'].ewm(span=26, adjust=False).mean()
        
        # Calculate MACD line
        macd_line = ema_12 - ema_26
        
        # Calculate signal line (9-day EMA of MACD)
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        
        # Calculate histogram
        histogram = macd_line - signal_line
        
        result = {
            "macd": float(macd_line.iloc[-1]) if not pd.isna(macd_line.iloc[-1]) else None,
            "macd_signal": float(signal_line.iloc[-1]) if not pd.isna(signal_line.iloc[-1]) else None,
            "macd_histogram": float(histogram.iloc[-1]) if not pd.isna(histogram.iloc[-1]) else None,
        }
        
        print(f"--- Tool: Calculated MACD indicators ---")
        return {"status": "success", "data": result}
        
    except Exception as e:
        print(f"--- Tool: Error calculating MACD: {str(e)} ---")
        return {"status": "error", "error_message": f"Error calculating MACD: {str(e)}"}


def identify_support_resistance(price_data: List[Dict]) -> dict:
    """
    Identifies support and resistance levels based on recent price action.
    
    Args:
        price_data: List of dicts with 'date', 'high', 'low', 'close' prices
    
    Returns:
        dict: Dictionary with support and resistance levels
    """
    print(f"--- Tool: identify_support_resistance called with {len(price_data)} data points ---")
    
    try:
        if not price_data or len(price_data) < 20:
            return {"status": "error", "error_message": "Insufficient data for support/resistance calculation"}
        
        df = pd.DataFrame(price_data)
        df['high'] = pd.to_numeric(df['high'])
        df['low'] = pd.to_numeric(df['low'])
        df['close'] = pd.to_numeric(df['close'])
        
        # Simple approach: use recent highs and lows
        recent_high = df['high'].tail(30).max()
        recent_low = df['low'].tail(30).min()
        
        # Support: 20-day low
        support = float(recent_low)
        
        # Resistance: 20-day high
        resistance = float(recent_high)
        
        result = {
            "support_level": support,
            "resistance_level": resistance,
        }
        
        print(f"--- Tool: Identified support: ${support:.2f}, resistance: ${resistance:.2f} ---")
        return {"status": "success", "data": result}
        
    except Exception as e:
        print(f"--- Tool: Error identifying support/resistance: {str(e)} ---")
        return {"status": "error", "error_message": f"Error identifying support/resistance: {str(e)}"}


def get_comprehensive_technical_indicators(ticker: str, price_data: List[Dict]) -> dict:
    """
    Calculates comprehensive technical indicators for a stock.
    
    Args:
        ticker: Stock ticker symbol
        price_data: List of dicts with price history
    
    Returns:
        dict: Dictionary with comprehensive TechnicalIndicators
    """
    print(f"--- Tool: get_comprehensive_technical_indicators called for {ticker} ---")
    
    try:
        # Calculate all indicators
        ma_result = calculate_moving_averages(price_data)
        rsi_result = calculate_rsi(price_data)
        macd_result = calculate_macd(price_data)
        sr_result = identify_support_resistance(price_data)
        
        # Combine results
        indicators = {
            "ticker": ticker.upper(),
            **(ma_result.get("data", {}) if ma_result.get("status") == "success" else {}),
            **(rsi_result.get("data", {}) if rsi_result.get("status") == "success" else {}),
            **(macd_result.get("data", {}) if macd_result.get("status") == "success" else {}),
            **(sr_result.get("data", {}) if sr_result.get("status") == "success" else {}),
        }
        
        # Determine trend based on moving averages
        current_price = price_data[-1]['close'] if price_data else None
        if current_price and indicators.get('sma_50') and indicators.get('sma_200'):
            if current_price > indicators['sma_50'] > indicators['sma_200']:
                indicators['trend'] = "bullish"
            elif current_price < indicators['sma_50'] < indicators['sma_200']:
                indicators['trend'] = "bearish"
            else:
                indicators['trend'] = "neutral"
        
        # Create TechnicalIndicators model
        technical_indicators = TechnicalIndicators(**indicators)
        
        print(f"--- Tool: Compiled comprehensive technical indicators for {ticker} ---")
        return {
            "status": "success",
            "data": technical_indicators.model_dump()
        }
        
    except Exception as e:
        print(f"--- Tool: Error getting comprehensive technical indicators: {str(e)} ---")
        return {
            "status": "error",
            "error_message": f"Error calculating comprehensive technical indicators: {str(e)}"
        }
