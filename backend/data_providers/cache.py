import time

CACHE = {}
TTL = 60  # seconds

def cache_get(key):
    """Return cached value if not expired."""
    if key in CACHE:
        value, timestamp = CACHE[key]
        if time.time() - timestamp < TTL:
            return value
    return None

def cache_set(key, value):
    """Store value in cache with timestamp."""
    CACHE[key] = (value, time.time())
