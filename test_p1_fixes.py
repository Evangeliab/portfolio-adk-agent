"""Test P1 critical fixes - RSI edge cases and basic functionality."""

import time
import pytest
from portfolio_agent.tools.technical_analysis import calculate_rsi
from portfolio_agent.tools.cache_utils import ttl_cache


class TestRSIEdgeCases:
    """Test RSI calculation handles edge cases correctly."""
    
    def test_rsi_all_gains(self):
        """Test RSI calculation with all gains (should return 100, not crash)."""
        all_gains = [{"date": f"2024-01-{i:02d}", "close": 100 + i} for i in range(1, 20)]
        result = calculate_rsi(all_gains)
        assert result["status"] == "success", f"Expected success, got {result}"
        assert result["data"]["rsi"] == 100.0, f"Expected RSI=100, got {result['data']['rsi']}"

    def test_rsi_all_losses(self):
        """Test RSI calculation with all losses (should return 0, not crash)."""
        all_losses = [{"date": f"2024-01-{i:02d}", "close": 100 - i} for i in range(1, 20)]
        result = calculate_rsi(all_losses)
        assert result["status"] == "success", f"Expected success, got {result}"
        assert result["data"]["rsi"] == 0.0, f"Expected RSI=0, got {result['data']['rsi']}"

    def test_rsi_no_movement(self):
        """Test RSI calculation with no price movement (should return 50)."""
        no_movement = [{"date": f"2024-01-{i:02d}", "close": 100} for i in range(1, 20)]
        result = calculate_rsi(no_movement)
        assert result["status"] == "success", f"Expected success, got {result}"
        assert result["data"]["rsi"] == 50.0, f"Expected RSI=50, got {result['data']['rsi']}"

    def test_rsi_normal_case(self):
        """Test RSI with normal mixed gains/losses."""
        normal_prices = [
            {"date": "2024-01-01", "close": 100},
            {"date": "2024-01-02", "close": 102},
            {"date": "2024-01-03", "close": 101},
            {"date": "2024-01-04", "close": 103},
            {"date": "2024-01-05", "close": 102},
            {"date": "2024-01-06", "close": 104},
            {"date": "2024-01-07", "close": 103},
            {"date": "2024-01-08", "close": 105},
            {"date": "2024-01-09", "close": 104},
            {"date": "2024-01-10", "close": 106},
            {"date": "2024-01-11", "close": 105},
            {"date": "2024-01-12", "close": 107},
            {"date": "2024-01-13", "close": 106},
            {"date": "2024-01-14", "close": 108},
            {"date": "2024-01-15", "close": 107},
        ]
        result = calculate_rsi(normal_prices)
        assert result["status"] == "success", f"Expected success, got {result}"
        assert 0 <= result["data"]["rsi"] <= 100, f"RSI out of range: {result['data']['rsi']}"

    def test_rsi_insufficient_data(self):
        """Test RSI returns error with insufficient data."""
        insufficient_data = [{"date": f"2024-01-{i:02d}", "close": 100 + i} for i in range(1, 5)]
        result = calculate_rsi(insufficient_data, period=14)
        assert result["status"] == "error", f"Expected error with insufficient data, got {result}"
        assert "Insufficient data" in result["error_message"]

    def test_rsi_invalid_data(self):
        """Test RSI handles non-numeric data gracefully."""
        invalid_data = [{"date": f"2024-01-{i:02d}", "close": "invalid"} for i in range(1, 20)]
        result = calculate_rsi(invalid_data)
        assert result["status"] == "error", f"Expected error with invalid data, got {result}"


class TestTTLCache:
    """Test TTL cache functionality."""
    
    def test_cache_hit(self):
        """Test cache returns cached value on second call."""
        call_count = 0
        
        @ttl_cache(seconds=10, maxsize=10)
        def test_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # First call - should execute
        result1 = test_func(5)
        assert result1 == 10
        assert call_count == 1
        
        # Second call - should hit cache
        result2 = test_func(5)
        assert result2 == 10
        assert call_count == 1  # No new execution

    def test_cache_expiry(self):
        """Test cache expires after TTL."""
        call_count = 0
        
        @ttl_cache(seconds=1, maxsize=10)
        def test_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # First call
        result1 = test_func(10)
        assert result1 == 20
        assert call_count == 1
        
        # Wait for expiry
        time.sleep(1.1)
        
        # Second call - cache expired, should execute again
        result2 = test_func(10)
        assert result2 == 20
        assert call_count == 2

    def test_cache_different_args(self):
        """Test cache distinguishes between different arguments."""
        call_count = 0
        
        @ttl_cache(seconds=10, maxsize=10)
        def test_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        result1 = test_func(5)
        result2 = test_func(10)
        
        assert result1 == 10
        assert result2 == 20
        assert call_count == 2  # Both executed

    def test_cache_max_size(self):
        """Test cache evicts oldest entry when full."""
        call_count = 0
        
        @ttl_cache(seconds=10, maxsize=2)
        def test_func(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        # Fill cache
        test_func(1)
        test_func(2)
        assert call_count == 2
        
        # This should evict the first entry
        test_func(3)
        assert call_count == 3
        
        # Calling with 1 again should execute (was evicted)
        test_func(1)
        assert call_count == 4
