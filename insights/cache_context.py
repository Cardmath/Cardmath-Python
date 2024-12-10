from database.auth.user import User, Onboarding
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Dict, Tuple, Union
import time

class PurchaseCache:
    def __init__(self, cache_ttl_seconds: int = 3600):
        self._cache = {}
        self._cache_ttl = cache_ttl_seconds
    
    def _get_cache_key(self, user) -> str:
        current_month = datetime.now().strftime("%Y-%m")
        return f"{user.id}:{current_month}"
    
    async def get_cached_purchases(
        self,
        user: Union[User, Onboarding],
        db: Session,
        compute_func
    ) -> Tuple[Dict[str, float], float]:
        cache_key = self._get_cache_key(user)
        
        if cache_key in self._cache:
            cached_data, timestamp = self._cache[cache_key]
            if time.time() - timestamp < self._cache_ttl:
                print(f"[INFO] Returning cached result for user {user.id}")
                return cached_data
            else:
                del self._cache[cache_key]
        
        result = await compute_func(user, db)
        self._cache[cache_key] = (result, time.time())
        return result
    
    def clear(self):
        self._cache.clear()

class CacheContext:
    _cache = None
    
    @classmethod
    def initialize(cls, cache_ttl_seconds: int = 3600):
        if cls._cache is not None:
            print("[WARNING] Cache already initialized")
            return
        cls._cache = PurchaseCache(cache_ttl_seconds)
        print("[INFO] Cache initialized")
    
    @classmethod
    def get_cache(cls) -> PurchaseCache:
        if cls._cache is None:
            raise RuntimeError("Cache not initialized. Call CacheContext.initialize() first")
        return cls._cache
    
    @classmethod
    def clear(cls):
        if cls._cache is not None:
            cls._cache.clear()
            print("[INFO] Cache cleared")
