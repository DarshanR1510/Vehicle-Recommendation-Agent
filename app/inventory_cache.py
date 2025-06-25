import json
import time
import pandas as pd
from vehicle_inventory import generate_synthetic_inventory

class InventoryCache:
    """
    Sophisticated caching system for inventory data management

    Features:
    - Lazy loading with automatic refresh
    - Memory -efficient data storage
    - Cache invalidation strategies
    - Performance monitoring
    """

    def __init__(self):
        self._cache = None
        self._last_loaded = None
        self._cache_duration = 86400 # 1 day cache lifetime

    def get_inventory(self):
        """
        Intelligent cache management with automatic refresh
        """
        current_time = time.time()

        # Check if cache needs refresh
        if (self._cache is None or
            self._last_loaded is None or
            current_time - self._last_loaded > self._cache_duration):
            self._refresh_cache ()

        return self._cache

    def _refresh_cache(self):
        """ Load and cache inventory data """
        try:
            with open('data/synthetic_inventory.json', 'r') as f:
                inventory_data = json.load(f)

            self._cache = pd.DataFrame(inventory_data)
            self._last_loaded = time.time()

            print(f"Cache refreshed: {len(self._cache)} vehicles loaded")

        except Exception as e:
            print(f"Cache refresh failed: {e}")
            if self._cache is None:
                # Fallback to synthetic data generation
                self._generate_fallback_data ()

    def _generate_fallback_data(self):
        """ Emergency fallback data generation """
        inventory_data = generate_synthetic_inventory ()
        self._cache = pd.DataFrame(inventory_data)
        self._last_loaded = time.time()

# Global cache instance

inventory_cache = InventoryCache ()

# To refresh the cache and get the inventory manually
# inventory_cache._refresh_cache()
# print(inventory_cache.get_inventory())
