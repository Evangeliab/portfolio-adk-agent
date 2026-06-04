"""Caching utilities with TTL support."""

import time
import functools
from typing import Any, Callable, Optional
import logging


def ttl_cache(seconds: int = 300, maxsize: int = 128):
    """
    Time-To-Live cache decorator.
    
    Caches function results for a specified time period. After expiry,
    the function is re-executed and cache is updated.
    
    Args:
        seconds: Cache TTL in seconds (default: 300 = 5 minutes)
        maxsize: Maximum cache size (default: 128)
    
    Returns:
        Decorator function
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        cache_order = []  # Track insertion order for LRU eviction
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from args and kwargs
            key = str(args) + str(sorted(kwargs.items()))
            
            now = time.time()
            
            # Check if key exists and is not expired
            if key in cache:
                result, timestamp = cache[key]
                age = now - timestamp
                
                if age < seconds:
                    # Cache hit - return cached result
                    logging.debug(f"Cache HIT for {func.__name__}{args} (age: {age:.1f}s)")
                    return result
                else:
                    # Cache expired - remove from cache
                    logging.debug(f"Cache EXPIRED for {func.__name__}{args} (age: {age:.1f}s)")
                    del cache[key]
                    cache_order.remove(key)
            
            # Cache miss or expired - execute function
            logging.debug(f"Cache MISS for {func.__name__}{args}")
            result = func(*args, **kwargs)
            
            # Store in cache
            cache[key] = (result, now)
            cache_order.append(key)
            
            # Evict oldest entry if cache is full
            if len(cache) > maxsize:
                oldest_key = cache_order.pop(0)
                del cache[oldest_key]
                logging.debug(f"Cache EVICTED {oldest_key} (cache full)")
            
            return result
        
        # Add cache management methods
        def clear_cache():
            """Clear all cached entries."""
            cache.clear()
            cache_order.clear()
            logging.info(f"Cache cleared for {func.__name__}")
        
        def cache_info():
            """Get cache statistics."""
            return {
                'size': len(cache),
                'maxsize': maxsize,
                'ttl': seconds,
                'keys': list(cache_order)
            }
        
        wrapper.clear_cache = clear_cache
        wrapper.cache_info = cache_info
        
        return wrapper
    
    return decorator
